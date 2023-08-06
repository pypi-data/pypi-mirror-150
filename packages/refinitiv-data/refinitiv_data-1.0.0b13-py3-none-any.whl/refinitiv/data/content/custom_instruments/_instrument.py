import datetime
from typing import Union, Optional

from .._intervals import Intervals
from ..custom_instruments._stream import CustomInstrumentsStream


class Instrument:
    def __init__(
        self,
        data,
    ):
        self._data = data

    def get_history_events(
        self,
        start: Optional[Union[str, datetime.datetime]] = None,
        end: Optional[Union[str, datetime.datetime]] = None,
        count: Optional[int] = None,
    ):
        from . import events

        response = events.Definition(
            universe=self.id, start=start, end=end, count=count
        ).get_data()
        return response

    def get_history_summaries(
        self,
        interval: Union[str, Intervals] = None,
        start: Optional[Union[str, datetime.datetime]] = None,
        end: Optional[Union[str, datetime.datetime]] = None,
        count: Optional[int] = None,
    ):
        from . import summaries

        response = summaries.Definition(
            universe=self.id, interval=interval, start=start, end=end, count=count
        ).get_data()
        return response

    @property
    def symbol(self):
        return self._data.get("symbol")

    @property
    def formula(self):
        return self._data.get("formula")

    @property
    def instrument_name(self):
        return self._data.get("instrumentName")

    @property
    def exchange_name(self):
        return self._data.get("exchangeName")

    @property
    def currency(self):
        return self._data.get("currency")

    @property
    def time_zone(self):
        return self._data.get("timeZone")

    @property
    def holidays(self):
        return self._data.get("holidays")

    @property
    def description(self):
        return self._data.get("description")

    @property
    def id(self):
        return self._data.get("id")

    @property
    def owner(self):
        return self._data.get("owner")

    def get_stream(self, session=None):
        stream = CustomInstrumentsStream(self.symbol, session=session)
        return stream
