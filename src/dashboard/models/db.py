import os
from typing import Tuple

from dotenv import load_dotenv
from pymongo import MongoClient, errors
from pymongo.database import Database

from dashboard.models.db_types import DocumentType

load_dotenv()


def connect(server_url: str, db_name: str) -> Database[DocumentType] | None:
    """Connect to a MongoDB database.

    Args:
        server_url (str): the MongoDB URL to connnect to.
        db_name (str): the database object to retrieve.

    Returns:
        Database[DocumentType] | None: A Database object if a connection
        could be established, otherwise returns None.
    """
    try:
        client: MongoClient[DocumentType] = MongoClient(server_url)
    except errors.ConnectionFailure:
        return None

    db = client[db_name]

    return db


def get_connection_params(url_env_name: str, db_env_name: str) -> Tuple[str, str]:
    server_url = os.getenv(url_env_name)
    db_name = os.getenv(db_env_name)
    if not server_url or not db_name:
        raise EnvironmentError(
            "Can't find environment variables "
            + f"{url_env_name}:{str(server_url)} or {db_env_name}:{db_name}"
        )

    return (server_url, db_name)


def connect_data_db() -> Database[DocumentType] | None:
    connection_params = get_connection_params("DATA_DB_URL", "DATA_DB_NAME")
    server_url = connection_params[0]
    db_name = connection_params[1]

    db = connect(server_url, db_name)
    return db


def connect_user_db() -> Database[DocumentType] | None:
    connection_params = get_connection_params("USER_DB_URL", "USER_DB_NAME")
    server_url = connection_params[0]
    db_name = connection_params[1]

    db = connect(server_url, db_name)
    return db
