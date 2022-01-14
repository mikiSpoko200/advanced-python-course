#!/usr/bin/python
# -*- coding: utf-8 -*-

import operator
import itertools
import textwrap
from typing import Iterable


def multi_table(x1: int, x2: int, y1: int, y2: int) -> None:
    """Print formatted multiplication table with rows from y1 to y2 and columns from x1 to x2."""

    if x2 < x1:
        raise ValueError(f"Invalid x range. Expected x1 <= x2, received: {x1=} > {x2=}")
    if y2 < y1:
        raise ValueError(f"Invalid y range. Expected y1 <= y2, received: {y1=} > {y2=}")

    x_range = [1] + [*range(x1, x2 + 1)]
    y_range = [0] + [*range(y1, y2 + 1)]
    col_count = abs(x2 - x1) + 1
    pairs = itertools.product((x1, x2), (y1, y2))
    max_len = max(itertools.starmap(lambda x, y: len(str(x * y)), pairs))
    raw_table: Iterable[str] = list(
        map(
            str,
            itertools.starmap(
                operator.mul,
                itertools.product(
                    y_range,
                    x_range))))
    raw_table[:col_count+1] = [""] + [str(x) for x in x_range[1:]]
    formatted_table = [str(elem).rjust(max_len) for elem in raw_table]
    formatted_table_str = textwrap.fill(
        " ".join(formatted_table),
        (col_count + 1) * (max_len + 1),
        replace_whitespace=False,
        drop_whitespace=False,
        initial_indent=" ")
    print(formatted_table_str)


def main():
    multi_table(-15, 15, -15, 15)


if __name__ == "__main__":
    main()
