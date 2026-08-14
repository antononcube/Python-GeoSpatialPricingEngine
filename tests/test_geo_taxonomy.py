import pytest
import types
from math import pi, sqrt

pytest.importorskip("pandas")
package = pytest.importorskip("GeoSpatialPricingEngine")

import pandas as pd

GeoTaxonomy = package.GeoTaxonomy
PricingEngine = package.PricingEngine
PricingEngineCalibrator = package.PricingEngineCalibrator


class _FakePostgreSQLAccess:
    def __init__(self, db_config):
        self.db_config = db_config
        self.last_geo_taxonomy_id = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return None

    def import_geo_taxonomy(self, geo_taxonomy_id):
        self.last_geo_taxonomy_id = geo_taxonomy_id
        return pd.DataFrame(
            [
                {
                    "id": "1",
                    "geo_taxonomy_id": geo_taxonomy_id,
                    "tile_id": "tile-1",
                    "center_lat": 12.3,
                    "center_lon": 45.6,
                    "coordinates": [[1.0, 2.0], [3.0, 4.0]],
                }
            ]
        )


def test_read_sql_imports_geo_taxonomy(monkeypatch):
    captured = {}

    def _fake_constructor(db_config):
        captured["db_config"] = db_config
        access = _FakePostgreSQLAccess(db_config)
        captured["access"] = access
        return access

    monkeypatch.setattr(
        "GeoSpatialPricingEngine.geo_taxonomy.PostgreSQLAccess",
        _fake_constructor,
    )

    geo_taxonomy = GeoTaxonomy.read_sql(None, "Hextile1deg")

    assert captured["db_config"] == {
        "dbname": "geo_spatial_pricing_engine",
        "user": "postgres",
        "password": "",
        "host": "localhost",
        "port": "5432",
    }
    assert captured["access"].last_geo_taxonomy_id == "Hextile1deg"
    assert isinstance(geo_taxonomy.data, pd.DataFrame)
    assert geo_taxonomy.data.loc[0, "coordinates"] == [[1.0, 2.0], [3.0, 4.0]]


def test_tile_area_and_calibration_diameter_precedence():
    taxonomy = GeoTaxonomy(
        pd.DataFrame(
            [
                {
                    "tile_id": "tile-1",
                    "center_lat": 0.5,
                    "center_lon": 0.5,
                    "coordinates": [[0, 0], [1, 0], [1, 1], [0, 1]],
                }
            ]
        )
    )
    calibrator = PricingEngineCalibrator(
        types.SimpleNamespace(),
        types.SimpleNamespace(geo_taxonomy=taxonomy),
        PricingEngine(),
    )

    assert taxonomy.tile_diameter is None
    assert taxonomy.tile_area("tile-1") == pytest.approx(1.0)
    assert calibrator._tile_data()["tile-1"]["diameter"] == pytest.approx(
        2.0 / sqrt(pi)
    )

    taxonomy.set_tile_diameter(7.5)

    assert taxonomy.get_tile_diameter() == 7.5
    assert calibrator._tile_data()["tile-1"]["diameter"] == 7.5
