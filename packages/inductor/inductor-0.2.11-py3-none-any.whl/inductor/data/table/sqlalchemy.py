# Copyright 2022 Inductor, Inc.

"""Abstractions for SQLAlchemy tables."""

import abc
import datetime
import re
from typing import Any, Dict, Iterable, Optional, Tuple, Union

from alembic import migration, operations
import sqlalchemy

from inductor.data.table import table


# Name of empty placeholder column used to ensure that SQLAlchemy tables never
# contain no columns
_PLACEHOLDER_COLUMN = "inductor_placeholder_column"

# Suffix appended to names of columns that thus far contain only null values.
_ALL_NULL_COLUMN_SUFFIX = "__allnull__"


class SqlAlchemyView(table.Table, abc.ABC):
    """A view of a SQLAlchemy table."""

    def __init__(
        self,
        parent: "SqlAlchemyTable",
        query: table.SqlSelectQuery,
    ):
        """Constructs a new SqlAlchemyView instance.

        Args:
            parent: The underlying SqlAlchemyTable of which this instance
                is a view.
            query: The query (over parent) defining this view.
        """
        self._parent = parent
        self._query = query

    @abc.abstractmethod
    def to_metadata(self) -> Dict[str, Any]:
        """See base class."""

    @staticmethod
    @abc.abstractmethod
    def from_metadata(metadata: Dict[str, Any]) -> table.Table:
        """See base class."""

    def _query_string(self) -> Tuple[str, Dict[str, Any]]:
        """Returns the SQL query string and values underlying this view.

        SQLAlchemy requires that query values be contained in a dictionary,
        with query placeholders consisting of keys of that dictionary preceded
        by colons.  Therefore, this method replaces all instances of
        self._query.placeholder in the query with such keys, and constructs
        a corresponding dictionary of values.

        Returns:
            Internal query and values in a form that SQLAlchemy accepts for
            query execution.
        """
        # Get query with placeholders
        query_string, values_seq = self._query.to_sql_query_string(
            self._parent._table_name)  # pylint: disable=protected-access
        placeholder = self._query.placeholder
        if not placeholder:
            assert not values_seq
            return (query_string, {})
        assert len(values_seq) == query_string.count(placeholder)
        # Reformat query for use with SQLAlchemy
        formatted_query = ""
        formatted_values = {}
        split_query_string = query_string.split(placeholder)
        assert len(split_query_string) == len(values_seq) + 1
        colon_segments = query_string.split(":")[1:]
        i = 0
        for query_segment, value in zip(split_query_string[:-1], values_seq):
            # Generate a unique key that is not already present in query_string
            i += 1
            key = f"interpval{i}"
            while any(s.startswith(key) for s in colon_segments):
                i += 1
                key = f"interpval{i}"
            # Update formatted_query and formatted_values
            formatted_query += f"{query_segment}:{key}"
            formatted_values[key] = value
        formatted_query += split_query_string[-1]
        return (formatted_query, formatted_values)

    def __iter__(self) -> Iterable[table.Row]:
        """See base class."""
        query_string, query_values = self._query_string()
        rows = []
        with self._parent._engine.connect() as connection:  # pylint: disable=protected-access
            try:
                result = connection.execute(
                    sqlalchemy.text(query_string),
                    query_values,
                )
                for row in result:
                    row_dict = row._asdict()  # pylint: disable=protected-access
                    if self._parent._auto_ddl:
                        row_dict = self._parent._clean_row_dict(row_dict)
                    rows.append(row_dict)
                connection.commit()
            except sqlalchemy.exc.DBAPIError as error:
                connection.rollback()
                if self._parent.columns:
                    raise error
                else:
                    rows = []
        return rows.__iter__()

    def first_row(self) -> Optional[table.Row]:
        """See base class."""
        query_string, query_values = self._query_string()
        with self._parent._engine.connect() as connection:  # pylint: disable=protected-access
            try:
                result = connection.execute(
                    sqlalchemy.text(
                        f"SELECT * FROM ({query_string}) AS sq LIMIT 1"
                    ),
                    query_values,
                )
                row = result.first()
                connection.commit()
            except sqlalchemy.exc.DBAPIError as error:
                connection.rollback()
                if self._parent.columns:
                    raise error
                row = None
        if row is None:
            return None
        row_dict = row._asdict()  # pylint: disable=protected-access
        if self._parent._auto_ddl:  # pylint: disable=protected-access
            return self._parent._clean_row_dict(row_dict)  # pylint: disable=protected-access
        return row_dict

    @property
    def columns(self) -> Iterable[str]:
        """See base class."""
        row = self.first_row()
        return list(row.keys()) if row is not None else []


class SqlAlchemyTable(table.SqlQueryable, table.Appendable, abc.ABC):
    """A Table utilizing SQLAlchemy."""

    def __init__(
        self,
        table_name: str,
        sqlalchemy_url: str,
        indexed_columns: Iterable[str] = tuple(),
        auto_ddl: bool = True,
        include_index_postfix: bool = True,
    ):
        """Constructs a new SqlAlchemyTable instance.

        Args:
            table_name: Name of table in database.
            sqlalchemy_url: A SQLAlchemy-compatible database URL.
                https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls
            indexed_columns: Names of columns that should be indexed for faster
                queries.
            auto_ddl: Boolean value indicating whether or not to automatically
                execute DDL commands to create the table and add and modify
                columns. If False, then no processing of retrieved rows to
                account for prior automatic DDL is performed.
            include_index_postfix: Boolean value indicating whether or not to
                automatically include the index postfix generated by
                _get_sqlalchemy_type() when creating indices.
        """
        self._table_name = table_name
        self._engine = sqlalchemy.create_engine(sqlalchemy_url)
        self._indexed_columns = list(indexed_columns)
        self._auto_ddl = auto_ddl
        self._include_index_postfix = include_index_postfix
        if auto_ddl:
            with self._engine.connect() as connection:
                connection.execute(sqlalchemy.text(
                    f"CREATE TABLE IF NOT EXISTS {self._table_name} "
                    f"({_PLACEHOLDER_COLUMN} INTEGER)"
                ))
                connection.commit()

    @abc.abstractmethod
    def _is_undefined_column_error(
        self, error: sqlalchemy.exc.DBAPIError
    ) -> bool:
        """Returns True if error is related to an undefined column.

        Args:
            error: The SQLAlchemy error.

        Returns:
            True if the error was caused by an undefined column, otherwise
            False.
        """

    @abc.abstractmethod
    def _gen_view(self, query: table.SqlSelectQuery) -> SqlAlchemyView:
        """Creates a view over a provided query.

        Args:
            query: A SqlSelectQuery.

        Returns:
            An instance of a view class which extends SqlAlchemyView.
        """

    @abc.abstractmethod
    def to_metadata(self) -> Dict[str, Any]:
        """See base class."""

    @staticmethod
    @abc.abstractmethod
    def from_metadata(metadata: Dict[str, Any]) -> table.Table:
        """See base class."""

    def __del__(self):
        """Disposes self._engine as necessary on object destruction."""
        self._engine.dispose()

    def __iter__(self) -> Iterable[table.Row]:
        """See base class."""
        return self._gen_view(table.SqlSelectQuery("*")).__iter__()

    def first_row(self) -> Optional[table.Row]:
        """See base class."""
        return self._gen_view(table.SqlSelectQuery("*")).first_row()

    @property
    def _columns_with_nulls(self) -> Iterable[str]:
        """Returns names of all columns except for placeholder column."""
        metadata = sqlalchemy.MetaData()
        metadata.reflect(
            self._engine, only=[self._table_name], resolve_fks=False)
        sqlalchemy_table = metadata.tables[self._table_name]
        cols = sqlalchemy_table.columns
        return [c.name for c in cols if c.name != _PLACEHOLDER_COLUMN]

    @property
    def columns(self) -> Iterable[str]:
        """See base class."""
        cols = self._columns_with_nulls
        return [c for c in cols if not c.endswith(_ALL_NULL_COLUMN_SUFFIX)]

    def indexed_columns(self) -> Iterable[str]:
        """See base class."""
        return self._indexed_columns.copy()

    def select(self, expression: str, after_from: str = "") -> SqlAlchemyView:
        """See base class."""
        # Generate placeholder that does not appear in expression,
        # after_from, or self._table_name
        i = 0
        placeholder = f"[~placeholder{i}~]"
        while (
            placeholder in expression or
            placeholder in after_from or
            placeholder in self._table_name):
            i += 1
            placeholder = f"[~placeholder{i}~]"
        # Return view
        return self._gen_view(
            table.SqlSelectQuery(
                expression=expression,
                after_from=after_from,
                placeholder=placeholder,
            ),
        )

    def _consolidate_rows(self, rows: Iterable[table.Row]) -> Dict[str, Any]:
        """Consolidates a collection of rows into a single row.

        Given a collection of rows, this method returns a single row whose
        columns are the union of all columns in the provided rows. If a
        column exists in multiple rows, the value from the first non-None
        value in the collection is used. A column that has both None and
        non-None values will never be None in the returned row.

        Args:
            rows: The rows to consolidate.

        Returns:
            A dictionary containing the consolidated row.
        """
        return_dict = {}
        for row in rows:
            for col_name, value in row.items():
                # Ensure every column is present
                # If a value for a column is non-None, ensure
                # it's present
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

    def _get_sqlalchemy_type(
        self,
        value: Any,
        is_primary_key: bool,
    ) -> Tuple[sqlalchemy.types.TypeEngine, Optional[str]]:
        """Returns the SQLAlchemy type for a provided value.

        Args:
            value: A column value.
            is_primary_key: True if this column is a primary key,
                otherwise False.

        Returns:
            Tuple of (SQLAlchemy type, index postfix), where "index postfix"
            refers to a string which some databases require to accompany a
            type when that type is used to create an index.
            If the index postfix is not required by a type, the return tuple
            will be (SQLAlchemy type, None).
        """
        index_postfix = None
        if isinstance(value, bool):
            sqlalchemy_type = sqlalchemy.Boolean
        elif isinstance(value, int):
            sqlalchemy_type = sqlalchemy.Integer
        elif isinstance(value, float):
            sqlalchemy_type = sqlalchemy.Double
        elif isinstance(value, str):
            if is_primary_key:
                sqlalchemy_type = sqlalchemy.String(255)
                index_postfix = "(255)"
            else:
                sqlalchemy_type = sqlalchemy.Text
                index_postfix = "(300)"
        elif isinstance(value, bytes):
            sqlalchemy_type = sqlalchemy.LargeBinary
            index_postfix = "(600)"
        elif isinstance(value, datetime.datetime):
            sqlalchemy_type = sqlalchemy.DateTime
        elif isinstance(value, datetime.date):
            sqlalchemy_type = sqlalchemy.Date
        else:
            raise TypeError(f"Unsupported value type: {type(value)}")
        return (sqlalchemy_type, index_postfix)

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
        with self._engine.connect() as connection:
            ctx = migration.MigrationContext.configure(connection)
            op = operations.Operations(ctx)
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
                            op.add_column(  # pylint: disable=no-member
                                self._table_name,
                                sqlalchemy.Column(
                                    col_to_add,
                                    sqlalchemy.Text,
                                    quote=False,
                                ),
                            )
                            existing_col_names.add(col_to_add)
                    else:
                        is_keyed_table = isinstance(self, SqlAlchemyKeyedTable)
                        primary_key_column = (self.primary_key_column()
                            if is_keyed_table
                            else None)
                        assert col_name is not None
                        is_primary_key = col_name == primary_key_column
                        (sqlalchemy_type, index_postfix) = (
                            self._get_sqlalchemy_type(value, is_primary_key))
                        # Null-placeholder columns should be dropped
                        if is_null_present:
                            op.drop_column(  # pylint: disable=no-member
                                self._table_name, null_col_name)
                            existing_col_names.remove(null_col_name)
                        # If column exists, drop it
                        if col_name in existing_col_names:
                            op.drop_column(self._table_name, col_name)  # pylint: disable=no-member
                        op.add_column(  # pylint: disable=no-member
                            self._table_name,
                            sqlalchemy.Column(
                                col_name,
                                sqlalchemy_type,
                                nullable=not is_primary_key,
                                quote=False,
                            ),
                        )
                        existing_col_names.add(col_name)
                        # Create index if required.
                        if col_name in self._indexed_columns:
                            include_postfix = (index_postfix is not None
                                               and self._include_index_postfix)
                            index_col_name = (
                                f"{col_name}{index_postfix}"
                                if include_postfix
                                else col_name)
                            op.create_index(  # pylint: disable=no-member
                                f"{self._table_name}__{col_name}_index",
                                self._table_name,
                                [sqlalchemy.text(index_col_name)],
                            )
                        # Add primary key if required.
                        if is_primary_key:
                            connection.execute(sqlalchemy.text(
                                f"ALTER TABLE {self._table_name} "
                                f"ADD PRIMARY KEY ({col_name})"
                            ))
            connection.commit()

    def _get_clauses_from_row(
        self,
        row: table.Row,
        omit_none_values: bool = False,
    ) -> Tuple[str, str, Dict[str, Any]]:
        """Returns columns and values clause and values dict from row.

        Args:
            row: A table row.
            omit_none_values: Boolean flag indicating whether or not columns
                and values should be added to their respective clauses if the
                value is None.

        Returns:
            Tuple of (column clause, values clause, dictionary of values).
        """
        col_names = []
        values = []
        values_dict = {}
        for i, (col, value) in enumerate(row.items()):
            if value is not None or not omit_none_values:
                key = f"val{i}"
                col_names.append(col)
                values.append(f":{key}")
                values_dict[key] = value
        col_names_clause = ",".join(col_names)
        values_clause = ",".join(values)
        return (col_names_clause, values_clause, values_dict)

    def extend(self, rows: Iterable[table.Row]):
        """See base class."""
        self._add_table_columns(rows)
        with self._engine.connect() as connection:
            columns = None
            for row in rows:
                all_values_none = all(value is None for value in row.values())
                if all_values_none:
                    if columns is None:
                        columns = self.columns
                    col_names_clause = ",".join(columns)
                    default_values = ",".join(["DEFAULT" for _ in columns])
                    connection.execute(sqlalchemy.text(
                        f"INSERT INTO {self._table_name} "
                        f"({col_names_clause}) "
                        f"VALUES({default_values})"
                    ))
                else:
                    (col_names_clause, values_clause, values) = (
                        self._get_clauses_from_row(row, omit_none_values=True))
                    query = sqlalchemy.text(
                        f"INSERT INTO {self._table_name} "
                        f"({col_names_clause}) "
                        f"VALUES({values_clause})"
                    )
                    connection.execute(query, values)
            connection.commit()

    def _standardize_value(self, value: Any) -> Any:
        """Standardizes a raw Table column value.
        
        By default, this method returns the value it receives.
        Implementations which require additional value conversions should
        override this method.
        
        Args:
            value: A raw column value from a Table row.
        
        Returns:
            A standardized value.
        """
        return value

    def _clean_row_dict(self, row_dict: table.Row) -> table.Row:
        """Cleans a raw row dictionary returned by sqlalchemy.cursors._asdict().

        By default, only _PLACEHOLDER_COLUMN and any columns ending with the
        _ALL_NULL_COLUMN_SUFFIX are removed from the return dictionary.
        Implementations which require additional cleaning should override this
        method.

        Args:
            row: A raw row dictionary returned by sqlalchemy.cursors._asdict().

        Returns:
            A new dictionary containing the cleaned contents of row_dict.
        """
        clean_row_dict = {}
        for key, value in row_dict.items():
            if key != _PLACEHOLDER_COLUMN:
                converted_value = self._standardize_value(value)
                if key.endswith(_ALL_NULL_COLUMN_SUFFIX):
                    clean_row_dict[
                        key[:-len(_ALL_NULL_COLUMN_SUFFIX)]] = converted_value
                else:
                    clean_row_dict[key] = converted_value
        return clean_row_dict

class SqlAlchemyKeyedTable(SqlAlchemyTable, table.WithPrimaryKey, abc.ABC):
    """A SqlAlchemyTable having a primary key."""

    def __init__(
        self,
        table_name: str,
        sqlalchemy_url: str,
        primary_key_column: str,
        indexed_columns: Iterable[str] = tuple(),
        auto_ddl: bool = True,
        include_index_postfix: bool = True,
    ):
        """Constructs a new SqlAlchemyKeyedTable instance.

        Args:
            table_name: Name of table in database.
            sqlalchemy_url: A SQLAlchemy-compatible database URL.
                https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls
            primary_key_column: Name of column containing primary key.
            indexed_columns: Names of columns that should be indexed for faster
                queries.
            auto_ddl: Boolean value indicating whether or not to automatically
                execute DDL commands to create the table and add and modify
                columns. If False, then no processing of retrieved rows to
                account for prior automatic DDL is performed.
            include_index_postfix: Boolean value indicating whether or not to
                automatically include the index postfix generated by
                _get_sqlalchemy_type() when creating indices.
        """
        super().__init__(
            table_name=table_name,
            sqlalchemy_url=sqlalchemy_url,
            indexed_columns=indexed_columns,
            auto_ddl=auto_ddl,
            include_index_postfix=include_index_postfix,
        )
        self._primary_key_column = primary_key_column

    @property
    @abc.abstractmethod
    def _insert_skip_if_exists_suffix(self) -> str:
        """Returns INSERT statement suffix that yields skip-if-exists behavior.

        In particular, appending the returned string to an INSERT statement
        should cause the statement to skip the insert if a row already exists
        having the same primary key.
        """

    @abc.abstractmethod
    def to_metadata(self) -> Dict[str, Any]:
        """See base class."""

    @staticmethod
    @abc.abstractmethod
    def from_metadata(metadata: Dict[str, Any]) -> table.Table:
        """See base class."""

    def extend(self, rows: Iterable[table.Row]):
        """See base class.

        All rows in rows must contain a primary key in the column named
        self.primary_key_column(). If a row in rows contains a primary key
        that already exists in the table, then the existing row in the table
        will be replaced.
        """
        for row in rows:
            if (self._primary_key_column not in row
                or row[self._primary_key_column] is None):
                raise ValueError(
                    f"All rows in rows must contain a primary key in the "
                    f"column named {self._primary_key_column}."
                )
        self._add_table_columns(rows)
        with self._engine.connect() as connection:
            for row in rows:
                delete_query = sqlalchemy.text(
                    f"DELETE FROM {self._table_name} "
                    f"WHERE {self._primary_key_column}=:key"
                )
                delete_values = {"key": row[self._primary_key_column]}
                connection.execute(delete_query, delete_values)
                (col_names_clause, values_clause, insert_values) = (
                    self._get_clauses_from_row(row, omit_none_values=True))
                insert_query = sqlalchemy.text(
                    f"INSERT INTO {self._table_name} "
                    f"({col_names_clause}) "
                    f"VALUES({values_clause})"
                )
                connection.execute(insert_query, insert_values)
            connection.commit()

    def primary_key_column(self) -> str:
        """See base class."""
        return self._primary_key_column

    def get(
        self,
        key: Any,
        default: Optional[table.Row] = None,
    ) -> Optional[table.Row]:
        """See base class."""
        with self._engine.connect() as connection:
            try:
                query = sqlalchemy.text(
                    f"SELECT * FROM {self._table_name} "
                    f"WHERE {self._primary_key_column}=:key"
                )
                values = {"key": key}
                result = connection.execute(query, values)
                table_rows = result.fetchall()
                connection.commit()
            except sqlalchemy.exc.DBAPIError as error:
                connection.rollback()
                if self._is_undefined_column_error(error):
                    columns = self.columns
                    if columns or columns is None:
                        raise error
                    table_rows = []
                else:
                    raise error
        if not table_rows:
            return default
        if len(table_rows) > 1:
            raise RuntimeError("Found multiple rows having same primary key.")
        table_row = table_rows[0]
        row_dict = table_row._asdict()
        if self._auto_ddl:
            row_dict = self._clean_row_dict(row_dict)
        return row_dict

    def __contains__(self, key: Any) -> bool:
        """See base class."""
        with self._engine.connect() as connection:
            try:
                query = sqlalchemy.text(
                    f"SELECT COUNT(*) FROM {self._table_name} "
                    f"WHERE {self._primary_key_column}=:key"
                )
                values = {"key": key}
                result = connection.execute(query, values)
                return_value = result.scalar_one() > 0
                connection.commit()
                return return_value
            except sqlalchemy.exc.DBAPIError as error:
                connection.rollback()
                if self._is_undefined_column_error(error):
                    columns = self.columns
                    if columns or columns is None:
                        raise error
                    return False
                else:
                    raise error

    def set(
        self,
        key: Any,
        row: table.Row,
        skip_if_exists: bool = False,
    ) -> bool:
        """See base class.

        Primary key value cannot be None.
        """
        # Ensure that key is not None
        if key is None:
            raise ValueError("Primary key value cannot be None.")
        # Ensure that row contains primary key value
        if self._primary_key_column in row:
            if key != row[self._primary_key_column]:
                raise ValueError(
                    "Primary key value in row does not match key argument."
                )
        else:
            row = row.copy()
            row[self._primary_key_column] = key
        # Add any new table columns
        self._add_table_columns([row])
        # Insert or replace row
        with self._engine.connect() as connection:
            if skip_if_exists:
                # Check if the key exists if skip_if_exists is True
                query = sqlalchemy.text(
                    f"SELECT COUNT(*) FROM {self._table_name} "
                    f"WHERE {self._primary_key_column}=:key"
                )
                values = {"key": key}
                result = connection.execute(query, values)
                if result.scalar_one() > 0:
                    return False
            else:
                # Delete any existing row having given key if skip_if_exists
                # is False
                query = sqlalchemy.text(
                    f"DELETE FROM {self._table_name} "
                    f"WHERE {self._primary_key_column}=:key"
                )
                values = {"key": key}
                connection.execute(query, values)
            # Insert row
            (col_names_clause, values_clause, values) = (
                self._get_clauses_from_row(row, omit_none_values=True))
            query = sqlalchemy.text(
                f"INSERT INTO {self._table_name} ({col_names_clause}) "
                f"VALUES({values_clause})"
            )
            connection.execute(query, values)
            connection.commit()
        return True

    def update(self, key: Any, values: table.Row):
        """See base class.

        Primary key value cannot be None.
        """
        # Ensure that key is not None
        if key is None:
            raise ValueError("Primary key value cannot be None.")
        # Ensure that values contains a primary key value
        if self._primary_key_column in values:
            if key != values[self._primary_key_column]:
                raise ValueError(
                    "Primary key value in values does not match key argument."
                )
        else:
            values = values.copy()
            values[self._primary_key_column] = key
        # Add any new table columns
        self._add_table_columns([values])
        # Insert or update values
        with self._engine.connect() as connection:
            query = sqlalchemy.text(
                f"INSERT INTO {self._table_name} ({self._primary_key_column}) "
                f"VALUES(:key) {self._insert_skip_if_exists_suffix}"
            )
            query_values = {"key": key}
            connection.execute(query, query_values)
            if len(values) > 1:  # if values does not contain only primary key
                set_clauses = []
                query_values = {}
                for i, (col_name, col_value) in enumerate(values.items()):
                    if col_name != self._primary_key_column:
                        query_key = f"val{i}"
                        set_clauses.append(f"{col_name}=:{query_key}")
                        query_values[query_key] = col_value
                query_values["key"] = values[self._primary_key_column]
                query = sqlalchemy.text(
                    f"UPDATE {self._table_name} SET " +
                    ",".join(set_clauses) +
                    f" WHERE {self._primary_key_column}=:key")
                connection.execute(query, query_values)
            connection.commit()

    def __delitem__(self, key: Any):
        """See base class."""
        # Ensure that key is not None.
        if key is None:
            raise ValueError("Primary key value cannot be None.")
        with self._engine.connect() as connection:
            query = sqlalchemy.text(
                f"DELETE FROM {self._table_name} "
                f"WHERE {self._primary_key_column}=:key"
            )
            query_values = {"key": key}
            try:
                connection.execute(query, query_values)
                connection.commit()
            except sqlalchemy.exc.DBAPIError as error:
                connection.rollback()
                if self._is_undefined_column_error(error):
                    columns = self.columns
                    if columns or columns is None:
                        raise error
                else:
                    raise error

    def increment(
        self,
        key: Any,
        column_name: str,
        increment_by: int
    ) -> Union[int, float]:
        """See base class."""
        # Ensure that key is not None.
        if key is None:
            raise ValueError("Primary key value cannot be None.")
        # Ensure that column_name is not the primary key column.
        if column_name == self._primary_key_column:
            raise ValueError(
                "Cannot increment primary key column."
            )
        # Increment column.
        with self._engine.connect() as connection:
            try:
                update_query = sqlalchemy.text(
                    f"UPDATE {self._table_name} "
                    f"SET {column_name}={column_name}+:increment "
                    f"WHERE {self._primary_key_column}=:key"
                )
                update_values = {
                    "increment": increment_by,
                    "key": key,
                }
                connection.execute(update_query, update_values)
                select_query = sqlalchemy.text(
                    f"SELECT {column_name} FROM {self._table_name} "
                    f"WHERE {self._primary_key_column}=:key"
                )
                select_values = {"key": key}
                result = connection.execute(
                    select_query, select_values
                ).fetchone()
                if result is not None:
                    result = result._asdict()
                connection.commit()
            except sqlalchemy.exc.DBAPIError as error:
                connection.rollback()
                if self._is_undefined_column_error(error):
                    columns = self.columns
                    if columns or columns is None:
                        raise error
                    result = None
                else:
                    raise error
        if result is None or column_name not in result:
            raise ValueError(
                f"Column name {column_name} does not exist in table "
                f"{self._table_name}."
            )
        return result[column_name]
