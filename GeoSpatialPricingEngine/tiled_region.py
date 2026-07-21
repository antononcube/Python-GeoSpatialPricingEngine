from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .geo_point import GeoPoint
from .geo_taxonomy import GeoTaxonomy


class TiledRegion(ABC):
    def __init__(self, geo_taxonomy: GeoTaxonomy) -> None:
        self._geo_taxonomy = geo_taxonomy

    @property
    def geo_taxonomy(self) -> GeoTaxonomy:
        return self._geo_taxonomy

    @geo_taxonomy.setter
    def geo_taxonomy(self, value: GeoTaxonomy) -> None:
        self._geo_taxonomy = value

    def get_geo_taxonomy(self) -> GeoTaxonomy:
        return self.geo_taxonomy

    def set_geo_taxonomy(self, value: GeoTaxonomy) -> None:
        self.geo_taxonomy = value

    def tile_for_point(self, point: GeoPoint) -> Any:
        raise NotImplementedError

    def tile_for_coords(self, x: float, y: float) -> Any:
        raise NotImplementedError

    @abstractmethod
    def find_path(self, start: GeoPoint, end: GeoPoint) -> Any:
        raise NotImplementedError

    @abstractmethod
    def find_path_for_coords(
        self, x1: float, y1: float, x2: float, y2: float
    ) -> Any:
        raise NotImplementedError
