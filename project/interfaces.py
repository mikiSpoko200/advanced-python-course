#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import annotations

# STD lib imports
import abc


class IObserver(abc.ABC):

    @abc.abstractmethod
    def update(self, event: IObservable) -> None:
        pass


class IObservable(abc.ABC):
    """"""

    @abc.abstractmethod
    def attach(self, observer: IObserver) -> None:
        """Attach the observer object to self."""
        pass

    @abc.abstractmethod
    def detach(self, observer: IObserver) -> None:
        """Detach observer object from self's list of event subscribers."""
        pass

    @abc.abstractmethod
    def notify(self):
        """Notify all observers that an event has occurred."""
        pass


class IDefault(abc.ABC):
    """Interface that provides default factory method."""

    @classmethod
    @abc.abstractmethod
    def default(cls) -> IDefault:
        """Return default initialized instance."""
        pass
