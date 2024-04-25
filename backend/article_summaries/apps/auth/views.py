from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from article_summaries.models import db, User
from article_summaries import bcrypt
from sqlalchemy import or_


auth_bp = Blueprint(
    "auth_bp", __name__, template_folder="templates", static_folder="static"
)


@auth_bp.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")

    if not username or not email or not password:
        return jsonify({"error": "No username or email or password provided."}), 400

    user = User.query.filter_by(username=username).first()
    if user:
        return (
            jsonify(
                {"error": "User with given email address or username already exists."}
            ),
            400,
        )

    new_user = User(
        username=username,
        email=email,
        password=bcrypt.generate_password_hash(password).decode("utf-8"),
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Account successfully created."}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    login_name = request.json.get("login-name")
    password = request.json.get("password")

    if not login_name or not password:
        return jsonify({"error": "No username or email or password provided."}), 400

    user = User.query.filter(
        or_(User.username == login_name, User.email == login_name)
    ).first()
    if not user:
        return (
            jsonify({"error": "User with given credentials does not exist."}),
            404,
        )

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Please check your login details and try again."}), 401

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({"access_token": access_token, "refresh_token": refresh_token})


@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify({"message": "Access to protected endpoint."}), 200
