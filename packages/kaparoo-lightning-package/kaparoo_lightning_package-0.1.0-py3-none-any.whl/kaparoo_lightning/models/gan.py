# -*- coding: utf-8 -*-

from __future__ import annotations

__all__ = ("GAN",)

from typing import TYPE_CHECKING

import torch
import torch.nn.functional as F
from lightning import LightningModule

if TYPE_CHECKING:
    from torch import Tensor


class GAN(LightningModule):
    def __init__(self) -> None:
        super().__init__()
        self.automatic_optimization = False

    def get_labels(self, preds: Tensor, as_real: bool = True) -> Tensor:
        return torch.ones_like(preds) if as_real else torch.zeros_like(preds)

    def adversarial_loss(self, preds: Tensor, as_real: bool = True) -> Tensor:
        labels = self.get_labels(preds, as_real)
        return F.binary_cross_entropy(preds, labels)
