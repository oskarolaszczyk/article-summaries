from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
    # unset_jwt_cookies,
)
from article_summaries.models import db, User, UserType
from article_summaries import bcrypt
from sqlalchemy import or_
from flask_jwt_extended import current_user
from article_summaries.apps.auth.blocklist import BLOCKLIST

auth_bp = Blueprint(
    "auth_bp", __name__, template_folder="templates", static_folder="static"
)


@auth_bp.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")

    if not username or not email or not password:
        response_body = {"error": "No username or email or password provided."}
        return jsonify(response_body), 400

    user = User.query.filter_by(username=username).first()
    if user:
        response_body = {"error": "User with given username already exists."}
        return jsonify(response_body), 400

    new_user = User(
        username=username,
        email=email,
        password=password,
    )
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.id, fresh=True)
    refresh_token = create_refresh_token(identity=new_user.id)

    response_body = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "is_admin": new_user.type == UserType.ADMIN,
    }

    return jsonify(response_body), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        response_body = {"error": "No username or email or password provided."}
        return jsonify(response_body), 400

    user = User.query.filter(
        or_(User.username == username, User.email == username)
    ).first()
    if not user:
        response_body = {"error": "User with given credentials does not exist."}
        return jsonify(response_body), 404

    if not bcrypt.check_password_hash(user.password, password):
        response_body = {"error": "Please check your login details and try again."}
        return jsonify(response_body), 401

    access_token = create_access_token(identity=user.id, fresh=True)
    refresh_token = create_refresh_token(identity=user.id)

    response_body = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "is_admin": user.type == UserType.ADMIN,
    }
    return jsonify(response_body), 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)

    return jsonify({"access_token": access_token}), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    BLOCKLIST.add(jti)
    response = jsonify({"message": "Logout successful."}), 200

    return response


@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify({"message": "Access to protected endpoint."}), 200


@auth_bp.route("/who-am-i", methods=["GET"])
@jwt_required()
def who_am_i():
    return (
        jsonify(
            id=current_user.id,
            username=current_user.username,
            email=current_user.email,
            type=current_user.type.name,
            created_on=current_user.created_on,
        ),
        200,
    )
