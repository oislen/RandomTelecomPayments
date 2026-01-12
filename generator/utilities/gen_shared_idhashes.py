import numpy as np
import pandas as pd
from beartype import beartype

@beartype
def gen_shared_idhashes(
    idhashes_cnts_dict:dict,
    prop_shared_idhashes:float
    ) -> dict:
    """
    Generates a dictionary of shared idhashes proportions

    Parameters
    ----------
    idhashes_cnts_dict : dict
        A dictionary of idhashes counts.
    prop_shared_idhashes : float
        The total proportion of shared idhashes.

    Returns
    -------
    dict
        A dictionary of shared idhashes proportion.
    """
    # calculate the total number of idhashes
    n_idhashes = len(idhashes_cnts_dict)
    # randomly sample the idhashes based on the total proportion of shared idhashes
    shared_idhashes_list = list(
        np.random.choice(
            a=list(idhashes_cnts_dict.keys()),
            size=int(np.round(n_idhashes * prop_shared_idhashes)),
            replace=False
        )
    )
    shared_idhash_map_dict = {}
    if shared_idhashes_list != []:
        # determine how many networks
        n_groups = int(np.floor(np.sqrt(len(shared_idhashes_list))))
        group_uniform_dict = {g:np.random.uniform() for g in range(n_groups)}
        group_prop_dict = {key:value/sum(group_uniform_dict.values()) for key, value in group_uniform_dict.items()}
        # generate groups for all shared id hashes
        shared_idhashes_groups_list = list(np.random.choice(a=list(group_prop_dict.keys()), size=len(shared_idhashes_list), replace=True, p=list(group_prop_dict.values())))
        shared_idhashes_groups_dict = dict(zip(shared_idhashes_list, shared_idhashes_groups_list))
        shared_idhashes_groups_df = pd.Series(shared_idhashes_groups_dict, name="shared_idhashes_group").to_frame().reset_index().rename(columns={'index':'idhash'})
        shared_entity_groups_dict = shared_idhashes_groups_df.groupby('shared_idhashes_group').agg({'idhash':list}).to_dict()['idhash']
        shared_idhashes_groups_df['shared_idhash'] = shared_idhashes_groups_df.apply(lambda series: np.random.choice(a=shared_entity_groups_dict[series['shared_idhashes_group']]), axis=1)
        # create the shared idhash map dictionary
        shared_idhash_map_dict = shared_idhashes_groups_df.set_index('idhash')['shared_idhash'].to_dict()
    return shared_idhash_map_dict
