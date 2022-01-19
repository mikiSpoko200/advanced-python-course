#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import annotations

# region Third party imports.
import pygame.font as font
# endregion

# region Internal imports.
import gui.utils.interfaces as gui_interfaces
import gui.config.defaults as defaults
# endregion


class Font(font.Font, gui_interfaces.IDefault):
    __doc__ = font.Font.__doc__

    @classmethod
    def default(cls) -> Font:
        return cls(
            defaults.FONT_PATH,
            defaults.FONT_SIZE
        )
