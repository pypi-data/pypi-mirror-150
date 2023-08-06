from typing import Optional, List

from ._data_provider import CustomInstsData, is_instrument_id, get_correct_symbol
from ._stream import CustomInstrumentsStream
from ...delivery._data._data_provider import DataProviderLayer, Response
from ...delivery._data._endpoint_data import RequestMethod


class CustomInstrumentResponse(Response):
    data: CustomInstsData


class CustomInstrumentDataProviderLayer:
    def __init__(self, *args, **kwargs):
        self._data_provider_layer = DataProviderLayer(*args, **kwargs)

    def get_details(self, session=None, on_response=None) -> CustomInstrumentResponse:
        response = self._data_provider_layer.get_data(
            session, on_response, method=RequestMethod.GET
        )
        return response

    def update(
        self,
        symbol: Optional[str] = None,
        formula: Optional[str] = None,
        instrument_name: Optional[str] = None,
        exchange_name: Optional[str] = None,
        currency: Optional[str] = None,
        time_zone: Optional[str] = None,
        holidays: Optional[List[dict]] = None,
        description: Optional[str] = None,
        session=None,
        on_response=None,
    ) -> CustomInstrumentResponse:
        response = self.get_details(session=session, on_response=on_response)
        instrument_details = response.data.raw
        if symbol is None:
            symbol = instrument_details.get("symbol")
        if formula is None:
            formula = instrument_details.get("formula")
        if instrument_name is None:
            instrument_name = instrument_details.get("instrumentName")
        if exchange_name is None:
            exchange_name = instrument_details.get("exchangeName")
        if currency is None:
            currency = instrument_details.get("currency")
        if time_zone is None:
            time_zone = instrument_details.get("timeZone")
        if holidays is None:
            holidays = instrument_details.get("holidays")
        if description is None:
            description = instrument_details.get("description")

        response = self._data_provider_layer.get_data(
            session,
            on_response,
            method=RequestMethod.PUT,
            symbol=symbol,
            formula=formula,
            instrument_name=instrument_name,
            exchange_name=exchange_name,
            currency=currency,
            time_zone=time_zone,
            holidays=holidays,
            description=description,
        )
        return response

    def delete(
        self,
        session=None,
        on_response=None,
    ) -> Response:
        return self._data_provider_layer.get_data(
            session, on_response, method=RequestMethod.DELETE
        )

    def get_stream(self, session=None) -> CustomInstrumentsStream:
        universe = self._data_provider_layer._kwargs.get("universe")
        if is_instrument_id.match(universe):
            instrument_response = self.get_details()
            name = instrument_response.data.raw.get("symbol")
        else:
            name = get_correct_symbol(universe, session)
        stream = CustomInstrumentsStream(name, session=session)
        return stream
