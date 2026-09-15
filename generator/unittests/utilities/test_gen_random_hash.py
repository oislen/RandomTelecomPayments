import os
import sys
import unittest

import numpy as np

sys.path.append(os.path.join(os.getcwd(), "generator"))

import cons
from utilities import gen_random_hash

np.random.seed(cons.unittest_seed)

exp_random_hash = [
    "63cea7c46926aa74",
    "37725417bd51fb40",
    "b95cb80aae9fbbfe",
    "dded2b63f8242648",
]
obs_random_hash = gen_random_hash(size=4, nbytes=16)


class Test_gen_random_hash(unittest.TestCase):
    """
    Unit tests for the gen_random_hash utility function.

    Verifies that a list of random hex-style hash strings of the requested
    size is produced deterministically when a random seed is fixed.
    """

    def setUp(self):
        self.obs_random_hash = obs_random_hash
        self.exp_random_hash = exp_random_hash

    def test_type(self):
        self.assertEqual(type(self.obs_random_hash), type(self.exp_random_hash))

    def test_len(self):
        self.assertEqual(len(self.obs_random_hash), len(self.exp_random_hash))

    def test_object(self):
        self.assertEqual(self.obs_random_hash, self.exp_random_hash)


if __name__ == "__main__":
    unittest.main()
