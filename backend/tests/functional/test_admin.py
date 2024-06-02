import pytest
from flask import url_for
from article_summaries.models import User, Article, Summary, UserType
from ..conftest import (
    client,
    new_user_db,
    new_user_admin_db,
    new_article_db,
    user_data,
    admin_data,
)


def test_get_all_users_as_non_admin(client, new_user_db, user_data):
    # Log in as regular user to get the token
    login_response = client.post(
        url_for("auth_bp.login"),
        json={"username": user_data["username"], "password": user_data["password"]},
    )
    access_token = login_response.json["access_token"]

    response = client.get(
        url_for("admin_bp.get_all_users"),
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 403
    assert response.json == "error:Admin privileges required!"


def test_get_all_users_as_admin(
    client, new_user_admin_db, admin_data
):  # TODO fill more users
    # Log in as admin to get the token
    login_response = client.post(
        url_for("auth_bp.login"),
        json={"username": admin_data["username"], "password": admin_data["password"]},
    )
    access_token = login_response.json["access_token"]

    response = client.get(
        url_for("admin_bp.get_all_users"),
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert len(response.json) == 2  # Admin and regular user
