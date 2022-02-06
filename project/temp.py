# -*- encoding: utf-8 -*-

from games.caravan.logic.round import *
from os import system


class TwoWayIterator(Generic[T]):

    def __init__(self, sequence: MutableSequence[T], start=0):
        self.sequence = sequence
        self._current_position = start

    @property
    def index(self):
        return self._current_position

    @property
    def current(self) -> T:
        """Currently selected item from the sequence."""
        return self.sequence[self._current_position]

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


def cls():
    system("cls")


def main():
    card = Rank.JACK
    print(card)


if __name__ == '__main__':
    main()
