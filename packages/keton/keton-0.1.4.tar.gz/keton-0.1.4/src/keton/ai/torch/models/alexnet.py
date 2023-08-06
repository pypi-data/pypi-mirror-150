from collections import OrderedDict

import torch
import torch.nn as nn
import torchvision

from torchvision.models.alexnet import model_urls

from .common import Model


__all__ = [
    "AlexNet"
]


class AlexNet(torchvision.models.AlexNet, Model):

    ARCH: str = "alexnet"

    def __init__(self, num_classes: int = 1000, pretrained: bool = False, **kwargs) -> None:
        self.num_classes = num_classes
        torchvision.models.AlexNet.__init__(self, num_classes=num_classes, **kwargs)
        Model.__init__(self, pretrained=pretrained)

    def _load_pretrained_weights(self) -> None:
        state_dict = torch.hub.load_state_dict_from_url(model_urls[self.ARCH])
        for state_key in list(state_dict.keys()):
            module_name = state_key.split(".")[0]
            if module_name == "classifier" and self.num_classes != 1000:
                state_dict.pop(state_key)
                continue
            if module_name not in self._pretrained_modules:
                self._pretrained_modules[module_name] = self.get_submodule(module_name)
        self.load_state_dict(state_dict, strict=False)

    @property
    def feature_modules(self) -> nn.ModuleDict:
        modules = nn.ModuleDict(OrderedDict(
            features=self.features
        ))
        return modules
