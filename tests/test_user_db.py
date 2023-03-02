import pytest
import mongoengine

from dashboard.models import user
from dashboard.models import db

@pytest.fixture
def connection(autouse=True):
    server_url, _ = get_connection_params("USER_DB_URL", "USER_DB_NAME")
    conn = mongoengine.connect(server_url, "dashboard_test")

    return conn


@pytest.fixture
def clear_database(connection):
    connection.user.drop()

@pytest.fixture
def example_user():
    username = "fixture-user"
    return user.register_user(username)


def find_user(username):
    return user.User.objects(username=username).first()


def test_register_user():
    username = "test-register-user"
    u = user.register_user(username)
    assert u is not None

    assert find_user(username) is not None


def test_register_twice():
    username = "test-register-twice"

    user.register_user(username)

    with pytest.raises(ValueError):
        user.register_user(username)


def test_login(example_user):
    username = example_user.username

    u = user.login_user(username)
    assert u is not None
    assert u.username == username


def test_login_non_existant_user():
    username = "this-user-doesnt-exist"
    with pytest.raises(ValueError):
        u = user.login_user(username)
