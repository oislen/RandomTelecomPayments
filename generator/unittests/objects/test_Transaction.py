import unittest
import os
import sys
import random
import numpy as np

sys.path.append(os.path.join(os.getcwd(), "generator"))

import cons
from objects.Transaction import Transaction

exp_transaction_hashes_cnts_dict = {
    "63cea7c46926aa74": 10,
    "37725417bd51fb40": 30,
    "b95cb80aae9fbbfe": 32,
    "dded2b63f8242648": 44,
}
exp_transaction_hashes_props_dict = {
    "63cea7c46926aa74": 0.08620689655172414,
    "37725417bd51fb40": 0.25862068965517243,
    "b95cb80aae9fbbfe": 0.27586206896551724,
    "dded2b63f8242648": 0.3793103448275862,
}
exp_transaction_hashes_status_dict = {
    "63cea7c46926aa74": "Successful",
    "37725417bd51fb40": "Successful",
    "b95cb80aae9fbbfe": "Successful",
    "dded2b63f8242648": "Successful",
}
exp_transaction_hashes_amounts_dict = {
    "63cea7c46926aa74": 2.99,
    "37725417bd51fb40": 7.59,
    "b95cb80aae9fbbfe": 0.59,
    "dded2b63f8242648": 4.55,
}
exp_transaction_status = cons.data_model_transaction_status
exp_n_transaction_hashes = cons.unittest_n_entities
exp_start_date = cons.unittest_transaction_start_date
exp_end_date = cons.unittest_transaction_end_date
exp_lam = cons.data_model_poisson_params["transaction"]["lambda"]

random.seed(cons.unittest_seed)
np.random.seed(cons.unittest_seed)
transaction_object = Transaction(exp_n_transaction_hashes, exp_start_date, exp_end_date)

obs_transaction_hashes_cnts_dict = transaction_object.transaction_hashes_cnts_dict
obs_transaction_hashes_props_dict = transaction_object.transaction_hashes_props_dict
obs_transaction_hashes_status_dict = transaction_object.transaction_hashes_status_dict
obs_transaction_hashes_amounts_dict = transaction_object.transaction_hashes_amounts_dict
obs_transaction_status = transaction_object.transaction_status
obs_start_date = transaction_object.start_date
obs_end_date = transaction_object.end_date
obs_n_transaction_hashes = transaction_object.n_transaction_hashes
obs_lam = transaction_object.lam


class Test_Transaction(unittest.TestCase):
    """"""

    def setUp(self):
        self.exp_transaction_hashes_cnts_dict = exp_transaction_hashes_cnts_dict
        self.obs_transaction_hashes_cnts_dict = obs_transaction_hashes_cnts_dict
        self.exp_transaction_hashes_props_dict = exp_transaction_hashes_props_dict
        self.obs_transaction_hashes_props_dict = obs_transaction_hashes_props_dict
        self.exp_transaction_hashes_status_dict = exp_transaction_hashes_status_dict
        self.obs_transaction_hashes_status_dict = obs_transaction_hashes_status_dict
        self.exp_transaction_hashes_amounts_dict = exp_transaction_hashes_amounts_dict
        self.obs_transaction_hashes_amounts_dict = obs_transaction_hashes_amounts_dict
        self.exp_transaction_status = exp_transaction_status
        self.obs_transaction_status = obs_transaction_status
        self.exp_start_date = exp_start_date
        self.obs_start_date = obs_start_date
        self.exp_end_date = exp_end_date
        self.obs_end_date = obs_end_date
        self.exp_n_transaction_hashes = exp_n_transaction_hashes
        self.obs_n_transaction_hashes = obs_n_transaction_hashes
        self.exp_lam = exp_lam
        self.obs_lam = obs_lam

    def test_type(self):
        self.assertEqual(type(self.obs_transaction_hashes_cnts_dict),type(self.exp_transaction_hashes_cnts_dict),)
        self.assertEqual(type(self.obs_transaction_hashes_props_dict),type(self.exp_transaction_hashes_props_dict),)
        self.assertEqual(type(self.obs_transaction_hashes_status_dict),type(self.exp_transaction_hashes_status_dict),)
        self.assertEqual(type(self.obs_transaction_hashes_amounts_dict),type(self.exp_transaction_hashes_amounts_dict),)
        self.assertEqual(type(self.obs_transaction_status), type(self.exp_transaction_status))
        self.assertEqual(type(self.obs_start_date), type(self.exp_start_date))
        self.assertEqual(type(self.obs_end_date), type(self.exp_end_date))
        self.assertEqual(type(self.obs_n_transaction_hashes), type(self.exp_n_transaction_hashes))
        self.assertEqual(type(self.obs_lam), type(self.exp_lam))

    def test_len(self):
        self.assertEqual(len(self.obs_transaction_hashes_cnts_dict),len(self.exp_transaction_hashes_cnts_dict),)
        self.assertEqual(len(self.obs_transaction_hashes_props_dict),len(self.exp_transaction_hashes_props_dict),)
        self.assertEqual(len(self.obs_transaction_hashes_status_dict),len(self.exp_transaction_hashes_status_dict),)
        self.assertEqual(len(self.obs_transaction_hashes_amounts_dict),len(self.exp_transaction_hashes_amounts_dict),)
        self.assertEqual(len(self.obs_transaction_status), len(self.exp_transaction_status))

    def test_keys(self):
        self.assertEqual(list(self.obs_transaction_hashes_cnts_dict.keys()),list(self.exp_transaction_hashes_cnts_dict.keys()),)
        self.assertEqual(list(self.obs_transaction_hashes_props_dict.keys()),list(self.exp_transaction_hashes_props_dict.keys()),)
        self.assertEqual(list(self.obs_transaction_hashes_status_dict.keys()),list(self.exp_transaction_hashes_status_dict.keys()),)
        self.assertEqual(list(self.obs_transaction_status.keys()),list(self.exp_transaction_status.keys()),)
        self.assertEqual(list(self.obs_transaction_hashes_amounts_dict.keys()),list(self.exp_transaction_hashes_amounts_dict.keys()),)

    def test_values(self):
        self.assertEqual(list(self.obs_transaction_hashes_cnts_dict.values()),list(self.exp_transaction_hashes_cnts_dict.values()),)
        self.assertEqual(list(self.obs_transaction_hashes_props_dict.values()),list(self.exp_transaction_hashes_props_dict.values()),)
        self.assertEqual(list(self.obs_transaction_hashes_status_dict.values()),list(self.exp_transaction_hashes_status_dict.values()),)
        self.assertEqual(list(self.obs_transaction_status.values()),list(self.exp_transaction_status.values()),)
        self.assertEqual(list(self.obs_transaction_hashes_amounts_dict.values()),list(self.exp_transaction_hashes_amounts_dict.values()),)

    def test_object(self):
        self.assertEqual(self.obs_transaction_hashes_cnts_dict, self.exp_transaction_hashes_cnts_dict)
        self.assertEqual(self.obs_transaction_hashes_props_dict,self.exp_transaction_hashes_props_dict,)
        self.assertEqual(self.obs_transaction_hashes_status_dict,self.exp_transaction_hashes_status_dict,)
        self.assertEqual(self.obs_transaction_hashes_amounts_dict,self.exp_transaction_hashes_amounts_dict,)
        self.assertEqual(self.obs_transaction_status, self.exp_transaction_status)
        self.assertEqual(self.obs_start_date, self.exp_start_date)
        self.assertEqual(self.obs_end_date, self.exp_end_date)
        self.assertEqual(self.obs_n_transaction_hashes, self.exp_n_transaction_hashes)
        self.assertEqual(self.obs_lam, self.exp_lam)


if __name__ == "__main__":
    unittest.main()
