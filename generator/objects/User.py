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
        fpath_firstnames:str=cons.fpath_firstnames,
        fpath_lastnames:str=cons.fpath_lastnames,
        fpath_countrieseurope:str=cons.fpath_countrieseurope,
        fpath_domain_email:str=cons.fpath_domain_email,
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
        fpath_firstnames : str
            The full file path to the first names reference data, default is cons.fpath_firstnames.
        fpath_lastnames : str
            The full file path to the last names reference data, default is cons.fpath_lastnames.
        fpath_countrieseurope : str
            The full file path to the europe countries reference data, default is cons.fpath_countrieseurope.
        fpath_domain_email : str
            The full file path to the email domain reference data, default is cons.fpath_domain_email.
        
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
        user_ids_firstname_dict : Dict[str, str]
            The user id first names dictionary
        user_ids_lastname_dict : Dict[str, str]
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
        self.fpath_firstnames = fpath_firstnames
        self.fpath_lastnames = fpath_lastnames
        self.fpath_countrieseurope = fpath_countrieseurope
        self.fpath_domain_email = fpath_domain_email
        self.lam = cons.data_model_poisson_params["user"]["lambda"]
        self.power = cons.data_model_poisson_params["user"]["power"]
        self.user_ids_cnts_dict = gen_idhash_cnt_dict(idhash_type="id", n=self.n_user_ids, lam=self.lam, power=self.power)
        self.user_ids = list(self.user_ids_cnts_dict.keys())
        self.user_ids_props_dict = cnt2prop_dict(idhashes_cnts_dict=self.user_ids_cnts_dict)
        self.user_ids_country_code_dict = gen_country_codes_dict(idhashes_cnts_dict=self.user_ids_cnts_dict, fpath_countrieseurope=self.fpath_countrieseurope)
        self.user_ids_firstname_dict = self.gen_user_firstname(fpath_firstnames=self.fpath_firstnames)
        self.user_ids_lastname_dict = self.gen_user_lastname(fpath_lastnames=self.fpath_lastnames)
        self.user_ids_email_domain_dict = self.gen_user_email_domain(fpath_domain_email=self.fpath_domain_email)
        self.user_ids_dates_dict = gen_dates_dict(idhashes_cnts_dict=self.user_ids_cnts_dict, start_date=self.start_date, end_date=self.end_date)
    
    @beartype
    def gen_user_firstname(
        self,
        fpath_firstnames:str,
        ) -> Dict[str, str]:
        """
        Generates a dictionary of random user id first names
        
        Parameters
        ----------
        fpath_firstnames : str
            The file path to the first names reference file
        
        Returns
        -------
        Dict[str, str]
            A dictionary of user id first names
        """
        # load in list of first names
        first_name_data = pd.read_csv(fpath_firstnames)
        # randomly sample names firstnames according to country code and counts
        country_code_dataframe = pd.Series(self.user_ids_country_code_dict, name="country_code").to_frame().reset_index().rename(columns={"index":"user_ids"}).assign(count=1)
        country_codes_cnt = country_code_dataframe.groupby(by="country_code").agg({"user_ids":list,"count":"sum"}).reset_index()
        country_codes_cnt["names"] = country_codes_cnt.apply(lambda series: first_name_data.loc[(first_name_data["ISO numeric"] == series["country_code"]), "firstnames"].sample(n=series["count"], replace=True).to_list(), axis=1)
        # create the key value pairs mapping user id to firstname
        user_ids_names_pairs = country_codes_cnt.apply(lambda series: dict(zip(series["user_ids"], series["names"])), axis=1).to_list()
        # convert key value pairs to dict
        user_ids_firstname_dict = pd.concat([pd.Series(d) for d in user_ids_names_pairs])[country_code_dataframe["user_ids"]].to_dict()
        return user_ids_firstname_dict
    
    @beartype
    def gen_user_lastname(
        self,
        fpath_lastnames:str,
        ) -> Dict[str, str]:
        """
        Generates a dictionary of random user id last names.
        
        Parameters
        ----------
        fpath_lastnames : str
            The file path to the last names reference file.
        
        Returns
        -------
        Dict[str, str]
            A dictionary of user id last names.
        """
        # load in list of last names
        last_name_data = pd.read_csv(fpath_lastnames)
        # randomly sample names firstnames according to country code and counts
        country_code_dataframe = pd.Series(self.user_ids_country_code_dict, name="country_code").to_frame().reset_index().rename(columns={"index":"user_ids"}).assign(count=1)
        country_codes_cnt = country_code_dataframe.groupby(by="country_code").agg({"user_ids":list,"count":"sum"}).reset_index()
        country_codes_cnt["names"] = country_codes_cnt.apply(lambda series: last_name_data.loc[(last_name_data["ISO numeric"] == series["country_code"]), "lastnames"].sample(n=series["count"], replace=True).to_list(), axis=1)
        # create the key value pairs mapping user id to firstname
        user_ids_names_pairs = country_codes_cnt.apply(lambda series: dict(zip(series["user_ids"], series["names"])), axis=1).to_list()
        # convert key value pairs to dict
        user_ids_lastname_dict = pd.concat([pd.Series(d) for d in user_ids_names_pairs])[country_code_dataframe["user_ids"]].to_dict()
        return user_ids_lastname_dict
    
    @beartype
    def gen_user_email_domain(
        self,
        fpath_domain_email:str,
        ) -> Dict[str, str]:
        """
        Generates a dictionary of random user id email domains
        
        Parameters
        ----------
        fpath_domain_email : str
            The file path to the email domains reference file
        
        Returns
        -------
        Dict[str, str]
            A dictionary of user id email domains
        """
        # load domain names data
        email_domain_data = pd.read_csv(fpath_domain_email, index_col=0)
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
