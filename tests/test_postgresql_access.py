import pytest

pytest.importorskip("pandas")
pytest.importorskip("psycopg")

from GeoSpatialPricingEngine import PostgreSQLAccess


DB_CONFIG = {
    "dbname": "geo_spatial_pricing_engine",
    "user": "postgres",
    "password": "",
    "host": "localhost",
    "port": "5432",
}


@pytest.fixture
def database_access():
    access = PostgreSQLAccess(DB_CONFIG)
    yield access
    access.close()


def test_import_geo_taxonomy(database_access):
    query = """
        SELECT * FROM geo_taxonomy WHERE geo_taxonomy_id = 'Hextile1deg'
    """
    expected_columns = [
        "id",
        "geo_taxonomy_id",
        "tile_id",
        "center_lat",
        "center_lon",
        "coordinates",
    ]

    dataframe = database_access.import_dataframe(query)

    assert len(dataframe) > 1000
    assert list(dataframe.columns) == expected_columns


def test_import_raw_transportation_trips(database_access):
    query = """
        SELECT * FROM raw_transportation_trips
        WHERE raw_transportation_trips_id = 'FAFDerived'
    """
    expected_columns = [
        "id",
        "raw_transportation_trips_id",
        "start_lat",
        "start_lon",
        "start_state",
        "start_city",
        "start_zip_code",
        "end_lat",
        "end_lon",
        "end_state",
        "end_city",
        "end_zip_code",
        "distance",
        "price",
    ]

    dataframe = database_access.import_dataframe(query)

    assert len(dataframe) > 4000
    assert list(dataframe.columns) == expected_columns


def test_import_transportation_trips_types_are_parsed(monkeypatch):
    access = PostgreSQLAccess(DB_CONFIG)

    def _fake_import_dataframe(query, params=None, column_names=None):
        assert params == ("FAFDerivedLinear",)
        return pd.DataFrame(
            [
                {
                    "id": "1",
                    "transportation_trips_id": "FAFDerivedLinear",
                    "start_lat": "10.5",
                    "start_lon": "20.5",
                    "end_lat": "30.5",
                    "end_lon": "40.5",
                    "distance": "99.9",
                    "price": "123.45",
                    "is_training": "true",
                }
            ]
        )

    monkeypatch.setattr(access, "import_dataframe", _fake_import_dataframe)

    dataframe = access.import_transportation_trips("FAFDerivedLinear")

    assert dataframe.loc[0, "id"] == "1"
    assert dataframe.loc[0, "transportation_trips_id"] == "FAFDerivedLinear"
    assert dataframe.loc[0, "start_lat"] == pytest.approx(10.5)
    assert dataframe.loc[0, "start_lon"] == pytest.approx(20.5)
    assert dataframe.loc[0, "end_lat"] == pytest.approx(30.5)
    assert dataframe.loc[0, "end_lon"] == pytest.approx(40.5)
    assert dataframe.loc[0, "distance"] == pytest.approx(99.9)
    assert dataframe.loc[0, "price"] == pytest.approx(123.45)
    assert dataframe.loc[0, "is_training"] is True
