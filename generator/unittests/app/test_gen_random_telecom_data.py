import unittest
import os
import sys
import random

import numpy as np
import pandas as pd

sys.path.append(os.path.join(os.getcwd(), "generator"))

import cons
from app.gen_random_telecom_data import gen_random_telecom_data

# Run once at module load with a fixed seed so the test is deterministic.
random.seed(cons.unittest_seed)
np.random.seed(cons.unittest_seed)

_result = gen_random_telecom_data(
    n_users=cons.unittest_n_users,
    random_seed=cons.unittest_seed,
    n_applications=cons.default_n_applications,
    registration_start_date=cons.unittest_registration_start_date,
    registration_end_date=cons.unittest_registration_end_date,
    transaction_start_date=cons.unittest_transaction_start_date,
    transaction_end_date=cons.unittest_transaction_end_date,
)

_EXPECTED_USER_COLS = set(cons.user_cols)
_EXPECTED_TRANS_COLS = set(
    cons.user_cols + cons.device_cols + cons.card_cols +
    cons.ip_cols + cons.app_cols + cons.trans_cols + cons.itr_cols
)


class Test_gen_random_telecom_data(unittest.TestCase):
    """
    Unit tests for the gen_random_telecom_data top-level orchestration function.

    Checks return type, dictionary keys, DataFrame structure, column presence,
    and basic data-model invariants on a small seeded run.
    """

    def setUp(self):
        self.result = _result
        self.user_data = _result["user_data"]
        self.trans_data = _result["trans_data"]

    # ------------------------------------------------------------------
    # Return type and keys
    # ------------------------------------------------------------------

    def test_return_type(self):
        """Return value is a dict."""
        self.assertIsInstance(self.result, dict)

    def test_return_keys(self):
        """Dict contains exactly 'user_data' and 'trans_data'."""
        self.assertEqual(set(self.result.keys()), {"user_data", "trans_data"})

    # ------------------------------------------------------------------
    # user_data DataFrame
    # ------------------------------------------------------------------

    def test_user_data_type(self):
        """user_data is a pandas DataFrame."""
        self.assertIsInstance(self.user_data, pd.DataFrame)

    def test_user_data_row_count(self):
        """user_data has exactly n_users rows."""
        self.assertEqual(len(self.user_data), cons.unittest_n_users)

    def test_user_data_contains_expected_columns(self):
        """user_data contains all expected user-level columns."""
        for col in _EXPECTED_USER_COLS:
            self.assertIn(col, self.user_data.columns, msg=f"Missing column: {col}")

    def test_user_data_uid_unique(self):
        """Every uid in user_data is unique."""
        self.assertEqual(self.user_data["uid"].nunique(), len(self.user_data))

    def test_user_data_userid_not_null(self):
        """userid column has no null values."""
        self.assertFalse(self.user_data["userid"].isnull().any())

    # ------------------------------------------------------------------
    # trans_data DataFrame
    # ------------------------------------------------------------------

    def test_trans_data_type(self):
        """trans_data is a pandas DataFrame."""
        self.assertIsInstance(self.trans_data, pd.DataFrame)

    def test_trans_data_non_empty(self):
        """trans_data has at least one row."""
        self.assertGreater(len(self.trans_data), 0)

    def test_trans_data_contains_expected_columns(self):
        """trans_data contains all expected transaction-level columns."""
        for col in _EXPECTED_TRANS_COLS:
            self.assertIn(col, self.trans_data.columns, msg=f"Missing column: {col}")

    def test_trans_data_transaction_hash_not_null(self):
        """transaction_hash has no null values."""
        self.assertFalse(self.trans_data["transaction_hash"].isnull().any())

    def test_trans_data_transaction_status_valid(self):
        """All non-null transaction_status values are within the valid set."""
        valid = set(cons.data_model_transaction_status.keys())
        actual = set(self.trans_data["transaction_status"].dropna().unique())
        self.assertTrue(actual.issubset(valid), msg=f"Unexpected statuses: {actual - valid}")

    def test_trans_data_sorted_by_transaction_date(self):
        """trans_data is sorted ascending by transaction_date."""
        dates = self.trans_data["transaction_date"].dropna()
        self.assertTrue((dates.diff().dropna() >= pd.Timedelta(0)).all())

    def test_trans_data_all_userids_in_user_data(self):
        """Every userid in trans_data exists in user_data."""
        user_ids = set(self.user_data["userid"])
        trans_user_ids = set(self.trans_data["userid"])
        self.assertTrue(trans_user_ids.issubset(user_ids))

    # ------------------------------------------------------------------
    # Error-code / status consistency
    # ------------------------------------------------------------------

    def test_successful_pending_have_no_error_code(self):
        """Rows with status Successful or Pending should not have an error code."""
        non_rejected = self.trans_data[
            self.trans_data["transaction_status"].isin({"Successful", "Pending"})
        ]
        self.assertTrue(non_rejected["transaction_error_code"].isnull().all())

    def test_rejected_have_error_code(self):
        """Rows with status Rejected must have a non-null error code."""
        rejected = self.trans_data[self.trans_data["transaction_status"] == "Rejected"]
        if not rejected.empty:
            self.assertFalse(rejected["transaction_error_code"].isnull().any())


if __name__ == "__main__":
    unittest.main()
