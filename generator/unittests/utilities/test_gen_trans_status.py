import os
import random
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append(os.path.join(os.getcwd(), "generator"))

import cons
from utilities.gen_trans_status import gen_trans_status

# ---------------------------------------------------------------------------
# Shared rejection-rate fixtures
# ---------------------------------------------------------------------------
# Deliberately simple dictionaries that give deterministic, edge-case-covering
# rejection rates for the test row(s) used below.

_REJECTION_RATES_DICT = {
    "country_code_trans_reject_rate_dict": {"IE": 0.0, "DE": 0.0, "FR": 0.0},
    "domain_email_trans_reject_rate_dict": {"gmail.com": 0.0},
    "shared_devices_reject_rate_dict": {"d1": 0.0},
    "shared_ips_reject_rate_dict": {"i1": 0.0},
    "shared_cards_reject_rate_dict": {"c1": 0.0},
    "count_devices_reject_rate_dict": {"u001": 0.0},
    "count_ips_reject_rate_dict": {"u001": 0.0},
    "count_cards_reject_rate_dict": {"u001": 0.0},
}

# A rejection-rate dict where every rate is maximum – forces a "Rejected" path.
_HIGH_REJECTION_RATES_DICT = {
    "country_code_trans_reject_rate_dict": {"IE": 1.0, "DE": 1.0},
    "domain_email_trans_reject_rate_dict": {"gmail.com": 1.0},
    "shared_devices_reject_rate_dict": {"d1": 1.0},
    "shared_ips_reject_rate_dict": {"i1": 1.0},
    "shared_cards_reject_rate_dict": {"c1": 1.0},
    "count_devices_reject_rate_dict": {"u001": 1.0},
    "count_ips_reject_rate_dict": {"u001": 1.0},
    "count_cards_reject_rate_dict": {"u001": 1.0},
}

# Canonical "card-present" row (all fields populated)
_CARD_PRESENT_ROW = pd.Series(
    {
        "userid": "u001",
        "card_hash": "c1",
        "device_hash": "d1",
        "ip_hash": "i1",
        "email_domain": "gmail.com",
        "registration_country_code": "IE",
        "ip_country_code": "IE",
        "card_country_code": "IE",
    }
)

# Canonical "card-absent" row (card_hash is NaN)
_CARD_ABSENT_ROW = pd.Series(
    {
        "userid": "u001",
        "card_hash": np.nan,
        "device_hash": "d1",
        "ip_hash": "i1",
        "email_domain": "gmail.com",
        "registration_country_code": "IE",
        "ip_country_code": "IE",
        "card_country_code": np.nan,
    }
)

_VALID_STATUSES = {"Successful", "Pending", "Rejected"}
_VALID_ERROR_CODES = (
    set(cons.data_model_rejection_codes_fraud.keys())
    | set(cons.data_model_rejection_codes_connection.keys())
    | set(cons.data_model_rejection_codes_user.keys())
    | set(cons.data_model_rejection_codes_funds.keys())
    | set(cons.data_model_rejection_codes_authentication.keys())
)


class Test_gen_trans_status(unittest.TestCase):
    """
    Unit tests for the gen_trans_status utility function.

    Covers the two main code paths (card present vs card absent) and
    verifies return type, length, and that returned status / error-code
    values are drawn from the valid sets defined in cons.
    """

    # ------------------------------------------------------------------
    # Return structure
    # ------------------------------------------------------------------

    def test_returns_list(self):
        """gen_trans_status always returns a list."""
        result = gen_trans_status(
            series=_CARD_PRESENT_ROW,
            rejection_rates_dict=_REJECTION_RATES_DICT,
        )
        self.assertIsInstance(result, list)

    def test_returns_two_elements(self):
        """Returned list has exactly two elements: [status, error_code]."""
        result = gen_trans_status(
            series=_CARD_PRESENT_ROW,
            rejection_rates_dict=_REJECTION_RATES_DICT,
        )
        self.assertEqual(len(result), 2)

    # ------------------------------------------------------------------
    # Card-absent path
    # ------------------------------------------------------------------

    def test_card_absent_status_is_successful_or_pending(self):
        """When card_hash is NaN, status is Successful or Pending."""
        random.seed(cons.unittest_seed)
        np.random.seed(cons.unittest_seed)
        result = gen_trans_status(
            series=_CARD_ABSENT_ROW,
            rejection_rates_dict=_REJECTION_RATES_DICT,
        )
        self.assertIn(result[0], {"Successful", "Pending"})

    def test_card_absent_error_code_is_nan(self):
        """When card_hash is NaN, error_code is NaN."""
        random.seed(cons.unittest_seed)
        np.random.seed(cons.unittest_seed)
        result = gen_trans_status(
            series=_CARD_ABSENT_ROW,
            rejection_rates_dict=_REJECTION_RATES_DICT,
        )
        self.assertTrue(pd.isna(result[1]))

    # ------------------------------------------------------------------
    # Card-present path – low rejection rates → successful
    # ------------------------------------------------------------------

    def test_card_present_low_rates_status_in_valid_set(self):
        """With all rejection rates at 0, status is Successful or Pending."""
        random.seed(cons.unittest_seed)
        np.random.seed(cons.unittest_seed)
        result = gen_trans_status(
            series=_CARD_PRESENT_ROW,
            rejection_rates_dict=_REJECTION_RATES_DICT,
        )
        self.assertIn(result[0], {"Successful", "Pending"})

    def test_card_present_low_rates_error_code_is_nan(self):
        """With all rejection rates at 0, error_code is NaN."""
        random.seed(cons.unittest_seed)
        np.random.seed(cons.unittest_seed)
        result = gen_trans_status(
            series=_CARD_PRESENT_ROW,
            rejection_rates_dict=_REJECTION_RATES_DICT,
        )
        self.assertTrue(pd.isna(result[1]))

    # ------------------------------------------------------------------
    # Card-present path – high rejection rates → rejected
    # ------------------------------------------------------------------

    def test_card_present_high_rates_status_is_rejected(self):
        """With all rejection rates at 1.0, status is Rejected."""
        random.seed(cons.unittest_seed)
        np.random.seed(cons.unittest_seed)
        result = gen_trans_status(
            series=_CARD_PRESENT_ROW,
            rejection_rates_dict=_HIGH_REJECTION_RATES_DICT,
        )
        self.assertEqual(result[0], "Rejected")

    def test_card_present_high_rates_error_code_in_valid_set(self):
        """With all rejection rates at 1.0, error_code is a known error code."""
        random.seed(cons.unittest_seed)
        np.random.seed(cons.unittest_seed)
        result = gen_trans_status(
            series=_CARD_PRESENT_ROW,
            rejection_rates_dict=_HIGH_REJECTION_RATES_DICT,
        )
        self.assertIn(result[1], _VALID_ERROR_CODES)

    # ------------------------------------------------------------------
    # Status and error-code values are always from the valid universe
    # ------------------------------------------------------------------

    def test_status_always_in_valid_set_card_present(self):
        """Status value is always in the valid transaction status set (card present)."""
        for seed in range(10):
            random.seed(seed)
            np.random.seed(seed)
            result = gen_trans_status(
                series=_CARD_PRESENT_ROW,
                rejection_rates_dict=_REJECTION_RATES_DICT,
            )
            self.assertIn(result[0], _VALID_STATUSES)

    def test_error_code_is_nan_or_valid_string(self):
        """Error code is either NaN or a known rejection-code string."""
        for seed in range(10):
            random.seed(seed)
            np.random.seed(seed)
            result = gen_trans_status(
                series=_CARD_PRESENT_ROW,
                rejection_rates_dict=_REJECTION_RATES_DICT,
            )
            if not pd.isna(result[1]):
                self.assertIn(result[1], _VALID_ERROR_CODES)

    # ------------------------------------------------------------------
    # Rejected status implies a non-NaN error code
    # ------------------------------------------------------------------

    def test_rejected_status_has_error_code(self):
        """When status is Rejected, error_code must not be NaN."""
        random.seed(cons.unittest_seed)
        np.random.seed(cons.unittest_seed)
        result = gen_trans_status(
            series=_CARD_PRESENT_ROW,
            rejection_rates_dict=_HIGH_REJECTION_RATES_DICT,
        )
        if result[0] == "Rejected":
            self.assertFalse(pd.isna(result[1]))


if __name__ == "__main__":
    unittest.main()
