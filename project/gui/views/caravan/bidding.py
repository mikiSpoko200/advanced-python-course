# -*- encoding: utf-8 -*-


"""
This module exposes gameloop bidding game stage view.
"""

import pygame.sprite as sprite

import gui.controls as controls


class BaseView:

    def __init__(self,
                 buttons: list[controls.buttons.Button],
                 sprites: list[sprite.Sprite],
                 fonts: list[controls.fonts.Font]) -> None:
        self.buttons = buttons
        self.sprites = sprites
        self.fonts = fonts
