import typing

import pandas as pd
from pydantic import BaseModel, ValidationError

from .types import cast_series


def cast(
    df: pd.DataFrame, model: typing.Type[BaseModel], datetime_format: str = "%Y-%m-%d", strict: bool = False
) -> pd.DataFrame:
    if not isinstance(df, pd.DataFrame):
        raise ValueError()

    if strict:
        if set(df.columns) == set(model.__fields__.keys()):
            raise ValueError("dataframe is different from spefified schema.")

    for col in df.columns:
        typ = typing.cast(typing.Type, model.__fields__[col].type_)
        df[col] = cast_series(typ, df[col], datetime_format)
    return df


def validate(df: pd.DataFrame, model: typing.Type[BaseModel]) -> bool:
    if not isinstance(df, pd.DataFrame):
        raise ValueError()

    record_ls = df.to_dict(orient="records")
    for record in record_ls:
        try:
            model.parse_obj(record)
        except ValidationError:
            return False
    return True
