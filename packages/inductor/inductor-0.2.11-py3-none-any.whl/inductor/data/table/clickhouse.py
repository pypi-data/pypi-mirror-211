# Copyright 2022 Inductor, Inc.

"""Abstractions for ClickHouse tables."""

import datetime
import re
from typing import Any, Dict, Iterable, Optional, Tuple

import clickhouse_connect
from clickhouse_connect.driver import exceptions
import pandas as pd

from inductor.data.table import table


# Name of empty placeholder column used to ensure that ClickHouse tables never
# contain no columns
_PLACEHOLDER_COLUMN = "inductor_placeholder_column"

# Suffix appended to names of columns that thus far contain only null values.
_ALL_NULL_COLUMN_SUFFIX = "__allnull__"


def _is_undefined_column_error(error: exceptions.DatabaseError) -> bool:
    """Returns True if error is deemed to be related to an undefined column.

    Args:
        error: An exception raised by the ClickHouse Python connector.

    Returns:
        True if the error was deemed to be caused by an undefined column,
        otherwise False.
    """
    error_str = str(error)
    return "Missing column" in error_str


def _clean_row_dict(row_dict: table.Row) -> table.Row:
    """Cleans a raw row dictionary.

    Specifically, removes _PLACEHOLDER_COLUMN and any columns ending with
    the _ALL_NULL_COLUMN_SUFFIX.

    Args:
        row: A raw row dictionary retrieved from a ClickHouse table.

    Returns:
        A new dictionary containing the cleaned contents of row_dict.
    """
    clean_row_dict = {}
    for key, value in row_dict.items():
        if (key != _PLACEHOLDER_COLUMN and
            not key.endswith(_ALL_NULL_COLUMN_SUFFIX)):
            clean_row_dict[key] = value
    return clean_row_dict


def _value_to_clickhouse_type(value: Any) -> str:
    """Returns name of ClickHouse type for value.

    Args:
        value: Python value for which to return corresponding ClickHouse
            type name.
    """
    if isinstance(value, bool):
        return "Bool"
    elif isinstance(value, int):
        return "Int64"
    elif isinstance(value, float):
        return "Float64"
    elif isinstance(value, str):
        return "String"
    elif isinstance(value, bytes):
        # NOTE: ClickHouse does not offer a distinct column type for bytes
        # values.  Hence, the ClickHouse Python connector will return values
        # that were originally of Python type bytes (prior to insertion) as
        # strings when they are retrieved; it is then the responsibility of
        # the user of this file to convert those string values to bytes as
        # needed, in Python.
        return "String"
    elif isinstance(value, datetime.datetime):
        return "DateTime64"
    elif isinstance(value, datetime.date):
        return "Date32"
    else:
        raise TypeError(f"Unsupported value type: {type(value)}")


class ClickHouseView(table.Table):
    """A view of a ClickHouse table."""

    def __init__(
        self,
        parent: "ClickHouseTable",
        query: table.SqlSelectQuery,
    ):
        """Constructs a new ClickHouseView instance.

        Args:
            parent: The underlying ClickHouseTable of which this instance
                is a view.
            query: The query (over parent) defining this view.
        """
        self._parent = parent
        self._query = query

    def _query_string(self) -> Tuple[str, Tuple[Any]]:
        """Returns the SQL query string and values underlying this view."""
        # pylint: disable-next=protected-access
        return self._query.to_sql_query_string(self._parent._table_name)

    def __iter__(self) -> Iterable[table.Row]:
        """See base class."""
        query_string, query_values = self._query_string()
        try:
            # pylint: disable-next=protected-access
            result = self._parent._client.query(
                query_string, parameters=query_values)
        except exceptions.DatabaseError as error:
            if (_is_undefined_column_error(error) and
                not self._parent.columns):
                return [].__iter__()
            else:
                raise error
        rows = []
        for row in result.result_rows:
            row_dict = dict(zip(result.column_names, row))
            if self._parent._auto_ddl:
                row_dict = _clean_row_dict(row_dict)
            rows.append(row_dict)
        return rows.__iter__()

    def first_row(self) -> Optional[table.Row]:
        """See base class."""
        query_string, query_values = self._query_string()
        try:
            # pylint: disable-next=protected-access
            result = self._parent._client.query(
                f"SELECT * FROM ({query_string}) AS sq LIMIT 1",
                parameters=query_values)
        except exceptions.DatabaseError as error:
            if (_is_undefined_column_error(error) and
                not self._parent.columns):
                return None
            else:
                raise error
        rows = []
        for row in result.result_rows:
            row_dict = dict(zip(result.column_names, row))
            if self._parent._auto_ddl:  # pylint: disable=protected-access
                row_dict = _clean_row_dict(row_dict)
            rows.append(row_dict)
        assert len(rows) <= 1
        if not rows:
            return None
        return rows[0]

    @property
    def columns(self) -> Iterable[str]:
        """See base class."""
        row = self.first_row()
        return list(row.keys()) if row is not None else []

    def pandas_df(self) -> pd.DataFrame:
        """See base class."""
        query_string, query_values = self._query_string()
        try:
            # pylint: disable-next=protected-access
            df = self._parent._client.query_df(
                query_string, parameters=query_values)
        except exceptions.DatabaseError as error:
            if (_is_undefined_column_error(error) and
                not self._parent.columns):
                return pd.DataFrame([])
            else:
                raise error
        if self._parent._auto_ddl:  # pylint: disable=protected-access
            for c in df.columns:
                if (c == _PLACEHOLDER_COLUMN or
                    c.endswith(_ALL_NULL_COLUMN_SUFFIX)):
                    del df[c]
        return df

    def to_metadata(self) -> Dict[str, Any]:
        """See base class."""
        return NotImplementedError()

    @staticmethod
    def from_metadata(metadata: Dict[str, Any]) -> table.Table:
        return NotImplementedError()


class ClickHouseTable(table.SqlQueryable, table.Appendable):
    """A Table backed by a ClickHouse table."""

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        database: str,
        table_name: str,
        https: Optional[bool] = None,
        port: Optional[int] = None,
        auto_ddl: bool = True
    ):
        """Constructs a new ClickHouseTable instance.

        Args:
            host: Hostname or IP address of ClickHouse server.
            username: ClickHouse server username.
            password: Password for username.
            database: Name of database containing table.
            table_name: Name of table in database given by preceding arguments.
            https: If True, then HTTPS will be used for communication with the
                ClickHouse server.  If False, then HTTP will be used.  Defaults
                to True unless host == "localhost", in which case defaults to
                False.
            port: ClickHouse server port.  If not specified, ClickHouse default
                (which depends on `https`) will be used.
            auto_ddl: Boolean value indicating whether or not to automatically
                execute DDL commands to create the table and add and modify
                columns.  If False, then no processing of retrieved rows to
                account for prior automatic DDL is performed.
        """
        self._host = host
        self._username = username
        self._password = password
        self._database = database
        self._table_name = table_name
        self._https = https
        self._port = port
        self._auto_ddl = auto_ddl

        client_interface = "https" if https else "http"
        if https is None and host != "localhost":
            client_interface = "https"
        self._client = clickhouse_connect.get_client(
            interface=client_interface,
            host=host,
            port=port,
            username=username,
            password=password,
            database=database,
            secure=(client_interface == "https"))

        if auto_ddl:
            self._client.command(f"CREATE DATABASE IF NOT EXISTS {database}")
            self._client.command(
                f"CREATE TABLE IF NOT EXISTS {table_name} "
                f"({_PLACEHOLDER_COLUMN} Nullable(Int8)) "
                "ENGINE = MergeTree() "
                "PRIMARY KEY tuple()")

    def __iter__(self) -> Iterable[table.Row]:
        """See base class."""
        return ClickHouseView(self, table.SqlSelectQuery("*")).__iter__()

    def first_row(self) -> Optional[table.Row]:
        """See base class."""
        return ClickHouseView(self, table.SqlSelectQuery("*")).first_row()

    @property
    def _columns_with_nulls(self) -> Iterable[str]:
        """Returns names of all columns except placeholder column."""
        cols = self._client.query(
            "SELECT name FROM system.columns "
            "WHERE database=%s AND table=%s",
            parameters=(self._database, self._table_name)).result_columns[0]
        return [c for c in cols if c != _PLACEHOLDER_COLUMN]

    @property
    def columns(self) -> Iterable[str]:
        """See base class."""
        cols = self._columns_with_nulls
        return [c for c in cols if not c.endswith(_ALL_NULL_COLUMN_SUFFIX)]

    def pandas_df(self) -> pd.DataFrame:
        """See base class."""
        return ClickHouseView(self, table.SqlSelectQuery("*")).pandas_df()

    def indexed_columns(self) -> Iterable[str]:
        """See base class."""
        return []

    def select(self, expression: str, after_from: str = "") -> ClickHouseView:
        """See base class."""
        return ClickHouseView(
            self,
            table.SqlSelectQuery(
                expression=expression, after_from=after_from, placeholder="%s"))

    def _consolidate_rows(self, rows: Iterable[table.Row]) -> Dict[str, Any]:
        """Consolidates a collection of rows into a single row.

        Given a collection of rows, this method returns a single row whose
        columns are the union of all columns in the provided rows.  If a
        column exists in multiple rows, the value from the first non-None
        value in the collection is used.  A column that has both None and
        non-None values will never be None in the returned row.

        Args:
            rows: The rows to consolidate.

        Returns:
            A dictionary containing the consolidated row.
        """
        return_dict = {}
        for row in rows:
            for col_name, value in row.items():
                # Ensure that every column is present.
                # If a value for a column is non-None, ensure that
                # it is present.
                if (col_name not in return_dict
                    or return_dict[col_name] is None):
                    return_dict[col_name] = value
        return return_dict

    def _validate_col_name(self, col_name: Optional[str]):
        """Raises a ValueError if column name is invalid.

        Args:
            col_name: The column name to validate.

        Raises:
            ValueError if the provided column name is invalid.
        """
        if col_name == _PLACEHOLDER_COLUMN:
            raise ValueError(
                "Cannot add a column having name equal to "
                f"placeholder column name ({_PLACEHOLDER_COLUMN})."
            )
        elif col_name.endswith(_ALL_NULL_COLUMN_SUFFIX):
            raise ValueError(
                "Column names cannot end with "
                f"\"{_ALL_NULL_COLUMN_SUFFIX}\" "
                f"(encountered column name {col_name})."
            )
        elif not re.match(r"\A[a-zA-Z0-9_]+\Z", col_name):
            raise ValueError(
                "Column names must match "
                r"\A[a-zA-Z0-9_]+\Z "
                f"(encountered column name {col_name})."
            )

    def _add_table_columns(self, rows: Iterable[table.Row]):
        """Adds columns to the underlying table for any new columns in rows.

        Args:
            rows: Rows that may contain columns not present in the underlying
                table.
        """
        if not self._auto_ddl:
            return
        existing_col_names = set(self._columns_with_nulls)
        consolidated_rows = self._consolidate_rows(rows)
        add_column_clauses = []
        drop_column_clauses = []
        for col_name, value in consolidated_rows.items():
            self._validate_col_name(col_name)
            null_col_name = col_name + _ALL_NULL_COLUMN_SUFFIX
            is_null_present = null_col_name in existing_col_names
            should_add_col = col_name not in existing_col_names
            should_alter_col = value is not None and is_null_present
            if should_add_col or should_alter_col:
                if value is None:
                    # Create column and null column
                    for col_to_add in [col_name, null_col_name]:
                        add_column_clauses.append(
                            f"ADD COLUMN {col_to_add} Nullable(String) "
                            "DEFAULT NULL")
                        existing_col_names.add(col_to_add)
                else:
                    clickhouse_type = _value_to_clickhouse_type(value)
                    # If present, null-placeholder column should be dropped
                    if is_null_present:
                        drop_column_clauses.append(
                            f"DROP COLUMN {null_col_name}")
                        existing_col_names.remove(null_col_name)
                    # If column exists, drop it
                    if col_name in existing_col_names:
                        assert is_null_present
                        drop_column_clauses.append(
                            f"DROP COLUMN {col_name}")
                    # Add column
                    add_column_clauses.append(
                        f"ADD COLUMN {col_name} Nullable({clickhouse_type}) "
                        "DEFAULT NULL")
                    existing_col_names.add(col_name)
        if drop_column_clauses:
            self._client.command(
                f"ALTER TABLE {self._table_name} " +
                ", ".join(drop_column_clauses) + ";")
        if add_column_clauses:
            self._client.command(
                f"ALTER TABLE {self._table_name} " +
                ", ".join(add_column_clauses) + ";")

    def extend(self, rows: Iterable[table.Row]):
        """See base class."""
        # Add table columns as necessary
        self._add_table_columns(rows)
        # Get mapping from current table column names to ClickHouse type names
        result = self._client.query(
            "SELECT name, type FROM system.columns "
            "WHERE database=%s AND table=%s",
            parameters=(self._database, self._table_name))
        result_columns_dict = dict(zip(
            result.column_names, result.result_columns))
        col_name_to_type = dict(zip(
            result_columns_dict["name"], result_columns_dict["type"]))
        # Insert data
        cur_col_set = None
        cur_col_list = None
        cur_row_values = []
        def insert_cur_rows():
            if cur_row_values:
                self._client.insert(
                    table=self._table_name,
                    data=cur_row_values,
                    column_names=cur_col_list,
                    column_type_names=[
                        col_name_to_type[c] for c in cur_col_list],
                    settings={
                        "async_insert": 1,
                        "wait_for_async_insert": 1
                    })
        for row in rows:
            if cur_col_set is None or cur_col_set != set(row.keys()):
                insert_cur_rows()
                if row:
                    cur_col_set = set(row.keys())
                    cur_col_list = list(row.keys())
                else:
                    cur_col_set = set(col_name_to_type.keys())
                    cur_col_list = list(col_name_to_type.keys())
                cur_row_values = []
            if row:
                cur_row_values.append([row[c] for c in cur_col_list])
            else:
                cur_row_values.append([None for _ in cur_col_list])
        insert_cur_rows()

    def to_metadata(self) -> Dict[str, Any]:
        """See base class."""
        return {
            "host": self._host,
            "username": self._username,
            "database": self._database,
            "table_name": self._table_name,
            "https": self._https,
            "port": self._port,
            "auto_ddl": self._auto_ddl
        }

    @staticmethod
    def from_metadata(metadata: Dict[str, Any]) -> "ClickHouseTable":
        """See base class."""
        table_metadata = metadata.copy()
        if "clickhouse_password" in table_metadata:
            table_metadata["password"] = table_metadata["clickhouse_password"]
            del table_metadata["clickhouse_password"]
        return ClickHouseTable(**table_metadata)
