import os
import random
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append(os.path.join(os.getcwd(), "generator"))

import cons
from app import ProgrammeParams, gen_user_data
from objects import Application, Card, Device, Ip, Transaction, User
from utilities.gen_random_entity_counts import gen_random_entity_counts

# ---------------------------------------------------------------------------
# Shared setup – run once at module load with a fixed seed
# ---------------------------------------------------------------------------

random.seed(cons.unittest_seed)
np.random.seed(cons.unittest_seed)

_fpath_first_names = "." + cons.fpath_llama_first_names.split(cons.fpath_repo_dir)[1]
_fpath_last_names = "." + cons.fpath_llama_last_names.split(cons.fpath_repo_dir)[1]
_fpath_countries_europe = (
    "." + cons.fpath_countries_europe.split(cons.fpath_repo_dir)[1]
)
_fpath_email_domain = "." + cons.fpath_llama_email_domains.split(cons.fpath_repo_dir)[1]
_fpath_smartphones = "." + cons.fpath_smartphones.split(cons.fpath_repo_dir)[1]

_params = ProgrammeParams(
    n_users=cons.unittest_n_users,
    random_seed=cons.unittest_seed,
    registration_start_date=cons.unittest_registration_start_date,
    registration_end_date=cons.unittest_registration_end_date,
    transaction_start_date=cons.unittest_transaction_start_date,
    transaction_end_date=cons.unittest_transaction_end_date,
)

_user_obj = User(
    n_user_ids=_params.n_users,
    start_date=_params.registration_start_date,
    end_date=_params.registration_end_date,
    fpath_first_names=_fpath_first_names,
    fpath_last_names=_fpath_last_names,
    fpath_countries_europe=_fpath_countries_europe,
    fpath_email_domain=_fpath_email_domain,
)
_entity_counts = gen_random_entity_counts(
    user_obj=_user_obj, transaction_timescale=_params.transaction_timescale
)
_device_obj = Device(
    n_device_hashes=_entity_counts["n_devices"].sum(),
    fpath_smartphones=_fpath_smartphones,
)
_card_obj = Card(
    n_card_hashes=_entity_counts["n_cards"].sum(),
    fpath_countries_europe=_fpath_countries_europe,
)
_ip_obj = Ip(
    n_ip_hashes=_entity_counts["n_ips"].sum(),
    fpath_countries_europe=_fpath_countries_europe,
)
_transaction_obj = Transaction(
    n_transaction_hashes=_entity_counts["n_transactions"].sum(),
    start_date=_params.transaction_start_date,
    end_date=_params.transaction_end_date,
)
_application_obj = Application(n_application_hashes=_params.n_applications)

_user_data = gen_user_data(
    random_entity_counts=_entity_counts,
    user_obj=_user_obj,
    device_obj=_device_obj,
    card_obj=_card_obj,
    ip_obj=_ip_obj,
    transaction_obj=_transaction_obj,
    application_obj=_application_obj,
)

_EXPECTED_COLS = {
    "uid",
    "userid",
    "first_name",
    "last_name",
    "registration_date",
    "registration_country_code_alpha",
    "email_domain",
    "device_hash",
    "card_hash",
    "ip_hash",
    "transaction_hash",
    "application_hash",
    "itr_hash",
}
_LIST_COLS = [
    "device_hash",
    "card_hash",
    "ip_hash",
    "transaction_hash",
    "application_hash",
]


class TestGenUserData(unittest.TestCase):
    """
    Unit tests for the gen_user_data app-level function.

    Verifies that the user-level DataFrame returned has the correct type,
    shape, columns, and data-model invariants.
    """

    def setUp(self):
        self.user_data = _user_data

    # ------------------------------------------------------------------
    # Return type
    # ------------------------------------------------------------------

    def test_return_type(self):
        """Return value is a pandas DataFrame."""
        self.assertIsInstance(self.user_data, pd.DataFrame)

    # ------------------------------------------------------------------
    # Shape
    # ------------------------------------------------------------------

    def test_row_count_equals_n_users(self):
        """One row per user (n_users rows total)."""
        self.assertEqual(len(self.user_data), cons.unittest_n_users)

    # ------------------------------------------------------------------
    # Columns
    # ------------------------------------------------------------------

    def test_expected_columns_present(self):
        """All expected columns are present in the output."""
        for col in _EXPECTED_COLS:
            self.assertIn(col, self.user_data.columns, msg=f"Missing column: {col}")

    def test_count_columns_dropped(self):
        """Intermediate n_* count columns are removed from the output."""
        for col in [
            "n_devices",
            "n_cards",
            "n_ips",
            "n_transactions",
            "n_applications",
        ]:
            self.assertNotIn(
                col, self.user_data.columns, msg=f"Count column not dropped: {col}"
            )

    # ------------------------------------------------------------------
    # Key columns – nullability
    # ------------------------------------------------------------------

    def test_userid_not_null(self):
        """userid has no null values."""
        self.assertFalse(self.user_data["userid"].isnull().any())

    def test_uid_not_null(self):
        """uid has no null values."""
        self.assertFalse(self.user_data["uid"].isnull().any())

    def test_first_name_not_null(self):
        """first_name has no null values."""
        self.assertFalse(self.user_data["first_name"].isnull().any())

    def test_last_name_not_null(self):
        """last_name has no null values."""
        self.assertFalse(self.user_data["last_name"].isnull().any())

    def test_itr_hash_not_null(self):
        """itr_hash has no null values."""
        self.assertFalse(self.user_data["itr_hash"].isnull().any())

    # ------------------------------------------------------------------
    # uid uniqueness
    # ------------------------------------------------------------------

    def test_uid_unique(self):
        """Every uid value is unique across rows."""
        self.assertEqual(self.user_data["uid"].nunique(), len(self.user_data))

    # ------------------------------------------------------------------
    # itr_hash – all rows share the same iteration hash
    # ------------------------------------------------------------------

    def test_itr_hash_single_value(self):
        """All rows carry the same itr_hash (single generation run)."""
        self.assertEqual(self.user_data["itr_hash"].nunique(), 1)

    # ------------------------------------------------------------------
    # List columns contain lists
    # ------------------------------------------------------------------

    def test_hash_columns_contain_lists(self):
        """Entity-hash columns contain Python lists, not scalars."""
        for col in _LIST_COLS:
            sample = self.user_data[col].dropna().iloc[0]
            self.assertIsInstance(
                sample, list, msg=f"Column '{col}' is not list-valued"
            )

    # ------------------------------------------------------------------
    # registration_date is within the configured window
    # ------------------------------------------------------------------

    def test_registration_dates_within_range(self):
        """All registration_date values fall within the registration date window."""
        start = pd.Timestamp(cons.unittest_registration_start_date)
        end = pd.Timestamp(cons.unittest_registration_end_date)
        dates = pd.to_datetime(self.user_data["registration_date"])
        self.assertTrue((dates >= start).all())
        self.assertTrue((dates <= end).all())


if __name__ == "__main__":
    unittest.main()
