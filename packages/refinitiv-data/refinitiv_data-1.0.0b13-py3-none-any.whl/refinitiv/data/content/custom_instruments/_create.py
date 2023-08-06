from typing import Optional, List

from .._content_type import ContentType
from ._data_provider_layer import (
    CustomInstrumentResponse,
)

from ...delivery._data._data_provider import DataProviderLayer
from ...delivery._data._endpoint_data import RequestMethod


def create(
    symbol: str,
    formula: str,
    instrument_name: Optional[str] = None,
    exchange_name: Optional[str] = None,
    currency: Optional[str] = None,
    time_zone: Optional[str] = None,
    holidays: Optional[List[dict]] = None,
    description: Optional[str] = None,
    session=None,
    on_response=None,
) -> CustomInstrumentResponse:
    """
    symbol : str
        Instrument symbol in the format "S)someSymbol.YOURUUID".
    formula : str
        Formula consisting of rics (fields can be specified by comma).
    instrument_name : str, optional
        Human-readable name of the instrument. Maximum of 16 characters.
    exchange_name : str, optional
        4-letter code of the listing exchange.
    currency : str, optional
        3-letter code of the currency of the instrument, e.g. GBP.
    time_zone: str, optional
        Time Series uses an odd custom 3-letter value for time zone IDs, e.g. "LON" for London.
    holidays : list[dict], optional
        List of custom calendar definitions.
    description : str, optional
        Free text field from the user to put any notes or text. Up to 1000 characters.

    Examples
    --------
    >>> from refinitiv.data.content.custom_instruments import create
    >>> response = create(symbol="MyNewInstrument", formula="EUR=*3")
    """
    data_provider_layer = DataProviderLayer(
        data_type=ContentType.CUSTOM_INSTRUMENTS_INSTRUMENTS,
        symbol=symbol,
        formula=formula,
        instrument_name=instrument_name,
        exchange_name=exchange_name,
        currency=currency,
        time_zone=time_zone,
        holidays=holidays,
        description=description,
    )
    response = data_provider_layer.get_data(
        session, on_response, method=RequestMethod.POST
    )
    return response
