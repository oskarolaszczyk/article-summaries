import pytest
from flask import url_for
from article_summaries.models import User, Article, Summary, UserType
from ..conftest import (
    client,
    access_token,
    access_token_admin,
    new_article_db,
    new_summary_db,
)

# TODO fill more users, articles and summaries


def test_get_all_users_as_non_admin(client, access_token):
    response = client.get(
        url_for("admin_bp.get_all_users"),
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 403
    assert response.json["error"] == "Admin privileges required!"


def test_get_all_users_as_admin(client, access_token_admin):
    response = client.get(
        url_for("admin_bp.get_all_users"),
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )

    assert response.status_code == 200
    assert len(response.json) == 2  # Admin and regular user


def test_get_all_articles_as_non_admin(client, access_token):
    response = client.get(
        url_for("admin_bp.get_all_articles"),
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 403
    assert response.json["error"] == "Admin privileges required!"


def test_get_empty_articles(client, access_token_admin):
    response = client.get(
        url_for("admin_bp.get_all_articles"),
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )

    assert response.status_code == 200
    assert response.json["error"] == "No articles found in database"


def test_get_all_articles_as_admin(client, access_token_admin, new_article_db):
    response = client.get(
        url_for("admin_bp.get_all_articles"),
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )

    assert response.status_code == 200
    assert len(response.json) == 1
    assert "error" not in response.json
    assert "id" in response.json[0]
    assert "user_id" in response.json[0]
    assert "title" in response.json[0]
    assert "source_url" in response.json[0]
    assert "date_added" in response.json[0]


def test_get_article_summaries_as_non_admin(client, access_token):
    response = client.get(
        url_for("admin_bp.get_article_summaries"),
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 403
    assert response.json["error"] == "Admin privileges required!"


def test_get_empty_article_summaries(client, access_token_admin):
    response = client.get(
        url_for("admin_bp.get_article_summaries"),
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )

    assert response.status_code == 200
    assert response.json["error"] == "No summaries found in database"


def test_get_article_summaries_as_admin(client, access_token_admin, new_summary_db):
    response = client.get(
        url_for("admin_bp.get_article_summaries"),
        headers={"Authorization": f"Bearer {access_token_admin}"},
    )

    assert response.status_code == 200
    assert len(response.json) == 1
    assert "error" not in response.json
    assert "id" in response.json[0]
    assert "article_id" in response.json[0]
    assert "content" in response.json[0]
    assert "rating" in response.json[0]
    assert "model_type" in response.json[0]
    assert "date_generated" in response.json[0]
