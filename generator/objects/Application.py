import cons
from utilities.gen_idhash_cnt_dict import gen_idhash_cnt_dict
from utilities.cnt2prop_dict import cnt2prop_dict

import numpy as np
from beartype import beartype
from typing import List, Dict

class Application:
    
    @beartype
    def __init__(
        self,
        n_application_hashes:int,
        ):
        """
        Initialize the Application object with randomly generated data model.
        
        Parameters
        ----------
        n_application_hashes : int
            The number of application hashes to generate.
        
        Attributes
        ----------
        n_application_hashes : int
            The number of application hashes generated.
        lam : float
            The lambda parameter for the Poisson distribution used to generate application hash counts.
        power : float
            The power parameter for the Poisson distribution.
        payment_channels : Dict[str, float]
            The population proportions of available payment channels.
        application_hashes_cnts_dict : Dict[str, int]
            Mapping of application hashes to their occurrence counts.
        application_hashes_props_dict : Dict[str, float]
            Mapping of application hashes to their proportions.
        application_hashes_payment_channel_dict : Dict[str, str]
            Mapping of application hashes to randomly assigned payment channels.
        """
        self.n_application_hashes = n_application_hashes
        self.lam = cons.data_model_poisson_params["application"]["lambda"]
        self.power = cons.data_model_poisson_params["application"]["power"]
        self.payment_channels = cons.data_model_payment_channels
        self.application_hashes_cnts_dict = gen_idhash_cnt_dict(idhash_type="hash", n=self.n_application_hashes, lam=self.lam)
        self.application_hashes_props_dict = cnt2prop_dict(self.application_hashes_cnts_dict)
        self.application_hashes_payment_channel_dict = self.gen_transaction_payment_channel(list(self.application_hashes_cnts_dict.keys()), self.payment_channels)
    
    @beartype
    def gen_transaction_payment_channel(
        self,
        application_hashes:List[str],
        payment_channels:Dict[str, float],
        ) -> Dict[str, str]:
        """
        Generates a dictionary of random application payment channels.
        
        Parameters
        ----------
        application_hashes : List[str]
            The application hashes.
        payment_channels : Dict[str, float]
            The population proportion of payment channels.
        
        Returns
        -------
        Dict[str, str]
            A dictionary of transaction payment channels.
        """
        # randomly sample payment channels based on population proportions
        transaction_payment_channels = list(
            np.random.choice(
                a=list(payment_channels.keys()),
                p=list(payment_channels.values()),
                replace=True,
                size=len(application_hashes),
            )
        )
        # return payment channels and application hashes
        application_hashes_payment_channels_dict = dict(zip(application_hashes, transaction_payment_channels))
        return application_hashes_payment_channels_dict
