# -*- encoding: utf-8 -*-
import datetime
from typing import Optional

import peewee as pw

# =================================== #
#               Models                #
# =================================== #


# CONFIG:
DATABASE = "calendar.db"
database = pw.SqliteDatabase(DATABASE)


def init():
    database.create_tables([Participant, ParticipantEvent, Event, EventType])


class Model(pw.Model):
    """Model containing default configuration and functionality required by a component."""
    class Meta:
        database = database


class Register:
    """Registers all subclasses as Components.

    The information is used to automatically generate Components enum using enum's
    functional API: https://docs.python.org/3/library/enum.html#functional-api
    which is in turned used to fill choice argument of argparse.add_argument() in UI module.
    """
    names: list[str] = list()
    
    def __init_subclass__(cls, **kwargs):
        Register.names.append(cls.__name__)


class Participant(Model, Register):
    """Model for a participant."""
    id      = pw.AutoField(primary_key=True)
    name    = pw.TextField(null=False)
    surname = pw.TextField(null=False)
    email   = pw.TextField(null=False, unique=True)


class EventType(Model, Register):
    """Model for a listing of different event types.
    This table is in one-to-many relation with Event table (many events can have the same type).
    Typically would use SQL enumeration by sqlite does implement those."""
    name = pw.TextField()


class Event(Model, Register):
    """Model for an event."""
    # TODO: Add on insert check if this event collides with current plans of any other user.
    id          = pw.AutoField(primary_key=True)
    start_time  = pw.DateTimeField()
    end_time    = pw.DateTimeField()
    description = pw.TextField(null=True)
    event_type  = pw.ForeignKeyField(EventType)
    host        = pw.ForeignKeyField(Participant)


    # class Meta(Model.meta):
    #     raise NotImplementedError("TODO: Implement On insert check constraint.")


# I assume that one person can have multiple events scheduled and conversely many people can be
# assigned to the same event thus we have a many-to-many relation going on here.

class ParticipantEvent(Model):
    """Many-to-many relation between Participant and Event."""
    event       = pw.ForeignKeyField(Event)
    participant = pw.ForeignKeyField(Participant)


# =================================== #
#               Queries               #
# =================================== #


def add_participant(name: str, surname: str, email: str) -> None:
    Participant.insert({
        Participant.name: name, Participant.surname: surname, Participant.email: email
    }).execute()


def remove_participant(name: str, surname: str, email: str) -> None:
    Participant.delete().where({
        Participant.name: name, Participant.surname: surname, Participant.email: email
    }).execute()


def update_participant(
        prev_name: str, prev_surname: str, prev_email: str,
        new_name: str, new_surname: str, new_email: str) -> None:
    Participant.update({
        Participant.name: new_name, Participant.surname: new_surname, Participant.email: new_email
    }).where({
        Participant.name: prev_name, Participant.surname: prev_surname, Participant.email: prev_email
    }).execute()


def display_participant(name: str, surname: str, email: str) -> list[str]:
    query = Participant.select().where(
        { Participant.name: name, Participant.surname: surname, Participant.email: email }
    ).execute()
    print(query)


def add_event(starttime: str, endtime: str, description: Optional[str],
              event_type: str, host: str) -> None:
    Event.insert({
            Event.start_time: starttime, Event.end_time: endtime,
            Event.description: description, Event.event_type: event_type,
            Event.host: host
        }).execute()


def remove_event(starttime: str, endtime: str, description: Optional[str],
                 event_type: str, host: str) -> None:
    Event.delete().where({
            Event.start_time: starttime, Event.end_time: endtime,
            Event.description: description, Event.event_type: event_type,
            Event.host: host
        }).execute()


def update_event(
        prev_starttime: str, prev_endtime: str,
        prev_description: Optional[str], prev_event_type: str,
        prev_host: str, new_starttime: str, new_endtime: str,
        new_description: Optional[str], new_event_type: str,
        new_host: str) -> None:
    Event.update({
            Event.start_time: prev_starttime, Event.end_time: prev_endtime,
            Event.description: prev_description, Event.event_type: prev_event_type,
            Event.host: prev_host
        }).where({
            Event.start_time: new_starttime, Event.end_time: new_endtime,
            Event.description: new_description, Event.event_type: new_event_type,
            Event.host: new_host
        }).execute()


def display_event(starttime: str, endtime: str, description: Optional[str],
                  event_type: str, host: str) -> None:
    query = Event.select().where({
            Event.start_time: starttime, Event.end_time: endtime,
            Event.description: description, Event.event_type: event_type,
            Event.host: host
        })
    print([(event.start_time, event.end_time) for event in query])


def add_event_type(event_type: str) -> None:
    EventType.insert({
        EventType.name: event_type
    }).execute()


def remove_event_type(event_type: str) -> None:
    EventType.delete().where({
        EventType.name: event_type
    }).execute()


def update_event_type(prev_event_type: str, new_event_type: str) -> None:
    EventType.update({
        EventType.name: prev_event_type
    }).where({
        EventType.name: new_event_type
    }).execute()


def display_event_type(event_type: str) -> None:
    query = EventType.select().where({
        EventType.name: event_type
    })


def add_event_with_participants() -> None:



def main():
    init()
    print("Hello main!")
    add_event_type("Meeting")
    start = datetime.datetime.now()
    end = (datetime.datetime.now() + datetime.timedelta(hours=1))
    add_event(starttime=start, endtime=end, description=None,
              event_type="Meeting", host="Mikołaj Depta")
    display_event(starttime=start, endtime=end, description=None,
              event_type="Meeting", host="Mikołaj Depta")


if __name__ == "__main__":
    main()
