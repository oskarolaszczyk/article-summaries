import enum
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UserType(enum.Enum):
    ADMIN = 1
    USER = 2


class ModelType(enum.Enum):
    MEANINGCLOUD = 1
    OUR_MODEL = 2


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    type = db.Column(db.Enum(UserType), default=UserType.USER, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    source_url = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    
class Summary(db.Model):
    __tablename__ = 'summaries'
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Boolean, nullable=True)
    model_type = db.Column(db.Enum(ModelType), nullable=False)
    date_generated = db.Column(db.DateTime, default=datetime.utcnow())