"""
Logging utilities

Attributes:
    verbosity_level_dict (TYPE): Description
"""

import logging
import sys

verbosity_level_dict = {
    0: logging.CRITICAL,
    1: logging.ERROR,
    2: logging.WARNING,
    3: logging.INFO,
    4: logging.DEBUG,
    5: logging.NOTSET,
}


def verbose_print(
    message: str,
    verbosity: int,
    minimal_verbosity: int,
    newline: str = "\n",
    logger=None,
) -> None:
    """
    Function that decides whether to print a message based on the current verbosity
    and its minimum verbosity. If verbosity is equal or higher than the minimum, then we print.

    Args:
        message (str): message to print.
        verbosity (int): current verbosity level.
        minimal_verbosity (int): threshold verbosity above which to print.
        newline (str, optional): newline character (or set of characters), defaults to ``\n`` but ``\x0d`` (carriage return) might be useful.
        logger: logger object that can handle the logging.
    """

    if logger is None:
        # Log via print statements
        if verbosity >= minimal_verbosity:
            if newline == "\n":
                print(message)
            else:
                print(message, newline, sep="", end="")
            sys.stdout.flush()
    else:
        # Log through logging object
        logger.log(verbosity_level_dict[minimal_verbosity], message)
