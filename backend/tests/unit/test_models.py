from article_summaries.models import User, UserType


def test_new_user():
    user = User(username="test", email="test@mail.com", password="test")

    assert user.username == "test"
    assert user.email == "test@mail.com"
    assert user.password != "test"  # hashed password
    assert user.type == UserType.USER


def test_new_user_admin():
    user = User(
        username="admin", email="admin@mail.com", password="admin", type=UserType.ADMIN
    )

    assert user.username == "admin"
    assert user.email == "admin@mail.com"
    assert user.password != "admin"  # hashed password
    assert user.type == UserType.ADMIN
