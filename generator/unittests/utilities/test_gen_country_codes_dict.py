import unittest
import os
import sys
import numpy as np

sys.path.append(os.path.join(os.getcwd(), "generator"))

import cons
from utilities.gen_country_codes_dict import gen_country_codes_dict

np.random.seed(cons.unittest_seed)

idhashes = ["a", "b", "c", "d"]
exp_prop_dict = {"a": 276, "b": 756, "c": 642, "d": 826}
fpath_countries_europe = '.' + cons.fpath_countries_europe.split(cons.fpath_repo_dir)[1]
obs_prop_dict = gen_country_codes_dict(idhashes=idhashes, fpath_countries_europe=fpath_countries_europe)

class Test_gen_country_codes_dict(unittest.TestCase):
    """"""

    def setUp(self):
        self.idhashes = idhashes
        self.obs_prop_dict = obs_prop_dict
        self.exp_prop_dict = exp_prop_dict

    def test_type(self):
        self.assertEqual(type(self.obs_prop_dict), type(self.exp_prop_dict))

    def test_len(self):
        self.assertEqual(len(self.obs_prop_dict), len(self.exp_prop_dict))

    def test_keys(self):
        self.assertEqual(
            list(self.obs_prop_dict.keys()), list(self.exp_prop_dict.keys())
        )

    def test_values(self):
        self.assertEqual(
            list(self.obs_prop_dict.values()), list(self.exp_prop_dict.values())
        )

    def test_object(self):
        self.assertEqual(self.obs_prop_dict, self.exp_prop_dict)


if __name__ == "__main__":
    unittest.main()
