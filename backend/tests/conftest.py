import pytest
from article_summaries import create_app
from article_summaries.models import User, UserType, Article


@pytest.fixture()
def app():
    app = create_app()
    app.config.from_object("config.TestConfig")

    yield app


@pytest.fixture()
def client(app):
    client = app.test_client()
    ctx = app.test_request_context()
    ctx.push()

    yield client

    ctx.pop()


@pytest.fixture()
def new_user():
    user = User(username="test", email="test@mail.com", password="test")
    return user


@pytest.fixture()
def new_user_admin():
    user = User(
        username="admin", email="admin@mail.com", password="admin", type=UserType.ADMIN
    )
    return user


@pytest.fixture()
def new_article(new_user):
    article = Article(
        user_id=new_user.id, title="Test Article", source_url="https://test.com"
    )
    return article
