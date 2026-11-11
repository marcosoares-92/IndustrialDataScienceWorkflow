"""
Unit tests for idsw.etl.meandifference module.
Covers:
- anova_box_violin_plot (parametric ANOVA and non-parametric Kruskal-Wallis)
- AB_testing (parametric t-test/z-test and non-parametric Mann-Whitney U / Fisher's exact)
- test_proportion_diffs (parametric z-test/chi-square and non-parametric Fisher/permutation)
- monte_carlo_simulation
- generate_sampling_distribution
- bayesian_inference_analysis
- generate_and_fit_distribution
"""

import unittest
import numpy as np
import pandas as pd

from idsw import ControlVars, InvalidInputsError
from idsw.etl.meandifference import (
    anova_box_violin_plot,
    AB_testing,
    test_proportion_diffs,
    monte_carlo_simulation,
    generate_sampling_distribution,
    bayesian_inference_analysis,
    generate_and_fit_distribution
)


class TestETLMeanDifference(unittest.TestCase):

    def setUp(self):
        ControlVars.show_plots = False
        ControlVars.show_results = False
        np.random.seed(42)

    def test_anova_parametric_and_non_parametric(self):
        # Generate 3 groups with different means
        g1 = np.random.normal(10, 1, 30)
        g2 = np.random.normal(12, 1, 30)
        g3 = np.random.normal(15, 1, 30)
        df = pd.DataFrame({
            'val': np.concatenate([g1, g2, g3]),
            'group': ['G1'] * 30 + ['G2'] * 30 + ['G3'] * 30
        })

        # Parametric One-Way ANOVA
        summary_param, _ = anova_box_violin_plot(
            plot_type=None,
            data_in_same_column=True,
            df=df,
            column_with_labels_or_groups='group',
            variable_to_analyze='val',
            non_parametric=False
        )
        self.assertIn('F_statistic', summary_param)
        self.assertIn('p_value', summary_param)
        self.assertEqual(summary_param.get('test_used'), 'One-Way ANOVA (F-test)')
        self.assertFalse(summary_param.get('non_parametric'))

        # Non-parametric Kruskal-Wallis
        summary_nonparam, _ = anova_box_violin_plot(
            plot_type=None,
            data_in_same_column=True,
            df=df,
            column_with_labels_or_groups='group',
            variable_to_analyze='val',
            non_parametric=True
        )
        self.assertIn('H_statistic', summary_nonparam)
        self.assertIn('p_value', summary_nonparam)
        self.assertEqual(summary_nonparam.get('test_used'), 'Kruskal-Wallis H-test')
        self.assertTrue(summary_nonparam.get('non_parametric'))

    def test_ab_testing_means_parametric_and_non_parametric(self):
        y1 = np.random.normal(20, 2, 40)
        y2 = np.random.normal(25, 2, 40)
        series_input = [{'values_to_analyze': y1, 'label': 'A'}, {'values_to_analyze': y2, 'label': 'B'}]

        # Parametric t-test
        res_t = AB_testing(
            what_to_compare='mean',
            list_of_dictionaries_with_series_to_analyze=series_input,
            non_parametric=False
        )
        self.assertIn('t_statistic', res_t)
        self.assertIn('p_value', res_t)
        self.assertEqual(res_t.get('test_used'), 'Two-Sample Independent t-Test')
        self.assertTrue(res_t['reject_H0'])

        # Non-parametric Mann-Whitney U test
        res_u = AB_testing(
            what_to_compare='mean',
            list_of_dictionaries_with_series_to_analyze=series_input,
            non_parametric=True
        )
        self.assertIn('u_statistic', res_u)
        self.assertIn('p_value', res_u)
        self.assertEqual(res_u.get('test_used'), 'Mann-Whitney U Test')
        self.assertTrue(res_u['reject_H0'])

    def test_ab_testing_proportions_parametric_and_non_parametric(self):
        # 100 trials each, A has 15% conversion, B has 40% conversion
        y1 = np.random.choice([0, 1], size=100, p=[0.85, 0.15])
        y2 = np.random.choice([0, 1], size=100, p=[0.60, 0.40])
        series_input = [{'values_to_analyze': y1, 'label': 'Control'}, {'values_to_analyze': y2, 'label': 'Variant'}]

        # Parametric z-test
        res_z = AB_testing(
            what_to_compare='proportion',
            list_of_dictionaries_with_series_to_analyze=series_input,
            non_parametric=False
        )
        self.assertIn('z_statistic', res_z)
        self.assertIn('p_value', res_z)

        # Non-parametric Fisher's exact test
        res_fisher = AB_testing(
            what_to_compare='proportion',
            list_of_dictionaries_with_series_to_analyze=series_input,
            non_parametric=True
        )
        self.assertIn('odds_ratio', res_fisher)
        self.assertIn('p_value', res_fisher)
        self.assertEqual(res_fisher.get('test_used'), "Fisher's Exact Test")

    def test_test_proportion_diffs_two_and_multiple_groups(self):
        # Test 2 groups
        df_2 = pd.DataFrame({
            'group': ['A'] * 80 + ['B'] * 80,
            'converted': np.concatenate([
                np.random.choice([0, 1], size=80, p=[0.8, 0.2]),
                np.random.choice([0, 1], size=80, p=[0.5, 0.5])
            ])
        })
        summary_2, df_res_2 = test_proportion_diffs(
            df=df_2,
            column_with_labels_or_groups='group',
            variable_to_analyze='converted',
            non_parametric=False,
            show_plot=False
        )
        self.assertIn('z_statistic', summary_2)
        self.assertEqual(len(df_res_2), 2)

        # Test multiple groups (>2)
        df_3 = pd.DataFrame({
            'group': ['A'] * 50 + ['B'] * 50 + ['C'] * 50,
            'converted': np.concatenate([
                np.random.choice([0, 1], size=50, p=[0.8, 0.2]),
                np.random.choice([0, 1], size=50, p=[0.7, 0.3]),
                np.random.choice([0, 1], size=50, p=[0.5, 0.5])
            ])
        })
        summary_3, df_res_3 = test_proportion_diffs(
            df=df_3,
            column_with_labels_or_groups='group',
            variable_to_analyze='converted',
            non_parametric=True,
            show_plot=False
        )
        self.assertIn('chi2_statistic', summary_3)
        self.assertEqual(len(df_res_3), 3)

    def test_monte_carlo_simulation(self):
        # Equation: Profit = Revenue - Fixed_Cost - Variable_Cost
        distributions = {
            'revenue': ('normal', 100000, 10000),
            'fixed_cost': ('uniform', 20000, 30000),
            'variable_cost': ('uniform', 30000, 45000)
        }
        sim_df, summary = monte_carlo_simulation(
            simulation_function_or_equation="revenue - fixed_cost - variable_cost",
            input_distributions=distributions,
            n_iterations=2000,
            confidence_level_pct=95,
            show_plot=False
        )
        self.assertIsInstance(sim_df, pd.DataFrame)
        self.assertIn('simulation_output', sim_df.columns)
        self.assertEqual(len(sim_df), 2000)
        self.assertIn('mean', summary)
        self.assertIn('VaR_95', summary)
        self.assertIn('CVaR_95', summary)
        self.assertIn('confidence_interval', summary)

    def test_generate_sampling_distribution(self):
        # Testing CLT and bootstrap sampling
        pop_data = np.random.exponential(scale=5.0, size=500)
        df = pd.DataFrame({'sensor_readings': pop_data})

        sampling_dist, summary = generate_sampling_distribution(
            df,
            column_to_analyze='sensor_readings',
            statistic='mean',
            sample_size=50,
            n_replications=500,
            sampling_method='bootstrap',
            show_plot=False
        )
        self.assertIsInstance(sampling_dist, pd.Series)
        self.assertEqual(len(sampling_dist), 500)
        self.assertIn('standard_error_empirical', summary)
        self.assertIn('standard_error_analytical', summary)
        self.assertIn('confidence_interval', summary)

    def test_bayesian_inference_analysis(self):
        # 1. Beta-Binomial
        summary_bb, plot_bb = bayesian_inference_analysis(
            model_type='beta_binomial',
            prior_alpha=2.0,
            prior_beta=2.0,
            successes=25,
            trials=100,
            show_plot=False
        )
        self.assertIn('posterior_mean', summary_bb)
        self.assertIn('credible_interval', summary_bb)
        self.assertAlmostEqual(summary_bb['posterior_mean'], (2.0 + 25) / (2.0 + 2.0 + 100), delta=0.01)

        # 2. Normal-Normal
        sample = np.random.normal(loc=12.0, scale=2.0, size=40)
        summary_nn, plot_nn = bayesian_inference_analysis(
            model_type='normal_normal',
            prior_mean=10.0,
            prior_variance=4.0,
            data=sample,
            show_plot=False
        )
        self.assertIn('posterior_mean', summary_nn)
        self.assertIn('credible_interval', summary_nn)

    def test_generate_and_fit_distribution(self):
        gen_df, fit_summary = generate_and_fit_distribution(
            distribution_name='normal',
            distribution_params={'loc': 50.0, 'scale': 5.0},
            sample_size=500,
            fit_distribution=True,
            show_plot=False
        )
        self.assertIsInstance(gen_df, pd.DataFrame)
        self.assertIn('generated_values', gen_df.columns)
        self.assertEqual(len(gen_df), 500)
        self.assertIn('fitted_parameters', fit_summary)
        self.assertAlmostEqual(fit_summary['sample_mean'], 50.0, delta=1.5)


if __name__ == '__main__':
    unittest.main()
