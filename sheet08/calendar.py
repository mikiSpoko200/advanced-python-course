#!/usr/bin/python
# -*- encoding: utf-8 -*-


"""A Calendar app that allows for planing of the events with numerous participants.

Command Line User Interface provides means to add, remove, update and 
display currently sotred events, participants and pieces of information.

VERSION 0.0.1:
    add, remove, update, display functionality for different Events, Participants and EventTypes.
    when performing any of the operations all fields must be specified.

TODO: 
    - add proper error handling.
    - add sorting functionality for the CLI. e.g. Display Event On Monday Where Host is "xxx" or/and and so on.
"""


__VERSION__ = "0.0.1"
__AUTHOR__ = "Mikołaj Depta"


# import db
from dataclasses import dataclass
from enum import Enum, auto
from abc import ABC, abstractmethod
from ui import Config, Operation, Component 


class IComponent(ABC):
    """Interface that defines minimal functionality of calendar component.
    
    TODO:
        - in future add error handling via OperationStatus enum.
    """

    @abstractmethod
    def add(self, **kwargs) -> None:
        """Add component instance to the calendar."""
        pass

    @abstractmethod
    def remove(self, **kwargs) -> None:
        """Remove component instance from the calendar."""
        pass

    @abstractmethod
    def update(self, **kwargs) -> None:
        """Update component instance in the calendar."""
        pass

    @abstractmethod
    def display(self, **kwargs) -> None:
        """Display component instance information."""
        pass


