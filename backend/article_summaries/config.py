from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    FLASK_APP = "app.py"
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    TESTING = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SECRET_KEY = os.environ.get("SECRET_KEY")


class DevConfig(Config):
    FLASK_ENV = "development"
    TESTING = True
    DEBUG = True
