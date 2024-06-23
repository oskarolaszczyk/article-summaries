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
    users = User.query.filter_by(type="USER").all()
    if not users:
        return jsonify({"message": "No users in database."}), 200
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


@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
@admin_permissions
def delete_user(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "User not found."}), 404
    
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"User id:{user_id} has been deleted."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while deleting the user.", "error": str(e)}), 500


@admin_bp.route("/articles", methods=["GET"])
@jwt_required()
@admin_permissions
def get_all_articles():
    articles = Article.query.all()
    if not articles:
        return jsonify({"error": "No articles found in database."}), 200
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

@admin_bp.route("/articles/<int:article_id>", methods=["DELETE"])
@jwt_required()
@admin_permissions
def delete_article(article_id):
    article = Article.query.get(article_id)
    if not article:
        return jsonify({"error": "Article not found."}), 404
    
    try:
        db.session.delete(article)
        db.session.commit()
        return jsonify({"message": f"Article id:{article_id} has been deleted."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while deleting the article.", "details": str(e)}), 500



@admin_bp.route("/summaries", methods=["GET"])
@jwt_required()
@admin_permissions
def get_article_summaries():
    summaries = Summary.query.all()
    if not summaries:
        return jsonify({"error": "No summaries found in database."}), 200
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

@admin_bp.route("/summaries/<int:summary_id>", methods=["DELETE"])
@jwt_required()
@admin_permissions
def delete_summary(summary_id):
    summary = Summary.query.get(summary_id)
    if not summary:
        return jsonify({"error": "Summary not found."}), 404
    
    try:
        db.session.delete(summary)
        db.session.commit()
        return jsonify({"message": f"Summary id:{summary_id} has been deleted."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while deleting the summary.", "details": str(e)}), 500
