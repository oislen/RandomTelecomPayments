import string
import numpy as np
from beartype import beartype
from typing import Union, List

@beartype
def gen_random_hash(
    size:Union[int,np.int64],
    nbytes:int=16,
    ) -> List[str]:
    """
    Generates a list of random hashes.
    
    Parameters
    ----------
    size : int
        The total number of hashes to generate.
    nbytes : int
        The number of alphanumeric values in each hash, default is 16.
    
    Returns
    -------
    list
        A list of random hashes.
    
    Examples
    --------
    ```
    gen_random_hash(size=5, nbytes=16)
    ```
    """
    # generate a list of digits and lower case letters from string library
    alphanumeric = list(string.digits) + list(string.ascii_lowercase)[:6]
    # randomly sample nbytes digits, string concatenate and convert to integers
    random_hashes = [''.join(row) for row in np.random.choice(a=alphanumeric, size=(size, nbytes), replace=True).tolist()]
    return random_hashes
