import random
import numpy as np
import pandas as pd
from beartype import beartype

@beartype
def align_country_codes(
    series:pd.Series,
    proba_comm_ip:float=0.05,
    proba_comm_card:float=0.01,
    ) -> pd.Series:
    """
    Aligns inconsistent registration, ip and card country codes to have mostly common values; with a random chance of inconsistencies.
    
    Parameters
    ----------
    series : pandas.Series
        A series from the random transaction dataframe with inconsistent country codes to align.
    proba_comm_ip : float
        The probability of a common / shared registration country code and ip country code, default is 0.05.
    proba_comm_card : float
        The probability of a common / shared registration country code and card country code, default is 0.01.
    
    Returns
    -------
    pandas.Series
        A pandas series containing only the aligned country codes; registration, ip and card.
    
    Examples
    --------
    ```
    series = pd.Series({'registration_country_code_alpha': 353.0, 'ip_country_code_alpha': 42.0, 'card_country_code_alpha': 42.0})
    align_country_codes(series=series, proba_comm_ip=0.05, proba_comm_card=0.01,)
    ```
    """
    # generate random value between 0 and 1
    random_unif = random.uniform(0, 1)
    # extract country codes from input series
    registration_country_code = series["registration_country_code_alpha"]
    ip_country_code = series["ip_country_code_alpha"]
    card_country_code = series["card_country_code_alpha"]
    # determine shared or new ip country code
    if pd.notna(ip_country_code):
        if random_unif <= proba_comm_ip:
            new_ip_country_code = ip_country_code
        else:
            new_ip_country_code = registration_country_code
    else:
        new_ip_country_code = np.nan
    # determine shared or new card country code
    if pd.notna(card_country_code):
        if random_unif <= proba_comm_card:
            new_card_country_code = card_country_code
        else:
            new_card_country_code = registration_country_code
    else:
        new_card_country_code = np.nan
    # return aligned codes
    align_code_dict = {
        "registration_country_code_alpha": registration_country_code,
        "ip_country_code_alpha": new_ip_country_code,
        "card_country_code_alpha": new_card_country_code,
    }
    aligned_code_series = pd.Series(align_code_dict)
    return aligned_code_series
