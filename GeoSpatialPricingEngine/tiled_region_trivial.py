from __future__ import annotations

from typing import Any

from .geo_point import GeoPoint
from .tiled_region import TiledRegion


class TiledRegionTrivial(TiledRegion):
    def find_path(self, start: GeoPoint, end: GeoPoint) -> Any:
        raise NotImplementedError

    def find_path_for_coords(
        self, x1: float, y1: float, x2: float, y2: float
    ) -> Any:
        raise NotImplementedError
