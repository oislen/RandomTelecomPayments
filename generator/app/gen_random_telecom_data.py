import numpy as np
import pandas as pd
from typing import Dict
import random
from beartype import beartype

from app.ProgrammeParams import ProgrammeParams
from app.gen_user_data import gen_user_data
from app.gen_trans_data import gen_trans_data
from objects.Application import Application
from objects.Card import Card
from objects.Device import Device
from objects.Ip import Ip
from objects.Transaction import Transaction
from objects.User import User
from utilities.gen_random_entity_counts import gen_random_entity_counts
import cons

@beartype
def gen_random_telecom_data(
    n_users:int=1,
    random_seed:int=None,
    n_applications:int=20000,
    registration_start_date:str=cons.default_registration_start_date,
    registration_end_date:str=cons.default_registration_end_date,
    transaction_start_date:str=cons.default_transaction_start_date,
    transaction_end_date:str=cons.default_transaction_end_date,
    ) -> Dict[str, pd.DataFrame]:
    """
    Generates random telecommunications data.
    
    Parameters
    ----------
    n_users : int
        The number of users to generate random telecom payments data for, default is 1.
    random_seed : int
        A set random seed for reproducible results, default is None.
    n_applications : int
        The number of applications to generate, default is 20000.
    registration_start_date : str
        The user registration start date, default is cons.default_registration_start_date.
    registration_end_date : str
        The user registration end date, default is cons.default_registration_end_date.
    transaction_start_date : str
        The user transaction start date, default is cons.default_transaction_start_date.
    transaction_end_date : str
        The user transaction end date, default is cons.default_transaction_end_date.
    
    Returns
    -------
    Dict[str, pandas.DataFrame]
        A random telecommunication payments dataset.
    """
    
    # initalise programme parameters
    programmeparams = ProgrammeParams(
        n_users=n_users,
        random_seed=random_seed,
        n_applications=n_applications,
        registration_start_date=registration_start_date,
        registration_end_date=registration_end_date,
        transaction_start_date=transaction_start_date,
        transaction_end_date=transaction_end_date
        )
    
    # set random seed
    random.seed(programmeparams.random_seed)
    np.random.seed(seed=programmeparams.random_seed)
    
    # generate random users
    user_obj = User(
        n_user_ids=programmeparams.n_users,
        start_date=programmeparams.registration_start_date,
        end_date=programmeparams.registration_end_date,
        fpath_first_names=cons.fpath_llama_first_names,
        fpath_last_names=cons.fpath_llama_last_names,
        fpath_countries_europe=cons.fpath_countries_europe,
        fpath_email_domain=cons.fpath_email_domain,
        fpath_bedrock_email_domain=cons.fpath_llama_email_domains
        )
    
    # generate random entity counts for each user
    random_entity_counts = gen_random_entity_counts(
        user_obj=user_obj,
        transaction_timescale=programmeparams.transaction_timescale
        )
    
    # generate random entity values
    device_obj = Device(n_device_hashes=random_entity_counts['n_devices'].sum())
    card_obj = Card(n_card_hashes=random_entity_counts['n_cards'].sum())
    ip_obj = Ip(n_ip_hashes=random_entity_counts['n_ips'].sum())
    transaction_obj = Transaction(n_transaction_hashes=random_entity_counts['n_transactions'].sum(), start_date=programmeparams.transaction_start_date, end_date=programmeparams.transaction_end_date)
    application_obj = Application(n_application_hashes=programmeparams.n_applications)
    
    # generate user level data
    user_data = gen_user_data(
        random_entity_counts=random_entity_counts,
        user_obj=user_obj,
        device_obj=device_obj,
        card_obj=card_obj,
        ip_obj=ip_obj,
        transaction_obj=transaction_obj,
        application_obj=application_obj,
    )
    
    # generate transaction level data
    trans_data = gen_trans_data(
        user_data=user_data,
        user_obj=user_obj,
        device_obj=device_obj,
        card_obj=card_obj,
        ip_obj=ip_obj,
        transaction_obj=transaction_obj,
        application_obj=application_obj,
        fpath_countrycrimeindex=cons.fpath_countrycrimeindex
    )
    
    # map np.nans to None for JSON serialisation
    user_data = user_data.where(pd.notnull(user_data), None)
    trans_data = trans_data.where(pd.notnull(trans_data), None)
    
    return {"user_data":user_data, "trans_data":trans_data}
