import unittest
import os
import sys
import numpy as np

sys.path.append(os.path.join(os.getcwd(), "generator"))

import cons
from utilities.gen_country_codes_map import gen_country_codes_map

np.random.seed(cons.unittest_seed)

exp_country_codes_map = {
    804: 'UA', 250: 'FR', 724: 'ES', 752: 'SE', 276: 'DE', 246: 'FI', 578: 'NO', 616: 'PL', 380: 'IT', 826: 'GB', 642: 'RO', 
    112: 'BY', 300: 'GR', 100: 'BG', 352: 'IS', 620: 'PT', 203: 'CZ', 208: 'DK', 348: 'HU', 688: 'RS', 40: 'AT', 372: 'IE', 
    440: 'LT', 428: 'LV', 191: 'HR', 70: 'BA', 703: 'SK', 233: 'EE', 528: 'NL', 756: 'CH', 498: 'MD', 56: 'BE', 8: 'AL', 
    807: 'MK', 705: 'SI', 499: 'ME', 196: 'CY', 442: 'LU', 234: 'FO', 20: 'AD', 470: 'MT', 438: 'LI', 831: 'GG', 674: 'SM', 
    292: 'GI', 492: 'MC', 336: 'VA'
    }

fpath_countries_europe = '.' + cons.fpath_countries_europe.split(cons.fpath_repo_dir)[1]
obs_country_codes_map = gen_country_codes_map(fpath_countries_europe=fpath_countries_europe)

class Test_gen_country_codes_map(unittest.TestCase):
    """"""

    def setUp(self):
        self.exp_country_codes_map = exp_country_codes_map
        self.obs_country_codes_map = obs_country_codes_map

    def test_type(self):
        self.assertEqual(type(self.exp_country_codes_map), type(self.obs_country_codes_map))

    def test_len(self):
        self.assertEqual(len(self.exp_country_codes_map), len(self.obs_country_codes_map))

    def test_keys(self):
        self.assertEqual(list(self.exp_country_codes_map.keys()), list(self.obs_country_codes_map.keys()))

    def test_values(self):
        self.assertEqual(list(self.exp_country_codes_map.values()), list(self.obs_country_codes_map.values()))


if __name__ == "__main__":
    unittest.main()
