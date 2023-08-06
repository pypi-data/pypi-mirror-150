from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F


__all__ = [
    "FocalLoss"
]


class FocalLoss(nn.Module):
    """
    From: https://github.com/fastai/fastai/blob/master/fastai/losses.py
    """

    __constants__ = ['gamma', 'reduction']
    gamma: float
    weight: Optional[torch.Tensor]

    def __init__(self, gamma: float = 2.0, weight: Optional[torch.Tensor] = None, reduction: str = 'mean') -> None:
        super(FocalLoss, self).__init__()
        self.gamma = gamma
        self.reduction = reduction
        self.register_buffer('weight', weight)

    def forward(self, input: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        ce_loss = F.cross_entropy(input, target, weight=self.weight, reduction="none")
        p_t = torch.exp(-ce_loss)
        loss = (1 - p_t)**self.gamma * ce_loss
        if self.reduction == "mean":
            loss = loss.mean()
        elif self.reduction == "sum":
            loss = loss.sum()
        return loss
