import pandas as pd
import numpy as np
from datetime import datetime
from beartype import beartype
from typing import Dict, Union

@beartype
def gen_dates_dict(
    idhashes_cnts_dict:Dict[str, Union[str, int, np.int64]],
    start_date:str,
    end_date:str,
    ) -> Dict[str, Union[pd.Timestamp, np.datetime64]]:
    """
    Generates a dictionary of random dates for an input dictionary of idhashes counts.

    Parameters
    ----------
    idhashes_cnts_dict : Dict[str, Union[str, np.int64]]
        A dictionary of idhashes counts.
    start_date : str
        The start date ("%Y-%m-%d") to generate random dates from.
    end_date : str
        The end date ("%Y-%m-%d") to generate random dates till.

    Returns
    -------
    Dict[str, Union[pd.Timestamp,int, np.datetime64]]
        A dictionary of idhashes dates.
    """
    # generate a range of dates between the given input start and end dates
    dates = pd.date_range(start=datetime.strptime(start_date, "%Y-%m-%d"), end=datetime.strptime(end_date, "%Y-%m-%d"), freq="d", inclusive="both",)
    # extract out the idhashes from idhashes counts dictionary
    idhashes_list = list(idhashes_cnts_dict.keys())
    # randomly sample dates for each of the idhashes
    dates_list = list(np.random.choice(a=dates, replace=True, size=len(idhashes_list)))
    # return a dictionary of idhashes and dates
    idhashes_dates_dict = dict(zip(idhashes_list, dates_list))
    return idhashes_dates_dict
