# -*- encoding: utf-8 -*-

"""
This module exposes logic of bidding section.
"""


from enum import Enum, auto


class Bidding:
    # This needs references to player profiles.

    class State(Enum):
        UNDER    = auto()
        EQUAL    = auto()
        ACCEPTED = auto()
        EXIT     = auto()

    def __init__(self) -> None:
        self.current_ante = 0
        self.opponent_bid = 0
        self.player_bid = 0
        self.state = None

    def auto_match(self) -> None:
        pass

    def accept_ante(self) -> None:
        self.state = Bidding.State.ACCEPTED

    def exit(self) -> None:
        self.state = Bidding.State.EXIT

    def raise_ante(self) -> None:
        raise NotImplementedError("This requires player profiles.")
