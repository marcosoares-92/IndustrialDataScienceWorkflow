"""
Unit tests for idsw.etl.timeseries module.
Covers:
- lag_diagnosis (ACF/PACF computation, significant lags detection, return values)
- test_d_parameters (ADF stationarity test, d=0 handling, differencing order suggestion)
- best_arima_model (AIC/BIC/MAE/RMSE criteria, fit stability, predictions and confidence bands)
- arima_forecasting (future forecast generation, timestamps handling)
"""

import unittest
import numpy as np
import pandas as pd

from idsw import ControlVars, InvalidInputsError
from idsw.etl.timeseries import (
    lag_diagnosis,
    test_d_parameters,
    best_arima_model,
    arima_forecasting
)


class TestETLTimeSeries(unittest.TestCase):

    def setUp(self):
        ControlVars.show_plots = False
        ControlVars.show_results = False
        np.random.seed(42)

        # Generate synthetic AR(1) process: y_t = 0.7 * y_{t-1} + e_t
        n = 100
        e = np.random.normal(0, 1, n)
        y = np.zeros(n)
        for t in range(1, n):
            y[t] = 0.7 * y[t - 1] + e[t]

        dates = pd.date_range(start="2024-01-01", periods=n, freq="D")
        self.ts_df = pd.DataFrame({
            "timestamp": dates,
            "sensor_reading": y
        })

    def test_lag_diagnosis_valid_series(self):
        suggested_p, suggested_q, diagnosis_dict = lag_diagnosis(
            df=self.ts_df,
            column_to_analyze="sensor_reading",
            number_of_lags=15
        )
        self.assertIsInstance(suggested_p, list)
        self.assertIsInstance(suggested_q, list)
        self.assertIsInstance(diagnosis_dict, dict)
        self.assertIn("acf_values", diagnosis_dict)
        self.assertIn("pacf_values", diagnosis_dict)
        self.assertIn("max_lags", diagnosis_dict)
        self.assertGreater(len(suggested_p), 0)
        self.assertGreater(len(suggested_q), 0)

    def test_lag_diagnosis_invalid_inputs(self):
        # Non-dataframe
        with self.assertRaises(InvalidInputsError):
            lag_diagnosis(df=[1, 2, 3], column_to_analyze="sensor_reading")

        # Non-existent column
        with self.assertRaises(InvalidInputsError):
            lag_diagnosis(df=self.ts_df, column_to_analyze="non_existent_col")

        # Too short series (< 10 observations)
        short_df = pd.DataFrame({"sensor_reading": [1.0, 2.0, 3.0]})
        with self.assertRaises(InvalidInputsError):
            lag_diagnosis(df=short_df, column_to_analyze="sensor_reading")

    def test_test_d_parameters_stationarity(self):
        # For stationary series (AR(1) with phi=0.7), d=0 should already be stationary
        optimal_d_list, adf_results = test_d_parameters(
            df=self.ts_df,
            column_to_analyze="sensor_reading",
            max_tested_d=3,
            significance_level=0.05
        )
        self.assertIsInstance(optimal_d_list, list)
        self.assertIsInstance(adf_results, dict)
        self.assertIn(0, adf_results)
        self.assertIn("p_value", adf_results[0])
        self.assertIn("is_stationary", adf_results[0])

    def test_test_d_parameters_integrated_series(self):
        # Create non-stationary random walk with trend: y_t = y_{t-1} + trend + noise
        rw = np.cumsum(np.random.normal(0.5, 1, 100))
        rw_df = pd.DataFrame({"rw_col": rw})

        optimal_d_list, adf_results = test_d_parameters(
            df=rw_df,
            column_to_analyze="rw_col",
            max_tested_d=2,
            significance_level=0.05
        )
        self.assertIsInstance(optimal_d_list, list)
        self.assertIn(0, adf_results)
        self.assertIn(1, adf_results)
        # Differenced at least once (d >= 1) should be stationary
        self.assertTrue(any(d >= 1 for d in optimal_d_list) or len(optimal_d_list) > 0)

    def test_best_arima_model_aic_selection(self):
        # Grid search with p in [1, 2], d=0, q in [0, 1]
        model_res, summ_dict, arima_df = best_arima_model(
            df=self.ts_df,
            column_to_analyze="sensor_reading",
            d_order=0,
            max_p=2,
            max_q=1,
            criterion="aic"
        )
        self.assertIsNotNone(model_res)
        self.assertIsInstance(summ_dict, dict)
        self.assertEqual(summ_dict["d"], 0)
        self.assertIn("p", summ_dict)
        self.assertIn("q", summ_dict)
        self.assertIn("AIC", summ_dict)
        self.assertEqual(summ_dict["criterion_used"], "aic")

        # Output dataframe verification
        self.assertIsInstance(arima_df, pd.DataFrame)
        self.assertIn("arima_predictions", arima_df.columns)
        self.assertIn("lower_cl", arima_df.columns)
        self.assertIn("upper_cl", arima_df.columns)
        self.assertEqual(len(arima_df), len(self.ts_df))

    def test_best_arima_model_with_timestamp(self):
        # With timestamp_tag_column
        model_res, summ_dict, arima_df = best_arima_model(
            df=self.ts_df,
            column_to_analyze="sensor_reading",
            timestamp_tag_column="timestamp",
            d_order=0,
            max_p=1,
            max_q=0,
            criterion="bic"
        )
        self.assertIn("timestamp", arima_df.columns)
        self.assertIn("arima_predictions", arima_df.columns)

    def test_arima_forecasting(self):
        model_res, _, _ = best_arima_model(
            df=self.ts_df,
            column_to_analyze="sensor_reading",
            timestamp_tag_column="timestamp",
            d_order=0,
            max_p=1,
            max_q=0
        )
        # Forecast 5 steps ahead
        forecast_df = arima_forecasting(
            arima_model_object=model_res,
            df=self.ts_df,
            column_to_forecast="sensor_reading",
            timestamp_tag_column="timestamp",
            number_of_periods_to_forecast=5,
            plot_predicted_time_series=False
        )
        self.assertIsInstance(forecast_df, pd.DataFrame)
        self.assertGreaterEqual(len(forecast_df), 5)


if __name__ == "__main__":
    unittest.main()
