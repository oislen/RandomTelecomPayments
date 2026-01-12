import cons
from utilities.gen_idhash_cnt_dict import gen_idhash_cnt_dict
from utilities.cnt2prop_dict import cnt2prop_dict
from utilities.gen_dates_dict import gen_dates_dict
from utilities.round_trans_amount import round_trans_amount

import numpy as np
from beartype import beartype
from typing import List, Dict, Union

class Transaction:
    
    @beartype
    def __init__(
        self,
        n_transaction_hashes:Union[int,np.int64],
        start_date:str,
        end_date:str,
        ):
        """
        The randomly generated transaction data model object.
        
        Parameters
        ----------
        n_transaction_hashes : int
            The number of transaction hashes to generate.
        start_date : str
            The start date to generate transactions from.
        end_date : str
            The end date to generate transaction till.
        
        Attributes
        ----------
        n_transaction_hashes : int
            The number of transaction hashes generated.
        start_date : str
            The date transactions are generated from, must be of the form '%Y-%m-%d'.
        end_date : str
            The date transactions are generated till, must be of the form '%Y-%m-%d'.
        lam : float
            The lambda parameter of the squared poisson distribution used to generate the transaction hash counts.
        power : float
            The power parameter of the squared poisson distribution used to generate the transaction hash counts.
        transaction_status : Dict[str, float]
            The population proportion of transaction statuses.
        transaction_hashes_cnts_dict : Dict[str, int]
            The transaction hash counts dictionary.
        transaction_hashes_props_dict : Dict[str, float]
            The transaction hash proportions dictionary.
        transaction_hashes_dates_dict : Dict[str, str]
            The transaction hash dates dictionary.
        transaction_hashes_status_dict : Dict[str, str]
            The transaction hash status dictionary.
        transaction_hashes_amounts_dict : Dict[str, float]
            The transaction hash amount dictionary.
        """
        self.n_transaction_hashes = n_transaction_hashes
        self.start_date = start_date
        self.end_date = end_date
        self.lam = cons.data_model_poisson_params["transaction"]["lambda"]
        self.power = cons.data_model_poisson_params["transaction"]["power"]
        self.transaction_status = cons.data_model_transaction_status
        self.transaction_hashes_cnts_dict = gen_idhash_cnt_dict(idhash_type="hash", n=self.n_transaction_hashes, lam=self.lam, power=self.power)
        self.transaction_hashes = list(self.transaction_hashes_cnts_dict.keys())
        self.transaction_hashes_props_dict = cnt2prop_dict(idhashes_cnts_dict=self.transaction_hashes_cnts_dict)
        self.transaction_hashes_dates_dict = gen_dates_dict(idhashes_cnts_dict=self.transaction_hashes_cnts_dict,start_date=self.start_date,end_date=self.end_date,)
        self.transaction_hashes_status_dict = self.gen_transaction_status(transaction_hashes=self.transaction_hashes, transaction_status=self.transaction_status)
        self.transaction_hashes_amounts_dict = self.gen_transaction_amounts(transaction_hashes=self.transaction_hashes, loc=0, scale=2)
    
    @beartype
    def gen_transaction_status(
        self,
        transaction_hashes:List[str],
        transaction_status:Dict[str, float],
        ):
        """
        Generates a dictionary of random transaction statuses
        
        Parameters
        ----------
        transaction_hashes : List[str]
            The transaction hashes
        transaction_status : Dict[str, float]
            The population proportion of transaction statuses
        
        Returns
        -------
        Dict[str, str]
            A dictionary of transaction statuses
        """
        # randomly sample transaction status based on population proportions
        transaction_status = list(
            np.random.choice(
                a=list(transaction_status.keys()),
                p=list(transaction_status.values()),
                replace=True,
                size=len(transaction_hashes),
            )
        )
        # return transaction hashes and statuses
        transaction_hashes_status_dict = dict(zip(transaction_hashes, transaction_status))
        return transaction_hashes_status_dict
    
    @beartype
    def gen_transaction_amounts(
        self,
        transaction_hashes:List[str],
        loc:Union[int, float]=0,
        scale:Union[int, float]=2,
        ) -> Dict[str, float]:
        """
        Generates a dictionary of random transaction hash amounts.
        
        Parameters
        ----------
        transaction_hashes : List[str]
            The transaction hashes.
        loc : float
            The mean of the transaction amount distribution to generate, default is 0.
        scale : float
            The scale of the transaction amount distribution to generate, default is 2.
        
        Returns
        -------
        Dict[str, float]
            A dictionary of transaction hash prices
        """
        # randomly sample transaction prices from an absolute normal distribution with mean 0 and standard deviation 2
        trans_prices = np.round(np.abs(np.random.normal(loc=loc, scale=scale, size=len(transaction_hashes)))** 2,2,)
        # return the transaction hashes and prices
        trans_prices_dict = dict(zip(transaction_hashes, round_trans_amount(trans_prices)))
        return trans_prices_dict