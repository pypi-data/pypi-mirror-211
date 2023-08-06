from __future__ import annotations

import pathlib
import tempfile
from collections.abc import Mapping, Sequence
from functools import cached_property
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    Optional,
    Protocol,
    Union,
)
from urllib.parse import quote, urlencode

import pandas as pd
import pyarrow as pa
from atoti_core import (
    BASE_SCENARIO_NAME,
    EMPTY_MAPPING,
    JAVA_MAX_INT,
    ActiveViamClient,
    ColumnCoordinates,
    Condition,
    ConditionCombinationOperatorBound,
    ConditionComparisonOperatorBound,
    Constant,
    DataFrameColumnDescription,
    IPythonKeyCompletions,
    Plugin,
    ReprJson,
    ReprJsonable,
    condition_to_dict,
    create_dataframe,
    doc,
    get_ipython_key_completions_for_mapping,
    parse_data_type,
)
from numpy.typing import NDArray

from ._arrow_utils import write_arrow_to_file
from ._check_column_condition_table import check_column_condition_table
from ._condition_to_json_serializable_dict import condition_to_json_serializable_dict
from ._docs_utils import (
    CLIENT_SIDE_ENCRYPTION_DOC,
    CSV_KWARGS,
    PARQUET_KWARGS,
    SQL_KWARGS,
    TABLE_APPEND_DOC,
    TABLE_IADD_DOC,
)
from ._file_utils import split_path_and_pattern
from ._java_api import JavaApi
from ._pandas_utils import pandas_to_arrow
from ._report import TableReport
from ._runtime_type_checking_utils import typecheck
from ._sources.arrow import ArrowDataSource
from ._sources.csv import CsvDataSource, CsvPrivateParameters
from ._sources.parquet import ParquetDataSource
from ._spark_utils import write_spark_to_parquet
from .client_side_encryption_config import ClientSideEncryptionConfig
from .column import Column
from .type import DataType

if TYPE_CHECKING:
    from pyspark.sql import (  # pylint: disable=undeclared-dependency, nested-import
        DataFrame as SparkDataFrame,
    )

_Row = Union[tuple[Any, ...], Mapping[str, Any]]

_DOC_KWARGS = {"what": "table"}


class Table(ReprJsonable):
    """Represents a single table."""

    def __init__(
        self,
        name: str,
        /,
        *,
        client: ActiveViamClient,
        java_api: JavaApi,
        load_kafka: _LoadKafka,
        load_sql: _LoadSql,
        plugins: Mapping[str, Plugin],
        scenario: str = BASE_SCENARIO_NAME,
    ) -> None:
        super().__init__()

        self._client = client
        self._java_api = java_api
        self._load_kafka = load_kafka
        self._load_sql = load_sql
        self._name = name
        self._plugins = plugins
        self._scenario = scenario

        self._columns: Mapping[str, Column] = {
            column_name: Column(
                column_name,
                get_column_data_type=self._java_api.get_column_data_type,
                get_column_default_value=self._java_api.get_column_default_value,
                set_column_default_value=self._java_api.set_column_default_value,
                table_keys=self.keys,
                table_name=self._name,
            )
            for column_name in self._java_api.get_table_column_names(name)
        }

    @property
    def name(self) -> str:
        """Name of the table."""
        return self._name

    @cached_property
    def keys(self) -> Sequence[str]:
        """Names of the key columns of the table."""
        keys = self._java_api.get_key_columns(self.name)
        return [
            column
            for column in self._java_api.get_table_column_names(self._name)
            if column in keys
        ]

    @property
    def scenario(self) -> str:
        """Scenario on which the table is."""
        return self._scenario

    @property
    def columns(self) -> Sequence[str]:
        """Columns of the table."""
        return list(self._columns)

    @property
    def _types(self) -> Mapping[str, DataType]:
        """Columns and their types."""
        return {name: col.data_type for name, col in self._columns.items()}

    @property
    def _partitioning(self) -> str:
        """Table partitioning."""
        return self._java_api.get_table_partitioning(self.name)

    def join(
        self,
        other: Table,
        mapping: Optional[
            Condition[
                ColumnCoordinates,
                Literal["eq"],
                ColumnCoordinates,
                Optional[Literal["and"]],
            ]
        ] = None,
        /,
    ) -> None:
        """Define a join between this table and another.

        There are two kinds of joins:

        * full join if all the key columns of the *other* table are mapped and the joined tables share the same locality (either both :class:`~atoti.Table` or both ``ExternalTable``).
        * partial join otherwise.

        Depending on the cube creation mode, the join will also generate different hierarchies and measures:

        * ``manual``: No hierarchy is automatically created.
          For partial joins, creating a hierarchy for each mapped key column is necessary before creating hierarchies for the other columns.
          Once these required hierarchies exist, hierarchies for the un-mapped key columns of the *other* table will automatically be created.
        * ``no_measures``: All the key columns and non-numeric columns of the *other* table will be converted into hierarchies.
          No measures will be created in this mode.
        * ``auto``: The same hierarchies as in the ``no_measures`` mode will be created.
          Additionally, columns of the base table containing numeric values (including arrays), except for columns which are keys, will be converted into measures.
          Columns of the *other* table with these types will not be converted into measures.

        Args:
            other: The other table to join.
            mapping: An equality-based condition from columns of this table to columns of the *other* table.
              If ``None``, the key columns of the *other* table with the same name as columns in this table will be used.

        Example:
            >>> sales_table = session.create_table(
            ...     "Sales",
            ...     types={"ID": tt.STRING, "Product ID": tt.STRING, "Price": tt.INT},
            ... )
            >>> products_table = session.create_table(
            ...     "Products",
            ...     types={"ID": tt.STRING, "Name": tt.STRING, "Category": tt.STRING},
            ... )
            >>> sales_table.join(
            ...     products_table, sales_table["Product ID"] == products_table["ID"]
            ... )

        """
        normalized_mapping: Optional[Mapping[str, str]] = None

        if mapping is not None:
            check_column_condition_table(
                mapping, attribute_name="subject", expected_table_name=self.name
            )
            check_column_condition_table(
                mapping, attribute_name="target", expected_table_name=other.name
            )
            normalized_mapping = {
                self_coordinates.column_name: other_coordinates.column_name
                for self_coordinates, other_coordinates in condition_to_dict(
                    mapping
                ).items()
            }

        self._java_api.create_join(
            self.name,
            other.name,
            mapping=normalized_mapping,
        )

    @property
    def scenarios(self) -> TableScenarios:
        """All the scenarios the table can be on."""
        if self.scenario != BASE_SCENARIO_NAME:
            raise RuntimeError(
                "You can only create a new scenario from the base scenario"
            )

        return TableScenarios(
            self,
            java_api=self._java_api,
            load_kafka=self._load_kafka,
            load_sql=self._load_sql,
            plugins=self._plugins,
        )

    @property
    def _loading_report(self) -> TableReport:
        return TableReport(
            _clear_reports=self._java_api.clear_loading_report,
            _get_reports=self._java_api.get_loading_report,
            _table_name=self.name,
        )

    def __getitem__(self, key: str, /) -> Column:
        """Return the column with the given name."""
        return self._columns[key]

    def __len__(self) -> int:
        """Return the number of rows in the table."""
        return self._java_api.get_table_size(self.name, table_scenario=self.scenario)

    def _ipython_key_completions_(self) -> IPythonKeyCompletions:
        return get_ipython_key_completions_for_mapping(self._columns)

    @doc(TABLE_APPEND_DOC, **_DOC_KWARGS)
    def append(self, *rows: _Row) -> None:
        rows_df = pd.DataFrame(rows, columns=list(self.columns))
        self.load_pandas(rows_df)

    @doc(TABLE_IADD_DOC, **_DOC_KWARGS)
    def __iadd__(self, row: _Row) -> Table:
        """Add a single row to the table."""
        self.append(row)
        return self

    def drop(
        self,
        filter: Optional[  # noqa: A002
            Condition[
                ColumnCoordinates,
                ConditionComparisonOperatorBound,
                Optional[Constant],
                ConditionCombinationOperatorBound,
            ]
        ] = None,
        /,
    ) -> None:
        """Delete some of the table's rows.

        Args:
            filter: Rows where this condition evaluates to ``True`` will be deleted.
                If ``None``, all the rows will be deleted.

        Example:
            >>> df = pd.DataFrame(
            ...     columns=["City", "Price"],
            ...     data=[
            ...         ("London", 240.0),
            ...         ("New York", 270.0),
            ...         ("Paris", 200.0),
            ...     ],
            ... )
            >>> table = session.read_pandas(df, keys=["City"], table_name="Cities")
            >>> table.head().sort_index()
                      Price
            City
            London    240.0
            New York  270.0
            Paris     200.0
            >>> table.drop((table["City"] == "Paris") | (table["Price"] <= 250.0))
            >>> table.head().sort_index()
                      Price
            City
            New York  270.0
            >>> table.drop()
            >>> table.head()
            Empty DataFrame
            Columns: [Price]
            Index: []
        """
        if filter is not None:
            check_column_condition_table(
                filter, attribute_name="subject", expected_table_name=self.name
            )

        self._java_api.delete_rows_from_table(
            table_name=self.name,
            scenario_name=self.scenario,
            condition=filter,
        )

    def _repr_json_(self) -> ReprJson:
        return {
            name: column._repr_json_()[0] for name, column in self._columns.items()
        }, {"expanded": True, "root": self.name}

    def head(self, n: int = 5) -> pd.DataFrame:
        """Return at most *n* random rows of the table as a pandas DataFrame."""
        if n < 1:
            raise ValueError("n must be at least 1.")

        return self._java_api.get_table_dataframe(
            self.name,
            n,
            scenario_name=self.scenario,
        )

    @doc(**{**CSV_KWARGS, **CLIENT_SIDE_ENCRYPTION_DOC})
    def load_csv(
        self,
        path: Union[pathlib.Path, str],
        /,
        *,
        columns: Mapping[str, str] = EMPTY_MAPPING,
        separator: Optional[str] = ",",
        encoding: str = "utf-8",
        process_quotes: Optional[bool] = True,
        array_separator: Optional[str] = None,
        date_patterns: Mapping[str, str] = EMPTY_MAPPING,
        client_side_encryption: Optional[ClientSideEncryptionConfig] = None,
        **kwargs: Any,
    ) -> None:
        """Load a CSV into this scenario.

        Args:
            {path}
            {columns}
            {separator}
            {encoding}
            {process_quotes}
            {array_separator}
            {date_patterns}
            {client_side_encryption}
        """
        private_parameters = CsvPrivateParameters(**kwargs)

        path, pattern = split_path_and_pattern(path, ".csv", plugins=self._plugins)

        CsvDataSource(
            load_data_into_table=self._java_api.load_data_into_table,
            discover_csv_file_format=self._java_api.discover_csv_file_format,
        ).load_csv_into_table(
            path=path,
            table_name=self.name,
            columns=columns,
            scenario_name=self.scenario,
            separator=separator,
            encoding=encoding,
            process_quotes=process_quotes,
            array_separator=array_separator,
            pattern=pattern,
            date_patterns=date_patterns,
            client_side_encryption=client_side_encryption,
            parser_thread_count=private_parameters.parser_thread_count,
            buffer_size_kb=private_parameters.buffer_size_kb,
        )

    def load_pandas(
        self,
        dataframe: pd.DataFrame,
        /,
    ) -> None:
        """Load a pandas DataFrame into this scenario.

        Args:
            dataframe: The DataFrame to load.
        """
        arrow_table = pandas_to_arrow(dataframe, types=self._types)
        self.load_arrow(arrow_table)

    def load_arrow(
        self,
        table: pa.Table,  # pyright: ignore[reportUnknownParameterType]
        /,
    ) -> None:
        """Load an Arrow Table into this scenario.

        Args:
            table: The Arrow Table to load.
        """
        with tempfile.TemporaryDirectory() as directory:
            filepath = pathlib.Path(directory) / "table.arrow"
            write_arrow_to_file(table, filepath=filepath)
            ArrowDataSource(
                load_data_into_table=self._java_api.load_data_into_table
            ).load_arrow_into_table(
                table_name=self.name, path=str(filepath), scenario_name=self.scenario
            )

    def load_numpy(
        self,
        array: NDArray[Any],
        /,
    ) -> None:
        """Load a NumPy 2D array into this scenario.

        Args:
            array: The 2D array to load.
        """
        dataframe = pd.DataFrame(array, columns=list(self.columns))
        self.load_pandas(dataframe)

    @doc(**{**PARQUET_KWARGS, **CLIENT_SIDE_ENCRYPTION_DOC})
    def load_parquet(
        self,
        path: Union[pathlib.Path, str],
        /,
        *,
        columns: Mapping[str, str] = EMPTY_MAPPING,
        client_side_encryption: Optional[ClientSideEncryptionConfig] = None,
    ) -> None:
        """Load a Parquet file into this scenario.

        Args:
            {path}
            {columns}
            {client_side_encryption}
        """
        path, pattern = split_path_and_pattern(path, ".parquet", plugins=self._plugins)
        ParquetDataSource(
            load_data_into_table=self._java_api.load_data_into_table,
            infer_types=self._java_api.infer_table_types_from_source,
        ).load_parquet_into_table(
            path=path,
            table_name=self.name,
            columns=columns,
            scenario_name=self.scenario,
            pattern=pattern,
            client_side_encryption=client_side_encryption,
        )

    @typecheck(ignored_params=["dataframe"])
    def load_spark(
        self,
        dataframe: SparkDataFrame,
        /,
    ) -> None:
        """Load a Spark DataFrame into this scenario.

        Args:
            dataframe: The dataframe to load.
        """
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "spark"
            write_spark_to_parquet(dataframe, directory=path)
            self.load_parquet(path)

    def load_kafka(
        self,
        bootstrap_server: str,
        topic: str,
        *,
        group_id: str,
        batch_duration: int = 1000,
        consumer_config: Mapping[str, str] = EMPTY_MAPPING,
    ) -> None:
        """Consume a Kafka topic and stream its records in the table.

        Note:
            This method requires the :mod:`atoti-kafka <atoti_kafka>` plugin.

        The records' key deserializer default to `StringDeserializer <https://kafka.apache.org/21/javadoc/org/apache/kafka/common/serialization/StringDeserializer.html>`__.

        The records' message must be a JSON object with columns' name as keys.

        Args:
            bootstrap_server: ``host[:port]`` that the consumer should contact to bootstrap initial cluster metadata.
            topic: Topic to subscribe to.
            group_id: The name of the consumer group to join.
            batch_duration: Milliseconds spent batching received records before publishing them to the table.
                If ``0``, received records are immediately published to the table.
                Must not be negative.
            consumer_config: Mapping containing optional parameters to set up the KafkaConsumer.
                The list of available params can be found `here <https://kafka.apache.org/10/javadoc/index.html?org/apache/kafka/clients/consumer/ConsumerConfig.html>`__.
        """
        return self._load_kafka(
            self,
            bootstrap_server,
            topic,
            group_id=group_id,
            batch_duration=batch_duration,
            consumer_config=consumer_config,
        )

    @doc(
        **SQL_KWARGS,
        # Declare the types here because blackdoc and doctest conflict when inlining it in the docstring.
        types="""{"ID": tt.INT, "CITY": tt.STRING, "MY_VALUE": tt.DOUBLE}""",
    )
    def load_sql(
        self,
        sql: str,
        *,
        url: str,
        driver: Optional[str] = None,
    ) -> None:
        """Load the result of the passed SQL query into the table.

        Note:
            This method requires the :mod:`atoti-sql <atoti_sql>` plugin.

        Args:
            {sql}
            {url}
            {driver}

        Example:
            .. doctest:: load_sql

                >>> table = session.create_table("Cities", types={types}, keys=["ID"])
                >>> table.load_sql(
                ...     "SELECT * FROM MYTABLE;",
                ...     url=f"h2:file:{{RESOURCES}}/h2-database;USER=root;PASSWORD=pass",
                ... )
                >>> len(table)
                5

            .. doctest:: load_sql
                :hide:

                Remove the edited H2 database from Git's working tree.
                >>> session.close()
                >>> import os
                >>> os.system(f"git checkout -- {{RESOURCES}}/h2-database.mv.db")
                0
        """
        return self._load_sql(self, sql, url=url, driver=driver)

    def _query(
        self,
        *columns: Column,
        filter: Optional[  # noqa: A002
            Condition[
                ColumnCoordinates,
                ConditionComparisonOperatorBound,
                Constant,
                ConditionCombinationOperatorBound,
            ]
        ] = None,
        max_rows: int = JAVA_MAX_INT - 1,
    ) -> pd.DataFrame:
        for column in columns:
            if column._table_name != self.name:
                raise ValueError(
                    f"Expected all columns to be from table `{self.name}` but got column `{column.name}` from table `{column._table_name}`."
                )

        query = urlencode({"pageSize": max_rows})

        conditions = (
            condition_to_json_serializable_dict(filter) if filter is not None else {}  # type: ignore[var-annotated]
        )

        body = {
            "fields": [column.name for column in columns] if columns else None,
            "conditions": conditions,
        }
        route = f"database/data/tables/{quote(self.name)}"

        response = self._client.fetch_json(
            body=body,
            method="POST",
            namespace="activeviam/pivot",
            query=query,
            route=route,
        )
        assert isinstance(response.body, dict)

        types: dict[str, DataType] = {
            column_name: self[column_name].data_type for column_name in self.columns
        }

        for header in response.body["headers"]:
            column_name = header["name"]
            assert (
                parse_data_type(header["type"]) == types[column_name]
            ), f"Unexpected data type for column `{column_name}`."

        return create_dataframe(
            response.body["rows"],
            [
                DataFrameColumnDescription(
                    header["name"],
                    types[header["name"]],
                    nullable=self[header["name"]].default_value is None,
                )
                for header in response.body["headers"]
            ],
        )


class TableScenarios:
    """Scenarios of a table."""

    def __init__(
        self,
        table: Table,
        /,
        *,
        java_api: JavaApi,
        load_kafka: _LoadKafka,
        load_sql: _LoadSql,
        plugins: Mapping[str, Plugin],
    ) -> None:
        self._java_api = java_api
        self._load_kafka = load_kafka
        self._load_sql = load_sql
        self._table = table
        self._plugins = plugins

    def __getitem__(self, key: str, /) -> Table:
        """Get the scenario or create it if it does not exist.

        Args:
            key: the name of the scenario

        """
        return Table(
            self._table.name,
            client=self._table._client,
            java_api=self._java_api,
            load_kafka=self._load_kafka,
            load_sql=self._load_sql,
            plugins=self._plugins,
            scenario=key,
        )

    def __delitem__(self, key: str, /) -> None:
        raise RuntimeError(
            "You cannot delete a scenario from a table since they are shared between all tables."
            "Use the Session.delete_scenario() method instead."
        )


class _LoadKafka(Protocol):
    def __call__(
        self,
        table: Table,
        /,
        bootstrap_server: str,
        topic: str,
        *,
        group_id: str,
        batch_duration: int,
        consumer_config: Mapping[str, str],
    ) -> None:
        ...


class _LoadSql(Protocol):
    def __call__(
        self,
        table: Table,
        /,
        sql: str,
        *,
        url: str,
        driver: Optional[str] = None,
    ) -> None:
        ...
