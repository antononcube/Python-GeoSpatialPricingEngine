from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Any

from .postgresql_access import PostgreSQLAccess


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

    def ingest_db(self, connection: Any, **kwargs: Any) -> Any:
        transportation_trips_id = kwargs.get("transportation_trips_id")
        if transportation_trips_id is None:
            raise ValueError("transportation_trips_id is required")

        if isinstance(connection, PostgreSQLAccess):
            dataframe = connection.import_transportation_trips(transportation_trips_id)
        elif isinstance(connection, Mapping):
            with PostgreSQLAccess(connection) as database_access:
                dataframe = database_access.import_transportation_trips(
                    transportation_trips_id
                )
        elif connection is None:
            db_config: Mapping[str, Any] = {
                "dbname": "geo_spatial_pricing_engine",
                "user": "postgres",
                "password": "",
                "host": "localhost",
                "port": "5432",
            }
            with PostgreSQLAccess(db_config) as database_access:
                dataframe = database_access.import_transportation_trips(
                    transportation_trips_id
                )
        else:
            raise TypeError(
                "connection must be PostgreSQLAccess, mapping config, or None"
            )

        self.data = dataframe
        return dataframe
