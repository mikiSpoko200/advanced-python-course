#!/usr/bin/python
# -*- coding: utf-8 -*-


import functools
from typing import Iterable
from decimal import Decimal


""" 
========================    Introduction:    ========================

Abstract:
    This module and script contained within it briefly discuss the numerical properties of floating point arithmetic
    in python <=3.10.

Modules contents:
    This module contains two classes. They provide functions that calculate VAT on invoices and receipts.
    Only difference between them is algebraic type used in computations.
    
float vs Decimal:
    Fist set (class FloatBased) uses float datatype which in python correspond to 
    IEEE-754 double precision 64 bit floating point numbers.
    Due to it being machine type thus having limited size in memory, this format is not numerically exact.
    Though in most cases float is exact enough since the relative error is 14 orders of magnitude lower 
    than the actual value.
    
    Other set uses Decimal type which is python's implementation of IBM's General Decimal 
    Arithmetic Specification Standard. 
    This is a complex datatype not a machine type primitive. Thus it's not going to receive the same hardware support
    as float which has dedicated arithmetic circuits within CPU. This makes Decimal significantly slower and requires 
    allocation of more memory. 
    All these disadvantages are a tradeoff that sacrifice raw efficiency for numerical correctness.
    Decimal standard was designed with simple philosophy in mind.
    Namely it should work just as math in primary school did.
    
Conclusion:
    In most cases we usually don't desire absolute mathematical precision. 
    Several orders of magnitude of accuracy are, in most cases, plenty enough.
    However, if we must ensure that no information is lost we should use Decimal type instead.


========================    Practical demonstration:    ========================  
    
Hypothesis:
    Due to accumulation of representation errors we should refrain from using floating point numbers
    in long summations which results must be exact.
"""


class FloatBased:
    """Class for namespacing purposes."""

    TAX_RATE = 0.23

    @staticmethod
    def vat_invoice(prices: Iterable[float]) -> float:
        """Calculate VAT tax on aggregated prices. Use type float for calculations."""
        return sum(prices) * FloatBased.TAX_RATE

    @staticmethod
    def vat_receipt(prices: Iterable[float]) -> float:
        """Aggregate VAT tax calculated on per product basis. Use type float for calculations."""
        return functools.reduce(lambda acc, p: acc + p * FloatBased.TAX_RATE, prices, 0.0)


class DecimalBased:
    """Class for namespacing purposes."""

    TAX_RATE = Decimal("0.23")

    @staticmethod
    def vat_invoice(prices: Iterable[Decimal]) -> Decimal:
        """Calculate VAT tax on aggregated prices. Use type Decimal for calculations."""
        return sum(prices) * DecimalBased.TAX_RATE

    @staticmethod
    def vat_receipt(prices: Iterable[Decimal]) -> Decimal:
        """Aggregate VAT tax calculated on per product basis. Use type Decimal for calculations."""
        return functools.reduce(lambda acc, p: acc + p * DecimalBased.TAX_RATE, prices, Decimal(0))


def main():
    prices_f64 = [0.2, 0.5, 4.59, 6] * 10000
    prices_Dec = [Decimal(str(num)) for num in prices_f64]

    float_r = FloatBased.vat_receipt(prices_f64)
    float_i = FloatBased.vat_invoice(prices_f64)
    decimal_i = DecimalBased.vat_invoice(prices_Dec)
    decimal_r = DecimalBased.vat_receipt(prices_Dec)
    print("Numerical correctness test:")
    print("FloatBased:")
    print(f"\tvat_invoice = {float_i}")
    print(f"\tvat_receipt = {float_r}")
    print(f"Result comparison: vat_invoice == vat_receipt = {float_i == float_r}")
    print("DecimalBased:")
    print(f"\tvat_invoice = {decimal_i}")
    print(f"\tvat_receipt = {decimal_r}")
    print(f"Result comparison: vat_invoice == vat_receipt = {decimal_i == decimal_r}")
    print()
    print("Execution time test:")
    print("FloatBased:")
    print("\tvat_invoice = {:.3f}s".format(
        timeit("float_wrapper_r()", setup="from __main__ import float_wrapper_r", number=10000)))
    print("\tvat_receipt = {:.3f}s".format(
        timeit("float_wrapper_i()", setup="from __main__ import float_wrapper_i", number=10000)), end='')
    print("   <--- whoa look at that C implemented functools.reduce *-*")
    print("DecimalBased:")
    print("\tvat_invoice = {:.3f}s".format(
        timeit("Decimal_wrapper_r()", setup="from __main__ import Decimal_wrapper_r", number=10000)))
    print("\tvat_receipt = {:.3f}s".format(
        timeit("Decimal_wrapper_i()", setup="from __main__ import Decimal_wrapper_i", number=10000)))


def float_wrapper_r():
    prices_f64 = [0.2, 0.5, 4.59, 6] * 100
    FloatBased.vat_receipt(prices_f64)


def float_wrapper_i():
    prices_f64 = [0.2, 0.5, 4.59, 6] * 100
    FloatBased.vat_invoice(prices_f64)


"""
Here is why Decimal(str(float)) works: https://docs.python.org/3/tutorial/floatingpoint.html
> Just remember, even though the printed result looks like the exact value of 1/10, 
> the actual stored value is the nearest representable binary fraction.
> 
> Interestingly, there are many different decimal numbers that share the same nearest approximate binary fraction. 
> For example, the numbers 0.1 and 0.10000000000000001 and 0.1000000000000000055511151231257827021181583404541015625 
> are all approximated by 3602879701896397 / 2 ** 55. Since all of these decimal values share the same approximation, 
> any one of them could be displayed while still preserving the invariant eval(repr(x)) == x.

> Historically, the Python prompt and built-in repr() function would choose the one with 17 significant digits, 
> 0.10000000000000001. Starting with Python 3.1, 
> Python (on most systems) is now able to choose the shortest of these and simply display 0.1.
"""

def Decimal_wrapper_r():
    prices_f64 = [0.2, 0.5, 4.59, 6] * 100
    prices_Dec = [Decimal(str(num)) for num in prices_f64]
    DecimalBased.vat_invoice(prices_Dec)


def Decimal_wrapper_i():
    prices_f64 = [0.2, 0.5, 4.59, 6] * 100
    prices_Dec = [Decimal(str(num)) for num in prices_f64]
    DecimalBased.vat_receipt(prices_Dec)


if __name__ == "__main__":
    from timeit import timeit
    main()


"""
Experiment results:
    As we can see due to repeated multiplication in FloatBased.vat_receipt function we lost some information
    and ended up with different results which should be equal.
    This wasn't an issue in case of implementation based on Decimal type.
    Another thing that we can notice it execution time difference. 
    Float based implementations clocked as 5 times the speed of Decimal based implementation.
    
Conclusion:
    Our theoretical assumptions turned out to be correct. 
    Float -> less precision, faster execution
    Decimal -> Mathematical precision, mediocre performance
"""


"""
My little side quest:

    I really enjoy exercises so simple as this one. Time saved on not having to implement some tricky algorithm can be
    spend otherwise. In this case, me being huge type annotation fan, I thought that it would be really cool to allow 
    our VAT calculating functions to accept and return any arbitrary object that supports addition and multiplication. 

    In hindsight maybe this wasn't the best idea. Simply because you don't really need that broad 
    argument type range for VAT calculating function but the information I obtained is definitely more than interesting.
    And I'm sure I'll make extensive use of 

    First thing that came to my mind was a generic function with type constraint that forces the type to implement
    certain behaviour. This can be done in C# with following syntax:

    class Foo<T> where T : constraint1, constraint2, ...

    And then I discovered Protocols from typing module. Introduced in python version 3.8 accepted in PEP544
    doc: https://www.python.org/dev/peps/pep-0544/ these bad boys implement what documentation refers to as 
    structural subtyping. Which is basically statically verifiable duck typing and I think that's pretty sick.
    It's very similar to ordinary interface implementation known from C++/C#/Rust (called nominal subtyping) though it
    works in "other direction". Normally we would say that because object implements certain interface we can assume 
    that is exhibits certain behaviour, but it's very explicit and thus as documentation claims not very pythonic*.
    That's where Protocols embrace duck typing.
    Protocols allow us to define certain common behaviour and than IF object implements this behaviour then
    the object is considered compatible with this Protocol. No explicit inheritance from a abstract base class needed.

    typing module itself defines several very common Protocols like Iterable (__next__() needed) 

    *My thoughts on unpythonicness of explicit interface implementation:
    I don't really get why explicit interface implementation would be less pythonic than implicit adherence
    to a Protocol; especially that line 2 of "zen of python" states "Explicit is better than implicit".
    Perhaps it's because structural subtyping was created from what I gathered, with typecheckers in mind.
"""