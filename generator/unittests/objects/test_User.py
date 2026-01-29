import unittest
import os
import sys
import random
import numpy as np

sys.path.append(os.path.join(os.getcwd(), "generator"))

import cons
from objects.User import User

exp_user_ids_cnts_dict = {
    "6374692674377254": 20,
    "1751409580926382": 29,
    "4264861381989413": 19,
    "6720317315593519": 26,
}
exp_user_ids_props_dict = {
    "6374692674377254": 0.2127659574468085,
    "1751409580926382": 0.30851063829787234,
    "4264861381989413": 0.20212765957446807,
    "6720317315593519": 0.2765957446808511,
}
exp_user_ids_first_name_dict = {
    "6374692674377254": "simone",
    "1751409580926382": "francesca",
    "4264861381989413": "igor",
    "6720317315593519": "beckett",
}
exp_user_ids_last_name_dict = {
    "6374692674377254": "de filippo",
    "1751409580926382": "gagliardi",
    "4264861381989413": "lupu",
    "6720317315593519": "leslie",
}
exp_user_ids_country_code_dict = {
    "6374692674377254": 380,
    "1751409580926382": 380,
    "4264861381989413": 498,
    "6720317315593519": 826,
}
exp_user_ids_email_domain_dict = {
    "6374692674377254": "yahoo.com",
    "1751409580926382": "yahoo.com",
    "4264861381989413": "yahoo.com",
    "6720317315593519": "gmail.com",
}
exp_user_ids_dates_dict = {
    "6374692674377254": np.datetime64("2020-03-21T00:00:00.000000000"),
    "1751409580926382": np.datetime64("2020-06-11T00:00:00.000000000"),
    "4264861381989413": np.datetime64("2020-10-15T00:00:00.000000000"),
    "6720317315593519": np.datetime64("2020-09-17T00:00:00.000000000"),
}
exp_start_date = cons.unittest_registration_start_date
exp_end_date = cons.unittest_registration_end_date
exp_n_user_ids = cons.unittest_n_entities
exp_lam = cons.data_model_poisson_params["user"]["lambda"]

random.seed(cons.unittest_seed)
np.random.seed(cons.unittest_seed)

fpath_first_names = '.' + cons.fpath_llama_first_names.split(cons.fpath_repo_dir)[1]
fpath_last_names = '.' + cons.fpath_llama_last_names.split(cons.fpath_repo_dir)[1]
fpath_countries_europe = '.' + cons.fpath_countries_europe.split(cons.fpath_repo_dir)[1]
fpath_email_domain = '.' + cons.fpath_email_domain.split(cons.fpath_repo_dir)[1]
user_object = User(n_user_ids=exp_n_user_ids, start_date=exp_start_date, end_date=exp_end_date, fpath_first_names=fpath_first_names, fpath_last_names=fpath_last_names, fpath_countries_europe=fpath_countries_europe, fpath_email_domain=fpath_email_domain)

obs_user_ids_cnts_dict = user_object.user_ids_cnts_dict
obs_user_ids_props_dict = user_object.user_ids_props_dict
obs_user_ids_first_name_dict = user_object.user_ids_first_name_dict
obs_user_ids_last_name_dict = user_object.user_ids_last_name_dict
obs_user_ids_country_code_dict = user_object.user_ids_country_code_dict
obs_user_ids_email_domain_dict = user_object.user_ids_email_domain_dict
obs_user_ids_dates_dict = user_object.user_ids_dates_dict
obs_start_date = user_object.start_date
obs_end_date = user_object.end_date
obs_n_user_ids = user_object.n_user_ids
obs_lam = user_object.lam


class Test_User(unittest.TestCase):
    """"""

    def setUp(self):
        self.exp_user_ids_cnts_dict = exp_user_ids_cnts_dict
        self.obs_user_ids_cnts_dict = obs_user_ids_cnts_dict
        self.exp_user_ids_props_dict = exp_user_ids_props_dict
        self.obs_user_ids_props_dict = obs_user_ids_props_dict
        self.exp_user_ids_first_name_dict = exp_user_ids_first_name_dict
        self.obs_user_ids_first_name_dict = obs_user_ids_first_name_dict
        self.exp_user_ids_last_name_dict = exp_user_ids_last_name_dict
        self.obs_user_ids_last_name_dict = obs_user_ids_last_name_dict
        self.exp_user_ids_country_code_dict = exp_user_ids_country_code_dict
        self.obs_user_ids_country_code_dict = obs_user_ids_country_code_dict
        self.exp_user_ids_email_domain_dict = exp_user_ids_email_domain_dict
        self.obs_user_ids_email_domain_dict = obs_user_ids_email_domain_dict
        self.exp_user_ids_dates_dict = exp_user_ids_dates_dict
        self.obs_user_ids_dates_dict = obs_user_ids_dates_dict
        self.exp_start_date = exp_start_date
        self.obs_start_date = obs_start_date
        self.exp_end_date = exp_end_date
        self.obs_end_date = obs_end_date
        self.exp_n_user_ids = exp_n_user_ids
        self.obs_n_user_ids = obs_n_user_ids
        self.exp_lam = exp_lam
        self.obs_lam = obs_lam

    def test_type(self):
        self.assertEqual(type(self.obs_user_ids_cnts_dict), type(self.exp_user_ids_cnts_dict))
        self.assertEqual(type(self.obs_user_ids_props_dict), type(self.exp_user_ids_props_dict))
        self.assertEqual(type(self.obs_user_ids_first_name_dict),type(self.exp_user_ids_first_name_dict),)
        self.assertEqual(type(self.obs_user_ids_last_name_dict), type(self.exp_user_ids_last_name_dict))
        self.assertEqual(type(self.obs_user_ids_country_code_dict),type(self.exp_user_ids_country_code_dict),)
        self.assertEqual(type(self.obs_user_ids_email_domain_dict),type(self.exp_user_ids_email_domain_dict),)
        self.assertEqual(type(self.obs_user_ids_dates_dict), type(self.exp_user_ids_dates_dict))
        self.assertEqual(type(self.obs_start_date), type(self.exp_start_date))
        self.assertEqual(type(self.obs_end_date), type(self.exp_end_date))
        self.assertEqual(type(self.obs_n_user_ids), type(self.exp_n_user_ids))
        self.assertEqual(type(self.obs_lam), type(self.exp_lam))

    def test_len(self):
        self.assertEqual(len(self.obs_user_ids_cnts_dict), len(self.exp_user_ids_cnts_dict))
        self.assertEqual(len(self.obs_user_ids_props_dict), len(self.exp_user_ids_props_dict))
        self.assertEqual(len(self.obs_user_ids_first_name_dict), len(self.exp_user_ids_first_name_dict))
        self.assertEqual(len(self.obs_user_ids_last_name_dict), len(self.exp_user_ids_last_name_dict))
        self.assertEqual(len(self.obs_user_ids_country_code_dict),len(self.exp_user_ids_country_code_dict),)
        self.assertEqual(len(self.obs_user_ids_email_domain_dict),len(self.exp_user_ids_email_domain_dict),)
        self.assertEqual(len(self.obs_user_ids_dates_dict), len(self.exp_user_ids_dates_dict))

    def test_keys(self):
        self.assertEqual(list(self.obs_user_ids_cnts_dict.keys()),list(self.exp_user_ids_cnts_dict.keys()),)
        self.assertEqual(list(self.obs_user_ids_props_dict.keys()),list(self.exp_user_ids_props_dict.keys()),)
        self.assertEqual(list(self.obs_user_ids_first_name_dict.keys()),list(self.exp_user_ids_first_name_dict.keys()),)
        self.assertEqual(list(self.obs_user_ids_last_name_dict.keys()),list(self.exp_user_ids_last_name_dict.keys()),)
        self.assertEqual(list(self.obs_user_ids_country_code_dict.keys()),list(self.exp_user_ids_country_code_dict.keys()),)
        self.assertEqual(list(self.obs_user_ids_email_domain_dict.keys()),list(self.exp_user_ids_email_domain_dict.keys()),)
        self.assertEqual(list(self.obs_user_ids_dates_dict.keys()),list(self.exp_user_ids_dates_dict.keys()),)

    def test_values(self):
        self.assertEqual(list(self.obs_user_ids_cnts_dict.values()),list(self.exp_user_ids_cnts_dict.values()),)
        self.assertEqual(list(self.obs_user_ids_props_dict.values()),list(self.exp_user_ids_props_dict.values()),)
        self.assertEqual(list(self.obs_user_ids_first_name_dict.values()),list(self.exp_user_ids_first_name_dict.values()),)
        self.assertEqual(list(self.obs_user_ids_last_name_dict.values()),list(self.exp_user_ids_last_name_dict.values()),)
        self.assertEqual(list(self.obs_user_ids_country_code_dict.values()),list(self.exp_user_ids_country_code_dict.values()),)
        self.assertEqual(list(self.obs_user_ids_email_domain_dict.values()),list(self.exp_user_ids_email_domain_dict.values()),)
        self.assertEqual(list(self.obs_user_ids_dates_dict.values()),list(self.exp_user_ids_dates_dict.values()),)

    def test_object(self):
        self.assertEqual(self.obs_user_ids_cnts_dict, self.exp_user_ids_cnts_dict)
        self.assertEqual(self.obs_user_ids_props_dict, self.exp_user_ids_props_dict)
        self.assertEqual(self.obs_user_ids_first_name_dict, self.exp_user_ids_first_name_dict)
        self.assertEqual(self.obs_user_ids_last_name_dict, self.exp_user_ids_last_name_dict)
        self.assertEqual(self.obs_user_ids_country_code_dict, self.exp_user_ids_country_code_dict)
        self.assertEqual(self.obs_user_ids_email_domain_dict, self.exp_user_ids_email_domain_dict)
        self.assertEqual(self.obs_user_ids_dates_dict, self.exp_user_ids_dates_dict)
        self.assertEqual(self.obs_start_date, self.exp_start_date)
        self.assertEqual(self.obs_end_date, self.exp_end_date)
        self.assertEqual(self.obs_n_user_ids, self.exp_n_user_ids)
        self.assertEqual(self.obs_lam, self.exp_lam)


if __name__ == "__main__":
    unittest.main()
