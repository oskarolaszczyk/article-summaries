import pytest
from article_summaries import create_app
from article_summaries.models import User, UserType, Article


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )
    # other setup can go here
    yield app
    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


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
