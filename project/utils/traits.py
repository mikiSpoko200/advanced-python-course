# -*- encoding: utf-8 -*-

"""
This module exposes a classes that supply some default behaviour:
    - Derive    -- groups classes that provide default implementations of some double underscore methods.
"""


class Derive:
    """collection of classes that when derived from automatically implement certain double underscore methods."""

    class Debug:
        """Default __str__ implementations.

        printing convention: <class name>([<attribute>, ]?)
        """
        def __init_subclass__(cls, **kwargs):
            super().__init_subclass__(**kwargs)

            def default_format(self) -> str:
                str_builder = [f'{attr}: {getattr(self, attr)},' for attr in vars(self)]
                params = ''.join(str_builder)
                return f"{cls.__name__}(\n\t{params})"

            cls.__repr__ = default_format
            return cls

    class Hash:
        """Default implementation for hashing function."""

        def __key(self):
            return tuple(getattr(self, attr) for attr in vars(self))

        def __hash__(self):
            return hash(self.__key())

    class PartialEq:
        """Default implementation of __eq__.
        It requires that both self and other have exactly same attributes and values of said attributes.
        It does not care however about object types.
        """
        def __init_subclass__(cls, **kwargs):
            super().__init_subclass__(**kwargs)

            def default_eq(self, other) -> bool:
                attrs_self = tuple(vars(self))
                attrs_other = tuple(vars(other))
                return attrs_self == attrs_other

            cls.__eq__ = default_eq
            return cls
