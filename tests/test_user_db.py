import mongoengine
import mongomock
import pytest

from dashboard.models import user


@pytest.fixture(autouse=True)
def connection():
    conn = mongoengine.connect(
            host="mongodb://localhost", name="dashboard", mongo_client_class=mongomock.MongoClient
    )

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
