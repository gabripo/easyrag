import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import sys

curr_dir = os.path.dirname(__file__)
root_dir = os.path.abspath(os.path.join(curr_dir, ".."))
sys.path.append(root_dir)
import process_handler
import streamlit_settings

UPLOAD_FOLDER = os.path.join(curr_dir, "uploaded_files")
ALLOWED_EXTENSIONS = {"pdf"}
RAG_FOLDER_NAME = "chroma_data"
DEFAULT_SYSTEM_PROMPT = "You got some documents.\nReply to questions concerning them."

easyrag_flask_app = Flask(__name__)
easyrag_flask_app.config["SECRET_KEY"] = "supersecretkey"
easyrag_flask_app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
easyrag_flask_app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS


@easyrag_flask_app.route("/")
def upload_file_form():
    return render_template("upload.html")


@easyrag_flask_app.route("/upload", methods=["POST"])
def upload_file():
    if "files[]" not in request.files:
        return redirect(request.url)

    if not os.path.exists(easyrag_flask_app.config["UPLOAD_FOLDER"]):
        os.makedirs(easyrag_flask_app.config["UPLOAD_FOLDER"])

    files = request.files.getlist("files[]")

    success_msg_list = []
    for file in files:
        if file.filename == "":
            return redirect(request.url)
        target_filename = secure_filename(file.filename)

        if file and target_filename.endswith(".pdf"):
            file_path = os.path.join(
                easyrag_flask_app.config["UPLOAD_FOLDER"], target_filename
            )
            file.save(file_path)
            success_msg_list.append(
                f"File\n{target_filename}\nuploaded successfully to\n{file_path}!\n"
            )

    return render_template("upload.html", message=success_msg_list)


@easyrag_flask_app.route("/run-easyrag", methods=["POST"])
def start_easyrag():
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        json_data = request.get_json()
    else:
        return jsonify({"message": "Data from front-end is not JSON!"})

    user_options_flask = {}
    user_options_flask["system_prompt"] = json_data.get(
        "system-prompt", DEFAULT_SYSTEM_PROMPT
    )
    user_options_flask["llm"] = json_data.get("selected-llm", "")
    user_options_flask["data_folder"] = UPLOAD_FOLDER
    user_options_flask["rag_folder"] = os.path.join(
        user_options_flask["data_folder"],
        RAG_FOLDER_NAME + "_" + user_options_flask["llm"],
    )
    user_options_flask["use_web_interface"] = True  # hardcoded, needed since no GUI!
    user_options_flask["consider_history"] = True  # hardcoded

    streamlit_settings.write_streamlit_secrets(user_options_flask)
    streamlit_script = "web_interface_chat.py"
    streamlit_cmd = "streamlit run " + streamlit_script
    streamlit_pid = process_handler.execute_command_and_get_pid(streamlit_cmd)

    result = {"message": f"Easyrag started with PID {streamlit_pid}!"}
    return jsonify(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    easyrag_flask_app.run(debug=True, host="0.0.0.0", port=port)
