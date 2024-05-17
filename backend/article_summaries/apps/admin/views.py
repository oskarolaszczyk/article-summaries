from flask import Blueprint, jsonify, request
from article_summaries.models import db, Summary, Article, User

admin_bp = Blueprint(
    "admin_bp", __name__, template_folder="templates", static_folder="static"
)


@admin_bp.route("/users", methods=['GET'])
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
            "created_on": user.created_on
        } for user in users
    ]
    return jsonify(res), 200

@admin_bp.route("/articles", methods=['GET'])
def get_all_articles():
    articles = Article.query.all()
    if not articles:
        return jsonify({"error": "No articles found in database"}), 200
    
    res = [
        {
            "id": article.id,
            "title": article.title,
            "source_url": article.source_url,
            "date_added": article.date_added
        } for article in articles
    ]
    return jsonify(res), 200

@admin_bp.route("/all_summaries/<int:article_id>", methods=['GET'])
def get_article_summaries(article_id):
    summaries = Summary.query.filter_by(article_id=article_id).all()
    if not summaries:
        return jsonify({"error": "No summaries found for this article"}), 200
    res = [
        {
            "id": summary.id,
            "article_id": summary.article_id,
            "content": summary.content,
            "rating": summary.rating,
            "model_type": summary.model_type.name,
            "date_generated": summary.date_generated
        } for summary in summaries
    ]
    return jsonify(res), 200

