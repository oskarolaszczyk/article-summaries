from flask import Blueprint, jsonify, request
from goose3 import Goose
from article_summaries.models import db, Article


headers = { "Accept-Language": "pl,en-US;q=0.7,en;q=0.3" }
goose = Goose({ "http_headers": headers })

article_bp = Blueprint(
            "article_bp", __name__, template_folder="templates", static_folder="static"
)

@article_bp.route("/scrape", methods=['GET'])
def scrape():
    try:
        url = request.args.get('url')
        if not url:
            return jsonify({ "error": "URL parameter is missing" }), 400
        article = goose.extract(url=url)
        title = article.title
        web_text = article.cleaned_text
        return jsonify({ "title": title, "content": web_text })
    except Exception as e:
        return jsonify({ "error": str(e) }), 500


@article_bp.route("/", methods=['POST'])
def add_article():
    data = request.get_json()
    user_id = data.get('user_id')
    title = data.get('title')
    source_url = data.get('source_url')
    if not user_id or not title or not source_url:
        return jsonify({"error": "Missing user id, title or source URL"}), 400
    article = Article(
        user_id=user_id, 
        title=title, 
        source_url=source_url
    )
    db.session.add(article)
    db.session.commit()
    return jsonify({"message": "Article saved successfully!", "article_id": article.id}), 201