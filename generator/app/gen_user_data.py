import pandas as pd
import numpy as np
from beartype import beartype

from objects.User import User
from objects.Device import Device
from objects.Card import Card
from objects.Ip import Ip
from objects.Transaction import Transaction
from objects.Application import Application
from utilities.gen_obj_idhash_series import gen_obj_idhash_series
from utilities.join_idhashes_dict import join_idhashes_dict
from utilities.gen_random_hash import gen_random_hash

@beartype
def gen_user_data(
    random_entity_counts:pd.DataFrame,
    user_obj:User,
    device_obj:Device,
    card_obj:Card,
    ip_obj:Ip,
    transaction_obj:Transaction,
    application_obj:Application
    ) -> pd.DataFrame:
    """
    Generates random user level telecom payments data

    Parameters
    ----------
    random_entity_counts : pd.DataFrame
        The randomly generated entities count data
    user_obj : User
        The random user data model object
    device_obj : Device
        The random device data model object
    card_obj : Card
        The random card data model object
    ip_obj : Ip
        The random ip data model object
    transaction_obj : Transaction
        The random transaction data model object
    application_obj : Application
        The random application data model object

    Returns
    -------
    pandas.DataFrame
        The random user level telecom payments data
    """
    # take a deep copy of the data
    user_data = random_entity_counts.copy()
    # add user data
    user_data = join_idhashes_dict(data=user_data, idhashes_dict=user_obj.user_ids_first_name_dict, idhash_key_name='uid', idhash_val_name='first_name')
    user_data = join_idhashes_dict(data=user_data, idhashes_dict=user_obj.user_ids_last_name_dict, idhash_key_name='uid', idhash_val_name='last_name')
    user_data = join_idhashes_dict(data=user_data, idhashes_dict=user_obj.user_ids_dates_dict, idhash_key_name='uid', idhash_val_name='registration_date')
    user_data = join_idhashes_dict(data=user_data, idhashes_dict=user_obj.user_ids_country_code_dict, idhash_key_name='uid', idhash_val_name='registration_country_code_alpha')
    user_data = join_idhashes_dict(data=user_data, idhashes_dict=user_obj.user_ids_email_domain_dict, idhash_key_name='uid', idhash_val_name='email_domain')
    userid_date_country_code = user_data['registration_date'].dt.strftime('%Y%m%d') + user_data['registration_country_code_alpha'].astype(str)
    zero_pad = (userid_date_country_code.str.len() - 11).abs().apply(lambda x: '0'*x)
    user_data['userid'] = userid_date_country_code + zero_pad + user_data['uid'].astype(str).str[-5:]
    # add hash data lists
    user_data['device_hash'] = gen_obj_idhash_series(idhashes=device_obj.device_hashes, n_counts_series=user_data['n_devices'])
    user_data['card_hash'] = gen_obj_idhash_series(idhashes=card_obj.card_hashes, n_counts_series=user_data['n_cards'])
    user_data['ip_hash'] = gen_obj_idhash_series(idhashes=ip_obj.ip_hashes, n_counts_series=user_data['n_ips'])
    user_data['transaction_hash'] = gen_obj_idhash_series(idhashes=transaction_obj.transaction_hashes, n_counts_series=user_data['n_transactions'])
    # generate application hashes per user
    #user_data['application_hash'] = user_data['n_applications'].apply(lambda x: list(np.random.choice(a = list(application_obj.application_hashes_props_dict.keys()), p = list(application_obj.application_hashes_props_dict.values()), replace = True, size = x)))
    total_application_hashes = user_data['n_applications'].sum()
    split_indices = user_data['n_applications'].cumsum()[:-1].values
    application_hashes = np.random.choice(a = list(application_obj.application_hashes_props_dict.keys()), p=list(application_obj.application_hashes_props_dict.values()), replace=True, size=total_application_hashes)
    user_data['application_hash'] = pd.Series(np.split(application_hashes, split_indices)).apply(lambda x: x.tolist())
    # drop excess columns
    user_data = user_data.drop(columns = ['n_devices', 'n_cards', 'n_ips', 'n_applications', 'n_transactions'])
    # create a hash value for the dataset (to distinguish between different iterations)
    user_data['itr_hash'] = gen_random_hash(size=1)[0]
    return user_data