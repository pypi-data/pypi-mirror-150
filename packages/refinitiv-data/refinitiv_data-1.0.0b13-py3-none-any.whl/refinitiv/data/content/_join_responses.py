from types import SimpleNamespace
from typing import List, Callable

import pandas as pd
from pandas import DataFrame

from ..delivery._data._data_provider import Response, Data


def join_dfs(dfs: List[DataFrame], how: str = "inner") -> DataFrame:
    if len(dfs) == 0:
        raise ValueError(f"Cannot join dfs, because dfs list is empty, dfs={dfs}")

    df = dfs.pop()
    df = df.join(dfs, how=how)  # noqa
    df = df.convert_dtypes()

    return df


def join_responses(
    responses: List[Response],
    join_dataframes: Callable = pd.concat,
    response_class=Response,
    data_class=Data,
    reset_index=False,
) -> Response:
    def build_df(*args, **kwargs):
        dfs = []
        df = None

        for response in responses:
            dfs.append(response.data.df)

        all_dfs_is_none = all(a is None for a in dfs)
        if not all_dfs_is_none:
            df = join_dataframes(dfs)

        if reset_index and df is not None:
            df = df.reset_index(drop=True)

        return df

    if len(responses) == 1:
        return responses[0]

    raws = []
    http_statuses = []
    http_headers = []
    request_messages = []
    http_responses = []
    errors = []
    is_successes = []

    for response in responses:
        raws.append(response.data.raw)
        http_statuses.append(response.http_status)
        http_headers.append(response.http_headers)
        request_messages.append(response.request_message)
        http_responses.append(response.http_response)
        is_successes.append(response.is_success)

        if response.errors:
            errors += response.errors

    raw_response = SimpleNamespace()
    raw_response.headers = http_headers
    raw_response.request = request_messages
    is_success = any(is_successes)
    response = response_class(raw_response=raw_response, is_success=is_success)
    response.data = data_class(raws, dfbuilder=build_df)
    response.errors += errors
    response.http_response = http_responses
    response._status = http_statuses

    return response
