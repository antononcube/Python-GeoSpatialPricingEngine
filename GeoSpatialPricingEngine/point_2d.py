from __future__ import annotations

import math
from typing import Union


PointLike = Union["Point2D", tuple[float, float]]


class Point2D:
    def __init__(self, x: float, y: float) -> None:
        self._x = x
        self._y = y

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = value

    def get_x(self) -> float:
        return self.x

    def set_x(self, value: float) -> None:
        self.x = value

    def get_y(self) -> float:
        return self.y

    def set_y(self, value: float) -> None:
        self.y = value

    def norm(self) -> float:
        return math.hypot(self.x, self.y)

    def dot_product(self, other: PointLike) -> float:
        if isinstance(other, Point2D):
            other_x, other_y = other.x, other.y
        elif isinstance(other, tuple) and len(other) == 2:
            other_x, other_y = other
        else:
            raise TypeError(
                "'other' must be a Point2D instance or a 2-item tuple of coordinates"
            )

        return (self.x * other_x) + (self.y * other_y)

    def distance_to(self, other: "Point2D") -> float:
        if not isinstance(other, Point2D):
            raise TypeError("'other' must be a Point2D instance")

        return math.hypot(self.x - other.x, self.y - other.y)
