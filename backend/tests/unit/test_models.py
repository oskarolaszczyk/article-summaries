from article_summaries.models import UserType, Summary, ModelType
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


def test_new_article(new_user, new_article):
    assert new_article.user_id == new_user.id
    assert new_article.title == "Test Article"
    assert new_article.source_url == "https://test.com"


def test_new_summary_our_model(new_article):
    summary = Summary(
        article_id=new_article.id,
        content="Test summary",
        model_type=ModelType.OUR_MODEL,
    )

    assert summary.article_id == new_article.id
    assert summary.content == "Test summary"
    assert summary.model_type == ModelType.OUR_MODEL


def test_new_summary_meaningcloud(new_article):
    summary = Summary(
        article_id=new_article.id,
        content="Test summary",
        model_type=ModelType.MEANINGCLOUD,
    )

    assert summary.article_id == new_article.id
    assert summary.content == "Test summary"
    assert summary.model_type == ModelType.MEANINGCLOUD
