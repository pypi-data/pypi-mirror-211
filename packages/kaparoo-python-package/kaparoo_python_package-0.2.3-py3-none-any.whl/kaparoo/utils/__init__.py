# -*- coding: utf-8 -*-

__all__ = (
    "unwrap_or_default",
    "unwrap_or_factory",
    "Singleton",
    "SingletonMeta",
    "singleton",
)

from kaparoo.utils.optional import unwrap_or_default, unwrap_or_factory
from kaparoo.utils.singleton import Singleton, SingletonMeta, singleton
