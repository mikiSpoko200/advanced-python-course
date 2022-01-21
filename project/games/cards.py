#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module implements standard 52 card deck of French suited playing cards.
With added functionality specific to the game of caravan.

# CODE STRUCTURE: consider making clean implementation of the deck for possible different games.
who would I go about doing that?
Should I prepare a generic cards and make some sort of wrappers around them in order to add game specific functionality?
"""


import random
from typing import NamedTuple, Iterable, Iterator
from enum import Enum, auto
from collections import deque


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
    suit:  Suit
    rank:  Rank
    value: int


class NumericCard(Card):
    """Data structure representing a numeric card."""
    pass


class Ace(Card):
    """Data structure representing an ace."""
    pass


class FaceCard(Card):
    """Data structure representing a face card."""
    pass


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
