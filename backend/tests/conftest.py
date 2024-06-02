from datetime import timedelta
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
def new_user():
    user = User(username="test", email="test@mail.com", password="password123")
    return user


@pytest.fixture()
def new_user_admin():
    user = User(
        username="admin",
        email="admin@mail.com",
        password="password123",
        type=UserType.ADMIN,
    )
    return user


@pytest.fixture()
def new_article(new_user):
    article = Article(
        user_id=new_user.id, title="Test Article", source_url="https://test.com"
    )
    return article


@pytest.fixture()
def user_data():
    return {"username": "test", "email": "test@mail.com", "password": "password123"}
