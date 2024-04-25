from flask import Flask, request, jsonify
from goose3 import Goose
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
headers = { "Accept-Language": "pl,en-US;q=0.7,en;q=0.3" }
goose = Goose({ "http_headers": headers })


@app.route("/scrape", methods=['GET'])
def scrape():
    try:
        url = request.args.get('url')
        if not url:
            return jsonify({ "error": "URL parameter is missing" }), 400
        web_text = goose.extract(url=url).cleaned_text
        return jsonify({ "content": web_text })
    except Exception as e:
        return jsonify({ "error": str(e) }), 500
