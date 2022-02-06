# -*- encoding: utf-8 -*-

from __future__ import annotations

"""
This module provides common functionality for GUI objects.
"""

# STD lib imports
import abc
import enum
import typing

# Internal imports
from gui.types import RGB


class ISelect(abc.ABC):
    """Interface that allows GUI objects to react to being selected.

    Selection can be achieved by mouse selected or key selection.
    """

    class FontBackgroundColors(typing.NamedTuple):
        """Convenience data aggregate."""
        font: RGB
        background: RGB

    @abc.abstractmethod
    def selected(self) -> None:
        """selected event handler."""
        pass

    @abc.abstractmethod
    def unselected(self) -> None:
        """Restore default state, called when object is not selecteded."""
        pass


class IPress(abc.ABC):
    """Interface that allows objects to react to being pressed.

    Pressed === obj.rect.iscollidepoint(*pygame.event.MOUSEBUTTONDOWN.pos) = True.
    """

    @abc.abstractmethod
    def pressed(self) -> None:
        """Press event handler.

        pygame.event.MOUSEBUTTONDOWN event to be precise.
        """
        pass

    @abc.abstractmethod
    def released(self) -> None:
        """Restore default state, called when object is not pressed.

        pygame.event.MOUSEBUTTONUP event to be precise.
        """
        pass


class IDisabled(abc.ABC):
    """Interface that allows objects to become disabled and unresponsive.

    This can be used to notify user that current
    """

    class State(enum.Enum):
        DISABLED = enum.auto()
        ENABLED  = enum.auto()

    @property
    @abc.abstractmethod
    def is_disabled(self) -> bool:
        """Specify is object is currently disabled."""
        pass

    @abc.abstractmethod
    def disable(self) -> None:
        """Disable responsiveness."""
        pass

    @abc.abstractmethod
    def enable(self) -> None:
        """Enable responsiveness"""
        pass
