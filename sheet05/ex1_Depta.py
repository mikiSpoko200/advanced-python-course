# -*- encoding: utf-8 -*-

from __future__ import annotations

from abc import ABC, abstractmethod
import primitives
import traits

__VERSION__ = "0.0.1"
__AUTHOR__ = "Mikołaj Depta"

"""
# VERSION: 0.0.1
DESIGN CHOICES:
    - curly braces dictate lexical scope.
    - statically and strongly typed -- this assumptions make this exercise feasible as it 
                                       allows me to omit cross type operations which require huge 
                                       amount of boilerplate code.
    - primitive types: IntValue (integer), FloatValue (float)
"""


def main():
    print("Hello world!")


if __name__ == '__main__':
    main()
