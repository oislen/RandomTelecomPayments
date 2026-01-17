import unittest
import os
import sys
import random
import numpy as np

sys.path.append(os.path.join(os.getcwd(), "generator"))

import cons
from utilities.gen_idhash_cnt_dict import gen_idhash_cnt_dict
from utilities.gen_shared_idhashes import gen_shared_idhashes

random.seed(cons.unittest_seed)
np.random.seed(cons.unittest_seed)

obs_prop_shared_idhashes=cons.data_model_shared_entities_dict["ip"]
idhashes = list(gen_idhash_cnt_dict(idhash_type="hash", n=4, lam=1, nbytes=16).keys())
obs_shared_idhashes = gen_shared_idhashes(idhashes=idhashes, prop_shared_idhashes=obs_prop_shared_idhashes)
exp_shared_idhashes = {}

class Test_gen_shared_idhashes(unittest.TestCase):
    """"""

    def setUp(self):
        self.exp_shared_idhashes = exp_shared_idhashes
        self.obs_shared_idhashes = obs_shared_idhashes

    def test_type(self):
        self.assertEqual(type(self.exp_shared_idhashes), type(self.obs_shared_idhashes))

    def test_len(self):
        self.assertEqual(len(self.exp_shared_idhashes), len(self.obs_shared_idhashes))

    def test_keys(self):
        self.assertEqual(list(self.exp_shared_idhashes.keys()), list(self.obs_shared_idhashes.keys()))

    def test_values(self):
        self.assertEqual(list(self.exp_shared_idhashes.values()), list(self.obs_shared_idhashes.values()))

if __name__ == "__main__":
    unittest.main()
