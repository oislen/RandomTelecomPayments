import cons
from utilities.gen_idhash_cnt_dict import gen_idhash_cnt_dict
from utilities.cnt2prop_dict import cnt2prop_dict
from utilities.gen_country_codes_dict import gen_country_codes_dict
from utilities.gen_dates_dict import gen_dates_dict

import numpy as np
import pandas as pd
from beartype import beartype
from typing import Dict

class User:
    
    @beartype
    def __init__(
        self,
        n_user_ids:int,
        start_date:str,
        end_date:str,
        fpath_first_names:str=cons.fpath_llama_first_names,
        fpath_last_names:str=cons.fpath_llama_last_names,
        fpath_countries_europe:str=cons.fpath_countries_europe,
        fpath_email_domain:str=cons.fpath_email_domain,
        fpath_bedrock_email_domain:str=cons.fpath_llama_email_domains,
        ):
        """
        The randomly generated user data model object
        
        Parameters
        ----------
        n_user_ids : int
            The number of user uids to generate
        start_date : str
            The start date to generate users from
        end_date : str
            The end date to generate users till
        fpath_first_names : str
            The full file path to the first names reference data, default is cons.fpath_llama_first_names.
        fpath_last_names : str
            The full file path to the last names reference data, default is cons.fpath_llama_last_names.
        fpath_countries_europe : str
            The full file path to the europe countries reference data, default is cons.fpath_countries_europe.
        fpath_email_domain : str
            The full file path to the email domain reference data, default is cons.fpath_llama_email_domains .
        
        Attributes
        ----------
        n_user_ids : int
            The number of user ids generated
        start_date : str
            The date user ids are generated from, must be of the form '%Y-%m-%d'
        end_date : str
            The date user ids are generated till, must be of the form '%Y-%m-%d'
        lam : float
            The lambda parameter of the squared poisson distribution used to generate the user ids counts
        power : float
            The power parameter of the squared poisson distribution used to generate the user ids counts
        user_ids_cnts_dict : Dict[str, int]
            The user id counts dictionary
        user_ids_props_dict : Dict[str, float]
            The user id proportions dictionary
        user_ids_first_name_dict : Dict[str, str]
            The user id first names dictionary
        user_ids_last_name_dict : Dict[str, str]
            The user id last names dictionary
        user_ids_country_code_dict : Dict[str, str]
            The user id country codes dictionary
        user_ids_email_domain_dict : Dict[str, str]
            The user id email domains dictionary
        user_ids_dates_dict : Dict[str, str]
            The user id dates dictionary
        """
        self.n_user_ids = n_user_ids
        self.start_date = start_date
        self.end_date = end_date
        self.fpath_first_names = fpath_first_names
        self.fpath_last_names = fpath_last_names
        self.fpath_countries_europe = fpath_countries_europe
        self.fpath_email_domain = fpath_email_domain
        self.fpath_bedrock_email_domain = fpath_bedrock_email_domain
        self.lam = cons.data_model_poisson_params["user"]["lambda"]
        self.power = cons.data_model_poisson_params["user"]["power"]
        self.user_ids_cnts_dict = gen_idhash_cnt_dict(idhash_type="id", n=self.n_user_ids, lam=self.lam, power=self.power)
        self.user_ids = list(self.user_ids_cnts_dict.keys())
        self.user_ids_props_dict = cnt2prop_dict(idhashes_cnts_dict=self.user_ids_cnts_dict)
        self.user_ids_country_code_dict = gen_country_codes_dict(idhashes=self.user_ids, fpath_countries_europe=self.fpath_countries_europe)
        self.user_ids_first_name_dict = self.gen_user_bedrock_name_data(fpath_first_names=self.fpath_first_names, sample_column_name="first_names")
        self.user_ids_last_name_dict = self.gen_user_bedrock_name_data(fpath_last_names=self.fpath_last_names, sample_column_name="last_names")
        self.user_ids_email_domain_dict = self.gen_user_email_domain(fpath_email_domain=self.fpath_email_domain, fpath_bedrock_email_domain=self.fpath_bedrock_email_domain)
        self.user_ids_dates_dict = gen_dates_dict(idhashes=self.user_ids, start_date=self.start_date, end_date=self.end_date)
    
    @beartype
    def gen_user_bedrock_name_data(
        self,
        fpath_bedrock_data:str,
        sample_column_name:str,
        ) -> Dict[str, str]:
        """
        Generates a dictionary of random user bedrock data, e.g. first_names or last_names
        
        Parameters
        ----------
        fpath_bedrock_data : str
            The file path to the bedrock data reference file
        sample_column_name : str
            The column name to sample from in the bedrock data reference file
        
        Returns
        -------
        Dict[str, str]
            A dictionary of user id bedrock data
        """
        # load in list of first names
        bedrock_data = pd.read_csv(fpath_bedrock_data)
        # randomly sample names first_names according to country code and counts
        country_code_dataframe = pd.Series(self.user_ids_country_code_dict, name="country_code").to_frame().reset_index().rename(columns={"index":"user_ids"}).assign(count=1)
        country_codes_cnt = country_code_dataframe.groupby(by="country_code").agg({"user_ids":list,"count":"sum"}).reset_index()
        country_codes_cnt["sample"] = country_codes_cnt.apply(lambda series: bedrock_data.loc[(bedrock_data["ISO numeric"] == series["country_code"]), sample_column_name].sample(n=series["count"], replace=True, weights=None).to_list(), axis=1)
        # create the key value pairs mapping user id to bedrock data points
        user_ids_bedrock_pairs = country_codes_cnt.apply(lambda series: dict(zip(series["user_ids"], series["sample"])), axis=1).to_list()
        # convert key value pairs to dict
        user_ids_bedrock_dict = pd.concat([pd.Series(d) for d in user_ids_bedrock_pairs])[country_code_dataframe["user_ids"]].to_dict()
        return user_ids_bedrock_dict
    
    @beartype
    def gen_user_bedrock_email_domain(
        self,
        fpath_email_domain:str,
        fpath_bedrock_email_domain:str,
        ) -> Dict[str, str]:
        """
        Generates a dictionary of random user id email domains
        
        Parameters
        ----------
        fpath_email_domain : str
            The file path to the email domains reference file
        
        Returns
        -------
        Dict[str, str]
            A dictionary of user id email domains
        """
        # load domain names data
        email_domain_data = pd.read_csv(fpath_email_domain, index_col=0)
        # calculate the proportion of email domains
        email_domain_data["proportion"] = email_domain_data["proportion"].divide(email_domain_data["proportion"].sum())
        # convert email domain proportions to a dictionary
        email_domain_dict = email_domain_data.set_index("domain").to_dict()["proportion"]
        # randomly choose the email domains based on proportions
        user_email_domain_list = list(
            np.random.choice(
                a=list(email_domain_dict.keys()),
                p=list(email_domain_dict.values()),
                replace=True,
                size=len(self.user_ids),
            )
        )
        # return the user ids email domains
        user_ids_email_domain_dict = dict(zip(self.user_ids, user_email_domain_list))
        return user_ids_email_domain_dict