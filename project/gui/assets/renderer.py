# -*- encoding: utf-8 -*-

"""
In this module reside function that where used to generate assets.
"""


import utils.colors as colors
import config.defaults as defaults
import pygame.surface as surface
import pygame.draw
import itertools as it
import random


width = defaults.WIDTH
height = defaults.HEIGHT
default_background_color = defaults.Colors.BACKGROUND.value

# Custom background texture
background = surface.Surface((width, height))
background.fill(default_background_color)
x_margin = 20
y_margin = 20
border_thickness = 3
vertical_border_length = height - 2 * y_margin
vertical_segment_length = vertical_border_length / 3

PY1 = y_margin
PY2 = PY1 + vertical_segment_length
PY2_EX = PY2 + x_margin
PY3 = PY2 + vertical_segment_length
PY3_EX = PY3 - x_margin
PY4 = PY3 + vertical_segment_length

PX1 = x_margin
PX1_EX = x_margin * 2
PX2 = width - x_margin
PX2_EX = width - x_margin * 2

BORDER_POINTS = [
    (PX1, PY1), (PX2, PY1), (PX2, PY2), (PX2_EX, PY2_EX), (PX2_EX, PY3_EX), (PX2, PY3),
    (PX2, PY4), (PX1, PY4), (PX1, PY3), (PX1_EX, PY3_EX), (PX1_EX, PY2_EX), (PX1, PY2)
]


pygame.draw.line(background, colors.GREY, BORDER_POINTS[-1], BORDER_POINTS[0], width=border_thickness)
for p1, p2 in it.pairwise(BORDER_POINTS):
    pygame.draw.line(background, colors.GREY, p1, p2, width=border_thickness)

pygame.image.save(background, f"background{width}x{height}.png")


# Background animation.
ANIMATION_BACKGROUND = 13, 13, 0


def generate_pixel(_) -> tuple[int, int, int]:
    num = random.random()
    bnum = int(num * 1000) or 1
    return (13, 13, 0) if num > 0.03 else (13 * bnum , 13 * bnum, 13 * bnum)

