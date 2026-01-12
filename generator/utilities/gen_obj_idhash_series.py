import pandas as pd
from beartype import beartype
from typing import List

@beartype
def gen_obj_idhash_series(
    idhashes:List[str],
    n_counts_series:pd.Series
    ) -> pd.Series:
    """
    Generates a series of entity idhash lists using the entity counts per user Series and idhashes list.
    
    Parameters
    ----------
    idhashes : List[str]
        The idhashes list.
    n_counts_series : pd.Series
        The entity counts for each uid as Series.
    
    Returns
    -------
    pd.Series
        A Series of lists containing entity idhashes  for each user.
    """
    # create an exploded series for idhashes within the entity object
    obj_idhash_series = pd.Series(data=idhashes, index=n_counts_series.index.repeat(n_counts_series.values).to_list())
    # group by uid index and collate idhashes as lists
    obj_idhash_agg = obj_idhash_series.groupby(level=0).apply(list)
    return obj_idhash_agg