import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "uploaded_files"
)
ALLOWED_EXTENSIONS = {"pdf"}

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
    result = {"message": "Easyrag started!"}
    # TODO forward to back-end, the source folder for PDFs becomes ./uploaded_files
    return jsonify(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    easyrag_flask_app.run(debug=True, host="0.0.0.0", port=port)
