from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .postgresql_access import PostgreSQLAccess


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

    @classmethod
    def read_sql(cls, geo_taxonomy_id: str) -> "GeoTaxonomy":
        db_config: Mapping[str, Any] = {
            "dbname": "geo_spatial_pricing_engine",
            "user": "postgres",
            "password": "",
            "host": "localhost",
            "port": "5432",
        }

        with PostgreSQLAccess(db_config) as database_access:
            dataframe = database_access.import_geo_taxonomy(geo_taxonomy_id)
        return cls(dataframe)
