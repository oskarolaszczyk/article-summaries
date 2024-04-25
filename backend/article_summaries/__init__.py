from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DevConfig")

    from article_summaries.apps.core.views import core_bp

    app.register_blueprint(core_bp)

    return app
