import json

import pytest

pytest.importorskip("psycopg")

from GeoSpatialPricingEngine import PricingEngineBuilder


def test_build_from_json_loads_spec(tmp_path):
    spec = {"pricing_engine_id": "example", "calibration": {"objective_norm": "l1"}}
    spec_path = tmp_path / "pricing-engine-spec.json"
    spec_path.write_text(json.dumps(spec), encoding="utf-8")

    builder = PricingEngineBuilder.build_from_json(spec_path)

    assert isinstance(builder, PricingEngineBuilder)
    assert builder.get_spec() == spec


def test_build_from_json_requires_existing_file(tmp_path):
    missing_path = tmp_path / "missing.json"

    with pytest.raises(FileNotFoundError, match="does not exist"):
        PricingEngineBuilder.build_from_json(missing_path)


def test_build_from_json_rejects_invalid_json(tmp_path):
    spec_path = tmp_path / "invalid.json"
    spec_path.write_text('{"pricing_engine_id":', encoding="utf-8")

    with pytest.raises(ValueError, match="not valid JSON"):
        PricingEngineBuilder.build_from_json(spec_path)
