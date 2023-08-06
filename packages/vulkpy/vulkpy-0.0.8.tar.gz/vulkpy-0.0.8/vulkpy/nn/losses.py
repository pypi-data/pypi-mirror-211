"""
Neural Network Loss Module (:mod:`vulkpy.nn.losses`)
====================================================

Examples
--------
>>> import vulkpy as vk
>>> from vulkpy import nn
>>> gpu = vk.GPU()
>>> x = vk.Array(gpu, data=[[ ... ]]) # Predicted
>>> y = vk.Array(gpu, data=[[ ... ]]) # True

Loss class takes predicted values and true labels/targets, then returns scalar loss.

>>> L = nn.CrossEntropy()
>>> loss = L(x, y)

Gradients can be computed with `grad()` method

>>> dx = L.grad()
"""
from __future__ import annotations
from typing import cast, Callable, Iterable, Literal, Optional, Tuple

from vulkpy.util import getShader
from vulkpy.vkarray import Array, DataShape, VectorParams
from .core import Loss
from .layers import Softmax

__all__ = [
    "CrossEntropyLoss",
    "SoftmaxCrossEntropyLoss",
    "MSELoss",
    "HuberLoss",
    "MixLoss",
]


F = Callable[[Array], Array]
class ReduceLoss(Loss):
    def __init__(self, reduce: Literal["mean", "sum"] = "mean"):
        tmp: Tuple[F, Optional[F]] = {
            "mean": (lambda _L: _L.mean(axis=0), lambda _dx: 1/_dx.shape[0]),
            "sum": (lambda _L: _L.sum(axis=0), None),
        }[reduce]
        self.reduce, self.scale_backward = tmp


    def __call__(self, x: Array, y: Array) -> Array:
        r"""
        Compute Loss

        Parameters
        ----------
        x : vulkpy.Array
            Batch input features
        y : vulkpy.Array
            Batch labels/targets

        Returns
        -------
        loss : vulkpy.Array
            Loss
        """
        self._x = x
        self._y = y
        L = self.forward(x, y)
        return self.reduce(L)

    def grad(self) -> Array:
        r"""
        Compute Gradients

        Returns
        -------
        dx : vulkpy.Array
            Batch gradients of dL/dx

        Notes
        -----
        This method calculates gradients for the last ``__call__(x, y)``.
        """
        dx = self.backward()
        if self.scale_backward is not None:
            dx *= self.scale_backward(dx)
        return dx

    def forward(self, x: Array, y: Array) -> Array:
        raise NotImplementedError

    def backward(self) -> Array:
        raise NotImplementedError


class CrossEntropyLoss(ReduceLoss):
    """
    Cross Entropy Loss
    """
    _forward = getShader("nn_cross_entropy.spv")
    _backward = getShader("nn_cross_entropy_backward.spv")

    def __init__(self, *args, **kwargs):
        """
        Initialize Cross Entropy Loss

        Parameters
        ----------
        reduce : {"mean", "sum"}, optional
            Reduction method over batch. The default is ``"mean"``.
        """
        super().__init__(*args, **kwargs)

    def forward(self, x: Array, y: Array) -> Array:
        r"""
        Forward

        Parameters
        ----------
        x : vulkpy.Array
            Batch input features
        y : vulkpy.Array
            Batch input labels as One hot vector

        Returns
        -------
        loss : vulkpy.Array
            Cross Entropy Loss

        Notes
        -----
        .. math::

             L = - f _{\text{reduce}} ( y_i \log (x_i) )

        .. warning::

             Generally, users should not call this method directly.
             Use ``__call__`` instead, where input / output are stored for training.
        """
        size = x.buffer.size()
        L = Array(x._gpu, shape=x.shape)
        L.job = x._gpu._submit(self._forward, 64, 1, 1,
                               [x, y, L],
                               DataShape(size, 1, 1),
                               VectorParams(size))
        L._keep.extend([x, y])
        return L.sum(axis=1)

    def backward(self) -> Array:
        r"""
        Backward

        Returns
        -------
        loss : vulkpy.Array
           Batch gradients

        Notes
        -----
        .. math::

             dx = \frac{-y}{x + \epsilon}

        .. warning::

             Generally, users should not call this method directly.
             Use ``grad()`` instead, where reduction scale is corrected.
        """
        size = self._x.buffer.size()
        dx = Array(self._x._gpu, shape=self._x.shape)
        dx.job = self._x._gpu._submit(self._backward, 64, 1, 1,
                                      [self._x, self._y, dx],
                                      DataShape(size, 1, 1),
                                      VectorParams(size))
        dx._keep.extend([self._x, self._y])
        return dx


class SoftmaxCrossEntropyLoss(CrossEntropyLoss):
    """
    Softmax Cross Entropy Loss

    See Also
    --------
    vulkpy.nn.Softmax : Softmax layer
    vulkpy.nn.CrossEntropyLoss : Cross Entropy loss without Softmax
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize Softmax Cross Entropy Loss

        Parameters
        ----------
        reduce : {"mean", "sum"}
            Reduction method over batch. The default is ``"mean"``.
        """
        super().__init__(*args, **kwargs)
        self._sm = Softmax()

    def forward(self, x: Array, y: Array) -> Array:
        r"""
        Forward

        Parameters
        ----------
        x : vulkpy.Array
            Batch input features
        y : vulkpy.Array
            Batch labels

        Returns
        -------
        loss : vulkpy.Array
            Loss

        Notes
        -----
        .. math::

             L = - f _{\text{reduce}} (y_i \log (\rm{softmax}(x) _i))

        .. warning::

             Generally, users should not call this method directly.
             Use ``__call__`` instead, where input / output are stored for training.
        """
        return super().forward(self._sm(x), y)

    def backward(self) -> Array:
        r"""
        Backward

        Returns
        -------
        loss : vulkpy.Array
           Batch gradients

        Notes
        -----
        .. math::

             dx = \rm{softmax}(x) - y

        .. warning::

             Generally, users should not call this method directly.
             Use ``grad()`` instead, where reduction scale is corrected.
        """
        return cast(Array, self._sm._y) - self._y


class MSELoss(ReduceLoss):
    """
    Mean Squared Loss
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize MSE Loss

        Parameters
        ----------
        reduce : {"mean", "sum"}
            Reduction method over batch. The default is ``"mean"``.
        """
        super().__init__(*args, **kwargs)

    def forward(self, x: Array, y: Array) -> Array:
        r"""
        Forward

        Parameters
        ----------
        x : vulkpy.Array
            Batch input features
        y : vulkpy.Array
            Batch labels

        Returns
        -------
        loss : vulkpy.Array
            Loss

        Notes
        -----
        .. math::

             L = f _{\text{reduce}} |x - y|^2

        .. warning::

             Generally, users should not call this method directly.
             Use ``__call__`` instead, where input / output are stored for training.
        """
        L = (y - x)          # Allocate
        L **= 2.0
        return L.sum(axis=1) # Allocate

    def backward(self) -> Array:
        r"""
        Backward

        Returns
        -------
        loss : vulkpy.Array
           Batch gradients

        Notes
        -----
        .. math::

             dx = 2 (x - y)

        .. warning::

             Generally, users should not call this method directly.
             Use ``grad()`` instead, where reduction scale is corrected.
        """
        dx = self._x - self._y # Allocate
        dx *= 2
        return dx


class HuberLoss(ReduceLoss):
    """
    Huber Loss
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize Huber Loss

        Parameters
        ----------
        reduce : {"mean", "sum"}
            Reduction method over batch. The default is ``"mean"``.
        """
        super().__init__(*args, **kwargs)

    def forward(self, x: Array, y: Array) -> Array:
        r"""
        Forward

        Parameters
        ----------
        x : vulkpy.Array
            Batch input features
        y : vulkpy.Array
            Batch labels

        Returns
        -------
        loss : vulkpy.Array
            Loss

        Notes
        -----
        .. math::

             L = 0.5 f _{\text{reduce}} \min(|x - y|^2, |x - y|)

        .. warning::

             Generally, users should not call this method directly.
             Use ``__call__`` instead, where input / output are stored for training.
        """
        delta = y - x # Allocate
        delta.abs(inplace=True)               # |y-x|
        delta.min(delta ** 2.0, inplace=True) # min(|y-x|^2, |y-x|)
        delta *= 0.5                          # min(|y-x|^2, |y-x|) * 0.5
        return delta.sum(axis=1) # Allocate

    def backward(self) -> Array:
        r"""
        Backward

        Returns
        -------
        loss : vulkpy.Array
           Batch gradients

        Notes
        -----
        .. math::

             dx = \text{clamp}(x - y, -1.0, 1.0)

        .. warning::

             Generally, users should not call this method directly.
             Use ``grad()`` instead, where reduction scale is corrected.
        """
        delta = self._x - self._y
        delta.clamp(-1.0, 1.0, inplace=True)
        return delta


class MixLoss(Loss):
    """
    Mixing Loss class
    """
    def __init__(self, losses: Iterable[Tuple[float, Loss]]):
        """
        Initializer MixLoss

        Parameters
        ----------
        losses : iterable of tuple of float and vulkpy.Loss
            Sets of coefficient and loss.

        Raises
        ------
        ValueError
            When losses is empty
        """
        self.L: Tuple[Tuple[float, Loss], ...] = tuple(losses)
        if len(self.L) < 1:
            raise ValueError(f"losses should not empty")

    def __call__(self, x: Array, y: Array) -> Array:
        r"""
        Compute Loss

        Parameters
        ----------
        x : vulkpy.Array
            Batch input features
        y : vulkpy.Array
            Batch labels/targets

        Returns
        -------
        loss : vulkpy.Array
            Loss
        """
        return self._sum(lambda _L: _L(x, y))

    def grad(self) -> Array:
        r"""
        Compute Gradients

        Returns
        -------
        dx : vulkpy.Array
            Batch gradients of dL/dx

        Notes
        -----
        This method calculates gradients for the last ``__call__(x, y)``.
        """
        return self._sum(lambda _L: _L.grad())

    def _sum(self, F: Callable[[Loss], Array]) -> Array:
        coeff, _L = self.L[0]
        s = coeff * F(_L)

        for coeff, _L in self.L[1:]:
            s += coeff * F(_L)

        return s
