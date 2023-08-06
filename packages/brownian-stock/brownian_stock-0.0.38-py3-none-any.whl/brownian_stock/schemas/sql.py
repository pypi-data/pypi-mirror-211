from typing import Dict, List, Type

import pandas as pd
from brownian_stock.schemas.types import Datetime64
from pydantic import BaseModel, StrictBool, StrictFloat, StrictInt, StrictStr


def create_table_query(model: Type[BaseModel], table_name: str) -> str:
    conversion_dict = {
        str: "str",
        int: "integer",
        float: "real",
        bool: "bool",
        Datetime64: "str",
        StrictStr: "str",
        StrictInt: "integer",
        StrictFloat: "real",
        StrictBool: "bool",
    }
    definition: Dict[str, str] = {}
    for key in sorted(model.__fields__.keys()):
        field = model.__fields__[key]
        sql_type = conversion_dict[field.type_]
        definition[key] = sql_type

    fields_str = ", ".join([f"'{k}' {v}" for k, v in definition.items()])
    query = f"CREATE TABLE {table_name}(id INTEGER PRIMARY KEY AUTOINCREMENT, {fields_str});"
    return query


def read_sql_query(model: Type[BaseModel], table_name: str, conditions: List[str] = []) -> pd.DataFrame:
    columns = list(sorted(model.__fields__.keys()))

    columns_query = ", ".join(columns)
    where_query = " AND ".join(conditions)

    query = "SELECT {} " "FROM {}"
    query = query.format(columns_query, table_name)

    if len(conditions) > 0:
        query = query + " WHERE " + where_query
    query += ";"
    return query
