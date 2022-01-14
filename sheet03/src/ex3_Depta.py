# -*- encoding: utf-8 -*-

import itertools as it
import math
from collections import Counter
from typing import Iterable


PrimeFactorization = Iterable[tuple[int, int]]


def prime_sieve(n) -> Iterable[int]:
    """Functional implementation of prime sieve."""
    if n <= 2:
        return []
    return filter(lambda number: all(number % div != 0 for div in range(3, int(math.ceil(number ** 0.5)) + 1, 2)),
                  it.chain([2], range(3, n, 2)))


class PrimeFactor:
    """Provides different implementations of prime factorization algorithm.
    All functions preform prime factorization of a number.
    Difference lies in the programing 'paradigm' used.
    1. Imperative
    2. Using list comprehensions
    3. Functional
    More thorough overview can be found in separate report.
    """

    @staticmethod
    def is_prime(n):
        """Primality test helper function."""
        for div in range(3, int(math.ceil(n ** 0.5)), 2):
            if n % div == 0:
                return False
        return True

    def __init__(self, n: int) -> None:
        self.n = n

    def factors_imperative_fast(self) -> PrimeFactorization:
        """Calculate prime factorization.
        This implementation is a bit faster
        """
        factors = []
        n = self.n
        for div in [2, *range(3, int(self.n ** 0.5) + 1, 2)]:
            # Exponential value decreasing.
            while n % div == 0:
                n /= div
                factors.append(div)
        if not factors:
            factors.append(self.n)
        return Counter(factors).most_common()

    def factors_imperative(self) -> PrimeFactorization:
        factors = []
        for number in range(2, int(self.n ** 0.5)):
            if PrimeFactor.is_prime(number):
                for exp in range(1, int(math.log(self.n, number)) + 1):
                    if

    def factors_comprehension(self) -> PrimeFactorization:
        """List comprehensions are not flexible enough to do this optimally due to missing
        while loop equivalent thus continuous n division until n % div != 0 is impossible to accomplish.
        Also it's very difficult to carry state information about changing n that is needed to avoid adding multiples
        of prime divisors.
        """
        n = self.n
        div_range = [2, *range(3, int(n ** 0.5) + 1, 2)]
        product = [(div, [exp for exp in range(1, int(math.log(n, div)) + 1) if n % div ** exp == 0])
                   for div in div_range]
        #product = [(div, exp) for div in product if]
        #factorization = [(div, exp) for index, (div, exp) in enumerate(product)
        #                 if not any([div % ediv == 0 for ediv, _ in product[:index] if ediv != div])]
        return product

    def factors_functional(self) -> PrimeFactorization:
        return


def main():
    factor = PrimeFactor(19)
    print(factor.factors_imperative())


main()