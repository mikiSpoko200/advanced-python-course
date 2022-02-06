# -*- encoding: utf-8 -*-


from enum import Enum, auto


class Game:
    """
    This class manages the state and defines control flow for the ENTIRE GAME OF CARAVAN that is all the 4 stages.

    NOTE: this class I think shouldn't add any functionality besides state switching. which will occur
          only in two cases:
            1. Earlier stage has finished and game should precede to the next one.
            2. Player decided to quit the game (similar to 1. now that I think of it)
          This implies that all stages define their own behaviour and expose appropriate Manager object.
    """

    class Stages(Enum):
        """Enumeration of the game stages."""
        BIDDING       = auto()
        DECK_ASSEMBLY = auto()
        ROUND         = auto()
        SUMMARY       = auto()

    def __init__(self, stage: Stages):
        self.current_stage = stage
