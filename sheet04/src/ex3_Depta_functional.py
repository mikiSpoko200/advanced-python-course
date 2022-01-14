#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import annotations


import itertools as it
from copy import deepcopy
from typing import Iterable, Optional, NamedTuple


EXAMPLE_SUDOKU = [
    [None, None, 3, None, 2, None, 6, None, None],
    [9, None, None, 3, None, 5, None, None, 1],
    [None, None, 1, 8, None, 6, 4, None, None],
    [None, None, 8, 1, None, 2, 9, None, None],
    [7, None, None, None, None, None, None, None, 8],
    [None, None, 6, 7, None, 8, 2, None, None],
    [None, None, 2, 6, None, 9, 5, None, None],
    [8, None, None, 2, None, 3, None, None, 9],
    [None, None, 5, None, 1, None, 3, None, None]
]


"""
I have tested only this module because they use same exact functions and it's easier to do on functions alone
instead of creating a ton of objets and dealing with changing state.

Between iterations we need to pass a Sudoku board alongside with item that we just inserted and it's position.

Algorithm:
    1. We pick a tree root.
    2. We check if it's worth further inspection. If not return None
    3. We check if we didn't already finish. If we did we return said solution.
    4. We repeat the same for all children.

"""


Sudoku = list[list[Optional[int]]]


SUDOKU_SIZE = 9
BOX_SIZE = int(SUDOKU_SIZE // 3)


class Position(NamedTuple):
    """Simple data structure to make operations on indexes more convenient."""
    row: int
    col: int

    @property
    def flattened_index(self) -> int:
        """Mapping of 2 coordinate index into it's counter part from single dimensional list."""
        return self.row * SUDOKU_SIZE + self.col

    @classmethod
    def from_flattened_index(cls, index: int) -> Position:
        """Create instance by extracting 2d index information from a single dimensional index."""
        return Position(index // SUDOKU_SIZE, index % SUDOKU_SIZE)


class Node(NamedTuple):
    state: Sudoku
    value: int
    pos: Position


def row_valid(node: Node) -> bool:
    """Determine if a current node's state is valid with regard to a row in which it is positioned."""
    return node.state[node.pos.row].count(node.value) <= 1


def col_valid(node: Node) -> bool:
    """Determine if a current node's state is valid with regard to a column in which it is positioned."""
    return [node.state[i][node.pos.col] for i in range(len(node.state))].count(node.value) <= 1


def box_valid(node: Node) -> bool:
    """Determine if a current node's state is valid with regard to neighbouring items (within inner box)."""
    box_row, box_col = ((elem // BOX_SIZE) * BOX_SIZE for elem in node.pos)
    box = []
    for row in node.state[box_row: box_row + BOX_SIZE]:
        box.extend(row[box_col: box_col + BOX_SIZE])
    return box.count(node.value) <= 1


def child_nodes(node: Node) -> Iterable[Node]:
    next_pos = next_index(node.state, node.pos.flattened_index)
    for n in range(1, 10):
        state_copy = deepcopy(node.state)
        state_copy[next_pos.row][next_pos.col] = n
        yield Node(state_copy, n, next_pos)


def next_index(sudoku: Sudoku, start_index: int = 0) -> Position:
    """Find the nearest free spot on sudoku board."""
    return Position.from_flattened_index(
        list(it.chain.from_iterable(sudoku)).index(None, start_index))


def reject(node: Node) -> bool:
    """Determine if current node contradicts sudoku rules."""
    return not (row_valid(node) and col_valid(node) and box_valid(node))


def accept(node: Node) -> bool:
    """Determine if current node is a sudoku solution."""
    return all(None not in row for row in node.state)


def solve(sudoku: Sudoku) -> Sudoku:
    """Solve sudoku specified using backtracking search algorithm."""

    def wrapper(root: Node) -> Optional[Node]:
        if reject(root):
            return None
        if accept(root):
            return root
        for child in child_nodes(root):
            res = wrapper(child)
            if res is not None:
                return res
        return None

    result = wrapper(Node(sudoku, 0, next_index(sudoku)))
    return result.state if result is not None else None


def pretty_print(sudoku: Sudoku) -> str:
    """Format sudoku board so it looks better."""
    str_buffer = []
    max_dig = len(str(SUDOKU_SIZE)) + 1
    for row_index, row in enumerate(sudoku):
        for col_index, cell in enumerate(row):
            if col_index and col_index % BOX_SIZE == 0:
                str_buffer.append("| ")
            if row_index and row_index % BOX_SIZE == 0 and col_index == 0:
                line_sep = "|".join(["-" * ((max_dig * 3) + 1)] * BOX_SIZE)[1:]
                str_buffer.append(f"\n{line_sep}")
            if row_index and col_index % SUDOKU_SIZE == 0:
                str_buffer.append("\n")
            if cell is None:
                str_buffer.append("__".ljust(max_dig, " "))
            else:
                str_buffer.append(f"{cell}".ljust(max_dig, " "))
    return "".join(str_buffer)


def main():
    print(pretty_print(solve(EXAMPLE_SUDOKU)))


if __name__ == '__main__':
    main()