"""
Neural Network Model Module (:mod:`vulkpy.nn.models`)
=====================================================
"""
from __future__ import annotations
from typing import Iterable, Optional, Tuple, Union

from vulkpy import Array
from .core import Module, Loss, Regularizer


__all__ = ["Sequence"]


class Sequence:
    """
    Sequential Model

    All layers sequentially connceted.
    """
    def __init__(self,
                 layers: Iterable[Module],
                 loss: Loss):
        """
        Initialize Sequence

        Parameters
        ----------
        layers : iterable of vulkpy.nn.Module
            Layers to be called sequentially
        loss : vulkpy.nn.Loss
            Loss layer
        """
        self.L: Tuple[Module, ...] = tuple(layers)
        self.loss: Loss = loss

    def _forward(self, x: Array) -> Array:
        for _L in self.L:
            x = _L(x)
        return x

    def _backward(self):
        dx = self.loss.grad()
        for _L in self.L[::-1]:
            dx = _L.backward(dx)

    def _zero_grad(self):
        for _L in self.L:
            _L.zero_grad()

    def _update(self):
        for _L in self.L:
            _L.update()

    def train(self, x: Array, y: Array) -> Tuple[Array, Array]:
        """
        Train model

        Parameters
        ----------
        x, y : vulkpy.Array
            Features and Labels/Targets

        Returns
        -------
        y : vulkpy.Array
            Predicted Labels/Targets
        loss : vulkpy.Array
            Loss
        """
        _y = self._forward(x)
        _loss = self.loss(_y, y)

        self._zero_grad()
        self._backward()
        self._update()

        return _y, _loss

    def predict(self,
                x: Array,
                y: Optional[Array] = None) -> Union[Array, Tuple[Array, Array]]:
        """
        Predict Label/Target

        Parameters
        ----------
        x : vulkpy.Array
            Features
        y : vulkpy.Array, optional
            Labels/Targets.

        Returns
        -------
        pred_y : vulkpy.Array
            Predicted Labels/Targets
        loss : vulkpy.Array
            Loss. Return only if ``y`` is specified.
        """
        _y = self._forward(x)
        if y is None:
            return _y

        _loss = self.loss(_y, y)
        return _y, _loss
