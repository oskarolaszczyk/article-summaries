import pytest
from article_summaries import User, UserType


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
