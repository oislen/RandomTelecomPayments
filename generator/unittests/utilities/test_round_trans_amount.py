import unittest
import os
import sys
import numpy as np
import pandas as pd
import random

sys.path.append(os.path.join(os.getcwd(), "generator"))

import cons
from utilities.round_trans_amount import round_trans_amount

random.seed(cons.unittest_seed)
np.random.seed(seed=cons.unittest_seed)

obs_amount = round_trans_amount(amounts=np.array([1, 2, 3]))
exp_amount = np.array([0.99, 1, 2.59])


class Test_round_trans_amount(unittest.TestCase):
    """
    Unit tests for the round_trans_amount utility function.

    Verifies that transaction amounts are rounded to common store-price-like
    endings (e.g. .99, .50, .45) in a deterministic manner when seeded.
    """

    def setUp(self):
        self.obs_amount = obs_amount
        self.exp_amount = exp_amount

    def test_type(self):
        self.assertEqual(type(self.obs_amount),type(self.exp_amount),)

    def test_shape(self):
        self.assertEqual(type(self.obs_amount.shape),type(self.exp_amount.shape),)

    def test_object(self):
        self.assertTrue((self.obs_amount == self.exp_amount).all())


if __name__ == "__main__":

    unittest.main()
