from __future__ import annotations

from typing import Any

from .geo_point import GeoPoint


class PricingEngine:
    def __init__(self, parameters: Any = None) -> None:
        self._parameters = parameters

    @property
    def parameters(self) -> Any:
        return self._parameters

    @parameters.setter
    def parameters(self, value: Any) -> None:
        self._parameters = value

    def get_parameters(self) -> Any:
        return self.parameters

    def set_parameters(self, value: Any) -> None:
        self.parameters = value

    def compute_price(
        self, start: GeoPoint, end: GeoPoint, distance: float | None = None
    ) -> float:
        raise NotImplementedError

    def compute_price_for_coords(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
        distance: float | None = None,
    ) -> float:
        raise NotImplementedError
