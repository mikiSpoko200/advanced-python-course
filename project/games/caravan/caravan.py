# -*- encoding: utf-8 -*-

from __future__ import annotations


# STD lib imports
import functools
import random
from collections import deque
from enum import Enum, auto
from typing import NamedTuple, Iterable, Iterator, Optional

# Internal imports
from interfaces import IDefault


class Suit(Enum):
    """Enumeration of card color suits."""
    SPADES   = auto()
    HEARTS   = auto()
    DIAMONDS = auto()
    CLUBS    = auto()


class Rank(Enum):
    """Enumeration of card ranks and value associated with them."""
    ACE   = 1
    TWO   = 2
    THREE = 3
    FOUR  = 4
    FIVE  = 5
    SIX   = 6
    SEVEN = 7
    EIGHT = 8
    NINE  = 9
    TEN   = 10
    JACK  = None
    QUEEN = None
    KING  = None
    JOKER = None


class Card(NamedTuple):
    """Base class for all cards."""
    rank: Rank
    suit: Optional[Suit]


class ValueCard(Card):
    """Card that has an associated value."""
    pass


class FunctionCard(Card):
    """Card that has an associated function."""
    pass


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


# aesthetic: consider changing name to Pile or sth and free the Caravan name for the main game managing object?
class Caravan:
    """Represents an in game caravan.

    Each caravan is basically a pile of ValueCards - Ace + cards 2-10
    Some ValueCards can have FunctionCards associated with them - Jack, Queen, King, Joker.
    These apply apply specific effects to singular card, a whole caravan or even entire table (Joker on Ace).
    """

    _cards: list[ValueCard]
    _applied_face_cards: dict[int, list[FunctionCard]]

    def append(self, _: ValueCard) -> None:
        """Append new card on top of the pile."""
        self._cards.append(_)

    def apply(self, function_card: FunctionCard, card_position: int) -> None:
        """Apply given function to a card with specified position."""
        self._applied_face_cards[card_position].append(function_card)

    @property
    def value(self) -> int:
        return functools.reduce(
            # double the card's value that many times as there are kings associated with it.
            lambda pos_card: pos_card[1].rank.value * 2 ** functools.reduce(
                # Count the number of kings associated with a card.
                lambda acc, face_card: acc + int(face_card.rank == Rank.KING),
                self._applied_face_cards.get(pos_card[0], []),
                0
            ),
            enumerate(self._cards),
            0
        )


class Deck(Iterable):
    """Deck of cards.

    Cards are stored from left to right.
    That is card on top of the deck is on the left end of a queue, conversely Bottom is on the right.
    """

    def __init__(self, cards: list[Card]) -> None:
        self.__card_queue = deque(cards)

    def __iter__(self) -> Iterator[Card]:
        """Produce an iterator over the deck.

        Iteration is delegated to the composited deque object.
        """
        return iter(self.__card_queue)

    def shuffle(self) -> None:
        """Shuffle the deck in place."""
        random.shuffle(self.__card_queue)

    def pop(self) -> Card:
        """Return a card from the top of the deck."""
        return self.__card_queue.popleft()

    def place_back(self, _: Card) -> None:
        """Place a card at the bottom of the deck."""
        self.__card_queue.append(_)


class Hand:
    """Player's hand."""

    def __init__(self, cards: list[Card]) -> None:
        self._cards = cards

    def discard(self, position: int) -> None:
        """Discard a card with specified position."""
        del self._cards[position]

    def append(self, _: Card) -> None:
        self._cards.append(_)


class Player:
    """Representation of a Player.

    Player composes a Hand, Deck and three Caravans.
    """

    def __init__(self, deck: Deck, hand: Hand, caravans: list[Caravan]) -> None:
        self._deck = deck
        self._hand = hand
        self._caravans = caravans


class Table:
    """Table object that encapsulates the whole game logic."""
    def __init__(self, player1: Player, player2: Player) -> None:
        self.player1 = player1
        self.player2 = player2

    def append(self, player: Player):
        pass


class GameLoop:
    class GameStateError(Exception):
        def __init__(self, msg):
            super().__init__()
            self.msg = msg

        def __str__(self) -> str:
            return self.msg

    class States(Enum):
        """Enumeration of main loop states."""
        SelectCard     = auto()
        DiscardCaravan = auto()
        PlaceCard      = auto()
        QuitGame       = auto()

    def __init__(self, game_table: Table, state: States):
        self._game_table = game_table
        self._state = state

    """
    OK let's T H I N K
    
    Let's start with buttons. When user presses a button (or a key corresponding to it) the button fires an Event.
    Let's call it OnClick for example. That is cool, this allows us to assign different game state modifications to
    those events by subscribing / passing appropriate method as callbacks and so on.
    Similarly there are certain changes in game state that the view should reflect, say we added a new card to the top
    of one of our caravans. This consequently can again fire yet another event let's call it OnCardAppend.
    This event needs to pass some more CONTEXT to the subscribers to disambiguate the caravan on which the card was placed.
    So we can design the OnCardAppend event's notify() method to take appropriate args like caravan.
    Well this is quite nice if I could say so myself. Now user interface knows where to put the bloody sprite on the screen.
    
    Well and how about pressing a KEY in order to enter specific GAME STATE? Well this is quite tricksy not gonna lie.
    Let's think about how the positions where the cards can move should be calculated shall we?
    
    We know the core geometry of the game screen. We know where each pile starts 
    
    
    """


    def _quit_game(self) -> None:
        raise NotImplementedError("Add exiting logic here.")

    def state_change(self, new_state: States):
        raise NotImplementedError("Add state change logic here.")


    def cancel(self) -> None:
        match self._state:
            case GameLoop.States.PlaceCard:
                self._state = GameLoop.States.SelectCard
            case GameLoop.States.DiscardCaravan:
                self._state = GameLoop.States.SelectCard
            case GameLoop.States.SelectCard:
                self._state = GameLoop.States.QuitGame
            case other:
                raise GameLoop.GameStateError(f"Invalid state for cancel call: self._state = {other}")


class GameCaravan(IDefault):
    """Represents a game object that manages the state of the game.

    This extends to all diverent views that is deck composition, game proper and final screen with results.
    NOTE: THIS IS NOT COMPLETE GAME LOGIC. STILL THE ONLINE LOBBY, PROFILE CREATION AND MAIN MENU NEED TO BE HANDLED!
    """

    class Stages(Enum):
        """Enumeration of the game stages."""
        DeckComposition = auto()
        MainLoop        = auto()
        Summary         = auto()


    def __init__(self, stage: Stages, game_table: Table):
        self._stage = stage
        self._main_loop_state = None
        self._game_table = game_table


    @classmethod
    def default(cls) -> GameCaravan:
        pass
