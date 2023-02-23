from dashboard.models import db

def test_connection_established():
    client = db.connect()
    
