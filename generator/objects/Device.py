import cons
from utilities.gen_idhash_cnt_dict import gen_idhash_cnt_dict
from utilities.cnt2prop_dict import cnt2prop_dict
from utilities.gen_shared_idhashes import gen_shared_idhashes

import numpy as np
import pandas as pd
from beartype import beartype
from typing import List, Dict, Union

class Device:
    
    @beartype
    def __init__(
        self,
        n_device_hashes:Union[int,np.int64],
        fpath_smartphones:str=cons.fpath_smartphones,
        ):
        """
        The randomly generated device data model object.
        
        Parameters
        ----------
        n_device_hashes : int
            The number of device hashes to generate.
        fpath_smartphones : str
            The file path to the smart phones reference file, default is cons.fpath_smartphones.
        
        Attributes
        ----------
        n_device_hashes : int
            The number of device hashes generated.
        lam : float
            The lambda parameter of the squared poisson distribution used to generate the device hash counts.
        power : float
            The power parameter of the squared poisson distribution used to generate the device hash counts.
        prop_shared_device_hashes : float
            The population proportion of shared device hashes.
        device_hashes_cnts_dict : Dict[str, int]
            The device hash counts dictionary.
        device_hashes_props_dict : Dict[str, float]
            The device hash proportions dictionary.
        device_hashes_type_dict : Dict[str, str]
            The device hash types dictionary.
        device_shared_idhash_map_dict : Dict[str, str]
            The device shared idhash mapping dictionary.
        """
        self.n_device_hashes = n_device_hashes
        self.fpath_smartphones = fpath_smartphones
        self.lam = cons.data_model_poisson_params["device"]["lambda"]
        self.power = cons.data_model_poisson_params["device"]["power"]
        self.prop_shared_device_hashes = cons.data_model_shared_entities_dict["device"]
        self.device_hashes_cnts_dict = gen_idhash_cnt_dict(idhash_type="hash", n=self.n_device_hashes, lam=self.lam, power=self.power)
        self.device_hashes = list(self.device_hashes_cnts_dict.keys())
        self.device_hashes_props_dict = cnt2prop_dict(idhashes_cnts_dict=self.device_hashes_cnts_dict)
        self.device_hashes_type_dict = self.gen_device_types(device_hashes=self.device_hashes, fpath_smartphones=self.fpath_smartphones)
        self.device_shared_idhash_map_dict = gen_shared_idhashes(idhashes=self.device_hashes, prop_shared_idhashes=self.prop_shared_device_hashes)

    @beartype
    def gen_device_types(
        self,
        device_hashes:List[str],
        fpath_smartphones:str,
        ) -> Dict[str, str]:
        """
        Generates a dictionary of random device types
        
        Parameters
        ----------
        device_hashes : List[str]
            The device hashes.
        fpath_smartphones : str
            The file path to the smart phones reference file.
        
        Returns
        -------
        Dict[str, str]
            A dictionary of device hash types.
        """
        # load in smartphone data
        smartphone_data = pd.read_csv(fpath_smartphones, usecols=['model','rating','os'])
        smartphone_data = smartphone_data.loc[smartphone_data['os'] == 'android', :].copy()
        # derive a proportion popularity from the ratings(TODO: expand this to be average rating per mobile phone brand)
        smartphone_data['rating'] = smartphone_data['rating'].fillna(value=smartphone_data['rating'].mean())
        smartphone_data['popularity'] =  smartphone_data['rating'] / smartphone_data['rating'].sum()
        # randomly choose different device types
        device_types = list(np.random.choice(a=smartphone_data['model'].to_list(), size=len(device_hashes), replace=True, p=smartphone_data['popularity'].to_list()))
        # return device hashes and types
        device_hashes_type_dict = dict(zip(device_hashes, device_types))
        return device_hashes_type_dict
