# -*- encoding: utf-8 -*-

from abc import ABC, abstractmethod


class IView(ABC):

    @abstractmethod
    def draw(self, surface) -> None:
        pass


def draw_main_menu() -> None:
    pass

def draw_ga


class Menu(IView):
    pass


class


class MultiplayerLobby(IView):
    pass


class Game(IView):
    pass

