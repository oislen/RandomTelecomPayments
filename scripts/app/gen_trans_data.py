import random
import pandas as pd
import numpy as np
import cons
from datetime import datetime
from utilities.gen_country_codes_map import gen_country_codes_map
from utilities.align_country_codes import align_country_codes
from utilities.gen_trans_rejection_rates import gen_trans_rejection_rates
from utilities.gen_trans_status import gen_trans_status


def gen_trans_data(user_data, user_obj, device_obj, card_obj, ip_obj, transaction_obj, application_obj):
    """Generates random transaction level telecom payments data

    Parameters
    ----------
    user_data : pandas.DataFrame
        The random user level data
    user_obj : class
        The random user data model object
    device_obj : class
        The random device data model object
    card_obj : class
        The random card data model object
    ip_obj : class
        The random ip data model object
    transaction_obj : class
        The random transaction data model object
    application_obj : class
        The random application data model object

    Returns
    -------
    pandas.DataFrame
        The random transaction level telecom payments data
    """

    # explode user data to transaction level
    trans_data = user_data.explode('transaction_hash').dropna(subset = ['transaction_hash']).reset_index(drop = True)

    # select hashes
    trans_data['device_hash'] = trans_data['device_hash'].apply(lambda x: np.random.choice(x, size = 1)[0] if x != [] else np.nan)
    trans_data['card_hash'] = trans_data['card_hash'].apply(lambda x: np.random.choice(x, size = 1)[0] if x != [] else np.nan)
    trans_data['ip_hash'] = trans_data['ip_hash'].apply(lambda x: np.random.choice(x, size = 1)[0] if x != [] else np.nan)
    trans_data['application_hash'] = trans_data['application_hash'].apply(lambda x: np.random.choice(x, size = 1)[0])
    # add shared hashed entities
    trans_data['ip_hash'] = trans_data['ip_hash'].apply(lambda x: np.random.choice(a = list(ip_obj.ip_hashes_shared_props_dict.keys()), p = list(ip_obj.ip_hashes_shared_props_dict.values()), size = 1)[0] if random.uniform(0, 1) <= cons.data_model_shared_entities_dict['ip'] else x)
    trans_data['card_hash'] = trans_data['card_hash'].apply(lambda x: np.random.choice(a = list(card_obj.card_hashes_shared_props_dict.keys()), p = list(card_obj.card_hashes_shared_props_dict.values()), size = 1)[0] if random.uniform(0, 1) <= cons.data_model_shared_entities_dict['card'] else x)
    trans_data['device_hash'] = trans_data['device_hash'].apply(lambda x: np.random.choice(a = list(device_obj.device_hashes_shared_props_dict.keys()), p = list(device_obj.device_hashes_shared_props_dict.values()), size = 1)[0] if random.uniform(0, 1) <= cons.data_model_shared_entities_dict['device'] else x)
    # add null rates
    trans_data['ip_hash'] = trans_data['ip_hash'].apply(lambda x: np.nan if random.uniform(0, 1) <= cons.data_model_null_rates['ip'] else x)
    trans_data['card_hash'] = trans_data['card_hash'].apply(lambda x: np.nan if random.uniform(0, 1) <= cons.data_model_null_rates['card'] else x)
    trans_data['device_hash'] = trans_data['device_hash'].apply(lambda x: np.nan if random.uniform(0, 1) <= cons.data_model_null_rates['device'] else x)
    # add type data
    trans_data['device_type'] = trans_data['device_hash'].replace(device_obj.device_hashes_type_dict)
    trans_data['card_type'] = trans_data['card_hash'].replace(card_obj.card_hashes_type_dict)
    # add country code data
    trans_data['card_country_code'] = trans_data['card_hash'].replace(card_obj.card_hashes_country_code_dict)
    trans_data['ip_country_code'] = trans_data['ip_hash'].replace(ip_obj.ip_hashes_country_code_dict)
    # add transaction data
    trans_data['transaction_amount'] = trans_data['transaction_hash'].replace(transaction_obj.transaction_hashes_amounts_dict)
    trans_data['card_payment_channel'] = trans_data['transaction_hash'].replace(transaction_obj.transaction_hashes_payment_channel_dict)
    trans_data['transaction_date'] = trans_data['transaction_hash'].replace(transaction_obj.transaction_hashes_dates_dict)

    # TODO: wrap this logic up into a seperate function
    # align payment channel with missing card hashes and 0 transaction amounts
    zero_transaction_amount_filter = (trans_data['transaction_amount'] == 0.0)
    missing_card_hash_filter = (trans_data['card_hash'].isnull())
    trans_data.loc[zero_transaction_amount_filter | missing_card_hash_filter, ['card_payment_channel']] = np.nan
    trans_data.loc[zero_transaction_amount_filter, ['card_hash', 'card_type', 'card_country_code']] = np.nan
    # add payment method as either card, store_wallet or store_points
    trans_data['transaction_payment_method'] = 'card'
    zero_transaction_amount_filter = (trans_data['transaction_amount'] == 0.0)
    missing_card_hash_filter = (trans_data['card_hash'].isnull())
    trans_data.loc[missing_card_hash_filter, 'transaction_payment_method'] = missing_card_hash_filter.apply(lambda x: np.random.choice(a = list(cons.data_model_non_card_trans_methods.keys()), size = 1, p = list(cons.data_model_non_card_trans_methods.values()))[0])
    trans_data.loc[zero_transaction_amount_filter, 'transaction_payment_method'] = np.nan
    # align country codes for user, ip and card
    country_code_columns = ['registration_country_code', 'ip_country_code', 'card_country_code']
    trans_data[country_code_columns] = trans_data[country_code_columns].apply(lambda series: align_country_codes(series), axis = 1)
    agg_aligned_ips = trans_data.groupby(by = ['ip_hash', 'ip_country_code'], as_index = False).size().sort_values(by = ['ip_hash', 'ip_country_code'], ascending = [True, False]).drop_duplicates(subset = ['ip_hash'], keep = 'first').drop(columns = ['size'])
    agg_aligned_cards = trans_data.groupby(by = ['card_hash', 'card_country_code'], as_index = False).size().sort_values(by = ['card_hash', 'card_country_code'], ascending = [True, False]).drop_duplicates(subset = ['card_hash'], keep = 'first').drop(columns = ['size'])
    trans_data = pd.merge(left = trans_data.drop(columns = ['ip_country_code']), right = agg_aligned_ips, on = 'ip_hash', how = 'left')
    trans_data = pd.merge(left = trans_data.drop(columns = ['card_country_code']), right = agg_aligned_cards, on = 'card_hash', how = 'left')
    # align registration and transaction dates
    date_columns = ['registration_date', 'transaction_date']
    if datetime.strptime(user_obj.end_date, "%Y-%m-%d") > datetime.strptime(transaction_obj.start_date, "%Y-%m-%d"):
        dates_series = pd.date_range(start=datetime.strptime(transaction_obj.start_date, "%Y-%m-%d"), end=datetime.strptime(transaction_obj.end_date, "%Y-%m-%d") - pd.Timedelta(days=1), freq="d")
        trans_data[date_columns] = trans_data[date_columns].apply(lambda s: [s['registration_date'], np.random.choice(a=dates_series[dates_series >= max(s['registration_date'], s['transaction_date'])], size=1)[0]], result_type = 'expand', axis = 1).copy()
    # map iso numeric country codes to iso alpha country codes
    country_codes_map = gen_country_codes_map()
    trans_data['registration_country_code']  = trans_data['registration_country_code'].replace(country_codes_map)
    trans_data['card_country_code']  = trans_data['card_country_code'].replace(country_codes_map)
    trans_data['ip_country_code']  = trans_data['ip_country_code'].replace(country_codes_map)

    # generate transaction status and error code
    rejection_rates_dict = gen_trans_rejection_rates(trans_data = trans_data)
    trans_data[['transaction_status', 'transaction_error_code']] = trans_data.apply(lambda series: gen_trans_status(series = series, rejection_rates_dict = rejection_rates_dict), result_type = 'expand', axis = 1)

    # order columns and sort rows by transaction date
    user_cols = ['userid', 'firstname', 'lastname', 'registration_date', 'registration_country_code', 'uid', 'email_domain']
    device_cols = ['device_hash', 'device_type']
    card_cols = ['card_hash', 'card_type', 'card_country_code']
    ip_cols = ['ip_hash', 'ip_country_code']
    app_cols = ['application_hash']
    trans_cols = ['transaction_hash', 'transaction_date', 'transaction_amount', 'transaction_payment_method', 'card_payment_channel', 'transaction_status', 'transaction_error_code']
    col_order = user_cols +  device_cols + card_cols + ip_cols + app_cols + trans_cols
    trans_data = trans_data[col_order].sort_values(by = 'transaction_date').reset_index(drop = True)

    return trans_data