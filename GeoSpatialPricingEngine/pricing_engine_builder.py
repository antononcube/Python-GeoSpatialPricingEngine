from __future__ import annotations

import json
from copy import deepcopy
from os import PathLike
from pathlib import Path
from typing import Any

from .geo_taxonomy import GeoTaxonomy
from .orders import Orders
from .tiled_region_trivial import TiledRegionTrivial


class _BuilderOrders(Orders):
    def ingest_csv(self, path: str, **kwargs: Any) -> Any:
        raise NotImplementedError(
            "CSV order ingestion is not supported by the builder"
        )

    def ingest_json(self, path: str, **kwargs: Any) -> Any:
        raise NotImplementedError(
            "JSON order ingestion is not supported by the builder"
        )

class PricingEngineBuilder:
    DEFAULT_SPEC_PATH = (
        Path(__file__).resolve().parents[1]
        / "resources"
        / "PricingEngineCalibrationSpec.json"
    )

    def __init__(self, spec: Any = None) -> None:
        self._spec = spec
        self.geo_taxonomy: GeoTaxonomy | None = None
        self.orders: Orders | None = None
        self.tiled_region: TiledRegionTrivial | None = None
        self.calibration_records: dict[str, dict[str, Any]] | None = None

    @property
    def spec(self) -> Any:
        return self._spec

    @spec.setter
    def spec(self, value: Any) -> None:
        self._spec = value

    def get_spec(self) -> Any:
        return self.spec

    def set_spec(self, value: Any) -> None:
        self.spec = value

    @classmethod
    def build_from_json(
        cls, file_path: str | PathLike[str]
    ) -> "PricingEngineBuilder":
        path = Path(file_path)
        user_spec = cls._load_json_file(path)
        default_spec = cls._load_json_file(cls.DEFAULT_SPEC_PATH)

        if not isinstance(user_spec, dict):
            raise ValueError(f"JSON specification must be a dictionary: {path}")
        if not isinstance(default_spec, dict):
            raise ValueError(
                "Default JSON specification must be a dictionary: "
                f"{cls.DEFAULT_SPEC_PATH}"
            )

        spec = cls._merge_specs(default_spec, user_spec)
        path_strategy = spec.get("model", {}).get("path_strategy")
        if path_strategy != "trivial-path":
            raise ValueError(
                "Unsupported model.path_strategy "
                f"{path_strategy!r}; only 'trivial-path' is supported"
            )

        builder = cls(spec)
        database = spec.get("database")
        taxonomy_spec = spec.get("retrieve_geo_taxonomy", {})
        if taxonomy_spec.get("source") != "postgresql":
            raise ValueError(
                "Unsupported retrieve_geo_taxonomy.source: "
                f"{taxonomy_spec.get('source')!r}"
            )
        builder.geo_taxonomy = GeoTaxonomy.read_sql(
            database, taxonomy_spec["geo_taxonomy_id"]
        )

        orders_spec = spec.get("ingest_orders", {})
        if orders_spec.get("source") != "postgresql":
            raise ValueError(
                "Unsupported ingest_orders.source: "
                f"{orders_spec.get('source')!r}"
            )
        builder.orders = _BuilderOrders()
        builder.orders.ingest_db(
            database, orders_spec["transportation_trips_id"]
        )

        builder.tiled_region = TiledRegionTrivial(builder.geo_taxonomy)
        builder.calibration_records = builder.tiled_region.to_calibration_records(
            builder.orders
        )
        return builder

    @staticmethod
    def _load_json_file(path: Path) -> Any:
        if not path.is_file():
            raise FileNotFoundError(f"JSON specification file does not exist: {path}")

        try:
            with path.open(encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"JSON specification file is not valid JSON: {path}"
            ) from error

    @staticmethod
    def _merge_specs(
        default_spec: dict[str, Any], user_spec: dict[str, Any]
    ) -> dict[str, Any]:
        merged_spec = deepcopy(default_spec)
        for key, value in user_spec.items():
            if isinstance(value, dict) and isinstance(merged_spec.get(key), dict):
                merged_spec[key] = PricingEngineBuilder._merge_specs(
                    merged_spec[key], value
                )
            else:
                merged_spec[key] = deepcopy(value)
        return merged_spec

    def retrieve_geo_taxonomy(self, **kwargs: Any) -> Any:
        raise NotImplementedError

    def ingest_orders(self, **kwargs: Any) -> Any:
        raise NotImplementedError

    def calibrate(self, **kwargs: Any) -> Any:
        raise NotImplementedError

    def post_process(self, **kwargs: Any) -> Any:
        raise NotImplementedError
