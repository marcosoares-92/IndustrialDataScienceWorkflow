"""
Unit tests for idsw.etl.characterize module.
Covers:
- test_data_normality
- test_stat_distribution (continuous: normal, lognormal, exponential; discrete: poisson, negative_binomial)
- partition_and_rank_df
- discrete_fourier_transform
- adv_imputation_missing_values
"""

import unittest
import numpy as np
import pandas as pd

from idsw import ControlVars, InvalidInputsError
from idsw.etl.characterize import (
    test_data_normality,
    test_stat_distribution,
    partition_and_rank_df,
    discrete_fourier_transform,
    adv_imputation_missing_values
)


class TestETLCharacterize(unittest.TestCase):

    def setUp(self):
        # Disable plots and printing during automated unit test runs
        ControlVars.show_plots = False
        ControlVars.show_results = False
        np.random.seed(42)

    def test_test_data_normality_single_column(self):
        # Generate 100 samples from normal distribution
        data = np.random.normal(loc=10.0, scale=2.0, size=100)
        df = pd.DataFrame({'sensor_val': data})

        results = test_data_normality(df, column_to_analyze='sensor_val', show_probability_plot=False)
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)

        res = results[0]
        self.assertIn('normality_dict', res)
        self.assertIn('general_statistics', res)
        stats = res['general_statistics']
        self.assertAlmostEqual(stats['series_mean'], 10.0, delta=1.0)
        self.assertIn('series_skewness', stats)
        self.assertIn('series_kurtosis', stats)

    def test_test_data_normality_with_subgroups(self):
        # Verify fix: subgroups must not be truncated, and sub_df prevents KeyError
        data_a = np.random.normal(loc=5.0, scale=1.0, size=50)
        data_b = np.random.normal(loc=15.0, scale=1.5, size=50)
        df = pd.DataFrame({
            'val': np.concatenate([data_a, data_b]),
            'group': ['A'] * 50 + ['B'] * 50
        })

        results = test_data_normality(
            df,
            column_to_analyze='val',
            column_with_labels_to_test_subgroups='group',
            show_probability_plot=False
        )
        self.assertIsInstance(results, list)
        # Both subgroups A and B must be present (not truncated to only last subgroup)
        self.assertEqual(len(results), 2)
        group_ids = [r['series_id'] for r in results]
        self.assertIn('val_A', group_ids)
        self.assertIn('val_B', group_ids)

    def test_test_stat_distribution_continuous(self):
        # Test lognormal distribution
        data = np.random.lognormal(mean=1.5, sigma=0.4, size=120)
        df = pd.DataFrame({'log_val': data})

        results = test_stat_distribution(
            df,
            column_to_analyze='log_val',
            statistical_distribution_to_test='lognormal',
            show_probability_plot=False
        )
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)
        stats = results[0]['general_statistics']
        self.assertIn('distribution_parameters', stats)
        self.assertIn('KolmogorovSmirnov_statistic', stats)
        self.assertIn('goodness_of_fit_p_value', stats)
        self.assertEqual(stats['distribution_tested'], 'lognormal')
        self.assertFalse(stats['is_discrete'])

    def test_test_stat_distribution_discrete_poisson(self):
        # Test Poisson distribution option
        data = np.random.poisson(lam=4.5, size=150)
        df = pd.DataFrame({'counts': data})

        results = test_stat_distribution(
            df,
            column_to_analyze='counts',
            statistical_distribution_to_test='poisson',
            show_probability_plot=False
        )
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)
        stats = results[0]['general_statistics']
        self.assertTrue(stats['is_discrete'])
        self.assertIn('distribution_parameters', stats)
        self.assertAlmostEqual(stats['distribution_parameters'][0], 4.5, delta=0.5)

    def test_test_stat_distribution_discrete_negative_binomial(self):
        # Test Negative Binomial distribution option
        data = np.random.negative_binomial(n=5, p=0.3, size=150)
        df = pd.DataFrame({'nb_counts': data})

        results = test_stat_distribution(
            df,
            column_to_analyze='nb_counts',
            statistical_distribution_to_test='negative_binomial',
            show_probability_plot=False
        )
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)
        stats = results[0]['general_statistics']
        self.assertTrue(stats['is_discrete'])
        self.assertIn('distribution_parameters', stats)

    def test_partition_and_rank_df(self):
        df = pd.DataFrame({
            'department': ['Sales', 'Sales', 'Sales', 'IT', 'IT', 'IT'],
            'score': [70, 95, 80, 60, 90, 85]
        })

        ranked_df = partition_and_rank_df(
            df,
            column_for_partition='department',
            column_to_rank='score',
            ascending=False,
            new_rank_col_name='rank'
        )
        self.assertIn('rank', ranked_df.columns)
        # Sales scores: 95 -> rank 1, 80 -> rank 2, 70 -> rank 3
        sales_ranks = ranked_df[ranked_df['department'] == 'Sales'].sort_values(by='score', ascending=False)['rank'].values
        np.testing.assert_array_equal(sales_ranks, [1.0, 2.0, 3.0])

        # IT scores: 90 -> rank 1, 85 -> rank 2, 60 -> rank 3
        it_ranks = ranked_df[ranked_df['department'] == 'IT'].sort_values(by='score', ascending=False)['rank'].values
        np.testing.assert_array_equal(it_ranks, [1.0, 2.0, 3.0])

    def test_partition_and_rank_df_invalid_inputs(self):
        df = pd.DataFrame({'colA': [1, 2], 'colB': [3, 4]})
        with self.assertRaises(InvalidInputsError):
            partition_and_rank_df(df, column_for_partition='nonexistent', column_to_rank='colB')
        with self.assertRaises(InvalidInputsError):
            partition_and_rank_df(df, column_for_partition='colA', column_to_rank='nonexistent')

    def test_discrete_fourier_transform(self):
        # 100 samples with a clear sine wave at 5 cycles
        t = np.linspace(0, 1, 100)
        signal = 3.0 * np.sin(2 * np.pi * 5 * t) + 1.0 * np.sin(2 * np.pi * 15 * t)
        df = pd.DataFrame({'sensor_signal': signal})

        complex_coefs, freq_df = discrete_fourier_transform(
            df,
            column_to_analyze='sensor_signal',
            average_frequency_of_data_collection='second',
            window='hann',
            detrend=True
        )
        self.assertIsInstance(complex_coefs, np.ndarray)
        self.assertIsInstance(freq_df, pd.DataFrame)
        self.assertIn('freq_in_counts_per_year', freq_df.columns)
        self.assertIn('abs_dft_amplitude', freq_df.columns)
        self.assertIn('spectral_power', freq_df.columns)
        self.assertGreater(len(freq_df), 0)

    def test_adv_imputation_missing_values_numeric(self):
        # Create dataset with missing values in target column
        np.random.seed(42)
        x = np.linspace(0, 10, 80)
        y = 2.5 * x + np.random.normal(0, 0.5, size=80)
        df = pd.DataFrame({'time_step': x, 'measurement': y})
        # Inject 15 missing values
        missing_mask = np.random.choice([True, False], size=80, p=[0.2, 0.8])
        df.loc[missing_mask, 'measurement'] = np.nan

        imputed_df = adv_imputation_missing_values(
            df,
            column_to_fill='measurement',
            timestamp_tag_column='time_step',
            show_imputation_comparison_plots=False
        )
        self.assertIsInstance(imputed_df, pd.DataFrame)
        # Ensure 0 missing values remain in the imputed column
        self.assertEqual(imputed_df['measurement'].isna().sum(), 0)

    def test_adv_imputation_missing_values_categorical(self):
        # Test categorical column with missing values
        categories = ['Type_A', 'Type_B', 'Type_C']
        data = np.random.choice(categories, size=60, p=[0.5, 0.3, 0.2]).astype(object)
        data[5] = np.nan
        data[22] = np.nan
        df = pd.DataFrame({'category': data})

        imputed_df = adv_imputation_missing_values(
            df,
            column_to_fill='category',
            show_imputation_comparison_plots=False
        )
        self.assertEqual(imputed_df['category'].isna().sum(), 0)
        self.assertTrue(imputed_df['category'].isin(categories).all())


if __name__ == '__main__':
    unittest.main()
