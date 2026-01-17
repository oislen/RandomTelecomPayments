import os
import re
import sys
import datetime

root_dir_re_match = re.findall(string=os.getcwd(), pattern="^.+RandomTelecomPayments")
fpath_repo_dir = root_dir_re_match[0] if len(root_dir_re_match) > 0 else os.path.join(".", "RandomTelecomPayments")
sys.path.append(fpath_repo_dir)
# set sub directories
subdir_data = os.path.join(fpath_repo_dir, 'data')
subdir_generator = os.path.join(fpath_repo_dir, 'generator')
subdir_unittest = os.path.join(subdir_data, 'unittest')
subdir_creds = os.path.join(fpath_repo_dir, '.creds')
# set data files
fpath_randomtelecomtransdata = os.path.join(subdir_data,'RandomTelecomPayments.csv')
fpath_randomtelecomusersdata = os.path.join(subdir_data,'RandomTelecomUsers.parquet')
fpath_arch_randomtelecomdata = os.path.join(subdir_data, 'arch', 'RandomTelecomPayments.csv')
fpath_temp_llama_firstnames = os.path.join(subdir_data, 'temp', 'llama_firstnames_{country}.csv')
fpath_temp_llama_lastnames = os.path.join(subdir_data, 'temp', 'llama_lastnames_{country}.csv')
fpath_email_domain = os.path.join(subdir_data, 'ref', 'email-domains.csv')
fpath_countrycrimeindex = os.path.join(subdir_data, 'ref', 'country_crime_index.csv')
fpath_countries_europe = os.path.join(subdir_data, 'ref', 'Countries-Europe.csv')
fpath_firstnames = os.path.join(subdir_data, 'ref', 'first-names.txt')
fpath_lastnames = os.path.join(subdir_data, 'ref', 'last-names.txt')
fpath_llama_firstnames = os.path.join(subdir_data, 'ref', 'llama_firstnames.csv')
fpath_llama_lastnames = os.path.join(subdir_data, 'ref', 'llama_lastnames.csv')
fpath_smartphones = os.path.join(subdir_data, 'ref', 'smartphones.csv')
fpath_unittest_user_data = os.path.join(subdir_unittest, 'user_data.parquet')
fpath_unittest_transaction_data = os.path.join(subdir_unittest, 'transaction_data.parquet')
fpath_aws_session_token = os.path.join(subdir_creds,'sessionToken.json')

# set url links to files available online
url_european_populations = 'https://raw.githubusercontent.com/ajturner/acetate/master/places/Countries-Europe.csv'
url_country_populations = 'https://raw.githubusercontent.com/ajturner/acetate/master/places/Countries.csv'
url_first_names = 'https://gist.githubusercontent.com/elifiner/cc90fdd387449158829515782936a9a4/raw/e1a219c33d91b3eecb51ae7b5647d26ed667a11d/first-names.txt'
url_last_names = 'https://gist.githubusercontent.com/elifiner/cc90fdd387449158829515782936a9a4/raw/e1a219c33d91b3eecb51ae7b5647d26ed667a11d/last-names.txt'

# set date constants
date_date_strftime = "%Y-%m-%d"
date_today = datetime.datetime.today()

# set programme defaults
default_n_users = 100
default_use_random_seed = 0
default_n_itr = 1
default_n_applications = 20000
default_registration_start_date = (date_today - datetime.timedelta(days=731)).strftime(date_date_strftime)
default_registration_end_date = (date_today - datetime.timedelta(days=366)).strftime(date_date_strftime)
default_transaction_start_date = (date_today - datetime.timedelta(days=365)).strftime(date_date_strftime)
default_transaction_end_date = date_today.strftime(date_date_strftime)

# set unittest constants
unittest_seed = 42
unittest_n_entities = 4
unittest_n_device_types = 10
unittest_gen_test_dfs = False
unittest_n_users = 10
unittest_registration_start_date = '2020-01-01'
unittest_registration_end_date = '2020-12-31'
unittest_transaction_start_date = '2021-01-01'
unittest_transaction_end_date = '2021-12-31'

# set data model constants
data_model_entity_user_ratios = {'card':1.3, 'device':2.5, 'transaction':5.3, 'ip':4.3}
data_model_poisson_params = {'user':{'lambda':20, 'power':1}, 'device':{'lambda':0.2, 'power':2}, 'card':{'lambda':0.1, 'power':2}, 'ip':{'lambda':1.3, 'power':2}, 'application':{'lambda':1, 'power':2}, 'transaction':{'lambda':5, 'power':2}}
data_model_shared_entities_dict = {'ip':0.05, 'card':0.005, 'device':0.01}
data_model_null_rates = {'card':0.05}
data_model_card_types_dict = {'visa':0.5, 'mastercard':0.5}
data_model_payment_channels = {'paypal':0.4, 'adyen':0.15, 'appstore':0.25, 'worldpay':0.15, 'docomo':0.05}
data_model_transaction_status = {'successful':0.94, 'pending':0.03, 'rejected':0.03}
data_model_inconsistent_country_codes_rejection_rate = {1:0.001, 2:0.005, 3:0.01}
data_model_non_card_trans_methods = {'wallet':0.95, 'points':0.05}
data_model_rejection_codes_fraud = {'E900:ConnectionTimeout':0.1, 'E901:SuspectedFraud':0.55, 'E902:AuthenicationFailure':0.2, 'E903:UserCancelled':0.05, 'E904:InsufficientFunds':0.1}
data_model_rejection_codes_connection = {'E900:ConnectionTimeout':0.45, 'E901:SuspectedFraud':0.1, 'E902:AuthenicationFailure':0.2, 'E903:UserCancelled':0.15, 'E904:InsufficientFunds':0.1}
data_model_rejection_codes_user = {'E900:ConnectionTimeout':0.05, 'E901:SuspectedFraud':0.1, 'E902:AuthenicationFailure':0.1, 'E903:UserCancelled':0.45, 'E904:InsufficientFunds':0.3}
data_model_rejection_codes_funds = {'E900:ConnectionTimeout':0.1, 'E901:SuspectedFraud':0.1, 'E902:AuthenicationFailure':0.1, 'E903:UserCancelled':0.25, 'E904:InsufficientFunds':0.45}
data_model_rejection_codes_authentication = {'E900:ConnectionTimeout':0.25, 'E901:SuspectedFraud':0.05, 'E902:AuthenicationFailure':0.45, 'E903:UserCancelled':0.15, 'E904:InsufficientFunds':0.1}

# set lists of generator object types
object_types = ["device","card","ip","transaction","application"]