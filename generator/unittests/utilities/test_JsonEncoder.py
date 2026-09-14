import json
import unittest
import os
import sys

import numpy as np
import pandas as pd

sys.path.append(os.path.join(os.getcwd(), "generator"))

from utilities.JsonEncoder import JsonEncoder


class Test_JsonEncoder(unittest.TestCase):
    """
    Unit tests for the JsonEncoder custom JSON encoder.

    Verifies that numpy and pandas types that are not natively
    JSON-serialisable are correctly converted to their Python
    primitive equivalents.
    """

    def _encode(self, value):
        """Serialise a single value through json.dumps with JsonEncoder."""
        return json.loads(json.dumps(value, cls=JsonEncoder))

    # ------------------------------------------------------------------
    # numpy.datetime64
    # ------------------------------------------------------------------

    def test_numpy_datetime64_encodes_to_string(self):
        """np.datetime64 is serialised as a non-empty string."""
        result = self._encode(np.datetime64("2021-06-15"))
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_numpy_datetime64_value(self):
        """np.datetime64 string representation contains the date."""
        result = self._encode(np.datetime64("2021-06-15"))
        self.assertIn("2021", result)

    # ------------------------------------------------------------------
    # pandas.Timestamp
    # ------------------------------------------------------------------

    def test_pandas_timestamp_encodes_to_string(self):
        """pd.Timestamp is serialised as a non-empty string."""
        result = self._encode(pd.Timestamp("2022-03-01"))
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_pandas_timestamp_value(self):
        """pd.Timestamp string representation contains the year."""
        result = self._encode(pd.Timestamp("2022-03-01"))
        self.assertIn("2022", result)

    # ------------------------------------------------------------------
    # numpy.integer
    # ------------------------------------------------------------------

    def test_numpy_int64_encodes_to_int(self):
        """np.int64 is serialised as a Python int."""
        result = self._encode(np.int64(42))
        self.assertIsInstance(result, int)
        self.assertEqual(result, 42)

    def test_numpy_int32_encodes_to_int(self):
        """np.int32 is serialised as a Python int."""
        result = self._encode(np.int32(7))
        self.assertIsInstance(result, int)
        self.assertEqual(result, 7)

    # ------------------------------------------------------------------
    # numpy.floating
    # ------------------------------------------------------------------

    def test_numpy_float64_encodes_to_float(self):
        """np.float64 is serialised as a Python float."""
        result = self._encode(np.float64(3.14))
        self.assertIsInstance(result, float)
        self.assertAlmostEqual(result, 3.14, places=5)

    def test_numpy_float32_encodes_to_float(self):
        """np.float32 is serialised as a Python float."""
        result = self._encode(np.float32(1.5))
        self.assertIsInstance(result, float)
        self.assertAlmostEqual(result, 1.5, places=3)

    # ------------------------------------------------------------------
    # Native Python types still work
    # ------------------------------------------------------------------

    def test_native_int_unchanged(self):
        """Standard Python int passes through unchanged."""
        result = self._encode(99)
        self.assertEqual(result, 99)

    def test_native_float_unchanged(self):
        """Standard Python float passes through unchanged."""
        result = self._encode(2.71)
        self.assertAlmostEqual(result, 2.71, places=5)

    def test_native_string_unchanged(self):
        """Standard Python str passes through unchanged."""
        result = self._encode("hello")
        self.assertEqual(result, "hello")

    def test_none_unchanged(self):
        """None is serialised as JSON null (Python None after decode)."""
        result = self._encode(None)
        self.assertIsNone(result)

    # ------------------------------------------------------------------
    # Inside a dict (simulating the API response path)
    # ------------------------------------------------------------------

    def test_dict_with_mixed_types(self):
        """Dicts containing numpy types round-trip correctly."""
        payload = {
            "amount": np.float64(9.99),
            "count": np.int64(3),
            "date": pd.Timestamp("2023-01-01"),
        }
        serialised = json.dumps(payload, cls=JsonEncoder)
        result = json.loads(serialised)
        self.assertIsInstance(result["amount"], float)
        self.assertIsInstance(result["count"], int)
        self.assertIsInstance(result["date"], str)

    # ------------------------------------------------------------------
    # Unsupported type raises TypeError
    # ------------------------------------------------------------------

    def test_unsupported_type_raises(self):
        """Objects not handled by JsonEncoder raise TypeError."""
        class _Unsupported:
            pass

        with self.assertRaises(TypeError):
            json.dumps(_Unsupported(), cls=JsonEncoder)


if __name__ == "__main__":
    unittest.main()
