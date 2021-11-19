class Derive:
    """Class that provides meta-functions that automatically implement certain dunder methods."""

    class Format:
        """Default formatting."""
        def __init_subclass__(cls, **kwargs):
            super().__init_subclass__(**kwargs)

            def default_format(self) -> str:
                str_builder = [str(getattr(self, attr)) for attr in vars(self)]
                return f"{cls.__name__}({', '.join(str_builder)})"

            cls.__str__ = default_format
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

        TODO: fix this garbage.
        note: I coded this on the train that was running 3 hour late so circumstances were less than ideal.
        """
        def __init_subclass__(cls, **kwargs):
            super().__init_subclass__(**kwargs)

            def default_eq(self, other) -> bool:
                attrs_self = tuple(vars(self))
                attrs_other = tuple(vars(other))
                return attrs_self == attrs_other

            cls.__eq__ = default_eq
            return cls
