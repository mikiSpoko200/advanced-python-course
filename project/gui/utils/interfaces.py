#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import annotations

"""
This module provides common functionality for GUI objects.
"""

from abc import ABC, abstractmethod
from typing import NamedTuple

from gui.utils.types import RGB


class IDefault:
    """Interface that provides default factory method."""

    @classmethod
    @abstractmethod
    def default(cls) -> IDefault:
        """Return default initialized instance."""
        pass


class ISelect(ABC):
    """Interface that allows GUI objects to react to being selected.

    Selection can be achieved by mouse selected or key selection.
    """

    class FontBackgroundColors(NamedTuple):
        """Convenience data aggregate."""
        font: RGB
        background: RGB

    @abstractmethod
    def selected(self) -> None:
        """selected event handler."""
        pass

    @abstractmethod
    def unselected(self) -> None:
        """Restore default state, called when object is not selecteded."""
        pass


class IPress(ABC):
    """Interface that allows objects to react to being pressed.

    Pressed === obj.rect.iscollidepoint(*pygame.event.MOUSEBUTTONDOWN.pos) = True.
    """

    @abstractmethod
    def pressed(self) -> None:
        """Press event handler.

        pygame.event.MOUSEBUTTONDOWN event to be precise.
        """
        pass

    @abstractmethod
    def released(self) -> None:
        """Restore default state, called when object is not pressed.

        pygame.event.MOUSEBUTTONUP event to be precise.
        """
        pass
