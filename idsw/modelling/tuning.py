import time
import copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.base import clone, is_classifier, is_regressor
from sklearn.model_selection import (
    GridSearchCV,
    RandomizedSearchCV,
    cross_val_score,
    KFold,
    StratifiedKFold
)

from idsw import InvalidInputsError, ControlVars


def _extract_estimator(model_object):
    """Helper to extract an unfitted or cloned scikit-learn compatible estimator."""
    if isinstance(model_object, tuple):
        model_object = model_object[0]

    if hasattr(model_object, "fit") and hasattr(model_object, "predict"):
        try:
            return clone(model_object)
        except Exception:
            return model_object

    raise InvalidInputsError(
        f"Invalid model_object of type {type(model_object)}. Expected an estimator supporting .fit() and .predict()."
    )


def grid_search_tuning(
    model_object,
    param_grid,
    X_train,
    y_train,
    scoring = None,
    cv = 5,
    n_jobs = -1,
    refit = True,
    X_test = None,
    y_test = None,
    show_top_n = 10,
    plot_results = True,
    orientation = 'vertical',
    x_axis_rotation = 70,
    y_axis_rotation = 0,
    grid = True,
    export_png = False,
    directory_to_save = None,
    file_name = None,
    png_resolution_dpi = 330
):
    """
    grid_search_tuning:
    Exhaustively searches over specified parameter values for an IDSW estimator.

    : param: model_object: scikit-learn / XGBoost model or tuple returned by an IDSW model training function.
    : param: param_grid: dictionary or list of dictionaries with parameters names (str) as keys and lists of parameter settings to try as values.
    : param: X_train: features matrix for training (DataFrame or ndarray).
    : param: y_train: target response values for training (Series or ndarray).
    : param: scoring: strategy to evaluate performance (e.g. 'r2', 'neg_mean_squared_error', 'accuracy', 'f1', 'roc_auc').
    : param: cv: integer, cross-validation generator or an iterable determining the cross-validation splitting strategy (default 5).
    : param: n_jobs: number of jobs to run in parallel (default -1 uses all available cores).
    : param: refit: boolean (default True), whether to refit the best estimator on the whole dataset.
    : param: X_test: optional test features for validation.
    : param: y_test: optional test targets for validation.
    : param: show_top_n: integer (default 10), number of top candidates to display.
    : return: tuple (best_estimator, best_params_dict, results_df).
    """
    estimator = _extract_estimator(model_object)

    if not isinstance(param_grid, (dict, list)):
        raise InvalidInputsError("param_grid must be a dictionary or list of dictionaries.")

    y_arr = np.asarray(y_train).ravel()
    X_mat = X_train.copy(deep = True) if isinstance(X_train, pd.DataFrame) else np.asarray(X_train)

    start_time = time.time()
    grid_search = GridSearchCV(
        estimator = estimator,
        param_grid = param_grid,
        scoring = scoring,
        cv = cv,
        n_jobs = n_jobs,
        refit = refit,
        return_train_score = True
    )
    grid_search.fit(X_mat, y_arr)
    elapsed_time = time.time() - start_time

    best_estimator = grid_search.best_estimator_
    best_params = grid_search.best_params_
    best_score = float(grid_search.best_score_)

    results_df = pd.DataFrame(grid_search.cv_results_)
    sort_col = 'rank_test_score' if 'rank_test_score' in results_df.columns else 'mean_test_score'
    results_df = results_df.sort_values(by = sort_col, ascending = True).reset_index(drop = True)

    test_score = None
    if X_test is not None and y_test is not None and refit:
        X_test_mat = X_test.copy(deep = True) if isinstance(X_test, pd.DataFrame) else np.asarray(X_test)
        y_test_arr = np.asarray(y_test).ravel()
        test_score = float(best_estimator.score(X_test_mat, y_test_arr))

    if ControlVars.show_results:
        print("=" * 80)
        print("GRID SEARCH HYPERPARAMETER TUNING COMPLETED")
        print("=" * 80)
        print(f"Elapsed Time: {elapsed_time:.2f} seconds")
        print(f"Total Combinations Evaluated: {len(results_df)}")
        print(f"Best CV Score ({scoring or 'default metric'}): {best_score:.4f}")
        if test_score is not None:
            print(f"Holdout Test Score: {test_score:.4f}")
        print("\nOptimal Hyperparameters:")
        for k, v in best_params.items():
            print(f"  - {k}: {v}")

        print(f"\nTop {min(show_top_n, len(results_df))} Parameter Configurations:")
        display_cols = [c for c in ['rank_test_score', 'mean_test_score', 'std_test_score', 'mean_train_score', 'params'] if c in results_df.columns]
        top_df = results_df[display_cols].head(show_top_n)
        try:
            from IPython.display import display
            display(top_df)
        except Exception:
            print(top_df.to_string())

    if ControlVars.show_plots and plot_results and len(results_df) > 1:
        fig, ax = plt.subplots(figsize = (10, 5))
        plot_scores = results_df['mean_test_score'].values
        ax.plot(range(1, len(plot_scores) + 1), plot_scores, marker = 'o', color = 'royalblue', linewidth = 1.5, markersize = 4)
        ax.axhline(best_score, color = 'crimson', linestyle = '--', label = f'Best Score ({best_score:.4f})')
        ax.set_title("Grid Search Model Evaluation Across Candidate Ranks")
        ax.set_xlabel("Candidate Rank (Best to Worst)")
        ax.set_ylabel(f"Mean CV Score ({scoring or 'metric'})")
        ax.grid(grid)
        ax.legend(loc = 'upper right')

        if export_png:
            import os
            if directory_to_save is None:
                directory_to_save = ""
            if file_name is None:
                file_name = "grid_search_scores"
            new_file_path = os.path.join(directory_to_save, file_name + ".png")
            plt.savefig(new_file_path, dpi = png_resolution_dpi, bbox_inches = 'tight')
            if ControlVars.show_results:
                print(f"Plot saved to '{new_file_path}'.")

        plt.show()

    return best_estimator, best_params, results_df


def random_search_tuning(
    model_object,
    param_distributions,
    X_train,
    y_train,
    n_iter = 50,
    scoring = None,
    cv = 5,
    random_state = 42,
    n_jobs = -1,
    refit = True,
    X_test = None,
    y_test = None,
    show_top_n = 10,
    plot_results = True,
    grid = True,
    export_png = False,
    directory_to_save = None,
    file_name = None,
    png_resolution_dpi = 330
):
    """
    random_search_tuning:
    Randomized search on hyperparameters for an IDSW estimator.
    Samples a given number of candidates from a parameter space with a specified distribution.

    : param: model_object: estimator or tuple returned by an IDSW model training function.
    : param: param_distributions: dict with parameters names as keys and distributions or lists of parameters to try.
    : param: n_iter: integer (default 50), number of parameter settings that are sampled.
    : return: tuple (best_estimator, best_params_dict, results_df).
    """
    estimator = _extract_estimator(model_object)

    if not isinstance(param_distributions, dict):
        raise InvalidInputsError("param_distributions must be a dictionary.")

    y_arr = np.asarray(y_train).ravel()
    X_mat = X_train.copy(deep = True) if isinstance(X_train, pd.DataFrame) else np.asarray(X_train)

    start_time = time.time()
    random_search = RandomizedSearchCV(
        estimator = estimator,
        param_distributions = param_distributions,
        n_iter = n_iter,
        scoring = scoring,
        cv = cv,
        random_state = random_state,
        n_jobs = n_jobs,
        refit = refit,
        return_train_score = True
    )
    random_search.fit(X_mat, y_arr)
    elapsed_time = time.time() - start_time

    best_estimator = random_search.best_estimator_
    best_params = random_search.best_params_
    best_score = float(random_search.best_score_)

    results_df = pd.DataFrame(random_search.cv_results_)
    sort_col = 'rank_test_score' if 'rank_test_score' in results_df.columns else 'mean_test_score'
    results_df = results_df.sort_values(by = sort_col, ascending = True).reset_index(drop = True)

    test_score = None
    if X_test is not None and y_test is not None and refit:
        X_test_mat = X_test.copy(deep = True) if isinstance(X_test, pd.DataFrame) else np.asarray(X_test)
        y_test_arr = np.asarray(y_test).ravel()
        test_score = float(best_estimator.score(X_test_mat, y_test_arr))

    if ControlVars.show_results:
        print("=" * 80)
        print("RANDOM SEARCH HYPERPARAMETER TUNING COMPLETED")
        print("=" * 80)
        print(f"Elapsed Time: {elapsed_time:.2f} seconds")
        print(f"Total Iterations Evaluated: {len(results_df)}")
        print(f"Best CV Score ({scoring or 'default metric'}): {best_score:.4f}")
        if test_score is not None:
            print(f"Holdout Test Score: {test_score:.4f}")
        print("\nOptimal Hyperparameters:")
        for k, v in best_params.items():
            print(f"  - {k}: {v}")

        print(f"\nTop {min(show_top_n, len(results_df))} Parameter Configurations:")
        display_cols = [c for c in ['rank_test_score', 'mean_test_score', 'std_test_score', 'mean_train_score', 'params'] if c in results_df.columns]
        top_df = results_df[display_cols].head(show_top_n)
        try:
            from IPython.display import display
            display(top_df)
        except Exception:
            print(top_df.to_string())

    if ControlVars.show_plots and plot_results and len(results_df) > 1:
        fig, ax = plt.subplots(figsize = (10, 5))
        plot_scores = results_df['mean_test_score'].values
        ax.plot(range(1, len(plot_scores) + 1), plot_scores, marker = 's', color = 'darkorange', linewidth = 1.5, markersize = 4)
        ax.axhline(best_score, color = 'darkgreen', linestyle = '--', label = f'Best Score ({best_score:.4f})')
        ax.set_title("Random Search Model Performance Distribution")
        ax.set_xlabel("Candidate Rank (Best to Worst)")
        ax.set_ylabel(f"Mean CV Score ({scoring or 'metric'})")
        ax.grid(grid)
        ax.legend(loc = 'upper right')

        if export_png:
            import os
            if directory_to_save is None:
                directory_to_save = ""
            if file_name is None:
                file_name = "random_search_scores"
            new_file_path = os.path.join(directory_to_save, file_name + ".png")
            plt.savefig(new_file_path, dpi = png_resolution_dpi, bbox_inches = 'tight')

        plt.show()

    return best_estimator, best_params, results_df


def coarse_to_fine_tuning(
    model_object,
    broad_param_distributions,
    X_train,
    y_train,
    coarse_iterations = 30,
    top_candidates_to_refine = 3,
    refine_steps = 3,
    scoring = None,
    cv = 5,
    random_state = 42,
    n_jobs = -1,
    X_test = None,
    y_test = None
):
    """
    coarse_to_fine_tuning:
    Implements informed hyperparameter optimization via multi-stage Coarse-to-Fine search.
    Stage 1 (Coarse): Explores a wide parameter space using randomized search.
    Stage 2 (Fine): Identifies promising regions and builds a dense localized grid around top performers.

    : param: model_object: IDSW model or estimator.
    : param: broad_param_distributions: wide bounds dictionary for initial coarse random exploration.
    : param: coarse_iterations: number of iterations for the coarse search stage (default 30).
    : param: top_candidates_to_refine: number of top performing hyperparameter zones to isolate (default 3).
    : param: refine_steps: number of fine-grained candidate variations generated around each best parameter (default 3).
    : return: tuple (best_estimator, best_params_dict, summary_dict).
    """
    estimator = _extract_estimator(model_object)

    if ControlVars.show_results:
        print("=" * 80)
        print("STAGE 1: COARSE SEARCH - BROAD RANDOM EXPLORATION")
        print("=" * 80)

    # Stage 1: Coarse random search
    coarse_model, coarse_best_params, coarse_results = random_search_tuning(
        model_object = estimator,
        param_distributions = broad_param_distributions,
        X_train = X_train,
        y_train = y_train,
        n_iter = coarse_iterations,
        scoring = scoring,
        cv = cv,
        random_state = random_state,
        n_jobs = n_jobs,
        plot_results = False
    )

    # Extract top N distinct hyperparameter configurations
    top_rows = coarse_results.head(top_candidates_to_refine)

    if ControlVars.show_results:
        print("\n" + "=" * 80)
        print("STAGE 2: FINE SEARCH - DENSE LOCALIZED GRID SEARCH AROUND PROMISING REGIONS")
        print("=" * 80)

    # Construct refined localized grid around top candidates
    refined_grid = {}
    for param_name in broad_param_distributions.keys():
        observed_vals = []
        for p_dict in top_rows['params']:
            if param_name in p_dict:
                observed_vals.append(p_dict[param_name])

        if len(observed_vals) == 0:
            continue

        first_val = observed_vals[0]
        if isinstance(first_val, (int, np.integer)):
            min_v = max(1, int(min(observed_vals) * 0.8))
            max_v = int(max(observed_vals) * 1.2) + 1
            refined_grid[param_name] = sorted(list(set(np.linspace(min_v, max_v, refine_steps + 2, dtype = int))))
        elif isinstance(first_val, (float, np.floating)):
            min_v = float(min(observed_vals) * 0.8)
            max_v = float(max(observed_vals) * 1.2)
            refined_grid[param_name] = sorted(list(set(np.round(np.linspace(min_v, max_v, refine_steps + 2), 5))))
        else:
            # Categorical / string
            refined_grid[param_name] = list(set(observed_vals))

    if ControlVars.show_results:
        print("Refined parameter space generated:")
        for k, v in refined_grid.items():
            print(f"  - {k}: {v}")

    fine_model, fine_best_params, fine_results = grid_search_tuning(
        model_object = estimator,
        param_grid = refined_grid,
        X_train = X_train,
        y_train = y_train,
        scoring = scoring,
        cv = cv,
        n_jobs = n_jobs,
        X_test = X_test,
        y_test = y_test,
        plot_results = True
    )

    summary_dict = {
        "coarse_best_params": coarse_best_params,
        "coarse_best_score": float(coarse_results['mean_test_score'].iloc[0]),
        "fine_best_params": fine_best_params,
        "fine_best_score": float(fine_results['mean_test_score'].iloc[0]),
        "coarse_results_df": coarse_results,
        "fine_results_df": fine_results
    }

    if ControlVars.show_results:
        print("\n" + "=" * 80)
        print("COARSE-TO-FINE OPTIMIZATION SUMMARY")
        print("=" * 80)
        print(f"Coarse Stage Best Score: {summary_dict['coarse_best_score']:.4f}")
        print(f"Fine Stage Best Score:   {summary_dict['fine_best_score']:.4f}")
        gain = summary_dict['fine_best_score'] - summary_dict['coarse_best_score']
        print(f"Performance Improvement: {gain:+.4f}\n")

    return fine_model, fine_best_params, summary_dict


def bayesian_optimization_tuning(
    model_object,
    param_space,
    X_train,
    y_train,
    n_iterations = 25,
    n_initial_points = 5,
    scoring = None,
    cv = 5,
    random_state = 42,
    X_test = None,
    y_test = None,
    plot_convergence = True,
    grid = True,
    export_png = False,
    directory_to_save = None,
    file_name = None,
    png_resolution_dpi = 330
):
    """
    bayesian_optimization_tuning:
    Performs informed Bayesian Hyperparameter Optimization using Gaussian Process surrogate
    modeling and Upper Confidence Bound (UCB) / Expected Improvement acquisition strategy.
    Sequentially builds belief posterior from past trial evidence to choose next optimal evaluation points.

    : param: model_object: IDSW estimator or training function output.
    : param: param_space: dict defining search ranges.
              Supported formats per parameter:
              - tuple (low, high, 'int'): integer bounds.
              - tuple (low, high, 'float'): continuous floating-point bounds.
              - list [val1, val2, ...]: discrete or categorical options.
    : param: n_iterations: total sequential Bayesian optimization steps (default 25).
    : param: n_initial_points: number of random initial evaluations prior to surrogate fitting (default 5).
    : return: tuple (best_estimator, best_params_dict, history_df).
    """
    estimator = _extract_estimator(model_object)
    rng = np.random.RandomState(random_state)

    y_arr = np.asarray(y_train).ravel()
    X_mat = X_train.copy(deep = True) if isinstance(X_train, pd.DataFrame) else np.asarray(X_train)

    # Function to sample a single random hyperparameter configuration
    def _sample_random_config():
        config = {}
        for p_name, p_def in param_space.items():
            if isinstance(p_def, tuple) and len(p_def) == 3:
                low, high, p_type = p_def
                if p_type == 'int':
                    config[p_name] = int(rng.randint(low, high + 1))
                else:
                    config[p_name] = float(rng.uniform(low, high))
            elif isinstance(p_def, (list, tuple)):
                idx = rng.randint(0, len(p_def))
                config[p_name] = p_def[idx]
            else:
                config[p_name] = p_def
        return config

    # Evaluates candidate config with cross-validation
    def _evaluate_config(config):
        cand = clone(estimator)
        cand.set_params(**config)
        scores = cross_val_score(cand, X_mat, y_arr, cv = cv, scoring = scoring)
        return float(np.mean(scores))

    history_records = []
    best_score = -float('inf')
    best_config = None

    if ControlVars.show_results:
        print("=" * 80)
        print("BAYESIAN HYPERPARAMETER OPTIMIZATION (GAUSSIAN PROCESS SURROGATE)")
        print("=" * 80)

    # Try importing GaussianProcessRegressor for surrogate model
    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.gaussian_process.kernels import Matern

    gp = GaussianProcessRegressor(
        kernel = Matern(nu = 2.5),
        alpha = 1e-4,
        normalize_y = True,
        random_state = random_state
    )

    numeric_params = [k for k, v in param_space.items() if isinstance(v, tuple) and len(v) == 3]

    for iteration in range(1, n_iterations + 1):
        if iteration <= n_initial_points or len(numeric_params) == 0:
            config = _sample_random_config()
        else:
            # Informed candidate generation via surrogate prediction and UCB
            X_hist = []
            y_hist = []
            for rec in history_records:
                X_hist.append([rec[k] for k in numeric_params])
                y_hist.append(rec['score'])

            X_hist = np.array(X_hist)
            y_hist = np.array(y_hist)

            try:
                gp.fit(X_hist, y_hist)

                # Generate 100 candidate samples and select max acquisition score (UCB)
                candidates = [_sample_random_config() for _ in range(100)]
                X_cand = np.array([[c[k] for k in numeric_params] for c in candidates])
                mu, sigma = gp.predict(X_cand, return_std = True)
                kappa = 1.96  # 95% exploration bonus
                acquisition = mu + kappa * sigma
                best_cand_idx = int(np.argmax(acquisition))
                config = candidates[best_cand_idx]
            except Exception:
                config = _sample_random_config()

        score = _evaluate_config(config)

        if score > best_score:
            best_score = score
            best_config = copy.deepcopy(config)

        rec = copy.deepcopy(config)
        rec['iteration'] = iteration
        rec['score'] = score
        rec['best_score_so_far'] = best_score
        history_records.append(rec)

        if ControlVars.show_results and (iteration % 5 == 0 or iteration == n_iterations):
            print(f"Iteration {iteration:02d}/{n_iterations:02d} | Current Score: {score:.4f} | Best So Far: {best_score:.4f}")

    # Refit best estimator on entire dataset
    best_estimator = clone(estimator)
    best_estimator.set_params(**best_config)
    best_estimator.fit(X_mat, y_arr)

    history_df = pd.DataFrame(history_records)

    test_score = None
    if X_test is not None and y_test is not None:
        X_test_mat = X_test.copy(deep = True) if isinstance(X_test, pd.DataFrame) else np.asarray(X_test)
        y_test_arr = np.asarray(y_test).ravel()
        test_score = float(best_estimator.score(X_test_mat, y_test_arr))

    if ControlVars.show_results:
        print("\n" + "=" * 80)
        print("BAYESIAN OPTIMIZATION CONVERGED")
        print("=" * 80)
        print(f"Total Trials: {n_iterations}")
        print(f"Optimal Score ({scoring or 'metric'}): {best_score:.4f}")
        if test_score is not None:
            print(f"Holdout Test Score: {test_score:.4f}")
        print("\nOptimal Hyperparameters:")
        for k, v in best_config.items():
            print(f"  - {k}: {v}")

    if ControlVars.show_plots and plot_convergence:
        fig, ax = plt.subplots(figsize = (10, 5))
        ax.plot(history_df['iteration'], history_df['score'], marker = 'o', color = 'lightsteelblue', alpha = 0.7, label = 'Trial Score')
        ax.plot(history_df['iteration'], history_df['best_score_so_far'], marker = 's', color = 'navy', linewidth = 2, label = 'Best Score (Bayesian UCB)')
        ax.set_title("Bayesian Optimization Convergence History")
        ax.set_xlabel("Trial Iteration")
        ax.set_ylabel(f"CV Score ({scoring or 'metric'})")
        ax.grid(grid)
        ax.legend(loc = 'lower right')

        if export_png:
            import os
            if directory_to_save is None:
                directory_to_save = ""
            if file_name is None:
                file_name = "bayesian_opt_convergence"
            new_file_path = os.path.join(directory_to_save, file_name + ".png")
            plt.savefig(new_file_path, dpi = png_resolution_dpi, bbox_inches = 'tight')

        plt.show()

    return best_estimator, best_config, history_df


def genetic_algorithm_tuning(
    model_object,
    param_space,
    X_train,
    y_train,
    population_size = 15,
    generations = 5,
    mutation_rate = 0.15,
    crossover_rate = 0.8,
    scoring = None,
    cv = 5,
    random_state = 42,
    X_test = None,
    y_test = None
):
    """
    genetic_algorithm_tuning:
    Evolutionary hyperparameter tuning based on natural selection, crossover, and mutation principles.
    Refines a population of hyperparameter chromosomes across generations towards global optimum.

    : param: model_object: IDSW estimator.
    : param: param_space: dict of hyperparameter choices or (low, high, 'int'/'float') ranges.
    : param: population_size: number of individuals in each generation (default 15).
    : param: generations: number of evolutionary cycles (default 5).
    : param: mutation_rate: probability of random gene mutation (default 0.15).
    : param: crossover_rate: probability of chromosome mating/crossover (default 0.8).
    : return: tuple (best_estimator, best_params_dict, history_df).
    """
    estimator = _extract_estimator(model_object)
    rng = np.random.RandomState(random_state)

    y_arr = np.asarray(y_train).ravel()
    X_mat = X_train.copy(deep = True) if isinstance(X_train, pd.DataFrame) else np.asarray(X_train)

    def _sample_gene(p_name):
        p_def = param_space[p_name]
        if isinstance(p_def, tuple) and len(p_def) == 3:
            low, high, p_type = p_def
            if p_type == 'int':
                return int(rng.randint(low, high + 1))
            return float(rng.uniform(low, high))
        elif isinstance(p_def, (list, tuple)):
            return p_def[rng.randint(0, len(p_def))]
        return p_def

    def _sample_individual():
        return {k: _sample_gene(k) for k in param_space.keys()}

    def _evaluate(indiv):
        cand = clone(estimator)
        cand.set_params(**indiv)
        scores = cross_val_score(cand, X_mat, y_arr, cv = cv, scoring = scoring)
        return float(np.mean(scores))

    # Initialize population
    population = [_sample_individual() for _ in range(population_size)]
    history = []

    best_individual = None
    best_fitness = -float('inf')

    if ControlVars.show_results:
        print("=" * 80)
        print("GENETIC ALGORITHM HYPERPARAMETER OPTIMIZATION (EVOLUTIONARY)")
        print("=" * 80)

    for gen in range(1, generations + 1):
        fitnesses = [_evaluate(ind) for ind in population]

        for ind, fit in zip(population, fitnesses):
            if fit > best_fitness:
                best_fitness = fit
                best_individual = copy.deepcopy(ind)

            rec = copy.deepcopy(ind)
            rec['generation'] = gen
            rec['fitness'] = fit
            rec['best_fitness'] = best_fitness
            history.append(rec)

        mean_fit = float(np.mean(fitnesses))
        max_fit = float(np.max(fitnesses))

        if ControlVars.show_results:
            print(f"Generation {gen}/{generations} | Population Mean Fitness: {mean_fit:.4f} | Peak Fitness: {max_fit:.4f}")

        # Elite individual carries forward intact
        elite_idx = int(np.argmax(fitnesses))
        new_population = [copy.deepcopy(population[elite_idx])]

        # Selection (tournament of size 2) and Crossover
        while len(new_population) < population_size:
            # Tournament selection for parent 1
            i1, i2 = rng.randint(0, population_size, 2)
            p1 = population[i1] if fitnesses[i1] > fitnesses[i2] else population[i2]

            # Tournament selection for parent 2
            i3, i4 = rng.randint(0, population_size, 2)
            p2 = population[i3] if fitnesses[i3] > fitnesses[i4] else population[i4]

            # Crossover
            offspring = {}
            for gene in param_space.keys():
                if rng.rand() < crossover_rate:
                    offspring[gene] = p1[gene] if rng.rand() < 0.5 else p2[gene]
                else:
                    offspring[gene] = p1[gene]

            # Mutation
            for gene in param_space.keys():
                if rng.rand() < mutation_rate:
                    offspring[gene] = _sample_gene(gene)

            new_population.append(offspring)

        population = new_population

    best_estimator = clone(estimator)
    best_estimator.set_params(**best_individual)
    best_estimator.fit(X_mat, y_arr)

    history_df = pd.DataFrame(history)

    if ControlVars.show_results:
        print("\n" + "=" * 80)
        print("GENETIC OPTIMIZATION COMPLETE")
        print("=" * 80)
        print(f"Optimal Fitness ({scoring or 'metric'}): {best_fitness:.4f}")
        print("Best evolved chromosomes:")
        for k, v in best_individual.items():
            print(f"  - {k}: {v}")

    return best_estimator, best_individual, history_df
