import pytest
from article_summaries.models import User, UserType, Article


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
