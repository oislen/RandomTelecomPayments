import cons

import argparse
from typing import Dict

def commandline_interface() -> Dict[str, object]:
    """
    A commandline interface for parsing input parameters with
    
    Windows
    python RandomTeleComData\\generator\\main.py --n_users 100 --random_seed 1 --n_itr 2
    
    Linux
    python3 RandomTeleComData/generator/main.py --n_users 100 --random_seed 1 --n_itr 2
    
    Parameters
    ----------
    n_users : int
        The number of users to generate random telecom payments data for.
    use_random_seed : int
        Use a set random seed for reproducible results; must be either 0 or 1.
    n_itr : int
        Number of iterations to run.
    n_applications : int
        The number of applications to generate random telecom payments data for.
    registration_start_date : str
        The start date for registrations.
    registration_end_date : str
        The end date for registrations.
    transaction_start_date : str
        The start date for transactions.
    transaction_end_date : str
        The end date for transactions.
    
    Returns
    -------
    Dict[str, object]
        A dictionary of key, value pairs where the values are parsed input parameters.
    """
    # define argument parser object
    parser = argparse.ArgumentParser(description="Execute Random TeleCom Data Programme.")
    # add input arguments
    parser.add_argument("--n_users", action="store", dest="n_users", type=int, default=cons.default_n_users, help="Integer, the number of users to generate random telecom payments data for",)
    parser.add_argument("--use_random_seed", action="store", dest="use_random_seed", type=int, default=cons.default_use_random_seed, choices=[0, 1], help="Integer, use a set random seed for reproducible results; must be either 0 or 1",)
    parser.add_argument("--n_itr", action="store", dest="n_itr", type=int, default=cons.default_n_itr, help="Integer, number of iterations to run",)
    parser.add_argument("--n_applications", action="store", dest="n_applications", type=int, default=cons.default_n_applications, help="Integer, the number of applications to generate random telecom payments data for",)
    parser.add_argument("--registration_start_date", action="store", dest="registration_start_date", type=str, default=cons.default_registration_start_date, help="String, the start date for registrations",)
    parser.add_argument("--registration_end_date", action="store", dest="registration_end_date", type=str, default=cons.default_registration_end_date, help="String, the end date for registrations",)
    parser.add_argument("--transaction_start_date", action="store", dest="transaction_start_date", type=str, default=cons.default_transaction_start_date, help="String, the start date for transactions",)
    parser.add_argument("--transaction_end_date", action="store", dest="transaction_end_date", type=str, default=cons.default_transaction_end_date, help="String, the end date for transactions",)
    # create an output dictionary to hold the results
    input_params_dict = cons.default_input_params_dict.copy()
    # extract input arguments
    args = parser.parse_args()
    # map input arguments into output dictionary
    input_params_dict["n_users"] = args.n_users
    input_params_dict["use_random_seed"] = args.use_random_seed
    input_params_dict["n_itr"] = args.n_itr
    input_params_dict["n_applications"] = args.n_applications
    input_params_dict["registration_start_date"] = args.registration_start_date
    input_params_dict["registration_end_date"] = args.registration_end_date
    input_params_dict["transaction_start_date"] = args.transaction_start_date
    input_params_dict["transaction_end_date"] = args.transaction_end_date
    return input_params_dict
