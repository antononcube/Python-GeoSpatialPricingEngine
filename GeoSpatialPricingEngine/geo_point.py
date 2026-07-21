from __future__ import annotations

from .point_2d import Point2D


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
        raise NotImplementedError

    def distance_miles(self, other: "GeoPoint") -> float:
        raise NotImplementedError

    def distance_km(self, other: "GeoPoint") -> float:
        raise NotImplementedError
