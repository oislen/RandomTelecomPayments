import pandas as pd
import cons
from beartype import beartype
from typing import Dict

@beartype
def gen_trans_rejection_rates(
    trans_data:pd.DataFrame,
    fpath_countries_europe:str=cons.fpath_countries_europe,
    fpath_countrycrimeindex:str=cons.fpath_countrycrimeindex,
    fpath_email_domain:str=cons.fpath_email_domain,
    ) -> Dict[str, Dict[str, float]]:
    """
    Generates the transaction rejection rates based on features within the transaction level telecom payments data.
    
    Parameters
    ----------
    trans_data : pandas.DataFrame
        The transaction level telecom payments data.
    fpath_countries_europe : str
        The file path to the europe countries reference data, default is cons.fpath_countries_europe.
    fpath_countrycrimeindex : str
        The file path to the country crime index reference data, default is cons.fpath_countrycrimeindex.
    fpath_email_domain :str
        The file path to the email domains reference data, default is cons.fpath_email_domain.
    
    Returns
    -------
    dict
        The rejection rates based on features within the transaction level telecom payments data.
    """
    # initialize dictionary to store all computed rejection rates
    rejection_rates_dict = {}
    
    # generate country code rejection based rates
    countrieseurope = pd.read_csv(fpath_countries_europe, usecols=["ISO alpha 2"])
    countrycrimeindex = pd.read_csv(fpath_countrycrimeindex, usecols=["country_code", "crime_index"])
    europecountrycrimeindex = pd.merge(left=countrieseurope, right=countrycrimeindex, left_on="ISO alpha 2", right_on="country_code", how="left",)
    europecountrycrimeindex["trans_reject_rate"] = europecountrycrimeindex["crime_index"].divide(europecountrycrimeindex["crime_index"].sum())
    country_code_trans_reject_rate_dict = europecountrycrimeindex.set_index("ISO alpha 2")["trans_reject_rate"].to_dict()
    rejection_rates_dict["country_code_trans_reject_rate_dict"] = country_code_trans_reject_rate_dict
    
    # generate domain email rejection based rates
    domain_email = pd.read_csv(fpath_email_domain, usecols=["domain", "proportion"])
    domain_email["trans_reject_rate"] = (1 - domain_email["proportion"]) / (1 - domain_email["proportion"]).sum()
    domain_email_trans_reject_rate_dict = domain_email.set_index("domain")["trans_reject_rate"].to_dict()
    rejection_rates_dict["domain_email_trans_reject_rate_dict"] = domain_email_trans_reject_rate_dict
    
    # generate shared entities with rejection rates dictionary
    shared_devices = (trans_data.groupby(by="device_hash").agg({"userid": "nunique"}).sort_values(by="userid"))
    shared_ips = (trans_data.groupby(by="ip_hash").agg({"userid": "nunique"}).sort_values(by="userid"))
    shared_cards = (trans_data.groupby(by="card_hash").agg({"userid": "nunique"}).sort_values(by="userid"))
    shared_devices_reject_rate_dict = shared_devices.divide(shared_devices["userid"].sum())["userid"].to_dict()
    shared_ips_reject_rate_dict = shared_ips.divide(shared_ips["userid"].sum()).to_dict()["userid"]
    shared_cards_reject_rate_dict = shared_cards.divide(shared_cards["userid"].sum()).to_dict()["userid"]
    rejection_rates_dict["shared_devices_reject_rate_dict"] = shared_devices_reject_rate_dict
    rejection_rates_dict["shared_ips_reject_rate_dict"] = shared_ips_reject_rate_dict
    rejection_rates_dict["shared_cards_reject_rate_dict"] = shared_cards_reject_rate_dict
    
    # generate occurrence based rejection rates
    count_devices = (trans_data.groupby(by="userid").agg({"device_hash": "nunique"}).sort_values(by="device_hash"))
    count_ips = (trans_data.groupby(by="userid").agg({"ip_hash": "nunique"}).sort_values(by="ip_hash"))
    count_cards = (trans_data.groupby(by="userid").agg({"card_hash": "nunique"}).sort_values(by="card_hash"))
    count_devices_reject_rate_dict = count_devices.divide(count_devices["device_hash"].sum())["device_hash"].to_dict()
    count_ips_reject_rate_dict = count_ips.divide(count_ips["ip_hash"].sum()).to_dict()["ip_hash"]
    count_cards_reject_rate_dict = count_cards.divide(count_cards["card_hash"].sum()).to_dict()["card_hash"]
    rejection_rates_dict["count_devices_reject_rate_dict"] = count_devices_reject_rate_dict
    rejection_rates_dict["count_ips_reject_rate_dict"] = count_ips_reject_rate_dict
    rejection_rates_dict["count_cards_reject_rate_dict"] = count_cards_reject_rate_dict
    
    return rejection_rates_dict
