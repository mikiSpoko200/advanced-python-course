# -*- encoding: utf-8 -*-

from __future__ import annotations

import sys
import inspect
from typing import Callable, Iterable, get_type_hints, ParamSpec, Union
from abc import ABC, abstractmethod

"""
Idea:
    Create a class Derive that contains superclasses which when derived from provide default
    implementation for certain methods e.g.
        - Format would provide unified formatting style,
        - PartialEq would provide default __eq__ and __nq__ method implementations
        ... and so on.

    This mechanism is inspired by rust's #[Derive(..)] attributes

    Desired syntax:
        class Foo(Derive.Format)
            ...

    NOTE: it's essential that subclasses must not be allowed to override methods supplied by
    these 'traits'.
    ---> implement __subclass_hook__ method!
IT WORKS!

Idea:
    Create dynamically generated classes for value types.
    Each Value supports operations (for now) only on it's own type
    raises error TypeError e.g. TypeError: unsupported operand type(s) for +: 'int' and 'Foo'

"""


class Derive:
    """Class that provides meta-functions that automatically implement certain dunder methods."""
    @staticmethod
    class Format:
        def __init_subclass__(cls, **kwargs):
            super().__init_subclass__(**kwargs)

            def default_format(self) -> str:
                str_builder = [str(getattr(self, attr)) for attr in vars(self)]
                return f"{cls.__name__}({', '.join(str_builder)})"

            cls.__str__ = default_format
            return cls


class Value(ABC):
    @abstractmethod
    def __init__(self, arg: Union[int, float, str, bool, Callable, Iterable]) -> None:
        pass

    @abstractmethod
    def __add__(self, rhs: Value) -> Value:
        pass

    @abstractmethod
    def __sub__(self, rhs: Value) -> Value:
        pass

    @abstractmethod
    def __mul__(self, rhs: Value) -> Value:
        pass

    @abstractmethod
    def __truediv__(self, rhs: Value) -> Value:
        pass


def register_class(cls: type):
    current_module = sys.modules[__name__]
    current_module.__dict__[cls.__name__] = cls


def register_primitive_types() -> None:

    primitives = [("IntValue", int), ("FloatValue", float), ("BoolValue", bool),
                  ("StringValue", str), ("ClosureValue", Callable), ("IteratorValue", Iterable)]
    atithmetic_primitives = [("IntValue", int), ("FloatValue", float)]
    for ValName, ValType in atithmetic_primitives:

        def _(self, value: ValType) -> None:
            self.__name__ = "__init__"
            if not isinstance(value, ValType):
                raise ValueError(f"{ValName}: Incorrect type of value in __init__ -- expected {ValType} got {type(value)}")
            self.value = value
        init = _
        # If object initialization succeeded than its save to perform arithmetic operations.

        basic_arithmetic_func_names = ["__add__", "__sub__", "__mul__", "__truediv__"]
        basic_arithmetic_func_impl = []
        for name in basic_arithmetic_func_names:
            def _(self, rhs: ValType):
                if not isinstance(rhs, ValType):
                    raise ValueError(f"Incorrect type of value rhs in {name} -- expected {ValType} got {type(rhs)}")
                return ValType(getattr(name, self.value)(rhs.value))
            basic_arithmetic_func_impl.append(_)

        primitive_namespace = {name: impl for name, impl in
                               zip(basic_arithmetic_func_names, basic_arithmetic_func_impl)}
        primitive_namespace["__init__"] = init

        register_class(type(ValName, (Value, Derive.Format), primitive_namespace))


register_primitive_types()


_T = ParamSpec("_T")


def assert_type_check(func: Callable[..., _T]) -> Callable[..., _T]:
    """Runtime type check. """
    signature = inspect.signature(func)
    params = get_type_hints(func)
    del params['return']
    for param, param_type in params.items():
        assert isinstance(param, signature.parameters[param].annotation), \
            f"TypeCheck assertion error -- param {param} of function {func.__name__} has type {'FILL ME'} expected {'FILL ME'}"

    return lambda: print("Hello World!")


def main():
    iv1 = FloatValue(1.0)
    iv2 = FloatValue(2.0)
    print(iv2 + iv1)


if __name__ == "__main__":
    main()
