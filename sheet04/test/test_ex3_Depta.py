#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import ex3_Depta_functional as Ex3


SUDOKU_STR = "003020600\n900305001\n001806400\n008102900\n700000008\n006708200\n002609500\n800203009\n005010300"


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

# I added +0 to indicate values that are meant to create errors.
INCORRECT_SUDOKU = [
    [3+0, None, 3+0, None, 2, None, 6, None, None],  # Note double 3 in this row and box
    [9, None, None, 3, None, 5, None, None, 1+0],
    [None, None, 1, 8, None, 6, 4, None, None],
    [None, None, 8, 1, None, 2, 9, None, None],
    [7, None, None, None, None, None, None, None, 8],
    [None, None, 6, 7, None, 8, 2, None, 1+0],  # Note double 1 in column
    [None, None, 2+0, 6, None, 9, 5, None, 2+0],  # Note double 2 in this row
    [8, None, 2+0, 2+0, None, 3, None, None, 9],  # Note double 2 in row, column and box
    [None, None, 5, None, 1, None, 3, None, None]
]

CORRECT_SUDOKU = [
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


class RowCheckTest(unittest.TestCase):

    def test_row_check_false1(self):
        self.assertFalse(
            Ex3.row_valid(Ex3.Node([[None, 1, None, 1, None, 6, 7, 8, 9]], 1, Ex3.Position(0, 0)))
        )

    def test_row_check_false2(self):
        self.assertFalse(
            Ex3.row_valid(Ex3.Node([[6, None, None, 1, None, 6, 7, 8, 9]], 6, Ex3.Position(0, 0)))
        )

    def test_row_check_true1(self):
        self.assertTrue(
            Ex3.row_valid(Ex3.Node([[None] * 9], 1, Ex3.Position(0, 0)))
        )

    def test_row_check_true2(self):
        self.assertTrue(
            Ex3.row_valid(Ex3.Node([[(num % 9) + 1 for num in range(1, 11) if num != 5]], 5, Ex3.Position(0, 0)))
        )


class ColCheckTest(unittest.TestCase):

    def test_col_check_true1(self):
        self.assertTrue(
            Ex3.col_valid(Ex3.Node(INCORRECT_SUDOKU, 2, Ex3.Position(0, 1)))
        )

    def test_col_check_true2(self):
        self.assertTrue(
            Ex3.col_valid(Ex3.Node(CORRECT_SUDOKU, 3, Ex3.Position(0, 0)))
        )

    def test_col_check_false1(self):
        self.assertFalse(
            Ex3.col_valid(Ex3.Node(INCORRECT_SUDOKU, 2, Ex3.Position(0, 2)))
        )

    def test_col_check_false2(self):
        self.assertFalse(
            Ex3.col_valid(Ex3.Node(INCORRECT_SUDOKU, 1, Ex3.Position(0, 8)))
        )


class BoxCheckTest(unittest.TestCase):

    def test_box_check_true1(self):
        self.assertTrue(
            Ex3.box_valid(Ex3.Node(CORRECT_SUDOKU, 2, Ex3.Position(0, 0)))
        )

    def test_box_check_true2(self):
        self.assertTrue(
            Ex3.box_valid(Ex3.Node(CORRECT_SUDOKU, 3, Ex3.Position(8, 1)))
        )

    def test_box_check_true3(self):
        self.assertTrue(
            Ex3.box_valid(Ex3.Node(CORRECT_SUDOKU, 4, Ex3.Position(4, 4)))
        )

    def test_box_check_true4(self):
        self.assertTrue(
            Ex3.box_valid(Ex3.Node(CORRECT_SUDOKU, 3, Ex3.Position(3, 8)))
        )

    def test_box_check_false1(self):
        self.assertFalse(
            Ex3.box_valid(Ex3.Node(INCORRECT_SUDOKU, 2, Ex3.Position(8, 0)))
        )

    def test_box_check_false2(self):
        self.assertFalse(
            Ex3.box_valid(Ex3.Node(INCORRECT_SUDOKU, 3, Ex3.Position(2, 1)))
        )


SOLUTION = [
    [4, 8, 3, 9, 2, 1, 6, 5, 7],
    [9, 6, 7, 3, 4, 5, 8, 2, 1],
    [2, 5, 1, 8, 7, 6, 4, 9, 3],
    [5, 4, 8, 1, 3, 2, 9, 7, 6],
    [7, 2, 9, 5, 6, 4, 1, 3, 8],
    [1, 3, 6, 7, 9, 8, 2, 4, 5],
    [3, 7, 2, 6, 8, 9, 5, 1, 4],
    [8, 1, 4, 2, 5, 3, 7, 6, 9],
    [6, 9, 5, 4, 1, 7, 3, 8, 2]
]


class AcceptTest(unittest.TestCase):

    def test_accept_true1(self):
        self.assertTrue(
            Ex3.accept(Ex3.Node([[1, 2]], 0, Ex3.Position(0, 0)))
        )

    def test_accept_true2(self):
        self.assertTrue(
            Ex3.accept(Ex3.Node(SOLUTION, 0, Ex3.Position(0, 0)))
        )

    def test_accept_false1(self):
        self.assertFalse(
            Ex3.accept(Ex3.Node(INCORRECT_SUDOKU, 0, Ex3.Position(0, 0)))
        )

    def test_accept_false2(self):
        self.assertFalse(
            Ex3.accept(Ex3.Node(CORRECT_SUDOKU, 0, Ex3.Position(0, 0)))
        )


if __name__ == '__main__':
    unittest.main()
