"""Test user db."""
from datetime import datetime

from flask import Flask
from flask.ctx import RequestContext
from flask_login import LoginManager, current_user
import mongoengine
import mongomock
import pymongo
import pytest

from dashboard.models.user import Dashboard, User, login_user


@pytest.fixture(autouse=True)
def connection():
    """Connect mongoengine to mongomock and return client."""
    conn = mongoengine.connect(
        db="dashboard",
        host="mongodb://localhost",
        mongo_client_class=mongomock.MongoClient,
        uuidRepresentation="standard",
    )

    return conn


@pytest.fixture
def example_user():
    """Example user."""
    username = "fixture-user"
    user = login_user(username)
    user.dashboards.append(Dashboard(created=datetime.now()))
    user.save()

    return user


@pytest.fixture
def app() -> Flask:
    """Return a Flask app."""
    app = Flask(__name__)
    app.secret_key = "test-key123"

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str) -> User:
        """Load a user by id.

        Required by flask-login. For more information, see
        https://flask-login.readthedocs.io/en/latest/#your-user-class
        """
        user: User = User.objects(id=user_id).get()

        return user

    return app


@pytest.fixture
def ctx(app: Flask) -> RequestContext:
    """Yield a flask request context."""
    with app.test_request_context() as ctx:
        yield ctx


def find_user(username):
    """Find user by username."""
    return User.objects(username=username).first()


@pytest.mark.test_user_db
class TestUserDb:
    """Contains tests for testing user db."""

    def test_login_new_user(self, ctx: RequestContext):
        """Test login new user."""
        username = "test-new-user"

        usr = login_user(username)

        assert usr is not None
        assert usr.username == username

    def test_login_new_user_in_db(self, ctx: RequestContext):
        """Test user is stored in db."""
        username = "test-new-user-in-db"

        usr = login_user(username)

        assert find_user(username).id == usr.id

    def test_login_existing_user(self, ctx: RequestContext, example_user: User):
        """Test login returns same user if username in use."""
        usr = login_user(example_user.username)

        assert usr.id == example_user.id

    def test_login_session(self, ctx: RequestContext, example_user: User):
        """Test that the logged in user is stored in session."""
        login_user(example_user.username)

        assert current_user.id == example_user.id

    def test_missing_dashboard_time(
        self, ctx: RequestContext, connection: pymongo.MongoClient, example_user: User
    ):
        """Test that dashboard time info is not updated.

        Test that dashboard time info is not updated
        when user is queried after a dashboard has
        been created and saved.
        """
        db = connection["dashboard"]
        queried_user = db["user"].find_one({"username": example_user.username})
        assert queried_user is not None
        queried_dashboard = queried_user["dashboards"][0]

        odm_user = login_user(example_user.username)
        odm_dashboard = odm_user.dashboards[0]

        assert queried_dashboard["created"] == odm_dashboard.created
        assert queried_dashboard["modified"] == odm_dashboard.modified
