#!/usr/bin/python
# -*- coding: utf-8 -*-


"""This module contains user interface functionality.


"""


__VERSION__ = "0.1.0"
__AUTHOR__ = "Mikołaj Depta"


import argparse
import datetime
import logging
import textwrap as tw
from enum import Enum
from typing import NamedTuple
from termcolor import colored
from sheet06_main import WebsiteState, OperationMode, DEFAULT_DATETIME_FORMAT


DEFAULT_CONFIG_FILE = "layout.json"
DEFAULT_LOG_FILE = "changes.log"
logging.basicConfig(
    filename=DEFAULT_LOG_FILE,
    filemode="a",
    format="%(message)s",
    datefmt=DEFAULT_DATETIME_FORMAT,
    level=logging.DEBUG
)


class ConfigInfo(NamedTuple):
    """Data struct that groups configuration information."""
    operation_mode: OperationMode
    input: str
    run_sync: bool


def command_line_interface() -> ConfigInfo:
    parser = argparse.ArgumentParser(description="Track changes in websites.")
    parser.add_argument(
        "--config-file", "-c",
        default=DEFAULT_CONFIG_FILE,
        help="Allows to specify .json file from which program will attempt read urls.",
    )
    parser.add_argument(
        "--operation-mode", "-o",
        type=OperationMode.from_str,
        help="Choose operation mode for this script:\n"
             " - text | t   -- in this mode program tracks changes to the text contents of the website\n"
             " - layout | l -- track changes to the layout of tha page"
    )
    parser.add_argument(
        "--try-sync",
        help="Runs website fetching section synchronously to showoff the difference between the two."
    )
    namespace = parser.parse_args()
    return ConfigInfo(namespace.operation_mode, namespace.config_file or DEFAULT_CONFIG_FILE, namespace.try_sync)


class Communicates(Enum):
    """Enum representing all possible communicates that program can display to a user.

    The value for each enum option is the communicate formatted as string that should be displayed
    for that specific option.
    """
    OPERATION_MODE = "Operation mode   "
    INPUT          = "Input file       "
    INITIAL        = "New website added"
    CHANGES        = "Changes detected in %d/%d websites"
    ERROR          = "ERROR"  # special case


def log_config(config: ConfigInfo) -> None:
    """Log information about scripts configuration."""
    print(f"Operation Mode      :: {colored(config.operation_mode, color='cyan')}")
    print(f"Input file          :: {colored(config.input, color='cyan')}")


def log_communicate(state: WebsiteState, communicat: str) -> None:
    """Default communicate logging template."""
    print(f"{state.check_timestamp} :: {communicat} :: {state.title}")


def log_initial(state: WebsiteState) -> None:
    """Log information about initial website processing."""
    log_communicate(state, colored(Communicates.INITIAL.value, color="blue"))


def log_error(state: WebsiteState, errmsg: str) -> None:
    """Log information about request error."""
    log_communicate(state, colored(f"{Communicates.ERROR.value} :: {errmsg}", on_color="red"))


def log_changes(state: WebsiteState, changes: list[str]) -> None:
    """Log information about website state change."""
    logging.log(
        logging.DEBUG,
        f"{state.check_timestamp} :: Changes detected in website {state.title}" +
        tw.fill(
            "\n".join(changes),
            width=120,
            initial_indent="\t",
            subsequent_indent="\t")
    )


def log_new(changed: int, total: int) -> None:
    """Log information about website state change."""
    print(f"{datetime.datetime.now().strftime(DEFAULT_DATETIME_FORMAT)} :: "
          f"{colored(Communicates.CHANGES.value % (changed, total), color='yellow')}")
