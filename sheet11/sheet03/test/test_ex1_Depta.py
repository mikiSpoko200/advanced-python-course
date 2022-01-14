import unittest
from itertools import combinations


import sheet03.ex1_Depta as Ex


class TestEX1(unittest.TestCase):

    def setUp(self) -> None:
        self.ps = Ex.PrimeSieve(100)

    def test_is_prime(self):
        """Tests if prime check works correctly"""
        self.assertEqual(False, Ex.PrimeSieve.is_prime(1), "1 is not a prime number.")
        self.assertEqual(False, Ex.PrimeSieve.is_prime(0), "0 is not a prime number.")
        self.assertEqual(False, Ex.PrimeSieve.is_prime(-1), "No negative number is a prime number.")
        self.assertEqual(True, Ex.PrimeSieve.is_prime(2), "2 is a prime number.")
        self.assertEqual(True, Ex.PrimeSieve.is_prime(3), "3 is a prime number.")
        self.assertEqual(False, Ex.PrimeSieve.is_prime(4), "4 is not a prime number.")
        self.assertEqual(True, Ex.PrimeSieve.is_prime(13), "13 is a prime number.")

    def test_results(self):
        """Tests if all implementations yield same results."""
        funcs = self.ps.prime_imperative, self.ps.prime_comprehension, lambda: list(self.ps.prime_functional())
        labeled_functions = {func.__name__: func() for func in funcs}
        for (l1, v1), (l2, v2) in combinations(labeled_functions.items(), 2):
            self.assertEqual(v1, v2, f"functions {l1} and {l2} returned different results\n"
                                     f"{l1} -> {v1}\n"
                                     f"{l2} -> {v2}")

    def test_prime_func(self):
        """Checks correctness of a functional prime sieve implementation."""
        ps = Ex.PrimeSieve(10)
        self.assertEqual([2, 3, 5, 7], ps.prime_imperative(), "")
        ps.n = 20
        self.assertEqual([2, 3, 5, 7, 11, 13, 17, 19], ps.prime_imperative(),  "")
        ps.n = 30
        self.assertEqual([2, 3, 5, 7, 11, 13, 17, 19, 23, 29], ps.prime_imperative(), "")
