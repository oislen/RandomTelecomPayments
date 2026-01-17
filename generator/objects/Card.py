import cons
from utilities.gen_idhash_cnt_dict import gen_idhash_cnt_dict
from utilities.cnt2prop_dict import cnt2prop_dict
from utilities.gen_country_codes_dict import gen_country_codes_dict
from utilities.gen_shared_idhashes import gen_shared_idhashes

import numpy as np
from beartype import beartype
from typing import List, Dict, Union

class Card:
    
    @beartype
    def __init__(
        self,
        n_card_hashes:Union[int,np.int64],
        fpath_countries_europe:str=cons.fpath_countries_europe,
        ):
        """
        The randomly generated card data model object.
        
        Parameters
        ----------
        n_card_hashes : int
            The number of card hashes to generate.
        fpath_countries_europe : str
            The file path to the european countries reference file, default is cons.fpath_countries_europe.
        
        Attributes
        ----------
        n_card_hashes : int
            The number of card hashes generated.
        card_types_dict : Dict[str, float]
            The population proportions of card types.
        lam : float
            The lambda parameter of the squared poisson distribution used to generate the card hash counts.
        power : float
            The power parameter of the squared poisson distribution used to generate the card hash counts.
        prop_shared_card_hashes : float
            The population proportion of shared card hashes.
        card_hashes_cnts_dict : Dict[str, int]
            The card hash counts dictionary.
        card_hashes_props_dict : Dict[str, float]
            The card hash proportions dictionary.
        card_hashes_type_dict : Dict[str, str]
            The card hash types dictionary.
        card_hashes_country_code_dict : Dict[str, str]
            The card hash country codes dictionary.
        card_shared_idhash_map_dict : Dict[str, str]
            The card shared idhash mapping dictionary.
        """
        self.n_card_hashes = n_card_hashes
        self.fpath_countries_europe = fpath_countries_europe
        self.card_types_dict = cons.data_model_card_types_dict
        self.lam = cons.data_model_poisson_params["card"]["lambda"]
        self.power = cons.data_model_poisson_params["card"]["power"]
        self.prop_shared_card_hashes = cons.data_model_shared_entities_dict["card"]
        self.card_hashes_cnts_dict = gen_idhash_cnt_dict(idhash_type="hash", n=self.n_card_hashes, lam=self.lam, power=self.power)
        self.card_hashes = list(self.card_hashes_cnts_dict.keys())
        self.card_hashes_props_dict = cnt2prop_dict(idhashes_cnts_dict=self.card_hashes_cnts_dict)
        self.card_hashes_type_dict = self.gen_card_type(card_hashes=self.card_hashes, card_types_dict=self.card_types_dict)
        self.card_hashes_country_code_dict = gen_country_codes_dict(idhashes=self.card_hashes, fpath_countries_europe=self.fpath_countries_europe)
        self.card_shared_idhash_map_dict = gen_shared_idhashes(idhashes=self.card_hashes, prop_shared_idhashes=self.prop_shared_card_hashes)
    
    @beartype
    def gen_card_type(
        self,
        card_hashes:List[str],
        card_types_dict:Dict[str, float],
        ) -> Dict[str, str]:
        """
        Generates a dictionary of random card types.
        
        Parameters
        ----------
        card_hashes : List[str]
            The card hashes.
        card_types_dict : Dict[str, float]
            The population proportions of card types.
        
        Returns
        -------
        Dict[str, str]
            A dictionary of card types.
        """
        # randomly choose card types based on the population proportions of card types
        card_types = np.random.choice(
            a=list(card_types_dict.keys()),
            p=list(card_types_dict.values()),
            size=len(card_hashes),
            replace=True,
        )
        # return the card hashes and card types
        card_hashes_type_dict = dict(zip(card_hashes, card_types))
        return card_hashes_type_dict
