from typing import Any
from collections import OrderedDict
from functools import partial

import torch
import torch.nn as nn
import torchvision

from torchvision.models.efficientnet import MBConvConfig, model_urls

from .common import Model


__all__ = [
    "EfficientNet",
    "EfficientNetB0",
    "EfficientNetB1",
    "EfficientNetB2",
    "EfficientNetB3",
    "EfficientNetB4",
    "EfficientNetB5",
    "EfficientNetB6",
    "EfficientNetB7"
]


class EfficientNet(torchvision.models.EfficientNet, Model):

    ARCH: str = None

    def __init__(self, num_classes: int, pretrained: bool = False, **kwargs) -> None:
        self.num_classes = num_classes
        torchvision.models.EfficientNet.__init__(self, num_classes=num_classes, **kwargs)
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


def _get_inverted_residual_setting(width_mult: float, depth_mult: float):
    bneck_conf = partial(MBConvConfig, width_mult=width_mult, depth_mult=depth_mult)
    inverted_residual_setting = [
        bneck_conf(1, 3, 1, 32, 16, 1),
        bneck_conf(6, 3, 2, 16, 24, 2),
        bneck_conf(6, 5, 2, 24, 40, 2),
        bneck_conf(6, 3, 2, 40, 80, 3),
        bneck_conf(6, 5, 1, 80, 112, 3),
        bneck_conf(6, 5, 2, 112, 192, 4),
        bneck_conf(6, 3, 1, 192, 320, 1),
    ]
    return inverted_residual_setting


class EfficientNetB0(EfficientNet):

    ARCH: str = "efficientnet_b0"

    def __init__(self, num_classes: int, pretrained: bool = False, **kwargs) -> None:
        inverted_residual_setting = _get_inverted_residual_setting(1.0, 1.0)
        super().__init__(num_classes=num_classes,
                         pretrained=pretrained,
                         inverted_residual_setting=inverted_residual_setting,
                         dropout=0.2,
                         **kwargs)


class EfficientNetB1(EfficientNet):

    ARCH: str = "efficientnet_b1"

    def __init__(self, num_classes: int, pretrained: bool = False, **kwargs) -> None:
        inverted_residual_setting = _get_inverted_residual_setting(1.0, 1.1)
        super().__init__(num_classes=num_classes,
                         pretrained=pretrained,
                         inverted_residual_setting=inverted_residual_setting,
                         dropout=0.2,
                         **kwargs)


class EfficientNetB2(EfficientNet):

    ARCH: str = "efficientnet_b2"

    def __init__(self, num_classes: int, pretrained: bool = False, **kwargs) -> None:
        inverted_residual_setting = _get_inverted_residual_setting(1.1, 1.2)
        super().__init__(num_classes=num_classes,
                         pretrained=pretrained,
                         inverted_residual_setting=inverted_residual_setting,
                         dropout=0.3,
                         **kwargs)


class EfficientNetB3(EfficientNet):

    ARCH: str = "efficientnet_b3"

    def __init__(self, num_classes: int, pretrained: bool = False, **kwargs) -> None:
        inverted_residual_setting = _get_inverted_residual_setting(1.2, 1.4)
        super().__init__(num_classes=num_classes,
                         pretrained=pretrained,
                         inverted_residual_setting=inverted_residual_setting,
                         dropout=0.3,
                         **kwargs)


class EfficientNetB4(EfficientNet):

    ARCH: str = "efficientnet_b4"

    def __init__(self, num_classes: int, pretrained: bool = False, **kwargs) -> None:
        inverted_residual_setting = _get_inverted_residual_setting(1.4, 1.8)
        super().__init__(num_classes=num_classes,
                         pretrained=pretrained,
                         inverted_residual_setting=inverted_residual_setting,
                         dropout=0.4,
                         **kwargs)


class EfficientNetB5(EfficientNet):

    ARCH: str = "efficientnet_b5"

    def __init__(self, num_classes: int, pretrained: bool = False, **kwargs) -> None:
        inverted_residual_setting = _get_inverted_residual_setting(1.6, 2.2)
        super().__init__(num_classes=num_classes,
                         pretrained=pretrained,
                         inverted_residual_setting=inverted_residual_setting,
                         dropout=0.4,
                         norm_layer=partial(nn.BatchNorm2d, eps=0.001, momentum=0.01),
                         **kwargs)


class EfficientNetB6(EfficientNet):

    ARCH: str = "efficientnet_b6"

    def __init__(self, num_classes: int, pretrained: bool = False, **kwargs) -> None:
        inverted_residual_setting = _get_inverted_residual_setting(1.8, 2.6)
        super().__init__(num_classes=num_classes,
                         pretrained=pretrained,
                         inverted_residual_setting=inverted_residual_setting,
                         dropout=0.5,
                         norm_layer=partial(nn.BatchNorm2d, eps=0.001, momentum=0.01),
                         **kwargs)


class EfficientNetB7(EfficientNet):

    ARCH: str = "efficientnet_b7"

    def __init__(self, num_classes: int, pretrained: bool = False, **kwargs) -> None:
        inverted_residual_setting = _get_inverted_residual_setting(2.0, 3.1)
        super().__init__(num_classes=num_classes,
                         pretrained=pretrained,
                         inverted_residual_setting=inverted_residual_setting,
                         dropout=0.5,
                         norm_layer=partial(nn.BatchNorm2d, eps=0.001, momentum=0.01),
                         **kwargs)
