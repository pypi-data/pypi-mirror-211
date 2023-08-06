# Copyright 2022 Inductor, Inc.

"""Abstractions for BigQuery tables."""

import datetime
import re
from typing import Any, Dict, Iterable, Optional, Tuple

from google.cloud import bigquery
from google.cloud import exceptions
import pandas as pd

from inductor.data.table import table


# Name of empty placeholder column used to ensure that BigQuery tables never
# contain no columns
_PLACEHOLDER_COLUMN = "inductor_placeholder_column"

# Suffix appended to names of columns that thus far contain only null values.
_ALL_NULL_COLUMN_SUFFIX = "__allnull__"


def _is_undefined_column_error(error: exceptions.GoogleCloudError) -> bool:
    """Returns True if error is deemed to be related to an undefined column.

    Args:
        error: An exception raised by the Google Cloud Python API.

    Returns:
        True if the error was deemed to be caused by an undefined column,
        otherwise False.
    """
    return error.message.startswith("Unrecognized name:")


def _clean_row_dict(row_dict: table.Row) -> table.Row:
    """Cleans a raw row dictionary.

    Specifically, removes _PLACEHOLDER_COLUMN and any columns ending with
    the _ALL_NULL_COLUMN_SUFFIX.

    Args:
        row: A raw row dictionary retrieved from a BigQuery table.

    Returns:
        A new dictionary containing the cleaned contents of row_dict.
    """
    clean_row_dict = {}
    for key, value in row_dict.items():
        if (key != _PLACEHOLDER_COLUMN and
            not key.endswith(_ALL_NULL_COLUMN_SUFFIX)):
            clean_row_dict[key] = value
    return clean_row_dict


def _value_to_bigquery_type(value: Any) -> str:
    """Returns BigQuery type for value.

    Args:
        value: Python value for which to return corresponding BigQuery type.
    """
    if isinstance(value, bool):
        return "BOOL"
    elif isinstance(value, int):
        return "INTEGER"
    elif isinstance(value, float):
        return "FLOAT64"
    elif isinstance(value, str):
        return "STRING"
    elif isinstance(value, bytes):
        return "BYTES"
    elif isinstance(value, datetime.datetime):
        if value.tzinfo is None:
            return "DATETIME"
        else:
            return "TIMESTAMP"
    elif isinstance(value, datetime.date):
        return "DATE"
    else:
        raise TypeError(f"Unsupported value type: {type(value)}")


class BigQueryView(table.Table):
    """A view of a BigQuery table."""

    def __init__(
        self,
        parent: "BigQueryTable",
        query: table.SqlSelectQuery,
    ):
        """Constructs a new BigQueryView instance.

        Args:
            parent: The underlying BigQueryTable of which this instance
                is a view.
            query: The query (over parent) defining this view.
        """
        self._parent = parent
        self._query = query

    def _query_string(self) -> Tuple[str, Tuple[Any]]:
        """Returns the SQL query string and values underlying this view."""
        # pylint: disable-next=protected-access
        return self._query.to_sql_query_string(f"`{self._parent._table_id}`")

    def __iter__(self) -> Iterable[table.Row]:
        """See base class."""
        query_string, query_values = self._query_string()
        query_parameters = [
            bigquery.ScalarQueryParameter(None, _value_to_bigquery_type(v), v)
            for v in query_values]
        job_config = bigquery.QueryJobConfig(query_parameters=query_parameters)
        query_job = self._parent._client.query(
            query_string, job_config=job_config)
        try:
            result = query_job.result()
        except exceptions.GoogleCloudError as error:
            if (_is_undefined_column_error(error) and
                not self._parent.columns):
                return [].__iter__()
            else:
                raise error
        rows = []
        for row in result:
            row_dict = dict(row.items())
            if self._parent._auto_ddl:
                row_dict = _clean_row_dict(row_dict)
            rows.append(row_dict)
        return rows.__iter__()

    def first_row(self) -> Optional[table.Row]:
        """See base class."""
        query_string, query_values = self._query_string()
        query_parameters = [
            bigquery.ScalarQueryParameter(None, _value_to_bigquery_type(v), v)
            for v in query_values]
        job_config = bigquery.QueryJobConfig(query_parameters=query_parameters)
        query_job = self._parent._client.query(  # pylint: disable=protected-access
            f"SELECT * FROM ({query_string}) AS sq LIMIT 1",
            job_config=job_config)
        try:
            result = query_job.result()
        except exceptions.GoogleCloudError as error:
            if (_is_undefined_column_error(error) and
                not self._parent.columns):
                return None
            else:
                raise error
        rows = []
        for row in result:
            row_dict = dict(row.items())
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
        query_parameters = [
            bigquery.ScalarQueryParameter(None, _value_to_bigquery_type(v), v)
            for v in query_values]
        job_config = bigquery.QueryJobConfig(query_parameters=query_parameters)
        query_job = self._parent._client.query(  # pylint: disable=protected-access
            query_string, job_config=job_config)
        try:
            df = query_job.to_dataframe()
        except exceptions.GoogleCloudError as error:
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


class BigQueryTable(table.SqlQueryable, table.Appendable):
    """A Table backed by a BigQuery table."""

    def __init__(
        self,
        dataset_name: str,
        table_name: str,
        project_id: Optional[str] = None,
        auto_ddl: bool = True
    ):
        """Constructs a new BigQueryTable instance.

        Args:
            dataset_name: Name of dataset containing table.  Must already
                exist.
            table_name: Name of table within dataset.
            project_id: Optionally, ID of project containing dataset and
                table.  If None, then inferred from environment in which this
                code is running by Google's BigQuery Python library.
            auto_ddl: Boolean value indicating whether or not to automatically
                execute DDL commands to create the table and add and modify
                columns. If False, then no processing of retrieved rows to
                account for prior automatic DDL is performed.
        """
        self._dataset_name = dataset_name
        self._table_name = table_name
        self._project_id = project_id
        self._auto_ddl = auto_ddl
        self._client = bigquery.Client(project_id)
        self._table_id = f"{dataset_name}.{table_name}"
        if project_id is not None:
            self._table_id = f"{project_id}.{self._table_id}"
        elif self._client.project is not None:
            self._table_id = f"{self._client.project}.{self._table_id}"
        if auto_ddl:
            bigquery_table = bigquery.Table(self._table_id, schema=[
                bigquery.SchemaField(_PLACEHOLDER_COLUMN, "INTEGER")
            ])
            self._client.create_table(bigquery_table, exists_ok=True)

    def __del__(self):
        """Calls the BigQuery client's close() method."""
        self._client.close()

    def __iter__(self) -> Iterable[table.Row]:
        """See base class."""
        return BigQueryView(self, table.SqlSelectQuery("*")).__iter__()

    def first_row(self) -> Optional[table.Row]:
        """See base class."""
        return BigQueryView(self, table.SqlSelectQuery("*")).first_row()

    @property
    def _columns_with_nulls(self) -> Iterable[str]:
        """Returns names of all columns except placeholder column."""
        bigquery_table = self._client.get_table(self._table_id)
        cols = [sf.name for sf in bigquery_table.schema]
        return [c for c in cols if c != _PLACEHOLDER_COLUMN]

    @property
    def columns(self) -> Iterable[str]:
        """See base class."""
        cols = self._columns_with_nulls
        return [c for c in cols if not c.endswith(_ALL_NULL_COLUMN_SUFFIX)]

    def pandas_df(self) -> pd.DataFrame:
        """See base class."""
        return BigQueryView(self, table.SqlSelectQuery("*")).pandas_df()

    def indexed_columns(self) -> Iterable[str]:
        """See base class."""
        return []

    def select(self, expression: str, after_from: str = "") -> BigQueryView:
        """See base class."""
        return BigQueryView(
            self,
            table.SqlSelectQuery(
                expression=expression, after_from=after_from, placeholder="?"))

    def __len__(self) -> int:
        """See base class."""
        return self.select("count(*)").value()

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
                            f"ADD COLUMN {col_to_add} STRING")
                        existing_col_names.add(col_to_add)
                else:
                    bigquery_type = _value_to_bigquery_type(value)
                    # If present, null-placeholder column should be dropped
                    if is_null_present:
                        drop_column_clauses.append(
                            f"DROP COLUMN {null_col_name}")
                        existing_col_names.remove(null_col_name)
                    # If column exists, drop it (BigQuery does not
                    # allow arbitrarily altering column types)
                    if col_name in existing_col_names:
                        drop_column_clauses.append(
                            f"DROP COLUMN {col_name}")
                    # Add column
                    add_column_clauses.append(
                        f"ADD COLUMN {col_name} {bigquery_type}")
                    existing_col_names.add(col_name)
        query_lines = []
        if drop_column_clauses:
            query_lines.append(
                f"ALTER TABLE `{self._table_id}` " +
                ", ".join(drop_column_clauses) + ";")
        if add_column_clauses:
            query_lines.append(
                f"ALTER TABLE `{self._table_id}` " +
                ", ".join(add_column_clauses) + ";")
        if query_lines:
            self._client.query("\n".join(query_lines)).result()

    def extend(self, rows: Iterable[table.Row]):
        """See base class."""
        self._add_table_columns(rows)
        bigquery_table = self._client.get_table(self._table_id)
        col_types = {}
        for schema_field in bigquery_table.schema:
            col_types[schema_field.name] = (
                "BOOL" if schema_field.field_type == "BOOLEAN"
                else schema_field.field_type)
        query_strings = []
        query_params = []
        for row in rows:
            if row:
                col_names, values = zip(*row.items())
                query_strings.append(
                    f"INSERT INTO `{self._table_id}` " +
                    "(" + ",".join(col_names) + ") " +
                    "VALUES(" + ",".join(["?"] * len(values)) + ");")
                query_params.extend([
                    bigquery.ScalarQueryParameter(None, col_types[c], v)
                    for c, v in zip(col_names, values)
                ])
            else:
                col_names = [sf.name for sf in bigquery_table.schema]
                query_strings.append(
                    f"INSERT INTO `{self._table_id}` " +
                    "(" + ",".join(col_names) + ") " +
                    "VALUES(" + ",".join(["DEFAULT"] * len(col_names)) + ");")
        job_config = bigquery.QueryJobConfig(query_parameters=query_params)
        self._client.query(
            "\n".join(query_strings), job_config=job_config).result()

    def to_metadata(self) -> Dict[str, Any]:
        """See base class."""
        metadata = {
            "dataset_name": self._dataset_name,
            "table_name": self._table_name,
            "auto_ddl": self._auto_ddl
        }
        if self._project_id is not None:
            metadata["project_id"] = self._project_id
        return metadata

    @staticmethod
    def from_metadata(metadata: Dict[str, Any]) -> table.Table:
        """See base class."""
        return BigQueryTable(**metadata)
