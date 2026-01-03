import unittest
import os
import sys
import numpy as np
import pandas as pd
import random

sys.path.append(os.path.join(os.getcwd(), "generator"))

import cons
from utilities.gen_random_entity_counts import gen_random_entity_counts
from objects.User import User

exp_start_date = cons.unittest_registration_start_date
exp_end_date = cons.unittest_registration_end_date
exp_n_user_ids = cons.unittest_n_entities
exp_lam = cons.data_model_poisson_params["user"]["lambda"]

random.seed(cons.unittest_seed)
np.random.seed(cons.unittest_seed)

fpath_firstnames = '.' + cons.fpath_llama_firstnames.split(cons.fpath_repo_dir)[1]
fpath_lastnames = '.' + cons.fpath_llama_lastnames.split(cons.fpath_repo_dir)[1]
fpath_countrieseurope = '.' + cons.fpath_countrieseurope.split(cons.fpath_repo_dir)[1]
fpath_domain_email = '.' + cons.fpath_domain_email.split(cons.fpath_repo_dir)[1]
user_object = User(n_user_ids=exp_n_user_ids, start_date=exp_start_date, end_date=exp_end_date, fpath_firstnames=fpath_firstnames, fpath_lastnames=fpath_lastnames, fpath_countrieseurope=fpath_countrieseurope, fpath_domain_email=fpath_domain_email)

exp_randomentity_counts_dict = {
    'uid': ['6374692674377254', '6720317315593519', '4264861381989413', '1751409580926382'], 
    'n_devices': [1, 2, 1, 1],
    'n_cards': [1, 1, 1, 1],
    'n_ips': [3, 5, 5, 1],
    'n_transactions': [72, 16, 13, 29],
    'n_applications': [4, 2, 3, 5]
    }

exp_randomentity_counts_df = pd.DataFrame.from_dict(exp_randomentity_counts_dict)
obs_random_entity_counts_df = gen_random_entity_counts(user_object)

class Test_gen_random_entity_counts(unittest.TestCase):
    """"""

    def setUp(self):
        self.exp_randomentity_counts_df = exp_randomentity_counts_df
        self.obs_random_entity_counts_df = obs_random_entity_counts_df

    def test_type(self):
        self.assertEqual(type(self.exp_randomentity_counts_df), type(self.obs_random_entity_counts_df))

    def test_shape(self):
        self.assertEqual(self.exp_randomentity_counts_df.shape, self.obs_random_entity_counts_df.shape)

    def test_columns(self):
        self.assertEqual(self.exp_randomentity_counts_df.columns.to_list(), self.obs_random_entity_counts_df.columns.to_list())

    def test_values(self):
        self.assertTrue((self.exp_randomentity_counts_df.values == self.obs_random_entity_counts_df.values).all().all())

if __name__ == "__main__":
    unittest.main()
