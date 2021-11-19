import unittest
from expressions import *
from primitives import IntValue


class TestDerivative(unittest.TestCase):

    def test_const(self):
        """Derivation variable cannot be inferred so we expect a DerivationError."""
        self.assertRaises(
            DerivationError,
            lambda: ArithmeticExpression.derivative(Constant(IntValue(1)))
        )

    def test_variable_infer(self):
        """In this case derivation variable should be inferred."""
        exprs = [Variable(var) for var in "abcdefgh"]
        for var in exprs:
            self.assertEqual(ArithmeticExpression.derivative(var), Constant(IntValue(1)))

    def test_add(self):
        expr = Add(Variable("x"), Constant(IntValue(1)))
        self.assertTrue(ArithmeticExpression.derivative(expr) == Add(Constant(IntValue(1)), Constant(IntValue(0))))

    def test_times(self):
        expr = Times(Variable("y"), Constant(IntValue(42)))
        self.assertEqual(
            ArithmeticExpression.derivative(expr),
            Times(
                Times(
                    Constant(IntValue(1)),
                    Constant(IntValue(42))
                    ),
                Times(
                    Constant(IntValue(0)),
                    Variable("y")
                )
            ))

    def test_const_with_var(self):
        """No DerivationError because we specify the var."""
        exprs = [Constant(IntValue(i)) for i in range(-50, 50)]
        some_var = Variable("z")
        for const in exprs:
            self.assertEqual(ArithmeticExpression.derivative(const, some_var), Constant(IntValue(0)))


if __name__ == '__main__':
    unittest.main()
