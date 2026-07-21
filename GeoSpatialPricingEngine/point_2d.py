from __future__ import annotations

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
        raise NotImplementedError

    def dot_product(self, other: PointLike) -> float:
        raise NotImplementedError

    def distance_to(self, other: "Point2D") -> float:
        raise NotImplementedError
