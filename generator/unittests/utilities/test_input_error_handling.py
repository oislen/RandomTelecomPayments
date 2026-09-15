import os
import sys
import unittest

sys.path.append(os.path.join(os.getcwd(), "generator"))

from utilities import input_error_handling


class Test_input_error_handling(unittest.TestCase):
    """
    Unit tests for the input_error_handling utility function.

    Verifies that valid parameter dictionaries are accepted without error,
    and that each invalid parameter value raises a ValueError with an
    informative message.
    """

    # ------------------------------------------------------------------
    # Valid inputs – should not raise
    # ------------------------------------------------------------------

    def test_valid_params_no_exception(self):
        """A fully valid parameter dictionary raises no exception."""
        valid = {
            "n_users": 100,
            "use_random_seed": 1,
            "n_itr": 2,
            "n_applications": 5000,
        }
        try:
            input_error_handling(valid)
        except Exception as exc:
            self.fail(f"input_error_handling raised unexpectedly: {exc}")

    def test_valid_minimum_values(self):
        """Boundary minimum values (all 1s) are accepted."""
        minimum = {
            "n_users": 1,
            "use_random_seed": 0,
            "n_itr": 1,
            "n_applications": 1,
        }
        try:
            input_error_handling(minimum)
        except Exception as exc:
            self.fail(f"input_error_handling raised unexpectedly: {exc}")

    # ------------------------------------------------------------------
    # Invalid n_users
    # ------------------------------------------------------------------

    def test_n_users_zero_raises(self):
        """n_users = 0 must raise ValueError."""
        with self.assertRaises(ValueError):
            input_error_handling(
                {"n_users": 0, "use_random_seed": 0, "n_itr": 1, "n_applications": 1}
            )

    def test_n_users_negative_raises(self):
        """Negative n_users must raise ValueError."""
        with self.assertRaises(ValueError):
            input_error_handling(
                {"n_users": -5, "use_random_seed": 0, "n_itr": 1, "n_applications": 1}
            )

    def test_n_users_float_raises(self):
        """Float n_users must raise (beartype or ValueError)."""
        with self.assertRaises(Exception):
            input_error_handling(
                {"n_users": 1.5, "use_random_seed": 0, "n_itr": 1, "n_applications": 1}
            )

    # ------------------------------------------------------------------
    # Invalid use_random_seed
    # ------------------------------------------------------------------

    def test_use_random_seed_invalid_value_raises(self):
        """use_random_seed = 2 must raise ValueError."""
        with self.assertRaises(ValueError):
            input_error_handling(
                {"n_users": 10, "use_random_seed": 2, "n_itr": 1, "n_applications": 1}
            )

    def test_use_random_seed_negative_raises(self):
        """use_random_seed = -1 must raise ValueError."""
        with self.assertRaises(ValueError):
            input_error_handling(
                {"n_users": 10, "use_random_seed": -1, "n_itr": 1, "n_applications": 1}
            )

    # ------------------------------------------------------------------
    # Invalid n_itr
    # ------------------------------------------------------------------

    def test_n_itr_zero_raises(self):
        """n_itr = 0 must raise ValueError."""
        with self.assertRaises(ValueError):
            input_error_handling(
                {"n_users": 10, "use_random_seed": 0, "n_itr": 0, "n_applications": 1}
            )

    def test_n_itr_negative_raises(self):
        """Negative n_itr must raise ValueError."""
        with self.assertRaises(ValueError):
            input_error_handling(
                {"n_users": 10, "use_random_seed": 0, "n_itr": -1, "n_applications": 1}
            )

    # ------------------------------------------------------------------
    # Invalid n_applications
    # ------------------------------------------------------------------

    def test_n_applications_zero_raises(self):
        """n_applications = 0 must raise ValueError."""
        with self.assertRaises(ValueError):
            input_error_handling(
                {"n_users": 10, "use_random_seed": 0, "n_itr": 1, "n_applications": 0}
            )

    def test_n_applications_negative_raises(self):
        """Negative n_applications must raise ValueError."""
        with self.assertRaises(ValueError):
            input_error_handling(
                {
                    "n_users": 10,
                    "use_random_seed": 0,
                    "n_itr": 1,
                    "n_applications": -100,
                }
            )

    # ------------------------------------------------------------------
    # Error message content
    # ------------------------------------------------------------------

    def test_error_message_contains_param_name_n_users(self):
        """ValueError for n_users mentions the parameter name."""
        with self.assertRaises(ValueError) as ctx:
            input_error_handling(
                {"n_users": 0, "use_random_seed": 0, "n_itr": 1, "n_applications": 1}
            )
        self.assertIn("n_users", str(ctx.exception))

    def test_error_message_contains_param_name_use_random_seed(self):
        """ValueError for use_random_seed mentions the parameter name."""
        with self.assertRaises(ValueError) as ctx:
            input_error_handling(
                {"n_users": 1, "use_random_seed": 5, "n_itr": 1, "n_applications": 1}
            )
        self.assertIn("use_random_seed", str(ctx.exception))

    def test_error_message_contains_param_name_n_itr(self):
        """ValueError for n_itr mentions the parameter name."""
        with self.assertRaises(ValueError) as ctx:
            input_error_handling(
                {"n_users": 1, "use_random_seed": 0, "n_itr": 0, "n_applications": 1}
            )
        self.assertIn("n_itr", str(ctx.exception))

    def test_error_message_contains_param_name_n_applications(self):
        """ValueError for n_applications mentions the parameter name."""
        with self.assertRaises(ValueError) as ctx:
            input_error_handling(
                {"n_users": 1, "use_random_seed": 0, "n_itr": 1, "n_applications": 0}
            )
        self.assertIn("n_applications", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
