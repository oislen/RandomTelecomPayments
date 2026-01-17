import os
from multiprocessing import Pool
from beartype import beartype
from typing import List, Any

@beartype
def multiprocess(
    func,
    args:List[tuple],
    ncpu:int=None,
    ) -> List[Any]:
    """
    Generates a dictionary of random dates for an input dictionary of idhashes counts by utilizing multiprocessing.

    Parameters
    ----------
    func : Callable[..., Any]
        The function to be executed in parallel
    args : List[tuple]
        The input parameters as a list of tuples to be passed with the function in parallel via starmap.
    ncpu : int
        The number of cpus to execute across, default is None.

    Returns
    -------
    List[Any]
        A list of output returned from the func calls ran in parallel
    """
    # set number of cpus
    if ncpu is None:
        ncpu = os.cpu_count()
    # initialize a pool of ncpus
    results = []
    with Pool(ncpu) as pool:
        # execution given function and arguments across pool of ncpus
        results = pool.starmap(func, args)
    return results
