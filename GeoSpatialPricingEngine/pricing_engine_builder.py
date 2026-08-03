from __future__ import annotations

import json
from os import PathLike
from pathlib import Path
from typing import Any


class PricingEngineBuilder:
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
        if not path.is_file():
            raise FileNotFoundError(f"JSON specification file does not exist: {path}")

        try:
            with path.open(encoding="utf-8") as file:
                spec = json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"JSON specification file is not valid JSON: {path}"
            ) from error

        return cls(spec)

    def retrieve_geo_taxonomy(self, **kwargs: Any) -> Any:
        raise NotImplementedError

    def ingest_orders(self, **kwargs: Any) -> Any:
        raise NotImplementedError

    def calibrate(self, **kwargs: Any) -> Any:
        raise NotImplementedError

    def post_process(self, **kwargs: Any) -> Any:
        raise NotImplementedError
