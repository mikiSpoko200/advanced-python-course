# -*- encoding: utf-8 -*-

"""
This module defines functions and classes to work with classes.
"""


# URGENT: Verify that the sorted references do not mess with garbage collector!
# FIXME: do some reading about the __new__ arguments and maybe find better way to do this.


# External imports
import pygame.font


def register_instances(wrapped_class: type):
    """Wrapper for classes that adds instance registration.

    This function adds custom attribute to the CLASS object that is wrapped classed instance_registry.
    It's a list of references to the objects.
    """

    setattr(wrapped_class, "instance_registry", list())

    if "__new__" in wrapped_class.__dict__:
        # If wrapped class defines __new__ store it and override.
        __prev_new = wrapped_class.__new__
        setattr(wrapped_class, "__prev_new", __prev_new)

        def __new__(cls, *args, **kwargs):
            instance = cls.__prev_new(*args, **kwargs)
            cls.instance_registry.append(instance)
            return instance
    else:
        def __new__(cls, *args, **kwargs):
            instance = super(type(cls), cls).__new__(cls)
            cls.instance_registry.append(instance)
            return instance

    setattr(wrapped_class, "__new__", __new__)
    return wrapped_class


class SharedFontObject:
    """Provides shares pygame.font.Font object amongst subclass instances."""

    def __init__(self, font_object: pygame.font.Font) -> None:
        self._font_object = font_object
