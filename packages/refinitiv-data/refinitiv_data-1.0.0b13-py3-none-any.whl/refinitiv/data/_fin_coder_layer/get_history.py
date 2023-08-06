import re
from collections import Counter
from datetime import datetime, timedelta, date
from typing import Union, Optional, Callable, List

import pandas as pd
from numpy import nan
from pandas import DataFrame, Index
from pandas import MultiIndex
from pandas import to_datetime

from .get_data import ADC_TR_PATTERN, ADC_FUNC_PATTERN_IN_FIELDS
from .get_data import _add_flag
from .get_data import _convert_date_columns_to_datetime
from .get_data import _create_default_df
from .get_data import _find_and_rename_duplicated_columns
from .get_data import _look_for_two_exceptions
from .get_data import _rename_column_n_to_column
from .get_data import _send_request
from ..content import fundamental_and_reference
from ..content import historical_pricing
from ..content.historical_pricing._hp_data_provider import EventTypes
from .._core.session import get_default
from .._tools import fields_arg_parser, universe_arg_parser, ohlc, fr_datetime_adapter

EVENTS_INTERVALS = ["tick", "tas", "taq"]

INTERVALS = {
    "tick": {"event_types": None, "adc": "D"},
    "tas": {"event_types": EventTypes.TRADE, "adc": "D"},
    "taq": {"event_types": EventTypes.QUOTE, "adc": "D"},
    "minute": {"pricing": "PT1M", "adc": "D"},
    "1min": {"pricing": "PT1M", "adc": "D"},
    "5min": {"pricing": "PT5M", "adc": "D"},
    "10min": {"pricing": "PT10M", "adc": "D"},
    "30min": {"pricing": "PT30M", "adc": "D"},
    "60min": {"pricing": "PT60M", "adc": "D"},
    "hourly": {"pricing": "PT1H", "adc": "D"},
    "1h": {"pricing": "PT1H", "adc": "D"},
    "daily": {"pricing": "P1D", "adc": "D"},
    "1d": {"pricing": "P1D", "adc": "D"},
    "1D": {"pricing": "P1D", "adc": "D"},
    "7D": {"pricing": "P7D", "adc": "W"},
    "7d": {"pricing": "P7D", "adc": "W"},
    "weekly": {"pricing": "P1W", "adc": "W"},
    "1W": {"pricing": "P1W", "adc": "W"},
    "monthly": {"pricing": "P1M", "adc": "M"},
    "1M": {"pricing": "P1M", "adc": "M"},
    "quarterly": {"pricing": "P3M", "adc": "CQ"},
    "3M": {"pricing": "P3M", "adc": "CQ"},
    "6M": {"pricing": "P6M", "adc": "CS"},
    "yearly": {"pricing": "P1Y", "adc": "CY"},
    "1Y": {"pricing": "P1Y", "adc": "CY"},
}

NON_INTRA_DAY_INTERVALS = {
    "daily",
    "1d",
    "1D",
    "weekly",
    "7D",
    "7d",
    "1W",
    "monthly",
    "1M",
    "quarterly",
    "3M",
    "yearly",
    "1Y",
}


def get_history(
    universe: Union[str, list],
    fields: Union[str, list, None] = None,
    interval: Optional[str] = None,
    start: Union[str, date, datetime, timedelta] = None,
    end: Union[str, date, datetime, timedelta] = None,
    adjustments: Optional[str] = None,
    count: Optional[int] = None,
    use_field_names_in_headers: Optional[bool] = False,
) -> DataFrame:
    """
    With this tool you can request historical data from Pricing and ADC

    Parameters
    ----------
        universe: str | list
            instruments to request.
        fields: str | list, optional
            fields to request.
        interval: str, optional
            The consolidation interval. Supported intervals are:
            tick, tas, taq, minute, 1min, 5min, 10min, 30min, 60min, hourly, 1h, daily,
            1d, 1D, 7D, 7d, weekly, 1W, monthly, 1M, quarterly, 3M, 6M, yearly, 1Y
        start: str or date or datetime or timedelta, optional
            The start date and timestamp of the query in ISO8601 with UTC only
        end: str or date or datetime or timedelta, optional
            The end date and timestamp of the query in ISO8601 with UTC only
        adjustments : str, optional
            The adjustment
        count : int, optional
            The maximum number of data returned. Values range: 1 - 10000
        use_field_names_in_headers : bool, optional
            Return field name in headers instead of title

    Returns
    -------
    pandas.DataFrame

     Examples
    --------
    >>> get_history(universe="GOOG.O")
    >>> get_history(universe="GOOG.O", fields="tr.Revenue", interval="1Y")
    >>> get_history(
    ...     universe="GOOG.O",
    ...     fields=["BID", "ASK", "tr.Revenue"],
    ...     interval="1Y",
    ...     start="2015-01-01",
    ...     end="2020-10-01",
    ... )
    """

    if interval not in INTERVALS and interval is not None:
        raise ValueError(
            f"Not supported interval value.\nSupported intervals are:"
            f"{list(INTERVALS.keys())}"
        )

    _pricing_events = historical_pricing.events.Definition
    _pricing_summaries = historical_pricing.summaries.Definition

    _fundamental_data = fundamental_and_reference.Definition
    params = {
        "universe": universe,
        "fields": fields,
        "interval": interval,
        "start": start,
        "end": end,
        "adjustments": adjustments,
        "count": count,
        "use_field_names_in_headers": use_field_names_in_headers,
    }

    return _get_history(
        p_events=_pricing_events,
        p_summaries=_pricing_summaries,
        adc=_fundamental_data,
        params=params,
    )


def _get_history(
    p_events: Callable,
    p_summaries: Callable,
    adc: Callable,
    params: dict,
) -> DataFrame:
    logger = get_default().logger()

    universe = universe_arg_parser.get_list(params["universe"])
    universe = list(dict.fromkeys(universe))
    is_multiuniverse = len(universe) > 1
    interval = params["interval"]

    adc_df = DataFrame()
    _add_flag(adc_df)

    pricing_df = DataFrame()
    _add_flag(pricing_df)

    adc_params = _translate_pricing_params_to_adc(params)

    use_field_names_in_headers = params.pop("use_field_names_in_headers", False)

    if params["interval"] in EVENTS_INTERVALS:
        p_provider = p_events
        interval = params.pop("interval")
        params["eventTypes"] = INTERVALS[interval]["event_types"]
        index_name = "Timestamp"

    else:
        p_provider = p_summaries

        if params["interval"] is not None:
            params["interval"] = INTERVALS[params["interval"]]["pricing"]
        index_name = "Date"

    fields = fields_arg_parser.get_list(params["fields"] or [])

    adc_tr_fields = [i for i in fields if re.match(ADC_TR_PATTERN, i)]
    adc_funcs_in_fields = [i for i in fields if re.match(ADC_FUNC_PATTERN_IN_FIELDS, i)]

    adc_fields = adc_tr_fields + adc_funcs_in_fields

    pricing_fields = [i for i in fields if i not in adc_fields]

    _fields = adc_fields or ["TR.RIC"]
    adc_default_df = _create_default_df(universe, adc_fields)
    _adc_df = _send_request(
        data_provider=adc,
        params={
            "universe": universe,
            "fields": _fields,
            "parameters": adc_params,
            "row_headers": "date",
            "use_field_names_in_headers": use_field_names_in_headers,
        },
        logger=logger,
        default_df=adc_default_df,
    )

    # update universe
    if "Instrument" in _adc_df:
        instrument = _adc_df["Instrument"]
        universe = list(instrument) or universe
    elif "RIC" in _adc_df:
        instrument = _adc_df["RIC"]
        universe = list(instrument) or universe
    else:
        columns = [column[0] for column in _adc_df.columns if isinstance(column, tuple)]
        universe = columns or universe
    params["universe"] = universe

    if adc_fields:
        adc_df = _adc_df
    else:
        _add_flag(adc_df, {"raise_exception": True, "exception": ""})

    if params["fields"]:
        if pricing_fields:
            pricing_default_df = _create_default_pricing_df(
                universe, pricing_fields, is_multiuniverse
            )
            params["fields"] = pricing_fields
            pricing_df = _send_request(
                data_provider=p_provider,
                params=params,
                logger=logger,
                default_df=pricing_default_df,
            )
            _remove_field_if_not_requested(
                "EVENT_TYPE", pricing_fields, pricing_df, is_multiuniverse
            )
        else:
            _add_flag(pricing_df, {"raise_exception": True, "exception": ""})

    else:
        pricing_df = _send_request(
            data_provider=p_provider,
            params=params,
            logger=logger,
        )

    _look_for_two_exceptions(pricing_df, adc_df)

    if pricing_df.empty:
        result = adc_df

    elif adc_df.empty:
        result = pricing_df

    else:
        result = _merge(
            pricing_df, adc_df, index_name=index_name, multiindex=is_multiuniverse
        )

    result.ohlc = ohlc.__get__(result, None)
    result.replace({pd.NaT: pd.NA, nan: pd.NA}, inplace=True)

    result = _set_index_name_and_change_index_type(result, interval)
    result.sort_index(ascending=True, inplace=True)

    if isinstance(result.columns, MultiIndex):
        result = result.reindex(columns=sorted(result.columns))

    result = _sort_by_universe(result, universe)
    result = _update_columns_title(result)
    return result


def _sort_by_universe(df: DataFrame, universe: List[str]) -> DataFrame:
    length = len(universe)

    if length == 1:
        return df

    columns = df.columns

    def make_getidx():
        get_index = universe.index
        if isinstance(columns, MultiIndex):

            def geti(i):
                return i[0]

        else:

            def geti(i):
                return i

        def inner(i):
            try:
                index = get_index(geti(i))
            except ValueError:
                index = length
            return index

        return inner

    getidx = make_getidx()
    # [3, 0, 2, 1]
    curr_order = [getidx(col) for col in columns]
    # [0, 1, 2, 3]
    expected_order = list(range(length))
    if curr_order != expected_order:
        sorted_columns = (col for _, col in sorted(zip(curr_order, columns)))
        df = df.reindex(columns=sorted_columns)
    return df


def _update_columns_title(df: DataFrame) -> DataFrame:
    """
    Transform dataframe from:

                AAPL.O          IBM.N
                Revenue - Mean  Revenue - Mean
    Date
    2022-04-12  396147651250    <NA>
    2022-04-18  <NA>            60686514370

    to:

    Revenue - Mean  AAPL.O            IBM.N
    Date
    2022-04-12      396147651250      <NA>
    2022-04-18      <NA>              60686514370
    """

    columns = df.columns
    if isinstance(columns, MultiIndex):

        c = Counter(col[1] for col in columns if len(col) == 2)
        keys = list(c.keys())
        if len(keys) == 1:
            df.columns = Index([col[0] for col in columns], name=keys[0])

    return df


def _translate_pricing_params_to_adc(p_params: dict) -> dict:
    adc_params = {}

    if p_params["start"]:
        adc_params["SDate"] = fr_datetime_adapter.get_str(p_params["start"])

    if p_params["end"]:
        adc_params["EDate"] = fr_datetime_adapter.get_str(p_params["end"])

    if p_params["interval"]:
        adc_params["FRQ"] = INTERVALS[p_params["interval"]]["adc"]

    return adc_params


def _set_index_name_and_change_index_type(df, interval):
    if interval is not None:

        if interval not in NON_INTRA_DAY_INTERVALS:
            df.index.names = ["Timestamp"]

    if interval in NON_INTRA_DAY_INTERVALS or interval is None:

        if isinstance(df.index, pd.Index):
            df.index = pd.to_datetime(df.index)

        df.index = df.index.strftime("%Y-%m-%d")

    return df


def _merge(
    pricing_df: DataFrame, adc_df: DataFrame, index_name: str, multiindex: bool = False
) -> DataFrame:
    duplicated_columns = []
    if adc_df.index.name in {"Date", "date"}:
        date_column = adc_df.index.name
    else:
        date_column = "Date"

    if "instrument" in adc_df:
        instrument_column = "instrument"
    else:
        instrument_column = "Instrument"

    if not (adc_df.index.name == date_column):
        duplicated_columns = _find_and_rename_duplicated_columns(adc_df)

        if date_column in duplicated_columns:
            date_column = f"{date_column}_0"

        _convert_date_columns_to_datetime(adc_df, pattern=date_column)

        adc_df.drop_duplicates(inplace=True)

    if pricing_df.index.tz is None:
        pricing_df.index = to_datetime(pricing_df.index, utc=True)

    if multiindex:
        # Check if adc_df wasn't formatted with date as index
        if adc_df.index.name != date_column:
            if adc_df.flags.exception_event["raise_exception"]:
                adc_df = adc_df.pivot(columns=instrument_column)
            else:
                adc_df = adc_df.pivot(index=date_column, columns=instrument_column)

            adc_df = adc_df.swaplevel(axis=1)
            adc_df = adc_df.loc[adc_df.index.dropna()]
            adc_df.dropna(how="all", inplace=True)

        result = pricing_df.join(adc_df, how="outer")
        result.sort_index(axis=1, inplace=True)
    else:
        # Check if adc_df wasn't formatted with date as index
        if adc_df.index.name != date_column:
            if instrument_column in adc_df:
                adc_df.pop(instrument_column)

            if not adc_df.flags.exception_event["raise_exception"]:
                adc_df.set_index(date_column, inplace=True)

        universe = pricing_df.columns.name

        result = pricing_df.merge(
            adc_df, left_index=True, right_index=True, how="outer"
        )

        result.columns.name = universe

    # Remove all rows with all values to NaN
    result.dropna(how="all", inplace=True)

    for i in duplicated_columns:
        _rename_column_n_to_column(i, result, multiindex=multiindex)

    result.index.name = index_name
    return result


def _create_default_pricing_df(
    universe: list,
    fields: Optional[list] = None,
    multiindex: bool = False,
) -> DataFrame:
    if multiindex:
        columns = []
        for u in universe:
            for f in fields:
                columns.append((u, f))

        df = DataFrame(
            columns=MultiIndex.from_tuples(columns), index=[to_datetime(nan)]
        )
    else:
        df = DataFrame(columns=fields, index=[to_datetime(nan)])
        df.columns.name = universe[0]

    return df


def _remove_field_if_not_requested(
    field_name: str, fields_list: list, df: DataFrame, multiindex: bool
) -> None:
    if not df.empty and field_name not in set(i.upper() for i in fields_list):
        level = 1 if multiindex else None
        df.drop(field_name, axis=1, level=level, inplace=True, errors="ignore")
