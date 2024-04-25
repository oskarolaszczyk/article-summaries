from flask import Flask
from flask_jwt_extended import JWTManager
from article_summaries.models import db

jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DevConfig")

    db.init_app(app)
    jwt.init_app(app)

    from article_summaries.apps.core.views import core_bp

    app.register_blueprint(core_bp)

    return app
