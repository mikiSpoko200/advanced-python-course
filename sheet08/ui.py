#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import annotations


import argparse
from enum import Enum, auto
from typing import NamedTuple, Type, Optional


def enum_variant_names(_: Type[Enum]) -> list[str]:
    """Return lower-cased enum variant names."""
    return [v.name.lower() for v in _]


class FromStringEnum(Enum):
    """Mixin that allows for Enum instantiation from a string representation."""

    @classmethod
    def from_string(cls, _: str) -> FromStringEnum:
        """Allows for an Enum instantiation from a string representation.

        Input is case-insensitive and should match one of enum's variants.
        """

        for variant in cls:
            if variant.name.lower() == _.lower():
                return variant
        raise ValueError(f"Could not match any enum variant. {_} does not match any variant of {FromStringEnum.name}")


class Component(FromStringEnum):
    """Listing of existing calendar components."""
    Event       = auto()
    Participant = auto()


class Operation(FromStringEnum):
    """Listing of operations that can be performed by a user."""
    Add     = auto()
    Remove  = auto()
    Update  = auto()
    Display = auto()


class Config(NamedTuple):
    """Data structure representing app's configuration."""
    operation: Operation
    component: Component


class ArgumentInfo(NamedTuple):
    name: str
    type: str
    nullable: bool


def prompt_until_valid(valid_cases: list[str], prompt: str) -> str:
    """Prompts user until value specified is one of valid cases."""
    while True:
        _ = input(f"{prompt} {valid_cases}: ")
        if _ in valid_cases:
            return _
        print("Invalid input. Please try again.")


def confirm(prompt: str) -> bool:
    """Prompt for confirmation. Loops until input is either 'Y' (True) or 'n' (False)."""
    _ = prompt_until_valid(['Y', 'n'], prompt)
    return True if _ == 'Y' else False


def get_user_input(args: list[ArgumentInfo]) -> dict[str, Optional[str]]:
    """Prompts for specification of values."""

    def prettify_arg_name(name: str) -> str:
        return name.replace("_", " ").capitalize()

    print("Please input data:")
    data = {}
    for i, arg in enumerate(args, start=1):
        if arg.nullable and not confirm("This parameter is optional. Do you want to SKIP it?"):
            data[arg.name] = None
        else:
            data[arg.name] = input(f"{i}. {prettify_arg_name(arg.name)}\n> ")
    print("You inputted the following data:")
    for index, (name, value) in enumerate(data.items(), start=1):
        print(f"{index}. {prettify_arg_name(name)}: {value}")
    if confirm("Do you confirm your input?"):
        return data
    return get_user_input(args)


def get_configuration() -> Config:
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
        description="Calendar app.")
    parser.add_argument("operation",
                        choices=enum_variant_names(Operation),
                        help="TODO: fixme!")
    parser.add_argument("component", 
                        choices=enum_variant_names(Component),
                        help="TODO: fixme!")
    namespace = parser.parse_args()
    return Config(
        operation=Operation.from_string(namespace.operation),
        component=Component.from_string(namespace.component)
    )
