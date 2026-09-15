import os
import random
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append(os.path.join(os.getcwd(), "generator"))

import cons
from utilities import gen_trans_rejection_rates

# Build a minimal but realistic transaction DataFrame with the columns
# that gen_trans_rejection_rates reads.
random.seed(cons.unittest_seed)
np.random.seed(cons.unittest_seed)

_trans_data = pd.DataFrame(
    {
        "userid": ["u001", "u001", "u002", "u002", "u003"],
        "device_hash": ["d1", "d1", "d2", "d3", "d2"],
        "ip_hash": ["i1", "i2", "i1", "i3", "i3"],
        "card_hash": ["c1", "c2", "c2", None, "c3"],
        "email_domain": [
            "gmail.com",
            "gmail.com",
            "yahoo.com",
            "yahoo.com",
            "hotmail.com",
        ],
        "registration_country_code": ["IE", "IE", "DE", "DE", "FR"],
        "ip_country_code": ["IE", "IE", "DE", "DE", "FR"],
        "card_country_code": ["IE", "IE", "DE", None, "FR"],
    }
)

fpath_countries_europe = "." + cons.fpath_countries_europe.split(cons.fpath_repo_dir)[1]
fpath_countrycrimeindex = (
    "." + cons.fpath_countrycrimeindex.split(cons.fpath_repo_dir)[1]
)
# gen_trans_rejection_rates reads 'email_domains' and 'probability' columns,
# which are present in llama_email_domains.csv, not in email-domains.csv.
# Pass the file that matches the column names the function actually uses.
fpath_email_domain = "." + cons.fpath_llama_email_domains.split(cons.fpath_repo_dir)[1]

obs_rejection_rates_dict = gen_trans_rejection_rates(
    trans_data=_trans_data,
    fpath_countries_europe=fpath_countries_europe,
    fpath_countrycrimeindex=fpath_countrycrimeindex,
    fpath_email_domain=fpath_email_domain,
)

_EXPECTED_TOP_KEYS = {
    "country_code_trans_reject_rate_dict",
    "domain_email_trans_reject_rate_dict",
    "shared_devices_reject_rate_dict",
    "shared_ips_reject_rate_dict",
    "shared_cards_reject_rate_dict",
    "count_devices_reject_rate_dict",
    "count_ips_reject_rate_dict",
    "count_cards_reject_rate_dict",
}


class Test_gen_trans_rejection_rates(unittest.TestCase):
    """
    Unit tests for the gen_trans_rejection_rates utility function.

    Checks the structure, types, and basic statistical properties of the
    rejection-rate dictionaries produced from a small synthetic transaction
    DataFrame.
    """

    def setUp(self):
        self.result = obs_rejection_rates_dict

    # ------------------------------------------------------------------
    # Return type
    # ------------------------------------------------------------------

    def test_return_type(self):
        """Return value is a dict."""
        self.assertIsInstance(self.result, dict)

    # ------------------------------------------------------------------
    # Top-level keys
    # ------------------------------------------------------------------

    def test_top_level_keys_present(self):
        """All eight expected top-level keys are present."""
        self.assertEqual(set(self.result.keys()), _EXPECTED_TOP_KEYS)

    # ------------------------------------------------------------------
    # Inner dict types
    # ------------------------------------------------------------------

    def test_all_values_are_dicts(self):
        """Every value in the outer dict is itself a dict."""
        for key, value in self.result.items():
            self.assertIsInstance(value, dict, msg=f"Key '{key}' is not a dict")

    def test_inner_values_are_floats(self):
        """All values within each inner dict are floats."""
        for outer_key, inner_dict in self.result.items():
            for inner_key, rate in inner_dict.items():
                self.assertIsInstance(
                    rate,
                    float,
                    msg=f"Non-float at result['{outer_key}']['{inner_key}'] = {rate!r}",
                )

    # ------------------------------------------------------------------
    # Country-code rejection rates
    # ------------------------------------------------------------------

    def test_country_code_dict_non_empty(self):
        """Country-code rejection rate dict contains at least one entry."""
        self.assertGreater(len(self.result["country_code_trans_reject_rate_dict"]), 0)

    def test_country_code_rates_sum_to_one(self):
        """Country-code rejection rates sum approximately to 1.0."""
        total = sum(self.result["country_code_trans_reject_rate_dict"].values())
        self.assertAlmostEqual(total, 1.0, places=5)

    def test_country_code_rates_non_negative(self):
        """All country-code rejection rates are >= 0."""
        for rate in self.result["country_code_trans_reject_rate_dict"].values():
            self.assertGreaterEqual(rate, 0.0)

    # ------------------------------------------------------------------
    # Email-domain rejection rates
    # ------------------------------------------------------------------

    def test_domain_email_dict_non_empty(self):
        """Email-domain rejection rate dict contains at least one entry."""
        self.assertGreater(len(self.result["domain_email_trans_reject_rate_dict"]), 0)

    def test_domain_email_rates_sum_to_one(self):
        """Email-domain rejection rates sum approximately to 1.0."""
        total = sum(self.result["domain_email_trans_reject_rate_dict"].values())
        self.assertAlmostEqual(total, 1.0, places=5)

    def test_domain_email_rates_non_negative(self):
        """All email-domain rejection rates are >= 0."""
        for rate in self.result["domain_email_trans_reject_rate_dict"].values():
            self.assertGreaterEqual(rate, 0.0)

    # ------------------------------------------------------------------
    # Shared-entity and count-based rejection rates
    # ------------------------------------------------------------------

    def test_shared_device_keys_match_transaction_device_hashes(self):
        """shared_devices_reject_rate_dict keys are the unique device hashes."""
        self.assertEqual(
            set(self.result["shared_devices_reject_rate_dict"].keys()),
            set(_trans_data["device_hash"].unique()),
        )

    def test_shared_ip_keys_match_transaction_ip_hashes(self):
        """shared_ips_reject_rate_dict keys are the unique ip hashes."""
        self.assertEqual(
            set(self.result["shared_ips_reject_rate_dict"].keys()),
            set(_trans_data["ip_hash"].unique()),
        )

    def test_count_device_keys_match_userids(self):
        """count_devices_reject_rate_dict keys are the unique user IDs."""
        self.assertEqual(
            set(self.result["count_devices_reject_rate_dict"].keys()),
            set(_trans_data["userid"].unique()),
        )

    def test_count_ip_keys_match_userids(self):
        """count_ips_reject_rate_dict keys are the unique user IDs."""
        self.assertEqual(
            set(self.result["count_ips_reject_rate_dict"].keys()),
            set(_trans_data["userid"].unique()),
        )

    def test_shared_rates_non_negative(self):
        """All entity sharing rejection rates are >= 0."""
        for key in (
            "shared_devices_reject_rate_dict",
            "shared_ips_reject_rate_dict",
            "shared_cards_reject_rate_dict",
        ):
            for rate in self.result[key].values():
                self.assertGreaterEqual(rate, 0.0, msg=f"Negative rate in {key}")

    def test_count_rates_non_negative(self):
        """All entity count rejection rates are >= 0."""
        for key in (
            "count_devices_reject_rate_dict",
            "count_ips_reject_rate_dict",
            "count_cards_reject_rate_dict",
        ):
            for rate in self.result[key].values():
                self.assertGreaterEqual(rate, 0.0, msg=f"Negative rate in {key}")


if __name__ == "__main__":
    unittest.main()
