import random

from flask import url_for

from article_summaries.apps.summary.summarizers.Wadim import tokenize, count_words, calc_tf, calc_idf, rank_sentence, \
    summarize
from article_summaries.models import Summary, Article


def test_tokenize():
    line = "This is a test sentence."
    expected_tokens = ['thi', 'is', 'a', 'test', 'sentenc', '']
    assert tokenize(line) == expected_tokens


def test_count_words():
    words = ['this', 'is', 'a', 'test', 'test']
    expected_counts = {'this': 1, 'is': 1, 'a': 1, 'test': 2}
    assert count_words(words) == expected_counts


def test_calc_tf():
    text = "This is a test test sentence."
    expected_tf = {'': 0.14285714285714285,
                   'a': 0.14285714285714285,
                   'is': 0.14285714285714285,
                   'sentenc': 0.14285714285714285,
                   'test': 0.2857142857142857,
                   'thi': 0.14285714285714285}
    assert calc_tf(text) == expected_tf


def test_rank_sentence():
    sentence = "This is a test sentence."
    idf = {'thi': 0.2, 'is': 0.2, 'a': 0.2, 'test': 0.4, 'sentenc': 0.2}
    expected_rank = 0.2  # Oczekiwana wartość dla przykładu
    assert rank_sentence(sentence, idf) == expected_rank


def test_summarize():
    article = "This is the first sentence. This is the second sentence. This is the third sentence."
    idf = {'thi': 0.2, 'is': 0.2, 'a': 0.2, 'test': 0.4, 'sentenc': 0.2}  # Przykładowe wartości dla testu
    num_of_sentences = 1
    expected_summary = "This is the third sentence.."
    assert summarize(article, idf, num_of_sentences) == expected_summary

def test_add_summary_fail(client, access_token):
    response = client.post(url_for("summary_bp.add_summary"),headers={"Authorization": f"Bearer {access_token}"}, json={})
    assert response.status_code == 400
    assert response.json == {"error": "Missing article ID, summary content or used model type"}

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