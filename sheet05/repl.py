class REPLState:
    def __init__(self) -> None:
        raise NotImplementedError


def repl() -> None:
    state = REPLState()
