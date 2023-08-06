# -*- coding: utf-8 -*-

__all__ = ("BATCH_SIZE", "MAX_WORKERS", "NUM_WORKERS")

import os
from typing import Final

from torch import cuda

BATCH_SIZE: Final[int] = 32 if cuda.is_available() else 8

_CPU_COUNT = os.cpu_count()
MAX_WORKERS: Final[int] = _CPU_COUNT if isinstance(_CPU_COUNT, int) else 0
NUM_WORKERS: Final[int] = MAX_WORKERS // 2
