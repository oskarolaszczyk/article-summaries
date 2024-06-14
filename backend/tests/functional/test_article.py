import json
import random

from flask import url_for


def test_scrape_success(client):
    response = client.get(url_for("article_bp.scrape"), query_string={'url': 'https://example.com'})
    data = response.get_json()
    assert response.status_code == 200
    assert 'title' in data
    assert 'content' in data


def test_scrape_missing_url(client):
    response = client.get(url_for("article_bp.scrape"))
    data = response.get_json()
    assert response.status_code == 400
    assert data == {"error": "URL parameter is missing"}


def test_add_article_succes(client, access_token):
    title = 'Test-Article-' + str(random.randint(1, 1000))
    data = {
        'user_id': 1,
        'title': title,
        'source_url': 'https://example.com'
    }
    response = client.post(
        url_for("article_bp.add_article"), headers={"Authorization": f"Bearer {access_token}"}, json=data
    )
    assert response.status_code == 201

def test_add_duplicate_article(client, access_token):
    title = 'Test-Article-' + str(random.randint(1, 1000))
    data = {
        'user_id': 1,
        'title': title,
        'source_url': 'https://example.com'
    }
    response = client.post(
        url_for("article_bp.add_article"), headers={"Authorization": f"Bearer {access_token}"}, json=data
    )
    assert response.status_code == 201
    response = client.post(
        url_for("article_bp.add_article"), headers={"Authorization": f"Bearer {access_token}"}, json=data
    )
    assert response.status_code == 200
def test_add_article_bad_request(client, access_token):
    data = {
        'user_id': 1,
        'source_url': 'https://example.com'
    }
    response = client.post(
        url_for("article_bp.add_article"), headers={"Authorization": f"Bearer {access_token}"}, json=data
    )
    data = response.get_json()
    assert response.status_code == 400


def test_add_article_unauthorized(client, new_article):
    data = {
        'user_id': 1,
        'title': 'Test Article',
        'source_url': 'https://example.com'
    }
    response = client.post(
        url_for("article_bp.add_article"), json=data
    )
    data = response.get_json()
    assert response.status_code == 401
