# -*- encoding: utf-8 -*-

import itertools as it
from typing import Iterable


class PerfectNumberSieve:
    """TODO: add description."""

    def __init__(self, n: int) -> None:
        self.n = n

    def perfect_imperative(self) -> list[int]:
        raise NotImplementedError

    def perfect_comprehension(self) -> list[int]:
        raise NotImplementedError

    def perfect_functional(self) -> Iterable[int]:
        raise NotImplementedError


def main():
    print("Hello world!")


if __name__ == '__main__':
    main()