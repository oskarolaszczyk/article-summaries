from datetime import timedelta
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
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    CORS_HEADERS = "Content-Type"


class DevConfig(Config):
    FLASK_ENV = "development"
    TESTING = True
    DEBUG = True
