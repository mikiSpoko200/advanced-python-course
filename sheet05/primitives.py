from __future__ import annotations

from typing import Union, Callable, Iterable, Any
from abc import ABC, abstractmethod
from enum import Enum, auto
from traits import Derive
from exceptions import LangZeroDivisionError


"""
                            #============================================#
                            ######    Primitive types and values    ######
                            #============================================#

This file contains primitive values and types.
    As of now -- 18:19 19.11 -- only Arithmetic types needed for ex1c are implemented,
    but im looking forward to adding more in my own spare time then I also will document
    them more thoroughly.
    
    Why does this module even exist?
        Well I could've simply used python default primitive types instead of creating these 
        wrappers but that way I wouldn't learn anything more about how languages work.
        Such distinction creates some abstract idea of value which is a result of evaluation.
        Creating a public interface for values allows me for much higher flexibility.
   
   ABCs:
    = Value             -- an abstract base class that defines what a value is and what are minimal
                           requirements for an object to be considered a value.
                           I decided that my language will be statically and strongly typed.
                           I thought that it might be easier to implement that way.
    = ArithmeticValue   -- an abstract base class that defines minimal functionality for objects
                           that want to support basic arithmetic operations.
    
    - Type          -- Enumeration that contains all basic types.
    - IntValue      -- a value that represents an integer.
    - FloatValue    -- a value that represents a floating point number.
"""


_wrapped_type = Union[int, float, str, bool, Callable[..., Any], Iterable[Any]]


class Type(Enum):
    IntType = auto()
    FloatType = auto()
    StringType = auto()
    BoolType = auto()
    ClosureType = auto()
    IteratorType = auto()
    
    
class TypeCheckError(Exception):
    """Exception raised when code type-check fails."""
    def __init__(self, received_type: _wrapped_type, expected_type: type, msg: str) -> None:
        super().__init__(msg)
        self.received_type = received_type
        self.expected_type = expected_type


def type_check(value: Any, expected_type: type) -> None:
    if not isinstance(value, expected_type):
        received_type = type(value)
        raise TypeCheckError(received_type, expected_type,
                             f"Incorrect type of value -- expected {expected_type} got {received_type}")


class Value(ABC, Derive.PartialEq):
    """Abstract base class for all Values."""
    def __init__(self, value: Union[int, float, str, bool, Callable, Iterable], value_type: Type) -> None:
        self._value = value
        self._value_type = value_type

    def __str__(self) -> str:
        """Return the representation of a Value."""
        return str(self._value)

    def __repr__(self) -> str:
        """Return the representation of a Value. Useful for printing collections."""
        return str(self._value)

    @property
    def type(self) -> Type:
        return self._value_type


class ArithmeticValue(Value):
    """Abstract base class for all values that should support arithmetic operations."""
    @abstractmethod
    def __add__(self, rhs: ArithmeticValue) -> ArithmeticValue:
        """Overload of + operator."""
        pass

    @abstractmethod
    def __mul__(self, rhs: ArithmeticValue) -> ArithmeticValue:
        """Overload of * operator."""
        pass

    @abstractmethod
    def __sub__(self, rhs: ArithmeticValue) -> ArithmeticValue:
        """Overload of - operator."""
        pass

    @abstractmethod
    def __truediv__(self, other: ArithmeticValue) -> ArithmeticValue:
        """Overload of / operator."""
        pass


class IntValue(ArithmeticValue):
    """Value that represents an integer."""
    def __init__(self, value: int) -> None:
        type_check(value, int)
        super().__init__(value, Type.IntType)

    def __add__(self, rhs: IntValue) -> IntValue:
        type_check(rhs, IntValue)
        return IntValue(self._value + rhs._value)

    def __mul__(self, rhs: IntValue) -> IntValue:
        type_check(rhs, IntValue)
        return IntValue(self._value * rhs._value)

    def __sub__(self, rhs: IntValue) -> IntValue:
        type_check(rhs, IntValue)
        return IntValue(self._value - rhs._value)

    def __truediv__(self, rhs: IntValue) -> IntValue:
        type_check(rhs, IntValue)
        try:
            return IntValue(self._value // rhs._value)
        except ZeroDivisionError as err:
            raise LangZeroDivisionError(f"Attempted zero division.") from err


class FloatValue(ArithmeticValue):
    """Value that represents a floating precision number."""
    def __init__(self, value: float) -> None:
        type_check(value, float)
        super().__init__(value, Type.FloatType)

    def __add__(self, rhs: FloatValue) -> FloatValue:
        type_check(rhs, FloatValue)
        return FloatValue(self._value + rhs._value)

    def __mul__(self, rhs: FloatValue) -> FloatValue:
        type_check(rhs, FloatValue)
        return FloatValue(self._value * rhs._value)

    def __sub__(self, rhs: FloatValue) -> FloatValue:
        type_check(rhs, FloatValue)
        return FloatValue(self._value - rhs._value)

    def __truediv__(self, rhs: FloatValue) -> FloatValue:
        type_check(rhs, FloatValue)
        return FloatValue(self._value // rhs._value)


# TODO: implement me!
class StringValue:
    def __init__(self, value: str) -> None:
        raise NotImplementedError


# TODO: implement me!
class BoolValue:
    def __init__(self, value: bool) -> None:
        raise NotImplementedError


# TODO: implement me!
class ClosureValue:
    def __init__(self, value: Callable[..., Any]) -> None:
        raise NotImplementedError


# TODO: implement me!
class IteratorValue:
    def __init__(self, value: int) -> None:
        raise NotImplementedError


def main():
    print("Hello primitives!")


if __name__ == '__main__':
    main()
