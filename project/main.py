# -*- encoding: utf-8 -*-

# region STD lib imports
import sys
import random
# endregion

# region External imports
import pygame
# endregion

# region Internal imports
import games.caravan.cards
import gui.assets.cards
from games.caravan.cards import Suit
from gui.utils import colors
from gui.config import defaults
import gui.controls.buttons as buttons
# endregion

# Configuration:
pygame.init()
clock = pygame.time.Clock()

WINDOW_SIZE = WIDTH, HEIGHT = defaults.WIDTH, defaults.HEIGHT
FULL_SCREEN = defaults.FULLSCREEN
SCREEN = pygame.display.set_mode(WINDOW_SIZE) if not FULL_SCREEN else pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

card = pygame.surface.Surface((100, 160))
filled_card = card.fill((230, 153, 0))


# Card games
# CODE STRUCTURE: make card a sprite
CARD_WIDTH = defaults.Card.WIDTH.value
CARD_HEIGHT = defaults.Card.HEIGHT.value

FONT_OBJ = pygame.font.Font(defaults.FONT_PATH, 20)

# Game layout:
DRAW_POINTS = [
    (200, 300 - CARD_HEIGHT), (400, 300 - CARD_HEIGHT), (600, 300 - CARD_HEIGHT),
    (150, 380),               (350, 380),               (550, 380),
    (750, 180), (770, 180), (790, 180), (810, 180), (830, 180),
    (750, 380), (770, 380), (790, 380), (810, 380), (830, 380)
]

RAND_DRAW_POINTS = list(map(
    lambda x: (x[0] + random.randint(-10, 10), x[1] + random.randint(-10, 10)),
    DRAW_POINTS
))


def draw_game_layout(texts: list[str], positions: list[tuple[int, int]]) -> None:
    for text, pos in zip(texts, positions):
        rect = pygame.rect.Rect(pos, (CARD_WIDTH, CARD_HEIGHT))
        pygame.draw.rect(SCREEN, colors.GREY, rect, border_radius=12)
        pygame.draw.rect(SCREEN, colors.HEAVY_NAVY, rect.inflate(-10, -10), border_radius=12)
        card_x, card_y = rect.topleft
        SCREEN.blit(FONT_OBJ.render(text, False, colors.GREY), (card_x + 10, card_y + 10))


card_texts = [
    "2S", "4H", "7D", "7C", "KC", "10S",
    "XX", "XX", "XX", "XX", "XX",
    "XX", "XX", "XX", "XX", "XX"
]


def main():
    """Main game loop."""

    # Load game assets.
    BACKGROUND = pygame.image.load(F"gui/assets/background{WIDTH}x{HEIGHT}.png")

    button_group = pygame.sprite.Group(
        buttons.Button("START", lambda: print("START"), (200, 600)),
        buttons.Button("DRAW", lambda: print("DRAW"), (400, 600)),
        buttons.Button("PLACE", lambda: print("PLACE"), (600, 600))
    )

    card_group = pygame.sprite.Group(
        [gui.assets.cards.Card(games.caravan.caravan.cards.Card(Suit.SPADE, 10, rank), position) for
         rank, position in
         zip(["2", "4", "7", "K", "10"], DRAW_POINTS)]
    )

    while True:

        # Event handling
        # OPTIMIZATION: try using C implemented higher order functions in event loop.
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    sys.exit()
                case pygame.MOUSEMOTION:
                    for button in button_group:
                        if button.rect.collidepoint(*event.pos):
                            if not button.is_pressed:
                                button.selected()
                        else:
                            button.unselected()
                case pygame.MOUSEBUTTONDOWN:
                    for button in button_group:
                        if button.rect.collidepoint(*event.pos):
                            button.pressed()
                            event_loop_is_mouse_button_down = True
                            break
                case pygame.MOUSEBUTTONUP:
                    for button in button_group:
                        if button.rect.collidepoint(*event.pos):
                            button.released()
                            event_loop_is_mouse_button_down = False
                            break

        # Rendering
        SCREEN.blit(BACKGROUND, (0, 0))

        for index, button in enumerate(button_group):
            # if index == 0:
            #     counter = (counter + 1) * int(counter < WIDTH)
            #     button.rect.center = (counter, 600)
            button.update()
        button_group.draw(SCREEN)
        card_group.draw(SCREEN)

        pygame.display.flip()
        clock.tick(defaults.FRAMERATE)


if __name__ == '__main__':
    main()
