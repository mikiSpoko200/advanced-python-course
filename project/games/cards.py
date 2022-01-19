#!/usr/bin/python
# -*- coding: utf-8 -*-


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


class Card(NamedTuple):
    """Data structure representing a card."""
    suit:  Suit
    value: int
    rank:  str


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
