# -*- encoding: utf-8 -*-

from __future__ import annotations

# External imports
import pygame.font as font

# Internal imports
import interfaces as general_interfaces
import gui.config.defaults as defaults


class Font(font.Font, general_interfaces.IDefault):
    __doc__ = font.Font.__doc__

    @classmethod
    def default(cls) -> Font:
        return cls(
            defaults.FONT_PATH,
            defaults.FONT_SIZE
        )
