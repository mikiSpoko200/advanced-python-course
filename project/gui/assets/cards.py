#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains sprite object for cards.

Cards should have the following states:
    - selected           - make card brighter
    - correctly_paced    - make card green
    - incorrectly_placed - make card red
    - reversed           - display the back side of the card

Cards should be movable across the table.
Cards should have animations of being moved.
Cards should be selectable.
"""

from typing import Optional


import pygame.sprite
import pygame.surface
import games.cards

# region Internal imports
import gui.controls.fonts
import gui.config.defaults as defaults
import gui.utils.interfaces as gui_interfaces
from gui.utils.interfaces import IDefault
from gui.utils.types import RGB, Position
# endregion


class CardColorScheme(gui_interfaces.IDefault):
    """Struct that contains Card color scheme information.

    Scheme consist of 3 sets of color values which correspond to the card's 3 states:
        - select  - used to signal that card CAN be placed in its current location.
        - pressed - used to signal that card CANNOT be places in its current location.
        - default - used in all other cases.
    """

    def __init__(self,
                 background: RGB,
                 default_placement: RGB,
                 correct_placement: RGB,
                 incorrect_placement: RGB) -> None:
        self.background = background
        self.default_placement = default_placement
        self.correct_placement = correct_placement
        self.incorrect_placement = incorrect_placement

    @classmethod
    def default(cls) -> IDefault:
        return cls(
            defaults.Card.BACKGROUND_COLOR.value,
            defaults.Card.DEFAULT_PLACEMENT_COLOR.value,
            defaults.Card.CORRECT_PLACEMENT_COLOR.value,
            defaults.Card.INCORRECT_PLACEMENT_COLOR.value,
        )


# NOTE: DirtySprite may have consequences when im not changing self.dirty
class Card(pygame.sprite.DirtySprite):
    """Card sprite."""

    def __init__(self,
                 card: games.cards.Card,
                 position: Position,
                 width: int = defaults.Card.WIDTH.value,
                 height: int = defaults.Card.HEIGHT.value,
                 color_scheme: Optional[CardColorScheme] = None) -> None:
        super().__init__()
        self.__card = card
        self.__color_scheme = color_scheme or CardColorScheme.default()
        self.__current_color = self.__color_scheme.default_placement
        self.__font_object = gui.controls.fonts.Font.default()
        # sprite implementation
        self.image = pygame.surface.Surface((width, height))
        self.rect = pygame.rect.Rect(position, (width, height))

    def update(self) -> None:
        # render frame by overlapping two rects on top of each other.
        pygame.draw.rect(
            self.image,
            self.__current_color,
            self.rect,
            border_radius=defaults.Card.RECT_BORDER_RADIUS.value)
        pygame.draw.rect(
            self.image,
            self.__current_color,
            self.rect.inflate(-defaults.Card.BORDER_THICKNESS.value, -defaults.Card.BORDER_THICKNESS.value),
            border_radius=defaults.Card.RECT_BORDER_RADIUS.value)
        card_x, card_y = self.rect.topleft

        self.image.blit(
            self.__font_object.render(
                f"{self.__card.rank}{self.__card.suit}",
                defaults.USE_AA,
                self.__current_color,
                self.__color_scheme.background
                ),
            (card_x + defaults.Card.TEXT_X_MARGIN, card_y + defaults.Card.TEXT_Y_MARGIN))

    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)
