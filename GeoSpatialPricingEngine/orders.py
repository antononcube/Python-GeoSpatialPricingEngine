from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Orders(ABC):
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

    @abstractmethod
    def ingest_csv(self, path: str, **kwargs: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    def ingest_json(self, path: str, **kwargs: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    def ingest_db(self, connection: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
