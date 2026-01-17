from utilities.gen_random_hash import gen_random_hash
from utilities.gen_random_id import gen_random_id
from utilities.gen_random_poisson_power import gen_random_poisson_power

import numpy as np
from beartype import beartype
from typing import Union, Dict

@beartype
def gen_idhash_cnt_dict(
    idhash_type:str,
    n:Union[int,np.int64],
    lam:Union[int,float],
    nbytes:int=16,
    power:int=2,
    ) -> Dict[str, Union[str, int, np.int64]]:
    """
    Generates a dictionary of n random idhashes and associated counts.
    
    Parameters
    ----------
    idhash_type : str
        Whether to generate a "id" or "hash" value.
    n : int
        The total number of idhash values to generate.
    lam : float
        The lambda value to sample n poisson count values with.
    nbytes : int
        The number bytes to include in the idhash value, default is 16.
    power : int
        The power of the polynomial random poisson variable, default is 2.
    
    Returns
    -------
    Dict[str, Union[str, int, np.int64]]
        A dictionary of idhashes counts.
    
    Examples
    --------
    ```
    import cons
    gen_idhash_cnt_dict(
        idhash_type="hash",
        n=10,
        lam=5.0,
        nbytes=16,
        power=2,
        )
    ```
    """
    # if generating a random hash value
    if idhash_type == "hash":
        idhash_list = gen_random_hash(size=n, nbytes=nbytes)
    # else if generating a random id value
    elif idhash_type == "id":
        idhash_list = gen_random_id(size=n, nbytes=nbytes)
    else:
        raise ValueError("idhash_type must be either 'id' or 'hash'")
    # randomly sample n counts from a squared poisson distribution with given lam value
    cnts_list = gen_random_poisson_power(lam=lam, size=n, power=power).tolist()
    # return a dictionary of idhashes and counts
    if len(idhash_list) != len(set(idhash_list)):
        raise ValueError("Generated idhash values are not unique, please increase nbytes value")
    idhash_dict = dict(zip(idhash_list, cnts_list))
    return idhash_dict
