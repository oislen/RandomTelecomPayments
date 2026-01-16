import string
import numpy as np
from beartype import beartype
from typing import Union, List

@beartype
def gen_random_id(
    size:Union[int,np.int64],
    nbytes:int=16,
    ) -> List[str]:
    """
    Generates a list of random ids.
    
    Parameters
    ----------
    size : int
        The total number of ids to generate.
    nbytes : int
        The number of numeric values in each id, default is 16.
    
    Returns
    -------
    list
        A list of random ids.
    
    Examples
    --------
    ```
    gen_random_id(size=5, nbytes=16)
    ```
    """
    # generate a list of digits from string library
    digits = list(string.digits)
    # randomly sample nbytes digits, string concatenate
    random_ids = ["".join(row) for row in np.random.choice(a=digits, size=(size, nbytes), replace=True).tolist()]
    return random_ids
