# -*- coding: utf-8 -*-

from __future__ import annotations

__all__ = (
    "SingleDomainDataset",
    "DoubleDomainDataset",
    "MultiDomainDataset",
    "BinarizedDataset",
    "CategorizedDataset",
)

from abc import abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

from beartype import beartype
from kaparoo.beartype import PosInt
from kaparoo.utils.types import T_co
from torch.utils.data import Dataset
from typing_extensions import LiteralString

if TYPE_CHECKING:
    from torch import Tensor

    D_co = TypeVar("D_co", bound=tuple[Tensor, ...], covariant=True)


class DomainDatasetBase(Dataset[T_co]):
    @beartype
    def __init__(self, num_domains: PosInt) -> None:
        super().__init__()
        self._num_domains = num_domains

    @property
    def num_domains(self) -> int:
        return self._num_domains

    @property
    @abstractmethod
    def data(self) -> T_co:
        raise NotImplementedError

    def __str__(self) -> LiteralString:
        return self.__class__.__name__


class SingleDomainDataset(DomainDatasetBase[Tensor]):
    def __init__(self) -> None:
        super().__init__(num_domains=1)


class DoubleDomainDataset(DomainDatasetBase[tuple[Tensor, Tensor]]):
    def __init__(self) -> None:
        super().__init__(num_domains=2)


class MultiDomainDataset(DomainDatasetBase[tuple[Tensor, ...]]):
    pass


class DomainwiseBase(Generic[D_co]):
    _domains: D_co
    _length: int

    @property
    def data(self) -> D_co:
        return self.domains

    @property
    def domains(self) -> D_co:
        return self._domains

    @property
    def length(self) -> int:
        if not hasattr(self, "_length"):
            if (length := min(len(d) for d in self.domains)) == 0:
                raise ValueError("minimum length of domains should be greater than 0")
            self._length = length
        return self._length

    def __len__(self) -> int:
        return self.length

    def __getitem__(self, index) -> D_co:
        return tuple(d[index] for d in self.domains)  # type: ignore[return-value]


class BinarizedDataset(DomainwiseBase[tuple[Tensor, Tensor]], DoubleDomainDataset):
    pass


class CategorizedDataset(DomainwiseBase[tuple[Tensor, ...]], MultiDomainDataset):
    pass
