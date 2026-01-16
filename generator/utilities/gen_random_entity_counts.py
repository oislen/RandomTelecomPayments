import cons
from objects.User import User
from utilities.gen_random_poisson_power import gen_random_poisson_power

import numpy as np
import pandas as pd
from beartype import beartype

@beartype
def gen_random_entity_counts(
    user_obj:User,
    transaction_timescale:float=1.0,
    ) -> pd.DataFrame:
    """
    Generates a dataframe of entity counts for all users from a given user object.
    
    Parameters
    ----------
    user_obj : User
        The User class object.
    transaction_timescale : float
        The transaction timescale where 1.0 is a single year of transactions, default is 1.0.
    
    Returns
    -------
    pd.DataFrame
        A dataframe of entity counts for all users from the specified user object.
    
    Examples
    --------
    ```
    from objects.User import User
    user_obj=User(n_user_ids=1000, start_date='2020-01-01', end_date='2023-01-01')
    gen_random_entity_counts(user_obj=user_obj, transaction_timescale=1.0)
    ```
    """
    # create an empty pandas dataframe to hold the random aggregated data
    random_entity_counts = pd.DataFrame()
    # randomly sample from the random user uids
    random_entity_counts["uid"] = np.random.choice(a=user_obj.user_ids, size=user_obj.n_user_ids, replace=False)
    # randomly simulate the number of entities per user
    for object_type in cons.object_types:
        random_entity_counts[f"n_{object_type}s"] = gen_random_poisson_power(lam = cons.data_model_poisson_params[object_type]["lambda"], size = user_obj.n_user_ids, power = cons.data_model_poisson_params[object_type]["power"])
    # scale n transactions by
    random_entity_counts["n_transactions"] = (random_entity_counts["n_transactions"] * transaction_timescale).astype(int)
    return random_entity_counts
