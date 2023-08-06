from typing import Iterable

import torch.nn as nn
import torch.optim as optim

from ..utils.modules import ClassBundle


__all__ = [
    "Callback",
    "Callbacks"
]


class Callback:

    def __init__(self) -> None:
        self._model: nn.Module = None
        self._optimizer: optim.Optimizer = None
        self._description: str = None

    def set_model(self, model: nn.Module) -> None:
        self._model = model

    def set_optimizer(self, optimizer: optim.Optimizer) -> None:
        self._optimizer = optimizer

    def set_params(self, params: dict) -> None:
        self._params = params

    def on_train_begin(self) -> None:
        pass

    def on_train_end(self) -> None:
        pass

    def on_epoch_begin(self, epoch: int) -> None:
        pass

    def on_epoch_end(self, epoch: int, metrics: dict) -> None:
        pass

    def on_train_epoch_begin(self, epoch: int) -> None:
        pass

    def on_train_epoch_end(self, epoch: int, metrics: dict) -> None:
        pass

    def on_train_batch_begin(self, batch: int) -> None:
        pass

    def on_train_batch_end(self, batch: int, metrics: dict) -> None:
        pass

    def on_eval_begin(self) -> None:
        pass

    def on_eval_end(self, metrics: dict) -> None:
        pass

    def on_eval_batch_begin(self, batch: int) -> None:
        pass

    def on_eval_batch_end(self, batch: int, metrics: dict) -> None:
        pass


class Callbacks(ClassBundle[Callback]):

    def __init__(self,
                 callbacks: Iterable[Callback] = None) -> None:
        if callbacks is None:
            callbacks = []
        super().__init__(callbacks)
