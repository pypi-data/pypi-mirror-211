# -*- coding: utf-8 -*-

__all__ = ("NonNegInt", "NonNegativeInt", "PosInt", "PositiveInt")

from typing import Annotated, TypeAlias

from beartype.vale import Is

NonNegativeInt: TypeAlias = Annotated[int, Is[lambda x: x >= 0]]
PositiveInt: TypeAlias = Annotated[int, Is[lambda x: x > 0]]

PosInt: TypeAlias = PositiveInt
NonNegInt: TypeAlias = NonNegativeInt
