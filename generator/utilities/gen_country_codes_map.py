import cons

import numpy as np
import pandas as pd
from beartype import beartype
from typing import Dict, Union

@beartype
def gen_country_codes_map(
    fpath_countries_europe:str=cons.fpath_countries_europe,
    ) -> Dict[int, Union[str, np.int64]]:
    """
    Generates a dictionary of ISO numeric codes mapping to ISO alpha codes.
    
    Parameters
    ----------
    fpath_countries_europe : str
        The full file path to the european countries reference file, default is cons.fpath_countries_europe.
    
    Returns
    -------
    Dict[int, Union[str, np.int64]]
        A dictionary of ISO numeric codes mapping to ISO alpha codes.
    
    Examples
    --------
    ```
    import cons
    gen_country_codes_map(fpath_countries_europe=cons.fpath_countries_europe)
    ```
    """
    # load european county codes data
    country_codes_data = pd.read_csv(filepath_or_buffer=fpath_countries_europe, usecols=["ISO numeric", "ISO alpha 2"],)
    # convert data to a dictionary of ISO numeric codes mapping to ISO alpha codes
    country_codes_map = country_codes_data.set_index("ISO numeric")["ISO alpha 2"].to_dict()
    return country_codes_map
