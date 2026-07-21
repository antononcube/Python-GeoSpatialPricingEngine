from __future__ import annotations

from typing import Any

from .pricing_engine import PricingEngine


class PricingEngineExtrapolator:
    def __init__(self, pricing_engine: PricingEngine | None = None) -> None:
        self._pricing_engine = pricing_engine

    @property
    def pricing_engine(self) -> PricingEngine | None:
        return self._pricing_engine

    @pricing_engine.setter
    def pricing_engine(self, value: PricingEngine | None) -> None:
        self._pricing_engine = value

    def get_pricing_engine(self) -> PricingEngine | None:
        return self.pricing_engine

    def set_pricing_engine(self, value: PricingEngine | None) -> None:
        self.pricing_engine = value

    def post_process(self, **kwargs: Any) -> PricingEngine | None:
        raise NotImplementedError
