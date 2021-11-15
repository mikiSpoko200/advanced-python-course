#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import annotations

import itertools as it
from typing import Iterable, Optional, NamedTuple, TypeVar, Iterator
from copy import deepcopy
from abc import ABC, abstractmethod


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


_T = TypeVar("_T")


class BacktrackMixin(ABC, Iterable):
    """Mixin providing backtracking behaviour."""

    def __init__(self, _state: list[_T]) -> None:
        self._state = _state

    @abstractmethod
    def reject(self) -> bool:
        """Determine if current partial candidate (self) is worth completing."""
        pass

    @abstractmethod
    def accept(self) -> bool:
        """Determine if current partial candidate (self) is a solution."""
        pass

    @abstractmethod
    def __iter__(self) -> Iterator[_T]:
        """Iterator for depth-first search tree traversal."""
        pass


class BacktrackingSearchNode(BacktrackMixin):
    """Backtracking search algorithm tree."""

    def __init__(self, state: Sudoku, value: int, pos: Position) -> None:
        super().__init__(state)
        self._value = value
        self._pos = pos

    @property
    def state(self) -> Sudoku:
        return self._state

    def row_valid(self) -> bool:
        """Determine if a current node's state is valid with regard to a row in which it is positioned."""
        return self._state[self._pos.row].count(self._value) <= 1
    
    def col_valid(self) -> bool:
        """Determine if a current node's state is valid with regard to a column in which it is positioned."""
        return [self._state[i][self._pos.col] for i in range(len(self._state))].count(self._value) <= 1
    
    def box_valid(self) -> bool:
        """Determine if a current node's state is valid with regard to neighbouring items (within inner box)."""
        box_row, box_col = ((elem // BOX_SIZE) * BOX_SIZE for elem in self._pos)
        box = []
        for row in self._state[box_row: box_row + BOX_SIZE]:
            box.extend(row[box_col: box_col + BOX_SIZE])
        return box.count(self._value) <= 1
    
    def reject(self) -> bool:
        """Determine if current node contradicts sudoku rules."""
        return not (self.row_valid() and self.col_valid() and self.box_valid())
    
    def accept(self) -> bool:
        """Determine if current node is a sudoku solution."""
        return all(None not in row for row in self._state)
    
    def __iter__(self) -> Iterable[BacktrackingSearchNode]:
        """Return Generator that yields sudoku states that can be obtained from current state."""
        next_pos = next_index(self._state, self._pos.flattened_index)
        for n in range(1, 10):
            state_copy = deepcopy(self._state)
            state_copy[next_pos.row][next_pos.col] = n
            yield BacktrackingSearchNode(state_copy, n, next_pos)


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


class SudokuSolver:
    """Wrapper class that provides convenient way of solving sudoku puzzle."""

    def __init__(self, board: Sudoku) -> None:
        self._board = board

    @classmethod
    def _from_lines(cls, lines: list[str]) -> SudokuSolver:
        board = []
        for line in lines:
            board.append([None if num == "0" else int(num) for num in line])
        return SudokuSolver(board)

    @classmethod
    def from_string(cls, str_repr: str) -> SudokuSolver:
        """Create SudokuSolver from a string representation."""
        return SudokuSolver._from_lines(str_repr.split())

    @classmethod
    def from_file(cls, file_name: str):
        with open(file_name, "r", encoding="utf-8") as raw_sudoku:
            return SudokuSolver._from_lines(raw_sudoku.readlines())

    @property
    def board(self) -> Sudoku:
        return self._board

    def __str__(self) -> str:
        """Format sudoku board so it looks better."""
        str_buffer = []
        for row_index, row in enumerate(self._board):
            for col_index, cell in enumerate(row):
                if col_index and col_index % BOX_SIZE == 0:
                    str_buffer.append("| ")
                if row_index and row_index % BOX_SIZE == 0 and col_index == 0:
                    line_sep = "|".join(["-" * ((2 * 3) + 1)] * BOX_SIZE)[1:]
                    str_buffer.append(f"\n{line_sep}")
                if row_index and col_index % SUDOKU_SIZE == 0:
                    str_buffer.append("\n")
                if cell is None:
                    str_buffer.append("_".ljust(2, " "))
                else:
                    str_buffer.append(f"{cell}".ljust(2, " "))
        return "".join(str_buffer)

    def solving_sudoku(self) -> None:
        """Solve sudoku in place specified using backtracking search algorithm."""

        def wrapper(root: BacktrackingSearchNode) -> Optional[BacktrackingSearchNode]:
            if root.reject():
                return None
            if root.accept():
                return root
            for child in root:
                res = wrapper(child)
                if res is not None:
                    return res
            return None

        result = wrapper(BacktrackingSearchNode(self._board, 0, next_index(self._board)))
        self._board = result.state if result is not None else None

    def animate(self) -> None:
        raise NotImplementedError


def next_index(sudoku: Sudoku, start_index: int = 0) -> Position:
    """Find the nearest free spot on sudoku board."""
    return Position.from_flattened_index(
        list(it.chain.from_iterable(sudoku)).index(None, start_index))


def main():
    # > Alongside this, implement another function that nicely
    # > draws a partially filled or a fully filled input diagram.
    # This functionality for programmed as __str__ method for SudokuSolver class.
    sudoku_solver = SudokuSolver(EXAMPLE_SUDOKU)
    print("Original sudoku:")
    print(sudoku_solver)
    sudoku_solver.solving_sudoku()
    print()
    print("Solved sudoku:")
    print(sudoku_solver)


if __name__ == "__main__":
    main()

