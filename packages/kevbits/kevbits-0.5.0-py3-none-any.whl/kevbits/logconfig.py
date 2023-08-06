"""
Configure python logging.
"""

# Note: see into eventlet related issue:
# 'logging, logging.config' modules use 'threading' module internally.
# Details: https://bugs.launchpad.net/keystone/+bug/1420788

from __future__ import print_function, division, absolute_import

import logging
import logging.config

import sys
import time
import re
import os
from typing import Any

from kevbits.misc import map_dict_deep


class GmTimeFormatter(logging.Formatter):
    "Use UTC timestamp for log messages."

    def __init__(self, fmt=None, datefmt=None):
        super().__init__(fmt=fmt, datefmt=datefmt)
        self.converter = time.gmtime


def gmtime_formatter_factory(fmt, datefmt):
    "Factory function which is referred to from .yaml file."
    return GmTimeFormatter(fmt, datefmt)


rx_expandvars = re.compile(r"(.*?)(\${.*?})(.*)")


def expandvars(string: str) -> str:
    "Expand env. variables when they are given in the form ${name} only."
    m = rx_expandvars.match(string)
    if m is None:
        return string
    left, curr, right = m.groups()
    value = os.environ.get(
        curr[2:-1], curr
    )  # left the text unchanged if no such variable
    return left + value + expandvars(right)


def from_dict(config: dict[str, Any]):
    "Configure logging from dict."
    # Configure logging. We don't use logfiles when running under pytest (pytest.watch)
    # as this may interfer with normal application execution taking place at the same
    # moment. (On every testing iteration pytest imports this application module.
    # Without logfiles disabling this import will lead to logging reinitialization
    # and possible logfiles changes.
    if hasattr(sys, "_called_from_test"):
        logging.basicConfig()
    else:
        # expand environment variables
        config = map_dict_deep(
            config, lambda v: v if not isinstance(v, str) else expandvars(v)
        )
        logging.config.dictConfig(config)

    logging.captureWarnings(
        True
    )  # Capture warnings issued by the built-in 'warnings' module

    # Add standard level aliases (based on forte/log/main.py)
    for l, a in [
        (logging.DEBUG, "D"),
        (logging.INFO, "."),
        (logging.WARNING, "w"),
        (logging.ERROR, "E"),
        (logging.CRITICAL, "!"),
    ]:
        logging.addLevelName(l, a)

    # Return logger so that the user of this module does not need to import the 'logging' module.
    return logging.getLogger()
