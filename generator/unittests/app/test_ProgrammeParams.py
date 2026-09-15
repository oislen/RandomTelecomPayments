import os
import sys
import unittest

sys.path.append(os.path.join(os.getcwd(), "generator"))

import cons
from app.ProgrammeParams import ProgrammeParams


class Test_ProgrammeParams(unittest.TestCase):
    """
    Unit tests for the ProgrammeParams application-parameter class.

    Verifies that all attributes are stored with the correct types and
    values, and that the derived transaction_timescale is computed
    correctly from the supplied date range.
    """

    # ------------------------------------------------------------------
    # Fixtures
    # ------------------------------------------------------------------

    def _make_params(self, **kwargs):
        """Convenience factory with sensible defaults."""
        defaults = {
            "n_users": cons.unittest_n_users,
            "random_seed": cons.unittest_seed,
            "n_applications": cons.default_n_applications,
            "registration_start_date": cons.unittest_registration_start_date,
            "registration_end_date": cons.unittest_registration_end_date,
            "transaction_start_date": cons.unittest_transaction_start_date,
            "transaction_end_date": cons.unittest_transaction_end_date,
        }
        defaults.update(kwargs)
        return ProgrammeParams(**defaults)

    # ------------------------------------------------------------------
    # Attribute types
    # ------------------------------------------------------------------

    def test_n_users_type(self):
        """n_users is stored as int."""
        p = self._make_params()
        self.assertIsInstance(p.n_users, int)

    def test_random_seed_type(self):
        """random_seed is stored as int when supplied."""
        p = self._make_params()
        self.assertIsInstance(p.random_seed, int)

    def test_n_applications_type(self):
        """n_applications is stored as int."""
        p = self._make_params()
        self.assertIsInstance(p.n_applications, int)

    def test_registration_start_date_type(self):
        """registration_start_date is stored as str."""
        p = self._make_params()
        self.assertIsInstance(p.registration_start_date, str)

    def test_registration_end_date_type(self):
        """registration_end_date is stored as str."""
        p = self._make_params()
        self.assertIsInstance(p.registration_end_date, str)

    def test_transaction_start_date_type(self):
        """transaction_start_date is stored as str."""
        p = self._make_params()
        self.assertIsInstance(p.transaction_start_date, str)

    def test_transaction_end_date_type(self):
        """transaction_end_date is stored as str."""
        p = self._make_params()
        self.assertIsInstance(p.transaction_end_date, str)

    def test_transaction_timescale_type(self):
        """transaction_timescale is computed as a float."""
        p = self._make_params()
        self.assertIsInstance(p.transaction_timescale, float)

    # ------------------------------------------------------------------
    # Attribute values
    # ------------------------------------------------------------------

    def test_n_users_value(self):
        """n_users matches the supplied value."""
        p = self._make_params(n_users=50)
        self.assertEqual(p.n_users, 50)

    def test_random_seed_value(self):
        """random_seed matches the supplied value."""
        p = self._make_params(random_seed=99)
        self.assertEqual(p.random_seed, 99)

    def test_n_applications_value(self):
        """n_applications matches the supplied value."""
        p = self._make_params(n_applications=5000)
        self.assertEqual(p.n_applications, 5000)

    def test_date_strings_stored_verbatim(self):
        """All four date strings are stored exactly as supplied."""
        p = self._make_params()
        self.assertEqual(
            p.registration_start_date, cons.unittest_registration_start_date
        )
        self.assertEqual(p.registration_end_date, cons.unittest_registration_end_date)
        self.assertEqual(p.transaction_start_date, cons.unittest_transaction_start_date)
        self.assertEqual(p.transaction_end_date, cons.unittest_transaction_end_date)

    # ------------------------------------------------------------------
    # transaction_timescale computation
    # ------------------------------------------------------------------

    def test_transaction_timescale_one_year(self):
        """Exactly 365 days (non-leap) ≈ 1.0 years."""
        p = self._make_params(
            transaction_start_date="2021-01-01",
            transaction_end_date="2022-01-01",
        )
        # 365 days span → (365 + 1) / 365 ≈ 1.0027
        self.assertAlmostEqual(p.transaction_timescale, 366 / 365, places=5)

    def test_transaction_timescale_half_year(self):
        """182-day span produces a timescale close to 0.5."""
        p = self._make_params(
            transaction_start_date="2021-01-01",
            transaction_end_date="2021-07-02",  # 182 days
        )
        expected = (182 + 1) / 365
        self.assertAlmostEqual(p.transaction_timescale, expected, places=5)

    def test_transaction_timescale_positive(self):
        """transaction_timescale is always positive."""
        p = self._make_params()
        self.assertGreater(p.transaction_timescale, 0.0)

    # ------------------------------------------------------------------
    # None random_seed is accepted
    # ------------------------------------------------------------------

    def test_random_seed_none_accepted(self):
        """random_seed defaults to None when not supplied."""
        p = ProgrammeParams(
            n_users=10,
            registration_start_date=cons.unittest_registration_start_date,
            registration_end_date=cons.unittest_registration_end_date,
            transaction_start_date=cons.unittest_transaction_start_date,
            transaction_end_date=cons.unittest_transaction_end_date,
        )
        self.assertIsNone(p.random_seed)

    # ------------------------------------------------------------------
    # Defaults
    # ------------------------------------------------------------------

    def test_default_n_users(self):
        """Default n_users is 100."""
        p = ProgrammeParams(
            registration_start_date=cons.unittest_registration_start_date,
            registration_end_date=cons.unittest_registration_end_date,
            transaction_start_date=cons.unittest_transaction_start_date,
            transaction_end_date=cons.unittest_transaction_end_date,
        )
        self.assertEqual(p.n_users, 100)

    def test_default_n_applications(self):
        """Default n_applications is 20000."""
        p = ProgrammeParams(
            registration_start_date=cons.unittest_registration_start_date,
            registration_end_date=cons.unittest_registration_end_date,
            transaction_start_date=cons.unittest_transaction_start_date,
            transaction_end_date=cons.unittest_transaction_end_date,
        )
        self.assertEqual(p.n_applications, 20000)


if __name__ == "__main__":
    unittest.main()
