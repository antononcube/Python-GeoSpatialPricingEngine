import types

import pytest

pytest.importorskip("ortools")

from GeoSpatialPricingEngine import PricingEngine, PricingEngineCalibrator


class _Table:
    def __init__(self, records):
        self.records = records

    def to_dict(self, orient):
        assert orient == "records"
        return self.records


def test_distance_only_calibration_fits_linear_trip_prices():
    orders = types.SimpleNamespace(
        data=_Table([
            {"id": "one", "is_training": True},
            {"id": "two", "is_training": True},
        ])
    )
    tiled_region = types.SimpleNamespace(
        geo_taxonomy=types.SimpleNamespace(data=_Table([]))
    )
    calibration_records = {
        "one": {"id": "one", "path": ["a", "b"], "distance": 10, "price": 23},
        "two": {"id": "two", "path": ["a", "b"], "distance": 20, "price": 43},
    }
    spec = {
        "model": {"distance_only_formula": True},
        "ingest_orders": {"split_training_testing": True},
        "calibration": {
            "objective_norm": "l1",
            "parameter_bounds": {
                "k": {"min": 0, "max": 10},
                "n": {"min": -100, "max": 100},
            },
        },
    }

    engine = PricingEngine()
    calibrated = PricingEngineCalibrator(orders, tiled_region, engine).calibrate(
        spec=spec, calibration_records=calibration_records
    )

    assert calibrated is engine
    assert engine.parameters["mode"] == "distance_only"
    assert engine.parameters["k"] == pytest.approx(2.0)
    assert engine.parameters["n"] == pytest.approx(3.0)
    assert engine.parameters["objective_value"] == pytest.approx(0.0)
