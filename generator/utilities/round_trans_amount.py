import numpy as np
from beartype import beartype

@beartype
def round_trans_amount(amounts:np.ndarray) -> np.ndarray:
    """
    Rounds transaction amounts to have store price like remainders such as 1.99, 3.45, and 2.5.
    
    Parameters
    ----------
    amounts : np.ndarray
        The transaction amounts to round.
    
    Returns
    -------
    np.array
        The rounded transaction amounts with store price like remainders.
    
    Examples
    --------
    ```
    import numpy as np
    amounts = np.array([2.34, 5.67, 3.21])
    round_trans_amount(amounts=amounts)
    ```
    """
    # a probability distribution for remainders
    round_dict = {0.01:0.4, 0.5:0.1, 0.45:0.1, 0.51:0.1, 0.41:0.1, 0.71:0.1, 1:0.1}
    remainder = np.random.choice(a=list(round_dict.keys()), size=amounts.shape[0], replace=True, p=list(round_dict.values()))
    rounded_amounts =np.maximum(0, np.round(np.ceil(amounts) - remainder, 2))
    return rounded_amounts