import unittest
import os
import sys
import numpy as np
import pandas as pd
import random

sys.path.append(os.path.join(os.getcwd(), "generator"))

import cons
from utilities.remove_duplicate_idhashes import remove_duplicate_idhashes

random.seed(cons.unittest_seed)
np.random.seed(seed=cons.unittest_seed)

obs_random_duplicate_idhashes_dict = {'idhashes':[['63cea7c46926aa74'], ['63cea7c46926aa74', '37725417bd51fb40'], ['b95cb80aae9fbbfe'], ['dded2b63f8242648']]}
obs_random_duplicate_idhashes_df = pd.DataFrame.from_dict(obs_random_duplicate_idhashes_dict, orient='columns')
obs_random_duplicate_idhashes = remove_duplicate_idhashes(user_data=obs_random_duplicate_idhashes_df, idhash_col='idhashes')

exp_random_duplicate_idhashes_dict = {'idhashes':[['63cea7c46926aa74'], ['37725417bd51fb40'], ['b95cb80aae9fbbfe'], ['dded2b63f8242648']]}
exp_random_duplicate_idhashes = pd.DataFrame.from_dict(exp_random_duplicate_idhashes_dict, orient='columns')

class Test_remove_duplicate_idhashes(unittest.TestCase):
    """
    Unit tests for the remove_duplicate_idhashes utility function.

    Verifies that duplicate idhash values across rows are removed, retaining
    the first occurrence in the correct row.
    """

    def setUp(self):
        self.exp_random_duplicate_idhashes = exp_random_duplicate_idhashes
        self.obs_random_duplicate_idhashes = obs_random_duplicate_idhashes

    def test_type(self):
        self.assertEqual(type(self.exp_random_duplicate_idhashes), type(self.obs_random_duplicate_idhashes))

    def test_shape(self):
        self.assertEqual(self.exp_random_duplicate_idhashes.shape, self.obs_random_duplicate_idhashes.shape)

    def test_columns(self):
        self.assertEqual(self.exp_random_duplicate_idhashes.columns.to_list(), self.obs_random_duplicate_idhashes.columns.to_list())

    def test_values(self):
        self.assertTrue((self.exp_random_duplicate_idhashes.values == self.exp_random_duplicate_idhashes.values).all().all())

if __name__ == "__main__":
    unittest.main()
