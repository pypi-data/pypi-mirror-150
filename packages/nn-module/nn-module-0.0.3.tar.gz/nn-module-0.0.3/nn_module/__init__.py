from typing import Callable, Optional

import torch
from torch import nn


class Module(nn.Module):
    """
    Module: nn.Module with device and dtype properties
    """
    DEVICE_BUFFER_NAME = "device_buffer"

    def __init__(self):
        super(Module, self).__init__()
        self.register_buffer(Module.DEVICE_BUFFER_NAME, torch.empty(0), persistent=True)

    def __get_device(self) -> torch.device:
        return self.state_dict()[Module.DEVICE_BUFFER_NAME].device

    def __set_device(self, device: torch.device):
        self.to(device)

    device = property(__get_device, __set_device)

    def __get_dtype(self) -> torch.dtype:
        return self.state_dict()[Module.DEVICE_BUFFER_NAME].dtype

    def __set_dtype(self, dtype: torch.dtype):
        self.to(dtype)

    dtype = property(__get_dtype, __set_dtype)


class Functional(Module):
    """
    Functional: wrapper for function
    """

    def __init__(self, f: Callable, name: Optional[str] = None):
        super(Functional, self).__init__()
        self.f = f
        if name is None:
            self.name = f
        else:
            self.name = name

    def __repr__(self):
        return f"{self.__class__.__name__} {self.name}"

    def forward(self, *args, **kwargs):
        return self.f(*args, **kwargs)


class Batch(Module):
    """
    Batch: wrapper for non-batch module
    """

    def __init__(self, module: nn.Module):
        super(Batch, self).__init__()
        self.module = module

    def __repr__(self):
        return f"{self.__class__.__name__} {self.module}"

    def forward(self, x_batch: torch.Tensor, *args, **kwargs) -> torch.Tensor:
        return torch.stack([
            self.module.forward(x, *args, **kwargs)
            for x in x_batch
        ])
