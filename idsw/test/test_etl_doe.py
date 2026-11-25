import unittest
import os
import tempfile
import numpy as np
import pandas as pd
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from idsw import ControlVars, InvalidInputsError
from idsw.etl.doe import (
    create_factorial_design,
    analyze_factorial_experiment,
    plot_cube_plot,
    response_surface_analysis,
    box_cox_transformation_analysis
)


class TestEtlDoe(unittest.TestCase):

    def setUp(self):
        ControlVars.show_plots = False
        ControlVars.show_results = False

    def test_create_factorial_and_ccd_designs(self):
        factors = {'Temp': (100, 200), 'Pressure': (1.0, 5.0), 'Time': (10, 30)}
        # Full 2^3 + 3 centers = 11 runs
        df_2k, coded_2k = create_factorial_design(factors, design_type='full_2k', n_center_points=3, randomize=False)
        self.assertEqual(len(df_2k), 11)
        self.assertIn('Response', df_2k.columns)

        # CCD / Star design: 2^3 (8) + 2*3 (6) + 2 centers = 16 runs
        df_ccd, coded_ccd = create_factorial_design(factors, design_type='ccd', n_center_points=2, randomize=False)
        self.assertEqual(len(df_ccd), 16)

        # Box-Behnken: 12 edge points + 3 centers = 15 runs
        df_bbd, _ = create_factorial_design(factors, design_type='box_behnken', n_center_points=3, randomize=False)
        self.assertEqual(len(df_bbd), 15)

    def test_analyze_factorial_and_cube_and_rsm(self):
        factors = {'Temp': (100, 200), 'Pressure': (1, 5), 'Time': (10, 30)}
        df_exp, _ = create_factorial_design(factors, design_type='ccd', n_center_points=3, randomize=False)
        # Simulated quadratic yield response
        df_exp['Response'] = (
            50.0
            + 0.2 * (df_exp['Temp'] - 150)
            + 3.0 * (df_exp['Pressure'] - 3)
            - 0.01 * (df_exp['Temp'] - 150) ** 2
            + np.random.RandomState(42).normal(0, 0.5, len(df_exp))
        )

        ols_res, effects_df, anova_summ = analyze_factorial_experiment(
            df_exp, factor_cols=['Temp', 'Pressure', 'Time'], response_col='Response'
        )
        self.assertGreater(anova_summ['R_squared'], 0.8)
        self.assertIn('Term', effects_df.columns)

        # Cube plot on 2^3 subset
        df_2k, _ = create_factorial_design(factors, design_type='full_2k', n_center_points=0, randomize=False)
        df_2k['Response'] = 10.0 + 0.1 * df_2k['Temp'] + 2.0 * df_2k['Pressure']
        corners = plot_cube_plot(df_2k, factor_cols=['Temp', 'Pressure', 'Time'], response_col='Response')
        self.assertEqual(len(corners), 8)

        # RSM analysis
        rsm_model, rsm_summ = response_surface_analysis(
            df_exp, factor_cols=['Temp', 'Pressure', 'Time'], response_col='Response',
            x_factor='Temp', y_factor='Pressure'
        )
        self.assertIn('max_predicted_response', rsm_summ)

    def test_box_cox_transformation(self):
        np.random.seed(42)
        df = pd.DataFrame({'y_skewed': np.random.exponential(scale=5.0, size=100)})
        df_out, summ = box_cox_transformation_analysis(df, column_to_analyze='y_skewed')
        self.assertIn('y_skewed_boxcox', df_out.columns)
        self.assertIn('optimal_lambda', summ)
        self.assertIn('recommended_transformation', summ)


if __name__ == '__main__':
    unittest.main()
