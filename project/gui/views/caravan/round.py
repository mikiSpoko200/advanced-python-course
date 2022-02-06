# -*- encoding: utf-8 -*-

"""
This module exposes the view of the Round.
"""

from __future__ import annotations

import collections
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Optional
import random

# External imports
import pygame.sprite
from pygame.surface import Surface

# Internal imports
import games.caravan.logic.round as round_logic
import gui.config.defaults as defaults
import gui.controls as controls
import interfaces as general_interfaces
from gui.types import Position, RGB


# Handy definitions
CARD_WIDTH = defaults.Card.WIDTH.value
CARD_HEIGHT = defaults.Card.HEIGHT.value


class IView(ABC):
    """Interface that make"""

    @abstractmethod
    def draw(self, surface) -> None:
        pass


class CardColorScheme(general_interfaces.IDefault):
    """Struct that contains Card color scheme information.

    Scheme consist of 3 sets of color values which correspond to the card's 3 states:
        - select  - used to signal that card CAN be placed in its current location.
        - pressed - used to signal that card CANNOT be places in its current location.
        - default - used in all other cases.
    """

    def __init__(self,
                 background: RGB,
                 default_color: RGB,
                 correct_color: RGB,
                 incorrect_color: RGB) -> None:
        self.background = background
        self.default_color = default_color
        self.correct_placement = correct_color
        self.incorrect_placement = incorrect_color

    @classmethod
    def default(cls) -> CardColorScheme:
        return cls(
            defaults.Card.BACKGROUND_COLOR.value,
            defaults.Card.DEFAULT_PLACEMENT_COLOR.value,
            defaults.Card.CORRECT_PLACEMENT_COLOR.value,
            defaults.Card.INCORRECT_PLACEMENT_COLOR.value
        )


class Card(pygame.sprite.Sprite):
    """Card sprite.

    Cards should have the following states:
        - selected           - make card brighter
        - correctly_paced    - make card green
        - incorrectly_placed - make card red
        - reversed           - display the back side of the card

    Cards should be movable across the table.
    Cards should have animations of being moved.
    Cards should be selectable.
    """

    class State(Enum):
        DEFAULT   = auto()
        CORRECT   = auto()
        INCORRECT = auto()

    def __init__(self,
                 card: round_logic.Card,
                 position: Position,
                 width: int = defaults.Card.WIDTH.value,
                 height: int = defaults.Card.HEIGHT.value,
                 color_scheme: Optional[CardColorScheme] = None,
                 hidden: bool = False) -> None:
        super().__init__()
        self.card = card
        self.hidden = hidden
        self.__color_scheme = color_scheme or CardColorScheme.default()
        self.__current_color = self.__color_scheme.correct_placement
        self.__font_object = controls.fonts.Font.default()
        # sprite implementation
        self.image = pygame.surface.Surface((width, height), pygame.SRCALPHA)
        self.rect = pygame.rect.Rect(position, (width, height))

    def update(self, state: Card.State = State.DEFAULT) -> None:
        # region border
        match state:
            case Card.State.DEFAULT:
                self.__current_color = self.__color_scheme.default_color
            case Card.State.CORRECT:
                self.__current_color = self.__color_scheme.correct_placement
            case Card.State.INCORRECT:
                self.__current_color = self.__color_scheme.incorrect_placement

        pygame.draw.rect(
            self.image,
            self.__current_color,
            self.image.get_rect(),
            border_radius=defaults.Card.RECT_BORDER_RADIUS.value)
        pygame.draw.rect(
            self.image,
            self.__color_scheme.background,
            self.image.get_rect().inflate(-defaults.Card.BORDER_THICKNESS.value, -defaults.Card.BORDER_THICKNESS.value),
            border_radius=defaults.Card.RECT_BORDER_RADIUS.value)
        # endregion border

        # region text
        if not self.hidden:
            # upper left corner
            text = self.__font_object.render(
                str(self.card),
                defaults.USE_AA,
                self.__current_color,
                self.__color_scheme.background
            )
            self.image.blit(
                text,
                self.image.get_rect().move(defaults.Card.TEXT_X_MARGIN.value, defaults.Card.TEXT_Y_MARGIN.value)
            )
            # upper right corner
            rotated = pygame.transform.flip(text, True, True)
            rect = self.image.get_rect()
            rect.move_ip(
                defaults.Card.WIDTH.value - defaults.Card.TEXT_X_MARGIN.value - rotated.get_width(),
                defaults.Card.HEIGHT.value - defaults.Card.TEXT_Y_MARGIN.value - rotated.get_height()
            )
            self.image.blit(
                rotated,
                rect
            )
        # endregion

    # CODE STRUCTURE: this should be used as Event handler!
    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)


class Hand(IView):

    WIDTH = 250
    HEIGHT = defaults.Card.HEIGHT.value

    def __init__(self, position: Position, hand_obj_ref: round_logic.Hand, hidden: bool = False) -> None:
        self.hand_obj_ref = hand_obj_ref

        card_count = len(self.hand_obj_ref.sequence) or 1

        # URGENT: REMOVE DEBUG
        self.hidden = hidden
        self.rect = pygame.rect.Rect(*position, Hand.WIDTH, Hand.HEIGHT)
        card_corner_offset = Hand.WIDTH // card_count
        self.card_positions = [(i * card_corner_offset + position[0],  position[1])
                               for i in range(card_count)]
        self.cards = [Card(card, position, hidden=self.hidden) for position, card
                  in zip(self.card_positions, self.hand_obj_ref.sequence)]

    def render_selection(self) -> None:
        pass

    def draw(self, surface) -> None:
        for card in self.cards:
            card.update()
            surface.blit(card.image, card.rect)


class GrowDirection(Enum):
    """Enumeration of directions in which caravan can grow."""
    UP = auto()
    DOWN = auto()


class Caravan(IView):
    """Caravan view."""
    def __init__(self, position: Position, caravan_ref: round_logic.Caravan, grow_direction: GrowDirection) -> None:
        self.x, self.y = position
        self.caravan_ref = caravan_ref
        self.grow_direction = grow_direction
        # anchore points where caravans can start. this will grow when new cards are added.
        self.card_positions = [()]
        self.y_offset = Y_OFFSET if grow_direction is GrowDirection.DOWN else -Y_OFFSET
        self.applied_x_offset = APPLIED_X_OFFSET if grow_direction is GrowDirection.DOWN else -APPLIED_X_OFFSET

        self.applied_cards: dict[int, list[Card]] = {}
        self.cards: list[Card] = []
        for index, card in enumerate(self.caravan_ref.cards):
            self.append_card(card)
            for applied_card in self.caravan_ref.applied_face_cards[index]:
                self.apply_card(applied_card, index)

    def append_card(self, card: round_logic.Card) -> None:
        card_sprite = Card(card, (self.x, self.y + self.y_offset * len(self.cards)))
        self.applied_cards[len(self.cards)] = []
        self.cards.append(card_sprite)

    def apply_card(self, function_card: round_logic.Card, card_index: int) -> None:
        """Create sprite for specified function_card and assign it to group"""
        number_of_card_applied = len(self.applied_cards[card_index])
        card_sprite = Card(
            function_card, (
                self.x + (number_of_card_applied + 1) * self.applied_x_offset,
                self.cards[card_index].rect.y))
        self.applied_cards[card_index].append(card_sprite)

    def draw(self, surface: Surface) -> None:
        for index, card in enumerate(self.cards):
            card.update()  # is this necessary?
            surface.blit(card.image, card.rect)
            for applied_card in self.applied_cards[index]:
                applied_card.update()  # is this necessary?
                surface.blit(applied_card.image, applied_card.rect)


X_OFFSET = 150
Y_OFFSET = 30
APPLIED_X_OFFSET = 40
TOP_DRAW_POINTS = [(255 + (85 + X_OFFSET) * i, 200) for i in range(3)]
BOTTOM_DRAW_POINTS = [(150 + (85 + X_OFFSET) * i, 470) for i in range(3)]


class Round(IView):
    DRAW_POINTS = [
        (200, 300 - CARD_HEIGHT), (400, 300 - CARD_HEIGHT), (600, 300 - CARD_HEIGHT),
        (150, 380), (350, 380), (550, 380),
        (750, 180), (770, 180), (790, 180), (810, 180), (830, 180),
        (750, 380), (770, 380), (790, 380), (810, 380), (830, 380)
    ]

    RAND_DRAW_POINTS = list(map(
        lambda x: (x[0] + random.randint(-10, 10), x[1] + random.randint(-10, 10)),
        DRAW_POINTS
    ))

    HAND_POSITIONS = [(900, 200), (900, 500)]

    CARAVAN_POSITIONS = TOP_DRAW_POINTS + BOTTOM_DRAW_POINTS

    def caravan(self, surface: pygame.surface.Surface, caravan: round_logic.Caravan.Position) -> None:
        pass

    def __init__(self, round_manager: Optional[round_logic.RoundManager] = None) -> None:
        self.hands = [Hand(position, hand, hidden=(index == 0)) for position, (index, hand)
                      in zip(Round.HAND_POSITIONS, enumerate(round_manager.hands()))]
        self.caravans = [Caravan(position, caravan, GrowDirection.DOWN if index > 2 else GrowDirection.UP) for position,
                         (index, caravan) in zip(Round.CARAVAN_POSITIONS, enumerate(round_manager.caravans()))]
        self.round_manager = round_manager or round_logic.RoundManager.default()

    def draw(self, surface) -> None:
        """Draws current state of the game to the screen."""

        for hand in self.hands:
            hand.draw(surface)
        for caravan in self.caravans:
            caravan.draw(surface)

        match self.round_manager.state:
            case round_logic.RoundManager.State.SELECT_CARD:
                index = self.round_manager.hand_selection.index
                selected_card = self.hands[1].cards[index]
                selected_card.update(state=Card.State.CORRECT)
                surface.blit(selected_card.image, selected_card.rect)

            case round_logic.RoundManager.State.PLACE_CARD:
                # here we finally need to project data stored in PickedCardPosition to a screen.
                picked_position = self.round_manager.picked_card_position
                positions, shift = {
                    round_logic.Player.Position.TOP: (TOP_DRAW_POINTS, 0),
                    round_logic.Player.Position.BOTTOM: (BOTTOM_DRAW_POINTS, 3)
                }[picked_position.player]
                index = {
                    round_logic.Caravan.Position.LEFT: 0,
                    round_logic.Caravan.Position.MIDDLE: 1,
                    round_logic.Caravan.Position.RIGHT: 2
                }[picked_position.caravan]
                caravan = self.round_manager.caravans()[index + shift]
                x_pos = positions[index][0]
                y_pos = positions[index][1]
                y_pos += self.caravans[index + shift].y_offset * picked_position.card_index
                if picked_position.location is round_logic.PickedCardPosition.Location.OTHER:
                    applied_card_count = len(caravan.applied_face_cards[picked_position.card_index])
                    x_pos += (applied_card_count + 1) * self.caravans[index + shift].applied_x_offset
                else:
                    y_pos += self.caravans[index + shift].y_offset

                card = self.round_manager.picked_card
                picked_card = Card(card, (x_pos, y_pos))
                picked_card.update(Card.State.CORRECT
                                   if self.round_manager.is_current_picked_card_position_correct()
                                   else Card.State.INCORRECT)
                surface.blit(picked_card.image, picked_card.rect)
            case round_logic.RoundManager.State.DISCARD_CARAVAN:
                pass

    @classmethod
    def example(cls) -> Round:
        rm = round_logic.RoundManager.default()

        from games.caravan.logic.round import Rank, Suit

        for index, card in enumerate([round_logic.Card(Rank.NINE, Suit.SPADES),
                               round_logic.Card(Rank.EIGHT, Suit.SPADES)]):
            rm.table.players[round_logic.Player.Position.BOTTOM].caravans[round_logic.Caravan.Position.LEFT].append(card)
            for fcard in {0: [round_logic.Card(Rank.KING, Suit.DIAMONDS)], 1: []}[index]:
                rm.table.players[round_logic.Player.Position.BOTTOM].caravans[round_logic.Caravan.Position.LEFT].apply(fcard, index)

        for index, card in enumerate([
                round_logic.Card(Rank.TWO, Suit.SPADES),
                round_logic.Card(Rank.THREE, Suit.CLUBS),
                round_logic.Card(Rank.FOUR, Suit.SPADES),
                round_logic.Card(Rank.TEN, Suit.CLUBS),
                round_logic.Card(Rank.THREE, Suit.SPADES)]):
            rm.table.players[round_logic.Player.Position.BOTTOM].caravans[round_logic.Caravan.Position.MIDDLE].append(card)
            for fcard in {0: [], 1: [], 2: [round_logic.Card(Rank.KING, Suit.HEARTS)], 3: [], 4: []}[index]:
                rm.table.players[round_logic.Player.Position.BOTTOM].caravans[round_logic.Caravan.Position.MIDDLE].apply(fcard, index)

        for index, card in enumerate([
                        round_logic.Card(Rank.NINE, Suit.CLUBS),
                        round_logic.Card(Rank.EIGHT, Suit.DIAMONDS),
                        round_logic.Card(Rank.FOUR, Suit.HEARTS),
                        round_logic.Card(Rank.THREE, Suit.DIAMONDS),
                        round_logic.Card(Rank.TWO, Suit.DIAMONDS)]):
            rm.table.players[round_logic.Player.Position.BOTTOM].caravans[round_logic.Caravan.Position.RIGHT].append(card)
            for fcard in {0: [], 1: [], 2: [], 3: [], 4: []}[index]:
                rm.table.players[round_logic.Player.Position.BOTTOM].caravans[round_logic.Caravan.Position.RIGHT].apply(fcard, index)

        for index, card in enumerate([
                        round_logic.Card(Rank.EIGHT, Suit.SPADES),
                        round_logic.Card(Rank.NINE, Suit.CLUBS),
                        round_logic.Card(Rank.FOUR, Suit.CLUBS),
                        round_logic.Card(Rank.THREE, Suit.DIAMONDS),
                        round_logic.Card(Rank.TWO, Suit.SPADES)
                    ]):
            rm.table.players[round_logic.Player.Position.TOP].caravans[round_logic.Caravan.Position.LEFT].append(card)
            for fcard in {0: [], 1: [], 2: [], 3: [], 4: []}[index]:
                rm.table.players[round_logic.Player.Position.TOP].caravans[round_logic.Caravan.Position.LEFT].apply(fcard, index)

        for index, card in enumerate([
                        round_logic.Card(Rank.NINE, Suit.DIAMONDS),
                        round_logic.Card(Rank.EIGHT, Suit.DIAMONDS),
                        round_logic.Card(Rank.SEVEN, Suit.DIAMONDS),
                        round_logic.Card(Rank.ACE, Suit.CLUBS),
                        round_logic.Card(Rank.SIX, Suit.CLUBS)
                    ]):
            rm.table.players[round_logic.Player.Position.TOP].caravans[round_logic.Caravan.Position.MIDDLE].append(card)
            for fcard in {0: [], 1: [], 2: [], 3: [], 4: []}[index]:
                rm.table.players[round_logic.Player.Position.TOP].caravans[round_logic.Caravan.Position.MIDDLE].apply(fcard, index)

        for index, card in enumerate([
                        round_logic.Card(Rank.SIX, Suit.SPADES),
                        round_logic.Card(Rank.TEN, Suit.DIAMONDS)
                    ]):
            rm.table.players[round_logic.Player.Position.TOP].caravans[round_logic.Caravan.Position.RIGHT].append(card)
            for fcard in {0: [], 1: [], 2: [], 3: [], 4: []}[index]:
                rm.table.players[round_logic.Player.Position.TOP].caravans[round_logic.Caravan.Position.RIGHT].apply(fcard, index)

        return cls(rm)
