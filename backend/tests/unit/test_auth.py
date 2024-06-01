import pytest
from ..conftest import client, new_user
from flask import url_for
from article_summaries.models import db, User, UserType
from flask_jwt_extended import create_access_token, create_refresh_token


def test_register_user(client):
    # Correct registration
    response = client.post(
        url_for("auth_bp.register"),
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 201
    assert "access_token" in response.json
    assert "refresh_token" in response.json
