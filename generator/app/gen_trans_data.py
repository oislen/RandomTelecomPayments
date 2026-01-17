import random
import pandas as pd
import numpy as np
from datetime import datetime
from beartype import beartype

from objects.User import User
from objects.Device import Device
from objects.Card import Card
from objects.Ip import Ip
from objects.Transaction import Transaction
from objects.Application import Application
from utilities.gen_country_codes_map import gen_country_codes_map
from utilities.align_country_codes import align_country_codes
from utilities.gen_trans_rejection_rates import gen_trans_rejection_rates
from utilities.gen_trans_status import gen_trans_status
from utilities.join_idhashes_dict import join_idhashes_dict
import cons

@beartype
def gen_trans_data(
    user_data:pd.DataFrame,
    user_obj:User,
    device_obj:Device,
    card_obj:Card,
    ip_obj:Ip,
    transaction_obj:Transaction,
    application_obj:Application,
    fpath_countrycrimeindex:str=cons.fpath_countrycrimeindex,
    ):
    """
    Generates random transaction level telecom payments data.
    
    Parameters
    ----------
    user_data : pandas.DataFrame
        The random user level data.
    user_obj : User
        The random user data model object.
    device_obj : Device
        The random device data model object.
    card_obj : Card
        The random card data model object.
    ip_obj : Ip
        The random ip data model object.
    transaction_obj : Transaction
        The random transaction data model object.
    application_obj : Application
        The random application data model object.
    fpath_countrycrimeindex : str
        The full file path to the country crime index reference data, default is cons.fpath_countrycrimeindex.
    
    Returns
    -------
    pandas.DataFrame
        The random transaction level telecom payments data.
    """
    
    # explode user data to transaction level
    trans_data = user_data.explode('transaction_hash').dropna(subset = ['transaction_hash']).reset_index(drop = True)
    # select uid entity hashes for each transaction
    trans_data['device_hash'] = trans_data['device_hash'].apply(lambda x: np.random.choice(x, size = 1)[0] if isinstance(x, list) and x != [] else np.nan)
    trans_data['card_hash'] = trans_data['card_hash'].apply(lambda x: np.random.choice(x, size = 1)[0] if isinstance(x, list) and x != [] else np.nan)
    trans_data['ip_hash'] = trans_data['ip_hash'].apply(lambda x: np.random.choice(x, size = 1)[0] if isinstance(x, list) and x != [] else np.nan)
    trans_data['application_hash'] = trans_data['application_hash'].apply(lambda x: np.random.choice(x, size = 1)[0] if isinstance(x, list) and x != [] else np.nan)
    # add null values card hashes
    trans_null_mask = np.random.uniform(size=trans_data.shape[0]) <= cons.data_model_null_rates['card']
    trans_data.loc[trans_null_mask, 'card_hash'] = np.nan
    # add shared hashed entities between users
    trans_data['ip_hash'] = trans_data['ip_hash'].apply(lambda x: ip_obj.ip_shared_idhash_map_dict[x] if x in ip_obj.ip_shared_idhash_map_dict.keys() else x)
    trans_data['card_hash'] = trans_data['card_hash'].apply(lambda x: card_obj.card_shared_idhash_map_dict[x] if x in card_obj.card_shared_idhash_map_dict.keys() else x)
    trans_data['device_hash'] = trans_data['device_hash'].apply(lambda x: device_obj.device_shared_idhash_map_dict[x] if x in device_obj.device_shared_idhash_map_dict.keys() else x)
    # add card and device entity types
    trans_data = join_idhashes_dict(data=trans_data, idhashes_dict=device_obj.device_hashes_type_dict, idhash_key_name='device_hash', idhash_val_name='device_type')
    trans_data = join_idhashes_dict(data=trans_data, idhashes_dict=card_obj.card_hashes_type_dict, idhash_key_name='card_hash', idhash_val_name='card_type')
    # add card and ip country codes
    trans_data = join_idhashes_dict(data=trans_data, idhashes_dict=card_obj.card_hashes_country_code_dict, idhash_key_name='card_hash', idhash_val_name='card_country_code_alpha')
    trans_data = join_idhashes_dict(data=trans_data, idhashes_dict=ip_obj.ip_hashes_country_code_dict, idhash_key_name='ip_hash', idhash_val_name='ip_country_code_alpha')
    # add transaction data
    trans_data = join_idhashes_dict(data=trans_data, idhashes_dict=transaction_obj.transaction_hashes_amounts_dict, idhash_key_name='transaction_hash', idhash_val_name='transaction_amount')
    trans_data = join_idhashes_dict(data=trans_data, idhashes_dict=transaction_obj.transaction_hashes_dates_dict, idhash_key_name='transaction_hash', idhash_val_name='transaction_date')
    # add application data
    trans_data = join_idhashes_dict(data=trans_data, idhashes_dict=application_obj.application_hashes_payment_channel_dict, idhash_key_name='application_hash', idhash_val_name='card_payment_channel')
    
    # TODO: wrap this logic up into a separate function
    # align payment channel with missing card hashes and 0 transaction amounts
    zero_transaction_amount_filter = (trans_data['transaction_amount'] == 0.0)
    missing_card_hash_filter = (trans_data['card_hash'].isnull())
    trans_data.loc[zero_transaction_amount_filter | missing_card_hash_filter, ['card_payment_channel']] = np.nan
    trans_data.loc[zero_transaction_amount_filter, ['card_hash', 'card_type', 'card_country_code_alpha']] = np.nan
    # add payment method as either card, store_wallet or store_points
    trans_data['transaction_payment_method'] = 'card'
    zero_transaction_amount_filter = (trans_data['transaction_amount'] == 0.0)
    missing_card_hash_filter = (trans_data['card_hash'].isnull())
    # trans_data.loc[missing_card_hash_filter, 'transaction_payment_method'] = missing_card_hash_filter.apply(lambda x: np.random.choice(a = list(cons.data_model_non_card_trans_methods.keys()), size = 1, p = list(cons.data_model_non_card_trans_methods.values()))[0])
    trans_data.loc[missing_card_hash_filter, 'transaction_payment_method'] = pd.Series(np.random.choice(a = list(cons.data_model_non_card_trans_methods.keys()), size = missing_card_hash_filter.sum(), p = list(cons.data_model_non_card_trans_methods.values()))[0])
    trans_data.loc[zero_transaction_amount_filter, 'transaction_payment_method'] = np.nan
    # align country codes for user, ip and card
    country_code_columns = ['registration_country_code_alpha', 'ip_country_code_alpha', 'card_country_code_alpha']
    trans_data[country_code_columns] = trans_data[country_code_columns].apply(lambda series: align_country_codes(series), axis = 1)
    agg_aligned_ips = trans_data.groupby(by = ['ip_hash', 'ip_country_code_alpha'], as_index = False).size().sort_values(by = ['ip_hash', 'ip_country_code_alpha'], ascending = [True, False]).drop_duplicates(subset = ['ip_hash'], keep = 'first').drop(columns = ['size'])
    agg_aligned_cards = trans_data.groupby(by = ['card_hash', 'card_country_code_alpha'], as_index = False).size().sort_values(by = ['card_hash', 'card_country_code_alpha'], ascending = [True, False]).drop_duplicates(subset = ['card_hash'], keep = 'first').drop(columns = ['size'])
    trans_data = pd.merge(left = trans_data.drop(columns = ['ip_country_code_alpha']), right = agg_aligned_ips, on = 'ip_hash', how = 'left')
    trans_data = pd.merge(left = trans_data.drop(columns = ['card_country_code_alpha']), right = agg_aligned_cards, on = 'card_hash', how = 'left')
    # align registration and transaction dates
    date_columns = ['registration_date', 'transaction_date']
    if datetime.strptime(user_obj.end_date, "%Y-%m-%d") > datetime.strptime(transaction_obj.start_date, "%Y-%m-%d"):
        dates_series = pd.date_range(start=datetime.strptime(transaction_obj.start_date, "%Y-%m-%d"), end=datetime.strptime(transaction_obj.end_date, "%Y-%m-%d") - pd.Timedelta(days=1), freq="d")
        trans_data[date_columns] = trans_data[date_columns].apply(lambda s: [s['registration_date'], np.random.choice(a=dates_series[dates_series >= max(s['registration_date'], s['transaction_date'])], size=1)[0]], result_type = 'expand', axis = 1).copy()
    # map iso numeric country codes to iso alpha country codes
    country_codes_map = gen_country_codes_map(fpath_countries_europe=user_obj.fpath_countries_europe)
    trans_data = join_idhashes_dict(data=trans_data, idhashes_dict=country_codes_map, idhash_key_name='registration_country_code_alpha', idhash_val_name='registration_country_code')
    trans_data = join_idhashes_dict(data=trans_data, idhashes_dict=country_codes_map, idhash_key_name='card_country_code_alpha', idhash_val_name='card_country_code')
    trans_data = join_idhashes_dict(data=trans_data, idhashes_dict=country_codes_map, idhash_key_name='ip_country_code_alpha', idhash_val_name='ip_country_code')
    
    # generate transaction status and error code
    rejection_rates_dict = gen_trans_rejection_rates(trans_data=trans_data, fpath_countries_europe=user_obj.fpath_countries_europe, fpath_countrycrimeindex=fpath_countrycrimeindex, fpath_email_domain =user_obj.fpath_email_domain )
    trans_data[['transaction_status', 'transaction_error_code']] = trans_data.apply(lambda series: gen_trans_status(series = series, rejection_rates_dict = rejection_rates_dict), result_type = 'expand', axis = 1)
    
    # order columns and sort rows by transaction date
    user_cols = ['userid', 'firstname', 'lastname', 'registration_date', 'registration_country_code', 'uid', 'email_domain']
    device_cols = ['device_hash', 'device_type']
    card_cols = ['card_hash', 'card_type', 'card_country_code']
    ip_cols = ['ip_hash', 'ip_country_code']
    app_cols = ['application_hash']
    trans_cols = ['transaction_hash', 'transaction_date', 'transaction_amount', 'transaction_payment_method', 'card_payment_channel', 'transaction_status', 'transaction_error_code']
    itr_cols = ['itr_hash']
    col_order = user_cols +  device_cols + card_cols + ip_cols + app_cols + trans_cols + itr_cols
    trans_data = trans_data[col_order].sort_values(by = 'transaction_date').reset_index(drop = True)
    
    return trans_data