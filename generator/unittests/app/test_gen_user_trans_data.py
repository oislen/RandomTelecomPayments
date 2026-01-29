import os
import sys
import unittest
import random
import numpy as np
import pandas as pd

sys.path.append(os.path.join(os.getcwd(), "generator"))

import cons
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

# initalise programme parameters
programmeparams = ProgrammeParams(
    n_users=cons.unittest_n_users,
    random_seed=cons.unittest_seed,
    registration_start_date=cons.unittest_registration_start_date,
    registration_end_date=cons.unittest_registration_end_date,
    transaction_start_date=cons.unittest_transaction_start_date,
    transaction_end_date=cons.unittest_transaction_end_date
    )

# set random seed
random.seed(programmeparams.random_seed)
np.random.seed(seed=programmeparams.random_seed)

# create relative file paths
fpath_first_names = '.' + cons.fpath_llama_first_names.split(cons.fpath_repo_dir)[1]
fpath_last_names = '.' + cons.fpath_llama_last_names.split(cons.fpath_repo_dir)[1]
fpath_countries_europe = '.' + cons.fpath_countries_europe.split(cons.fpath_repo_dir)[1]
fpath_email_domain = '.' + cons.fpath_email_domain.split(cons.fpath_repo_dir)[1]
fpath_smartphones = '.' + cons.fpath_smartphones.split(cons.fpath_repo_dir)[1]
fpath_countrycrimeindex = '.' + cons.fpath_countrycrimeindex.split(cons.fpath_repo_dir)[1]
fpath_unittest_user_data = '.' + cons.fpath_unittest_user_data.split(cons.fpath_repo_dir)[1]
fpath_unittest_transaction_data = '.' + cons.fpath_unittest_transaction_data.split(cons.fpath_repo_dir)[1]

# generate random users
user_obj = User(
    n_user_ids=programmeparams.n_users,
    start_date=programmeparams.registration_start_date,
    end_date=programmeparams.registration_end_date,
    fpath_first_names=fpath_first_names,
    fpath_last_names=fpath_last_names,
    fpath_countries_europe=fpath_countries_europe,
    fpath_email_domain=fpath_email_domain
    )

# generate random entity counts for each user
random_entity_counts = gen_random_entity_counts(user_obj)

# generate random entity values
device_obj = Device(n_device_hashes=random_entity_counts['n_devices'].sum(), fpath_smartphones=fpath_smartphones)
card_obj = Card(n_card_hashes=random_entity_counts['n_cards'].sum(), fpath_countries_europe=fpath_countries_europe)
ip_obj = Ip(n_ip_hashes=random_entity_counts['n_ips'].sum(), fpath_countries_europe=fpath_countries_europe)
transaction_obj = Transaction(n_transaction_hashes=random_entity_counts['n_transactions'].sum(), start_date=programmeparams.transaction_start_date, end_date=programmeparams.transaction_end_date)
application_obj = Application(n_application_hashes=programmeparams.n_applications)

# generate expected user and transaction level data
obs_user_data = gen_user_data(
    random_entity_counts=random_entity_counts,
    user_obj=user_obj,
    device_obj=device_obj,
    card_obj=card_obj,
    ip_obj=ip_obj,
    transaction_obj=transaction_obj,
    application_obj=application_obj,
)
obs_trans_data = gen_trans_data(
    user_data=obs_user_data,
    user_obj=user_obj,
    device_obj=device_obj,
    card_obj=card_obj,
    ip_obj=ip_obj,
    transaction_obj=transaction_obj,
    application_obj=application_obj,
    fpath_countrycrimeindex=fpath_countrycrimeindex
)

# if writing observed data to unittest data directory
if cons.unittest_gen_test_dfs:
    print(f"WARNING: cons.unittest_gen_test_dfs == {cons.unittest_gen_test_dfs}")
    obs_user_data.to_parquet(fpath_unittest_user_data)
    obs_trans_data.to_parquet(fpath_unittest_transaction_data)

# load in expected user level data
exp_user_data = pd.read_parquet(fpath_unittest_user_data)
exp_trans_data = pd.read_parquet(fpath_unittest_transaction_data)

class Test_gen_user_trans_data(unittest.TestCase):
    """"""

    def setUp(self):
        self.obs_user_data = obs_user_data
        self.exp_user_data = exp_user_data
        self.obs_trans_data = obs_trans_data
        self.exp_trans_data = exp_trans_data

    def test_type(self):
        self.assertEqual(type(self.obs_user_data), type(self.exp_user_data))
        self.assertEqual(type(self.obs_trans_data), type(self.exp_trans_data))

    def test_shape(self):
        self.assertEqual(self.obs_user_data.shape, self.exp_user_data.shape)
        self.assertEqual(self.obs_trans_data.shape, self.exp_trans_data.shape)

    def test_dtypes(self):
        self.assertTrue((self.obs_user_data.dtypes == self.exp_user_data.dtypes).all())
        self.assertTrue((self.obs_trans_data.dtypes == self.exp_trans_data.dtypes).all())

    def test_isnull(self):
        self.assertTrue((self.obs_user_data.isnull() == self.exp_user_data.isnull()).all().all())
        self.assertTrue((self.obs_trans_data.isnull() == self.exp_trans_data.isnull()).all().all())

    def test_notnull(self):
        self.assertTrue((self.obs_user_data.notnull() == self.exp_user_data.notnull()).all().all())
        self.assertTrue((self.obs_trans_data.notnull() == self.exp_trans_data.notnull()).all().all())

    def test_object(self):
        self.assertTrue((self.obs_trans_data.fillna(-999.0) == self.exp_trans_data.fillna(-999.0)).all().all())


if __name__ == "__main__":
    unittest.main()
