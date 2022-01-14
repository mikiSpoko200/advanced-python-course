import unittest
from sheet05.src.expressions import *
from sheet05.src.primitives import IntValue


class TestDerivative(unittest.TestCase):

    def test_const(self):
        """Derivation variable cannot be inferred, so we expect a DerivationError."""
        self.assertRaises(
            LangDerivationError,
            lambda: ArithmeticExpression.derivative(Constant(IntValue(1))),
            "No DerivationError raised when derivation variable was ambiguous."
        )

    def test_variable_infer(self):
        """Test if derivation variable works as intended"""
        exprs = [Variable(var) for var in "abcdefgh"]
        for var in exprs:
            self.assertEqual(
                ArithmeticExpression.derivative(var),
                Constant(IntValue(1)),
                "Derivation variable incorrectly inferred."
            )

    def test_add(self):
        """Test derivation for addition with one variable."""
        expr = Variable("x") + Constant(IntValue(1))
        self.assertEqual(
            ArithmeticExpression.derivative(expr),
            Constant(IntValue(1)) + Constant(IntValue(0)),
            "Derivation with derivation variable inference failed for addition."
        )

    def test_subtract(self):
        """Test derivation for subtraction with one variable."""
        expr = Variable("x") - Constant(IntValue(1))
        self.assertEqual(
            ArithmeticExpression.derivative(expr),
            Constant(IntValue(1)) - Constant(IntValue(0)),
            "Derivation with derivation variable inference failed for subtraction."
        )

    def test_times(self):
        """Test derivation for multiplication with one variable."""
        expr = Variable("y") * Constant(IntValue(42))
        self.assertEqual(
            ArithmeticExpression.derivative(expr),
            Constant(IntValue(1)) * Constant(IntValue(42)) + Constant(IntValue(0)) * Variable("y"),
            "Derivation with derivation variable inference failed for multiplication."
        )

    def test_divide(self):
        """Test derivation for division with one variable."""
        expr = Variable("y") / Constant(IntValue(42))
        self.assertEqual(
            ArithmeticExpression.derivative(expr),
            (Constant(IntValue(1)) * Constant(IntValue(42)) - Constant(IntValue(0)) * Variable("y"))
            / (Constant(IntValue(42)) * Constant(IntValue(42))),
            "Derivation with derivation variable inference failed for Division."
        )

    def test_const_with_var(self):
        """No DerivationError because we specify the var."""
        exprs = [Constant(IntValue(i)) for i in range(-50, 50)]
        some_var = Variable("z")
        for const in exprs:
            self.assertEqual(
                ArithmeticExpression.derivative(const, some_var),
                Constant(IntValue(0)),
                "Derivation for a specified variable failed on a const value."
            )


if __name__ == '__main__':
    unittest.main()
