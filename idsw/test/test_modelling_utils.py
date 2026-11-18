"""
Unit tests for idsw.modelling.utils and core.AnomalyDetector modules.
Covers:
- make_model_predictions (with sklearn, statsmodels, tuples)
- calculate_class_probability
- shap_feature_analysis (with error handling and fallbacks)
- AnomalyDetector (gaussian, exponential, poisson, uniform distributions)
"""

import unittest
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge, LogisticRegression

from idsw import ControlVars, InvalidInputsError
from idsw.modelling.utils import (
    make_model_predictions,
    calculate_class_probability,
    shap_feature_analysis
)
from idsw.modelling.core import AnomalyDetector
from idsw.modelling.linear import poisson_regression


class TestModellingUtils(unittest.TestCase):

    def setUp(self):
        ControlVars.show_plots = False
        ControlVars.show_results = False
        np.random.seed(42)

        self.X_reg = pd.DataFrame({
            "x1": np.random.normal(0, 1, 40),
            "x2": np.random.normal(0, 1, 40)
        })
        self.y_reg = 2.0 * self.X_reg["x1"] - 1.0 * self.X_reg["x2"] + 3.0

        self.X_cls = pd.DataFrame({
            "f1": np.random.normal(0, 1, 40),
            "f2": np.random.normal(0, 1, 40)
        })
        self.y_cls = (self.X_cls["f1"] + self.X_cls["f2"] > 0).astype(int)

    def test_make_model_predictions_sklearn(self):
        model = Ridge()
        model.fit(self.X_reg, self.y_reg)

        preds = make_model_predictions(model, self.X_reg)
        self.assertIsInstance(preds, (pd.DataFrame, pd.Series, np.ndarray))
        self.assertEqual(len(preds), len(self.X_reg))

    def test_make_model_predictions_statsmodels_tuple(self):
        # Fit poisson regression (returns tuple: model, metrics, coefs)
        y_count = np.random.poisson(lam=3.0, size=len(self.X_reg))
        model_tuple = poisson_regression(self.X_reg, y_count)

        preds = make_model_predictions(model_tuple, self.X_reg)
        self.assertIsNotNone(preds)
        self.assertEqual(len(preds), len(self.X_reg))

    def test_calculate_class_probability(self):
        clf = LogisticRegression()
        clf.fit(self.X_cls, self.y_cls)

        probs_df = calculate_class_probability(
            model_object=clf,
            X=self.X_cls,
            list_of_classes=[0, 1]
        )
        self.assertIsInstance(probs_df, pd.DataFrame)
        self.assertIn("prob_class_0", probs_df.columns)
        self.assertIn("prob_class_1", probs_df.columns)

    def test_shap_feature_analysis_robust(self):
        model = Ridge()
        model.fit(self.X_reg, self.y_reg)

        shap_res = shap_feature_analysis(
            model_object=model,
            X_train=self.X_reg,
            model_type="linear",
            total_of_shap_points=20
        )
        self.assertIsInstance(shap_res, dict)
        self.assertIn("SHAP_status", shap_res)

    def test_anomaly_detector_gaussian(self):
        ad = AnomalyDetector(epsilon=0.01, distribution="gaussian")
        X = np.random.normal(0, 1, (50, 2))
        ad.fit(X)
        ad.calculate_probabilities(X)
        self.assertIsNotNone(ad.estimated_probabilities)
        self.assertEqual(len(ad.estimated_probabilities), 50)

    def test_anomaly_detector_exponential(self):
        ad = AnomalyDetector(epsilon=0.01, distribution="exponential")
        X = np.random.exponential(scale=2.0, size=(50, 2))
        ad.fit(X)
        ad.calculate_probabilities(X)
        self.assertIsNotNone(ad.estimated_probabilities)

    def test_anomaly_detector_poisson(self):
        ad = AnomalyDetector(epsilon=0.01, distribution="poisson")
        X = np.random.poisson(lam=3.0, size=(50, 2))
        ad.fit(X)
        ad.calculate_probabilities(X)
        self.assertIsNotNone(ad.estimated_probabilities)

    def test_anomaly_detector_uniform(self):
        ad = AnomalyDetector(epsilon=0.01, distribution="uniform")
        X = np.random.uniform(0, 10, (50, 2))
        ad.fit(X)
        ad.calculate_probabilities(X)
        self.assertIsNotNone(ad.estimated_probabilities)


if __name__ == "__main__":
    unittest.main()
