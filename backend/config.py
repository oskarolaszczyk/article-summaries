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
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    CORS_HEADERS = ["Authorization", "Content-Type"]


class DevConfig(Config):
    FLASK_ENV = "development"
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class TestConfig(Config):
    FLASK_ENV = "testing"
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"
    
