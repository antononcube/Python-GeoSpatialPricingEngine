from __future__ import annotations

from typing import Any

from .pricing_engine import PricingEngine


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
    def build_from_json(cls, spec: Any) -> PricingEngine:
        raise NotImplementedError

    def retrieve_geo_taxonomy(self, **kwargs: Any) -> Any:
        raise NotImplementedError

    def ingest_orders(self, **kwargs: Any) -> Any:
        raise NotImplementedError

    def calibrate(self, **kwargs: Any) -> Any:
        raise NotImplementedError

    def post_process(self, **kwargs: Any) -> Any:
        raise NotImplementedError
