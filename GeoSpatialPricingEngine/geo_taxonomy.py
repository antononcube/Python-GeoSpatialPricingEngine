from __future__ import annotations

from typing import Any


class GeoTaxonomy:
    def __init__(self, data: Any = None) -> None:
        self._data = data

    @property
    def data(self) -> Any:
        return self._data

    @data.setter
    def data(self, value: Any) -> None:
        self._data = value

    def get_data(self) -> Any:
        return self.data

    def set_data(self, value: Any) -> None:
        self.data = value

    @classmethod
    def read_csv(cls, path: str, **kwargs: Any) -> "GeoTaxonomy":
        raise NotImplementedError

    @classmethod
    def read_json(cls, path: str, **kwargs: Any) -> "GeoTaxonomy":
        raise NotImplementedError

    @classmethod
    def read_dataframe(cls, dataframe: Any) -> "GeoTaxonomy":
        raise NotImplementedError
