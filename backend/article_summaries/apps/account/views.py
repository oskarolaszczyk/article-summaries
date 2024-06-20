import re
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from email_validator import validate_email, EmailNotValidError
from article_summaries import bcrypt
from article_summaries.models import db, Summary, Article, User


account_bp = Blueprint(
    "account_bp", __name__, template_folder="templates", static_folder="static"
)

@account_bp.route("/<int:user_id>/articles", methods=['GET'])
@jwt_required()
def get_user_articles(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    articles = Article.query.filter_by(user_id=user_id).all()
    articles_list = [
        {
            "id": article.id,
            "title": article.title,
            "source_url": article.source_url,
            "date_added": article.date_added
        } for article in articles
    ]
    return jsonify(articles_list), 200

@account_bp.route("/summaries/<int:article_id>", methods=['GET'])
@jwt_required()
def get_user_summaries(article_id):
    article = Article.query.get(article_id)
    if not article:
        return jsonify({"error": "Article not found"}), 404

    summaries = Summary.query.filter_by(article_id=article_id).all()
    result = [
        {
            "id": row.id,
            "content": row.content,
            "rating": row.rating,
            "model_type": row.model_type.name,
            "date_generated": row.date_generated
        } for row in summaries
    ]
    return jsonify(result), 200

@account_bp.route("/<int:user_id>", methods=['PUT'])
@jwt_required()
def update_user_data(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    req = request.get_json()
    try:
        emailinfo = validate_email(req.get('email'), check_deliverability=True)
        email = emailinfo.normalized
    except EmailNotValidError as e:
        response_body = {"error": "Provided email is invalid."}
        return jsonify(response_body), 400
    
    old_password = req.get('old_password')
    
    if not bcrypt.check_password_hash(user.password, old_password):
        return jsonify({"error": "Wrong password"}), 400
    
    username = req.get('username')
    password = req.get('password')
    email = req.get('email')

    if len(password) < 8:
        response_body = {"error": "Make sure your password is at least 8 letters"}
        return jsonify(response_body), 400
    elif re.search('[0-9]', password) is None:
        response_body = {"error": "Make sure your password has number in it"}
        return jsonify(response_body), 400
    elif re.search('[A-Z]', password) is None:
        response_body = {"error": "Make sure your password has capital letter in it"}
        return jsonify(response_body), 400
    elif not any(not c.isalnum() for c in password):
        response_body = {"error": "Make sure your password has special character in it"}
        return jsonify(response_body), 400

    if username:
        user.username = username
    if password:
        user.password = bcrypt.generate_password_hash(password).decode("utf-8")
    if email:
        user.email = email
        
    db.session.commit()
    return jsonify({"message": "Profile data updated successfully!"}), 200
    