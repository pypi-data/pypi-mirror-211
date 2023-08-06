# -*- coding: utf-8 -*-

__all__ = ("StrPath",)

from os import PathLike
from typing import TypeAlias

StrPath: TypeAlias = str | PathLike[str]
