import os, subprocess
from flask import Flask, jsonify, send_from_directory, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
CORS(app, resources={r"/api/*": {"origins": app.config["APP_URL"]}})

class Shapefile(db.Model):
    __tablename__ = "shapefiles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    def __init__(self, name):
        self.name = name

@app.route("/")
def hello_world():
    return jsonify(hello="world")

@app.route("/data/<path:filename>")
def mediafiles(filename):
    return send_from_directory(app.config["DATA_FOLDER"], filename)


@app.route("/api/upload", methods=["GET", "POST"])
def upload_files():
    files = request.files.getlist("shapefile[]")
    for file in files:
        file.save(os.path.join(app.config["DATA_FOLDER"], secure_filename(file.filename)))
    try:
        result = subprocess.check_output([app.config["IMPORT_STRING"].format(f"project/data/{request.form.get('name')}")], shell=True)
    except subprocess.CalledProcessError as e:
        return jsonify(error="An error occurred while trying to fetch task status updates.")

    return jsonify(uploaded=[file.filename for file in files], import_string='%s'%result)

