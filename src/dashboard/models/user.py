"""Models related to user database."""
from datetime import datetime
from typing import Any

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
    """

    username: str = StringField()
    dashboards: list[Dashboard] = EmbeddedDocumentListField(Dashboard)


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

    return user
