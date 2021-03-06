# -*- encoding: utf-8 -*-

from __future__ import annotations

"""
This module contains buttons jo.
"""

# OPTIMIZATION: Make sure to use DirtySprite, or otherwise minimize unnecessary drawing.

# STD lib imports
import functools
from typing import Optional

# External imports
import pygame.sprite
import pygame.surface as surf

# Internal imports
import interfaces as general_interfaces
import gui.interfaces as gui_interfaces
import gui.config.defaults as defaults
from gui.types import RGBA, Callback, Position
from gui.controls.fonts import Font


class ButtonColorScheme(general_interfaces.IDefault):
    """Struct that contains button color scheme information.

    Scheme consist of 3 sets of foreground, background color pairs which correspond to the button's 3 states:
        - default - not selected and not pressed
        - select  - select not pressed
        - pressed - pressed
    """

    def __init__(self,
                 default_foreground: RGBA,
                 default_background: RGBA,
                 select_foreground: RGBA,
                 select_background: RGBA,
                 press_foreground: RGBA,
                 press_background: RGBA) -> None:
        self.default_foreground = default_foreground
        self.default_background = default_background
        self.select_foreground = select_foreground
        self.select_background = select_background
        self.press_foreground = press_foreground
        self.press_background = press_background

    @classmethod
    def default(cls) -> ButtonColorScheme:
        return cls(
            defaults.Button.DEFAULT_FOREGROUND_COLOR.value,
            defaults.Button.DEFAULT_BACKGROUND_COLOR.value,
            defaults.Button.SELECT_FOREGROUND_COLOR.value,
            defaults.Button.SELECT_BACKGROUND_COLOR.value,
            defaults.Button.PRESS_FOREGROUND_COLOR.value,
            defaults.Button.PRESS_BACKGROUND_COLOR.value
        )


# aesthetic: consider adding padding between braces and label.
# NOTE: buttons brace border counts to the selected area.
class Button(pygame.sprite.DirtySprite, gui_interfaces.ISelect, gui_interfaces.IPress, gui_interfaces.IDisabled):
    """Simple button.

    Button with much simpler styling options based on the ones found Cataclysm Dark Days Ahead
    [<content>] and only the <content> gets highlighted.
    """

    def __init__(self,
                 label: str,
                 callback: Callback,
                 position: Position,
                 font_object: Font = None,
                 color_scheme: Optional[ButtonColorScheme] = None) -> None:
        super().__init__()
        self._disabled = False
        self.label = label
        self.callback = callback
        self.is_pressed = False
        self.__font_object = font_object or Font.default()
        self.__color_scheme = color_scheme or ButtonColorScheme.default()
        self.__current_color_scheme = self.__color_scheme.default_foreground, self.__color_scheme.default_background

        # other parts of the button.
        self.__open_brace = self.__font_object.render("[", defaults.USE_AA, *self.__current_color_scheme)
        self.__close_brace = self.__font_object.render("]", defaults.USE_AA, *self.__current_color_scheme)
        self.__render_offset = self.__open_brace.get_width()

        # render initial label, since text won't ever change we can store dimensions of the render surface.
        label_surface = self.__font_object.render(self.label, defaults.USE_AA, *self.__current_color_scheme)
        sizes = [_.get_rect().size for _ in (self.__open_brace, label_surface, self.__close_brace)]
        width = functools.reduce(lambda acc, size: acc + size[0], sizes, 0)
        _, height = max(sizes, key=lambda size: size[1])

        self.image = surf.Surface((width, height))
        self.image.blit(self.__open_brace, (0, 0))
        self.image.blit(self.__close_brace, (width - self.__close_brace.get_width(), 0))

        # used for collision detection.
        self.rect = pygame.rect.Rect(position, (width, height))

    # region Base class overrides
    def update(self) -> None:
        label_surface = self.__font_object.render(self.label, defaults.USE_AA, *self.__current_color_scheme)
        self.image.blit(label_surface, (self.__render_offset, 0))
    # endregion

    # Interface implementations
    # region ISelect
    def selected(self) -> None:
        self.dirty = True
        self.__current_color_scheme = self.__color_scheme.select_foreground, self.__color_scheme.select_background

    def unselected(self) -> None:
        self.dirty = True
        self.__current_color_scheme = self.__color_scheme.default_foreground, self.__color_scheme.default_background

    # endregion

    # region IPress
    def pressed(self) -> None:
        print("pressed")
        self.dirty = True
        self.is_pressed = True
        self.callback()
        self.__current_color_scheme = self.__color_scheme.press_foreground, self.__color_scheme.press_background

    def released(self) -> None:
        self.dirty = True
        self.is_pressed = False
        self.selected()
    # endregion

    # region IDisabled
    @property
    def is_disabled(self) -> bool:
        return self._disabled

    def disable(self) -> None:
        self._disabled = True

    def enable(self) -> None:
        self._disabled = False
    # endregion
