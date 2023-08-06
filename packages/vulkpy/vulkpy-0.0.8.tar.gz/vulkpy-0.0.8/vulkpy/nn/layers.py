"""
Neural Network Layer Module (:mod:`vulkpy.nn.layers`)
=====================================================
"""
from __future__ import annotations
from typing import Callable, Iterable, Optional

from vulkpy.util import getShader
from vulkpy.vkarray import GPU, Array, DataShape, BatchAffineParams
from .core import Module, Optimizer, Regularizer
from .parameters import Parameter
from .initializers import HeNormal


__all__ = ["Dense", "ReLU", "Sigmoid", "Softmax"]


class Dense(Module):
    """
    Fully connected Dense Layer
    """

    _batch_affine = getShader("batch_affine.spv")

    def __init__(self, gpu: GPU, input_dim: int, output_dim: int, *,
                 w_init: Optional[Callable[[GPU, Iterable[int]], Array]] = None,
                 b_init: Optional[Callable[[GPU, Iterable[int]], Array]] = None,
                 w_opt: Optional[Optimizer] = None,
                 b_opt: Optional[Optimizer] = None,
                 w_reg: Optional[Regularizer] = None,
                 b_reg: Optional[Regularizer] = None):
        """
        Initialize Dense

        Parameters
        ----------
        gpu : vulkpy.GPU
            GPU
        input_dim : int
            Input dimension
        output_dim : int
            Output dimension
        w_init Callable, optional
            Weight initializer. If ``None`` (default),
            ``vulkpy.nn.HeNormal`` is used.
        b_init Callable, optional
            Bias initializer. If ``None`` (default),
            bias is initialized with ``0``.
        w_opt : vulkpy.nn.Optimizer, optional
            Weight Optimizer. If ``None`` (default),
            ``vulkpy.nn.Adam`` is used.
        b_opt : vulkpy.nn.Optimizer, optional
            Bias Optimizer. If ``None`` (default),
            ``vulkpy.nn.Adam`` is used.
        w_reg : vulkpy.nn.Regularizer, optional
            Weight Regularizer.
        b_reg : vulkpy.nn.Regularizer, optional
            Bias Regularizer
        """
        self.input_dim = int(input_dim)
        self.output_dim = int(output_dim)

        if w_init is None:
            w_init = HeNormal(gpu, self.input_dim)

        self.w = Parameter(gpu, shape=(self.output_dim, self.input_dim),
                           initializer=w_init, opt=w_opt, regularizer=w_reg)
        self.b = Parameter(gpu, shape=(self.output_dim,),
                           initializer=b_init, opt=b_opt, regularizer=b_reg)

    def forward(self, x: Array) -> Array:
        r"""
        Forward

        Parameters
        ----------
        x : vulkpy.Array
            Batch input

        Returns
        -------
        vulkpy.Array
            Batch output

        Notes
        -----
        .. math:: y = Wx + b

        .. warning::

             Generally, users should not call this method directly.
             Use ``__call__`` instead, where input / output are stored for training.
        """
        y = Array(x._gpu, shape=(x.shape[0], self.output_dim))
        y.job = x._gpu._submit(self._batch_affine, 1, 64, 1,
                               [self.w.value, self.b.value, x, y],
                               DataShape(x.shape[0], self.output_dim, 1),
                               BatchAffineParams(x.shape[0],
                                                 x.shape[1],
                                                 self.output_dim))
        y._keep.extend([self.w.value, self.b.value, x])
        return y

    def backward(self, dy: Array) -> Array:
        r"""
        Backward

        Parameters
        ----------
        dy : vulkpy.Array
            Batch grad

        Returns
        -------
        vulkpy.Array
            Batch grad

        Notes
        -----
        .. math::

            dx = dy W\\
            dW = dy ^T \cdot x\\
            db = dy
        """
        db = dy.sum(axis=0) # Allocate
        self.b.add_grad(db)

        x_shape = self._x.shape
        dy_shape = dy.shape
        dy.reshape((dy.shape[0], dy.shape[1], 1))
        self._x.reshape((self._x.shape[0], 1, self._x.shape[1]))

        dW = dy * self._x # Allocate
        dW = dW.sum(axis=0) # Allocate
        self.w.add_grad(dW)

        self._x.reshape(x_shape)
        dy.reshape(dy_shape)

        return dy @ self.w.value # Allocate

    def zero_grad(self):
        """
        Clear accumulated gradients
        """
        self.w.zero_grad()
        self.b.zero_grad()

    def update(self):
        """
        Update values with accumulated gradients
        """
        self.w.update()
        self.b.update()


class ReLU(Module):
    """
    Rectified Linear Unit (ReLU)
    """
    def forward(self, x: Array) -> Array:
        r"""
        Forward

        Parameters
        ----------
        x : vulkpy.Array
            Batch input

        Returns
        -------
        vulkpy.Array
            Batch output

        Notes
        -----
        .. math:: y = \max(x, 0)

        .. warning::

             Generally, users should not call this method directly.
             Use ``__call__`` instead, where input / output are stored for training.
        """
        return x.max(0.0) # Allocate

    def backward(self, dy: Array) -> Array:
        r"""
        Backward

        Parameters
        ----------
        dy : vulkpy.Array
            Batch grad

        Returns
        -------
        vulkpy.Array
            Batch grad

        Notes
        -----
        .. math:: dx = dy \cdot \max(\rm{sign}(y), 0)

        if x == 0, dy/dx => 0
        """
        dx = self._y.sign() # Allocate
        dx.max(0.0, inplace=True)
        dx *= dy
        return dx


class Sigmoid(Module):
    """
    Sigmoid
    """
    def forward(self, x: Array) -> Array:
        r"""
        Forward

        Parameters
        ----------
        x : vulkpy.Array
            Batch input

        Returns
        -------
        vulkpy.Array
            Batch output

        Notes
        -----
        .. math:: y = 1/(1 + \exp (-x))

        .. warning::

             Generally, users should not call this method directly.
             Use ``__call__`` instead, where input / output are stored for training.
        """
        y = 0.0 - x # Allocate
        y.exp(inplace=True)
        y += 1.0
        y = 1.0 / y # Allocate
        return y

    def backward(self, dy: Array) -> Array:
        r"""
        Backward

        Parameters
        ----------
        dy : vulkpy.Array
            Batch grad

        Returns
        -------
        vulkpy.Array
            Batch grad

        Notes
        -----
        .. math:: dx = dy \cdot y(1 - y)
        """
        dx = 1.0 - self._y
        dx *= self._y
        dx *= dy
        return dx


class Softmax(Module):
    """
    SoftMax
    """
    def forward(self, x: Array) -> Array:
        r"""
        Forward

        Parameters
        ----------
        x : vulkpy.Array
            Batch input

        Returns
        -------
        vulkpy.Array
            Batch output

        Notes
        -----
        .. math:: y = \exp (x) / \sum _i \exp(x_i)

        .. warning::

             Generally, users should not call this method directly.
             Use ``__call__`` instead, where input / output are stored for training.
        """
        X = x - x.maximum(axis=1, rebroadcast=True)
        X.exp(inplace=True)
        X /= X.sum(axis=1, rebroadcast=True)
        return X

    def backward(self, dy: Array) -> Array:
        r"""
        Backward

        Parameters
        ----------
        dy : vulkpy.Array
            Batch grad

        Returns
        -------
        vulkpy.Array
            Batch grad

        Notes
        -----
        .. math:: dx = dy \cdot y(1 - y)
        """
        dx = 1.0 - self._y
        dx *= self._y
        dx *= dy
        return dx
