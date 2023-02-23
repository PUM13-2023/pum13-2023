import os

from pymongo import MongoClient
from pymongo.database import Database
from dotenv import load_dotenv


load_dotenv()


def connect(server_url: str, db_name: str) -> Database:
    """Connect to a MongoDB database.

    server_url: the MongoDB URL to connnect to.
    db_name: the database object to retrieve.
    
    """
    client = MongoClient(server_url)
    db = client[db_name]

    return db


def connect_data_db() -> Database:
    server_url = os.getenv("DATA_DB_URL")
    db_name = os.getenv("DATA_DB_NAME")

    db = connect(server_url, db_name)


def connect_user_db() -> Database:
    server_url = os.getenv("USER_DB_URL")
    db_name = os.getenv("USER_DB_NAME")

    db = connect(server_url, db_name)
