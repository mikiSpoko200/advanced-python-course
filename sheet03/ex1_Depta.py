# -*- coding: utf-8 -*-

import math
import timeit
import itertools as it
from typing import Iterable, Callable


class PrimeSieve:
    """Provides different implementations of prime sieve.
    All functions search for all prime number lower than n.
    Difference lies in the programing 'paradigm' used.
    1. Imperative
    2. Using list comprehensions
    3. Functional
    """

    @staticmethod
    def is_prime(n):
        """Primality test helper function."""
        for div in range(3, int(math.ceil(n ** 0.5)), 2):
            if n % div == 0:
                return False
        return True

    def __init__(self, n: int):
        self.n = n

    def prime_imperative(self) -> list[int]:
        """Imperative implementation of prime sieve."""
        if self.n <= 2:
            return []
        primes = []
        # little optimization: skip all even numbers as they are obviously not prime.
        for number in [2, *range(3, self.n, 2)]:
            if PrimeSieve.is_prime(number):
                primes.append(number)
        return primes

    def prime_comprehension(self) -> list[int]:
        """List comprehension based implementation of prime sieve.

        I've tried being very strict about list comprehension and at some point decided to modify this code as follows:

        [number for number in [2, *range(3, self.n, 2)]
                if all([self.n % div for div in range(3, int(math.ceil(self.n ** 0.5)), 2)])]

        # full list comprehension
        Time profiling prime_comprehension for big inputs...
            input: 1000, iterations: 200, time: 0.266s
            input: 2000, iterations: 100, time: 0.316s
            input: 3000, iterations: 50, time: 0.474s
            input: 4000, iterations: 20, time: 0.234s
            input: 5000, iterations: 20, time: 0.240s
            input: 6000, iterations: 20, time: 0.292s
            input: 7000, iterations: 20, time: 0.379s
            input: 8000, iterations: 10, time: 0.227s
            input: 9000, iterations: 10, time: 0.268s

        # call to is_prime
        Time profiling prime_comprehension for big inputs...
            input: 1000, iterations: 5000, time: 0.251s
            input: 2000, iterations: 5000, time: 0.540s
            input: 3000, iterations: 2000, time: 0.298s
            input: 4000, iterations: 1000, time: 0.200s
            input: 5000, iterations: 1000, time: 0.257s
            input: 6000, iterations: 1000, time: 0.307s
            input: 7000, iterations: 1000, time: 0.320s
            input: 8000, iterations: 500, time: 0.209s
            input: 9000, iterations: 500, time: 0.232s

        I was greatly surprised how performance tanked here so I switched back to less strict interpretation.
        """
        if self.n <= 2:
            return []
        return [number for number in [2, *range(3, self.n, 2)] if PrimeSieve.is_prime]

    def prime_functional(self) -> Iterable[int]:
        """Functional implementation of prime sieve.
        In my opinion this method should return Iterable instead of list.
        The reason would be the lazy evaluation which all functions from itertools provide
        as they return iterators which calculate and yield subsequent values on demand instead
        of eagerly computing the whole result like list comprehensions
        (which in my opinion is the main feature that distinguishes the two).
        Casting the filter object into the list would throw all that away.

        Also it's better in terms of flexibility of this class.
        If we return Iterable instead of list we give the end user ability to decide for themselves what
        data structure they prefer. Any iterable can be easily cast into the list. One could argue that the same
        is true for iterators when using generator expressions https://www.python.org/dev/peps/pep-0289/
        e.g. (number for number in list[...]).
        Yes we could obtain a iterable that way but the values that is would yield are already computed during list
        creation which is not the same as original lazy computation.
        """
        if self.n <= 2:
            return []
        return filter(PrimeSieve.is_prime, it.chain([2], range(3, self.n, 2)))


SETUP = "from __main__ import PrimeSieve\nps = PrimeSieve(%d)"


def profile_small_input_many_repetitions(func: Callable[[], None]) -> None:
    """Time profiling of func for small inputs."""
    print(f"Time profiling {func.__name__} for small inputs...")
    for n in [n * 10 for n in range(1, 10)]:
        stmt = f"ps.{func.__name__}()"
        timer = timeit.Timer(stmt, SETUP % n)
        iterations, time = timer.autorange()
        print(f"\tinput: {n}, iterations: {iterations}, time: {time:.3f}s")


def profile_big_input(func: Callable[[], None]) -> None:
    """Time profiling of func for big inputs."""
    print(f"Time profiling {func.__name__} for big inputs...")
    for n in [n * 1000 for n in range(1, 10)]:
        stmt = f"ps.{func.__name__}()"
        timer = timeit.Timer(stmt, SETUP % n)
        iterations, time = timer.autorange()
        print(f"\tinput: {n}, iterations: {iterations}, time: {time:.3f}s")


def main():
    for func in [PrimeSieve.prime_imperative, PrimeSieve.prime_comprehension, PrimeSieve.prime_functional]:
        profile_small_input_many_repetitions(func)
    for func in [PrimeSieve.prime_imperative, PrimeSieve.prime_comprehension, PrimeSieve.prime_functional]:
        profile_big_input(func)


if __name__ == '__main__':
    main()

"""
Testing methodology:
    Testing scripts where invoked from command line in order
    to reduce potential overhead produced by running IDE (I work in pycharm).
    I run tests using Python 3.10.0 and 3.9.10.
    results are stored in files named in the following convention:
    ex<number>-<python version>-<activation platform>.txt
    (wt stands for windows terminal).

Result summary:
    Test results are stored in ex1-3.9-wt.txt and ex1-3.10-wt.txt and the data appears to suggest that imperative 
    implementations are the slowest, on average list comprehensions are 10/20 times faster and functional
    implementation is just insanely fast clocking at about 500/750 times faster than list comprehensions.
    This applies for both small inputs and bigger ones. Python 3.9.10 seemed to be generally a bit faster 
    (approx. 1.2 times) than 3.10.0.
"""
