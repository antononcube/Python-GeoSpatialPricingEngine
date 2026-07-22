from __future__ import annotations

import math

from .point_2d import Point2D


EARTH_RADIUS_MILES = 3958.7613
EARTH_RADIUS_KM = 6371.0088


class GeoPoint(Point2D):
    def __init__(self, x: float, y: float, id: str | int | None = None) -> None:
        super().__init__(x, y)
        self._id = id

    @property
    def id(self) -> str | int | None:
        return self._id

    @id.setter
    def id(self, value: str | int | None) -> None:
        self._id = value

    def get_id(self) -> str | int | None:
        return self.id

    def set_id(self, value: str | int | None) -> None:
        self.id = value

    def __str__(self) -> str:
        return f"GeoPoint(id={self.id}, x={self.x}, y={self.y})"

    def distance_miles(self, other: "GeoPoint") -> float:
        return self._distance_in_units(other, EARTH_RADIUS_MILES)

    def distance_km(self, other: "GeoPoint") -> float:
        return self._distance_in_units(other, EARTH_RADIUS_KM)

    def _distance_in_units(self, other: "GeoPoint", earth_radius: float) -> float:
        central_angle = self._central_angle_radians(other)
        return earth_radius * central_angle

    def _central_angle_radians(self, other: "GeoPoint") -> float:
        if not isinstance(other, GeoPoint):
            raise TypeError("'other' must be a GeoPoint instance")

        lat1 = math.radians(self.x)
        lon1 = math.radians(self.y)
        lat2 = math.radians(other.x)
        lon2 = math.radians(other.y)

        delta_lat = lat2 - lat1
        delta_lon = lon2 - lon1

        haversine = (
            math.sin(delta_lat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2) ** 2
        )
        haversine = min(1.0, max(0.0, haversine))

        return 2.0 * math.asin(math.sqrt(haversine))
