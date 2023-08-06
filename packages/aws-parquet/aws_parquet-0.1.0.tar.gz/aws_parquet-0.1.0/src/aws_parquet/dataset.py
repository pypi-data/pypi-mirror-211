"""Dataset for Parquet files in S3."""
import os
import warnings
import awswrangler as wr
from typing import (
    Any,
    Callable,
    Iterator,
    List,
    Literal,
    Tuple,
    Dict,
    Optional,
    Union,
    cast,
    overload,
)
import pandas as pd
import pandera as pa
from abc import abstractmethod
from typeguard import typechecked

from aws_parquet._types import PartitionLike, DataFrameOrIteratorT
from aws_parquet.interface import ParquetDatasetInterface


@typechecked
def extract_partitions_metadata_from_paths(
    path: str, paths: List[str]
) -> Tuple[Optional[Dict[str, str]], Optional[Dict[str, List[str]]]]:
    """Extract partitions metadata from Amazon S3 paths."""
    path = path if path.endswith("/") else f"{path}/"
    partitions_types: Dict[str, str] = {}
    partitions_values: Dict[str, List[str]] = {}
    for p in paths:
        if path not in p:
            raise ValueError(f"Object {p} is not under the root path ({path}).")
        path_wo_filename: str = p.rpartition("/")[0] + "/"
        if path_wo_filename not in partitions_values:
            path_wo_prefix: str = path_wo_filename.replace(f"{path}/", "")
            dirs: Tuple[str, ...] = tuple(
                x
                for x in path_wo_prefix.split("/")
                if (x != "") and (x.count("=") == 1)
            )
            if dirs:
                values_tups = cast(
                    Tuple[Tuple[str, str]], tuple(tuple(x.split("=")[:2]) for x in dirs)
                )
                values_dics: Dict[str, str] = dict(values_tups)
                p_values: List[str] = list(values_dics.values())
                p_types: Dict[str, str] = {x: "string" for x in values_dics.keys()}
                if not partitions_types:
                    partitions_types = p_types
                if p_values:
                    partitions_types = p_types
                    partitions_values[path_wo_filename] = p_values
                elif p_types != partitions_types:
                    raise ValueError(
                        f"At least two different partitions schema detected: "
                        f"{partitions_types} and {p_types}"
                    )
    if not partitions_types:
        return None, None
    return partitions_types, partitions_values


@typechecked
class ParquetDataset(ParquetDatasetInterface):
    """Dataset for Parquet files in S3."""

    @property
    @abstractmethod
    def partition_cols(self) -> List[str]:
        """Return the partition columns."""
        ...

    @property
    @abstractmethod
    def database(self) -> str:
        """Return the name of the database."""
        ...

    @property
    @abstractmethod
    def table(self) -> str:
        """Return the name of the dataset."""
        ...

    @property
    @abstractmethod
    def path(self) -> str:
        """Return the path of the dataset."""
        ...

    @property
    @abstractmethod
    def schema(self) -> pa.DataFrameSchema:
        """Return the schema of the dataset."""

    @property
    def compression(self) -> Literal["snappy", "gzip", None]:
        """Return the compression of the dataset."""
        return "snappy"

    @property
    def categorical_columns(self) -> List[str]:
        """Return the categorical columns of the dataset."""
        return [
            col_name
            for col_name, col_schema in self.schema.columns.items()
            if str(col_schema.dtype) == "category"
        ]

    @property
    def columns(self) -> List[str]:
        """Return the columns of the dataset."""
        return list(self.schema.columns.keys())

    def _build_coercible_schema_given_columns(
        self, columns: Optional[List[str]] = None
    ) -> pa.DataFrameSchema:
        """Build the schema given a list of columns."""
        if columns is None:
            schema = self.schema
            schema.coerce = True
            return schema

        schema = pa.DataFrameSchema(
            columns={
                col_name: col_schema
                for col_name, col_schema in self.schema.columns.items()
                if col_name in columns
            }
        )
        schema.coerce = True
        return schema

    def _build_coercible_schema_given_partition(
        self, partition: PartitionLike
    ) -> pa.DataFrameSchema:
        """Build the schema of the partition."""
        return self._build_coercible_schema_given_columns(
            columns=list(partition.keys())
        )

    def _get_sample_df(self) -> pd.DataFrame:
        """Return a sample dataframe with the dataset schema."""
        cols = []
        for col, pa_col in self.schema.columns.items():
            s = pd.Series([], dtype=pa_col.dtype.type, name=col)
            cols.append(s)
        return pd.concat(cols, axis=1)

    def _get_athena_columns_types(self) -> Dict[str, str]:
        """Return the columns types for Athena."""
        df = self._get_sample_df()
        col_types, _ = wr._data_types.athena_types_from_pandas_partitioned(
            df=df,
            index=False,
            partition_cols=self.partition_cols,
        )

        return col_types

    def _get_athena_partitions_types(self) -> Dict[str, str]:
        """Return the partitions types for Athena."""
        df = self._get_sample_df()
        _, part_types = wr._data_types.athena_types_from_pandas_partitioned(
            df=df,
            index=False,
            partition_cols=self.partition_cols,
        )

        return part_types

    def _discover_partitions_from_s3(self) -> Optional[Dict[str, List[str]]]:
        paths = wr.s3.list_objects(path=self.path)

        _, partition_values = extract_partitions_metadata_from_paths(
            path=self.path, paths=paths
        )
        return partition_values

    def create(
        self,
        if_exists: Literal["ignore", "warn", "raise"] = "ignore",
        sync: bool = True,
    ) -> None:
        """Create the dataset."""
        table_exists_in_catalog = wr.catalog.does_table_exist(
            database=self.database, table=self.table
        )
        if table_exists_in_catalog:
            if if_exists == "warn":
                warnings.warn(
                    message=(
                        f"Table {self.table} already exists"
                        f" in database {self.database}."
                    ),
                    category=RuntimeWarning,
                )

            elif if_exists == "raise":
                raise RuntimeError(
                    f"Table {self.table} already exists in database {self.database}."
                )

            elif if_exists == "ignore":
                return

        wr.catalog.create_parquet_table(
            database=self.database,
            path=self.path,
            table=self.table,
            columns_types=self._get_athena_columns_types(),
            partitions_types=self._get_athena_partitions_types(),
        )

        if sync:
            self.sync()

    def sync(self) -> None:
        """Sync the dataset between s3 and glue.

        Note this is mainly required if the dataset has been modified outside
        of this class.
        """
        partition_values = self._discover_partitions_from_s3()

        wr.catalog.delete_all_partitions(database=self.database, table=self.table)

        if partition_values is not None:
            wr.catalog.add_parquet_partitions(
                database=self.database,
                table=self.table,
                partitions_values=partition_values,
                compression=self.compression,
                columns_types=self._get_athena_columns_types(),
            )

    def _build_partition_filter(
        self, partition_values: PartitionLike
    ) -> Callable[[Dict[str, str]], bool]:
        """Build a partition filter function."""

        def compare_partition(partition: PartitionLike) -> bool:
            """Compare the partition."""
            partition_df = pd.DataFrame(
                {k: [v] for k, v in partition.items() if k in partition_values.keys()}
            )
            partition_schema = self._build_coercible_schema_given_partition(
                partition_values
            )
            partition_df_coerced = partition_schema(partition_df)

            partition_values_df = pd.DataFrame(
                {k: [v] for k, v in partition_values.items()}
            )
            partition_values_coerced = partition_schema(partition_values_df)
            return cast(bool, partition_df_coerced.equals(partition_values_coerced))

        return compare_partition

    def _apply_schema(
        self, df: pd.DataFrame, schema: pa.DataFrameSchema
    ) -> pd.DataFrame:
        out = schema(df)
        return out[self.columns]

    def _coerce_and_check_schema(
        self,
        df: DataFrameOrIteratorT,
        columns: Optional[List[str]],
    ) -> DataFrameOrIteratorT:
        """Coerce the schema and check the schema."""
        schema = self._build_coercible_schema_given_columns(columns)
        if isinstance(df, pd.DataFrame):
            return cast(DataFrameOrIteratorT, self._apply_schema(df=df, schema=schema))

        elif isinstance(df, Iterator):
            return cast(
                DataFrameOrIteratorT,
                (self._apply_schema(df=sub_df, schema=schema) for sub_df in df),
            )

        else:
            raise TypeError("df must be a DataFrame or an Iterator of DataFrames.")

    @overload
    def read(
        self,
        partition: Optional[PartitionLike] = None,
        chunked: Literal[False] = False,
        columns: Optional[List[str]] = None,
        use_threads: bool = True,
    ) -> pd.DataFrame:
        ...

    @overload
    def read(
        self,
        partition: Optional[PartitionLike] = None,
        chunked: Literal[True] = True,
        columns: Optional[List[str]] = None,
        use_threads: bool = True,
    ) -> Iterator[pd.DataFrame]:
        ...

    def read(
        self,
        partition: Optional[PartitionLike] = None,
        chunked: bool = False,
        columns: Optional[List[str]] = None,
        use_threads: bool = True,
    ) -> Union[pd.DataFrame, Iterator[pd.DataFrame]]:
        """Read the dataset optionally from a given partition."""
        partition_filter = (
            self._build_partition_filter(partition) if partition is not None else None
        )

        out = wr.s3.read_parquet(
            path=self.path,
            dataset=True,
            chunked=chunked,
            partition_filter=partition_filter,
            columns=columns,
            use_threads=use_threads,
        )

        return self._coerce_and_check_schema(out, columns=columns)

    @overload
    def query(
        self,
        sql: str,
        *,
        workgroup: Optional[str] = None,
        chunksize: None = None,
        ctas_approach: bool = True,
        use_threads: bool = True,
        **kwargs: Any,
    ) -> pd.DataFrame:
        ...

    @overload
    def query(
        self,
        sql: str,
        *,
        workgroup: Optional[str] = None,
        chunksize: Union[int, bool],
        ctas_approach: bool = True,
        use_threads: bool = True,
        **kwargs: Any,
    ) -> Iterator[pd.DataFrame]:
        ...

    def query(
        self,
        sql: str,
        *,
        workgroup: Optional[str] = None,
        chunksize: Optional[Union[int, bool]] = None,
        ctas_approach: bool = True,
        use_threads: bool = True,
        **kwargs: Any,
    ) -> Union[pd.DataFrame, Iterator[pd.DataFrame]]:
        """Perform an athena query on the parquet dataset."""
        return wr.athena.read_sql_query(
            sql=sql,
            categories=self.categorical_columns,
            ctas_approach=ctas_approach,
            database=self.database,
            chunksize=chunksize,
            use_threads=use_threads,
            workgroup=workgroup,
            **kwargs,
        )

    def update(self, data: pd.DataFrame, overwrite: bool = False) -> None:
        """Update the dataset."""
        schema = self._build_coercible_schema_given_columns()
        input_df = schema(data)
        wr.s3.to_parquet(
            df=input_df,
            path=self.path,
            dataset=True,
            mode="overwrite_partitions" if overwrite else "append",
            partition_cols=self.partition_cols,
            database=self.database,
            table=self.table,
        )

    def _get_partition_record(self, partition: PartitionLike) -> Dict[str, str]:
        """Get the partition record."""
        partition_df = pd.DataFrame({k: [v] for k, v in partition.items()})
        partition_schema = self._build_coercible_schema_given_partition(partition)
        partition_df_coerced = partition_schema(partition_df)
        partition_record = partition_df_coerced.to_dict(orient="records")[0]
        return {k: str(v) for k, v in partition_record.items()}

    def _build_path(self, partition_record: PartitionLike) -> str:
        """Build the path pattern for a given partition."""
        path = self.path
        for col in self.partition_cols:
            if col in partition_record:
                val = partition_record[col]
                path = os.path.join(path, f"{col}={val}/")
            else:
                path = os.path.join(path, "*/")

        path = os.path.join(path, "*")
        return path

    def delete(self, partition: Optional[PartitionLike] = None) -> None:
        """Delete data optionally only a given partition."""
        if partition:
            partition_record = self._get_partition_record(partition)
            path = self._build_path(partition_record)
            _, partition_values = extract_partitions_metadata_from_paths(
                path=self.path, paths=wr.s3.list_objects(path)
            )

            if partition_values:
                for path, part_vals in partition_values.items():
                    wr.s3.delete_objects(path)
                    wr.catalog.delete_partitions(
                        database=self.database,
                        table=self.table,
                        partitions_values=[part_vals],
                    )

        else:
            wr.s3.delete_objects(path=self.path)
            wr.catalog.delete_table_if_exists(database=self.database, table=self.table)
