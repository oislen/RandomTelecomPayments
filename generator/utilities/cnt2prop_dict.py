from beartype import beartype
from typing import Dict

@beartype
def cnt2prop_dict(
    idhash_cnt_dict:Dict[str, int],
    ) -> Dict[str, float]:
    """
    Converts a dictionary of counts to a dictionary of proportions.
    
    Parameters
    ----------
    idhash_cnt_dict : dict
        A dictionary of key, value pairs where the value indicates a count.
    
    Returns
    -------
    dict
        A dictionary of key, value pairs where the value indicates a proportion.
    
    Examples
    --------
    ```
    idhash_cnt_dict = {'7125135c8882b0f6': 2, '049dd291d9506532': 3, 'd6708d344cb6f498': 5}
    prop_dict = cnt2prop_dict(idhash_cnt_dict=idhash_cnt_dict)
    ```
    """
    # empty dictionary for proportions
    prop_dict = {}
    if idhash_cnt_dict != {}:
        # sum of dictionary counts
        cnt_total = sum(idhash_cnt_dict.values())
        # iterate over input dictionary and convert counts to proportions
        prop_dict = {idhash: cnt / cnt_total for idhash, cnt in idhash_cnt_dict.items()}
    return prop_dict
