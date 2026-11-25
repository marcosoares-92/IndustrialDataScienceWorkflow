import unittest
import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from idsw import ControlVars
from idsw.etl.cleansing import drop_columns_or_rows, remove_duplicated_rows
from idsw.etl.transform import log_transform, square_root_transform, feature_scaling
from idsw.etl.procdiagnosis import process_capability


class TestEtlCoreUtils(unittest.TestCase):

    def setUp(self):
        ControlVars.show_plots = False
        ControlVars.show_results = False
        np.random.seed(42)
        self.df = pd.DataFrame({
            'id': [1, 2, 2, 3, 4],
            'val': [10.0, 20.0, 20.0, 30.0, 40.0],
            'extra': ['a', 'b', 'b', 'c', 'd']
        })

    def test_cleansing_functions(self):
        df_dedup = remove_duplicated_rows(self.df)
        self.assertEqual(len(df_dedup), 4)

        df_dropped = drop_columns_or_rows(df_dedup, columns_to_drop=['extra'])
        self.assertNotIn('extra', df_dropped.columns)

    def test_transform_functions(self):
        df_log = log_transform(self.df, subset_of_features_to_transform=['val'])
        self.assertTrue(any('val' in col for col in df_log.columns))

        df_sqrt = square_root_transform(self.df, subset_of_features_to_transform=['val'])
        self.assertTrue(any('val' in col for col in df_sqrt.columns))

    def test_process_capability(self):
        df_cap = pd.DataFrame({'measure': np.random.normal(50, 2, 50)})
        cap_df, stats_dict = process_capability(
            df_cap,
            column_with_variable_to_be_analyzed='measure',
            specification_limits={'lower_spec_lim': 44.0, 'upper_spec_lim': 56.0},
            plotly=False
        )
        self.assertIsNotNone(cap_df)
        self.assertIn('mu', stats_dict)


if __name__ == '__main__':
    unittest.main()
