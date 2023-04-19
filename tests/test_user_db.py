"""Test user db."""
import mongoengine
import mongomock
import pytest

from dashboard.models import user


@pytest.fixture(autouse=True)
def connection():
    """Connect mongoengine to mongomock and return client."""
    conn = mongoengine.connect(
        db="dashboard", host="mongodb://localhost", mongo_client_class=mongomock.MongoClient
    )

    return conn


@pytest.fixture
def example_user():
    """Example user."""
    username = "fixture-user"
    return user.login_user(username)


def find_user(username):
    """Find user by username."""
    return user.User.objects(username=username).first()


@pytest.mark.test_user_db
class TestUserDb:
    """Contains tests for testing user db."""

    def test_login_new_user(self):
        """Test login new user."""
        username = "test-new-user"

        usr = user.login_user(username)

        assert usr is not None
        assert usr.username == username

    def test_login_new_user_in_db(self):
        """Test user is stored in db."""
        username = "test-new-user-in-db"

        usr = user.login_user(username)

        assert find_user(username).id == usr.id

    def test_login_existing_user(self, example_user):
        """Test login returns same user if username in use."""
        usr = user.login_user(example_user.username)

        assert usr.id == example_user.id
