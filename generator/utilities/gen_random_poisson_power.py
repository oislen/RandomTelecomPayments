import numpy as np
from beartype import beartype
from typing import Union

@beartype
def gen_random_poisson_power(
    lam:Union[int,float],
    size:Union[int,np.int64],
    power:int
    ) -> np.ndarray:
    """
    Generates data from a polynomial random poisson variable to a given power.
    
    Parameters
    ----------
    lam : int,float
        The lambda of the underlying poisson random variable.
    size : int
        The number of values to generate.
    power : int
        The power of the polynomial sum.
    
    Returns
    -------
    numpy.ndarray
        The random sum of powered poisson values.
    
    Examples
    --------
    ```
    gen_random_poisson_power(lam=3.0, size=10, power=2)
    ```
    """
    # randomly generate a square poisson distribution
    a = np.array([np.random.poisson(lam, size) ** p for p in range(1, power+1)]).sum(axis = 0) + 1
    return a
