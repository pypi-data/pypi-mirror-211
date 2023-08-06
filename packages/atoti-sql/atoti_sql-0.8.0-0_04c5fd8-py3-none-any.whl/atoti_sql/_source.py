from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any, Optional

import atoti as tt
from atoti._jdbc_utils import normalize_jdbc_url
from atoti._sources.data_source import DataSource, InferTypes, LoadDataIntoTable
from atoti_core import Constant, ConstantValue

from ._infer_driver import infer_driver


def _create_source_params(
    *,
    driver: str,
    sql: str,
    url: str,
) -> dict[str, Any]:
    return {
        "driverClass": driver,
        "query": sql,
        "url": url,
    }


class SqlDataSource(DataSource):
    def __init__(
        self, *, infer_types: InferTypes, load_data_into_table: LoadDataIntoTable
    ) -> None:
        super().__init__(load_data_into_table=load_data_into_table)

        self._infer_types = infer_types

    @property
    def key(self) -> str:
        return "JDBC"

    def load_sql_into_table(
        self,
        sql: str,
        *,
        driver: str,
        scenario_name: str,
        table: tt.Table,
        url: str,
    ) -> None:
        source_params = _create_source_params(
            driver=driver,
            sql=sql,
            url=url,
        )
        self.load_data_into_table(
            table.name,
            scenario_name=scenario_name,
            source_params=source_params,
        )

    def infer_sql_types(
        self,
        sql: str,
        *,
        keys: Iterable[str],
        default_values: Mapping[str, Optional[Constant]],
        url: str,
        driver: str,
    ) -> dict[str, tt.DataType]:
        source_params = _create_source_params(
            driver=driver,
            sql=sql,
            url=url,
        )
        return self._infer_types(
            source_key=self.key,
            keys=keys,
            default_values=default_values,
            source_params=source_params,
        )


def read_sql(
    session: tt.Session,
    /,
    sql: str,
    *,
    url: str,
    table_name: str,
    driver: Optional[str] = None,
    keys: Iterable[str],
    partitioning: Optional[str] = None,
    types: Mapping[str, tt.DataType],
    default_values: Mapping[str, Optional[ConstantValue]],
) -> tt.Table:
    url = normalize_jdbc_url(url)
    inferred_types = SqlDataSource(
        load_data_into_table=session._java_api.load_data_into_table,
        infer_types=session._java_api.infer_table_types_from_source,
    ).infer_sql_types(
        sql,
        keys=keys,
        default_values={
            column_name: None if value is None else Constant(value)
            for column_name, value in default_values.items()
        },
        url=url,
        driver=driver or infer_driver(url),
    )
    types = {**inferred_types, **types} if types is not None else inferred_types
    table = session.create_table(
        table_name,
        types=types,
        keys=keys,
        partitioning=partitioning,
        default_values=default_values,
    )
    load_sql(table, sql, url=url, driver=driver)
    return table


def load_sql(
    table: tt.Table,
    /,
    sql: str,
    *,
    url: str,
    driver: Optional[str] = None,
) -> None:
    url = normalize_jdbc_url(url)
    SqlDataSource(
        load_data_into_table=table._java_api.load_data_into_table,
        infer_types=table._java_api.infer_table_types_from_source,
    ).load_sql_into_table(
        sql,
        driver=driver or infer_driver(url),
        scenario_name=table.scenario,
        table=table,
        url=url,
    )
