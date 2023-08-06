# -*- coding: utf-8 -*-

__all__ = ("Singleton", "SingletonMeta", "singleton")

from collections.abc import Callable
from typing import Type, TypeVar

from typing_extensions import Self

T = TypeVar("T")


class Singleton(object):
    """A class that only allows one instance to be created.

    Example:
        >>> class MyClass(Singleton):
        ...     pass
        ...
        >>> obj1 = MyClass()
        >>> obj2 = MyClass()
        >>> obj1 is obj2
        True
    """

    _instance: Self = None  # type: ignore[assignment]

    def __new__(cls: Type[Self], *args, **kwargs) -> Self:
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance  # type: ignore[return-value]


# TODO: Add type annotations (Self type cannot be used in a metaclass)
class SingletonMeta(type):
    """A metaclass that only allows one instance of a class to be created.

    Example:
        >>> class MyClass(metaclass=SingletonMeta):
        ...     pass
        ...
        >>> obj1 = MyClass()
        >>> obj2 = MyClass()
        >>> obj1 is obj2
        True
    """

    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


def singleton(cls: Type[T]) -> Callable[..., T]:
    """Make a given class as a singleton.

    Example:
        >>> @singleton
        ... class MyClass:
        ...     pass
        ...
        >>> obj1 = MyClass()
        >>> obj2 = MyClass()
        >>> obj1 is obj2
        True
    """

    _instances: dict[Type[T], T] = {}

    def wrapper(*args, **kwargs) -> T:
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]

    return wrapper
