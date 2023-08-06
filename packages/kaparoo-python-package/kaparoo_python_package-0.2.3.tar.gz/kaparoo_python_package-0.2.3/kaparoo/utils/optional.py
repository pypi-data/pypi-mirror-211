# -*- coding: utf-8 -*-

__all__ = ("unwrap_or_default", "unwrap_or_factory")

from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def unwrap_or_default(
    optional: T | None,
    default: T,
    callback: Callable[[T], T] | None = None,
) -> T:
    """Unwrap an optional value or returns a default value.

    If the `optional` value is not `None`, it is returned. Otherwise, the `default`
    value is returned. Optionally, a `callback` function can be provided to transform
    the resulting value.

    Args:
        optional: The optional value to unwrap.
        default: The default value to return if `optional` is `None`.
        callback: A function to transform the resulting value. Defaults to None.

    Returns:
        The unwrapped value or the default value.
    """

    if optional is not None:
        result = optional
    else:
        result = default

    if callable(callback):
        result = callback(result)

    return result


def unwrap_or_factory(
    optional: T | None,
    factory: Callable[[], T],
    callback: Callable[[T], T] | None = None,
) -> T:
    """Unwrap an optional value or returns a value created by a factory function.

    If the `optional` value is not `None`, it is returned. Otherwise, a value is created
    by calling the `factory` function. Optionally, a `callback` function can be provided
    to transform the resulting value.

    Args:
        optional: The optional value to unwrap.
        factory: A factory function to create a value if `optional` is `None`.
        callback: A function to transform the resulting value. Defaults to None.

    Returns:
       The unwrapped value or the value created by the factory function.
    """

    if optional is not None:
        result = optional
    else:
        result = factory()

    if callable(callback):
        result = callback(result)

    return result
