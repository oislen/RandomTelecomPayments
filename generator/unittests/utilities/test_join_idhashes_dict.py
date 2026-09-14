import unittest
import os
import sys

import numpy as np
import pandas as pd

sys.path.append(os.path.join(os.getcwd(), "generator"))

from utilities.join_idhashes_dict import join_idhashes_dict


class Test_join_idhashes_dict(unittest.TestCase):
    """
    Unit tests for the join_idhashes_dict utility function.

    Verifies that the function correctly left-joins an entity attribute
    dictionary onto a DataFrame using a specified key column, producing
    a new value column with the mapped attribute values.
    """

    def setUp(self):
        """Create reusable fixtures shared across tests."""
        self.base_df = pd.DataFrame({
            "device_hash": ["aaa", "bbb", "ccc", "ddd"],
            "userid": [1, 2, 3, 4],
        })
        self.device_type_dict = {
            "aaa": "Samsung Galaxy S21",
            "bbb": "Pixel 6",
            "ccc": "OnePlus 9",
            "ddd": "Xiaomi Mi 11",
        }

    # ------------------------------------------------------------------
    # Return type
    # ------------------------------------------------------------------

    def test_return_type(self):
        """Result is a pandas DataFrame."""
        result = join_idhashes_dict(
            data=self.base_df,
            idhashes_dict=self.device_type_dict,
            idhash_key_name="device_hash",
            idhash_val_name="device_type",
        )
        self.assertIsInstance(result, pd.DataFrame)

    # ------------------------------------------------------------------
    # Shape
    # ------------------------------------------------------------------

    def test_row_count_preserved(self):
        """Number of rows is unchanged after a full left-join."""
        result = join_idhashes_dict(
            data=self.base_df,
            idhashes_dict=self.device_type_dict,
            idhash_key_name="device_hash",
            idhash_val_name="device_type",
        )
        self.assertEqual(len(result), len(self.base_df))

    def test_new_column_added(self):
        """The value column specified by idhash_val_name is present in result."""
        result = join_idhashes_dict(
            data=self.base_df,
            idhashes_dict=self.device_type_dict,
            idhash_key_name="device_hash",
            idhash_val_name="device_type",
        )
        self.assertIn("device_type", result.columns)

    # ------------------------------------------------------------------
    # Values
    # ------------------------------------------------------------------

    def test_values_mapped_correctly(self):
        """Each row's new value column matches the dict lookup."""
        result = join_idhashes_dict(
            data=self.base_df,
            idhashes_dict=self.device_type_dict,
            idhash_key_name="device_hash",
            idhash_val_name="device_type",
        )
        for _, row in result.iterrows():
            self.assertEqual(row["device_type"], self.device_type_dict[row["device_hash"]])

    def test_no_nulls_when_all_keys_present(self):
        """No NaN values in the new column when every key is in the dict."""
        result = join_idhashes_dict(
            data=self.base_df,
            idhashes_dict=self.device_type_dict,
            idhash_key_name="device_hash",
            idhash_val_name="device_type",
        )
        self.assertFalse(result["device_type"].isnull().any())

    def test_null_for_missing_key(self):
        """Rows whose key is absent from the dict produce NaN in the value column."""
        partial_dict = {"aaa": "Samsung Galaxy S21"}  # only one entry
        result = join_idhashes_dict(
            data=self.base_df,
            idhashes_dict=partial_dict,
            idhash_key_name="device_hash",
            idhash_val_name="device_type",
        )
        missing_mask = result["device_hash"] != "aaa"
        self.assertTrue(result.loc[missing_mask, "device_type"].isnull().all())

    # ------------------------------------------------------------------
    # Existing columns are unchanged
    # ------------------------------------------------------------------

    def test_original_columns_unchanged(self):
        """Columns that existed before the join retain their original values."""
        result = join_idhashes_dict(
            data=self.base_df,
            idhashes_dict=self.device_type_dict,
            idhash_key_name="device_hash",
            idhash_val_name="device_type",
        )
        pd.testing.assert_series_equal(result["device_hash"], self.base_df["device_hash"])
        pd.testing.assert_series_equal(result["userid"], self.base_df["userid"])

    # ------------------------------------------------------------------
    # Integer key variant
    # ------------------------------------------------------------------

    def test_integer_key_join(self):
        """join_idhashes_dict works when the key column contains integers."""
        df = pd.DataFrame({"country_code_alpha": [276, 826, 642]})
        code_map = {276: "DE", 826: "GB", 642: "RO"}
        result = join_idhashes_dict(
            data=df,
            idhashes_dict=code_map,
            idhash_key_name="country_code_alpha",
            idhash_val_name="country_code",
        )
        self.assertEqual(list(result["country_code"]), ["DE", "GB", "RO"])


if __name__ == "__main__":
    unittest.main()
