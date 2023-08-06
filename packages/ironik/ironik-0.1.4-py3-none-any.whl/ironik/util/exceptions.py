"""

:author: Jonathan Decker
"""

import functools
import logging

from rich import print

logger = logging.getLogger("logger")


class IronikFatalError(Exception):
    """ """

    def __init__(self, message):
        self.message = "Ironik has stopped due to the following error: " + message
        super().__init__(self.message)
        logger.warning(self.message)


class IronikPassingError(Exception):
    """ """

    def __init__(self, message):
        self.message = "The following error occurred has occurred, execution will continue: " + message
        super().__init__(self.message)
        logger.warning(self.message)


def passing_error_handler(func):
    @functools.wraps(func)
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IronikPassingError as e:
            logger.debug(f"Passing error occurred in {func.__name__}")
            print(e)

    return inner_function
