"""Model for handling database connections.

User information such as usernames, dashboards etc. are stored in the
``dashboard`` database.

Each project is stored in its own database. These databases contain
three collections: data, settings, and metadata.
"""
import os
from typing import Any

from dotenv import load_dotenv
import mongoengine
from pymongo import MongoClient
from pymongo.database import Database

from dashboard import config

load_dotenv()

DB_URL_ENV_NAME = "DB_URL"
USER_DB_NAME = "dashboard"


def _get_db_url() -> str:
    """Find the db url from the environment."""
    db_url = os.getenv(DB_URL_ENV_NAME)
    if not db_url:
        raise EnvironmentError(f"Can't find environment variable {DB_URL_ENV_NAME}")

    return db_url


def _connect_mock_db(db_name: str, alias: str = "default") -> None:
    import mongomock

    mongoengine.connect(
        db=db_name, alias=alias, host="127.0.0.1", mongo_client_class=mongomock.MongoClient
    )


def connect_data_db(db_name: str, alias: str = "data") -> None:
    """Connect to project db.

    Attributes:
        db_name (str): the name of the project db.
        alias (str): the alias of the connection. This is only needed
            if multiple connections need to be managed.
    """
    if config.MOCK_DB:
        _connect_mock_db(db_name=db_name, alias=alias)
        return

    db_url = _get_db_url()
    mongoengine.connect(db=db_name, alias=alias, host=db_url)


def connect_user_db() -> None:
    """Connect to user db."""
    if config.MOCK_DB:
        _connect_mock_db(db_name=USER_DB_NAME)
        return

    db_url = _get_db_url()
    mongoengine.connect(db=USER_DB_NAME, host=db_url)


def _is_project_db(db: Database[dict[str, Any]]) -> bool:
    """Return True if the database matches the project db schema."""
    collections = db.list_collection_names()
    return "data" in collections and "settings" in collections


def list_project_dbs() -> list[str]:
    """Return a list of project dbs."""
    db_url = _get_db_url()
    client: MongoClient[dict[str, Any]] = MongoClient(db_url)

    return [db_name for db_name in client.list_database_names() if _is_project_db(client[db_name])]
