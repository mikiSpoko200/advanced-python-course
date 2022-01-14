# -*- encoding: utf-8 -*-

from __future__ import annotations

# ===========================================
# #####             Parser              #####
# ===========================================


class Parser:
    def __init__(self, code: str) -> None:
        self.code = code

    @classmethod
    def from_source_file(cls, src_file_path: str) -> Parser:
        with open(src_file_path, "r", encoding="utf-8") as source:
            cls(source.read())


def parse(input: str) -> Expression:
    raise NotImplementedError
