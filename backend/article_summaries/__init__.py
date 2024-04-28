from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from article_summaries.models import db, User, UserType

jwt = JWTManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DevConfig")

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app, origins="http://localhost:3000")

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()

    @jwt.additional_claims_loader
    def user_type_claims(identity):
        if identity.type == UserType.ADMIN:
            return {"is_admin": True}
        return {"is_admin": False}

    from article_summaries.apps.core.views import core_bp
    from article_summaries.apps.auth.views import auth_bp

    app.register_blueprint(core_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
