"""Models related to user database."""
from datetime import datetime
from typing import Any

import flask_login
from mongoengine import (
    DateTimeField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentListField,
    ListField,
    ReferenceField,
    StringField,
    signals,
)


class Diagram(EmbeddedDocument):
    """Diagram database mode.

    A diagram stores all the information needed to reconstruct a
    dashboard diagram.

    The current implementation is a stub, which will need to be
    extended to store various metadata about the diagram.

    Attributes:
        data (Data): A reference to the data object which contains the
            data to be plotted.
    """

    data = ReferenceField("Data", dbref=True)


class Dashboard(EmbeddedDocument):
    """Dashboard database model.

    A Dashboard stores all the data associated with reconstructing a
    dashboard page.

    Attributes:
        authorized_users (list[User]): the list of users authorized to
            access the dashboard.
        diagrams (list[Diagram]): the diagrams which the dashboard
            consists of.
    """

    name: str = StringField()
    description: str = StringField()
    modified: datetime = DateTimeField()
    created: datetime = DateTimeField(required=True)
    authorized_users: list["User"] = ListField(ReferenceField("User"))
    diagrams: list[Diagram] = EmbeddedDocumentListField(Diagram)

    def update_modified(self) -> None:
        """Sets self.modified to datetime.now()."""
        self.modified = datetime.now()

    @staticmethod
    def post_init(sender: type, document: "Dashboard", **kwargs: Any) -> None:
        """Initialize time information."""
        if not document.modified:
            document.modified = document.created


signals.post_init.connect(Dashboard.post_init, sender=Dashboard)


class User(Document):
    """User database model.

    The current User implementation contains no account security and
    is only used for testing purposes.

    Attributes:
        username (str): The users username, used to identify the user.
        dashboards (list[Dashboard]): list of embedded dashboard
            documents.
        is_authenticated (bool): True if the User is authenticated.
        is_active (bool): True if the User is active, i.e. not
            suspended or similar.
        is_anonymous (bool): Always False for User objects.
    """

    username: str = StringField()
    dashboards: list[Dashboard] = EmbeddedDocumentListField(Dashboard)
    _is_authenticated: bool

    def __init__(self, *args: Any, **kwargs: Any):
        """Initialize a User."""
        super().__init__(*args, **kwargs)
        self._is_authenticated = kwargs.get("is_authenticated", False)

    @property
    def is_authenticated(self) -> bool:
        """Get authentication status.

        Required by flask-login. For more information, see
        https://flask-login.readthedocs.io/en/latest/#your-user-class
        """
        return self._is_authenticated

    @is_authenticated.setter
    def is_authenticated(self, value: bool) -> None:
        """Set authentication status."""
        self._is_authenticated = value

    @property
    def is_active(self) -> bool:
        """Return True if the user is active.

        Currently all users are considered active.

        Required by flask-login. For more information, see
        https://flask-login.readthedocs.io/en/latest/#your-user-class
        """
        return True

    @property
    def is_anonymous(self) -> bool:
        """Return True if the user is an anonymous user.

        Anonymous users are not handled by this class, hence returns
        False.

        Required by flask-login. For more information, see
        https://flask-login.readthedocs.io/en/latest/#your-user-class
        """
        return False

    def get_id(self) -> str:
        """Return user id as a string.

        Required by flask-login. For more information, see
        https://flask-login.readthedocs.io/en/latest/#your-user-class
        """
        return str(self.id)

    def add_dashboard(self, name: str, desc: str) -> None:
        """Adds dashboard to mongoDB.

        Args:
            name (str): Dashboard name
            desc (str): Dashboard description
        """
        added_dashboard = Dashboard(name=name, description=desc, created=datetime.now())
        self.dashboards.append(added_dashboard)
        self.save()


def register_user(username: str) -> User:
    """Register a new user.

    Creates a new user with a given username.

    Args:
        username (str): the username of the new user.

    Returns:
        A User object representing the newly created user.

    Raises:
        ValueError: a user with the specified username already exists.
    """
    if User.objects(username=username):
        raise ValueError("Can't register username. Already exists.")

    user = User(username=username)
    user.save()

    return user


def login_user(username: str) -> User:
    """Login as a user.

    Logins as a user, creating the user if it does not exists.

    Args:
        username (str): the username of the user to login as.

    Returns:
        A User object representing the logged in user.
    """
    try:
        user: User = User.objects(username=username)[0]
    except IndexError:
        user = register_user(username)

    user.is_authenticated = True

    flask_login.login_user(user)

    return user
