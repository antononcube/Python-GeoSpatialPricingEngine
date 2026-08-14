from __future__ import annotations

from collections.abc import Mapping
from numbers import Real
from typing import Any

from .postgresql_access import PostgreSQLAccess


class GeoTaxonomy:
    def __init__(self, data: Any = None) -> None:
        self._data = data
        self._tile_diameter: float | None = None

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

    @property
    def tile_diameter(self) -> float | None:
        return self._tile_diameter

    @tile_diameter.setter
    def tile_diameter(self, value: float | None) -> None:
        if value is not None and not isinstance(value, Real):
            raise TypeError("tile_diameter must be a number or None")
        self._tile_diameter = value

    def get_tile_diameter(self) -> float | None:
        return self.tile_diameter

    def set_tile_diameter(self, value: float | None) -> None:
        self.tile_diameter = value

    def tile_area(self, tile_id: str) -> float:
        """Return the planar area of a tile polygon using the shoelace formula."""
        if self.data is None:
            raise ValueError("Geo taxonomy has no tile data")

        for record in self.data.to_dict(orient="records"):
            normalized = {str(key).lower(): value for key, value in record.items()}
            identifier = normalized.get("tile_id", normalized.get("tag"))
            if str(identifier) == str(tile_id):
                coordinates = normalized.get("coordinates")
                break
        else:
            raise KeyError(f"Unknown tile ID: {tile_id}")

        if not isinstance(coordinates, (list, tuple)) or len(coordinates) < 3:
            raise ValueError(f"Tile {tile_id!r} must have at least three coordinates")
        try:
            vertices = [(float(point[0]), float(point[1])) for point in coordinates]
        except (IndexError, TypeError, ValueError) as error:
            raise ValueError(f"Tile {tile_id!r} has invalid coordinates") from error

        return abs(
            sum(
                x1 * y2 - x2 * y1
                for (x1, y1), (x2, y2) in zip(
                    vertices, vertices[1:] + vertices[:1]
                )
            )
        ) / 2.0

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
    def read_sql(cls, connection: Any, geo_taxonomy_id: str) -> "GeoTaxonomy":
        if hasattr(connection, "import_geo_taxonomy") and callable(
            connection.import_geo_taxonomy
        ):
            dataframe = connection.import_geo_taxonomy(geo_taxonomy_id)
        elif isinstance(connection, Mapping):
            with PostgreSQLAccess(connection) as database_access:
                dataframe = database_access.import_geo_taxonomy(geo_taxonomy_id)
        elif connection is None:
            db_config: Mapping[str, Any] = {
                "dbname": "geo_spatial_pricing_engine",
                "user": "postgres",
                "password": "",
                "host": "localhost",
                "port": "5432",
            }
            with PostgreSQLAccess(db_config) as database_access:
                dataframe = database_access.import_geo_taxonomy(geo_taxonomy_id)
        else:
            raise TypeError(
                "connection must be PostgreSQLAccess, mapping config, or None"
            )

        return cls(dataframe)
