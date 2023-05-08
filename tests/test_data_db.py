"""Test data db."""
from datetime import datetime

import mongoengine
import mongomock
import pytest

from dashboard.models.data import ArrayData, Data, Marker, NumericData, Setting, Settings, XyData

DB_NAME = "test-db"


@pytest.fixture(scope="module")
def client():
    """Connect mongoengine to mongomock and return client."""
    client = mongoengine.connect(
        db=DB_NAME,
        alias="data",
        host="mongodb://localhost",
        mongo_client_class=mongomock.MongoClient,
        uuidRepresentation="standard",
    )

    return client


@pytest.fixture(scope="module")
def settings(client):
    """Return _id of test settings object."""
    db = client[DB_NAME]
    settings_collection = db["settings"]

    return settings_collection.insert_one(
        {
            "test_case": "Test case",
            "time": datetime.now(),
            "set_1_1": {"value": 1, "unit": "cm"},
            "set_1_2": {"value": 2, "unit": "cm"},
            "set_2_1": {"value": "yes"},
        }
    ).inserted_id


@pytest.fixture(scope="module")
def numeric_data(client, settings):
    """Return _id of numeric test data."""
    db = client[DB_NAME]
    data_collection = db["data"]

    return data_collection.insert_one(
        {
            "settings_id": settings,
            "name": "Numeric data",
            "type": "numeric",
            "value": 3.14,
            "unit": "cm",
        }
    ).inserted_id


@pytest.fixture(scope="module")
def array_data(client, settings):
    """Return _id of array test data."""
    db = client[DB_NAME]
    data_collection = db["data"]

    return data_collection.insert_one(
        {
            "settings_id": settings,
            "name": "Numeric data",
            "type": "array",
            "value": [1.6180, 2.7182, 3.1415],
            "unit": "cm",
        }
    ).inserted_id


@pytest.fixture(scope="module")
def xy_data(client, settings):
    """Return _id of xy test data."""
    db = client[DB_NAME]
    data_collection = db["data"]

    return data_collection.insert_one(
        {
            "settings_id": settings,
            "name": "Numeric data",
            "type": "xy_plot",
            "x": [1.0, 2.0, 3.0],
            "y": [1.0, 4.0, 9.0],
            "x_unit": "s",
            "y_unit": "dB",
            "markers": [{"text": "marker", "x": 1.0, "y": 1.0}],
        }
    ).inserted_id


@pytest.fixture(scope="module")
def xy_data_default_values(client, settings):
    """Return _id of test xy data with missing fields."""
    db = client[DB_NAME]
    data_collection = db["data"]

    return data_collection.insert_one(
        {
            "settings_id": settings,
            "name": "Numeric data",
            "type": "xy_plot",
            "x": [1.0, 2.0, 3.0],
            "y": [1.0, 4.0, 9.0],
        }
    ).inserted_id


@pytest.mark.test_data_db
class TestDataDb:
    """Contains tests for testing data db."""

    def test_resolve_numeric_data(self, numeric_data):
        """Test numeric data is resolved."""
        data_obj = Data.objects.get(id=numeric_data)
        numeric = data_obj.resolve()

        assert isinstance(numeric, NumericData)

    def test_resolve_array_data(self, array_data):
        """Test array data is resolved correctly."""
        data_obj = Data.objects.get(id=array_data)
        array = data_obj.resolve()

        assert isinstance(array, ArrayData)

    def test_resolve_xy_data(self, xy_data):
        """Test array data is resolved correctly."""
        data_obj = Data.objects.get(id=xy_data)
        xy = data_obj.resolve()

        assert isinstance(xy, XyData)

    def test_default_values(self, xy_data_default_values):
        """Test missing values are replaced with default values."""
        data_obj = Data.objects.get(id=xy_data_default_values)
        xy = data_obj.resolve()

        assert isinstance(xy.markers, list)
        assert xy.x_unit is None
        assert xy.y_unit is None

    def test_markers(self, xy_data):
        """Test markers are of Marker type."""
        data_obj = Data.objects.get(id=xy_data)
        xy = data_obj.resolve()

        assert isinstance(xy.markers[0], Marker)

    def test_settings(self, settings):
        """Test settings model."""
        settings = Settings.objects.get(id=settings)

        assert "set_1_1" in settings.settings
        assert "set_1_2" in settings.settings
        assert "set_2_1" in settings.settings

        assert isinstance(settings.settings["set_1_1"], Setting)
        assert isinstance(settings.settings["set_1_2"], Setting)
        assert isinstance(settings.settings["set_2_1"], Setting)
