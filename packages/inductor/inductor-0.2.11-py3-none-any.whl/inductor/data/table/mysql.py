# Copyright 2022 Inductor, Inc.

"""Abstractions for MySQL tables."""

from typing import Any, Dict, Iterable, Optional

import sqlalchemy

from inductor.data.table import table
from inductor.data.table import sqlalchemy as table_sa


class MysqlView(table_sa.SqlAlchemyView):
    """A view of a MySQL table."""

    def __init__(
        self,
        parent: "MysqlTable",
        query: table.SqlSelectQuery,
    ):
        """Constructs a new MysqlView instance.

        Args:
            parent: The underlying MysqlTable of which this instance
                is a view.
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


class MysqlTable(table_sa.SqlAlchemyTable):
    """A Table backed by a MySQL table."""

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
        """Constructs a new MysqlTable instance.

        Args:
            host: Name of database server host hosting the MySQL database
                containing this table.
            user: MySQL database server username.
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
            "mysql+pymysql",
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
        )
        self._metadata = {
            "host": host,
            "user": user,
            "database": database,
            "table_name": table_name,
            "indexed_columns": list(indexed_columns),
            "auto_ddl": auto_ddl
        }
        if port is not None:
            self._metadata["port"] = port

    def _is_undefined_column_error(
        self, error: sqlalchemy.exc.DBAPIError
    ) -> bool:
        """See base class."""
        return "Unknown column" in error.args[0]

    def _gen_view(
        self,
        query: table.SqlSelectQuery,
    ) -> MysqlView:
        """See base class."""
        return MysqlView(self, query)

    def to_metadata(self) -> Dict[str, Any]:
        """See base class."""
        table_metadata = self._metadata.copy()
        if "password" in table_metadata:
            del table_metadata["password"]
        return table_metadata

    @staticmethod
    def from_metadata(metadata: Dict[str, Any]) -> "MysqlTable":
        """See base class."""
        table_metadata = metadata.copy()
        if "mysql_password" in table_metadata:
            table_metadata["password"] = table_metadata["mysql_password"]
            del table_metadata["mysql_password"]
        return MysqlTable(**table_metadata)


class MysqlKeyedTable(MysqlTable, table_sa.SqlAlchemyKeyedTable):
    """A MysqlTable having a primary key."""

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
        """Constructs a new MysqlKeyedTable instance.

        Args:
            host: Name of database server host hosting the MySQL database
                containing this table.
            user: MySQL database server username.
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
        return (
            "ON DUPLICATE KEY UPDATE "
            f"{self.primary_key_column()}={self.primary_key_column()}")

    def to_metadata(self) -> Dict[str, Any]:
        """See base class."""
        table_metadata = super().to_metadata().copy()
        table_metadata["primary_key_column"] = self.primary_key_column()
        return table_metadata

    @staticmethod
    def from_metadata(metadata: Dict[str, Any]) -> "MysqlKeyedTable":
        """See base class."""
        table_metadata = metadata.copy()
        if "mysql_password" in table_metadata:
            table_metadata["password"] = table_metadata["mysql_password"]
            del table_metadata["mysql_password"]
        return MysqlKeyedTable(**table_metadata)
