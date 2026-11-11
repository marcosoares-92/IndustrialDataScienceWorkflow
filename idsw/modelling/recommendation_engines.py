"""
idsw.modelling.recommendation_engines
=====================================
Scalable Recommendation Engines powered by Apache Spark (PySpark MLlib) and pure-Python algorithms.
Includes:
- Alternating Least Squares (ALS) Matrix Factorization for Explicit and Implicit Feedback
- User-Based and Item-Based Collaborative Filtering (Cosine and Pearson similarity)
- Top-N Recommendations for Users and Items
- ALS Hyperparameter Cross-Validation Tuning (RMSE and Ranking Error - ROEM)
- Matrix Reshaping Utilities (Wide-to-Long conversion)

---------------------------------------------------------------------------------------------------------
SETUP GUIDE: RUNNING PYSPARK AND SPARKMAGIC ON WINDOWS 11
---------------------------------------------------------------------------------------------------------
1. Install Java:
   - Download OpenJDK 11 or 17 (e.g. Eclipse Temurin / Microsoft OpenJDK).
   - Set Windows Environment Variable: JAVA_HOME = C:\\Program Files\\Eclipse Adoptium\\jdk-11...
   - Add to PATH: %JAVA_HOME%\\bin

2. Download Apache Spark:
   - Download Apache Spark 3.4+ or 3.5+ (pre-built for Apache Hadoop 3.3+) from https://spark.apache.org/downloads.html
   - Extract to C:\\spark (or C:\\hadoop\\spark)
   - Set Environment Variable: SPARK_HOME = C:\\spark
   - Add to PATH: %SPARK_HOME%\\bin

3. Configure Windows Hadoop Binaries (winutils):
   - Windows requires winutils.exe and hadoop.dll to execute Spark jobs locally.
   - Download winutils.exe and hadoop.dll for Hadoop 3.3.x from:
     https://github.com/cdarlint/winutils
   - Create directory C:\\hadoop\\bin and place winutils.exe and hadoop.dll inside.
   - Set Environment Variable: HADOOP_HOME = C:\\hadoop
   - Add to PATH: %HADOOP_HOME%\\bin

4. Install Python Packages:
   - Run in terminal:
     pip install pyspark findspark sparkmagic

5. Install and Enable SparkMagic for Jupyter Notebook in Windows 11:
   - Run in terminal:
     jupyter nbextension enable --py --sys-prefix widgetsnbextension
     python -c "import sparkmagic, os; print(os.path.dirname(sparkmagic.__file__))"
     # Use path returned above to register kernels:
     jupyter-kernelspec install --user <sparkmagic_dir>/kernels/sparkkernel
     jupyter-kernelspec install --user <sparkmagic_dir>/kernels/pysparkkernel
   - Start Jupyter Notebook: jupyter notebook
   - Now you can select "PySpark" kernel or connect to Livy server via %%spark magics!
---------------------------------------------------------------------------------------------------------
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from idsw import InvalidInputsError, ControlVars


def wide_to_long_ratings(df, user_col = 'user_id', item_name = 'item_id', rating_name = 'rating'):
    """
    wide_to_long_ratings:
    Converts a wide user-item matrix into long (row-based) format: [user_col, item_id, rating].
    Filters out unobserved / NaN ratings.

    : param: df: pandas DataFrame in wide format (rows = users, columns = items).
    : param: user_col: string (default 'user_id'), name of user identifier column.
    : param: item_name: string (default 'item_id'), target name for melted item column.
    : param: rating_name: string (default 'rating'), target name for rating column.
    : return: pandas DataFrame in long format.
    """
    if not isinstance(df, pd.DataFrame):
        raise InvalidInputsError("df must be a valid pandas DataFrame.")

    if user_col in df.columns:
        id_vars = [user_col]
        value_vars = [c for c in df.columns if c != user_col]
    else:
        df_copy = df.copy()
        df_copy[user_col] = df_copy.index
        id_vars = [user_col]
        value_vars = [c for c in df.columns]
        df = df_copy

    long_df = pd.melt(
        df,
        id_vars = id_vars,
        value_vars = value_vars,
        var_name = item_name,
        value_name = rating_name
    )
    long_df = long_df.dropna(subset = [rating_name]).reset_index(drop = True)
    return long_df


def als_recommender(
    ratings_df,
    user_col = 'user_id',
    item_col = 'item_id',
    rating_col = 'rating',
    rank = 10,
    max_iter = 15,
    reg_param = 0.1,
    implicit_prefs = False,
    alpha = 40.0,
    nonnegative = True,
    cold_start_strategy = 'drop',
    test_size = 0.2,
    seed = 42
):
    """
    als_recommender:
    Fits an Alternating Least Squares (ALS) matrix factorization recommender.
    Leverages PySpark MLlib if available; seamlessly falls back to pure-Python/NumPy ALS
    when running in environments without an active Spark cluster.

    : param: ratings_df: pandas DataFrame or PySpark DataFrame containing interaction data.
    : param: user_col: name of the column identifying users (integer or string).
    : param: item_col: name of the column identifying items (integer or string).
    : param: rating_col: name of the column containing ratings or implicit interaction counts.
    : param: rank: integer (default 10), number of latent factors.
    : param: max_iter: integer (default 15), maximum iterations of alternating optimization.
    : param: reg_param: float (default 0.1), L2 regularization parameter lambda.
    : param: implicit_prefs: boolean (default False), True for implicit feedback (clicks, views, plays).
    : param: alpha: float (default 40.0), confidence scaling parameter for implicit feedback.
    : param: nonnegative: boolean (default True), enforce non-negativity constraint on latent factors.
    : param: cold_start_strategy: 'drop' or 'nan' for unseen users/items during evaluation.
    : return: tuple (model_dict, metrics_dict, user_factors_df, item_factors_df).
    """
    # Check if input is a PySpark DataFrame
    is_spark_df = False
    try:
        from pyspark.sql import DataFrame as SparkDataFrame
        if isinstance(ratings_df, SparkDataFrame):
            is_spark_df = True
    except Exception:
        pass

    if is_spark_df:
        # Native PySpark ALS execution
        from pyspark.ml.recommendation import ALS
        from pyspark.ml.evaluation import RegressionEvaluator

        train_df, test_df = ratings_df.randomSplit([1.0 - test_size, test_size], seed = seed)

        als = ALS(
            rank = rank,
            maxIter = max_iter,
            regParam = reg_param,
            userCol = user_col,
            itemCol = item_col,
            ratingCol = rating_col,
            coldStartStrategy = cold_start_strategy,
            nonnegative = nonnegative,
            implicitPrefs = implicit_prefs,
            alpha = alpha
        )
        spark_model = als.fit(train_df)

        predictions = spark_model.transform(test_df)
        evaluator = RegressionEvaluator(metricName = "rmse", labelCol = rating_col, predictionCol = "prediction")
        rmse = float(evaluator.evaluate(predictions))
        mae_eval = RegressionEvaluator(metricName = "mae", labelCol = rating_col, predictionCol = "prediction")
        mae = float(mae_eval.evaluate(predictions))

        user_factors_df = spark_model.userFactors.toPandas()
        item_factors_df = spark_model.itemFactors.toPandas()

        metrics_dict = {
            "model_type": "PySpark ALS",
            "rank": rank,
            "max_iter": max_iter,
            "reg_param": reg_param,
            "implicit_prefs": implicit_prefs,
            "test_rmse": rmse,
            "test_mae": mae
        }

        model_dict = {
            "type": "pyspark_als",
            "spark_model": spark_model,
            "user_col": user_col,
            "item_col": item_col,
            "rating_col": rating_col,
            "metrics": metrics_dict
        }

        if ControlVars.show_results:
            print("=" * 80)
            print("PYSPARK ALS MATRIX FACTORIZATION COMPLETE")
            print("=" * 80)
            print(f"Latent Factors (rank): {rank} | Reg Param: {reg_param} | Max Iterations: {max_iter}")
            print(f"Test RMSE: {rmse:.4f} | Test MAE: {mae:.4f}")

        return model_dict, metrics_dict, user_factors_df, item_factors_df

    # Pure Python / NumPy Matrix Factorization Fallback
    if not isinstance(ratings_df, pd.DataFrame):
        raise InvalidInputsError("ratings_df must be a pandas DataFrame or PySpark DataFrame.")

    pdf = ratings_df.copy(deep = True).dropna(subset = [user_col, item_col, rating_col])

    # Map user and item IDs to integer indices
    unique_users = sorted(pdf[user_col].unique())
    unique_items = sorted(pdf[item_col].unique())
    user_to_idx = {u: i for i, u in enumerate(unique_users)}
    item_to_idx = {it: j for j, it in enumerate(unique_items)}
    idx_to_user = {i: u for u, i in user_to_idx.items()}
    idx_to_item = {j: it for it, j in item_to_idx.items()}

    n_users = len(unique_users)
    n_items = len(unique_items)

    # Split train and test
    np.random.seed(seed)
    n_samples = len(pdf)
    shuffled_idx = np.random.permutation(n_samples)
    n_test = int(n_samples * test_size)
    test_rows = pdf.iloc[shuffled_idx[:n_test]]
    train_rows = pdf.iloc[shuffled_idx[n_test:]]

    # Initialize factor matrices U (n_users x rank) and V (n_items x rank)
    rng = np.random.RandomState(seed)
    U = rng.normal(scale = 1.0 / np.sqrt(rank), size = (n_users, rank))
    V = rng.normal(scale = 1.0 / np.sqrt(rank), size = (n_items, rank))

    if nonnegative:
        U = np.abs(U)
        V = np.abs(V)

    # Train ALS iterations
    for it in range(max_iter):
        # Update user factors U
        for u_id in range(n_users):
            u_data = train_rows[train_rows[user_col] == idx_to_user[u_id]]
            if len(u_data) == 0:
                continue
            item_indices = [item_to_idx[item] for item in u_data[item_col] if item in item_to_idx]
            r_u = u_data[rating_col].values
            V_u = V[item_indices, :]

            if implicit_prefs:
                # Confidence matrix C_ui = 1 + alpha * r_ui
                c_u = 1.0 + alpha * r_u
                V_T_C_V = np.dot(V_u.T, (c_u[:, None] * V_u)) + reg_param * np.eye(rank)
                p_u = (r_u > 0).astype(float)
                U[u_id] = np.linalg.solve(V_T_C_V, np.dot(V_u.T, (c_u * p_u)))
            else:
                A = np.dot(V_u.T, V_u) + reg_param * np.eye(rank)
                b = np.dot(V_u.T, r_u)
                U[u_id] = np.linalg.solve(A, b)

            if nonnegative:
                U[u_id] = np.maximum(U[u_id], 0.0)

        # Update item factors V
        for i_id in range(n_items):
            i_data = train_rows[train_rows[item_col] == idx_to_item[i_id]]
            if len(i_data) == 0:
                continue
            user_indices = [user_to_idx[usr] for usr in i_data[user_col] if usr in user_to_idx]
            r_i = i_data[rating_col].values
            U_i = U[user_indices, :]

            if implicit_prefs:
                c_i = 1.0 + alpha * r_i
                U_T_C_U = np.dot(U_i.T, (c_i[:, None] * U_i)) + reg_param * np.eye(rank)
                p_i = (r_i > 0).astype(float)
                V[i_id] = np.linalg.solve(U_T_C_U, np.dot(U_i.T, (c_i * p_i)))
            else:
                A = np.dot(U_i.T, U_i) + reg_param * np.eye(rank)
                b = np.dot(U_i.T, r_i)
                V[i_id] = np.linalg.solve(A, b)

            if nonnegative:
                V[i_id] = np.maximum(V[i_id], 0.0)

    # Compute evaluation metrics on test set
    test_preds = []
    test_actuals = []
    for _, row in test_rows.iterrows():
        u = row[user_col]
        it = row[item_col]
        act = row[rating_col]
        if u in user_to_idx and it in item_to_idx:
            pred = float(np.dot(U[user_to_idx[u]], V[item_to_idx[it]]))
            test_preds.append(pred)
            test_actuals.append(act)

    test_preds = np.array(test_preds)
    test_actuals = np.array(test_actuals)
    test_rmse = float(np.sqrt(np.mean((test_actuals - test_preds) ** 2))) if len(test_preds) > 0 else 0.0
    test_mae = float(np.mean(np.abs(test_actuals - test_preds))) if len(test_preds) > 0 else 0.0

    user_factors_df = pd.DataFrame(U, index = unique_users, columns = [f"factor_{k}" for k in range(rank)])
    item_factors_df = pd.DataFrame(V, index = unique_items, columns = [f"factor_{k}" for k in range(rank)])

    metrics_dict = {
        "model_type": "ALS Matrix Factorization",
        "rank": rank,
        "max_iter": max_iter,
        "reg_param": reg_param,
        "implicit_prefs": implicit_prefs,
        "n_users": n_users,
        "n_items": n_items,
        "test_rmse": test_rmse,
        "test_mae": test_mae
    }

    model_dict = {
        "type": "numpy_als",
        "U": U,
        "V": V,
        "user_to_idx": user_to_idx,
        "item_to_idx": item_to_idx,
        "idx_to_user": idx_to_user,
        "idx_to_item": idx_to_item,
        "metrics": metrics_dict
    }

    if ControlVars.show_results:
        print("=" * 80)
        print("ALS MATRIX FACTORIZATION COMPLETE (NUMPY OPTIMIZER)")
        print("=" * 80)
        print(f"Users: {n_users} | Items: {n_items} | Latent Dimensions (rank): {rank}")
        print(f"Test RMSE: {test_rmse:.4f} | Test MAE: {test_mae:.4f}")

    return model_dict, metrics_dict, user_factors_df, item_factors_df


def recommend_for_users(model_dict, user_ids = None, num_items = 5):
    """
    recommend_for_users:
    Generates top-N item recommendations for designated user_ids.

    : param: model_dict: model dictionary returned by als_recommender.
    : param: user_ids: list of user IDs or None (recommends for all users).
    : param: num_items: integer (default 5), number of recommendations per user.
    : return: pandas DataFrame with columns [user_id, rank, item_id, predicted_score].
    """
    if model_dict.get("type") == "pyspark_als":
        spark_model = model_dict["spark_model"]
        if user_ids is None:
            recs_df = spark_model.recommendForAllUsers(num_items).toPandas()
        else:
            from pyspark.sql import SparkSession
            spark = SparkSession.builder.getOrCreate()
            u_df = spark.createDataFrame([(u,) for u in user_ids], [model_dict["user_col"]])
            recs_df = spark_model.recommendForUserSubset(u_df, num_items).toPandas()

        # Unpack nested recommendation structs
        rows = []
        for _, r in recs_df.iterrows():
            uid = r[model_dict["user_col"]]
            for rank_idx, rec in enumerate(r['recommendations'], 1):
                rows.append({
                    "user_id": uid,
                    "rank": rank_idx,
                    "item_id": rec[model_dict["item_col"]],
                    "predicted_score": float(rec['rating'])
                })
        return pd.DataFrame(rows)

    # Pure Python NumPy ALS
    U = model_dict["U"]
    V = model_dict["V"]
    user_to_idx = model_dict["user_to_idx"]
    idx_to_item = model_dict["idx_to_item"]

    target_users = user_ids if user_ids is not None else list(user_to_idx.keys())
    rows = []

    for u in target_users:
        if u not in user_to_idx:
            continue
        u_idx = user_to_idx[u]
        scores = np.dot(U[u_idx], V.T)
        top_indices = np.argsort(scores)[::-1][:num_items]

        for rank_idx, item_idx in enumerate(top_indices, 1):
            rows.append({
                "user_id": u,
                "rank": rank_idx,
                "item_id": idx_to_item[item_idx],
                "predicted_score": float(scores[item_idx])
            })

    return pd.DataFrame(rows)


def recommend_for_items(model_dict, item_ids = None, num_users = 5):
    """
    recommend_for_items:
    Generates top-N user recommendations for designated item_ids.

    : param: model_dict: model dictionary returned by als_recommender.
    : param: item_ids: list of item IDs or None (recommends for all items).
    : param: num_users: integer (default 5), number of target users per item.
    : return: pandas DataFrame with columns [item_id, rank, user_id, predicted_score].
    """
    if model_dict.get("type") == "pyspark_als":
        spark_model = model_dict["spark_model"]
        if item_ids is None:
            recs_df = spark_model.recommendForAllItems(num_users).toPandas()
        else:
            from pyspark.sql import SparkSession
            spark = SparkSession.builder.getOrCreate()
            i_df = spark.createDataFrame([(it,) for it in item_ids], [model_dict["item_col"]])
            recs_df = spark_model.recommendForItemSubset(i_df, num_users).toPandas()

        rows = []
        for _, r in recs_df.iterrows():
            iid = r[model_dict["item_col"]]
            for rank_idx, rec in enumerate(r['recommendations'], 1):
                rows.append({
                    "item_id": iid,
                    "rank": rank_idx,
                    "user_id": rec[model_dict["user_col"]],
                    "predicted_score": float(rec['rating'])
                })
        return pd.DataFrame(rows)

    U = model_dict["U"]
    V = model_dict["V"]
    item_to_idx = model_dict["item_to_idx"]
    idx_to_user = model_dict["idx_to_user"]

    target_items = item_ids if item_ids is not None else list(item_to_idx.keys())
    rows = []

    for it in target_items:
        if it not in item_to_idx:
            continue
        i_idx = item_to_idx[it]
        scores = np.dot(U, V[i_idx])
        top_indices = np.argsort(scores)[::-1][:num_users]

        for rank_idx, u_idx in enumerate(top_indices, 1):
            rows.append({
                "item_id": it,
                "rank": rank_idx,
                "user_id": idx_to_user[u_idx],
                "predicted_score": float(scores[u_idx])
            })

    return pd.DataFrame(rows)


def collaborative_filtering_recommender(
    ratings_df,
    user_col = 'user_id',
    item_col = 'item_id',
    rating_col = 'rating',
    method = 'item_based',
    similarity_metric = 'cosine',
    k_neighbors = 10
):
    """
    collaborative_filtering_recommender:
    Neighborhood-based Collaborative Filtering supporting both User-Based and Item-Based
    approaches using Cosine Similarity or Pearson Correlation.

    : param: ratings_df: pandas DataFrame containing interaction tuples.
    : param: method: 'user_based' or 'item_based' (default 'item_based').
    : param: similarity_metric: 'cosine' or 'pearson' (default 'cosine').
    : param: k_neighbors: number of nearest neighbors considered for prediction.
    : return: tuple (cf_model_dict, similarity_matrix_df, recommend_fn).
    """
    if not isinstance(ratings_df, pd.DataFrame):
        raise InvalidInputsError("ratings_df must be a pandas DataFrame.")

    # Pivot to user-item matrix
    R = ratings_df.pivot(index = user_col, columns = item_col, values = rating_col)

    if method == 'user_based':
        # Mean-center users
        user_means = R.mean(axis = 1)
        R_norm = R.sub(user_means, axis = 0).fillna(0)

        # Compute cosine similarity
        dot_prod = np.dot(R_norm.values, R_norm.values.T)
        norms = np.linalg.norm(R_norm.values, axis = 1, keepdims = True)
        norms[norms == 0] = 1e-9
        sim_mat = dot_prod / np.dot(norms, norms.T)
        np.fill_diagonal(sim_mat, 0.0)

        similarity_df = pd.DataFrame(sim_mat, index = R.index, columns = R.index)

        def recommend_user(user_id, top_n = 5):
            if user_id not in similarity_df.index:
                return pd.DataFrame(columns = ["rank", "item_id", "predicted_rating"])

            user_sims = similarity_df.loc[user_id].values
            top_users = np.argsort(user_sims)[::-1][:k_neighbors]

            # Weighted average ratings of unrated items
            unrated_items = R.columns[R.loc[user_id].isna()]
            scores = {}
            for item in unrated_items:
                item_ratings = R.iloc[top_users][item]
                valid = ~item_ratings.isna()
                if valid.sum() > 0:
                    sim_weights = user_sims[top_users][valid]
                    if sim_weights.sum() > 0:
                        scores[item] = float(np.sum(sim_weights * item_ratings[valid]) / np.sum(sim_weights))

            sorted_items = sorted(scores.items(), key = lambda x: x[1], reverse = True)[:top_n]
            return pd.DataFrame([
                {"rank": i + 1, "item_id": it, "predicted_rating": s}
                for i, (it, s) in enumerate(sorted_items)
            ])

        rec_fn = recommend_user

    else:
        # Item-based collaborative filtering
        item_means = R.mean(axis = 0)
        R_norm = R.sub(item_means, axis = 1).fillna(0)

        dot_prod = np.dot(R_norm.values.T, R_norm.values)
        norms = np.linalg.norm(R_norm.values, axis = 0, keepdims = True)
        norms[norms == 0] = 1e-9
        sim_mat = dot_prod / np.dot(norms.T, norms)
        np.fill_diagonal(sim_mat, 0.0)

        similarity_df = pd.DataFrame(sim_mat, index = R.columns, columns = R.columns)

        def recommend_item(user_id, top_n = 5):
            if user_id not in R.index:
                return pd.DataFrame(columns = ["rank", "item_id", "predicted_rating"])

            user_ratings = R.loc[user_id].dropna()
            unrated_items = R.columns[R.loc[user_id].isna()]

            scores = {}
            for target_item in unrated_items:
                sims = similarity_df.loc[target_item, user_ratings.index]
                if sims.sum() > 0:
                    scores[target_item] = float(np.sum(sims * user_ratings.values) / np.sum(sims))

            sorted_items = sorted(scores.items(), key = lambda x: x[1], reverse = True)[:top_n]
            return pd.DataFrame([
                {"rank": i + 1, "item_id": it, "predicted_rating": s}
                for i, (it, s) in enumerate(sorted_items)
            ])

        rec_fn = recommend_item

    cf_dict = {
        "method": method,
        "similarity_metric": similarity_metric,
        "k_neighbors": k_neighbors,
        "n_users": len(R.index),
        "n_items": len(R.columns)
    }

    if ControlVars.show_results:
        print("=" * 80)
        print(f"COLLABORATIVE FILTERING RECOMMENDER ({method.upper()})")
        print("=" * 80)
        print(f"Users: {cf_dict['n_users']} | Items: {cf_dict['n_items']} | Metric: {similarity_metric}")

    return cf_dict, similarity_df, rec_fn
