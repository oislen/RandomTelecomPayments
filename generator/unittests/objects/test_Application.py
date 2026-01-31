import unittest
import os
import sys
import random
import numpy as np

sys.path.append(os.path.join(os.getcwd(), "generator"))

import cons
from objects.Application import Application

exp_application_hashes_cnts_dict = {
    "63cea7c46926aa74": 1,
    "37725417bd51fb40": 5,
    "b95cb80aae9fbbfe": 2,
    "dded2b63f8242648": 3,
}
exp_application_hashes_prices_dict = {
    "63cea7c46926aa74": 1.51,
    "37725417bd51fb40": 0.44,
    "b95cb80aae9fbbfe": 7.63,
    "dded2b63f8242648": 0.32,
}
exp_application_hashes_props_dict = {
    "63cea7c46926aa74": 0.09090909090909091,
    "37725417bd51fb40": 0.45454545454545453,
    "b95cb80aae9fbbfe": 0.18181818181818182,
    "dded2b63f8242648": 0.2727272727272727,
}
exp_application_hashes_payment_channel_dict = {
    "63cea7c46926aa74": "Adyen",
    "37725417bd51fb40": "Adyen",
    "b95cb80aae9fbbfe": "PayPal",
    "dded2b63f8242648": "Docomo",
}
exp_n_application_hashes = cons.unittest_n_entities
exp_lam = cons.data_model_poisson_params["application"]["lambda"]
exp_payment_channels = cons.data_model_payment_channels

random.seed(cons.unittest_seed)
np.random.seed(cons.unittest_seed)
application_object = Application(n_application_hashes=exp_n_application_hashes)

obs_application_hashes_cnts_dict = application_object.application_hashes_cnts_dict
obs_application_hashes_props_dict = application_object.application_hashes_props_dict
obs_lam = application_object.lam
obs_n_application_hashes = application_object.n_application_hashes
obs_application_hashes_payment_channel_dict = application_object.application_hashes_payment_channel_dict
obs_payment_channels = application_object.payment_channels


class Test_Application(unittest.TestCase):
    """"""

    def setUp(self):
        self.exp_application_hashes_cnts_dict = exp_application_hashes_cnts_dict
        self.obs_application_hashes_cnts_dict = obs_application_hashes_cnts_dict
        self.exp_application_hashes_props_dict = exp_application_hashes_props_dict
        self.obs_application_hashes_props_dict = obs_application_hashes_props_dict
        self.exp_application_hashes_prices_dict = exp_application_hashes_prices_dict
        self.exp_n_application_hashes = exp_n_application_hashes
        self.obs_n_application_hashes = obs_n_application_hashes
        self.exp_lam = exp_lam
        self.obs_lam = obs_lam
        self.exp_application_hashes_payment_channel_dict = exp_application_hashes_payment_channel_dict
        self.obs_application_hashes_payment_channel_dict = obs_application_hashes_payment_channel_dict
        self.exp_payment_channels = exp_payment_channels
        self.obs_payment_channels = obs_payment_channels

    def test_type(self):
        self.assertEqual(type(self.obs_application_hashes_cnts_dict),type(self.exp_application_hashes_cnts_dict),)
        self.assertEqual(type(self.obs_application_hashes_props_dict),type(self.exp_application_hashes_props_dict),)
        self.assertEqual(type(self.obs_n_application_hashes), type(self.exp_n_application_hashes))
        self.assertEqual(type(self.obs_lam), type(self.exp_lam))
        self.assertEqual(type(self.obs_application_hashes_payment_channel_dict),type(self.exp_application_hashes_payment_channel_dict),)
        self.assertEqual(type(self.obs_payment_channels), type(self.exp_payment_channels))

    def test_len(self):
        self.assertEqual(len(self.obs_application_hashes_props_dict),len(self.exp_application_hashes_props_dict),)
        self.assertEqual(len(self.obs_application_hashes_cnts_dict),len(self.exp_application_hashes_cnts_dict),)
        self.assertEqual(len(self.obs_application_hashes_payment_channel_dict),len(self.exp_application_hashes_payment_channel_dict),)
        self.assertEqual(len(self.obs_payment_channels), len(self.exp_payment_channels))

    def test_keys(self):
        self.assertEqual(list(self.obs_application_hashes_props_dict.keys()),list(self.exp_application_hashes_props_dict.keys()),)
        self.assertEqual(list(self.obs_application_hashes_cnts_dict.keys()),list(self.exp_application_hashes_cnts_dict.keys()),)
        self.assertEqual(list(self.obs_application_hashes_payment_channel_dict.keys()),list(self.exp_application_hashes_payment_channel_dict.keys()),)
        self.assertEqual(list(self.obs_payment_channels.keys()),list(self.exp_payment_channels.keys()),)

    def test_values(self):
        self.assertEqual(list(self.obs_application_hashes_props_dict.values()),list(self.exp_application_hashes_props_dict.values()),)
        self.assertEqual(list(self.obs_application_hashes_cnts_dict.values()),list(self.exp_application_hashes_cnts_dict.values()),)
        self.assertEqual(list(self.obs_application_hashes_payment_channel_dict.values()),list(self.exp_application_hashes_payment_channel_dict.values()),)
        self.assertEqual(list(self.obs_payment_channels.values()),list(self.exp_payment_channels.values()),)

    def test_object(self):
        self.assertEqual(self.obs_application_hashes_cnts_dict, self.exp_application_hashes_cnts_dict)
        self.assertEqual(self.obs_application_hashes_props_dict,self.exp_application_hashes_props_dict,)
        self.assertEqual(self.obs_n_application_hashes, self.exp_n_application_hashes)
        self.assertEqual(self.obs_lam, self.exp_lam)
        self.assertEqual(self.obs_application_hashes_payment_channel_dict,self.exp_application_hashes_payment_channel_dict,)
        self.assertEqual(self.obs_payment_channels, self.exp_payment_channels)


if __name__ == "__main__":
    unittest.main()
