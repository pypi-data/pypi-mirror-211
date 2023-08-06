import numpy as np
from scipy.special import logsumexp


def logtrapz(log_y, x=None, dx=1.0, axis=-1):
    """
    Integrate y values that are given in log space.

    Parameters
    ----------
    log_y : array_like
        Natural logarithm of input `n`-dimensional array to integrate.
    x : array_like, optional
        The sample points corresponding to the `log_y` values.
        If `x` is None, the sample point are assumed to be evenly spaced `dx` apart.
        The default is None.
    dx : scalar, optional
        The spacing between the sample points when `x` is None.
        The default is 1.
    axis : int, optional
        The axis along which to integrate.

    Returns
    -------
    float or ndarray
        Natural logarithm of the definite integral of `exp(log_y)`.
        If `log_y` is a 1-dimensional array, then the result is a float.
        If `n` is greater than 1, then the result is an `n`-1 dimensional array.
    """

    # This first part is taken from np.trapz
    # https://github.com/numpy/numpy/blob/v1.24.0/numpy/lib/function_base.py#L4773-L4884

    log_y = np.asanyarray(log_y)
    nd = log_y.ndim

    if x is None:
        d = dx
    else:
        x = np.asanyarray(x)
        if x.ndim == 1:
            d = np.diff(x)
            shape = [1] * nd
            shape[axis] = d.shape[0]
            d = d.reshape(shape)
        else:
            d = np.diff(x, axis=axis)

    slice1 = [slice(None)] * nd
    slice2 = [slice(None)] * nd
    slice1[axis] = slice(1, None)
    slice2[axis] = slice(None, -1)
    slice1 = tuple(slice1)
    slice2 = tuple(slice2)

    # Now we write the trapezoidal rule in log space

    log_integrand = logsumexp([log_y[slice1], log_y[slice2]], axis=0) + np.log(d)
    log_integral = logsumexp(log_integrand, axis=axis) - np.log(2)

    return log_integral


