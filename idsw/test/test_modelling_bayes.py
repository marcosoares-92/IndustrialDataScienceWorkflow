"""
Unit tests for idsw.modelling.bayes module.
Covers:
- gaussian_naive_bayes
- multinomial_naive_bayes
- bernoulli_naive_bayes
- naive_bayes_classifier
- bayesian_linear_regression (Ridge and ARD)
- bayesian_logistic_regression
- bayesian_model (unified multi-task wrapper)
"""

import unittest
import numpy as np
import pandas as pd

from idsw import ControlVars, InvalidInputsError
from idsw.modelling.bayes import (
    gaussian_naive_bayes,
    multinomial_naive_bayes,
    bernoulli_naive_bayes,
    naive_bayes_classifier,
    bayesian_linear_regression,
    bayesian_logistic_regression,
    bayesian_model
)


class TestModellingBayes(unittest.TestCase):

    def setUp(self):
        ControlVars.show_plots = False
        ControlVars.show_results = False
        np.random.seed(42)

        # Continuous features classification
        self.X_cont = pd.DataFrame({
            "f1": np.random.normal(0, 1, 50),
            "f2": np.random.normal(2, 1.5, 50)
        })
        self.y_cls = (self.X_cont["f1"] + self.X_cont["f2"] > 2.0).astype(int)

        # Non-negative count features
        self.X_counts = pd.DataFrame({
            "word_count_1": np.random.poisson(lam=3.0, size=50),
            "word_count_2": np.random.poisson(lam=1.5, size=50)
        })

        # Binary indicator features
        self.X_bin = pd.DataFrame({
            "has_tag_a": np.random.binomial(1, 0.4, 50),
            "has_tag_b": np.random.binomial(1, 0.6, 50)
        })

        # Regression targets
        self.y_reg = 3.0 * self.X_cont["f1"] - 1.5 * self.X_cont["f2"] + np.random.normal(0, 0.3, 50)

    def test_gaussian_naive_bayes(self):
        model, metrics, summary_df, classes_dict = gaussian_naive_bayes(
            X_train=self.X_cont,
            y_train=self.y_cls
        )
        self.assertIsNotNone(model)
        self.assertIn("accuracy", metrics)
        self.assertEqual(classes_dict["number_of_classes"], 2)
        self.assertIsInstance(summary_df, pd.DataFrame)
        self.assertEqual(len(summary_df), 2)  # 2 features

    def test_multinomial_naive_bayes(self):
        model, metrics, feat_df, classes_dict = multinomial_naive_bayes(
            X_train=self.X_counts,
            y_train=self.y_cls,
            alpha=1.0
        )
        self.assertIsNotNone(model)
        self.assertIn("accuracy", metrics)
        self.assertIsInstance(feat_df, pd.DataFrame)

    def test_multinomial_negative_values_error(self):
        # Negative counts should raise InvalidInputsError
        invalid_counts = self.X_counts.copy()
        invalid_counts.iloc[0, 0] = -5
        with self.assertRaises(InvalidInputsError):
            multinomial_naive_bayes(X_train=invalid_counts, y_train=self.y_cls)

    def test_bernoulli_naive_bayes(self):
        model, metrics, feat_df, classes_dict = bernoulli_naive_bayes(
            X_train=self.X_bin,
            y_train=self.y_cls,
            alpha=1.0
        )
        self.assertIsNotNone(model)
        self.assertIn("accuracy", metrics)
        self.assertIsInstance(feat_df, pd.DataFrame)

    def test_naive_bayes_classifier_dispatcher(self):
        model, metrics, _, _ = naive_bayes_classifier(
            X_train=self.X_cont,
            y_train=self.y_cls,
            algorithm="gaussian"
        )
        self.assertIsNotNone(model)

        with self.assertRaises(InvalidInputsError):
            naive_bayes_classifier(
                X_train=self.X_cont,
                y_train=self.y_cls,
                algorithm="unsupported_nb"
            )

    def test_bayesian_linear_regression(self):
        # Ridge prior
        model, metrics, feat_imp = bayesian_linear_regression(
            X_train=self.X_cont,
            y_train=self.y_reg,
            ard=False
        )
        self.assertIsNotNone(model)
        self.assertIn("R2_score", metrics)
        self.assertIn("alpha_weight_precision", metrics)

        # ARD prior
        model_ard, metrics_ard, _ = bayesian_linear_regression(
            X_train=self.X_cont,
            y_train=self.y_reg,
            ard=True
        )
        self.assertIsNotNone(model_ard)
        self.assertIn("R2_score", metrics_ard)

    def test_bayesian_logistic_regression(self):
        model, metrics, feat_imp, classes_dict = bayesian_logistic_regression(
            X_train=self.X_cont,
            y_train=self.y_cls,
            prior_variance=0.5
        )
        self.assertIsNotNone(model)
        self.assertIn("accuracy", metrics)
        self.assertEqual(classes_dict["number_of_classes"], 2)

    def test_bayesian_model_unified(self):
        # Regression
        m_reg, met_reg, _ = bayesian_model(
            X_train=self.X_cont,
            y_train=self.y_reg,
            model_type="regression",
            algorithm="ridge"
        )
        self.assertIsNotNone(m_reg)

        # Classification
        m_cls, met_cls, _, _ = bayesian_model(
            X_train=self.X_cont,
            y_train=self.y_cls,
            model_type="classification",
            algorithm="logistic"
        )
        self.assertIsNotNone(m_cls)

        with self.assertRaises(InvalidInputsError):
            bayesian_model(
                X_train=self.X_cont,
                y_train=self.y_reg,
                model_type="invalid_type"
            )


if __name__ == "__main__":
    unittest.main()
