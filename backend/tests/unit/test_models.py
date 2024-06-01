from article_summaries.models import User, UserType


def test_new_user():
    user = User(username="test", email="test@mail.com", password="test")

    assert user.username == "test"
    assert user.email == "test@mail.com"
    assert user.password == "test"
    # assert user.type == UserType.USER
