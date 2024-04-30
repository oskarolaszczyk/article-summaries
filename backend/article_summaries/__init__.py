from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from article_summaries.models import db, User, UserType
from article_summaries.apps.auth.blocklist import BLOCKLIST
from flask_migrate import Migrate

jwt = JWTManager()
bcrypt = Bcrypt()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DevConfig")

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins="http://localhost:3000")

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.additional_claims_loader
    def user_type_claims(identity):
        user = User.query.filter_by(id=identity).first()
        if user.type == UserType.ADMIN:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback():
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "message": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback():
        return (
            jsonify(
                {"message": "The token is not fresh.", "error": "fresh_token_required"}
            ),
            401,
        )

    @jwt.revoked_token_loader
    def revoked_token_callback():
        return (
            jsonify(
                {"message": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    from article_summaries.apps.core.views import core_bp
    from article_summaries.apps.auth.views import auth_bp
    from article_summaries.apps.summary.views import summary_bp
    from article_summaries.apps.article.views import article_bp

    app.register_blueprint(core_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(summary_bp, url_prefix="/summary")
    app.register_blueprint(article_bp, url_prefix="/article")

    return app
