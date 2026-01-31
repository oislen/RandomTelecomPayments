import unittest
import os
import sys
import random
import numpy as np

sys.path.append(os.path.join(os.getcwd(), "generator"))

import cons
from objects.Card import Card

exp_card_hashes_cnts_dict = {
    "63cea7c46926aa74": 1,
    "37725417bd51fb40": 3,
    "b95cb80aae9fbbfe": 1,
    "dded2b63f8242648": 1,
}
exp_card_hashes_type_dict = {
    "63cea7c46926aa74": "Visa",
    "37725417bd51fb40": "Mastercard",
    "b95cb80aae9fbbfe": "Visa",
    "dded2b63f8242648": "Mastercard",
}
exp_card_hashes_props_dict = {
    "63cea7c46926aa74": 0.16666666666666666,
    "37725417bd51fb40": 0.5,
    "b95cb80aae9fbbfe": 0.16666666666666666,
    "dded2b63f8242648": 0.16666666666666666,
}
exp_card_hashes_country_code_dict = {
    "63cea7c46926aa74": 276,
    "37725417bd51fb40": 380,
    "b95cb80aae9fbbfe": 380,
    "dded2b63f8242648": 250,
}
exp_card_shared_idhash_map_dic = {}
exp_card_types_dict = cons.data_model_card_types_dict
exp_prop_shared_card_hashes = cons.data_model_shared_entities_dict["card"]
exp_n_card_hashes = cons.unittest_n_entities
exp_lam = cons.data_model_poisson_params["card"]["lambda"]

random.seed(cons.unittest_seed)
np.random.seed(cons.unittest_seed)

fpath_countries_europe = '.' + cons.fpath_countries_europe.split(cons.fpath_repo_dir)[1]
card_object = Card(n_card_hashes=exp_n_card_hashes, fpath_countries_europe=fpath_countries_europe)

obs_card_hashes_cnts_dict = card_object.card_hashes_cnts_dict
obs_card_types_dict = card_object.card_types_dict
obs_card_hashes_type_dict = card_object.card_hashes_type_dict
obs_card_hashes_props_dict = card_object.card_hashes_props_dict
obs_card_hashes_country_code_dict = card_object.card_hashes_country_code_dict
obs_card_shared_idhash_map_dict = card_object.card_shared_idhash_map_dict
obs_prop_shared_card_hashes = card_object.prop_shared_card_hashes
obs_lam = card_object.lam
obs_n_card_hashes = card_object.n_card_hashes


class Test_Card(unittest.TestCase):
    """"""

    def setUp(self):
        self.exp_card_hashes_cnts_dict = exp_card_hashes_cnts_dict
        self.obs_card_hashes_cnts_dict = obs_card_hashes_cnts_dict
        self.exp_card_types_dict = exp_card_types_dict
        self.obs_card_types_dict = obs_card_types_dict
        self.exp_card_hashes_type_dict = exp_card_hashes_type_dict
        self.obs_card_hashes_type_dict = obs_card_hashes_type_dict
        self.exp_card_hashes_props_dict = exp_card_hashes_props_dict
        self.obs_card_hashes_props_dict = obs_card_hashes_props_dict
        self.exp_card_hashes_country_code_dict = exp_card_hashes_country_code_dict
        self.obs_card_hashes_country_code_dict = obs_card_hashes_country_code_dict
        self.exp_card_shared_idhash_map_dic = exp_card_shared_idhash_map_dic
        self.obs_card_shared_idhash_map_dict = obs_card_shared_idhash_map_dict
        self.exp_prop_shared_card_hashes = exp_prop_shared_card_hashes
        self.obs_prop_shared_card_hashes = obs_prop_shared_card_hashes
        self.exp_lam = exp_lam
        self.obs_lam = obs_lam
        self.exp_n_card_hashes = exp_n_card_hashes
        self.obs_n_card_hashes = obs_n_card_hashes

    def test_type(self):
        self.assertEqual(type(self.obs_card_hashes_cnts_dict), type(self.exp_card_hashes_cnts_dict))
        self.assertEqual(type(self.obs_card_types_dict), type(self.exp_card_types_dict))
        self.assertEqual(type(self.obs_card_hashes_type_dict), type(self.exp_card_hashes_type_dict))
        self.assertEqual(type(self.obs_card_hashes_props_dict), type(self.exp_card_hashes_props_dict))
        self.assertEqual(type(self.obs_prop_shared_card_hashes),type(self.exp_prop_shared_card_hashes),)
        self.assertEqual(type(self.obs_card_hashes_country_code_dict),type(self.exp_card_hashes_country_code_dict),)
        self.assertEqual(type(self.obs_card_shared_idhash_map_dict),type(self.exp_card_shared_idhash_map_dic),)
        self.assertEqual(type(self.obs_lam), type(self.exp_lam))
        self.assertEqual(type(self.obs_n_card_hashes), type(self.exp_n_card_hashes))

    def test_len(self):
        self.assertEqual(len(self.obs_card_hashes_cnts_dict), len(self.exp_card_hashes_cnts_dict))
        self.assertEqual(len(self.obs_card_types_dict), len(self.exp_card_types_dict))
        self.assertEqual(len(self.obs_card_hashes_type_dict), len(self.exp_card_hashes_type_dict))
        self.assertEqual(len(self.obs_card_hashes_props_dict), len(self.exp_card_hashes_props_dict))
        self.assertEqual(len(self.obs_card_hashes_country_code_dict),len(self.exp_card_hashes_country_code_dict),)
        self.assertEqual(len(self.obs_card_shared_idhash_map_dict),len(self.exp_card_shared_idhash_map_dic),)

    def test_keys(self):
        self.assertEqual(list(self.obs_card_hashes_cnts_dict.keys()),list(self.exp_card_hashes_cnts_dict.keys()),)
        self.assertEqual(list(self.obs_card_types_dict.keys()), list(self.exp_card_types_dict.keys()))
        self.assertEqual(list(self.obs_card_hashes_type_dict.keys()),list(self.exp_card_hashes_type_dict.keys()),)
        self.assertEqual(list(self.obs_card_hashes_props_dict.keys()),list(self.exp_card_hashes_props_dict.keys()),)
        self.assertEqual(list(self.obs_card_hashes_country_code_dict.keys()),list(self.exp_card_hashes_country_code_dict.keys()),)
        self.assertEqual(list(self.obs_card_shared_idhash_map_dict.keys()),list(self.exp_card_shared_idhash_map_dic.keys()),)

    def test_values(self):
        self.assertEqual(list(self.obs_card_hashes_cnts_dict.values()),list(self.exp_card_hashes_cnts_dict.values()),)
        self.assertEqual(list(self.obs_card_types_dict.values()),list(self.exp_card_types_dict.values()),)
        self.assertEqual(list(self.obs_card_hashes_type_dict.values()),list(self.exp_card_hashes_type_dict.values()),)
        self.assertEqual(list(self.obs_card_hashes_props_dict.values()),list(self.exp_card_hashes_props_dict.values()),)
        self.assertEqual(list(self.obs_card_hashes_country_code_dict.values()),list(self.exp_card_hashes_country_code_dict.values()),)
        self.assertEqual(list(self.obs_card_shared_idhash_map_dict.values()),list(self.exp_card_shared_idhash_map_dic.values()),)

    def test_object(self):
        self.assertEqual(self.obs_card_hashes_cnts_dict, self.exp_card_hashes_cnts_dict)
        self.assertEqual(self.obs_card_types_dict, self.exp_card_types_dict)
        self.assertEqual(self.obs_card_hashes_type_dict, self.exp_card_hashes_type_dict)
        self.assertEqual(self.obs_card_hashes_props_dict, self.exp_card_hashes_props_dict)
        self.assertEqual(self.obs_prop_shared_card_hashes, self.exp_prop_shared_card_hashes)
        self.assertEqual(self.obs_card_hashes_country_code_dict,self.exp_card_hashes_country_code_dict,)
        self.assertEqual(self.obs_card_shared_idhash_map_dict,self.exp_card_shared_idhash_map_dic,)
        self.assertEqual(self.obs_lam, self.exp_lam)
        self.assertEqual(self.obs_n_card_hashes, self.exp_n_card_hashes)


if __name__ == "__main__":
    unittest.main()
