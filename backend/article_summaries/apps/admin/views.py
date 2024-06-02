from functools import wraps
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from article_summaries.models import db, Summary, Article, User, UserType

admin_bp = Blueprint(
    "admin_bp", __name__, template_folder="templates", static_folder="static"
)


def admin_permissions(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        is_admin = current_user.type == UserType.ADMIN
        if not is_admin:
            return jsonify({"error": "Admin privileges required!"}), 403
        return f(*args, **kwargs)

    return decorated


@admin_bp.route("/users", methods=["GET"])
@jwt_required()
@admin_permissions
def get_all_users():
    users = User.query.all()
    if not users:
        return jsonify({"message": "No users in database"}), 200
    res = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "type": user.type.name,
            "created_on": user.created_on,
        }
        for user in users
    ]
    return jsonify(res), 200


@admin_bp.route("/articles", methods=["GET"])
@jwt_required()
@admin_permissions
def get_all_articles():
    articles = Article.query.all()
    print(articles)
    if not articles:
        return jsonify({"error": "No articles found in database"}), 200
    res = [
        {
            "id": article.id,
            "user_id": article.user_id,
            "title": article.title,
            "source_url": article.source_url,
            "date_added": article.date_added,
        }
        for article in articles
    ]
    return jsonify(res), 200


@admin_bp.route("/summaries", methods=["GET"])
@jwt_required()
@admin_permissions
def get_article_summaries():
    summaries = Summary.query.all()
    if not summaries:
        return jsonify({"error": "No summaries found in database"}), 200
    res = [
        {
            "id": summary.id,
            "article_id": summary.article_id,
            "content": summary.content,
            "rating": summary.rating,
            "model_type": summary.model_type.name,
            "date_generated": summary.date_generated,
        }
        for summary in summaries
    ]
    return jsonify(res), 200
