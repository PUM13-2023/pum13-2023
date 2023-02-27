from dashboard.models import db


def test_connection_established() -> None:
    data_client = db.connect_data_db()
    assert data_client is not None
    # client_user = db.connect_user_db()
