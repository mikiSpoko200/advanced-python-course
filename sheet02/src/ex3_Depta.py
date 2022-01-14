#!/usr/bin/python
# -*- coding: utf-8 -*-

from functools import cache


@cache
def sudan(n: int, x: int, y: int) -> int:
    if n == 0:
        return x + y
    if y == 0:
        return x


def main():
    print(sudan(1, 1, 1))


if __name__ == "__main__":
    main()
