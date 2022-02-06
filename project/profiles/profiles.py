# -*- encoding: utf-8 -*-


from profiles.statistics import Statistics


class Profile:

    def __init__(self, nick: str, statistics: Statistics) -> None:
        self.nice = nick
        self.stats = statistics

    def register_loss(self, caps_lost: int, opponents_nick: str) -> None:
