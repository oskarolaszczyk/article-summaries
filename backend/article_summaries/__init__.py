from flask import Flask
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DevConfig")

    jwt = JWTManager(app)

    from article_summaries.apps.core.views import core_bp

    app.register_blueprint(core_bp)

    return app
