import cons
from utilities.cnt2prop_dict import cnt2prop_dict

import os
import numpy as np
import pandas as pd
from beartype import beartype
from typing import Dict, Union

@beartype
def gen_country_codes_dict(
    idhashes_cnts_dict:Dict[str, Union[int, np.int64]],
    fpath_countrieseurope:str=cons.fpath_countrieseurope,
    ) -> Dict[str, Union[int, np.int64]]:
    """
    Generates a dictionary of randomLy sampled country codes for an input dictionary of idhashes counts.
    
    Parameters
    ----------
    idhashes_cnts_dict : Dict[str, Union[int, np.int64]]
        A dictionary of idhashes counts.
    fpath_countrieseurope : str
        The file path to the european countries reference file, default is cons.fpath_countrieseurope.
    
    Returns
    -------
    Dict[str, Union[int, np.int64]]
        A dictionary of idhashes country codes.
    
    Examples
    --------
    ```
    import cons
    idhashes_cnts_dict:{'abcd1234': 5, 'defg4567': 3, 'ghij7891': 7}
    gen_country_codes_dict(idhashes_cnts_dict=idhashes_cnts_dict,
        fpath_countrieseurope=cons.fpath_countrieseurope,
        )
    ```
    """
    # check file path exists
    if os.path.exists(fpath_countrieseurope) == False:
        raise FileNotFoundError(f"File not found: {fpath_countrieseurope}")
    # load population data of european countries
    european_populations_cnt_data = pd.read_csv(filepath_or_buffer=fpath_countrieseurope, usecols=["ISO numeric", "population"],)
    # convert to a dictionary of ISO country codes with population counts
    european_populations_cnt_dict = european_populations_cnt_data.set_index("ISO numeric")["population"].to_dict()
    # convert dictionary of population counts to dictionary of population proportions
    european_populations_props_dict = cnt2prop_dict(european_populations_cnt_dict)
    # extract out idhashes from idhashes counts dictionary
    idhashes_list = list(idhashes_cnts_dict.keys())
    # check population proportions sum to 1.0
    if np.isclose(sum(european_populations_props_dict.values()), 1.0) == False:
        raise ValueError("Population proportions do not sum to 1.0")
    # randomly generate country codes for all idhashes based on population proportions
    country_codes_list = list(
        np.random.choice(
            a=list(european_populations_props_dict.keys()),
            p=list(european_populations_props_dict.values()),
            replace=True,
            size=len(idhashes_list),
        )
    )
    # return a dictionary of idhashes and country codes
    idhashes_country_codes = dict(zip(idhashes_list, country_codes_list))
    return idhashes_country_codes
