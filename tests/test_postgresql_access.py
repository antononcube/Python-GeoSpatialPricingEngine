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
