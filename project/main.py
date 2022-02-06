# -*- encoding: utf-8 -*-

# region STD lib imports
import sys
# endregion

# region External imports
import pygame
# endregion

# region Internal imports
from gui.config import defaults
import gui.views.caravan.round as views
import games.caravan.logic.round as logic
import gui.controls.buttons as buttons
# endregion

# region Configuration:
pygame.init()
clock = pygame.time.Clock()

WINDOW_SIZE = WIDTH, HEIGHT = defaults.WIDTH, defaults.HEIGHT
FULL_SCREEN = defaults.FULLSCREEN
SCREEN = pygame.display.set_mode(WINDOW_SIZE) if not FULL_SCREEN else pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

card = pygame.surface.Surface((100, 160))
filled_card = card.fill((230, 153, 0))
# endregion


def main():
    """Main game loop."""

    # Load game assets.
    BACKGROUND = pygame.image.load(F"gui/assets/background.bmp")

    button_group: pygame.sprite.Group = pygame.sprite.Group(
        buttons.Button("START", lambda: print("START"), (1280, 700)),
        buttons.Button("DRAW", lambda: print("DRAW"), (1080, 700)),
        buttons.Button("PLACE", lambda: print("PLACE"), (880, 700))
    )

    round_manager = logic.RoundManager.default()
    round_view = views.Round.example()

    while True:

        # Event handling
        # OPTIMIZATION: try using C implemented higher order functions in event loop.
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    sys.exit()
                case pygame.KEYDOWN:
                    round_view.round_manager.handle_user_input(event.key)
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
                            break
                case pygame.MOUSEBUTTONUP:
                    for button in button_group:
                        if button.rect.collidepoint(*event.pos):
                            button.released()
                            break

        # here render game to the screen.

        # Rendering
        SCREEN.blit(BACKGROUND, (0, 0))

        button_group.update()
        button_group.draw(SCREEN)

        round_view.draw(SCREEN)

        pygame.display.flip()
        clock.tick(defaults.FRAMERATE)


if __name__ == '__main__':
    main()
