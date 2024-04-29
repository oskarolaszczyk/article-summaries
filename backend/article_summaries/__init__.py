from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from article_summaries.models import db, User, UserType
from article_summaries.apps.auth.blocklist import BLOCKLIST

jwt = JWTManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DevConfig")

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app, origins="*")

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.additional_claims_loader
    def user_type_claims(identity):
        user = User.query.filter_by(id=identity).first()
        if user.type == UserType.ADMIN:
            return {"is_admin": True}
        return {"is_admin": False}

    from article_summaries.apps.core.views import core_bp
    from article_summaries.apps.auth.views import auth_bp

    app.register_blueprint(core_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app
