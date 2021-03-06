"""Logger module.

When first calling logger() it will call the setup() function.
"""

import logging
import sys

from sicg2 import __version__


FMT = '%(asctime)s    %(module)s    %(levelname)s    %(message)s'
LOGGER_NAME = 'sicglog'


def logger(debug=False):
    """Logger.

    Args:
        debug (bool): whether to set log level to debug or not
    """
    log = logging.getLogger(name=LOGGER_NAME)
    if not len(log.handlers):
        # handlers have not yet been added
        setup(log, debug=debug)
    return log


def setup(log, debug=True):
    """Configure the logger

    Args:
        log (logging.logger): logger to configure
        debug (bool): whether to set log level to debug or not
    """
    console_handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter(FMT)
    console_handler.setFormatter(formatter)
    if debug:
        console_handler.setLevel(logging.DEBUG)
        log.addHandler(console_handler)
        log.setLevel(logging.DEBUG)
    else:
        console_handler.setLevel(logging.INFO)
        log.addHandler(console_handler)
        log.setLevel(logging.INFO)
    log.debug('Setting up logger for SICG2 v%s', __version__)
