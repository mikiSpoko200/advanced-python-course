# -*- encoding: utf-8 -*-


from typing import NamedTuple


class Statistics(NamedTuple):
    total_games_won: int
    total_games_lost: int
    nemesis: str  # this field will be calculated based on database query results.
    total_caps_won: int

