# -*- encoding: utf-8 -*-

"""
            #===========================================#
            ######           Exceptions            ######
            #===========================================#

This file contains Language level Errors.
"""


class LangUndefinedSymbol(Exception):
    """Exception Raised on failed symbol resolution. As of now raised only on failed variable lookup."""
    def __init__(self, msg: str, *args):
        super().__init__(*args)
        self.msg = msg

    def __str__(self) -> str:
        return self.msg


class LangZeroDivisionError(Exception):
    """Exception Raised on zero division."""
    def __init__(self, msg: str, *args):
        super().__init__(*args)
        self.msg = msg

    def __str__(self) -> str:
        return self.msg


class LangDerivationError(Exception):
    """Exception raised when derivation operations cannot be performed."""
    def __init__(self, msg: str, *args) -> None:
        super().__init__(*args)
        self.msg = msg

    def __str__(self) -> str:
        return self.msg
