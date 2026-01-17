import cons

import random
import numpy as np
import pandas as pd
from beartype import beartype
from typing import List, Dict, Union

@beartype
def gen_trans_status(
    series:pd.Series,
    rejection_rates_dict:Dict[str, Dict[str, float]],
    rejection_scaling_factor:int=2,
    ) -> List[Union[str, float]]:
    """
    Generates the transaction status for a pandas series from the transaction level telecom payments data given the rejection rates dictionary from the same data.
    
    Parameters
    ----------
    series : pandas.Series
        A pandas series from the transaction level telecom payments data.
    rejection_rates_dict : Dict[str, Dict[str, float]]
        Rejection rates generated the transaction level telecom payments data.
    rejection_scaling_factor : int
        A multiplicative scaling factor for rejection rates, default is 2.
    
    Returns
    -------
    List[str]
        The transaction status and error code.
    """
    # set country code columns
    country_code_columns = ["registration_country_code","ip_country_code","card_country_code"]
    # if card hash
    if pd.notna(series['card_hash']):
        status = "rejected"
        # add rejections based on crime rates within country codes
        if rejection_rates_dict["country_code_trans_reject_rate_dict"][np.random.choice(a=series[country_code_columns].dropna().to_list(), size=1)[0]] >= random.uniform(0, 1)/rejection_scaling_factor:
            error_code = np.random.choice(a=list(cons.data_model_rejection_codes_fraud.keys()),p=list(cons.data_model_rejection_codes_fraud.values()),size=1)[0]
        # add rejections based on domain frequencies
        elif rejection_rates_dict["domain_email_trans_reject_rate_dict"][series["email_domain"]] >= random.uniform(0, 1)/rejection_scaling_factor:
            error_code = np.random.choice(a=list(cons.data_model_rejection_codes_authentication.keys()),p=list(cons.data_model_rejection_codes_authentication.values()),size=1)[0]
        # add rejections based on inconsistent country codes
        elif cons.data_model_inconsistent_country_codes_rejection_rate[series[country_code_columns].dropna().nunique()] >= random.uniform(0, 1)/rejection_scaling_factor:
            error_code = np.random.choice(a=list(cons.data_model_rejection_codes_connection.keys()),p=list(cons.data_model_rejection_codes_connection.values()),size=1)[0]
        # add rejections based on shared ips, cards and devices
        elif pd.notna(series["device_hash"]) and rejection_rates_dict["shared_devices_reject_rate_dict"][series["device_hash"]] >= random.uniform(0, 1)/rejection_scaling_factor:
            error_code = np.random.choice(a=list(cons.data_model_rejection_codes_fraud.keys()),p=list(cons.data_model_rejection_codes_fraud.values()),size=1)[0]
        elif series["ip_hash"] == series["ip_hash"] and rejection_rates_dict["shared_ips_reject_rate_dict"][series["ip_hash"]] >= random.uniform(0, 1)/rejection_scaling_factor:
            error_code = np.random.choice(a=list(cons.data_model_rejection_codes_fraud.keys()),p=list(cons.data_model_rejection_codes_fraud.values()),size=1)[0]
        elif series["card_hash"] == series["card_hash"] and rejection_rates_dict["shared_cards_reject_rate_dict"][series["card_hash"]] >= random.uniform(0, 1)/rejection_scaling_factor:
            error_code = np.random.choice(a=list(cons.data_model_rejection_codes_fraud.keys()),p=list(cons.data_model_rejection_codes_fraud.values()),size=1)[0]
        # add rejections based on counts of devices, ips and cards
        elif rejection_rates_dict["count_devices_reject_rate_dict"][series["userid"]] >= random.uniform(0, 1)/rejection_scaling_factor:
            error_code = np.random.choice(a=list(cons.data_model_rejection_codes_user.keys()),p=list(cons.data_model_rejection_codes_user.values()),size=1)[0]
        elif rejection_rates_dict["count_ips_reject_rate_dict"][series["userid"]] >= random.uniform(0, 1)/rejection_scaling_factor:
            error_code = np.random.choice(a=list(cons.data_model_rejection_codes_connection.keys()),p=list(cons.data_model_rejection_codes_connection.values()),size=1)[0]
        elif rejection_rates_dict["count_cards_reject_rate_dict"][series["userid"]] >= random.uniform(0, 1)/rejection_scaling_factor:
            error_code = np.random.choice(a=list(cons.data_model_rejection_codes_funds.keys()),p=list(cons.data_model_rejection_codes_funds.values()),size=1)[0]
        # otherwise return successful status
        else:
            successful_status = {key:cons.data_model_transaction_status[key] for key in ['successful', 'pending']}
            successful_probs = [value/sum(successful_status.values()) for value in successful_status.values()]
            status = np.random.choice(a=list(successful_status.keys()), size=1, p=successful_probs)[0]
            error_code = np.nan
    else:
        status = np.random.choice(a=['successful', 'pending'], size=1, p=[0.98, 0.02])[0]
        error_code = np.nan
    return [status, error_code]
