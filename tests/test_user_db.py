import mongoengine
import pytest

from dashboard.models import db, user


@pytest.fixture
def connection(autouse=True):
    server_url, _ = db.get_connection_params("USER_DB_URL", "USER_DB_NAME")
    conn = mongoengine.connect(server_url, "dashboard_test")

    return conn


@pytest.fixture
def clear_database(connection):
    connection.user.drop()


@pytest.fixture
def example_user():
    username = "fixture-user"
    return user.login_user(username)


def find_user(username):
    return user.User.objects(username=username).first()


def test_login_new_user():
    username = "test-new-user"

    usr = user.login_user(username)

    assert usr is not None
    assert usr.username == username


def test_login_new_user_in_db():
    username = "test-new-user-in-db"

    usr = user.login_user(username)

    assert find_user(username).id == usr.id


def test_login_existing_user(example_user):
    usr = user.login_user(example_user.username)

    assert usr.id == example_user.id
