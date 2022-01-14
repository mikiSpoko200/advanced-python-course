# -*- encoding: utf-8 -*-

import peewee as pw

# =================================== #
#               Models                #
# =================================== #


# CONFIG:
DATABASE = "calendar.db"
database = pw.SqliteDatabase(DATABASE)


def init():
    database.connect()
    database.create_tables([Participant, ParticipantEvent, Event, EventType])


class Model(pw.Model):
    """Model containing default configuration and functionality required by a component."""
    class Meta:
        database = database


class Participant(Model):
    """Model for a participant."""
    id      = pw.AutoField(primary_key=True)
    name    = pw.TextField(null=False)
    surname = pw.TextField(null=False)
    email   = pw.TextField(null=False, unique=True)

    @staticmethod
    def string_to_field(kwargs):
        return {
            Participant.name: kwargs["name"],
            Participant.surname: kwargs["surname"],
            Participant.email: kwargs["email"]
        }


class EventType(Model):
    """Model for a listing of different event types.
    This table is in one-to-many relation with Event table (many events can have the same type).
    Typically, would use SQL enumeration by sqlite does implement those."""
    name = pw.TextField()

    @staticmethod
    def string_to_field(kwargs):
        return {
            EventType.name: kwargs["name"]
        }


class Event(Model):
    """Model for an event."""
    # TODO: Add on insert check if this event collides with current plans of any other user.
    id          = pw.AutoField(primary_key=True)
    start_time  = pw.DateTimeField(formats="%Y-%m-%d %H:%M:%S")
    end_time    = pw.DateTimeField(formats="%Y-%m-%d %H:%M:%S")
    description = pw.TextField(null=True)
    event_type  = pw.ForeignKeyField(EventType)
    host        = pw.ForeignKeyField(Participant)

    @staticmethod
    def string_to_field(**kwargs):
        return {
            Event.start_time: kwargs["start_time"],
            Event.end_time: kwargs["end_time"],
            Event.description: kwargs["description"],
            Event.event_type: kwargs["event_type"],
            Event.host: kwargs["host"],
        }


# I assume that one person can have multiple events scheduled and conversely many people can be
# assigned to the same event thus we have a many-to-many relation going on here.

class ParticipantEvent(Model):
    """Many-to-many relation between Participant and Event."""
    event       = pw.ForeignKeyField(Event)
    participant = pw.ForeignKeyField(Participant)

