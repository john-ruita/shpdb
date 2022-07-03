import os
from flask import Flask, jsonify, send_from_directory, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)

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


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    file = request.files["file"]
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config["ZIP_FOLDER"], filename))
    return jsonify(uploaded=filename)

