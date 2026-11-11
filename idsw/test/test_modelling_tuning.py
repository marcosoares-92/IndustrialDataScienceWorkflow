"""
Unit tests for idsw.modelling.tuning module.
Covers:
- grid_search_tuning
- random_search_tuning
- coarse_to_fine_tuning
- bayesian_optimization_tuning
- genetic_algorithm_tuning
"""

import unittest
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.ensemble import RandomForestRegressor

from idsw import ControlVars, InvalidInputsError
from idsw.modelling.tuning import (
    grid_search_tuning,
    random_search_tuning,
    coarse_to_fine_tuning,
    bayesian_optimization_tuning,
    genetic_algorithm_tuning
)


class TestModellingTuning(unittest.TestCase):

    def setUp(self):
        ControlVars.show_plots = False
        ControlVars.show_results = False
        np.random.seed(42)

        # Synthetic regression dataset
        self.X_reg = pd.DataFrame({
            "x1": np.random.normal(0, 1, 40),
            "x2": np.random.normal(0, 1, 40)
        })
        self.y_reg = 2.0 * self.X_reg["x1"] + 0.5 * self.X_reg["x2"] + np.random.normal(0, 0.2, 40)

        # Synthetic classification dataset
        self.X_cls = pd.DataFrame({
            "f1": np.random.normal(0, 1, 40),
            "f2": np.random.normal(0, 1, 40)
        })
        self.y_cls = (self.X_cls["f1"] + self.X_cls["f2"] > 0).astype(int)

    def test_grid_search_tuning_regression(self):
        model = Ridge()
        param_grid = {"alpha": [0.01, 0.1, 1.0, 10.0]}

        best_est, best_params, results_df = grid_search_tuning(
            model_object=model,
            param_grid=param_grid,
            X_train=self.X_reg,
            y_train=self.y_reg,
            cv=3,
            plot_results=False
        )
        self.assertIsNotNone(best_est)
        self.assertIn("alpha", best_params)
        self.assertIsInstance(results_df, pd.DataFrame)
        self.assertEqual(len(results_df), 4)

    def test_random_search_tuning_classification(self):
        model = LogisticRegression(solver="liblinear")
        param_dist = {"C": [0.01, 0.1, 1.0, 10.0, 100.0]}

        best_est, best_params, results_df = random_search_tuning(
            model_object=model,
            param_distributions=param_dist,
            X_train=self.X_cls,
            y_train=self.y_cls,
            n_iter=3,
            cv=3,
            plot_results=False
        )
        self.assertIsNotNone(best_est)
        self.assertIn("C", best_params)
        self.assertIsInstance(results_df, pd.DataFrame)

    def test_coarse_to_fine_tuning(self):
        model = Ridge()
        broad_dist = {"alpha": [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]}

        best_est, best_params, summary = coarse_to_fine_tuning(
            model_object=model,
            broad_param_distributions=broad_dist,
            X_train=self.X_reg,
            y_train=self.y_reg,
            coarse_iterations=4,
            top_candidates_to_refine=2,
            refine_steps=2,
            cv=3
        )
        self.assertIsNotNone(best_est)
        self.assertIn("alpha", best_params)
        self.assertIn("coarse_best_score", summary)
        self.assertIn("fine_best_score", summary)

    def test_bayesian_optimization_tuning(self):
        model = Ridge()
        # Search alpha between 0.01 and 10.0 float
        param_space = {
            "alpha": (0.01, 10.0, "float")
        }

        best_est, best_params, hist_df = bayesian_optimization_tuning(
            model_object=model,
            param_space=param_space,
            X_train=self.X_reg,
            y_train=self.y_reg,
            n_iterations=5,
            n_initial_points=2,
            cv=3,
            plot_convergence=False
        )
        self.assertIsNotNone(best_est)
        self.assertIn("alpha", best_params)
        self.assertIsInstance(hist_df, pd.DataFrame)
        self.assertEqual(len(hist_df), 5)
        self.assertIn("best_score_so_far", hist_df.columns)

    def test_genetic_algorithm_tuning(self):
        model = Ridge()
        param_space = {
            "alpha": [0.01, 0.05, 0.1, 0.5, 1.0, 5.0, 10.0]
        }

        best_est, best_params, hist_df = genetic_algorithm_tuning(
            model_object=model,
            param_space=param_space,
            X_train=self.X_reg,
            y_train=self.y_reg,
            population_size=6,
            generations=2,
            cv=3
        )
        self.assertIsNotNone(best_est)
        self.assertIn("alpha", best_params)
        self.assertIsInstance(hist_df, pd.DataFrame)
        self.assertEqual(len(hist_df), 12)  # 6 ind * 2 gens

    def test_invalid_inputs(self):
        with self.assertRaises(InvalidInputsError):
            grid_search_tuning(
                model_object="not_a_model",
                param_grid={"alpha": [1]},
                X_train=self.X_reg,
                y_train=self.y_reg
            )

        with self.assertRaises(InvalidInputsError):
            grid_search_tuning(
                model_object=Ridge(),
                param_grid="not_a_dict",
                X_train=self.X_reg,
                y_train=self.y_reg
            )


if __name__ == "__main__":
    unittest.main()
