from __future__ import annotations

from typing import get_args, Union, Optional
from traits import Derive
from abc import ABC, abstractmethod
from primitives import ArithmeticValue, Value, IntValue

# ===========================================
# #####      ArithmeticExpressions      #####
# ===========================================

#  TODO:
#    - add curring
#    - think about possible mechanism for making __match_args__ always match argument sequence passed into __init__
#      same signature basically but without the need to specify __match_args__ manually every time.
#      idea: make a descriptor of some kind?


class ArithmeticExpression(ABC, Derive.Hash):
    @abstractmethod
    def evaluate(self, environment: Environment) -> ArithmeticValue:
        """Evaluate self."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Return nicely formatted formula."""
        pass

    def __add__(self, rhs: ArithmeticExpression) -> ArithmeticExpression:
        return Add(self, rhs)

    def __mul__(self, rhs: ArithmeticExpression) -> ArithmeticExpression:
        return Times(self, rhs)

    @staticmethod
    def derivative(expr: ArithExpr, var: Optional[Var] = None) -> ArithExpr:
        """Calculate a derivative of a function.
        This function is an extension of the original concept.
        Original assumption that expression contains only one variable can be generalized as follows.
        We can add an optional argument `var` that specifies with regard to what variable should the derivation be performed.
        Than precede as follows:
            - var is specified:       -- perform derivation with regard to var.
                 note: if var does not appear in expr derivation will result in Constant(0).
            - var is not specified:
                Traverse the AST of expr and collect all present variables into a set.
                If obtained set contains:
                    - no variables    -- raise DerivationError

                    I had a lot of debate what to do here exactly.
                    In my opinion If a consumer specifies the derivation variable explicitly
                    than we can assume that he knows what he's/she's doing.
                    In the other case when we try to infer the variable it's much more implicit.
                    Too implicit in my opinion.
                    I can see how returning Constant(0) could lead to a lot of frustration.
                    It would be doing too much on behalf of the end-user so we raise
                    an appropriate exception and ask to use more explicit version with var specified.

                    - one variable    -- assume derivation with regard to that variable.
                    - many variables  -- raise DerivationError
        """

        def var_set(expr: ArithExpr) -> list[Var]:
            """Generate the set of Variables present in AST of expr."""

            def wrapper(expr: ArithExpr, variables: set[Var]):
                match expr:
                    case Add(lhs, rhs) | Times(lhs, rhs):
                        return wrapper(lhs, variables) | wrapper(rhs, variables)
                    case Constant(_):
                        return variables
                    case Variable(_) as var:
                        variables.add(var)
                        return variables

            return list(wrapper(expr, set()))

        def derivative_with_regard_to(expr: ArithExpr, var: Var) -> ArithExpr:
            """Calculate the derivative of expr with regard to var."""
            match expr:
                # if we encounter our derivation variable return 1.
                # any other variable should be treated as a constant value.
                case Variable(_) as found_var:
                    value = IntValue(1) if found_var == var else IntValue(0)
                    return Constant(value)
                case Constant(_):
                    return Constant(IntValue(0))
                case Add(lhs, rhs):
                    return derivative_with_regard_to(lhs, var) + derivative_with_regard_to(rhs, var)
                case Times(lhs, rhs):
                    return derivative_with_regard_to(lhs, var) * rhs + lhs * derivative_with_regard_to(rhs, var)

        def infer_derivation_variable(expr: ArithExpr) -> Var:
            """Attempt to infer derivation variable."""
            present_vars = var_set(expr)
            match present_vars:
                case [var]:
                    return var
                case _:
                    raise DerivationError(
                        f"Cannot infer derivation variable "
                        f"-- Passed expression contains {len(present_vars)} variable(s): {present_vars}, expected: 1."
                        "\nPlease specify it with optional argument `var`."
                    )

        derv_var = var or infer_derivation_variable(expr)
        return derivative_with_regard_to(expr, derv_var)


class Variable(ArithmeticExpression, Derive.PartialEq, Derive.Hash):
    """AST leaf that represents a variable. Variables can be evaluated by looking up value
    assigned to them in Environment that is passed as evaluate method argument.
    """

    __match_args__ = ("name",)

    def __init__(self, name: str) -> None:
        self.name = name

    def evaluate(self, environment: Environment) -> Value:
        # TODO: raise variable lookup exception of some sort.
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


class Constant(ArithmeticExpression, Derive.PartialEq):
    """AST leaf that represents a literal / constant value."""

    __match_args__ = ("value",)

    def __init__(self, value: ArithmeticValue):
        self.value = value

    def evaluate(self, environment: Environment) -> ArithmeticValue:
        return self.value

    def __str__(self) -> str:
        return str(self.value)


class Add(ArithmeticExpression, Derive.PartialEq):
    """AST node that represents sum of two other ArithmeticExpressions."""

    __match_args__ = ("lhs", "rhs")

    def __init__(self, lhs: ArithmeticExpression, rhs: ArithmeticExpression) -> None:
        self.lhs = lhs
        self.rhs = rhs

    def evaluate(self, environment: Environment) -> ArithmeticValue:
        return self.lhs.evaluate(environment) + self.rhs.evaluate(environment)

    def __str__(self) -> str:
        return " + ".join(_parenthesize(self.lhs, self, self.rhs))


class Times(ArithmeticExpression, Derive.PartialEq):
    """AST node that represents product of two other ArithmeticExpressions."""

    __match_args__ = ("lhs", "rhs")

    def __init__(self, lhs: ArithmeticExpression, rhs: ArithmeticExpression):
        self.lhs = lhs
        self.rhs = rhs

    def evaluate(self, environment: Environment) -> ArithmeticValue:
        return self.lhs.evaluate(environment) * self.rhs.evaluate(environment)

    def __str__(self) -> str:
        return " * ".join(_parenthesize(self.lhs, self, self.rhs))


OPERATOR_PRECEDENCE: dict[type, int] = {Times: 3, Add: 2, Variable: 1, Constant: 1}


# Type aliases for more concise annotations:
ArithExpr = ArithmeticExpression
Var = Variable
Env = Environment
Const = Constant
AtomicExpr = Union[Constant, Variable]  # -- an expression that has no subexpressions - leaf in the AST.
CompositeExpr = Union[Add, Times]       # -- an expression that has subexpressions    - node in the AST.


class DerivationError(Exception):
    def __init__(self, msg: str, *args) -> None:
        super().__init__(*args)
        self.msg = msg

    def __str__(self) -> str:
        return self.msg


def _parenthesize(lhs: ArithExpr, self: CompositeExpr, rhs: ArithExpr) -> tuple[str, str]:
    """Helper function. Determine which, if any, sides of ArithmeticExpression require parenthesis
    while converting to str based on the operator priority.

    An ArithmeticExpression needs to be parenthesized if it has both a:
        - sub ArithmeticExpression          -- i.e. is AST node.
        - lower priority that current root  -- than current root would "steal" one of the operands.
    """

    root_prec = OPERATOR_PRECEDENCE[type(self)]
    str_builder = []
    for sub_expr in [lhs, rhs]:
        if isinstance(sub_expr, get_args(CompositeExpr)) and OPERATOR_PRECEDENCE[type(sub_expr)] < root_prec:
            str_builder.append(f"({sub_expr})")
        else:
            str_builder.append(str(sub_expr))

    par_lhs, par_rhs = str_builder
    return par_lhs, par_rhs


def main():
    expr = Times(Add(Variable("x"), Constant(IntValue(2))), Variable("x"))
    print(expr)
    print(ArithmeticExpression.derivative(expr))


if __name__ == "__main__":
    main()
