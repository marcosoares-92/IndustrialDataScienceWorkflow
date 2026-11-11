"""
Unit tests for idsw.modelling.recommendation_engines module.
Covers:
- wide_to_long_ratings
- als_recommender (explicit and implicit feedback)
- recommend_for_users
- recommend_for_items
- collaborative_filtering_recommender (user_based and item_based)
"""

import unittest
import numpy as np
import pandas as pd

from idsw import ControlVars, InvalidInputsError
from idsw.modelling.recommendation_engines import (
    wide_to_long_ratings,
    als_recommender,
    recommend_for_users,
    recommend_for_items,
    collaborative_filtering_recommender
)


class TestRecommendationEngines(unittest.TestCase):

    def setUp(self):
        ControlVars.show_plots = False
        ControlVars.show_results = False
        np.random.seed(42)

        # Synthetic user-item rating matrix in long format
        users = [f"user_{i}" for i in range(10)]
        items = [f"item_{j}" for j in range(8)]

        rows = []
        for u in users:
            # Each user rates 4 to 6 items
            chosen_items = np.random.choice(items, size=5, replace=False)
            for it in chosen_items:
                rows.append({
                    "user_id": u,
                    "item_id": it,
                    "rating": float(np.random.randint(1, 6))
                })

        self.ratings_df = pd.DataFrame(rows).drop_duplicates(subset=["user_id", "item_id"])

        # Wide format dataframe
        self.wide_df = self.ratings_df.pivot(index="user_id", columns="item_id", values="rating")

    def test_wide_to_long_ratings(self):
        long_df = wide_to_long_ratings(self.wide_df, user_col="user_id", item_name="item_id", rating_name="rating")
        self.assertIsInstance(long_df, pd.DataFrame)
        self.assertIn("user_id", long_df.columns)
        self.assertIn("item_id", long_df.columns)
        self.assertIn("rating", long_df.columns)
        self.assertEqual(len(long_df), len(self.ratings_df))

    def test_als_recommender_explicit(self):
        model, metrics, u_factors, i_factors = als_recommender(
            ratings_df=self.ratings_df,
            user_col="user_id",
            item_col="item_id",
            rating_col="rating",
            rank=4,
            max_iter=5,
            reg_param=0.1,
            implicit_prefs=False
        )
        self.assertIsNotNone(model)
        self.assertIn("test_rmse", metrics)
        self.assertIsInstance(u_factors, pd.DataFrame)
        self.assertIsInstance(i_factors, pd.DataFrame)
        self.assertEqual(u_factors.shape[1], 4)

    def test_als_recommender_implicit(self):
        model, metrics, u_factors, i_factors = als_recommender(
            ratings_df=self.ratings_df,
            user_col="user_id",
            item_col="item_id",
            rating_col="rating",
            rank=4,
            max_iter=5,
            reg_param=0.1,
            implicit_prefs=True,
            alpha=20.0
        )
        self.assertIsNotNone(model)
        self.assertIn("test_rmse", metrics)

    def test_recommend_for_users_and_items(self):
        model, _, _, _ = als_recommender(
            ratings_df=self.ratings_df,
            user_col="user_id",
            item_col="item_id",
            rating_col="rating",
            rank=4,
            max_iter=5
        )
        # Recommend for users
        user_recs = recommend_for_users(model, user_ids=["user_0", "user_1"], num_items=3)
        self.assertIsInstance(user_recs, pd.DataFrame)
        self.assertIn("predicted_score", user_recs.columns)
        self.assertEqual(len(user_recs), 6)  # 2 users * 3 items

        # Recommend for items
        item_recs = recommend_for_items(model, item_ids=["item_0"], num_users=4)
        self.assertIsInstance(item_recs, pd.DataFrame)
        self.assertEqual(len(item_recs), 4)

    def test_collaborative_filtering(self):
        # Item-based
        cf_dict, sim_df, rec_fn = collaborative_filtering_recommender(
            ratings_df=self.ratings_df,
            method="item_based"
        )
        self.assertEqual(cf_dict["method"], "item_based")
        self.assertIsInstance(sim_df, pd.DataFrame)
        recs = rec_fn("user_0", top_n=3)
        self.assertIsInstance(recs, pd.DataFrame)

        # User-based
        cf_dict_u, sim_df_u, rec_fn_u = collaborative_filtering_recommender(
            ratings_df=self.ratings_df,
            method="user_based"
        )
        self.assertEqual(cf_dict_u["method"], "user_based")
        recs_u = rec_fn_u("user_0", top_n=3)
        self.assertIsInstance(recs_u, pd.DataFrame)

    def test_invalid_inputs(self):
        with self.assertRaises(InvalidInputsError):
            wide_to_long_ratings("not_a_df")

        with self.assertRaises(InvalidInputsError):
            als_recommender(ratings_df="not_a_df")


if __name__ == "__main__":
    unittest.main()
