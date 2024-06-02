from datetime import timedelta
from functools import wraps
from flask import url_for
import pytest
from article_summaries import create_app, db
from article_summaries.models import User, UserType, Article, Summary, ModelType
from sqlalchemy.exc import IntegrityError


TOKEN_EXPIRATION_TIME = 2


def handle_db_integrity_error(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            db.session.commit()
            return result
        except IntegrityError:
            db.session.rollback()

    return decorated_function


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
@handle_db_integrity_error
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
@handle_db_integrity_error
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
@handle_db_integrity_error
def new_article_db(new_article):
    db.session.add(new_article)
    db.session.commit()

    return new_article


@pytest.fixture()
def new_summary(new_article):
    summary = Summary(
        article_id=new_article.id,
        content="Test summary",
        model_type=ModelType.OUR_MODEL,
    )
    return summary


@pytest.fixture()
@handle_db_integrity_error
def new_summary_db(new_summary):
    db.session.add(new_summary)
    db.session.commit()

    return new_summary


@pytest.fixture()
def access_token(client, new_user_db, user_data):
    # Log in as regular user to get the token
    response = client.post(
        url_for("auth_bp.login"),
        json={"username": user_data["username"], "password": user_data["password"]},
    )
    return response.json["access_token"]


@pytest.fixture()
def access_token_admin(client, new_user_admin_db, admin_data):
    # Log in as regular user to get the token
    response = client.post(
        url_for("auth_bp.login"),
        json={"username": admin_data["username"], "password": admin_data["password"]},
    )
    return response.json["access_token"]
