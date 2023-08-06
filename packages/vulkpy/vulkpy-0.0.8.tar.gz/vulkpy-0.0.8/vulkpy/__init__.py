"""
vulkpy: GPGPU array on Vulkan
=============================

vulkpy provides GPGPU computations.

See Also
--------
vulkpy.random : Random Module
vulkpy.nn : Neural Network Module
vulkpy.util : Utility Module


Examples
--------
>>> import vulkpy as vk

>>> gpu = vk.GPU()
>>> a = vk.Array(gpu, data=[1, 2, 3])
>>> b = vk.Array(gpu, data=[3, 3, 3])

>>> c = a + b
>>> print(c)
[4., 5., 6.]
"""
from .vkarray import GPU, U32Array, Shape, Array, zeros
from . import random
from . import nn
