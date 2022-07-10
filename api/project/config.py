import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATA_FOLDER = f"{os.getenv('APP_FOLDER')}/project/data"
    APP_URL = os.getenv('APP_URL')
    IMPORT_STRING = os.getenv('IMPORT_STRING')
