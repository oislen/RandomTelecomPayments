import numpy as np
import pandas as pd
from beartype import beartype
from typing import Dict, Union, List

@beartype
def gen_shared_idhashes(
    idhashes:List[str],
    prop_shared_idhashes:float
    ) -> Dict[str, str]:
    """
    Generates a dictionary of shared idhashes proportions
    
    Parameters
    ----------
    idhashes : list of str
        A list of idhashes.
    prop_shared_idhashes : float
        The total proportion of shared idhashes.
    
    Returns
    -------
    Dict[str, str]
        A dictionary  idhashes and their shared idhashes.
    
    Examples
    --------
    ```
    idhashes=['2e23f63807f6170a', 'b8816ed926bf9f83', 'b010fdb44fa68822']
    gen_shared_idhashes(idhashes=idhashes, prop_shared_idhashes=0.01)
    ```
    """
    # calculate the total number of idhashes
    n_idhashes = len(idhashes)
    # randomly sample the idhashes based on the total proportion of shared idhashes
    shared_idhashes_list = np.random.choice(
        a=idhashes,
        size=int(np.round(n_idhashes * prop_shared_idhashes)),
        replace=False
    ).tolist()
    shared_idhash_map_dict = {}
    if (shared_idhashes_list != []):
        # determine how many networks
        n_groups = int(np.ceil(np.sqrt(len(shared_idhashes_list))))
        group_uniform_dict = {g:np.random.uniform() for g in range(n_groups)}
        group_prop_dict = {key:value/sum(group_uniform_dict.values()) for key, value in group_uniform_dict.items()}
        # generate groups for all shared id hashes
        shared_idhashes_groups_list = list(np.random.choice(a=list(group_prop_dict.keys()), size=len(shared_idhashes_list), replace=True, p=list(group_prop_dict.values())))
        shared_idhashes_groups_dict = dict(zip(shared_idhashes_list, shared_idhashes_groups_list))
        shared_idhashes_groups_df = pd.Series(shared_idhashes_groups_dict, name="shared_idhashes_group").to_frame().reset_index().rename(columns={'index':'idhash'})
        shared_entity_groups_dict = shared_idhashes_groups_df.groupby('shared_idhashes_group').agg({'idhash':list}).to_dict()['idhash']
        shared_idhashes_groups_df['shared_idhash'] = [np.random.choice(shared_entity_groups_dict[group]) for group in shared_idhashes_groups_df['shared_idhashes_group']]
        # create the shared idhash map dictionary
        shared_idhash_map_dict = shared_idhashes_groups_df.set_index('idhash')['shared_idhash'].to_dict()
    return shared_idhash_map_dict
