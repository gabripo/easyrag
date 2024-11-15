import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import sys
import shutil

curr_dir = os.path.dirname(__file__)
root_dir = os.path.abspath(os.path.join(curr_dir, ".."))
sys.path.append(root_dir)
from ollama_manager import download_model
import process_handler
import streamlit_settings

UPLOAD_FOLDER = os.path.abspath(os.path.join(curr_dir, "uploaded_files"))
ALLOWED_EXTENSIONS = {"pdf"}
RAG_FOLDER_NAME = "chroma_data"
DEFAULT_SYSTEM_PROMPT = "You got some documents.\nReply to questions concerning them."

easyrag_flask_app = Flask(__name__)
easyrag_flask_app.config["SECRET_KEY"] = "supersecretkey"
easyrag_flask_app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
easyrag_flask_app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS

if not os.path.exists(easyrag_flask_app.config["UPLOAD_FOLDER"]):
    os.makedirs(easyrag_flask_app.config["UPLOAD_FOLDER"])


@easyrag_flask_app.route("/")
def upload_file_form():
    return render_template("upload.html")


@easyrag_flask_app.route("/upload", methods=["POST"])
def upload_file():
    if "files[]" not in request.files:
        return redirect(request.url)

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

    data_folder_content = os.listdir(user_options_flask["data_folder"])
    data_folder_files = [
        file
        for file in data_folder_content
        if os.path.isfile(os.path.join(user_options_flask["data_folder"], file))
    ]
    if len(data_folder_files) == 0:
        # back to roots
        data_folder = user_options_flask["data_folder"]
        print(f"No valid files in folder {data_folder}!")
        return {"nextpage": "/"}

    streamlit_settings.write_streamlit_secrets(user_options_flask)
    streamlit_script = "web_interface_chat.py"
    streamlit_cmd = f"streamlit run --server.port {os.getenv('STREAMLIT_PORT', '8501')} " + streamlit_script
    streamlit_pid = process_handler.execute_command_and_get_pid(streamlit_cmd)

    return {"nextpage": f"/streamlit-kill/{streamlit_pid}"}


@easyrag_flask_app.route("/streamlit-kill/<streamlit_pid>", methods=["GET", "POST"])
def kill_streamlit(streamlit_pid):
    if request.method == "POST":
        if streamlit_pid.isnumeric():
            streamlit_pid_num = int(streamlit_pid)
            process_handler.kill_process_by_pid(streamlit_pid_num)
        # coming back where all started...
        return {"nextsite": "/"}
    return render_template("streamlit_kill.html", pid=streamlit_pid)


@easyrag_flask_app.route("/clear-data", methods=["POST"])
def delete_files_on_server():
    for file in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    return {"nextpage": "/", "message": "Previously uploaded files have been deleted!"}


@easyrag_flask_app.route("/download-llm", methods=["POST"])
def download_llm():
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        json_data = request.get_json()
    else:
        return jsonify({"message": "Data from front-end is not JSON!"})

    llm_name = json_data.get("selected-llm", "")
    success = download_model(llm_name)
    if success:
        return {"nextpage": "/", "message": f"Model {llm_name} has been downloaded!"}
    else:
        return {
            "nextpage": "/",
            "message": f"Error while downloading the model {llm_name}!",
        }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    easyrag_flask_app.run(debug=True, host="0.0.0.0", port=port)
