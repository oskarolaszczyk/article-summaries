import random

from flask import url_for

from article_summaries.apps.summary.functions import tokenize, count_words, calc_tf, calc_idf, rank_sentence, \
    summarize
from article_summaries.models import Summary, Article


def test_add_summary(client, access_token):
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
    data = {
        "article_id": 1,
        "content": "This is a summary of the article.",
        "rating": True,
        "model_type": "OUR_MODEL"
    }
    response = client.post(url_for("summary_bp.add_summary"), headers={"Authorization": f"Bearer {access_token}"}, json=data)
    assert response.status_code == 201
    assert response.json == {"message": "Successfully added"}

def test_rate(client, access_token):
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
    data = {
        "article_id": 1,
        "content": "This is a summary of the article.",
        "rating": True,
        "model_type": "OUR_MODEL"
    }
    response = client.post(url_for("summary_bp.add_summary"), headers={"Authorization": f"Bearer {access_token}"}, json=data)
    assert response.status_code == 201
    assert response.json == {"message": "Successfully added"}
    data = {
        "rating": True
    }
    response = client.put(url_for("summary_bp.rate_summary", id=1), headers={"Authorization": f"Bearer {access_token}"},
                           json=data)
    assert response.status_code == 200


def test_rate_fail(client, access_token):
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
    data = {
        "article_id": 1,
        "content": "This is a summary of the article.",
        "rating": True,
        "model_type": "OUR_MODEL"
    }
    response = client.post(url_for("summary_bp.add_summary"), headers={"Authorization": f"Bearer {access_token}"}, json=data)
    assert response.status_code == 201
    assert response.json == {"message": "Successfully added"}
    data = {
        "rating": 2137
    }
    response = client.put(url_for("summary_bp.rate_summary", id=1), headers={"Authorization": f"Bearer {access_token}"},
                           json=data)
    assert response.status_code == 400

def test_rate_fail(client, access_token):
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
    data = {
        "article_id": 1,
        "content": "This is a summary of the article.",
        "rating": True,
        "model_type": "OUR_MODEL"
    }
    response = client.post(url_for("summary_bp.add_summary"), headers={"Authorization": f"Bearer {access_token}"}, json=data)
    assert response.status_code == 201
    assert response.json == {"message": "Successfully added"}
    data = {
        "rating": False
    }
    response = client.put(url_for("summary_bp.rate_summary", id=100), headers={"Authorization": f"Bearer {access_token}"},
                           json=data)
    assert response.status_code == 404

"""def test_generate_fail(client):
    data = {
        'txt': "Test. Test2. Test. Test. Test",
        'sentences': 3
    }
    response = client.post(
        url_for("summary_bp.summarize_endpoint"), json=data
    )
    assert response.status_code == 500"""

def test_generate_fail1(client):
    data = {
        'sentences': 3
    }
    response = client.post(
        url_for("summary_bp.summarize_endpoint"), json=data
    )
    assert response.status_code == 400

def test_generate_fail2(client):
    data = {
        'txt': "Test. Test2. Test. Test. Test",
    }
    response = client.post(
        url_for("summary_bp.summarize_endpoint"), json=data
    )
    assert response.status_code == 400