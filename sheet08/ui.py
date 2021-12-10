#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import annotations


import argparse
from enum import Enum, auto
from typing import NamedTuple
from main import Event, Participant, ParticipantEvent


class Operation(Enum):
    """Enumeration of all possible operations that the app can perform."""
    Display = auto()
    Add     = auto()
    Remove  = auto()
    Update  = auto()

    @staticmethod
    def operation_list() -> list[str]:
        return list(map(str.lower, Operation._member_names_))

    @classmethod
    def from_string(cls, _: str) -> Operation:
        return match

class Config(NamedTuple):
    operation: Operation


def CLI() -> Config:
    """Command line interface.
    First argument determines the Operation that should be performed:
        - add
        - update
        - remove
        - display
    Second argument determines the Object that the Operation affects:
        - event / events
        - participant / participants
    -- help flag - action depends on the context of use.
        - If used alone                      -- help for the whole application.
        - If used with Operation             -- help for specific Operation chosen.
        - If used with Operation and Object  -- help for application of chosen Operation for the chosen Object.

    When activated prompts user to input data needed specify the json file with new information.

    TODO Ideas for the future:
        --rollback
    """
    parser = argparse.ArgumentParser(description="Interactive calendar.")
    parser.add_argument("Operation",
                        choices=Operation.operation_list(),
                        type=lambda: None,
                        help="opis dla positional")
    parser.add_argument("--optional-mode", help="opis dla optional", action="store_true")

    namespace = parser.parse_args()


def main():
    print(Operation.operation_list())


if __name__ == '__main__':
    main()