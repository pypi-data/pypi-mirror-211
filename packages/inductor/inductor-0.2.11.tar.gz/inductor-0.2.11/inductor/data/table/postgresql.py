# Copyright 2022 Inductor, Inc.

"""Abstractions for PostgreSQL tables."""

from typing import Any, Dict, Iterable, Optional

import psycopg2
import sqlalchemy

from inductor.data.table import table
from inductor.data.table import sqlalchemy as table_sa


class PostgresqlView(table_sa.SqlAlchemyView):
    """A view of a PostgreSQL table."""

    def __init__(
        self,
        parent: "PostgresqlTable",
        query: table.SqlSelectQuery,
    ):
        """Constructs a new PostgresqlView instance.

        Args:
            parent: The underlying PostgresqlTable of which this
                instance is a view.
            query: The query (over parent) defining this view.
        """
        super().__init__(parent, query)

    def to_metadata(self) -> Dict[str, Any]:
        """See base class."""
        raise NotImplementedError()

    @staticmethod
    def from_metadata(metadata: Dict[str, Any]) -> table.Table:
        """See base class."""
        raise NotImplementedError()


class PostgresqlTable(table_sa.SqlAlchemyTable):
    """A Table backed by a PostgreSQL table."""

    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        database: str,
        table_name: str,
        indexed_columns: Iterable[str] = tuple(),
        port: Optional[int] = None,
        auto_ddl: bool = True,
        **kwargs,
    ):
        """Constructs a new PostgresqlTable instance.

        Args:
            host: Name of database server host hosting the PostgreSQL database
                containing this table.
            user: PostgreSQL database server username.
            password: Password for user.
            database: Name of database containing table.
            table_name: Name of table in database given by preceding arguments.
            indexed_columns: Names of columns that should be indexed for faster
                queries.
            port: Optionally, the port on which to connect to the database
                server.
            auto_ddl: Boolean value indicating whether or not to automatically
                execute DDL commands to create the table and add and modify
                columns.  If False, then no processing of retrieved rows to
                account for prior automatic DDL is performed.
            **kwargs: Additional parameters which should be passed to the
                constructor of the parent class.
        """
        sqlalchemy_url = sqlalchemy.URL.create(
            "postgresql+psycopg2",
            host=host,
            username=user,
            password=password,
            database=database,
            port=port,
        )
        super().__init__(
            **kwargs,
            table_name=table_name,
            sqlalchemy_url=sqlalchemy_url,
            indexed_columns=indexed_columns,
            auto_ddl=auto_ddl,
            include_index_postfix=False,
        )
        self._metadata = {
            "host": host,
            "user": user,
            "database": database,
            "table_name": table_name,
            "indexed_columns": list(indexed_columns),
            "auto_ddl": auto_ddl,
        }
        if port is not None:
            self._metadata["port"] = port

    def _is_undefined_column_error(
        self,
        error: sqlalchemy.exc.DBAPIError,
    ) -> bool:
        """See base class."""
        return isinstance(error.orig, psycopg2.errors.UndefinedColumn)  # pylint: disable=no-member

    def _standardize_value(self, value: Any) -> Any:
        """See base class."""
        if isinstance(value, memoryview):
            return value.tobytes()
        return value

    def _gen_view(
        self,
        query: table.SqlSelectQuery,
    ) -> table_sa.SqlAlchemyView:
        """See base class."""
        return PostgresqlView(self, query)

    def to_metadata(self) -> Dict[str, Any]:
        """See base class."""
        table_metadata = self._metadata.copy()
        if "password" in table_metadata:
            del table_metadata["password"]
        return table_metadata

    @staticmethod
    def from_metadata(metadata: Dict[str, Any]) -> "PostgresqlTable":
        """See base class."""
        table_metadata = metadata.copy()
        if "postgresql_password" in table_metadata:
            table_metadata["password"] = table_metadata["postgresql_password"]
            del table_metadata["postgresql_password"]
        return PostgresqlTable(**table_metadata)


class PostgresqlKeyedTable(PostgresqlTable, table_sa.SqlAlchemyKeyedTable):
    """A PostgresqlTable having a primary key."""

    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        database: str,
        table_name: str,
        primary_key_column: str,
        indexed_columns: Iterable[str] = tuple(),
        port: Optional[int] = None,
        auto_ddl: bool = True,
    ):
        """Constructs a new PostgresqlKeyedTable instance.

        Args:
            host: Name of database server host hosting the PostgreSQL database
                containing this table.
            user: PostgreSQL database server username.
            password: Password for user.
            database: Name of database containing table.
            table_name: Name of table in database given by preceding arguments.
            primary_key_column: Name of column containing primary key.
            indexed_columns: Names of columns that should be indexed for faster
                queries.
            port: Optionally, the port on which to connect to the database
                server.
            auto_ddl: Boolean value indicating whether or not to automatically
                execute DDL commands to create the table and add and modify
                columns.  If False, then no processing of retrieved rows to
                account for prior automatic DDL is performed.
        """
        super().__init__(
            host=host,
            user=user,
            password=password,
            database=database,
            table_name=table_name,
            indexed_columns=indexed_columns,
            port=port,
            auto_ddl=auto_ddl,
            primary_key_column=primary_key_column,
        )

    @property
    def _insert_skip_if_exists_suffix(self) -> str:
        """See base class."""
        return "ON CONFLICT DO NOTHING"

    def to_metadata(self) -> Dict[str, Any]:
        """See base class."""
        table_metadata = super().to_metadata().copy()
        table_metadata["primary_key_column"] = self.primary_key_column()
        return table_metadata

    @staticmethod
    def from_metadata(metadata: Dict[str, Any]) -> "PostgresqlKeyedTable":
        """See base class."""
        table_metadata = metadata.copy()
        if "postgresql_password" in table_metadata:
            table_metadata["password"] = table_metadata["postgresql_password"]
            del table_metadata["postgresql_password"]
        return PostgresqlKeyedTable(**table_metadata)
