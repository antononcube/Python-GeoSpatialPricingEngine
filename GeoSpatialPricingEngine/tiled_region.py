from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from GeometricNearestNeighborsProcessor import (
    GeometricNearestNeighborsProcessor,
)

from .geo_point import GeoPoint
from .geo_taxonomy import GeoTaxonomy
from .orders import Orders


class TiledRegion(ABC):
    def __init__(self, geo_taxonomy: GeoTaxonomy) -> None:
        self._geo_taxonomy = geo_taxonomy
        self._tile_mapper: Any = None

    @property
    def geo_taxonomy(self) -> GeoTaxonomy:
        return self._geo_taxonomy

    @geo_taxonomy.setter
    def geo_taxonomy(self, value: GeoTaxonomy) -> None:
        self._geo_taxonomy = value
        self._tile_mapper = None

    def get_geo_taxonomy(self) -> GeoTaxonomy:
        return self.geo_taxonomy

    def set_geo_taxonomy(self, value: GeoTaxonomy) -> None:
        self.geo_taxonomy = value

    def tile_for_point(self, point: GeoPoint) -> Any:
        if not isinstance(point, GeoPoint):
            raise TypeError("'point' must be a GeoPoint instance")

        return self.tile_for_coords(point.x, point.y)

    def tile_for_coords(self, x: float, y: float) -> Any:
        mapper = self._get_tile_mapper()
        nearest = mapper.find_nearest(point=(x, y), n=1).take_value()
        return nearest["ID"][0]

    def _get_tile_mapper(self) -> Any:
        if self._tile_mapper is None:
            taxonomy_data = self.geo_taxonomy.data
            records = taxonomy_data.to_dict(orient="records")
            tile_centers = {
                record["tile_id"]: (
                    record["center_lat"],
                    record["center_lon"],
                )
                for record in records
            }
            self._tile_mapper = GeometricNearestNeighborsProcessor(tile_centers)

        return self._tile_mapper

    @abstractmethod
    def find_path(self, start: GeoPoint, end: GeoPoint) -> Any:
        raise NotImplementedError

    @abstractmethod
    def find_path_for_coords(
        self, x1: float, y1: float, x2: float, y2: float
    ) -> Any:
        raise NotImplementedError

    def to_calibration_records(self, orders: Orders) -> dict[str, dict[str, Any]]:
        calibration_records = {}
        for order in orders.data.to_dict(orient="records"):
            order_id = order["id"]
            calibration_records[str(order_id)] = {
                "id": order_id,
                "path": self.find_path_for_coords(
                    order["start_lat"],
                    order["start_lon"],
                    order["end_lat"],
                    order["end_lon"],
                ),
                "distance": order["distance"],
                "price": order["price"],
            }

        return calibration_records