# -*- encoding: utf-8 -*-

from typing import NamedTuple, Optional
from enum import Enum, auto

import db
import ui
from types import ParamValue, QueryParams
from ui import Config, Operation, Component


class Repeat(Enum):
    Once = auto()
    Many = auto()


class ParamInfo(NamedTuple):
    name: str
    type: str
    nullable: bool


def event_type_params() -> list[ParamInfo]:
    return [ParamInfo("name", "text")]


def participant_params() -> list[ParamInfo]:
    return [
        ParamInfo("name", "text", False),
        ParamInfo("surname", "text", False),
        ParamInfo("email", "text", False)
    ]


def event_params() -> list[ParamInfo]:
    return [
        ParamInfo("start_time", "DATETIME", False),
        ParamInfo("end_time", "DATETIME", False),
        ParamInfo("description", "text", True),
    ]


def init_event():
    return ui.get_user_input(event_params())


def init_participant():
    return ui.get_user_input(participant_params())


def init_event_type():
    return ui.get_user_input(event_type_params())


def select_event_type(kwargs):
    while True:
        _ = ui.get_user_input(event_type_params())
        db.EventType.string_to_field({name: _})


def select_participant():

    _ = ui.prompt_until_pred(select_validate, "Specify the Participant \n> ")
    q = db.Participant.select().where({
        db.Participant.name: name,
        db.Participant.surname: surname,
        db.Participant.email: email
    }).execute()

    while True:
        _ = input(prompt)
        if pred(_):
            return _
        print("Invalid input. Please try again.")

    return q[0]


def get_params(c: Config) -> QueryParams:
    match c:
        case Operation.Update, _:
            prev = get_fields(c.component)
            new  = get_fields(c.component)
            ui.get_user_input()
        case Component.Participant, Operation.Update:
            pass
        case _:
            pass

