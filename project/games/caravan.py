# -*- encoding: utf-8 -*-

import cards
from dataclasses import dataclass


"""
This module exposes logic of the game of caravan.

import Player 


Caravan:

    GameTable:
        Player1,
            piles:
                Pile:
                    value
                    cards:
                        card:
                            applied_face_cards
        Player2,
            --||--
    Ante?
    

"""





@dataclass
class Pile:
    value: int
    cards: deque[]


class Game:
    """Game of caravan object."""
    def __init__(self) -> None:
        self.