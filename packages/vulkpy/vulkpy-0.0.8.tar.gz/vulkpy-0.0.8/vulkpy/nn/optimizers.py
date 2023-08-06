"""
Neural Network Optimizer Module (:mod:`vulkpy.nn.optimizers`)
=============================================================
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Union

from wblog import getLogger

from vulkpy.vkarray import GPU, Array, zeros
from .core import Optimizer, OptimizerState

__all__ = [
    "SGD", "SGDState",
    "AdaGrad", "AdaGradState",
    "Adam", "AdamState",
    "Optimizer", "OptimizerState",
]

logger = getLogger()


class SGDState(OptimizerState):
    """
    Optimizer State for SGD
    """
    def __init__(self, opt: SGD):
        """
        Initialize SGD state

        Parameters
        ----------
        opt : vulkpy.SGD
            SGD Optimizer
        """
        self.opt: SGD = opt

    def grad2diff(self, grad: Array) -> Array:
        """
        Compute diff from gradient

        Parameters
        ----------
        grad : vulkpy.Array
            Gradient

        Returns
        -------
        diff : vulkpy.Array
            Update diff
        """
        return (-self.opt.lr) * grad

class SGD(Optimizer):
    """
    SGD Optimizer

    Use constant learning rate

    See Also
    --------
    vulkpy.nn.Adam : Adam optimizer
    """
    def __init__(self, lr: float):
        """
        Initialize Stachostic Gradient Decent (SGD) Optimizer

        Parameters
        ----------
        lr : float
            Learning rate
        """
        self.lr: float = lr
        logger.debug("SGD(lr=%f)", self.lr)

    def init_state(self, shape: Iterable[int]) -> SGDState:
        """
        Initialize Optimizer state

        Parameters
        ----------
        shape : iterable of ints
            Shape of parameter

        Returns
        -------
        SGDState
            Optimizer state

        Notes
        -----
        Currently SGDState is empty, however,
        we might add some field like momentum in future.
        """
        return SGDState(self)


class AdaGradState(OptimizerState):
    """
    Optimizer State for AdaGrad
    """
    def __init__(self, opt: AdaGrad, shape: Iterable[int], tau: float):
        """
        Initialize AdaGrad

        Parameters
        ----------
        opt : vulkpy.AdaGrad
            AdaGrad Optimizer
        shape : iterable of ints
            Value shape
        tau : float
            Initial summation
        """
        self.opt: AdaGrad = opt
        self.h: Array = zeros(self.opt.gpu, shape=shape)
        self.h[:] = tau

    def grad2diff(self, grad: Array) -> Array:
        """
        Compute diff from gradient

        Parameters
        ----------
        grad : vulkpy.Array
            Gradient

        Returns
        -------
        diff : vulkpy.Array
            Update diff
        """
        self.h += (grad ** 2)

        sqrt = self.h.sqrt()  #               sqrt(sum)
        sqrt += self.opt.eps  #               sqrt(sum) + eps
        ret = grad / sqrt     #       grad / (sqrt(sum) + eps)
        ret *= (-self.opt.lr) # -lr * grad / (sqrt(sum) + eps)
        return ret

class AdaGrad(Optimizer):
    r"""
    AdaGrad Optimizer

    Notes
    -----
    This class implement AdaGrad [adagrad1]_.

    References
    ----------
    .. [adagrad1]
    """
    def __init__(self,
                 gpu: GPU, *,
                 lr: float = 0.01,
                 tau: float = 0.0,
                 eps: float = 1e-8):
        """
        Initialize AdaGrad

        Parameters
        ----------
        gpu : vulkpy.GPU
            GPU
        lr : float, optional
            AdaGrad parameter (learning rate). The default is ``0.01``.
        tau : float, optional
            AdaGrad parameter (initialial accumulator).
            The default is ``0``.
        eps : float, optional
            AdaGrad parameter (small positive).
            The default is ``1e-8``
        """
        self.gpu: GPU = gpu
        self.lr: float = lr
        self.tau: float = tau
        self.eps: float = eps

        logger.debug("AdaGrad(lr=%f, tau=%f, eps=%f)",
                     self.lr, self.tau, self.eps)

    def init_state(self, shape: Iterable[int]) -> AdaGradState:
        """
        Initialize Optimizer state

        Parameters
        ----------
        shape : iterable of ints
            Shape of parameter

        Returns
        -------
        AdaGradState
            Optimizer state
        """
        return AdaGradState(opt=self, shape=shape, tau=self.tau)


class AdamState(OptimizerState):
    """
    Optimizer State for Adam
    """
    def __init__(self, opt: Adam, shape: Iterable[int]):
        """
        Initialize Adam state

        Parameters
        ----------
        opt : vulkpy.Adam
            Adam Optimizer
        shape : iterable of ints
            Value shape
        """
        self.opt: Adam = opt
        self.m: Array = zeros(self.opt.gpu, shape=shape)
        self.v: Array = zeros(self.opt.gpu, shape=shape)
        self.beta1t: float = 1.0
        self.beta2t: float = 1.0

    def grad2diff(self, grad: Array) -> Array:
        """
        Compute diff from gradient

        Parameters
        ----------
        grad : vulkpy.Array
            Gradient

        Returns
        -------
        diff : vulkpy.Array
            Update diff
        """
        self.m *= self.opt.beta1
        self.m += (1 - self.opt.beta1) * grad        # Allocate

        self.v *= self.opt.beta2
        self.v += (1 - self.opt.beta2) * (grad ** 2) # Allocate

        self.beta1t *= self.opt.beta1
        self.beta2t *= self.opt.beta2

        mhat = self.m / (1 - self.beta1t) # Allocate
        vhat = self.v / (1 - self.beta2t) # Allocate

        vhat.sqrt(inplace=True) # sqrt(vhat)
        vhat += self.opt.eps    # sqrt(vhat) + eps

        mhat *= (-self.opt.lr)  # -lr * mhat
        mhat /= vhat            # -lr * mhat / (sqrt(vhat) + eps)

        return mhat


class Adam(Optimizer):
    r"""
    Adam Optimizer

    See Also
    --------
    vulkpy.nn.SGD : SGD optimizer

    Notes
    -----
    This class implement Adam [adam1]_.
    The algorithm utilizes moving averages of the 1st and 2nd order moment.
    The 1st (:math:`m_t`) and 2nd (:math:`v_t`) order moment are updated as follows;

    .. math::

         m_t = \beta _1 m_{t-1} + (1 - \beta _1) g_t\\
         v_t = \beta _2 v_{t-1} + (1 - \beta _2) g_t ^2

    where :math:`g_t` is gradient.

    To mitigate initial underestimation,
    corrected :math:`\hat{m_t}` and :math:`\hat{v_t}` are used for parameter update.

    .. math::

         \hat{m}_t = m_t / (1 - \beta _1 ^t)\\
         \hat{v}_t = v_t / (1 - \beta _2 ^t)

    Finally, parameter :math:`\theta _t` is updated by

    .. math::

         \theta _t = \theta _{t-1} - \text{lr} \times
         \hat{m}_t/(\sqrt{\hat{v}_t} + \epsilon)


    References
    ----------
    .. [adam1] D. Kingma and J. Ba, "Adam: A Method for Stochastic Optimization",
       ICLR (Poster) 2015, https://dblp.org/rec/journals/corr/KingmaB14.html

    Examples
    --------
    >>> import vulkpy.vk
    >>> from vulkpy import nn
    >>> gpu = vk.GPU()
    >>> adam = nn.Adam(gpu, lr=0.001, beta1=0.9, beta2=0.999)
    """
    def __init__(self,
                 gpu: GPU, *,
                 lr: float = 0.001,
                 beta1: float = 0.9,
                 beta2: float = 0.999,
                 eps: float = 1e-8):
        """
        Initialize Adam Optimizer

        Parameters
        ----------
        gpu : vulkpy.GPU
            GPU
        lr : float, optional
            Adam parameter. The default is ``0.001``.
        beta1 : float, optional
            Adam parameter. The default is ``0.9``.
        beta2 : float, optional
            Adam parameter. The defeault is ``0.999``.
        eps : float, optional
            Adam parameter. The default is ``1e-8``.
        """
        self.gpu: GPU = gpu
        self.lr: float = lr
        self.beta1: float = beta1
        self.beta2: float = beta2
        self.eps: float = eps

        logger.debug("Adam(lr=%f, beta1=%f, beta2=%f, eps=%f)",
                     self.lr, self.beta1, self.beta2, self.eps)

    def init_state(self, shape: Iterable[int]) -> AdamState:
        """
        Initialize Optimizer state

        Parameters
        ----------
        shape : iterable of ints
            Shape of parameter

        Returns
        -------
        AdamState
            Optimizer state
        """
        return AdamState(opt=self, shape=shape)
