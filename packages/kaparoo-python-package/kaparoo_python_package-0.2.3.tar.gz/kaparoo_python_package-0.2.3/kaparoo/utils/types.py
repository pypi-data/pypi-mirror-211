# -*- coding: utf-8 -*-

__all__ = ("T", "U", "K", "V", "T_co", "U_co", "K_co", "V_co")

from typing import TypeVar

# Type variables
T = TypeVar("T")
U = TypeVar("U")
K = TypeVar("K")
V = TypeVar("V")

# Covariant type variables
T_co = TypeVar("T_co", covariant=True)
U_co = TypeVar("U_co", covariant=True)
K_co = TypeVar("K_co", covariant=True)
V_co = TypeVar("V_co", covariant=True)
