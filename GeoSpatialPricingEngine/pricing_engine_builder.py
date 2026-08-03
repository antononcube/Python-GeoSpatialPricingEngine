from __future__ import annotations

import json
from copy import deepcopy
from os import PathLike
from pathlib import Path
from typing import Any


class PricingEngineBuilder:
    DEFAULT_SPEC_PATH = (
        Path(__file__).resolve().parents[1]
        / "resources"
        / "PricingEngineCalibrationSpec.json"
    )

    def __init__(self, spec: Any = None) -> None:
        self._spec = spec

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

        return cls(cls._merge_specs(default_spec, user_spec))

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
