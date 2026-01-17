import pandas as pd
import numpy as np
from datetime import datetime
from beartype import beartype
from typing import Dict, Union, List

@beartype
def gen_dates_dict(
    idhashes:List[str],
    start_date:str,
    end_date:str,
    ) -> Dict[str, Union[pd.Timestamp, np.datetime64]]:
    """
    Generates a dictionary of random dates for an input list of idhashes.

    Parameters
    ----------
    idhashes : List[str]
        A list of idhashes.
    start_date : str
        The start date ("%Y-%m-%d") to generate random dates from.
    end_date : str
        The end date ("%Y-%m-%d") to generate random dates till.

    Returns
    -------
    Dict[str, Union[pd.Timestamp,int, np.datetime64]]
        A dictionary of idhashes dates.
    
    Examples
    --------
    ```
    idhashes = ['2e23f63807f6170a', 'b8816ed926bf9f83', 'b010fdb44fa68822']
    gen_dates_dict(idhashes=idhashes, start_date='2020-01-01', end_date='2023-01-01')
    ```
    """
    # generate a range of dates between the given input start and end dates
    dates = pd.date_range(start=datetime.strptime(start_date, "%Y-%m-%d"), end=datetime.strptime(end_date, "%Y-%m-%d"), freq="d", inclusive="both",)
    # randomly sample dates for each of the idhashes
    dates_list = list(np.random.choice(a=dates, replace=True, size=len(idhashes)))
    # return a dictionary of idhashes and dates
    idhashes_dates_dict = dict(zip(idhashes, dates_list))
    return idhashes_dates_dict
