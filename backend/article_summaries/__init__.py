from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from article_summaries.models import db

jwt = JWTManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DevConfig")

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app, origins="http://localhost:3000")

    from article_summaries.apps.core.views import core_bp
    from article_summaries.apps.auth.views import auth_bp
    from article_summaries.apps.summary.views import summary_bp
    from article_summaries.apps.article.views import article_bp

    app.register_blueprint(core_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(summary_bp, url_prefix="/summary")
    app.register_blueprint(article_bp, url_prefix="/article")

    return app
