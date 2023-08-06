import numpy as np
import numba
from numba import jit

@jit(nopython=True)
def identity(x):
    """ A no-op link function.
    """
    return x

@jit(nopython=True)
def _identity_inverse(x):
    return x
identity.inverse = _identity_inverse

@jit(nopython=True)
def logit(x):
    """ A logit link function useful for going from probability units to log-odds units.
    """
    return np.log(x/(1-x))

@jit(nopython=True)
def _logit_inverse(x):
    return 1/(1+np.exp(-x))
logit.inverse = _logit_inverse
