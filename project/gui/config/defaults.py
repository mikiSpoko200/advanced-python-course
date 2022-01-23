# -*- encoding: utf-8 -*-

# STD lib imports
import enum

# External imports
import pygame
import pygame.display as disp

# Internal imports
import gui.utils.colors as colors


pygame.display.init()


# Display.
INFOOBJ = disp.Info()
WIDTH, HEIGHT = 1210, 700  # INFOOBJ.current_w, INFOOBJ.current_h
FRAMERATE = 60
FULLSCREEN = False


class Colors(enum.Enum):
    """Default configuration of """
    BACKGROUND = colors.HEAVY_NAVY


# Fonts.
FONT_PATH = r"gui/assets/fonts/upheavtt.ttf"
FONT_SIZE = 20
USE_AA = False


class Card(enum.Enum):
    """Default settings for a Card sprite."""
    DEFAULT_PLACEMENT_COLOR   = colors.GREY
    CORRECT_PLACEMENT_COLOR   = colors.LIGHT_GREY
    INCORRECT_PLACEMENT_COLOR = colors.DIM_RED
    BACKGROUND_COLOR          = Colors.BACKGROUND.value
    WIDTH                     = 80
    HEIGHT                    = 125
    FONT                      = FONT_PATH
    FONT_SIZE                 = FONT_SIZE
    BORDER_THICKNESS          = 8
    RECT_BORDER_RADIUS        = 12
    TEXT_X_MARGIN             = 10
    TEXT_Y_MARGIN             = 10


# aesthetic: work out nice default color scheme.
class Button(enum.Enum):
    """Default settings for buttons."""
    DEFAULT_FOREGROUND_COLOR = colors.LIGHT_GREY
    DEFAULT_BACKGROUND_COLOR = Colors.BACKGROUND.value
    SELECT_FOREGROUND_COLOR  = colors.WHITE
    SELECT_BACKGROUND_COLOR  = colors.BLUE
    PRESS_FOREGROUND_COLOR   = colors.BLUE
    PRESS_BACKGROUND_COLOR   = colors.WHITE
    FONT                     = FONT_PATH
    FONT_SIZE                = FONT_SIZE
