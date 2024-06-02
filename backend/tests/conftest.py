from datetime import timedelta
from flask import url_for
import pytest
from article_summaries import create_app, db
from article_summaries.models import User, UserType, Article


TOKEN_EXPIRATION_TIME = 2


@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config.from_object("config.TestConfig")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=TOKEN_EXPIRATION_TIME)

    with app.app_context():
        db.create_all()
        yield app
        db.session.commit()
        db.drop_all()


@pytest.fixture()
def client(app):
    client = app.test_client()
    ctx = app.test_request_context()
    ctx.push()

    yield client

    ctx.pop()


@pytest.fixture()
def user_data():
    return {"username": "test", "email": "test@mail.com", "password": "password123"}


@pytest.fixture()
def admin_data():
    return {"username": "admin", "email": "admin@mail.com", "password": "password123"}


@pytest.fixture()
def new_user(user_data):
    user = User(
        username=user_data["username"],
        email=user_data["email"],
        password=user_data["password"],
    )
    return user


@pytest.fixture()
def new_user_db(new_user):
    db.session.add(new_user)
    db.session.commit()

    return new_user


@pytest.fixture()
def new_user_admin(admin_data):
    user = User(
        username=admin_data["username"],
        email=admin_data["email"],
        password=admin_data["password"],
        type=UserType.ADMIN,
    )
    return user


@pytest.fixture()
def new_user_admin_db(new_user_admin):
    db.session.add(new_user_admin)
    db.session.commit()

    return new_user_admin


@pytest.fixture()
def new_article(new_user):
    article = Article(
        user_id=new_user.id, title="Test Article", source_url="https://test.com"
    )
    return article


@pytest.fixture()
def new_article_db(new_article):
    db.session.add(new_article)
    db.session.commit()

    return new_article
