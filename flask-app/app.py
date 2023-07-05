import os
from flask import Flask, render_template, request, redirect, send_file 
from s3demo import list_files, download_file, upload_file
import hostinfo

app = Flask(__name__)
BUCKET="big-data-999"
UPLOAD_FOLDER = "uploads"

@app.route("/")
def home():
    return render_template("home.html", hostinfo=hostinfo.get_info())

@app.route("/storage")
def storage():
    contents = list_files("flaskdrive")
    return render_template('storage.html', contents=contents)

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        f.save(os.path.join(UPLOAD_FOLDER, f.filename))
        upload_file(f"uploads/{f.filename}", BUCKET)

        return redirect("/storage")

@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = download_file(filename, BUCKET)

        return send_file(output, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
