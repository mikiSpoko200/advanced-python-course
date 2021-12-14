#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import annotations


import argparse
from enum import Enum, auto
from typing import NamedTuple
from abc import ABC


# consider mapping
# ui upon retreating user configuration can query a db layer for arguments that it should return
# the arguments could be bundled into a data structure? Would that be actually useful?
# It would require UI to be able to create dictionary that could be easily used as **kwargs argument for the
# actual queries. Since the UI got the field names from the Model and once it collects the inputs it
# returns them to the Model we can safely assume that there is not further need for any validation.

# UI asks for arguments that is should prompt user to input, than return collected values.
# Config -> Argument List
# collect user input -> {arg1: value1, arg1: value1 ... }.
# where would validation take place?
# Here we again have a decision to make about splitting responsibilities.
# We could arrange that Model not only provides Argument names but also specifies which values it
# absolutely needs (not null) and which can be skipped - skipped values can be marked with some
# internal value that represents said lack od state.
# The way user would specify it would be left for the UI. This is nice.


# Just a draft
class IUIComponent(ABC):
    """Interface that allows to make classes configurable from UI."""

    # implement all Operation variants
    # implement help communicates

    pass


class ConvertibleEnum(Enum):
    """Enum wrapper class that provides string conversion functionality."""

    @staticmethod
    def variants() -> list[str]:
        """Return all possible enum variants in lowercase string representation."""
        return list(map(str.lower, Operation._member_names_))

    @classmethod
    def from_string(cls, _: str) -> Operation:
        """Create enum instance from appropriate string representation."""
        lookup = { rep: value for rep, value in zip(Operation._member_names_, Operation.operation_list()) }
        return lookup[_]


class Component(ConvertibleEnum):
    """Enumeration of all possible Components that this app can manage.
    
    TODO: in the future think how could this be automated.
        e.g.: UI module would provide some interface that when implemented
            would automatically add new classes to UI along with argument configuration.
    """
    EventType    = auto()
    EventTypes   = auto()
    Event        = auto()
    Events       = auto()
    Participant  = auto()
    Participants = auto()


class Operation(ConvertibleEnum):
    """Enumeration of all possible operations that the app can perform."""
    Display = auto()
    Add     = auto()
    Remove  = auto()
    Update  = auto()


class Config(NamedTuple):
    """Data structure representing app's configuration."""
    operation : Operation
    component : Component


def CLI() -> Config:
    """Command line interface.
    Operations are mutually exclusive.
    First argument determines the Operation that should be performed:
        - add
        - update
        - remove
        - display
    Second argument determines the Component that the Operation affects:
        - event / events
        - participant / participants
        - event-type  / event-types
    -- help flag - action depends on the context of use.
        - If used alone                      -- help for the whole application.
        - If used with Operation             -- help for specific Operation chosen.
        - If used with Operation and Component  -- help for application of chosen Operation for the chosen Component.

    When activated prompts user to input data needed specify the json file with new information.
    
    TODO Ideas for the future:
        --rollback
    """
    parser = argparse.ArgumentParser(
        description="Callendar that allows for scheduling of different types of events.")
    parser.add_argument("operation",
                        choices=Operation.variants,
                        type=Operation.from_string,
                        help="TODO: fixme!")
    parser.add_argument("component", 
                        choices=Component.variants,
                        type=Component.from_string,
                        help="TODO: fixme!")
    namespace = parser.parse_args()
    return Config(
        operation=namespace.operation,
        component=namespace.Component
    )


def main():
    print(Operation.operation_list())


if __name__ == '__main__':
    main()