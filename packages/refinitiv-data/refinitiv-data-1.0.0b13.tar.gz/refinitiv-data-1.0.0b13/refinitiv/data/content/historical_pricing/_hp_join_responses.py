from types import SimpleNamespace
from typing import List, Tuple

import numpy as np
import pandas as pd
from pandas import DataFrame

from .._join_responses import join_dfs
from ...delivery._data._data_provider import Data, Response
from ...errors import RDError


def copy_fields(fields: List[str]) -> List[str]:
    if not (fields is None or isinstance(fields, list)):
        raise AttributeError(f"fields not support type {type(fields)}")

    fields = fields or []
    return fields[:]


def join_responses_hp_summaries(
    responses: List[Tuple[str, Response]],
    fields: List[str],
    kwargs,
) -> Response:
    from ._hp_data_provider import axis_by_day_interval_type

    index_name = "Date"
    new_axis_name = axis_by_day_interval_type.get(kwargs.get("day_interval_type"))
    response = join_responses(responses, new_axis_name, index_name, fields)
    return response


def join_responses_hp_events(
    responses: List[Tuple[str, Response]],
    fields: List[str],
    kwargs,
) -> Response:
    axis_name = "Timestamp"
    new_axis_name = axis_name
    index_name = axis_name
    response = join_responses(responses, new_axis_name, index_name, fields)
    return response


def get_first_success_response(responses: List[Tuple[str, Response]]) -> Response:
    successful = (response for _, response in responses if response.is_success)
    first_successful = next(successful, None)
    return first_successful


def validate_responses(responses: List[Tuple[str, Response]]):
    response = get_first_success_response(responses)
    if response is None:
        error_message = "ERROR: No successful response.\n"
        for inst_name, response in responses:
            if response.errors:
                error = response.errors[0]
                error_message += "({}, {}), ".format(error.code, error.message)
        error_message = error_message[:-2]
        raise RDError(1, f"No data to return, please check errors: {error_message}")


def join_responses(
    responses: List[Tuple[str, Response]],
    new_axis_name: str,
    index_name: str,
    fields: List[str],
) -> Response:
    if len(responses) == 1:
        inst_name, response = responses[0]

        if not response.is_success:
            return response

        def build_df(*args, **kwargs) -> DataFrame:
            df = data.df

            if fields:
                not_valid_columns = set(fields) - set(df.columns.values)
                df = df.assign(
                    **{column_name: np.NaN for column_name in not_valid_columns}
                )

            df.axes[1].name = inst_name
            df.index.name = index_name
            return df

        data = response.data
        response.data = Data(response.data.raw, dfbuilder=build_df)
        return response

    def build_df_as_join_dfs(*args, **kwargs) -> DataFrame:
        response = get_first_success_response(responses)

        if not response:
            return DataFrame()

        df = response.data.df

        index = df.index.to_numpy()
        columns = (None,)

        dfs = []
        for inst_name, response in responses:
            df = response.data.df

            if fields and response.is_success:
                not_valid_columns = set(fields) - set(df.columns.values)
                df = df.assign(
                    **{column_name: np.NaN for column_name in not_valid_columns}
                )

            elif fields and df is None:
                df = DataFrame(columns=fields, index=index)

            elif df is None:
                df = DataFrame(columns=columns, index=index)

            df.columns = pd.MultiIndex.from_product([[inst_name], df.columns])
            dfs.append(df)

        df = join_dfs(dfs, how="outer")

        if not df.empty:
            df = df.rename_axis(new_axis_name)

        return df

    raws = []
    errors = []
    http_statuses = []
    http_headers = []
    http_responses = []
    request_messages = []

    for inst_name, response in responses:
        raws.append(response.data.raw)
        http_statuses.append(response.http_status)
        http_headers.append(response.http_headers)
        request_messages.append(response.request_message)
        http_responses.append(response.http_response)

        if response.errors:
            errors += response.errors

    raw_response = SimpleNamespace()
    raw_response.request = request_messages
    raw_response.headers = http_headers
    response = Response(raw_response=raw_response, is_success=True)
    response.errors += errors
    response.data = Data(raws, dfbuilder=build_df_as_join_dfs)
    response._status = http_statuses
    response.http_response = http_responses

    return response
