from article_summaries.models import UserType
from ..conftest import new_user, new_user_admin


def test_new_user(new_user):
    assert new_user.username == "test"
    assert new_user.email == "test@mail.com"
    assert new_user.password != "test"  # hashed password
    assert new_user.type == UserType.USER


def test_new_user_admin(new_user_admin):
    assert new_user_admin.username == "admin"
    assert new_user_admin.email == "admin@mail.com"
    assert new_user_admin.password != "admin"  # hashed password
    assert new_user_admin.type == UserType.ADMIN
