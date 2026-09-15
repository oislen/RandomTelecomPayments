import numpy as np


def gen_trans_error_codes(trans_data, trans_status_col, rejection_codes):
    """Generates transaction error codes

    Parameters
    ----------
    trans_data : pandas.DataFrame
        Random transaction data
    trans_status_col : str
        The transaction status column name in trans_data
    rejection_codes : dict
        A dictionary of rejection codes and assoicated proportions

    Returns
    -------
    pandas.Series
        The transaction rejection codes data
    """
    # take a deep copy of the dataframe
    tmp_data = trans_data.copy()
    # create an empty transaction error code column
    tmp_data["transaction_error_code"] = np.nan
    # create a filter for only the rejected transactions
    failed_transactions_filter = tmp_data[trans_status_col] == "rejected"
    # randomly sample rejection codes for the rejected transactions
    random_error_codes = np.random.choice(
        a=list(rejection_codes.keys()),
        p=list(rejection_codes.values()),
        size=failed_transactions_filter.sum(),
        replace=True,
    )
    # assign the rejection codes to the transaction error code column
    tmp_data.loc[failed_transactions_filter, "transaction_error_code"] = (
        random_error_codes
    )
    return tmp_data["transaction_error_code"]
