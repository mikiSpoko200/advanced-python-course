# ===========================================
# #####           Exceptions            #####
# ===========================================

class LangException(Exception):
    def __init__(self, callstack: list[str], line: str, column: str, msg: str):
        self.callstack = callstack
        self.line = line
        self.column = column
        self.msg = msg


class LangSyntaxError(LangException):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        raise NotImplementedError


class LangUndefinedSymbol(LangException):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        raise NotImplementedError


class LangZeroDivisionError(LangException):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        raise NotImplementedError
