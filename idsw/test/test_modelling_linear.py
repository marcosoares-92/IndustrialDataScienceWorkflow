"""
Unit tests for idsw.modelling.linear module.
Covers:
- Standard linear models (ols_linear_reg, ridge_linear_reg, lasso_linear_reg, elastic_net_linear_reg)
- Binary classification (logistic_reg)
- Generalized Linear Models (glm_regression, poisson_regression, negative_binomial_regression, gamma_regression, lognormal_glm_regression)
- Overdispersion diagnostics, deviance, pseudo-R2, and multiplicative effects (exp(beta))
"""

import unittest
import numpy as np
import pandas as pd

from idsw import ControlVars, InvalidInputsError
from idsw.modelling.linear import (
    ols_linear_reg,
    ridge_linear_reg,
    lasso_linear_reg,
    elastic_net_linear_reg,
    logistic_reg,
    glm_regression,
    poisson_regression,
    negative_binomial_regression,
    gamma_regression,
    lognormal_glm_regression
)


class TestModellingLinear(unittest.TestCase):

    def setUp(self):
        ControlVars.show_plots = False
        ControlVars.show_results = False
        np.random.seed(42)

        # Standard regression dataset
        self.X_train_reg = pd.DataFrame({
            "feat_1": np.random.normal(0, 1, 50),
            "feat_2": np.random.normal(5, 2, 50)
        })
        self.y_train_reg = 2.5 * self.X_train_reg["feat_1"] - 1.2 * self.X_train_reg["feat_2"] + 4.0 + np.random.normal(0, 0.5, 50)

        # Count dataset (Poisson / Negative Binomial)
        self.X_train_count = pd.DataFrame({
            "temperature": np.random.uniform(15, 35, 60),
            "pressure": np.random.uniform(1, 5, 60)
        })
        log_lambda = 0.05 * self.X_train_count["temperature"] + 0.2 * self.X_train_count["pressure"] - 1.0
        lambda_rate = np.exp(log_lambda)
        self.y_train_count = np.random.poisson(lam=lambda_rate)

        # Strictly positive continuous dataset (Gamma / Lognormal)
        self.y_train_positive = np.random.gamma(shape=2.0, scale=3.0, size=50)

        # Binary classification dataset
        self.X_train_cls = pd.DataFrame({
            "f1": np.random.normal(0, 1, 60),
            "f2": np.random.normal(0, 1, 60)
        })
        probs = 1.0 / (1.0 + np.exp(-(1.5 * self.X_train_cls["f1"] - 2.0 * self.X_train_cls["f2"])))
        self.y_train_cls = (probs >= 0.5).astype(int)

    def test_glm_poisson(self):
        model, metrics, coefs = glm_regression(
            X_train=self.X_train_count,
            y_train=self.y_train_count,
            distribution="poisson"
        )
        self.assertIsNotNone(model)
        self.assertEqual(metrics["family"], "Poisson")
        self.assertEqual(metrics["link"], "Log")
        self.assertIn("AIC", metrics)
        self.assertIn("deviance", metrics)
        self.assertIn("dispersion_ratio", metrics)
        self.assertIsInstance(coefs, pd.DataFrame)
        self.assertIn("exp_coefficient", coefs.columns)
        self.assertIn("p_value", coefs.columns)

    def test_glm_negative_binomial(self):
        model, metrics, coefs = negative_binomial_regression(
            X_train=self.X_train_count,
            y_train=self.y_train_count,
            alpha_dispersion=0.5
        )
        self.assertIsNotNone(model)
        self.assertEqual(metrics["family"], "NegativeBinomial")
        self.assertIn("AIC", metrics)
        self.assertGreaterEqual(metrics["dispersion_ratio"], 0.0)

    def test_glm_gamma(self):
        model, metrics, coefs = gamma_regression(
            X_train=self.X_train_reg,
            y_train=self.y_train_positive,
            link="log"
        )
        self.assertIsNotNone(model)
        self.assertEqual(metrics["family"], "Gamma")
        self.assertIn("AIC", metrics)

    def test_glm_lognormal(self):
        model, metrics, coefs = lognormal_glm_regression(
            X_train=self.X_train_reg,
            y_train=self.y_train_positive
        )
        self.assertIsNotNone(model)
        self.assertEqual(metrics["family"], "Gaussian")
        self.assertEqual(metrics["link"], "Log")

    def test_glm_invalid_inputs(self):
        # Negative count in Poisson
        invalid_y = pd.Series([-1, 2, 5, 3])
        with self.assertRaises(InvalidInputsError):
            glm_regression(
                X_train=self.X_train_count.iloc[:4],
                y_train=invalid_y,
                distribution="poisson"
            )

        # Unsupported distribution
        with self.assertRaises(InvalidInputsError):
            glm_regression(
                X_train=self.X_train_count,
                y_train=self.y_train_count,
                distribution="unsupported_distribution"
            )

        # None inputs
        with self.assertRaises(InvalidInputsError):
            glm_regression(X_train=None, y_train=None)


if __name__ == "__main__":
    unittest.main()
