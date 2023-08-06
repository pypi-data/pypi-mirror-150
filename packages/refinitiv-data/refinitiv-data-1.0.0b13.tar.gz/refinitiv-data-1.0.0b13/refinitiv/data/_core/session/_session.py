# coding: utf-8

import abc
import asyncio
import itertools
import logging
import traceback
import warnings
from threading import Lock
from typing import Callable, TYPE_CHECKING

from . import http_service
from ._dacs_params import DacsParams
from ._session_cxn_type import SessionCxnType
from .event_code import EventCode
from .tools import is_closed
from ... import _configure as configure, _log as log
from ..._open_state import OpenState
from ..._tools import DEBUG, cached_property, create_repr

if TYPE_CHECKING:
    from ._session_cxn_factory import SessionConnection
    from .http_service import HTTPService
    from ..._configure import _RDPConfig


class Session(abc.ABC):
    _DUMMY_STATUS_CODE = -1
    _id_iterator = itertools.count()
    # Logger for messages outside of particular session instances
    class_logger = log.create_logger("session")

    __acquire_session_id_lock = Lock()

    @property
    def name(self):
        return self._name

    def __init__(
        self,
        app_key,
        on_state=None,
        on_event=None,
        token=None,
        deployed_platform_username=None,
        dacs_position=None,
        dacs_application_id=None,
        name="default",
    ):
        with self.__acquire_session_id_lock:
            self._session_id = next(self._id_iterator)

        session_type = self.type.name.lower()
        logger_name = f"sessions.{session_type}.{name}.{self.session_id}"
        self.class_logger.debug(
            f'Creating session "{logger_name}" based on '
            f'session.{session_type}.Definition("{session_type}.{name}")'
        )

        if app_key is None:
            raise ValueError("app_key value can't be None")

        self._state = OpenState.Closed
        self._status = EventCode.StreamDisconnected
        self._last_event_code = None
        self._last_event_message = None

        self._app_key = app_key
        self._on_event_callback = on_event
        self._on_state_callback = on_state
        self._access_token = token
        self._dacs_params = DacsParams()

        if deployed_platform_username:
            self._dacs_params.deployed_platform_username = deployed_platform_username
        if dacs_position:
            self._dacs_params.dacs_position = dacs_position
        if dacs_application_id:
            self._dacs_params.dacs_application_id = dacs_application_id

        self._logger = log.create_logger(logger_name)
        # redirect log method of this object to the log in logger object
        self.log = self._logger.log
        self.warning = self._logger.warning
        self.error = self._logger.error
        self.debug = self._logger.debug
        self.info = self._logger.info

        self._name = name

        try:
            loop = asyncio.get_event_loop()
            msg = f"to current"
        except RuntimeError:
            loop = asyncio.new_event_loop()
            msg = f"with a new"

        self.debug(
            "Session loop was set {} event loop {}, id {}".format(msg, loop, id(loop))
        )
        self._loop = loop

        self.__lock_callback = Lock()

        self._config: "_RDPConfig" = configure.get_config().copy()

        # override session api config with session's specific api parameters
        specific_api_path = f"sessions.{session_type}.{name}.apis"
        specific_api = self._config.get(specific_api_path)
        if specific_api:
            self._config.set_param("apis", specific_api)

        self._config.on(configure.ConfigEvent.UPDATE, self._on_config_updated)
        # rssl/rwf stream ids always starts with 5
        self._omm_stream_counter = itertools.count(5)

    @cached_property
    def _http_service(self) -> "HTTPService":
        return http_service.get_service(self)

    @cached_property
    def _connection(self) -> "SessionConnection":
        from ._session_cxn_factory import get_session_cxn

        cxn_type = self._get_session_cxn_type()
        cxn = get_session_cxn(cxn_type, self)
        self.debug(f"Created session connection {cxn_type}")
        return cxn

    @abc.abstractmethod
    def _get_session_cxn_type(self) -> SessionCxnType:
        pass

    def on_state(self, callback: Callable) -> None:
        """
        On state callback

        Parameters
        ----------
        callback: Callable
            Callback function or method

        Raises
        ----------
        Exception
            If user provided invalid object type
        """
        if not callable(callback):
            raise TypeError("Please provide callable object")

        self._on_state_callback = callback

    def get_on_state_callback(self) -> Callable:
        return self._on_state_callback

    def on_event(self, callback: Callable) -> None:
        """
        On event callback

        Parameters
        ----------
        callback: Callable
            Callback function or method

        Raises
        ----------
        Exception
            If user provided invalid object type
        """
        if not callable(callback):
            raise TypeError("Please provide callable object")

        self._on_event_callback = callback

    def get_on_event_callback(self) -> Callable:
        return self._on_event_callback

    def __repr__(self):
        return create_repr(
            self,
            middle_path="session",
            content=f"{{name='{self.name}'}}",
        )

    def _on_config_updated(self):
        log_level = log.read_log_level_config()

        if log_level != self.get_log_level():
            self.set_log_level(log_level)

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self._loop

    @property
    def config(self) -> "_RDPConfig":
        return self._config

    @property
    def open_state(self):
        """
        Returns the session state.
        """
        return self._state

    def get_last_event_code(self):
        """
        Returns the last session event code.
        """
        return self._last_event_code

    def get_last_event_message(self):
        """
        Returns the last event message.
        """
        return self._last_event_message

    @property
    def app_key(self):
        """
        Returns the application id.
        """
        return self._app_key

    @app_key.setter
    def app_key(self, app_key):
        """
        Set the application key.
        """
        from ...eikon._tools import is_string_type

        if app_key is None:
            return
        if not is_string_type(app_key):
            raise AttributeError("application key must be a string")

        self._app_key = app_key

    def update_access_token(self, access_token):
        DEBUG and self.debug(
            f"Session.update_access_token(access_token='{access_token}'"
        )
        self._access_token = access_token

        from ...delivery._stream import stream_cxn_cache

        if stream_cxn_cache.has_cxns(self):
            cxns_by_session = stream_cxn_cache.get_cxns(self)
            for cxn in cxns_by_session:
                cxn.send_login_message()

    @property
    def session_id(self):
        return self._session_id

    def logger(self) -> logging.Logger:
        return self._logger

    def _get_rdp_url_root(self) -> str:
        return ""

    @cached_property
    def http_request_timeout_secs(self):
        return self._http_service.request_timeout_secs

    ############################################################
    #   reconnection configuration

    @property
    def stream_auto_reconnection(self):
        return True

    @property
    def server_mode(self):
        return False

    @abc.abstractmethod
    def get_omm_login_message(self):
        """return the login message for OMM 'key' section"""
        pass

    @abc.abstractmethod
    def get_rdp_login_message(self, stream_id):
        """return the login message for RDP protocol"""
        pass

    ######################################
    # methods to manage log              #
    ######################################
    def set_log_level(self, log_level: [int, str]) -> None:
        """
        Set the log level.
        By default, logs are disabled.

        Parameters
        ----------
        log_level : int, str
            Possible values from logging module :
            [CRITICAL, FATAL, ERROR, WARNING, WARN, INFO, DEBUG, NOTSET]
        """
        log_level = log.convert_log_level(log_level)
        self._logger.setLevel(log_level)

        if DEBUG:
            # Enable debugging
            self._loop.set_debug(True)

            # Make the threshold for "slow" tasks very very small for
            # illustration. The default is 0.1, or 100 milliseconds.
            self._loop.slow_callback_duration = 0.001

            # Report all mistakes managing asynchronous resources.
            warnings.simplefilter("always", ResourceWarning)

    def get_log_level(self):
        """
        Returns the log level
        """
        return self._logger.level

    def trace(self, message):
        self._logger.log(log.TRACE, message)

    ######################################
    # methods to open and close session  #
    ######################################
    def open(self) -> OpenState:
        """open session

        do an initialization config file, and http session if it's necessary.

        Returns
        -------
        OpenState
            the current state of this session.
        """
        if self._state in [OpenState.Pending, OpenState.Open]:
            return self._state

        self.debug(f"Open session")

        self._on_state(OpenState.Pending, "Opening in progress")
        self._config.on(configure.ConfigEvent.UPDATE, self._on_config_updated)
        self._http_service.open()
        is_opened = self._connection.open()

        if is_opened:
            self._on_state(OpenState.Open, "Session is opened.")
        else:
            self.close()
            self._on_state(OpenState.Closed, "Session is closed")

        self.debug(f"Opened session")
        return self._state

    async def open_async(self):
        """open session

        do an initialization config file, and http session if it's necessary.

        Returns
        -------
        OpenState
            the current state of this session.
        """
        if self._state in [OpenState.Pending, OpenState.Open]:
            return self._state

        self.debug(f"Open async session")

        self._on_state(OpenState.Pending, "Opening in progress")
        self._config.on(configure.ConfigEvent.UPDATE, self._on_config_updated)
        await self._http_service.open_async()
        is_opened = self._connection.open()

        if is_opened:
            self._on_state(OpenState.Open, "Session is opened.")
        else:
            await self.close_async()
            self._on_state(OpenState.Closed, "Session is closed")

        self.debug(f"Opened async session")
        return self._state

    def close(self) -> OpenState:
        """
        Close platform/desktop session

        Returns
        -------
        State
        """
        if is_closed(self):
            return self._state

        self.debug(f"Close session")

        from ...delivery._stream import stream_cxn_cache

        stream_cxn_cache.close_cxns(self)
        self._http_service.close()
        self._connection.close()

        if DEBUG:
            import time
            from ...delivery._stream import stream_cxn_cache
            import threading

            time.sleep(5)
            s = "\n\t".join([str(t) for t in threading.enumerate()])
            self.debug(f"Threads:\n" f"\t{s}")

            if stream_cxn_cache.has_cxns(self):
                raise AssertionError(
                    f"Not all cxns are closed (session={self},\n"
                    f"cxns={stream_cxn_cache.get_cxns(self)})"
                )

        self._config.remove_listener(
            configure.ConfigEvent.UPDATE, self._on_config_updated
        )
        self._on_state(OpenState.Closed, "Session is closed")
        self.debug(f"Closed session")
        return self._state

    async def close_async(self) -> OpenState:
        """
        Close platform/desktop session

        Returns
        -------
        State
        """
        if is_closed(self):
            return self._state

        self.debug(f"Close async session")

        from ...delivery._stream import stream_cxn_cache

        stream_cxn_cache.close_cxns(self)
        await self._http_service.close_async()
        self._connection.close()

        if DEBUG:
            from ...delivery._stream import stream_cxn_cache
            import threading

            await asyncio.sleep(5)
            s = "\n\t".join([str(t) for t in threading.enumerate()])
            self.debug(f"Threads:\n\t{s}")

            if stream_cxn_cache.has_cxns(self):
                raise AssertionError(
                    f"Not all cxns are closed (session={self},\n"
                    f"cxns={stream_cxn_cache.get_cxns(self)})"
                )

        self._config.remove_listener(
            configure.ConfigEvent.UPDATE, self._on_config_updated
        )
        self._on_state(OpenState.Closed, "Session is closed")
        self.debug(f"Closed async session")
        return self._state

    ##########################################################
    # methods for session callbacks from streaming session   #
    ##########################################################

    def _on_state(self, state_code, state_text):
        with self.__lock_callback:
            if isinstance(state_code, OpenState):
                self._state = state_code
                if self._on_state_callback is not None:
                    try:
                        self._on_state_callback(self, state_code, state_text)
                    except Exception as e:
                        self.error(
                            f"on_state user function on session {self.session_id} raised error {e}"
                        )

    def _on_event(
        self,
        event_code,
        event_msg,
        streaming_session_id=None,
        stream_connection_name=None,
    ):
        self.debug(
            f"Session._on_event("
            f"event_code={event_code}, "
            f"event_msg={event_msg}, "
            f"streaming_session_id={streaming_session_id}, "
            f"stream_connection_name={stream_connection_name})"
        )
        with self.__lock_callback:
            #   check the on_event trigger from some of the stream connection or not?
            #   not stream connection on_event, just call the on_event callback
            #   call the callback function
            if self._on_event_callback:
                try:
                    self._on_event_callback(self, event_code, event_msg)
                except Exception as e:
                    self.error(
                        f"on_event user function on session {self.session_id} raised error {e}"
                    )

    ##############################################
    # methods for status reporting               #
    ##############################################
    @staticmethod
    def _report_session_status(self, session, session_status, event_msg):
        _callback = self._get_status_delegate(session_status)
        if _callback is not None:
            json_msg = self._define_results(session_status)[Session.CONTENT] = event_msg
            _callback(session, json_msg)

    def report_session_status(self, session, event_code, event_msg):
        # Report the session status event defined with the eventMsg to the appropriate delegate
        self._last_event_code = event_code
        self._last_event_message = event_msg
        _callback = self._get_status_delegate(event_code)
        if _callback is not None:
            try:
                _callback(session, event_code, event_msg)
            except Exception as e:
                self.error(
                    f"{self.__name__} on_event or on_state"
                    f" callback raised exception: {e!r}"
                )
                self.debug(f"{traceback.format_exc()}")

    def _get_status_delegate(self, event_code):
        _cb = None

        if event_code in [
            EventCode.SessionAuthenticationSuccess,
            EventCode.SessionAuthenticationFailed,
        ]:
            _cb = self._on_state_callback
        elif event_code not in [
            EventCode.DataRequestOk,
            EventCode.StreamConnecting,
            EventCode.StreamConnected,
            EventCode.StreamDisconnected,
        ]:
            _cb = self._on_event_callback
        return _cb

    async def http_request_async(
        self,
        url: str,
        method=None,
        headers=None,
        data=None,
        params=None,
        json=None,
        closure=None,
        **kwargs,
    ):
        return await self._http_service.request_async(
            url=url,
            method=method,
            headers=headers,
            data=data,
            params=params,
            json=json,
            closure=closure,
            **kwargs,
        )

    def http_request(
        self,
        url: str,
        method=None,
        headers=None,
        data=None,
        params=None,
        json=None,
        closure=None,
        **kwargs,
    ):
        response = self._http_service.request(
            url=url,
            method=method,
            headers=headers,
            data=data,
            params=params,
            json=json,
            closure=closure,
            **kwargs,
        )
        return response
