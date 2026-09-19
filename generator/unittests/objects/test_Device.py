import os
import random
import sys
import unittest

import numpy as np

sys.path.append(os.path.join(os.getcwd(), "generator"))

import cons
from objects import Device

exp_device_hashes_cnts_dict = {
    "63cea7c46926aa74": 1,
    "37725417bd51fb40": 3,
    "b95cb80aae9fbbfe": 1,
    "dded2b63f8242648": 1,
}
exp_device_hashes_props_dict = {
    "63cea7c46926aa74": 0.16666666666666666,
    "37725417bd51fb40": 0.5,
    "b95cb80aae9fbbfe": 0.16666666666666666,
    "dded2b63f8242648": 0.16666666666666666,
}
exp_device_hashes_type_dict = {
    "63cea7c46926aa74": "Samsung Galaxy M53 5G",
    "37725417bd51fb40": "Lyf Earth 2",
    "b95cb80aae9fbbfe": "Nubia Red Magic 8 Pro 5G",
    "dded2b63f8242648": "Vivo Y73T",
}
exp_device_shared_idhash_map_dict = {}
exp_prop_shared_device_hashes = cons.data_model_shared_entities_dict["device"]
exp_n_device_hashes = cons.unittest_n_entities
exp_n_device_types = cons.unittest_n_device_types
exp_lam = cons.data_model_poisson_params["device"]["lambda"]

random.seed(cons.unittest_seed)
np.random.seed(cons.unittest_seed)

fpath_smartphones = "." + cons.fpath_smartphones.split(cons.fpath_repo_dir)[1]
device_object = Device(exp_n_device_hashes, fpath_smartphones=fpath_smartphones)

obs_device_hashes_cnts_dict = device_object.device_hashes_cnts_dict
obs_device_hashes_props_dict = device_object.device_hashes_props_dict
obs_device_hashes_type_dict = device_object.device_hashes_type_dict
obs_device_shared_idhash_map_dict = device_object.device_shared_idhash_map_dict
obs_prop_shared_device_hashes = device_object.prop_shared_device_hashes
obs_n_device_hashes = device_object.n_device_hashes
obs_lam = device_object.lam


class TestDevice(unittest.TestCase):
    """
    Unit tests for the Device data-model object.

    Verifies that device hash counts, proportions, device types, and
    shared-idhash mappings have the expected types, lengths, keys, and values
    when constructed with a fixed random seed.
    """

    def setUp(self):
        self.exp_device_hashes_cnts_dict = exp_device_hashes_cnts_dict
        self.obs_device_hashes_cnts_dict = obs_device_hashes_cnts_dict
        self.exp_device_hashes_props_dict = exp_device_hashes_props_dict
        self.obs_device_hashes_props_dict = obs_device_hashes_props_dict
        self.exp_device_hashes_type_dict = exp_device_hashes_type_dict
        self.obs_device_hashes_type_dict = obs_device_hashes_type_dict
        self.exp_device_shared_idhash_map_dict = exp_device_shared_idhash_map_dict
        self.obs_device_shared_idhash_map_dict = obs_device_shared_idhash_map_dict
        self.exp_prop_shared_device_hashes = exp_prop_shared_device_hashes
        self.obs_prop_shared_device_hashes = obs_prop_shared_device_hashes
        self.exp_n_device_hashes = exp_n_device_hashes
        self.obs_n_device_hashes = obs_n_device_hashes
        self.exp_n_device_types = exp_n_device_types
        self.exp_lam = exp_lam
        self.obs_lam = obs_lam

    def test_type(self):
        self.assertEqual(
            type(self.obs_device_hashes_cnts_dict),
            type(self.exp_device_hashes_cnts_dict),
        )
        self.assertEqual(
            type(self.obs_device_hashes_props_dict),
            type(self.exp_device_hashes_props_dict),
        )
        self.assertEqual(
            type(self.obs_device_hashes_type_dict),
            type(self.exp_device_hashes_type_dict),
        )
        self.assertEqual(
            type(self.obs_device_shared_idhash_map_dict),
            type(self.exp_device_shared_idhash_map_dict),
        )
        self.assertEqual(
            type(self.obs_prop_shared_device_hashes),
            type(self.exp_prop_shared_device_hashes),
        )
        self.assertEqual(type(self.obs_n_device_hashes), type(self.exp_n_device_hashes))
        self.assertEqual(type(self.obs_lam), type(self.exp_lam))

    def test_len(self):
        self.assertEqual(
            len(self.obs_device_hashes_cnts_dict), len(self.exp_device_hashes_cnts_dict)
        )
        self.assertEqual(
            len(self.obs_device_hashes_props_dict),
            len(self.exp_device_hashes_props_dict),
        )
        self.assertEqual(
            len(self.obs_device_hashes_type_dict), len(self.exp_device_hashes_type_dict)
        )
        self.assertEqual(
            len(self.obs_device_shared_idhash_map_dict),
            len(self.exp_device_shared_idhash_map_dict),
        )

    def test_keys(self):
        self.assertEqual(
            list(self.obs_device_hashes_cnts_dict.keys()),
            list(self.exp_device_hashes_cnts_dict.keys()),
        )
        self.assertEqual(
            list(self.obs_device_hashes_props_dict.keys()),
            list(self.exp_device_hashes_props_dict.keys()),
        )
        self.assertEqual(
            list(self.obs_device_hashes_type_dict.keys()),
            list(self.exp_device_hashes_type_dict.keys()),
        )
        self.assertEqual(
            list(self.obs_device_shared_idhash_map_dict.keys()),
            list(self.exp_device_shared_idhash_map_dict.keys()),
        )

    def test_values(self):
        self.assertEqual(
            list(self.obs_device_hashes_cnts_dict.values()),
            list(self.exp_device_hashes_cnts_dict.values()),
        )
        self.assertEqual(
            list(self.obs_device_hashes_props_dict.values()),
            list(self.exp_device_hashes_props_dict.values()),
        )
        self.assertEqual(
            list(self.obs_device_hashes_type_dict.values()),
            list(self.exp_device_hashes_type_dict.values()),
        )
        self.assertEqual(
            list(self.obs_device_shared_idhash_map_dict.values()),
            list(self.exp_device_shared_idhash_map_dict.values()),
        )

    def test_object(self):
        self.assertEqual(
            self.obs_device_hashes_cnts_dict, self.exp_device_hashes_cnts_dict
        )
        self.assertEqual(
            self.obs_device_hashes_props_dict, self.exp_device_hashes_props_dict
        )
        self.assertEqual(
            self.obs_device_hashes_type_dict, self.exp_device_hashes_type_dict
        )
        self.assertEqual(
            self.obs_device_shared_idhash_map_dict,
            self.exp_device_shared_idhash_map_dict,
        )
        self.assertEqual(
            self.obs_prop_shared_device_hashes, self.exp_prop_shared_device_hashes
        )
        self.assertEqual(self.obs_n_device_hashes, self.exp_n_device_hashes)
        self.assertEqual(self.obs_lam, self.exp_lam)


if __name__ == "__main__":
    unittest.main()
