#!/usr/bin/python
# -*- encoding: utf-8 -*-


import peewee as pw


# CONFIG:
DATABASE = "calendar.db"
db = pw.SqliteDatabase(DATABASE)


class Model(pw.Model):
    """Model containing default configuration."""
    class Meta:
        database = db


class Participant(Model):
    """Model for a participant."""
    id      = pw.AutoField(primary_key=True)
    name    = pw.TextField(null=False)
    surname = pw.TextField(null=False)
    email   = pw.TextField(null=False, unique=True)


class Event(Model):
    """Model for an event."""
    # TODO: Add on insert check if this event collides with current plans of any other user.
    id          = pw.AutoField(primary_key=True)
    start_time  = pw.DateTimeField(null=False)
    end_time    = pw.DateTimeField(null=False)
    description = pw.TextField()
    host        = pw.ForeignKeyField(Participant)

    # class Meta(Model._meta):
    #     raise NotImplementedError("TODO: Implement On insert check constraint.")


# I assume that one person can have multiple events scheduled and conversely many people can be
# assigned to the same event thus we have a many-to-many relation going on here.


class ParticipantEvent(Model):
    """Many-to-many relation between Participant and Event."""
    event       = pw.ForeignKeyField(Event)
    participant = pw.ForeignKeyField(Participant)


def init():
    db.create_tables([Participant, ParticipantEvent, Event])


def main():
    print("Hello main!")
    ziomo = Participant.create(
        name="piotr",
        surname="lisowski",
        email="curring@jest.git"
    )
    a = Participant.create(
        name="foo",
        surname="foo",
        email="f"
    )
    b = Participant.create(
        name="bar",
        surname="bar",
        email="b"
    )
    c = Participant.create(
        name="baz",
        surname="baz",
        email="c"
    )
    some_event = Event.create(
        start_time=datetime.datetime.today(),
        end_time=datetime.datetime.today() + datetime.timedelta(hours=1.0),
        description="Spoko spotkanie elo.",
        host=ziomo.id
    )
    ParticipantEvent.create(
        event=some_event.id,
        participant=ziomo.id
    )
    ParticipantEvent.create(
        event=some_event.id,
        participant=a.id
    )
    ParticipantEvent.create(
        event=some_event.id,
        participant=b.id
    )
    ParticipantEvent.create(
        event=some_event.id,
        participant=c.id
    )

    query = Participant\
        .select()\
        .join(ParticipantEvent)\
        .join(Event)

    for participant in query:
        print(participant.name)


if __name__ == '__main__':
    main()
