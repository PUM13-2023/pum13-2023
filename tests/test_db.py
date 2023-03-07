from dashboard.models import db


def test_data_db_connection() -> None:
    db.connect_data_db("data-db")


def test_user_db_connection() -> None:
    db.connect_user_db()
