# -*- encoding: utf-8 -*-


"""
This module exposes logic of the game of caravan.

import Player


Caravan:

    GameTable:
        Player1:
            piles:
                Pile:
                    value
                    cards:
                        card:
                            applied_face_cards
        Player2:
            --||--
    Ante?
"""
import functools
import random
from collections import deque
from dataclasses import dataclass
from enum        import Enum, auto
from typing      import NamedTuple, Iterable, Iterator


class Suit(Enum):
    """Enumeration of card color suits."""
    SPADE    = auto()
    HEARTS   = auto()
    DIAMONDS = auto()
    CLUBS    = auto()


class Rank(Enum):
    """Enumeration of card ranks."""
    ACE   = auto()
    TWO   = auto()
    THREE = auto()
    FOUR  = auto()
    FIVE  = auto()
    SIX   = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE  = auto()
    TEN   = auto()
    JACK  = auto()
    QUEEN = auto()
    KING  = auto()
    JOKER = auto()


class Card(NamedTuple):
    """Data structure representing a card."""
    suit: Suit
    rank: Rank
    applied_face_cards: list[FaceCard]


class NumericCard(Card):
    """Data structure representing a numeric card."""
    pass


class Ace(Card):
    """Data structure representing an ace."""
    pass


class FaceCard(Card):
    """Data structure representing a face card."""
    def function(self):
        pass


class Pile:
    _cards: list[Card]
    _applied_face_cards: dict[int, list[Card]]

    def append(self, _: Card) -> None:
        """Append new card on top of the pile."""
        self._cards.append(_)

    def apply(self, function_card: FaceCard, card_position: int) -> None:
        """Apply given function to a card with specified position."""
        self._applied_face_cards[card_position].append(function_card)

    @property
    def value(self) -> int:
        return functools.reduce(lambda card:)


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


class Player:
    def __init__(self, piles: list[Pile]):
        self.piles = piles


class Game:
    """Game of caravan object."""
    def __init__(self) -> None:
        raise NotImplementedError
