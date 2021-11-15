#!/usr/bin/python
# -*- coding: utf-8 -*-

import abc
import re
import itertools
from enum import (Enum, auto)
from typing import (Iterable, Callable, Any, ParamSpec)
from collections import OrderedDict


class OrderingTags(Enum):
    DECORATORS = auto(),
    FUNCTION_SEQUENCE = auto()


_T = ParamSpec("_T")


class CallOrderVaiolationException(Exception):
    def __init__(self, msg: str, *args):
        super().__init__(*args)
        self.msg = msg

    def __str__(self):
        return self.msg


class EMO:
    """
    Enforce Method calling Ordering (coolness of name forced me to omit C in acronym).

    Wrapper class that allows to enforce method call order.
    Class will provide decorators to signal ordering of methods via dynamic attribute creation.
    e.g:

    @EMO()
    class Foo():

        @enforce_method_call_order.call_1()
        def first(): ...

        @enforce_method_call_order.call_2()
        def second(): ...

        ...

    As of now for this to succeed decorator needs to match to the following REGEX:
    /call_?([1-9]\d*|last)/

    where as name implies @enforce_method_call_order.call_last() will execute at the end.
    """

    def __init__(self, ordered_functions: Iterable[Callable[..., Any]] = None):
        self.__call_registry = OrderedDict()
        if ordered_functions is None:
            raise NotImplementedError
            # try looking for decorators
            # these should acctually be aleady defined.
        else:
            for func in ordered_functions:
                self.__call_registry[func.__name__] = False

    def __call__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        return self

    def dynamically_create_decorators(self):
        raise NotImplementedError

    def __getattr__(self, item):
        print("__getattr__ called!")

    def __getattribute__(self, item) -> Callable[..., _T]:
        print("__getattribute__ called!")

        regex = r"call_?([1-9]\d*|last)"

        if re.match(regex, item):
            try:
                sequence_num = int(str(filter(str.isnumeric, item)))
                sequence_name = str(filter(str.isalpha, item))
                # Dynamically add wrapper with name provided:

                def ordering_wrapper(func: Callable[..., _T]) -> Callable[..., _T]:
                    ordering_wrapper.__name__ = "_".join((sequence_name, sequence_num))

                    def wrapper(*args, **kwargs):
                        is_callable = self.__call_registry[func.__name__]
                        if is_callable:
                            func(*args, **kwargs)
                        else:
                            raise CallOrderVaiolationException(
                                f"Function {func.__name__} violated calling order."
                                f"Before calling {func.__name__} you first need to call:\n"
                                "\n\t- ".join(
                                    itertools.takewhile(
                                        lambda fname: fname != func.__name__,
                                        self.__call_registry.keys())))

                    return wrapper
                return ordering_wrapper
            except ValueError():
                raise AttributeError(f"Invalid decorator name. No number specified: {name}.")
        else:
            raise AttributeError(f"Invalid decorator name. Name {name} does not match with regex: {regex}.")


@EMO
class Foo:
    def __init__(self, x):
        self.x = x

    @EMO.call_1
    def bar(self): ...

    @EMO.call_2
    def han(self): ...

    @EMO.call_3
    def solo(self): ...


def main():
    foo = Foo(1)
    for name, inst in foo.__class__.__dict__.items():
        if callable(inst):
            print(name)


if __name__ == "__main__":
    main()
