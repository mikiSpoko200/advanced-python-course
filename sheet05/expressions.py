from __future__ import annotations

from typing import get_args, Union
from traits import Derive
from abc import ABC, abstractmethod
from primitives import ArithmeticValue, Value, IntValue

# ===========================================
# #####           Expressions           #####
# ===========================================


class Expression(ABC, Derive.Hash):
    """Abstract base class for all expressions."""

    @abstractmethod
    def evaluate(self, environment: Environment) -> ArithmeticValue:
        """Evaluate self."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Return nicely formatted formula."""
        pass

    # def __repr__(self) -> str:
    #     return str(self)

    def __add__(self, rhs: Expression) -> Expression:
        return Add(self, rhs)

    def __mul__(self, rhs) -> Expression:
        return Times(self, rhs)


class Variable(Expression, Derive.PartialEq, Derive.Hash):
    def __init__(self, name: str) -> None:
        self.name = name

    def evaluate(self, environment: Environment) -> Value:
        return environment[self]

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name


class Environment:
    """Lookup used for variable evaluation."""

    def __init__(self, /, entries: dict[Variable, ArithmeticValue]):
        self.lookup = entries

    def __getitem__(self, variable: Variable) -> ArithmeticValue:
        return self.lookup[variable]

    def __setitem__(self, variable: Variable, value: ArithmeticValue):
        self.lookup[variable] = value

    def __delitem__(self, variable: Variable) -> None:
        del self.lookup[variable]

    def __contains__(self, item: Variable) -> bool:
        return item in self.lookup

    def __str__(self) -> str:
        return f"Environment({str(self.lookup)[1:-1]})"


class Constant(Expression):

    def __init__(self, value: ArithmeticValue):
        self.value = value

    def evaluate(self, environment: Environment) -> ArithmeticValue:
        return self.value

    def __str__(self) -> str:
        return str(self.value)


AtomicExpression = Union[Constant, Variable]


class Add(Expression):
    """Program evaluation tree node that represents sum of two other expressions."""
    def __init__(self, lhs: Expression, rhs: Expression) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def evaluate(self, environment: Environment) -> ArithmeticValue:
        return self.lhs.evaluate(environment) + self.rhs.evaluate(environment)

    def __str__(self) -> str:
        return " + ".join(_parenthesise(self.lhs, self, self.rhs))


class Times(Expression):
    """Program evaluation tree node that represents product of two other expressions."""

    def __init__(self, lhs: Expression, rhs: Expression):
        self.lhs = lhs
        self.rhs = rhs

    def evaluate(self, environment: Environment) -> ArithmeticValue:
        return self.lhs.evaluate(environment) * self.rhs.evaluate(environment)

    def __str__(self) -> str:
        return " * ".join(_parenthesise(self.lhs, self, self.rhs))


# Non Atomic Expression - an expression that contains two subtrees.
CompositeExpression = Union[Add, Times]


OPERATOR_PRECEDENCE: dict[type, int] = {Times: 3, Add: 2, Variable: 1, Constant: 1}


def _parenthesise(lhs: Expression, self: CompositeExpression, rhs: Expression) -> tuple[str, str]:
    """Helper function. Determine which, if any, sides of expression require parenthesis while converting to str."""

    # filter Atomic nodes -- i.e. ones that cont have any child nodes.
    # They don't need parenthesis.,
    root_prec = OPERATOR_PRECEDENCE[type(self)]
    str_builder = []
    for sub_expr in [lhs, rhs]:
        # An expression needs to be parenthesised if it has a:
        #   - sub expression
        #   - lower priority that current root expression:
        if isinstance(sub_expr, get_args(CompositeExpression)) and OPERATOR_PRECEDENCE[type(sub_expr)] < root_prec:
            str_builder.append(f"({sub_expr})")
        else:
            str_builder.append(str(sub_expr))

    par_lhs, par_rhs = str_builder
    return par_lhs, par_rhs


def main():
    expr = Times(Add(Variable("x"), Constant(IntValue(2))), Variable("y"))
    example_env = Environment({Variable("x"): IntValue(1), Variable("y"): IntValue(3)})
    print("Evaluation environment:", example_env)
    print("Expression:", expr)
    print(f"Expression evaluation: {expr.evaluate(example_env)}")


if __name__ == "__main__":
    main()
