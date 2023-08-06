# -*- coding: utf-8 -*-

__all__ = ("DataModule",)

from typing import Any, Generic

from kaparoo.utils import unwrap_or_default
from kaparoo.utils.types import T_co
from lightning import LightningDataModule
from torch.utils.data import DataLoader, Dataset
from typing_extensions import LiteralString

from kaparoo_lightning.data.constants import BATCH_SIZE, NUM_WORKERS
from kaparoo_lightning.data.utils import DataLoaderSpec, update_dataloader_spec


class DataModuleBase(LightningDataModule, Generic[T_co]):
    def __init__(self) -> None:
        super().__init__()
        self.dataset_train: Dataset[T_co] | None = None
        self.dataset_valid: Dataset[T_co] | None = None
        self.dataset_test: Dataset[T_co] | None = None
        self.dataset_pred: Dataset[T_co] | None = None

    @property
    def has_train(self) -> bool:
        return isinstance(self.dataset_train, Dataset)

    @property
    def has_valid(self) -> bool:
        return isinstance(self.dataset_valid, Dataset)

    @property
    def has_test(self) -> bool:
        return isinstance(self.dataset_test, Dataset)

    @property
    def has_pred(self) -> bool:
        return isinstance(self.dataset_pred, Dataset)

    def __str__(self) -> LiteralString:
        return self.__class__.__name__


class DataModule(DataModuleBase[T_co]):
    def __init__(
        self,
        batch_size: int = BATCH_SIZE,
        num_workers: int = NUM_WORKERS,
        shuffle: bool = True,
        *,
        # for `Dataset`
        max_trains: int | None = None,
        max_valids: int | None = None,
        max_tests: int | None = None,
        max_preds: int | None = None,
        # for `DataLoader`
        dataloader_spec: DataLoaderSpec | None = None,
        train_loader_spec: DataLoaderSpec | None = None,
        valid_loader_spec: DataLoaderSpec | None = None,
        test_loader_spec: DataLoaderSpec | None = None,
        pred_loader_spec: DataLoaderSpec | None = None,
    ) -> None:
        super().__init__()

        self.use_train = max_trains != 0
        self.use_valid = max_valids != 0
        self.use_test = max_tests != 0
        self.use_pred = max_preds != 0

        if not (self.use_train or self.use_valid or self.use_test or self.use_pred):
            raise ValueError(f"cannot create {self} when none of the datasets exist")

        self.max_trains = max_trains
        self.max_valids = max_valids
        self.max_tests = max_tests
        self.max_preds = max_preds

        default_spec: DataLoaderSpec = {
            **unwrap_or_default(dataloader_spec, {}),  # type: ignore[misc]
            "batch_size": batch_size,
            "num_workers": num_workers,
            "shuffle": shuffle,
        }
        self.train_spec = update_dataloader_spec(default_spec, train_loader_spec)
        self.valid_spec = update_dataloader_spec(default_spec, valid_loader_spec)
        self.test_spec = update_dataloader_spec(default_spec, test_loader_spec)
        self.pred_spec = update_dataloader_spec(default_spec, pred_loader_spec)

    @property
    def config(self) -> dict[str, Any]:
        if not hasattr(self, "_config"):
            self._config = {}
            for stage in ("train", "valid", "test", "pred"):
                self._config[stage] = {
                    "dataset": {
                        "use": getattr(self, f"use_{stage}"),
                        "max": getattr(self, f"max_{stage}s"),
                    },
                    "dataloader": getattr(self, f"{stage}_spec"),
                }
        return self._config

    def train_dataloader(self) -> DataLoader[T_co]:
        if not self.has_train:
            raise AttributeError(f"{self} does not have a dataset for training")

        return DataLoader(
            self.dataset_train,  # type: ignore[arg-type]
            **self.train_spec,
        )

    def val_dataloader(self) -> DataLoader[T_co]:
        if not self.has_valid:
            raise AttributeError(f"{self} does not have a dataset for validation")

        return DataLoader(
            self.dataset_valid,  # type: ignore[arg-type]
            **self.valid_spec,
        )

    def test_dataloader(self) -> DataLoader[T_co]:
        if not self.has_test:
            raise AttributeError(f"{self} does not have a dataset for testing")

        return DataLoader(
            self.dataset_test,  # type: ignore[arg-type]
            **self.test_spec,
        )

    def predict_dataloader(self) -> DataLoader[T_co]:
        if not self.has_pred:
            raise AttributeError(f"{self} does not have a dataset for prediction")

        return DataLoader(
            self.dataset_pred,  # type: ignore[arg-type]
            **self.pred_spec,
        )
