# coding: utf-8
__version__ = "1.0.0b13"
__all__ = (
    "close_session",
    "content",
    "delivery",
    "eikon",
    "errors",
    "get_config",
    "get_data",
    "get_history",
    "load_config",
    "open_pricing_stream",
    "open_session",
    "OpenState",
    "PricingStream",
    "session",
)

"""
    refinitiv-data is a Python library to access Refinitiv Data Platform with Python.
"""

from . import _configure
from . import _log

from ._config_functions import get_config, load_config
from ._fin_coder_layer.session import open_session, close_session
from ._fin_coder_layer import get_data, get_history
from ._fin_coder_layer.get_stream import PricingStream, open_pricing_stream
from ._open_state import OpenState
from . import session, delivery, content, errors, eikon

import sys as _sys

_logger = _log.root_logger
_logger.debug(f"RD version is {__version__}; Python version is {_sys.version}")

try:
    import pkg_resources as _pkg_resources

    _installed_packages = _pkg_resources.working_set
    _installed_packages = sorted([f"{i.key}=={i.version}" for i in _installed_packages])
    _logger.debug(
        f"Installed packages ({len(_installed_packages)}): "
        f"{','.join(_installed_packages)}"
    )
except Exception as e:
    _logger.debug(f"Cannot log installed packages, {e}")

_logger.debug(f'Read configs: {", ".join(_configure._config_files_paths)}')
