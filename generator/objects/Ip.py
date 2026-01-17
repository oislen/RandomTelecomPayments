import cons
from utilities.gen_idhash_cnt_dict import gen_idhash_cnt_dict
from utilities.cnt2prop_dict import cnt2prop_dict
from utilities.gen_country_codes_dict import gen_country_codes_dict
from utilities.gen_shared_idhashes import gen_shared_idhashes

import numpy as np
from beartype import beartype
from typing import Union

class Ip:
    
    @beartype
    def __init__(
        self,
        n_ip_hashes:Union[int,np.int64],
        fpath_countries_europe:str=cons.fpath_countries_europe,
        ):
        """
        The randomly generated ip data model object.
        
        Parameters
        ----------
        n_ip_hashes : int
            The number of ip hashes to generate.
        fpath_countries_europe : str
            The file path to the european countries reference file, default is cons.fpath_countries_europe.
        
        Attributes
        ----------
        n_ip_hashes : int
            The number of ip hashes generated.
        lam : float
            The lambda parameter of the squared poisson distribution used to generate the ip hash counts.
        power : float
            The power parameter of the squared poisson distribution used to generate the ip hash counts.
        prop_shared_ip_hashes : float
            The population proportion of shared ip hashes.
        ip_hashes_cnts_dict : Dict[str, int]
            The ip hash counts dictionary.
        ip_hashes_props_dict : Dict[str, float]
            The ip hash proportions dictionary.
        ip_hashes_country_code_dict : Dict[str, str]
            The ip hash country codes dictionary.
        ip_shared_idhash_map_dict  : Dict[str, str]
            The shared ip hash mapping dictionary.
        """
        self.n_ip_hashes = n_ip_hashes
        self.fpath_countries_europe = fpath_countries_europe
        self.lam = cons.data_model_poisson_params["ip"]["lambda"]
        self.power = cons.data_model_poisson_params["ip"]["power"]
        self.prop_shared_ip_hashes = cons.data_model_shared_entities_dict["ip"]
        self.ip_hashes_cnts_dict = gen_idhash_cnt_dict(idhash_type="hash", n=self.n_ip_hashes, lam=self.lam, power=self.power)
        self.ip_hashes = list(self.ip_hashes_cnts_dict.keys())
        self.ip_hashes_props_dict = cnt2prop_dict(idhashes_cnts_dict=self.ip_hashes_cnts_dict)
        self.ip_hashes_country_code_dict = gen_country_codes_dict(idhashes=self.ip_hashes, fpath_countries_europe=self.fpath_countries_europe)
        self.ip_shared_idhash_map_dict = gen_shared_idhashes(idhashes=self.ip_hashes, prop_shared_idhashes=self.prop_shared_ip_hashes)