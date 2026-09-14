import unittest
import os
import sys

sys.path.append(os.path.join(os.getcwd(), "generator"))

from utilities.cnt2prop_dict import cnt2prop_dict


class Test_cnt2prop_dict(unittest.TestCase):
    """
    Unit tests for the cnt2prop_dict utility function.

    Verifies that a counts dictionary is correctly converted to a proportions
    dictionary where all values sum to 1.0.
    """

    def setUp(self):
        self.cnt_data = {"a": 1, "b": 2, "c": 3, "d": 4}
        self.obs_prop_dict = cnt2prop_dict(self.cnt_data)
        self.exp_prop_dict = {"a": 0.1, "b": 0.2, "c": 0.3, "d": 0.4}

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
