from __future__ import annotations

from collections.abc import Mapping, Sequence
import json
from typing import Any
import pandas as pd
from psycopg import sql

DB_CONFIG_KEYS = ("dbname", "user", "password", "host", "port")


class PostgreSQLAccess:
    """Encapsulate PostgreSQL connections and imports into pandas DataFrames."""

    def __init__(self, db_config: Mapping[str, Any]) -> None:
        missing_keys = [key for key in DB_CONFIG_KEYS if key not in db_config]
        if missing_keys:
            missing = ", ".join(missing_keys)
            raise ValueError(f"Missing database configuration keys: {missing}")

        self._dbname = db_config["dbname"]
        self._user = db_config["user"]
        self._password = db_config["password"]
        self._host = db_config["host"]
        self._port = db_config["port"]
        self._connection: Any = None

    @property
    def dbname(self) -> Any:
        return self._dbname

    @dbname.setter
    def dbname(self, value: Any) -> None:
        self._dbname = value

    def get_dbname(self) -> Any:
        return self.dbname

    def set_dbname(self, value: Any) -> None:
        self.dbname = value

    @property
    def user(self) -> Any:
        return self._user

    @user.setter
    def user(self, value: Any) -> None:
        self._user = value

    def get_user(self) -> Any:
        return self.user

    def set_user(self, value: Any) -> None:
        self.user = value

    @property
    def password(self) -> Any:
        return self._password

    @password.setter
    def password(self, value: Any) -> None:
        self._password = value

    def get_password(self) -> Any:
        return self.password

    def set_password(self, value: Any) -> None:
        self.password = value

    @property
    def host(self) -> Any:
        return self._host

    @host.setter
    def host(self, value: Any) -> None:
        self._host = value

    def get_host(self) -> Any:
        return self.host

    def set_host(self, value: Any) -> None:
        self.host = value

    @property
    def port(self) -> Any:
        return self._port

    @port.setter
    def port(self, value: Any) -> None:
        self._port = value

    def get_port(self) -> Any:
        return self.port

    def set_port(self, value: Any) -> None:
        self.port = value

    @property
    def db_config(self) -> dict[str, Any]:
        return {
            "dbname": self.dbname,
            "user": self.user,
            "password": self.password,
            "host": self.host,
            "port": self.port,
        }

    def get_db_config(self) -> dict[str, Any]:
        return self.db_config

    def connect(self) -> Any:
        if self._connection is None or self._connection.closed:
            import psycopg

            self._connection = psycopg.connect(**self.db_config)
        return self._connection

    def close(self) -> None:
        if self._connection is not None and not self._connection.closed:
            self._connection.close()

    def import_dataframe(
        self,
        query: Any,
        params: Sequence[Any] | Mapping[str, Any] | None = None,
        column_names: Sequence[str] | Mapping[str, str] | None = None,
    ) -> Any:
        """Execute a query and return its rows as a pandas DataFrame."""
        connection = self.connect()
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            database_column_names = [column.name for column in cursor.description]

        if isinstance(column_names, Mapping):
            dataframe = pd.DataFrame(rows, columns=database_column_names)
            return dataframe.rename(columns=dict(column_names))

        dataframe_column_names = (
            database_column_names if column_names is None else list(column_names)
        )
        if len(dataframe_column_names) != len(database_column_names):
            raise ValueError("column_names must match the query column count")
        return pd.DataFrame(rows, columns=dataframe_column_names)

    def import_table(
        self,
        table_name: str,
        column_names: Sequence[str] | Mapping[str, str] | None = None,
        schema: str | None = None,
    ) -> Any:
        """Import all rows from a table using safely quoted identifiers."""
        table_identifier = (
            sql.Identifier(schema, table_name)
            if schema is not None
            else sql.Identifier(table_name)
        )
        query = sql.SQL("SELECT * FROM {}").format(table_identifier)
        return self.import_dataframe(query, column_names=column_names)

    def import_geo_taxonomy(self, geo_taxonomy_id: str) -> Any:
        """Import a geo taxonomy by ID and parse coordinates JSON arrays."""
        query = sql.SQL(
            "SELECT * FROM {} WHERE {} = %s"
        ).format(
            sql.Identifier("geo_taxonomy"),
            sql.Identifier("geo_taxonomy_id"),
        )
        dataframe = self.import_dataframe(query, params=(geo_taxonomy_id,))

        for column_name in ("id", "geo_taxonomy_id", "tile_id"):
            if column_name in dataframe.columns:
                dataframe[column_name] = dataframe[column_name].astype("string")

        for column_name in ("center_lat", "center_lon"):
            if column_name in dataframe.columns:
                dataframe[column_name] = pd.to_numeric(
                    dataframe[column_name], errors="raise"
                )

        if "coordinates" in dataframe.columns:

            def _parse_coordinates(value: Any) -> Any:
                if pd.isna(value):
                    return value
                if isinstance(value, str):
                    parsed = json.loads(value)
                    if not isinstance(parsed, list):
                        raise ValueError(
                            "coordinates must decode to a JSON array"
                        )
                    return parsed
                if isinstance(value, tuple):
                    return list(value)
                return value

            dataframe["coordinates"] = dataframe["coordinates"].apply(_parse_coordinates)

        return dataframe

    def __enter__(self) -> "PostgreSQLAccess":
        self.connect()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.close()
