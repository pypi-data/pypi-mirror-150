from typing import Callable, Tuple

import torch
from torch import Tensor

from nn_module import Module
import torchdiffeq


class ODEFunc(Module):
    def forward(self, t: float, y: torch.Tensor):
        raise Exception("not implemented")


class NeuralODE(Module):
    ode_int: Callable[[ODEFunc, Tensor, Tensor], Tensor]
    ode: ODEFunc

    def __init__(self, ode: ODEFunc, t_range: Tuple[float, float] = (0, 1), adjoint: bool = True):
        """
        :param ode: f(t, y)
        """
        super().__init__()
        if adjoint:
            self.ode_int = torchdiffeq.odeint_adjoint
        else:
            self.ode_int = torchdiffeq.odeint
        self.ode = ode
        self.int_interval = Tensor(t_range).to(torch.float32)

    def forward(self, x: Tensor, **kwargs) -> Tensor:
        return self.ode_int(self.ode, x, self.int_interval, **kwargs)[1]
