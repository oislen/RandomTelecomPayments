import os
import random
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append(os.path.join(os.getcwd(), "generator"))

import cons
from app.gen_trans_data import gen_trans_data
from app.gen_user_data import gen_user_data
from app.ProgrammeParams import ProgrammeParams
from objects.Application import Application
from objects.Card import Card
from objects.Device import Device
from objects.Ip import Ip
from objects.Transaction import Transaction
from objects.User import User
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
_fpath_countrycrimeindex = (
    "." + cons.fpath_countrycrimeindex.split(cons.fpath_repo_dir)[1]
)

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
_trans_data = gen_trans_data(
    user_data=_user_data,
    user_obj=_user_obj,
    device_obj=_device_obj,
    card_obj=_card_obj,
    ip_obj=_ip_obj,
    transaction_obj=_transaction_obj,
    application_obj=_application_obj,
    fpath_countrycrimeindex=_fpath_countrycrimeindex,
)

_EXPECTED_COLS = set(
    cons.user_cols
    + cons.device_cols
    + cons.card_cols
    + cons.ip_cols
    + cons.app_cols
    + cons.trans_cols
    + cons.itr_cols
)
_VALID_STATUSES = set(cons.data_model_transaction_status.keys())
_VALID_ERROR_CODES = (
    set(cons.data_model_rejection_codes_fraud.keys())
    | set(cons.data_model_rejection_codes_connection.keys())
    | set(cons.data_model_rejection_codes_user.keys())
    | set(cons.data_model_rejection_codes_funds.keys())
    | set(cons.data_model_rejection_codes_authentication.keys())
)
_VALID_PAYMENT_METHODS = {"Card", "Wallet", "Points"}
_VALID_CARD_TYPES = set(cons.data_model_card_types_dict.keys())
_VALID_CHANNELS = set(cons.data_model_payment_channels.keys())


class Test_gen_trans_data(unittest.TestCase):
    """
    Unit tests for the gen_trans_data app-level function.

    Verifies DataFrame structure, column completeness, data-model invariants,
    and business rules (e.g. rejected status ↔ non-null error code).
    """

    def setUp(self):
        self.trans_data = _trans_data

    # ------------------------------------------------------------------
    # Return type
    # ------------------------------------------------------------------

    def test_return_type(self):
        """Return value is a pandas DataFrame."""
        self.assertIsInstance(self.trans_data, pd.DataFrame)

    # ------------------------------------------------------------------
    # Non-empty
    # ------------------------------------------------------------------

    def test_non_empty(self):
        """trans_data contains at least one row."""
        self.assertGreater(len(self.trans_data), 0)

    # ------------------------------------------------------------------
    # Columns
    # ------------------------------------------------------------------

    def test_expected_columns_present(self):
        """All expected output columns are present."""
        for col in _EXPECTED_COLS:
            self.assertIn(col, self.trans_data.columns, msg=f"Missing column: {col}")

    def test_no_list_columns_remain(self):
        """No column still holds Python lists (all must be exploded to scalars)."""
        for col in self.trans_data.columns:
            non_null = self.trans_data[col].dropna()
            if not non_null.empty:
                self.assertNotIsInstance(
                    non_null.iloc[0],
                    list,
                    msg=f"Column '{col}' still contains lists",
                )

    # ------------------------------------------------------------------
    # Key non-nullable columns
    # ------------------------------------------------------------------

    def test_transaction_hash_not_null(self):
        """transaction_hash has no null values."""
        self.assertFalse(self.trans_data["transaction_hash"].isnull().any())

    def test_userid_not_null(self):
        """userid has no null values."""
        self.assertFalse(self.trans_data["userid"].isnull().any())

    def test_transaction_date_not_null(self):
        """transaction_date has no null values."""
        self.assertFalse(self.trans_data["transaction_date"].isnull().any())

    # ------------------------------------------------------------------
    # Sorting
    # ------------------------------------------------------------------

    def test_sorted_ascending_by_transaction_date(self):
        """Rows are ordered ascending by transaction_date."""
        dates = self.trans_data["transaction_date"].dropna()
        diffs = dates.diff().dropna()
        self.assertTrue((diffs >= pd.Timedelta(0)).all())

    # ------------------------------------------------------------------
    # Transaction status and error code
    # ------------------------------------------------------------------

    def test_transaction_status_in_valid_set(self):
        """All non-null transaction_status values belong to the valid set."""
        actual = set(self.trans_data["transaction_status"].dropna().unique())
        self.assertTrue(
            actual.issubset(_VALID_STATUSES),
            msg=f"Unexpected: {actual - _VALID_STATUSES}",
        )

    def test_rejected_rows_have_error_code(self):
        """Rows with status Rejected must have a non-null error code."""
        rejected = self.trans_data[self.trans_data["transaction_status"] == "Rejected"]
        if not rejected.empty:
            self.assertFalse(rejected["transaction_error_code"].isnull().any())

    def test_successful_pending_rows_have_no_error_code(self):
        """Rows with status Successful or Pending must not have an error code."""
        non_rejected = self.trans_data[
            self.trans_data["transaction_status"].isin({"Successful", "Pending"})
        ]
        self.assertTrue(non_rejected["transaction_error_code"].isnull().all())

    def test_error_codes_in_valid_set(self):
        """All non-null error codes are from the known rejection-code universe."""
        actual = set(self.trans_data["transaction_error_code"].dropna().unique())
        self.assertTrue(
            actual.issubset(_VALID_ERROR_CODES),
            msg=f"Unexpected: {actual - _VALID_ERROR_CODES}",
        )

    # ------------------------------------------------------------------
    # Payment method and channel
    # ------------------------------------------------------------------

    def test_payment_method_in_valid_set(self):
        """All non-null transaction_payment_method values are in the valid set."""
        actual = set(self.trans_data["transaction_payment_method"].dropna().unique())
        self.assertTrue(
            actual.issubset(_VALID_PAYMENT_METHODS),
            msg=f"Unexpected: {actual - _VALID_PAYMENT_METHODS}",
        )

    def test_card_type_in_valid_set(self):
        """All non-null card_type values are Visa or Mastercard."""
        actual = set(self.trans_data["card_type"].dropna().unique())
        self.assertTrue(
            actual.issubset(_VALID_CARD_TYPES),
            msg=f"Unexpected: {actual - _VALID_CARD_TYPES}",
        )

    def test_payment_channel_in_valid_set(self):
        """All non-null card_payment_channel values are known payment channels."""
        actual = set(self.trans_data["card_payment_channel"].dropna().unique())
        self.assertTrue(
            actual.issubset(_VALID_CHANNELS),
            msg=f"Unexpected: {actual - _VALID_CHANNELS}",
        )

    # ------------------------------------------------------------------
    # Relationship between card_hash and card_type
    # ------------------------------------------------------------------

    def test_null_card_hash_implies_null_card_type(self):
        """Rows with no card_hash must also have null card_type."""
        no_card = self.trans_data[self.trans_data["card_hash"].isnull()]
        self.assertTrue(no_card["card_type"].isnull().all())

    # ------------------------------------------------------------------
    # Transaction amount
    # ------------------------------------------------------------------

    def test_transaction_amount_non_negative(self):
        """All non-null transaction amounts are >= 0."""
        amounts = self.trans_data["transaction_amount"].dropna()
        self.assertTrue((amounts >= 0).all())

    # ------------------------------------------------------------------
    # User–transaction referential integrity
    # ------------------------------------------------------------------

    def test_all_userids_came_from_user_data(self):
        """Every userid in trans_data is present in user_data."""
        user_ids = set(_user_data["userid"])
        trans_ids = set(self.trans_data["userid"])
        self.assertTrue(trans_ids.issubset(user_ids))


if __name__ == "__main__":
    unittest.main()
