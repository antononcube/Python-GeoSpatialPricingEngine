from __future__ import annotations

from typing import Any

from .geo_point import GeoPoint
from .tiled_region import TiledRegion


class TiledRegionGraph(TiledRegion):
    def __init__(
        self,
        geo_taxonomy: Any,
        coarse_graph: Any = None,
        fine_graph: Any = None,
    ) -> None:
        super().__init__(geo_taxonomy)
        self._coarse_graph = coarse_graph
        self._fine_graph = fine_graph

    @property
    def coarse_graph(self) -> Any:
        return self._coarse_graph

    @coarse_graph.setter
    def coarse_graph(self, value: Any) -> None:
        self._coarse_graph = value

    @property
    def fine_graph(self) -> Any:
        return self._fine_graph

    @fine_graph.setter
    def fine_graph(self, value: Any) -> None:
        self._fine_graph = value

    def get_coarse_graph(self) -> Any:
        return self.coarse_graph

    def set_coarse_graph(self, value: Any) -> None:
        self.coarse_graph = value

    def get_fine_graph(self) -> Any:
        return self.fine_graph

    def set_fine_graph(self, value: Any) -> None:
        self.fine_graph = value

    def find_path(self, start: GeoPoint, end: GeoPoint) -> Any:
        raise NotImplementedError

    def find_path_for_coords(
        self, x1: float, y1: float, x2: float, y2: float
    ) -> Any:
        raise NotImplementedError
