
import colorama.ansi
colorama.init()


def fixme(msg: str) -> str:
    return colorama.ansi.AnsiBack.RED + msg + colorama.ansi.AnsiBack.RESET