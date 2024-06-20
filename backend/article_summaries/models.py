import enum
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from article_summaries import bcrypt

db = SQLAlchemy()


class UserType(enum.Enum):
    ADMIN = 1
    USER = 2


class ModelType(enum.Enum):
    MEANINGCLOUD = 1
    TF_IDF = 2
    LSA = 3
    LUHN = 4

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    type = db.Column(db.Enum(UserType), default=UserType.USER, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, **kwargs):  # TODO: check if there is a better way to do this
        super(User, self).__init__(**kwargs)
        password = kwargs.get("password")
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")
        if "type" not in kwargs:
            self.type = UserType.USER
        if "created_on" not in kwargs:
            self.created_on = datetime.now()


class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    source_url = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now())


class Summary(db.Model):
    __tablename__ = "summaries"
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Boolean, nullable=True)
    model_type = db.Column(db.Enum(ModelType), nullable=False)
    date_generated = db.Column(db.DateTime, default=datetime.now())
