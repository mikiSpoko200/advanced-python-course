# -*- encoding: utf-8 -*-


from enum import Enum, auto


class UserInputOptions(Enum):
    """Enumeration of possible input values"""
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    MOVE_UP = auto()
    MOVE_DOWN = auto()
    CHAT = auto()
    ACCEPT = auto()
    CANCEL = auto()
