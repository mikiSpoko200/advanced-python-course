# -*- encoding: utf-8 -*-

"""
This module exposes the logic of the round of caravan via the RoundManager object.

URGENT: AS TEMPORARY SOLUTION I WILL ADD GAME RENDERING CODE HERE AS WELL TO FINISH ON TIME.
        PLEASE, PRETTY PLEASE FINISH THIS IN THE FUTURE, xoxo

FIXME:
"""


from __future__ import annotations

# STD lib imports
import functools
import random
from collections import deque
from collections.abc import Sized
from enum import Enum, auto
from typing import Iterable, Iterator, Optional, Generic, TypeVar, MutableSequence


import pygame


# Internal imports
from interfaces import IDefault
from utils.traits import Derive


# region Card
class Suit(Enum):
    """Enumeration of card color suits."""
    SPADES = auto()
    HEARTS = auto()
    DIAMONDS = auto()
    CLUBS = auto()

    def __str__(self) -> str:
        # ♣, ♦, ♥, ♠
        match self.name:
            case "SPADES":
                return "S"
            case "HEARTS":
                return "H"
            case "DIAMONDS":
                return "D"
            case "CLUBS":
                return "C"


class Rank(Enum):
    """Enumeration of card ranks and value associated with them."""
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = None
    QUEEN = None
    KING = None
    JOKER = None

    def __str__(self) -> str:
        match self.name:
            case "JACK":
                return "J"
            case "QUEEN":
                return "Q"
            case "KING":
                return "K"
            case "JOKER":
                return "*"
            case "ACE":
                return "ACE "
            case _:
                return str(self.value)


class Card(Derive.Debug):
    """Base class for all cards."""

    class Type(Enum):
        VALUE = auto()
        FUNCTION = auto()

    def __init__(self, rank: Rank, suit: Optional[Suit]) -> None:
        self.rank = rank
        self.suit = suit
        self.type = Card.Type.VALUE if rank.value is not None else Card.Type.FUNCTION

    def __str__(self) -> str:
        """Return string representation of the card"""
        return f"{self.rank}{self.suit}"

    def __gt__(self, other: Card) -> bool:
        return self.rank.value > other.rank.value

    def __lt__(self, other: Card) -> bool:
        return self.rank.value < other.rank.value

    def __eq__(self, other: Card) -> bool:
        return self.rank.value == other.rank.value

    def __ne__(self, other: Card) -> bool:
        return not self.__eq__(other)
# endregion


# region Deck
DEFAULT_DECK = [
    Card(Rank.ACE, Suit.SPADES),
    Card(Rank.ACE, Suit.HEARTS),
    Card(Rank.ACE, Suit.DIAMONDS),
    Card(Rank.ACE, Suit.CLUBS),
    Card(Rank.TWO, Suit.SPADES),
    Card(Rank.TWO, Suit.HEARTS),
    Card(Rank.TWO, Suit.DIAMONDS),
    Card(Rank.TWO, Suit.CLUBS),
    Card(Rank.THREE, Suit.SPADES),
    Card(Rank.THREE, Suit.HEARTS),
    Card(Rank.THREE, Suit.DIAMONDS),
    Card(Rank.THREE, Suit.CLUBS),
    Card(Rank.FOUR, Suit.SPADES),
    Card(Rank.FOUR, Suit.HEARTS),
    Card(Rank.FOUR, Suit.DIAMONDS),
    Card(Rank.FOUR, Suit.CLUBS),
    Card(Rank.FIVE, Suit.SPADES),
    Card(Rank.FIVE, Suit.HEARTS),
    Card(Rank.FIVE, Suit.DIAMONDS),
    Card(Rank.FIVE, Suit.CLUBS),
    Card(Rank.SIX, Suit.SPADES),
    Card(Rank.SIX, Suit.HEARTS),
    Card(Rank.SIX, Suit.DIAMONDS),
    Card(Rank.SIX, Suit.CLUBS),
    Card(Rank.SEVEN, Suit.SPADES),
    Card(Rank.SEVEN, Suit.HEARTS),
    Card(Rank.SEVEN, Suit.DIAMONDS),
    Card(Rank.SEVEN, Suit.CLUBS),
    Card(Rank.EIGHT, Suit.SPADES),
    Card(Rank.EIGHT, Suit.HEARTS),
    Card(Rank.EIGHT, Suit.DIAMONDS),
    Card(Rank.EIGHT, Suit.CLUBS),
    Card(Rank.NINE, Suit.SPADES),
    Card(Rank.NINE, Suit.HEARTS),
    Card(Rank.NINE, Suit.DIAMONDS),
    Card(Rank.NINE, Suit.CLUBS),
    Card(Rank.TEN, Suit.SPADES),
    Card(Rank.TEN, Suit.HEARTS),
    Card(Rank.TEN, Suit.DIAMONDS),
    Card(Rank.TEN, Suit.CLUBS),
    Card(Rank.JACK, Suit.SPADES),
    Card(Rank.JACK, Suit.HEARTS),
    Card(Rank.JACK, Suit.DIAMONDS),
    Card(Rank.JACK, Suit.CLUBS),
    Card(Rank.QUEEN, Suit.SPADES),
    Card(Rank.QUEEN, Suit.HEARTS),
    Card(Rank.QUEEN, Suit.DIAMONDS),
    Card(Rank.QUEEN, Suit.CLUBS),
    Card(Rank.KING, Suit.SPADES),
    Card(Rank.KING, Suit.HEARTS),
    Card(Rank.KING, Suit.DIAMONDS),
    Card(Rank.KING, Suit.CLUBS),
    Card(Rank.JOKER, None),
    Card(Rank.JOKER, None),
]


class Deck(Iterable, Sized, IDefault, Derive.Debug):
    """Deck of cards.

    Cards are stored from left to right.
    That is card on top of the deck is on the left end of a queue, conversely Bottom is on the right.
    """

    def __init__(self, cards: list[Card]) -> None:
        self.card_queue = deque(cards)

    def shuffle(self) -> None:
        """Shuffle the deck in place."""
        random.shuffle(self.card_queue)

    def pop(self) -> Card:
        """Return a card from the top of the deck."""
        return self.card_queue.popleft()

    # Interface implementations:

    def __iter__(self) -> Iterator[Card]:
        """Produce an iterator over the deck.

        Iteration is delegated to the composited deque object.
        """
        return iter(self.card_queue)

    def __len__(self) -> int:
        """Number of cards in the deck.

        :return: int number of cards in the deck.
        """
        return len(self.card_queue)

    @classmethod
    def default(cls) -> Deck:
        return cls(DEFAULT_DECK)


# endregion


# region Hand
T = TypeVar("T")


class TwoWayIterator(Generic[T]):

    def __init__(self, sequence: MutableSequence[T], start=0):
        self.sequence = sequence
        self._current_position = start
        self.__start = start

    @property
    def index(self):
        return self._current_position

    @property
    def current(self) -> T:
        """Currently selected item from the sequence."""
        return self.sequence[self._current_position]

    def reset(self) -> None:
        """Reset the iterator to original position."""
        self._current_position = self.__start

    def next(self) -> T:
        """Moves selection forward to the next element."""
        self._current_position = self._current_position + 1 if self._current_position < len(self.sequence) - 1 else 0
        return self.sequence[self._current_position]

    def prev(self) -> T:
        """Moves selection back to the previous element."""
        self._current_position = self._current_position - 1 if self._current_position > 0 else len(self.sequence) - 1
        return self.sequence[self._current_position]


class Selection(TwoWayIterator, Sized):
    """An iterator that wraps around"""

    def __init__(self, sequence: MutableSequence[T]):
        super().__init__(sequence)

    def __len__(self) -> int:
        return len(self.sequence)


class Hand(Selection, Sized, Derive.Debug):
    """Player's hand."""

    def __init__(self, cards: list[Card]) -> None:
        super().__init__(cards)

    def discard(self, position: int) -> None:
        """Discard a card with specified position."""
        del self.sequence[position]

    def append(self, _: Card) -> None:
        """Add a new card to the hand."""
        self.sequence.insert(len(self.sequence) - 1, _)


# endregion


# region Caravan
# aesthetic: consider changing name to Pile or sth and free the Caravan name for the main game managing object?
class Caravan(IDefault, Sized, Derive.Debug):
    """Represents an in game caravan.

    Each caravan is basically a pile of Cards - Ace + cards 2-10
    Some Cards can have Cards associated with them - Jack, Queen, King, Joker.
    These apply specific effects to singular card, a whole caravan or even entire table (Joker on Ace).
    """
    MAX_HEIGHT = 7
    MAX_WIDTH = 5

    class Direction(Enum):
        """Enumeration of caravan directions."""
        ASCENDING = auto()
        DESCENDING = auto()

    class Position(Enum):
        """Enumeration of possible caravan positions."""
        LEFT = auto()
        MIDDLE = auto()
        RIGHT = auto()

    def __init__(self, cards: deque[Card], applied_cards: dict[int, list[Card]],
                 suit: Optional[Suit] = None, direction: Optional[Direction] = None) -> None:
        self.cards = cards
        self.applied_face_cards = applied_cards or {}
        self.suit = suit
        self.direction = direction

    @property
    def prev_card(self) -> Card:
        return self.cards[-1]

    def matches_direction(self, _: Card) -> bool:
        """Check if a card matches caravan's direction."""
        return self.direction is Caravan.Direction.DESCENDING and self.prev_card.rank.value > _.rank.value or \
               self.direction is Caravan.Direction.ASCENDING and self.prev_card.rank.value < _.rank.value

    def matches_suit(self, _: Card) -> bool:
        return self.suit is _.suit

    def append(self, _: Card) -> None:
        """Append new card on top of the caravan."""
        match len(self.cards):
            case 0:
                self.suit = _.suit
            case 1:
                self.direction = Caravan.Direction.DESCENDING if self.cards[0] > _ else Caravan.Direction.ASCENDING

        self.applied_face_cards[len(self.cards)] = list()
        self.cards.append(_)

    def apply(self, function_card: Card, card_index: int) -> None:
        """Apply given function to a card with specified position."""

        self.applied_face_cards[card_index].append(function_card)

    def is_correct_append(self, new_card: Card) -> bool:
        """Determine in new_card can be placed on top of the caravan.

        This means it does not violate direction or is of the caravan suit."""
        is_value_card = new_card.type is Card.Type.VALUE
        match len(self.cards):
            case 0:     # Any value card is correct
                return is_value_card
            case 1:  # Only same value as previous is incorrect
                return is_value_card and new_card.rank is not self.prev_card.rank
            case _:
                return is_value_card and new_card.rank is not self.prev_card.rank and (
                    self.matches_suit(new_card) or self.matches_direction(new_card)
                )

    @property
    def value(self) -> int:
        return functools.reduce(
            # double the card's value that many times as there are kings associated with it.
            lambda acc_outer, pos_card: acc_outer + pos_card[1].rank.value * 2 ** functools.reduce(
                # Count the number of kings associated with a card.
                lambda acc_inner, face_card: acc_inner + int(face_card.rank is Rank.KING),
                self.applied_face_cards.get(pos_card[0], []),
                0
            ),
            enumerate(self.cards),
            0
        )

    @classmethod
    def default(cls) -> Caravan:
        return cls(deque(), dict(), None, None)

    def __len__(self) -> int:
        return len(self.cards)


Caravans = dict[Caravan.Position, Caravan]


# endregion


# region Player
class Player(IDefault, Derive.Debug):
    """Representation of a Player.

    Player composes a Hand, Deck and three Caravans.
    """
    CARAVAN_COUNT = 3

    class Position(Enum):
        """Enumeration of possible player positions."""
        TOP = auto()
        BOTTOM = auto()

    def __init__(self, deck: Deck, hand: Hand, caravans: Caravans) -> None:
        self.deck = deck
        self.hand = hand
        self.caravans = caravans

    @classmethod
    def default(cls) -> Player:
        deck = Deck.default()
        hand_cards = [deck.pop() for _ in range(8)]
        caravans = {
            Caravan.Position.LEFT: Caravan.default(),
            Caravan.Position.MIDDLE: Caravan.default(),
            Caravan.Position.RIGHT: Caravan.default()
        }
        return cls(deck, Hand(hand_cards), caravans)

    def draw_from_deck(self) -> None:
        """Draw a new card from player's deck to hand if there are any."""
        if len(self.deck) > 0:
            self.hand.append(self.deck.pop())

    def discard_caravan(self, caravan_pos: Caravan.Position) -> None:
        self.caravans[caravan_pos] = Caravan.default()


Players = dict[Player.Position, Player]


# endregion


# region Table
class Table(IDefault, Derive.Debug):
    PLAYER_COUNT = 2

    def __init__(self, players: Players) -> None:
        self.players = players

    @classmethod
    def default(cls) -> Table:
        return cls({
            Player.Position.TOP: Player.default(), Player.Position.BOTTOM: Player.default()
        })

    def swap_players(self) -> None:
        """This method is a hack for the server to swap positions during communication - temp."""
        self.players[Player.Position.BOTTOM], self.players[Player.Position.TOP] = \
            self.players[Player.Position.TOP], self.players[Player.Position.BOTTOM]


# endregion


# region Round
class Direction(Enum):
    """Enumeration of possible movement directions for a picked card.

    Variants here correspond to movements of the card on the table.
    """
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class HorizontalDirection(Enum):
    """Enumeration of possible directions in which card SELECTION can move.
    This corresponds to the way selection of a card in hand can happen.
    note: fix this mess of a description.
    """
    RIGHT = auto()
    LEFT = auto()


class PickedCardPosition(Derive.Debug):
    """Information about picked card."""

    class Location(Enum):
        TOP = auto()
        OTHER = auto()

    def __init__(self, player: Player.Position, caravan: Caravan.Position, card_index: int, location: Location) -> None:
        self.player = player
        self.caravan = caravan
        self.card_index = card_index
        self.location = location

    @classmethod
    def default_with_position(cls, location: PickedCardPosition.Location) -> PickedCardPosition:
        return cls(Player.Position.BOTTOM, Caravan.Position.LEFT, 0, location)


# URGENT: handle first 3 rounds in a special way.
class RoundManager(IDefault, Derive.Debug):
    # NOTE: All methods ASSUME THAT THEY CAN BE CALLED, and since they depend on certain configuration of the state,
    #       we must ensure is being correct before allowing for the call.

    """
    NOTE: This class manages the state of the round. It handles all the relevant events, and performs all operations
          necessary on the aggregated data.


    FIXME: certain methods should be available in certain states this corresponds to how the view should render buttons
           connected with this functionality. How should manage it?


    Overview:
    Game view Events:     KEYS:
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
    """

    class State(Enum):
        """Enumeration of round's states."""
        SELECT_CARD = auto()
        DISCARD_CARAVAN = auto()
        PLACE_CARD = auto()

    class StopGame(Exception):
        """Temporary exception raised when Game should return to main menu or lobby?"""
        def __init__(self, *args):
            self.args = args

        def __str__(self) -> str:
            return "EXIT GAME."

    def __init__(self, table: Table, state: State, turn_count: int = 1,
                 picked_card: Optional[Card] = None,
                 picked_card_position: Optional[PickedCardPosition] = None) -> None:
        self.table = table
        self.state = state
        self.turn_count = turn_count
        self.hand_selection = TwoWayIterator(self.table.players[Player.Position.BOTTOM].hand.sequence)
        self.selected_hand_card: Optional[Card] = self.hand_selection.current
        self.discard_selection = TwoWayIterator([Caravan.Position.LEFT, Caravan.Position.MIDDLE, Caravan.Position.RIGHT])
        self.selected_discard_caravan = None
        self.picked_card = picked_card
        self.picked_card_position = picked_card_position

    def players(self) -> tuple[Player, Player]:
        """Return tuple of references to top player and bottom player."""
        return self.table.players[Player.Position.TOP], self.table.players[Player.Position.BOTTOM]

    def caravans(self) -> tuple[Caravan, Caravan, Caravan, Caravan, Caravan, Caravan]:
        """Return tuple of all caravans starting from top player moving right."""
        return (self.table.players[Player.Position.TOP].caravans[Caravan.Position.LEFT],
                self.table.players[Player.Position.TOP].caravans[Caravan.Position.MIDDLE],
                self.table.players[Player.Position.TOP].caravans[Caravan.Position.RIGHT],
                self.table.players[Player.Position.BOTTOM].caravans[Caravan.Position.LEFT],
                self.table.players[Player.Position.BOTTOM].caravans[Caravan.Position.MIDDLE],
                self.table.players[Player.Position.BOTTOM].caravans[Caravan.Position.RIGHT])

    def handle_user_input(self, key: int) -> None:
        match self.state:
            case RoundManager.State.SELECT_CARD:
                assert self.picked_card is None
                assert self.selected_discard_caravan is None
                match key:
                    case pygame.K_LEFT:
                        self.move_card_selection(HorizontalDirection.RIGHT)  # FIXME: REVERS POLARITY
                    case pygame.K_RIGHT:
                        self.move_card_selection(HorizontalDirection.LEFT)  # FIXME: REVERS POLARITY
                    case pygame.K_ESCAPE:
                        print("ESCAPE")
                        self.cancel()
                    case pygame.K_RETURN:
                        print("ENTER")
                        self.pick_selected_card()
            case RoundManager.State.PLACE_CARD:
                assert self.selected_discard_caravan is None
                match key:
                    case pygame.K_UP:
                        self.move_picked_card(Direction.UP)
                    case pygame.K_DOWN:
                        self.move_picked_card(Direction.DOWN)
                    case pygame.K_LEFT:
                        self.move_picked_card(Direction.LEFT)
                    case pygame.K_RIGHT:
                        self.move_picked_card(Direction.RIGHT)
                    case pygame.K_ESCAPE:
                        self.cancel()
                    case pygame.K_RETURN:
                        if self.is_current_picked_card_position_correct():
                            self.place_picked_card()
            case RoundManager.State.DISCARD_CARAVAN:
                assert self.picked_card is None
                match key:
                    case pygame.K_LEFT:
                        self.move_discard_selection(HorizontalDirection.LEFT)
                    case pygame.K_RIGHT:
                        self.move_discard_selection(HorizontalDirection.RIGHT)
                    case pygame.K_ESCAPE:
                        self.cancel()
                    case pygame.K_KP_ENTER:
                        self.pick_selected_card()

    def hands(self) -> tuple[Hand, Hand]:
        """Return tuple of player hands in top player, bottom player order."""
        return self.table.players[Player.Position.TOP].hand, self.table.players[Player.Position.BOTTOM].hand

    @staticmethod
    def finish_turn() -> None:
        """Notify that the player has finished the turn."""
        print("TURN FINISHED!")

    def exit_game(self) -> None:
        """Exits game, this should prompt for confirmation."""
        while True:
            match input("Do you want to exit? [Y/n]\n> "):
                case "Y":
                    raise RoundManager.StopGame()
                case "n":
                    self.state = RoundManager.State.SELECT_CARD
                    return
                case _:
                    pass

    def cancel(self) -> None:
        """Return to card selection state, or begin process of exiting the game if already in card selection state.

        This method also performs all the necessary state changes.
        """
        match self.state:
            case RoundManager.State.PLACE_CARD:
                self.picked_card = None
                self.picked_card_position = None
                self.state = RoundManager.State.SELECT_CARD
            case RoundManager.State.DISCARD_CARAVAN:
                self.selected_discard_caravan = None
                self.state = RoundManager.State.SELECT_CARD
            case RoundManager.State.SELECT_CARD:
                self.exit_game()

    def change_state(self, destination_state: RoundManager.State) -> None:
        """Set state to the new value."""
        self.state = destination_state

    # region SELECT_CARD state methods
    def pick_selected_card(self) -> None:
        """Mark card selected in hand as picked card, move it to default position and change state."""
        self.picked_card = self.selected_hand_card
        self.picked_card_position = PickedCardPosition.default_with_position(
            PickedCardPosition.Location.OTHER
            if len(self.table.players[Player.Position.BOTTOM].caravans[Caravan.Position.LEFT]) != 0
            else PickedCardPosition.Location.TOP
        )
        self.change_state(RoundManager.State.PLACE_CARD)

    def move_card_selection(self, direction: HorizontalDirection) -> None:
        """Move discard caravan selection in the specified direction."""
        match direction:
            case HorizontalDirection.LEFT:
                self.selected_hand_card = self.hand_selection.next()
            case HorizontalDirection.RIGHT:
                self.selected_hand_card = self.hand_selection.prev()
    # endregion

    # region DISCARD_CARAVAN state methods
    def discard_caravan(self, player: Player.Position, caravan: Caravan.Position) -> None:
        """Discards selected caravan of selected player.

        To do this selected caravan is reset to default.
        """
        self.table.players[player].caravans[caravan] = Caravan.default()
        self.finish_turn()

    def move_discard_selection(self, direction: HorizontalDirection) -> None:
        """Move discard caravan selection in the specified direction."""
        match direction:
            case HorizontalDirection.LEFT:
                self.selected_discard_caravan = self.discard_selection.next()
            case HorizontalDirection.RIGHT:
                self.selected_discard_caravan = self.discard_selection.prev()
    # endregion

    # region PLACE_CARD state methods
    def move_picked_card(self, direction: Direction):
        """Perform bound checked move of the self.picked_card in a direction specified."""
        match direction, self.picked_card_position.player:
            # region PickedCardMovementDirection.UP
            case Direction.UP, Player.Position.TOP:
                # can go as most to len(caravan) + 1 (plus one corresponds to appending to the top of the caravan)
                caravan_len = len(
                    self.table.players[Player.Position.TOP].caravans[self.picked_card_position.caravan]
                )
                if self.picked_card_position.card_index + 1 < caravan_len:
                    self.picked_card_position.card_index += 1
                else:
                    self.picked_card_position.location = PickedCardPosition.Location.TOP

            case Direction.UP, Player.Position.BOTTOM:
                # move card up as long as there are cards on the caravan.
                # If at the top (card_index == 0) overlap to the caravan of the top player.
                # however, do this only if there are cards present on the caravan above!
                if self.picked_card_position.card_index > 0:
                    if self.picked_card_position.location is not PickedCardPosition.Location.TOP:
                        self.picked_card_position.card_index -= 1
                    self.picked_card_position.location = PickedCardPosition.Location.OTHER
                else:
                    # if caravan above is not empty move to it else don't move.
                    top_caravan_len = len(
                        self.table.players[Player.Position.TOP].caravans[self.picked_card_position.caravan]
                    )
                    if top_caravan_len != 0:
                        self.picked_card_position.player = Player.Position.TOP
            # endregion

            # region PickedCardMovementDirection.DOWN
            case Direction.DOWN, Player.Position.TOP:
                if self.picked_card_position.card_index > 0:
                    if self.picked_card_position.location is not PickedCardPosition.Location.TOP:
                        self.picked_card_position.card_index -= 1
                    self.picked_card_position.location = PickedCardPosition.Location.OTHER
                else:
                    bottom_caravan_len = len(
                        self.table.players[Player.Position.BOTTOM].caravans[self.picked_card_position.caravan]
                    )
                    if bottom_caravan_len != 0:
                        self.picked_card_position.player = Player.Position.BOTTOM

            case Direction.DOWN, Player.Position.BOTTOM:
                caravan_len = len(
                    self.table.players[Player.Position.BOTTOM].caravans[self.picked_card_position.caravan]
                )
                if self.picked_card_position.card_index + 1 < caravan_len:
                    self.picked_card_position.card_index += 1
                else:
                    self.picked_card_position.location = PickedCardPosition.Location.TOP
            # endregion

            # region PickedCardMovementDirection.LEFT
            case Direction.LEFT, _:
                if self.picked_card_position.caravan is not Caravan.Position.LEFT:
                    neighbour = Caravan.Position.LEFT \
                                if self.picked_card_position.caravan is Caravan.Position.MIDDLE \
                                else Caravan.Position.MIDDLE

                    neighbour_len = len(self.table
                                        .players[self.picked_card_position.player]
                                        .caravans[neighbour])
                    neighbour_max_index = neighbour_len - 1
                    match self.picked_card_position.location:
                        case PickedCardPosition.Location.TOP:
                            if neighbour_max_index > self.picked_card_position.card_index:
                                self.picked_card_position.card_index += 1
                                self.picked_card_position.location = PickedCardPosition.Location.OTHER
                            elif neighbour_max_index == self.picked_card_position.card_index:
                                pass  # just switch caravans
                            else:  # neighbour_max_index < self.picked_card_position.card_index
                                self.picked_card_position.card_index = neighbour_max_index
                        case PickedCardPosition.Location.OTHER:
                            if neighbour_max_index > self.picked_card_position.card_index:
                                pass
                            elif neighbour_max_index == self.picked_card_position.card_index:
                                pass
                            else:
                                self.picked_card_position.card_index = neighbour_max_index
                                self.picked_card_position.location = PickedCardPosition.Location.TOP
                    self.picked_card_position.caravan = neighbour
            # endregion

            # region PickedCardMovementDirection.RIGHT
            case Direction.RIGHT, _:
                if self.picked_card_position.caravan is not Caravan.Position.RIGHT:
                    neighbour = Caravan.Position.RIGHT \
                                if self.picked_card_position.caravan is Caravan.Position.MIDDLE \
                                else Caravan.Position.MIDDLE

                    neighbour_len = len(self.table
                                        .players[self.picked_card_position.player]
                                        .caravans[neighbour])
                    neighbour_max_index = neighbour_len - 1
                    match self.picked_card_position.location:
                        case PickedCardPosition.Location.TOP:
                            if neighbour_max_index > self.picked_card_position.card_index:
                                self.picked_card_position.card_index += 1
                                self.picked_card_position.location = PickedCardPosition.Location.OTHER
                            elif neighbour_max_index == self.picked_card_position.card_index:
                                pass  # just switch caravans
                            else:  # neighbour_max_index < self.picked_card_position.card_index
                                self.picked_card_position.card_index = neighbour_max_index
                        case PickedCardPosition.Location.OTHER:
                            if neighbour_max_index > self.picked_card_position.card_index:
                                pass
                            elif neighbour_max_index == self.picked_card_position.card_index:
                                pass
                            else:
                                self.picked_card_position.card_index = neighbour_max_index
                                self.picked_card_position.location = PickedCardPosition.Location.TOP
                    self.picked_card_position.caravan = neighbour
            # endregion

    def is_current_picked_card_position_correct(self) -> bool:
        """Determine if current position of picked card is correct.

        During first three turns all players need to start each of their caravans,
        So special rules apply.

        In all other cases the following rules determine if card is placed correctly.
        Value card is positioned correctly if it's located on top of some caravan and does follow either
        suit of said caravan or it's direction.
        Function card is positioned correctly if it's not located on top.
        """

        player = self.picked_card_position.player
        caravan = self.picked_card_position.caravan
        is_value_card_placed_on_top = self.picked_card_position.location is PickedCardPosition.Location.TOP and \
                                      self.picked_card.type is Card.Type.VALUE
        can_value_card_be_appended = self.table.players[player].caravans[caravan].is_correct_append(self.picked_card)
        is_function_card_not_on_top = self.picked_card_position.location is PickedCardPosition.Location.OTHER and \
                                      self.picked_card.type is Card.Type.FUNCTION
        return is_function_card_not_on_top or (is_value_card_placed_on_top and can_value_card_be_appended)

    def place_picked_card(self) -> None:
        match self.picked_card.type:
            case Card.Type.VALUE:
                self.table.players[self.picked_card_position.player] \
                    .caravans[self.picked_card_position.caravan] \
                    .append(self.picked_card)
            case Card.Type.FUNCTION:
                self.table.players[self.picked_card_position.player] \
                    .caravans[self.picked_card_position.caravan] \
                    .apply(self.picked_card, self.picked_card_position.card_index)
        self.finish_turn()
    # endregion

    @classmethod
    def default(cls) -> RoundManager:
        return cls(Table.default(), RoundManager.State.SELECT_CARD)
# endregion
