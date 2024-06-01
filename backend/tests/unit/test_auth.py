from time import sleep
import pytest
from ..conftest import client, user_data, TOKEN_EXPIRATION_TIME
from flask import url_for
from article_summaries.models import User


def test_register_user_success(client, user_data):
    response = client.post(url_for("auth_bp.register"), json=user_data)
    assert response.status_code == 201
    assert "access_token" in response.json
    assert "refresh_token" in response.json


def test_register_user_missing_data(client):
    response = client.post(
        url_for("auth_bp.register"),
        json={
            "username": "",
            "email": "newuser@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 400
    assert response.json["error"] == "No username or email or password provided."


# def test_register_user_existing_email(client, user_data):
#     client.post(url_for("auth_bp.register"), json=user_data)

#     response = client.post(
#         url_for("auth_bp.register"),
#         json={
#             "username": "newuser2",
#             "email": user_data["email"],
#             "password": "password123",
#         },
#     )
#     assert response.status_code == 400
#     assert response.json["error"] == "User with given username already exists."


def test_register_user_existing_username(client, user_data):
    response = client.post(
        url_for("auth_bp.register"),
        json={
            "username": user_data["username"],
            "email": "newemail@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 400
    assert response.json["error"] == "User with given username already exists."


def test_login_user_success(client, user_data):
    response = client.post(
        url_for("auth_bp.login"),
        json={"username": user_data["username"], "password": user_data["password"]},
    )
    assert response.status_code == 200
    assert "access_token" in response.json
    assert "refresh_token" in response.json


def test_login_user_wrong_password(client, user_data):
    response = client.post(
        url_for("auth_bp.login"),
        json={"username": user_data["username"], "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json["error"] == "Please check your login details and try again."


def test_login_user_nonexistent_user(client):
    response = client.post(
        url_for("auth_bp.login"),
        json={"username": "nonexistentuser", "password": "password"},
    )
    assert response.status_code == 404
    assert response.json["error"] == "User with given credentials does not exist."


def test_login_user_missing_data(client):
    response = client.post(
        url_for("auth_bp.login"), json={"username": "", "password": "password"}
    )
    assert response.status_code == 400
    assert response.json["error"] == "No username or email or password provided."


def test_refresh_token(client, user_data):
    response = client.post(
        url_for("auth_bp.login"),
        json={"username": user_data["username"], "password": user_data["password"]},
    )

    refresh_token = response.json["refresh_token"]

    response = client.post(
        url_for("auth_bp.refresh"), headers={"Authorization": f"Bearer {refresh_token}"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json


def test_refresh_token_missing(client):
    response = client.post(url_for("auth_bp.refresh"))
    assert response.status_code == 401


def test_refresh_token_invalid(client):
    response = client.post(
        url_for("auth_bp.refresh"), headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 401


def test_logout_user(client, user_data):
    response = client.post(
        url_for("auth_bp.login"),
        json={"username": user_data["username"], "password": user_data["password"]},
    )

    access_token = response.json["access_token"]

    response = client.post(
        url_for("auth_bp.logout"), headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json["message"] == "Logout successful."


def test_logout_user_missing_token(client):
    response = client.post(url_for("auth_bp.logout"))
    assert response.status_code == 401


def test_logout_user_invalid_token(client):
    response = client.post(
        url_for("auth_bp.logout"), headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 401


def test_protected_endpoint(client, user_data):
    response = client.post(
        url_for("auth_bp.login"),
        json={"username": user_data["username"], "password": user_data["password"]},
    )

    access_token = response.json["access_token"]

    response = client.get(
        url_for("auth_bp.protected"),
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert response.json["message"] == "Access to protected endpoint."


def test_protected_endpoint_missing_token(client):
    response = client.get(url_for("auth_bp.protected"))
    assert response.status_code == 401


def test_protected_endpoint_invalid_token(client):
    response = client.get(
        url_for("auth_bp.protected"), headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 401


def test_protected_endpoint_expired_token(client, user_data):
    response = client.post(
        url_for("auth_bp.login"),
        json={"username": user_data["username"], "password": user_data["password"]},
    )
    access_token = response.json["access_token"]

    sleep(TOKEN_EXPIRATION_TIME)  # Wait for token to expire

    response = client.get(
        url_for("auth_bp.protected"),
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 401
