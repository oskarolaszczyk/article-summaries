from flask import Blueprint, jsonify, request
from goose3 import Goose

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
