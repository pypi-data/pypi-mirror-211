# -*- coding: utf-8 -*-

from __future__ import annotations

__all__ = ("DataLoaderSpec", "update_dataloader_spec")

from collections.abc import Iterable, Sequence
from typing import Any, TypedDict

from kaparoo.utils import unwrap_or_default
from torch.utils.data import Sampler
from torch.utils.data.dataloader import _collate_fn_t, _worker_init_fn_t


class DataLoaderSpec(TypedDict, total=False):
    batch_size: int
    num_workers: int
    shuffle: bool
    sampler: Sampler | Iterable
    batch_sampler: Sampler[Sequence] | Iterable[Sequence]
    collate_fn: _collate_fn_t
    pin_memory: bool
    drop_last: bool
    timeout: float
    worker_init_fn: _worker_init_fn_t
    multiprocessing_context: Any
    generator: Any
    prefetch_factor: int
    persistent_workers: bool
    pin_memory_device: str


def update_dataloader_spec(
    default: DataLoaderSpec, optional: DataLoaderSpec | None
) -> DataLoaderSpec:
    optional = unwrap_or_default(optional, {})
    # false positive error by mypy (see issue #4122)
    return {**default, **optional}  # type: ignore[misc]
