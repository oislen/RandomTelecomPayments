import os
import random
import sys
import unittest

import numpy as np

sys.path.append(os.path.join(os.getcwd(), "generator"))

import cons
from utilities import gen_idhash_cnt_dict

random.seed(cons.unittest_seed)
np.random.seed(cons.unittest_seed)

exp_id_dict = {
    "6374692674377254": 6,
    "1751409580926382": 3,
    "4264861381989413": 2,
    "6720317315593519": 4,
}
exp_hash_dict = {
    "86870b77ea207220": 12,
    "a49698b687b10f66": 3,
    "d742b75a2024ed20": 2,
    "496ed6a8ee99bc2e": 2,
}
obs_id_dict = gen_idhash_cnt_dict(idhash_type="id", n=4, lam=1, nbytes=16)
obs_hash_dict = gen_idhash_cnt_dict(idhash_type="hash", n=4, lam=1, nbytes=16)


class Test_gen_idhash_cnt_dict(unittest.TestCase):
    """
    Unit tests for the gen_idhash_cnt_dict utility function.

    Verifies that random id and hash dictionaries with associated Poisson-power
    counts are generated with the correct keys and values when a seed is fixed.
    """

    def setUp(self):
        self.obs_id_dict = obs_id_dict
        self.exp_id_dict = exp_id_dict
        self.obs_hash_dict = obs_hash_dict
        self.exp_hash_dict = exp_hash_dict

    def test_type(self):
        self.assertEqual(type(self.obs_id_dict), type(self.exp_id_dict))
        self.assertEqual(type(self.obs_hash_dict), type(self.exp_hash_dict))

    def test_len(self):
        self.assertEqual(len(self.obs_id_dict), len(self.exp_id_dict))
        self.assertEqual(len(self.obs_hash_dict), len(self.exp_hash_dict))

    def test_keys(self):
        self.assertEqual(list(self.obs_id_dict.keys()), list(self.exp_id_dict.keys()))
        self.assertEqual(
            list(self.obs_hash_dict.keys()), list(self.exp_hash_dict.keys())
        )

    def test_values(self):
        self.assertEqual(
            list(self.obs_id_dict.values()), list(self.exp_id_dict.values())
        )
        self.assertEqual(
            list(self.obs_hash_dict.values()), list(self.exp_hash_dict.values())
        )

    def test_object(self):
        self.assertEqual(self.obs_id_dict, self.exp_id_dict)
        self.assertEqual(self.obs_hash_dict, self.exp_hash_dict)


if __name__ == "__main__":
    unittest.main()
