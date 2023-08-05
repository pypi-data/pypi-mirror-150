from typing import Any
# TODO: Move this to nv.utils.types and add conditional import


class Singleton(type):
    _instances: dict[type, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class UnSet(metaclass=Singleton):

    def __bool__(self):
        return False

    def __repr__(self):
        return f"{self.__class__.__name__}()"


UNSET = UnSet()
