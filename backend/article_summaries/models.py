import enum
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UserType(enum.Enum):
    ADMIN = 1
    USER = 2


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    type = db.Column(db.Enum(UserType), default=UserType.USER, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
