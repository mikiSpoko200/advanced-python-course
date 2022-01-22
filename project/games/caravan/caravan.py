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
from typing import NamedTuple, Iterable, Iterator, Optional, overload


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
    Card(Rank.ACE, Suit.SPADE),
    Card(Rank.ACE, Suit.HEART),
    Card(Rank.ACE, Suit.DIAMOND),
    Card(Rank.ACE, Suit.CLUBS),
    Card(Rank.TWO, Suit.SPADE),
    Card(Rank.TWO, Suit.HEART),
    Card(Rank.TWO, Suit.DIAMOND),
    Card(Rank.TWO, Suit.CLUBS),
    Card(Rank.THREE, Suit.SPADE),
    Card(Rank.THREE, Suit.HEART),
    Card(Rank.THREE, Suit.DIAMOND),
    Card(Rank.THREE, Suit.CLUBS),
    Card(Rank.FOUR, Suit.SPADE),
    Card(Rank.FOUR, Suit.HEART),
    Card(Rank.FOUR, Suit.DIAMOND),
    Card(Rank.FOUR, Suit.CLUBS),
    Card(Rank.FIVE, Suit.SPADE),
    Card(Rank.FIVE, Suit.HEART),
    Card(Rank.FIVE, Suit.DIAMOND),
    Card(Rank.FIVE, Suit.CLUBS),
    Card(Rank.SIX, Suit.SPADE),
    Card(Rank.SIX, Suit.HEART),
    Card(Rank.SIX, Suit.DIAMOND),
    Card(Rank.SIX, Suit.CLUBS),
    Card(Rank.SEVEN, Suit.SPADE),
    Card(Rank.SEVEN, Suit.HEART),
    Card(Rank.SEVEN, Suit.DIAMOND),
    Card(Rank.SEVEN, Suit.CLUBS),
    Card(Rank.EIGHT, Suit.SPADE),
    Card(Rank.EIGHT, Suit.HEART),
    Card(Rank.EIGHT, Suit.DIAMOND),
    Card(Rank.EIGHT, Suit.CLUBS),
    Card(Rank.NINE, Suit.SPADE),
    Card(Rank.NINE, Suit.HEART),
    Card(Rank.NINE, Suit.DIAMOND),
    Card(Rank.NINE, Suit.CLUBS),
    Card(Rank.TEN, Suit.SPADE),
    Card(Rank.TEN, Suit.HEART),
    Card(Rank.TEN, Suit.DIAMOND),
    Card(Rank.TEN, Suit.CLUBS),
    Card(Rank.JACK, Suit.SPADE),
    Card(Rank.JACK, Suit.HEART),
    Card(Rank.JACK, Suit.DIAMOND),
    Card(Rank.JACK, Suit.CLUBS),
    Card(Rank.QUEEN, Suit.SPADE),
    Card(Rank.QUEEN, Suit.HEART),
    Card(Rank.QUEEN, Suit.DIAMOND),
    Card(Rank.QUEEN, Suit.CLUBS),
    Card(Rank.KING, Suit.SPADE),
    Card(Rank.KING, Suit.HEART),
    Card(Rank.KING, Suit.DIAMOND),
    Card(Rank.KING, Suit.CLUBS),
    Card(Rank.JOKER, None),
    Card(Rank.JOKER, None),
]


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
        self._cards.pop(position)

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


class Game:
    """Game of caravan object."""
    def __init__(self, player1: Player, player2: Player) -> None:
        self.player1 = player1
        self.player2 = player2

    def append(self, player: Player):


