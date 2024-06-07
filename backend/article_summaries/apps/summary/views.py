from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from article_summaries.apps.summary.functions import summarize, calc_idf
from article_summaries.models import db, Summary

import re
import math
import nltk
import json

summary_bp = Blueprint(
    "summary_bp", __name__, template_folder="templates", static_folder="static"
)


@summary_bp.route("/summary/<int:id>/rate", methods=['PUT'])
@jwt_required()
def rate_summary(id):
    req = request.get_json()
    rating = req.get('rating')

    if rating not in [True, False]:
        return jsonify({"error": "Rating must have value true or false"}), 400
    
    summary = Summary.query.get(id)
    if not summary:
        return jsonify({"error": "Summary not found"}), 404
        
    summary.rating = rating
    db.session.commit()
    return jsonify({"message": "Rating updated successfully"}), 200

        
@summary_bp.route("/generate", methods=['POST'])
def summarize_endpoint():
    req = request.get_json()

    if not 'txt' in req:
        return jsonify({ "error": "No article content provided" }), 400
    if not 'sentences' in req:
        return jsonify({ "error": "Number of sentences not provided" }), 400

    try:
        with open("idf.json", "r") as f:
            idf = json.load(f)
    except FileNotFoundError:
        print("Calculating IDF...")
        try:
            idf = calc_idf('./apps/summary/dataset.csv')
            with open("idf.json", "w") as f:
                json.dump(idf, f)
        except FileNotFoundError as e:
            return jsonify({ "error": f"Internal server error {e}" }), 500

    summary = summarize(req['txt'], idf, req['sentences'])

    return jsonify({ "summary": summary })


@summary_bp.route("/", methods=["POST"])
@jwt_required()
def add_summary():
    data = request.get_json()
    article_id = data.get("article_id")
    content = data.get("content")
    rating = data.get("rating")
    model_type = data.get("model_type")
    if not article_id or not content or not model_type:
        return jsonify({"error": "Missing article ID, summary content or used model type"}), 400
    
    summary = Summary(
        article_id=article_id,
        content=content,
        rating=rating,
        model_type=model_type,
    )
    
    db.session.add(summary)
    db.session.commit()

    return jsonify({"message": "Successfully added"}), 201