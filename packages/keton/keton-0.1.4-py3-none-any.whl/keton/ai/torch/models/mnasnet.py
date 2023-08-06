from collections import OrderedDict

import torch
import torch.nn as nn
import torchvision

from torchvision.models.mnasnet import _MODEL_URLS as model_urls

from .common import Model


__all__ = [
    "MNASNet",
    "MNASNet050",
    "MNASNet075",
    "MNASNet100",
    "MNASNet130"
]


class MNASNet(torchvision.models.MNASNet, Model):

    ARCH: str = None

    def __init__(self, num_classes: int = 1000, pretrained: bool = False, **kwargs) -> None:
        torchvision.models.MNASNet.__init__(self, num_classes=num_classes, **kwargs)
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
            layers=self.layers
        ))
        return modules


class MNASNet050(MNASNet):

    ARCH: str = "mnasnet0_5"

    def __init__(self, num_classes: int, pretrained=False, **kwargs) -> None:
        super().__init__(num_classes,
                         alpha=0.5,
                         pretrained=pretrained,
                         **kwargs)


class MNASNet075(MNASNet):

    ARCH: str = "mnasnet0_75"

    def __init__(self, num_classes: int, pretrained=False, **kwargs) -> None:
        super().__init__(num_classes,
                         alpha=0.75,
                         pretrained=pretrained,
                         **kwargs)


class MNASNet100(MNASNet):

    ARCH: str = "mnasnet1_0"

    def __init__(self, num_classes: int, pretrained=False, **kwargs) -> None:
        super().__init__(num_classes,
                         alpha=1.0,
                         pretrained=pretrained,
                         **kwargs)


class MNASNet130(MNASNet):

    ARCH: str = "mnasnet1_3"

    def __init__(self, num_classes: int, pretrained=False, **kwargs) -> None:
        super().__init__(num_classes,
                         alpha=1.3,
                         pretrained=pretrained,
                         **kwargs)