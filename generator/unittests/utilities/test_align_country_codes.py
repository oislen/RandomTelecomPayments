import unittest
import os
import sys
import numpy as np
import pandas as pd
import random

sys.path.append(os.path.join(os.getcwd(), "generator"))

import cons
from utilities.align_country_codes import align_country_codes

random.seed(cons.unittest_seed)

input_data_df = pd.DataFrame.from_records(
    [
        {
            "registration_country_code_alpha": 353,
            "ip_country_code_alpha": 42.0,
            "card_country_code_alpha": 42.0,
        },
        {
            "registration_country_code_alpha": 353,
            "ip_country_code_alpha": 42.0,
            "card_country_code_alpha": np.nan,
        },
        {
            "registration_country_code_alpha": 42,
            "ip_country_code_alpha": 42.0,
            "card_country_code_alpha": 42,
        },
        {
            "registration_country_code_alpha": 42,
            "ip_country_code_alpha": np.nan,
            "card_country_code_alpha": np.nan,
        },
    ]
)
exp_data_df = pd.DataFrame.from_records(
    [
        {
            "registration_country_code_alpha": 353.0,
            "ip_country_code_alpha": 353,
            "card_country_code_alpha": 353,
        },
        {
            "registration_country_code_alpha": 353,
            "ip_country_code_alpha": 42.0,
            "card_country_code_alpha": np.nan,
        },
        {
            "registration_country_code_alpha": 42,
            "ip_country_code_alpha": 42.0,
            "card_country_code_alpha": 42.0,
        },
        {
            "registration_country_code_alpha": 42,
            "ip_country_code_alpha": np.nan,
            "card_country_code_alpha": np.nan,
        },
    ]
)
obs_data_df = input_data_df.apply(
    lambda series: align_country_codes(
        series, proba_comm_ip=0.05, proba_comm_card=0.01
    ),
    axis=1,
)


class Test_align_country_codes(unittest.TestCase):
    """"""

    def setUp(self):
        self.input_data_df = input_data_df
        self.obs_data_df = obs_data_df
        self.exp_data_df = exp_data_df

    def test_type(self):
        self.assertEqual(type(self.obs_data_df), type(self.exp_data_df))

    def test_shape(self):
        self.assertEqual(self.obs_data_df.shape, self.exp_data_df.shape)

    def test_dtypes(self):
        self.assertTrue((self.obs_data_df.dtypes == self.exp_data_df.dtypes).all())

    def test_isnull(self):
        self.assertTrue(
            (self.obs_data_df.isnull() == self.exp_data_df.isnull()).all().all()
        )

    def test_notnull(self):
        self.assertTrue(
            (self.obs_data_df.notnull() == self.exp_data_df.notnull()).all().all()
        )

    def test_object(self):
        self.assertTrue(
            (self.obs_data_df.fillna(-999.0) == self.exp_data_df.fillna(-999.0))
            .all()
            .all()
        )


if __name__ == "__main__":
    unittest.main()
