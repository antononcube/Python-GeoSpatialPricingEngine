from __future__ import annotations

from typing import Any

from .orders import Orders
from .pricing_engine import PricingEngine
from .tiled_region import TiledRegion


class PricingEngineCalibrator:
    def __init__(
        self,
        orders: Orders,
        tiled_region: TiledRegion,
        pricing_engine: PricingEngine,
    ) -> None:
        self._orders = orders
        self._tiled_region = tiled_region
        self._pricing_engine = pricing_engine

    @property
    def orders(self) -> Orders:
        return self._orders

    @orders.setter
    def orders(self, value: Orders) -> None:
        self._orders = value

    @property
    def tiled_region(self) -> TiledRegion:
        return self._tiled_region

    @tiled_region.setter
    def tiled_region(self, value: TiledRegion) -> None:
        self._tiled_region = value

    @property
    def pricing_engine(self) -> PricingEngine:
        return self._pricing_engine

    @pricing_engine.setter
    def pricing_engine(self, value: PricingEngine) -> None:
        self._pricing_engine = value

    def get_orders(self) -> Orders:
        return self.orders

    def set_orders(self, value: Orders) -> None:
        self.orders = value

    def get_tiled_region(self) -> TiledRegion:
        return self.tiled_region

    def set_tiled_region(self, value: TiledRegion) -> None:
        self.tiled_region = value

    def get_pricing_engine(self) -> PricingEngine:
        return self.pricing_engine

    def set_pricing_engine(self, value: PricingEngine) -> None:
        self.pricing_engine = value

    def calibrate(self, **kwargs: Any) -> PricingEngine:
        raise NotImplementedError
