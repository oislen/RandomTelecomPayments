import os
import platform

# set debug mode
debug_mode = False

# set file paths and locations with repo
fpath_root_dir = 'E:\\GitHub' if platform.system() == 'Windows' else '/home/ubuntu' 
fpath_randomtelecomdata = os.path.join(fpath_root_dir, 'RandomTelecomPayments', 'data','RandomTelecomPayments.csv')
fpath_arch_randomtelecomdata = os.path.join(fpath_root_dir, 'RandomTelecomPayments', 'data', 'arch', 'RandomTelecomPayments.csv')
fpath_domain_email = os.path.join(fpath_root_dir, 'RandomTelecomPayments', 'scripts', 'ref', 'email-domains.csv')
fpath_countrycrimeindex = os.path.join(fpath_root_dir, 'RandomTelecomPayments', 'scripts', 'ref', 'country_crime_index.csv')
fpath_countrieseurope = os.path.join(fpath_root_dir, 'RandomTelecomPayments', 'scripts', 'ref', 'Countries-Europe.csv')
fpath_firstnames = os.path.join(fpath_root_dir, 'RandomTelecomPayments', 'scripts', 'ref', 'first-names.txt')
fpath_lastnames = os.path.join(fpath_root_dir, 'RandomTelecomPayments', 'scripts', 'ref', 'last-names.txt')
fpath_unittest_user_data = os.path.join(fpath_root_dir, 'RandomTelecomPayments', 'data', 'unittest', 'user_data.pickle')
fpath_unittest_transaction_data = os.path.join(fpath_root_dir, 'RandomTelecomPayments', 'data', 'unittest', 'transaction_data.pickle')

# set url links to files available online
url_european_populations = 'https://raw.githubusercontent.com/ajturner/acetate/master/places/Countries-Europe.csv'
url_country_populations = 'https://raw.githubusercontent.com/ajturner/acetate/master/places/Countries.csv'
url_first_names = 'https://gist.githubusercontent.com/elifiner/cc90fdd387449158829515782936a9a4/raw/e1a219c33d91b3eecb51ae7b5647d26ed667a11d/first-names.txt'
url_last_names = 'https://gist.githubusercontent.com/elifiner/cc90fdd387449158829515782936a9a4/raw/e1a219c33d91b3eecb51ae7b5647d26ed667a11d/last-names.txt'

# set programme parameters
programme_parameters_factor = 0.5
programme_parameters_randomseed = 1
programme_parameters_nitr = 1
programme_parameters_n_users = 1372
programme_parameters_n_device_types = 53
programme_parameters_n_applications = 1642
programme_parameters_registration_start_date = '2020-01-01'
programme_parameters_registration_end_date = '2020-12-31'
programme_parameters_transaction_start_date = '2021-01-01'
programme_parameters_transaction_end_date = '2021-12-31'

# set unittest constants
unittest_seed = 42
unittest_n_entities = 4
unittest_n_device_types = 10
unittest_gen_test_dfs = False
unittest_debug_mode = True

# set data model constants
data_model_entity_user_ratios = {'card':1.3, 'device':2.5, 'transaction':5.3, 'ip':4.3}
data_model_poisson_lambda_params = {'user':20, 'device':0.3, 'card':0.1, 'ip':1.3, 'application':3, 'transaction':5}
data_model_shared_entities_dict = {'ip':0.05, 'card':0.005, 'device':0.01}
data_model_null_rates = {'ip':0.07, 'card':0.05,'device':0.05}
data_model_card_types_dict = {'visa':0.5, 'mastercard':0.5}
data_model_payment_channels = {'paypal':0.4, 'adyen':0.3, 'worldpay':0.2, 'docomo':0.1}
data_model_transaction_status = {'successful':0.94, 'pending':0.03, 'rejected':0.03}
data_model_inconsistent_country_codes_rejection_rate = {1:0.001, 2:0.005, 3:0.01}
data_model_non_card_trans_methods = {'wallet':0.95, 'points':0.05}
data_model_rejection_codes_fraud = {'E900:ConnectionTimeout':0.15, 'E901:SuspectedFraud':0.35, 'E902:AuthenicationFailure':0.20, 'E903:UserCancelled':0.15, 'E904:InsufficientFunds':0.15}
data_model_rejection_codes_connection = {'E900:ConnectionTimeout':0.35, 'E901:SuspectedFraud':0.15, 'E902:AuthenicationFailure':0.15, 'E903:UserCancelled':0.2, 'E904:InsufficientFunds':0.15}
data_model_rejection_codes_user = {'E900:ConnectionTimeout':0.15, 'E901:SuspectedFraud':0.15, 'E902:AuthenicationFailure':0.15, 'E903:UserCancelled':0.35, 'E904:InsufficientFunds':0.2}
data_model_rejection_codes_funds = {'E900:ConnectionTimeout':0.15, 'E901:SuspectedFraud':0.15, 'E902:AuthenicationFailure':0.15, 'E903:UserCancelled':0.2, 'E904:InsufficientFunds':0.35}
data_model_rejection_codes_authentication = {'E900:ConnectionTimeout':0.15, 'E901:SuspectedFraud':0.2, 'E902:AuthenicationFailure':0.35, 'E903:UserCancelled':0.15, 'E904:InsufficientFunds':0.15}