#!/usr/bin/python
# -*- coding: utf-8 -*-


"""This module contains user interface functionality.


"""


__VERSION__ = "0.1.0"
__AUTHOR__ = "Mikołaj Depta"


import os
import textwrap as tw
from enum import Enum
from termcolor import colored
from main import WebsiteState, ConfigInfo


class Communicates(Enum):
    """Enum representing all possible communicates that program can display to a user.

    The value for each enum option is the communicate formatted as string that should be displayed
    for that specific option.
    """
    OPERATION_MODE = "Operation mode     "
    INPUT          = "Input file         "
    UPDATE         = "New website added  "
    NO_UPDATE      = "Changes detected   "
    ERROR          = "No changes detected"
    INITIAL        = "ERROR"  # special case


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


def log_change(state: WebsiteState, changes: list[str]) -> None:
    """Log information about website state change."""
    log_communicate(state, colored(Communicates.UPDATE.value, color="green"))
    for change in changes:
        if change[0] == "-" and change[:3] != "---":
            change = colored(change, color="red")
        if change[0] == "+" and change[:3] != "+++":
            change = colored(change, color="green")
        if change[:2] == "@@":
            change = colored(change, color="blue")
        print(tw.fill(
            change,
            width=os.get_terminal_size().columns - 10,
            initial_indent="\t",
            subsequent_indent="\t")
        )


def log_no_change(state: WebsiteState) -> None:
    """Log information about website state change."""
    log_communicate(state, colored(Communicates.NO_UPDATE.value, color="yellow"))
