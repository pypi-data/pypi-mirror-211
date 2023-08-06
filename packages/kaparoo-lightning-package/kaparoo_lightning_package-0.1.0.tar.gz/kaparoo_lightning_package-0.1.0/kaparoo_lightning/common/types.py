# -*- coding: utf-8 -*-

__all__ = ("TensorFn",)

from collections.abc import Callable
from typing import TypeAlias

from kaparoo.utils.types import T_co
from torch import Tensor

TensorFn: TypeAlias = Callable[[T_co], Tensor]
