import unittest
import os
import sys
from unittest.mock import patch

sys.path.append(os.path.join(os.getcwd(), "generator"))

from utilities.commandline_interface import commandline_interface


class Test_commandline_interface(unittest.TestCase):
    """
    Unit tests for the commandline_interface utility function.

    Tests that the argparse-based CLI correctly parses all expected parameters
    and returns a dictionary with the right types and values when called with
    a known set of command-line arguments.
    """

    def _call_with_args(self, args):
        """Helper that patches sys.argv and calls commandline_interface."""
        with patch("sys.argv", ["prog"] + args):
            return commandline_interface()

    # ------------------------------------------------------------------
    # Default values (no arguments supplied)
    # ------------------------------------------------------------------

    def test_defaults_types(self):
        """Return types match expected Python primitives for all defaults."""
        result = self._call_with_args([])
        self.assertIsInstance(result["n_users"], int)
        self.assertIsInstance(result["use_random_seed"], int)
        self.assertIsInstance(result["n_itr"], int)
        self.assertIsInstance(result["n_applications"], int)
        self.assertIsInstance(result["registration_start_date"], str)
        self.assertIsInstance(result["registration_end_date"], str)
        self.assertIsInstance(result["transaction_start_date"], str)
        self.assertIsInstance(result["transaction_end_date"], str)

    def test_defaults_values(self):
        """Default values match the expected programme defaults."""
        result = self._call_with_args([])
        self.assertEqual(result["n_users"], 100)
        self.assertEqual(result["use_random_seed"], 0)
        self.assertEqual(result["n_itr"], 1)
        self.assertEqual(result["n_applications"], 20000)

    # ------------------------------------------------------------------
    # Explicit argument overrides
    # ------------------------------------------------------------------

    def test_n_users_override(self):
        """--n_users flag correctly overrides the default."""
        result = self._call_with_args(["--n_users", "50"])
        self.assertEqual(result["n_users"], 50)

    def test_use_random_seed_override(self):
        """--use_random_seed flag correctly overrides the default."""
        result = self._call_with_args(["--use_random_seed", "1"])
        self.assertEqual(result["use_random_seed"], 1)

    def test_n_itr_override(self):
        """--n_itr flag correctly overrides the default."""
        result = self._call_with_args(["--n_itr", "3"])
        self.assertEqual(result["n_itr"], 3)

    def test_n_applications_override(self):
        """--n_applications flag correctly overrides the default."""
        result = self._call_with_args(["--n_applications", "5000"])
        self.assertEqual(result["n_applications"], 5000)

    def test_date_overrides(self):
        """Date string flags are stored verbatim in the returned dict."""
        result = self._call_with_args([
            "--registration_start_date", "2021-01-01",
            "--registration_end_date", "2021-12-31",
            "--transaction_start_date", "2022-01-01",
            "--transaction_end_date", "2022-12-31",
        ])
        self.assertEqual(result["registration_start_date"], "2021-01-01")
        self.assertEqual(result["registration_end_date"], "2021-12-31")
        self.assertEqual(result["transaction_start_date"], "2022-01-01")
        self.assertEqual(result["transaction_end_date"], "2022-12-31")

    # ------------------------------------------------------------------
    # Return type
    # ------------------------------------------------------------------

    def test_return_type(self):
        """commandline_interface always returns a dict."""
        result = self._call_with_args([])
        self.assertIsInstance(result, dict)

    def test_return_keys(self):
        """Returned dict contains all expected parameter keys."""
        result = self._call_with_args([])
        expected_keys = {
            "n_users",
            "use_random_seed",
            "n_itr",
            "n_applications",
            "registration_start_date",
            "registration_end_date",
            "transaction_start_date",
            "transaction_end_date",
        }
        self.assertTrue(expected_keys.issubset(set(result.keys())))


if __name__ == "__main__":
    unittest.main()
