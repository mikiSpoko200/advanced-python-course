#!/usr/bin/python
# -*- encoding: utf-8 -*-


from __future__ import annotations

from abc import ABC, abstractmethod

from datetime import datetime
from typing import Optional, Type

import db
import ui
from ui import ArgumentInfo

"""A Calendar app that allows for planing of the events with numerous participants.

Command Line User Interface provides means to add, remove, update and 
display currently stored events, participants and pieces of information.

VERSION 0.0.3:
    add, remove, update, display functionality for different Events, Participants and EventTypes.
    when performing any of the operations all fields must be specified.

TODO: 
    - add proper error handling.
    - add sorting functionality for the CLI. e.g. Display Event On Monday Where Host is "xxx" or/and and so on.
"""

__VERSION__ = "0.0.1"
__AUTHOR__ = "Mikołaj Depta"


# TODO: consider moving this into the db.py module.
def model_arg_info(component: Type[IComponent]) -> list[ArgumentInfo]:
    """Return list of values needed to instantiate a Component based on underlying models fields."""
    arg_info = list()
    for field in component.model._meta.sorted_fields:
        if field.field_type not in ('AUTO',):
            arg_info.append(ArgumentInfo(field.name, field.field_type, field.null))
    return arg_info


class IUIComponent(ABC):
    """Interface that allows components to be instanced from UI."""

    @classmethod
    @abstractmethod
    def from_ui(cls, values: dict[str, str]) -> IComponent:
        """Create instance from arguments gathered from UI."""
        pass


class IComponent(ABC):
    """Common functionality for a component."""

    model: db.Model  # reference to a backing store.

    @property
    @abstractmethod
    def query_args(self) -> dict[db.pw.Field: str
                                              | datetime
                                              | Participant
                                              | EventType
                                              | Optional[str]
                                              | list[Participant]]:
        """Return dict of Filed to value needed for queries."""
        pass


class ComponentOperationHandler:
    """Handler class that performs operations on different components.

    Combines the functionality of a calendar component and simplifies the class interface.
    """

    def __init__(self, component: IComponent):
        self.component = component

    def add(self) -> None:
        """Add new an instance of component."""
        status = self.component.model.insert(self.component.query_args).execute()
        print(f"Successfully added {status} item(s).")

    def update(self, **kwargs) -> None:
        """Update an instance of existing component."""
        status = self.component.model.update(self.component.query_args).execute()
        print(f"Successfully updated {status} item(s).")

    def delete(self) -> None:
        """Delete an instance of existing component."""
        status = self.component.model.delete().where(self.component.query_args).execute()
        print(f"Successfully deleted {status} item(s).")

    def display(self) -> None:
        """Display information about a specific component."""
        print(f"Currently stored {self.component.__class__.__name__}s:")
        query = self.component.model.select().execute()
        for result in query:
            print(result)


#
# Adapter for User Interface and DataBase layers.
#


class Event(IComponent, IUIComponent):
    """Adapter for Event model."""
    model = db.Event

    def __init__(self, start_time: datetime, end_time: datetime, description: Optional[str],
                 participants: list[Participant], event_type: EventType, host: Participant) -> None:
        self.participants = participants
        self.host = host
        self._query_args = {
            self.model.start_time: start_time,
            self.model.end_time: end_time,
            self.model.description: description,
            self.model.event_type: event_type
        }

    @classmethod
    def from_ui(cls, values: dict[str, str]) -> IComponent:
        raise NotImplementedError("Add argument parsing?")

    def query_args(self) -> dict[db.pw.Field: str
                                              | datetime
                                              | Participant
                                              | EventType
                                              | Optional[str]
                                              | list[Participant]]:
        return self._query_args


class Participant(IComponent, IUIComponent):
    """Adapter for Participant model."""

    model = db.Participant

    def __init__(self, name: str, surname: str, email: str) -> None:
        self._query_args = {
            self.model.name: name, self.model.surname: surname, self.model.email: email
        }

    @classmethod
    def from_ui(cls, values: dict[str, str]) -> IComponent:
        return cls(**values)

    @property
    def query_args(self) -> dict[db.pw.Field: str
                                              | datetime
                                              | Participant
                                              | EventType
                                              | Optional[str]
                                              | list[Participant]]:
        return self._query_args


class EventType(IComponent, IUIComponent):
    """Adapter for an EventType model."""

    model = db.EventType

    def __init__(self, name: str) -> None:
        self._query_args = {self.model.name: name}

    @classmethod
    def from_ui(cls, values: dict[str, str]) -> IComponent:
        return cls(**values)

    @property
    def query_args(self) -> dict[db.pw.Field: str
                                              | datetime
                                              | Participant
                                              | EventType
                                              | Optional[str]
                                              | list[Participant]]:
        return self._query_args


def main():
    db.init()
    print(model_arg_info(EventType))
    handler = ComponentOperationHandler(
        EventType.from_ui(
            ui.get_user_input(
                model_arg_info(EventType))))
    handler.display()


if __name__ == '__main__':
    main()
