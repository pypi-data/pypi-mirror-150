""" FuelMap utility tools
"""

from math import ceil, floor
import numpy as np

try:
    from numba import njit

    has_numba = True
except ImportError:
    has_numba = False
    print("WARNING: Failed to find numba, loop acceleration will be not activated")
    pass


def njit_wrapper(function):
    if has_numba:
        return njit()(function)
    else:
        return function


@njit_wrapper
def fill_fuel_array_from_patch(fuelarray, patchmask, propertyvector, np, nx, ny):
    """Fill fuel array considering a mask

    Parameters
    ----------

    fuelarray : numpy.ndarray
        Array to modify according to `propertyvector` and `patchmask`.
    patchmask : numpy.ndarray
        Mask array.
    propertyvector : numpy.ndarray
        Vector of properties to fill in the fuel array.
    np : int
        Property vector size
    nx : int
        Fire mesh size on x axis
    ny : int
        Fire mesh size on y axis

    Returns
    -------

    fuelarray : numpy.ndarray
        Modified array according to `propertyvector` and `patchmask`.
    """
    # property loop
    for k in range(np):
        # y axis loop
        for j in range(ny):
            # x axis loop
            for i in range(nx):
                # check mask value
                if patchmask[j, i] == 1:
                    fuelarray[k, j, i] = propertyvector[k]
    return fuelarray


@njit_wrapper
def fire_array_2d_to_3d(firearray2d, nx, ny, gammax, gammay):
    """Reshape 2d fire array into 3d fire array readable by MesoNH

    Parameters
    ----------
    firearray2d : numpy.ndarray
        2d array to reshape
    nx : int
        Fire mesh size on x axis
    ny : int
        Fire mesh size on y axis
    gammax : int
        Fire mesh refinement on x axis
    gammay : int
        Fire mesh refinement on x axis

    Returns
    -------
    firearray3d : numpy.ndarray
        Reshaped 3d array
    """
    farray3d = np.zeros((gammax * gammay, ny, nx))
    for m in range(1, ny * gammay + 1):
        for l in range(1, nx * gammax + 1):
            # compute i,j,k
            i = ceil(float(l) / float(gammax))
            j = ceil(float(m) / float(gammay))
            a = l - (i - 1) * gammax
            b = m - (j - 1) * gammay
            k = (b - 1) * gammax + a

            # fill tables
            farray3d[k - 1, j - 1, i - 1] = firearray2d[m - 1, l - 1]
    return farray3d


@njit_wrapper
def fire_array_3d_to_2d(firearray3d, nx, ny, gammax, gammay):
    """Reshape 3d fire array readable by MesoNH to 2d fire array

    Parameters
    ----------
    firearray3d : numpy.ndarray
        3d array to reshape
    nx : int
        Fire mesh size on x axis
    ny : int
        Fire mesh size on y axis
    gammax : int
        Fire mesh refinement on x axis
    gammay : int
        Fire mesh refinement on x axis

    Returns
    -------
    firearray2d : numpy.ndarray
        Reshaped 2d array
    """
    farray2d = np.zeros((ny * gammay, nx * gammax))
    for k in range(1, gammax * gammay + 1):
        b = floor((k - 1) / gammax) + 1
        a = k - (b - 1) * gammax
        for j in range(1, ny + 1):
            m = (j - 1) * gammay + b
            for i in range(1, nx + 1):
                l = (i - 1) * gammax + a
                farray2d[m - 1, l - 1] = firearray3d[k - 1, j - 1, i - 1]
    return farray2d
