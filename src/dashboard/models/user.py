"""
Models related to user database.
"""
from mongoengine import (
    Document,
    EmbeddedDocument,
    EmbeddedDocumentListField,
    ListField,
    ReferenceField,
    StringField,
)


class Diagram(EmbeddedDocument):
    """Diagram database mode.

    A diagram stores all the information needed to reconstruct a Dast
    diagram.

    The current implementation is a stub, which will need to be
    extended to store various metadata about the diagram.

    Attributes:
        data (DBRef): A DBRef to the data object which contains the
            data to be plotted.
    """

    data = ReferenceField("data", dbref=True)


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

    authorized_users = ListField(ReferenceField("User"))
    diagrams = EmbeddedDocumentListField(Diagram)


class User(Document):
    """User database model.

    The current User implementation contains no account security and
    is only used for testing purposes.

    Attributes:
        username (str): The users username, used to identify the user.
        dashboards (list[Dashboard]): list of embedded dashboard
            documents.
    """

    username = StringField()
    dashboards = EmbeddedDocumentListField(Dashboard)


def register_user(username: str) -> User:
    pass


def login_user(username: str) -> User:
    pass
