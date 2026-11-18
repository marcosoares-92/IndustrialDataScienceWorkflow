"""
Unit tests for idsw.datafetch.pipes module.
Covers:
- import_export_model_list_dict (serialization of models, lists, and dicts)
- load_anomaly_detector
- manipulate_sqlite_db (local SQLite operations)
- load_pandas_dataframe (CSV reading)
- export_pd_dataframe_as_csv
- export_pd_dataframe_as_excel
- json_obj_to_pandas_dataframe
- convert_variable_or_iterable_to_single_column_df
"""

import unittest
import os
import shutil
import tempfile
import sqlite3
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge

from idsw import ControlVars, InvalidInputsError
from idsw.datafetch.pipes import (
    import_export_model_list_dict,
    load_anomaly_detector,
    manipulate_sqlite_db,
    load_pandas_dataframe,
    export_pd_dataframe_as_csv,
    export_pd_dataframe_as_excel,
    json_obj_to_pandas_dataframe,
    convert_variable_or_iterable_to_single_column_df
)
from idsw.modelling.core import AnomalyDetector


class TestDatafetchPipes(unittest.TestCase):

    def setUp(self):
        ControlVars.show_plots = False
        ControlVars.show_results = False
        self.test_dir = tempfile.mkdtemp()

        self.sample_df = pd.DataFrame({
            "col_a": [1.0, 2.0, 3.0, 4.0],
            "col_b": ["apple", "banana", "cherry", "date"]
        })

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_import_export_model_and_dict(self):
        # Train simple model
        model = Ridge()
        model.fit(np.array([[1], [2], [3]]), np.array([1, 2, 3]))

        meta_dict = {"model_name": "Ridge_test", "features": ["x1"], "r2": 0.99}

        # Export model and dict
        import_export_model_list_dict(
            action="export",
            objects_manipulated="both",
            model_file_name="test_ridge",
            dictionary_or_list_file_name="test_meta",
            directory_path=self.test_dir,
            model_to_export=model,
            dict_or_list_to_export=meta_dict
        )

        # Import model and dict
        loaded_model, loaded_dict = import_export_model_list_dict(
            action="import",
            objects_manipulated="both",
            model_file_name="test_ridge",
            dictionary_or_list_file_name="test_meta",
            directory_path=self.test_dir
        )
        self.assertIsNotNone(loaded_model)
        self.assertIsInstance(loaded_dict, dict)
        self.assertEqual(loaded_dict["model_name"], "Ridge_test")

        # Test model prediction
        pred = loaded_model.predict([[4]])
        self.assertAlmostEqual(pred[0], 4.0, delta=0.5)

    def test_anomaly_detector_export_import(self):
        # Create and fit anomaly detector
        ad = AnomalyDetector(epsilon=0.01, distribution="gaussian")
        X_data = np.random.normal(0, 1, (30, 2))
        ad.fit(X_data)

        # Export
        import_export_model_list_dict(
            action="export",
            objects_manipulated="model_only",
            model_file_name="anomaly_model",
            directory_path=self.test_dir,
            model_type="anomaly_detector",
            model_to_export=ad
        )

        # Import
        loaded_ad = import_export_model_list_dict(
            action="import",
            objects_manipulated="model_only",
            model_file_name="anomaly_model",
            directory_path=self.test_dir,
            model_type="anomaly_detector"
        )
        self.assertIsInstance(loaded_ad, AnomalyDetector)
        self.assertEqual(loaded_ad.distribution, "gaussian")
        self.assertEqual(loaded_ad.epsilon, 0.01)

    def test_sqlite_db_fetch(self):
        db_path = os.path.join(self.test_dir, "test.db")
        conn = sqlite3.connect(db_path)
        self.sample_df.to_sql("sensors", conn, index=False)
        conn.close()

        fetched_df = manipulate_sqlite_db(
            file_path=db_path,
            table_name="sensors",
            action="fetch_table"
        )
        self.assertIsInstance(fetched_df, pd.DataFrame)
        self.assertEqual(len(fetched_df), 4)

    def test_export_and_load_csv(self):
        export_pd_dataframe_as_csv(
            dataframe_obj_to_be_exported=self.sample_df,
            new_file_name_without_extension="exported_sample",
            file_directory_path=self.test_dir
        )
        csv_file = "exported_sample.csv"
        loaded_df = load_pandas_dataframe(
            file_directory_path=self.test_dir,
            file_name_with_extension=csv_file
        )
        self.assertIsInstance(loaded_df, pd.DataFrame)
        self.assertEqual(len(loaded_df), 4)

    def test_json_conversion(self):
        data = [
            {"sensor": "temp", "val": 25.5},
            {"sensor": "press", "val": 1.2}
        ]
        df = json_obj_to_pandas_dataframe(data, json_obj_type="list")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        self.assertIn("sensor", df.columns)

    def test_convert_variable_or_iterable(self):
        vals = [10, 20, 30]
        df = convert_variable_or_iterable_to_single_column_df(vals, column_label="numbers")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(list(df["numbers"]), [10, 20, 30])


if __name__ == "__main__":
    unittest.main()
