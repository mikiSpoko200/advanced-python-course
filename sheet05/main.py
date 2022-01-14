# -*- encoding: utf-8 -*-

from expressions import (Constant, Variable, Add, Subtract, Times, Division, Environment)
from primitives import (IntValue)


def main():
    expr = Times(Add(Constant(IntValue(2)),
                     Variable("x")),
                 Variable("y"))
    env = Environment({Variable("x"): IntValue(1), Variable("y"): IntValue(3)})
    print(expr)
    print(value := expr.evaluate(env))
    assert value == IntValue(9)


if __name__ == '__main__':
    main()