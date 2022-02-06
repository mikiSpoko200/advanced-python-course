#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
This module exposes a chat control that allows users to type in and send messages.
"""

import interfaces as general_interfaces
import gui.interfaces as gui_interfaces
from interfaces import IDefault
from gui.types import RGB


class ChatColorScheme(general_interfaces.IDefault):

    def __init__(self,
                 default_foreground: RGB,
                 default_background: RGB,
                 select_foreground: RGB,
                 select_background: RGB,
                 press_foreground: RGB,
                 press_background: RGB) -> None:
        self.default_foreground = default_foreground
        self.default_background = default_background
        self.select_foreground = select_foreground
        self.select_background = select_background
        self.press_foreground = press_foreground
        self.press_background = press_background

    @classmethod
    def default(cls) -> IDefault:
        pass


class Chat(gui_interfaces.ISelect, gui_interfaces.IPress):

    def __init__(self):
        self.chat_box = None  # please make this minecraft like for now?
        self.messages: list[str] = []
        self.width = None     #
        self.height = None    #  some common class for all controls? -- BaseWidget?

    # Interface implementations
    # region ISelect
    def selected(self) -> None:
        pass

    def unselected(self) -> None:
        pass
    # endregion

    # region IPress
    def pressed(self) -> None:
        pass

    def released(self) -> None:
        pass
    # endregion
