from __future__ import annotations

from typing import Union, Callable, Iterable, Any
from abc import ABC, abstractmethod
from enum import Enum, auto

# ===========================================
# #####    Primitive types and values   #####
# ===========================================


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


class Value(ABC):
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
        return IntValue(self._value // rhs._value)


class FloatValue(ArithmeticValue):
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
