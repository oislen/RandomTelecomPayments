import numpy as np
import pandas as pd
from beartype import beartype

@beartype
def remove_duplicate_idhashes(
    user_data:pd.DataFrame,
    idhash_col:str,
    ):
    """
    Removes duplicate idhashes from a given idhash column.
    
    Parameters
    ----------
    user_data : pandas.DataFrame
        The user level telecom payments data.
    idhash_col : str
        The column with duplicate idhashes to be removed.
    
    Returns
    -------
    pandas.DataFrame
        A user level telecom data with the duplicate idhashes removed from the specified idhash column.
    """
    # take deep copy of the data
    tmp_data = user_data.copy()
    # explode out the series of lists and deduplicate values
    tmp_deduplicated_series = tmp_data[idhash_col].explode().drop_duplicates()
    # roll up and redistribute the idhashes
    tmp_deduplicate_series=tmp_deduplicated_series.groupby(level=0).apply(lambda series: series.to_list())
    # overwrite series with empty lists
    tmp_data[idhash_col] = np.nan
    tmp_data[idhash_col] = tmp_deduplicate_series
    tmp_data[idhash_col] = tmp_data[idhash_col].apply(lambda x: x if pd.notnull(x) else [])
    return tmp_data
