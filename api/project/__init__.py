import os, subprocess
from pathlib import Path
from flask import Flask, jsonify, send_from_directory, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_cors import CORS
from sqlalchemy.dialects.postgresql import insert

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
CORS(app, resources={r"/api/*": {"origins": app.config["APP_URL"]}})

class Shapefile(db.Model):
    __tablename__ = "shapefiles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique = True)
    table = db.Column(db.String(128), nullable=False)

    def __init__(self, name, table):
        self.name = name
        self.table = table

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            'table': self.table,
        }

@app.route("/")
def hello_world():
    return jsonify(hello="world")

@app.route("/data/<path:filename>")
def mediafiles(filename):
    return send_from_directory(app.config["DATA_FOLDER"], filename)


@app.route("/api/shapefiles", methods=["GET", "POST"])
def shapefiles():
    shps = []
    data = {}
    for s in Shapefile.query.all():
        shps.append(s.serialize)
        data[s.table] = [{'id': row.ogc_fid, 'geom': row.geometry} for row in db.engine.execute(f'select ogc_fid, ST_AsEWKT(ST_Transform(wkb_geometry, 4326)) as geometry from "{s.table}"')]
    response = {'shapefiles': shps, 'data': data}
    return jsonify(**response)

@app.route("/api/upload", methods=["GET", "POST"])
def upload_files():
    files = request.files.getlist("shapefile[]")
    for file in files:
        file.save(os.path.join(app.config["DATA_FOLDER"], secure_filename(file.filename)))
    name = request.form.get('name')
    try:
        result = subprocess.check_output([app.config["IMPORT_STRING"].format(f"project/data/{name}")], shell=True)
        values = {'name': name, 'table': Path(f"{app.config['DATA_FOLDER']}/{name}").stem.lower() }
        query = insert(Shapefile).values(**values).on_conflict_do_nothing(index_elements=[Shapefile.name])
        db.session.execute(query)
        db.session.commit()
    except subprocess.CalledProcessError as e:
        return jsonify(error="An error occurred while trying to store shapefile.")

    return jsonify(uploaded=[file.filename for file in files], import_string='%s'%result)

