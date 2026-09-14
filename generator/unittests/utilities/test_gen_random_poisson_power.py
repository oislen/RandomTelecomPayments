import unittest
import os
import sys
import numpy as np

sys.path.append(os.path.join(os.getcwd(), "generator"))

import cons
from utilities.gen_random_poisson_power import gen_random_poisson_power

np.random.seed(cons.unittest_seed)

exp_random_poisson = np.array([11, 7, 1, 1])
obs_random_poisson = gen_random_poisson_power(lam=1, size=4, power=2)


class Test_gen_random_poisson_power(unittest.TestCase):
    """
    Unit tests for the gen_random_poisson_power utility function.

    Verifies that the Poisson-power random array has the correct shape and
    values when generated with a fixed seed.
    """

    def setUp(self):
        self.exp_random_poisson = exp_random_poisson
        self.obs_random_poisson = obs_random_poisson

    def test_type(self):
        self.assertEqual(type(self.obs_random_poisson), type(self.exp_random_poisson))

    def test_shape(self):
        self.assertEqual(self.obs_random_poisson.shape, self.exp_random_poisson.shape)

    def test_object(self):
        self.assertTrue((self.obs_random_poisson == self.exp_random_poisson).all())


if __name__ == "__main__":
    unittest.main()
