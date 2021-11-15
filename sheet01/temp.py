#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
from typing import Callable, Any, ParamSpec


_T = ParamSpec("_T")


def print_name_when_called(func: Callable[..., _T]) -> Callable[..., _T]:
    def wrapper(*args, **kwargs) -> _T:
        print(f"{func.__name__} called")
        func(*args, **kwargs)
    return wrapper


class Foo:
    #@print_name_when_called
    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs

    #@print_name_when_called
    def __call__(self, *args, **kwargs):
        print(args)


@Foo
class Bar:
    #@print_name_when_called
    def __init__(self, x, y):
        print(x, y)


def main():
    Bar(1, 2)


if __name__ == "__main__":
    main()
