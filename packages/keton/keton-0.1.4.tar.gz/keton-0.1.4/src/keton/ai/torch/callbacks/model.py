import json
import os
from typing import Any

import torch

from .common import Callback


__all__ = [
    "ModelCheckpoint"
]


class ModelCheckpoint(Callback):

    def __init__(self,
                 save_dir: str,
                 monitor: str = "val_loss",
                 mode: str = "min",
                 save_freq: int = 1,
                 save_best_only: bool = False,
                 baseline: Any = None,
                 verbose: bool = True) -> None:
        super().__init__()
        if mode not in {"min", "max"}:
            raise ValueError(f"monitor mode '{mode}' is not supported")
        self._save_dir = save_dir
        self._monitor = monitor
        self._mode = mode
        self._save_freq = save_freq
        self._save_best_only = save_best_only
        self._baseline = baseline
        self._verbose = verbose
        self._best_value = None

    def _is_better(self, v1: Any, v2: Any) -> bool:
        delta = (v1 - v2) if self._mode == "min" else (v2 - v1)
        return delta > 0

    def _save_checkpoint(self, epoch: int) -> None:
        os.makedirs(self._save_dir, exist_ok=True)
        model_name = os.path.join(self._save_dir, f"model-ckpt-{epoch:05d}.pt")
        config_name = os.path.join(self._save_dir, f"model-ckpt-{epoch:05d}.json")
        torch.save(self._model.state_dict(), model_name)
        with open(config_name, "w") as f:
            f.write(json.dumps({
                "arch": self._model._get_name(),
                "optimizer": {
                    "type": self._optimizer.__class__.__name__,
                    "param_groups": self._optimizer.state_dict()["param_groups"]
                }
            }))

    def on_epoch_end(self, epoch: int, metrics: dict) -> None:
        if epoch % self._save_freq != 0:
            return
        if self._save_best_only:
            value = metrics[self._monitor]
            if self._best_value is None or self._is_better(self._best_value, value):
                self._best_value = value
                if self._baseline is None or self._is_better(self._baseline, value):
                    if self._verbose:
                        print(f"Epoch {epoch:05d}: saving new best model with {self._monitor}={value}")
                    self._save_checkpoint(epoch)
                else:
                    if self._verbose:
                        print(f"Epoch {epoch:05d}: not saving new best model due to {self._monitor} lower than baseline")
        elif self._baseline is not None:
            value = metrics[self._monitor]
            if self._is_better(self._baseline, value):
                if self._verbose:
                    print(f"Epoch {epoch:05d}: saving model")
                self._save_checkpoint(epoch)
            else:
                if self._verbose:
                    print(f"Epoch {epoch:05d}: not saving model due to {self._monitor} worse than baseline")
        else:
            if self._verbose:
                print(f"Epoch {epoch:05d}: saving model")
            self._save_checkpoint(epoch)
