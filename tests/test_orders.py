import pytest

pytest.importorskip("pandas")
package = pytest.importorskip("GeoSpatialPricingEngine")

import pandas as pd
import numpy as np

Orders = package.Orders


class ConcreteOrders(Orders):
    def ingest_csv(self, path: str, **kwargs):
        raise NotImplementedError

    def ingest_json(self, path: str, **kwargs):
        raise NotImplementedError


class _FakePostgreSQLAccess:
    def __init__(self, db_config):
        self.db_config = db_config
        self.last_transportation_trips_id = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return None

    def import_transportation_trips(self, transportation_trips_id):
        self.last_transportation_trips_id = transportation_trips_id
        return pd.DataFrame(
            [
                {
                    "id": "1",
                    "transportation_trips_id": transportation_trips_id,
                    "start_lat": 10.0,
                    "start_lon": 20.0,
                    "end_lat": 30.0,
                    "end_lon": 40.0,
                    "distance": 100.0,
                    "price": 250.0,
                    "is_training": True,
                }
            ]
        )


def test_ingest_db_uses_default_db_config(monkeypatch):
    captured = {}

    def _fake_constructor(db_config):
        captured["db_config"] = db_config
        access = _FakePostgreSQLAccess(db_config)
        captured["access"] = access
        return access

    monkeypatch.setattr(
        "GeoSpatialPricingEngine.orders.PostgreSQLAccess",
        _fake_constructor,
    )

    orders = ConcreteOrders()
    dataframe = orders.ingest_db(None, transportation_trips_id="FAFDerivedLinear")

    assert captured["db_config"] == {
        "dbname": "geo_spatial_pricing_engine",
        "user": "postgres",
        "password": "",
        "host": "localhost",
        "port": "5432",
    }
    assert captured["access"].last_transportation_trips_id == "FAFDerivedLinear"
    assert dataframe.loc[0, "is_training"] is np.True_
    assert orders.data.equals(dataframe)
