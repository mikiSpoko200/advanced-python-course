# -*- encoding: utf-8 -*-

from __future__ import annotations

# STD lib imports
from abc import ABC, abstractmethod
from collections import deque
from copy import copy
from enum import Enum, auto
from typing import Optional, NamedTuple

# Internal imports
from interfaces import IDefault


class IView(ABC):

    @abstractmethod
    def draw(self, surface) -> None:
        pass


def draw_main_menu() -> None:
    pass


def draw_initial_game_table():
    # this should be loaded from json or pickle?
    player = {
        "hand": [],  # hand - a collection of card surfaces
        "deck": [],  # # card upside down
        "piles": {
            "pile1": [],  # card sprites
            "pile2": [],  # card sprites
            "pile3": [],  # card sprites
        }
    }
    opponent = {
        "hand": [],  # similar to player but turned upside down
        "deck": [],  # card upside down
        "piles": {
            "pile1": [],  # card sprites
            "pile2": [],  # card sprites
            "pile3": [],  # card sprites
        }
    }


class Card:
    raise NotImplementedError


Cards = deque[Card]


class Caravan(IDefault):
    MAX_HEIGHT = 7
    MAX_WIDTH = 5

    # URGENT: Card does not implementprovide custom implementation for hashing protocol!!!
    def __init__(self, cards: Cards, applied_cards: dict[Card, list[Card]]) -> None:
        self.cards = cards
        self.applied_cards = applied_cards

    @classmethod
    def default(cls) -> Caravan:
        return cls(deque(), dict())

    def __len__(self) -> int:
        return len(self.cards)


class CaravanPosition(Enum):
    """Enumeration of possible caravan positions."""
    LEFT = auto()
    MIDDLE = auto()
    RIGHT = auto()


Caravans = dict[CaravanPosition, Caravan]


class Player(IDefault):
    CARAVAN_COUNT = 3

    def __init__(self, caravans: Caravans) -> None:
        self.caravans = caravans

    @classmethod
    def default(cls) -> Player:
        return cls({
            CaravanPosition.LEFT: Caravan.default(),
            CaravanPosition.MIDDLE: Caravan.default(),
            CaravanPosition.RIGHT: Caravan.default()
        })


class PlayerPosition(Enum):
    """Enumeration of possible player positions."""
    TOP = auto()
    BOTTOM = auto()


Players = dict[PlayerPosition, Player]


class GameTable(IDefault):
    PLAYER_COUNT = 2

    def __init__(self, players: Players) -> None:
        self.players = players

    @classmethod
    def default(cls) -> GameTable:
        return cls({
            PlayerPosition.TOP: Player.default(), PlayerPosition.BOTTOM: Player.default()
        })

    def apply_card(self, player_index: int, caravan_index: int, card_index: int) -> None:
        pass


class GameState(Enum):
    """Enumeration of main loop states."""
    SELECTED_CARD = auto()
    DISCARD_CARAVAN = auto()
    PLACE_CARD = auto()
    QUIT_GAME = auto()


class PickedCardMovementDirection(Enum):
    """Enumeration of possible movement directions for a picked card.

    Variants here correspond to movements of the card on the table.
    """
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class CardSelectionMovementDirection(Enum):
    """Enumeration of possible directions in which card SELECTION can move.
    This corresponds to the way selection of a card in hand can happen.
    note: fix this mess of a description.
    """
    RIGHT = auto()
    LEFT = auto()


class PickedCardPosition(NamedTuple):
    player: PlayerPosition
    caravan: CaravanPosition
    card_index: int


class GameLoop(IView):
    """
    GameLoop view Events:    KEYS:
        - OnMoveSelection -- ArrowKeyUp | ArrowKeyDown | ArrowKeyLeft | ArrowKeyRight
        - OnSelectCard    -- W
        - OnDiscardCard   -- Q
        - OnDiscardTrack  -- E
        - OnCancel        -- R

        available_options: dict[State, set[State]]

        There is an important distinction between VALIDITY of a move, and it's CORRECTNESS.

        Move is considered VALID whenever it's within bounds. == the right datastructure should do the trick here
        Move is considered CORRECT if it satisfies the rules of the game.

        These, in game, correspond to :
        VALIDITY: places where a card CAN PHYSICALLY BE PLACE on screen.
        CORRECTNESS: places where card is highlighted in green.

        NOTE: correct moves are a subset of valid moves.
        NOTE: all correct moves ARE valid.
    """

    # URGENT: player needs to be specified as a parameter since we can interfer with other player's decks!!!
    # NOTE: this still needs to have actual graphics added!
    # CODE STRUCTURE: consider moving all the positioning logic to the model!

    def __init__(self, game_table: GameTable,
                 picked_card: Optional[Card] = None,
                 _picked_card_position: PickedCardPosition = None) -> None:
        self.game_table = game_table
        self.picked_card = picked_card
        self._picked_card_position = _picked_card_position

    # Game state change event handlers:

    def selection_movement_handler(self, direction: CardSelectionMovementDirection) -> None:
        """This one is tricky.

        Selection here refers to more generic concept of the thing on the screen that we are selecting in one way
        or another. Maybe it's too generic? Maybe I should try going with separate functions?
        """
        pass

    def draw_from_deck(self, direction: PickedCardMovementDirection) -> None:
        pass

    def move_picked_card(self, direction: PickedCardMovementDirection):
        """Perform bound checked move of the self.picked_card in a direction specified."""
        new_position = copy(self._picked_card_position)
        match direction, self._picked_card_position.player:
            # region PickedCardMovementDirection.UP
            case PickedCardMovementDirection.UP, PlayerPosition.TOP:
                # can go as most to len(caravan) + 1 (plus one corresponds to appending to the top of the caravan)
                caravan_len = len(
                    self.game_table.players[PlayerPosition.TOP].caravans[self._picked_card_position.caravan]
                )
                if self._picked_card_position.card_index < caravan_len:
                    self._picked_card_position += 1

            case PickedCardMovementDirection.UP, PlayerPosition.BOTTOM:
                # move card up as long as there are cards on the caravan.
                # If at the top (card_index == 0) overlap to the caravan of the top player.
                # however, do this only if there are cards present on the caravan above!
                if self._picked_card_position.card_index > 0:
                    new_position.card_index -= 1
                else:
                    # if caravan above is not empty move to it else don't move.
                    top_caravan_len = len(
                        self.game_table.players[PlayerPosition.TOP].caravans[self._picked_card_position.caravan]
                    )
                    if top_caravan_len != 0:
                        self._picked_card_position.player = PlayerPosition.TOP
            # endregion

            # region PickedCardMovementDirection.DOWN
            case PickedCardMovementDirection.DOWN, PlayerPosition.TOP:
                if self._picked_card_position.card_index > 0:
                    new_position.card_index -= 1
                else:
                    bottom_caravan_len = len(
                        self.game_table.players[PlayerPosition.BOTTOM].caravans[self._picked_card_position.caravan]
                    )
                    if bottom_caravan_len != 0:
                        self._picked_card_position.player = PlayerPosition.BOTTOM

            case PickedCardMovementDirection.DOWN, PlayerPosition.BOTTOM:
                caravan_len = len(self.game_table.players[PlayerPosition.BOTTOM]
                                  .caravans[self._picked_card_position.caravan])
                if self._picked_card_position.card_index < caravan_len:
                    self._picked_card_position += 1
            # endregion
        
            # region PickedCardMovementDirection.LEFT
            case PickedCardMovementDirection.LEFT, _:
                match self._picked_card_position.caravan:
                    case CaravanPosition.LEFT:
                        pass
                    case CaravanPosition.RIGHT:
                        self._picked_card_position.caravan = CaravanPosition.MIDDLE
                    case CaravanPosition.MIDDLE:
                        self._picked_card_position.caravan = CaravanPosition.LEFT
            # endregion
            
            # region PickedCardMovementDirection.RIGHT
            case PickedCardMovementDirection.RIGHT, _:
                match self._picked_card_position.caravan:
                    case CaravanPosition.LEFT:
                        self._picked_card_position.caravan = CaravanPosition.MIDDLE
                    case CaravanPosition.MIDDLE:
                        self._picked_card_position.caravan = CaravanPosition.RIGHT
                    case CaravanPosition.RIGHT:
                        pass
            # endregion

    def add_new_card_to_deck(self) -> None:
        """Move a new card from a deck to player's hand."""
        pass

        ##                                            ##
        ##          GAME LOOP EVENT HANDLERS          ##
        ##                                            ##

    def apply_face_card_handler(self, face_card, caravan, card) -> None:
        """Apply face_card specified to card in given caravan.

        This associates a new sprite as an applied_face_card.
        This needs to be
        """
        pass

    def append_card_handler(self, caravan: int, card: int) -> None:
        """Append a card to the top of the

        :param caravan: index into the list of player's caravans
        :param card:    index into caravan itself.
        :return: None
        """

    def draw(self, surface) -> None:
        pass
