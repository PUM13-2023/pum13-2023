import os
from typing import Tuple, Optional

from dotenv import load_dotenv
import mongoengine

load_dotenv()


def get_connection_params(url_env_name: str, db_env_name: str) -> Tuple[str, str]:
    server_url = os.getenv(url_env_name)
    db_name = os.getenv(db_env_name)
    if not server_url or not db_name:
        raise EnvironmentError(f"Can't find environment variables {url_env_name} or {db_env_name}")

    return (server_url, db_name)


def connect_data_db(alias: str) -> None:
    server_url, db_name = get_connection_params("DATA_DB_URL", "DATA_DB_NAME")
    mongoengine.connect(alias=alias, host=server_url, name=db_name)


def connect_user_db() -> None:
    server_url, db_name = get_connection_params("USER_DB_URL", "USER_DB_NAME")

    mongoengine.connect(host=server_url, name=db_name)
