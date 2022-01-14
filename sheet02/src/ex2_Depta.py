#!/usr/bin/python
# -*- coding: utf-8 -*-


import math
from decimal import Decimal
from fractions import Fraction
from itertools import count
from typing import Callable, ParamSpec
from numbers import Real

_T = ParamSpec("T")


def arg_validator_numeric_real_nonnegative(func: Callable[..., _T]) -> Callable[..., _T]:
    """Argument validator wrapper."""
    def wrapper(*args) -> _T:
        for arg in args:
            if isinstance(arg, Real | Decimal):
                if arg >= 0:
                    return func(*args)
                else:
                    raise ValueError(f"invalid value. Expected non-negative received {arg}")
            else:
                raise TypeError(f"invalid argument type. Expected subtype of Real, received {type(arg)}")
    return wrapper


@arg_validator_numeric_real_nonnegative
def square_root(n: Real | Decimal) -> int:
    """Calculate floor of square root of n. Where n is non-negative real number.
    In numbers module Python defines a hierarchy of numeric abstract base classes.
    Hierarchy looks as follows: (uml style inheritance notation)
    Number <- Complex <- Real <- Rational <- Integral.
    Formula specified in the exercise works for all real numbers
    because we are only interested in the floor of the square.

    Unfortunately we cannot simply require type to be numbers. Real because Decimal,
    which works in with algorithm, does not subclass Real due to lack of interoperability with binary floats.
    from Decimal source file comments: (numbers.py)

    > Decimal has all of the methods specified by the Real abc, but it should
    > not be registered as a Real because decimals do not interoperate with
    > binary floats (i.e.  Decimal('3.14') + 2.71828 is undefined).  But,
    > abstract reals are expected to interoperate (i.e. R1 + R2 should be
    > expected to work if R1 and R2 are both Reals).
    """
    acc = 0
    for next_odd, k in zip(count(1, 2), count(1)):
        acc += next_odd
        if acc >= n:
            return k if acc == n else k - 1


def main():
    print("Beginning auto testing for n in range(10**5) ...")
    for n in range(0, 10**5):
        assert square_root(n) == math.floor(math.sqrt(n)), \
            f"square_root({n}) = {square_root(n)} != {math.floor(math.sqrt(n))}"
    print("All passed ok.")
    print("Testing for different input types:")
    print(f"{square_root(6) = }")
    print(f"{square_root(6.0) = }")
    print(f"{square_root(Fraction(32, 5)) = }")
    print(f"{square_root(Decimal('6')) = }")


if __name__ == "__main__":
    main()
