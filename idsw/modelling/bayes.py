import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.naive_bayes import (
    GaussianNB,
    MultinomialNB,
    BernoulliNB,
    ComplementNB
)
from sklearn.linear_model import BayesianRidge, ARDRegression, LogisticRegression

from idsw import InvalidInputsError, ControlVars
from .core import ModelChecking


def gaussian_naive_bayes(
    X_train,
    y_train,
    priors = None,
    var_smoothing = 1e-9,
    X_test = None,
    y_test = None,
    X_valid = None,
    y_valid = None,
    column_map_dict = None,
    orientation = 'vertical',
    horizontal_axis_title = None,
    vertical_axis_title = None,
    plot_title = None,
    x_axis_rotation = 70,
    y_axis_rotation = 0,
    grid = True,
    export_png = False,
    directory_to_save = None,
    file_name = None,
    png_resolution_dpi = 330
):
    """
    gaussian_naive_bayes:
    Fits a Gaussian Naive Bayes classifier assuming continuous features follow a normal distribution.

    : param: X_train: training features (DataFrame or array).
    : param: y_train: target labels (Series or array).
    : param: priors: prior probabilities of the classes (array-like, optional).
    : param: var_smoothing: portion of the largest variance of all features added to variances for calculation stability (default 1e-9).
    : return: tuple (model, metrics_dict, feature_importance_df, classes_dict).
    """
    if X_train is None or y_train is None:
        raise InvalidInputsError("X_train and y_train must not be None.")

    y_arr = np.asarray(y_train).ravel()
    X_mat = X_train.copy(deep = True) if isinstance(X_train, pd.DataFrame) else np.asarray(X_train)
    feature_names = list(X_train.columns) if isinstance(X_train, pd.DataFrame) else [f"feature_{i}" for i in range(X_mat.shape[1])]

    # Instantiate GaussianNB
    gnb = GaussianNB(priors = priors, var_smoothing = var_smoothing)
    gnb.fit(X_mat, y_arr)

    # Class info
    classes = list(gnb.classes_)
    classes_dict = {
        "list_of_classes": classes,
        "number_of_classes": len(classes),
        "class_prior": list(gnb.class_prior_),
        "class_count": list(gnb.class_count_)
    }

    y_preds_train = gnb.predict(X_mat)
    y_preds_test = gnb.predict(X_test) if (X_test is not None and y_test is not None) else None
    y_preds_valid = gnb.predict(X_valid) if (X_valid is not None and y_valid is not None) else None

    # Attach pseudo-coefficients based on variance/mean dispersion for ModelChecking compatibility
    feature_variances = np.mean(gnb.var_, axis = 0)
    setattr(gnb, 'coef_', 1.0 / (feature_variances + 1e-6))

    model_check = ModelChecking(
        model_object = gnb,
        model_type = 'classification',
        model_package = 'sklearn',
        column_map_dict = column_map_dict,
        X = X_mat,
        y_train = y_arr,
        y_preds_for_train = y_preds_train,
        y_test = y_test,
        y_preds_for_test = y_preds_test,
        y_valid = y_valid,
        y_preds_for_validation = y_preds_valid
    )
    model_check = model_check.model_metrics()
    metrics_dict = model_check.metrics_dict

    # Feature summary table (mean and variance per class)
    summary_rows = []
    for f_idx, feat in enumerate(feature_names):
        rec = {"feature": feat}
        for c_idx, c_label in enumerate(classes):
            rec[f"mean_class_{c_label}"] = float(gnb.theta_[c_idx, f_idx])
            rec[f"variance_class_{c_label}"] = float(gnb.var_[c_idx, f_idx])
        summary_rows.append(rec)
    feature_summary_df = pd.DataFrame(summary_rows)

    if ControlVars.show_results:
        print("=" * 80)
        print("GAUSSIAN NAIVE BAYES CLASSIFIER")
        print("=" * 80)
        print(f"Number of Classes: {len(classes)} ({classes})")
        print(f"Class Priors: {dict(zip(classes, np.round(gnb.class_prior_, 4)))}")
        print(f"Class Sample Counts: {dict(zip(classes, gnb.class_count_))}")
        print("\nFeature Distribution Summary (Conditional Means and Variances):")
        try:
            from IPython.display import display
            display(feature_summary_df)
        except Exception:
            print(feature_summary_df.to_string())

    return gnb, metrics_dict, feature_summary_df, classes_dict


def multinomial_naive_bayes(
    X_train,
    y_train,
    alpha = 1.0,
    fit_prior = True,
    X_test = None,
    y_test = None,
    X_valid = None,
    y_valid = None,
    column_map_dict = None
):
    """
    multinomial_naive_bayes:
    Fits a Multinomial Naive Bayes classifier suitable for multinomially distributed count data
    (e.g., word occurrences, event frequency counts, discrete process counts).

    : param: X_train: count features (non-negative integers/floats).
    : param: y_train: target labels.
    : param: alpha: additive Laplace/Lidstone smoothing parameter (default 1.0, 0 for no smoothing).
    : param: fit_prior: whether to learn class prior probabilities or use uniform priors (default True).
    : return: tuple (model, metrics_dict, feature_importance_df, classes_dict).
    """
    if X_train is None or y_train is None:
        raise InvalidInputsError("X_train and y_train must not be None.")

    y_arr = np.asarray(y_train).ravel()
    X_mat = X_train.copy(deep = True) if isinstance(X_train, pd.DataFrame) else np.asarray(X_train)

    if np.any(np.asarray(X_mat) < 0):
        raise InvalidInputsError("MultinomialNB requires non-negative feature counts (X >= 0).")

    mnb = MultinomialNB(alpha = alpha, fit_prior = fit_prior)
    mnb.fit(X_mat, y_arr)

    classes = list(mnb.classes_)
    classes_dict = {
        "list_of_classes": classes,
        "number_of_classes": len(classes),
        "class_count": list(mnb.class_count_)
    }

    y_preds_train = mnb.predict(X_mat)
    y_preds_test = mnb.predict(X_test) if (X_test is not None and y_test is not None) else None
    y_preds_valid = mnb.predict(X_valid) if (X_valid is not None and y_valid is not None) else None

    # Expose log probability difference as coef_ for ModelChecking
    if len(classes) == 2:
        setattr(mnb, 'coef_', mnb.feature_log_prob_[1] - mnb.feature_log_prob_[0])
    else:
        setattr(mnb, 'coef_', mnb.feature_log_prob_[0])

    model_check = ModelChecking(
        model_object = mnb,
        model_type = 'classification',
        model_package = 'sklearn',
        column_map_dict = column_map_dict,
        X = X_mat,
        y_train = y_arr,
        y_preds_for_train = y_preds_train,
        y_test = y_test,
        y_preds_for_test = y_preds_test,
        y_valid = y_valid,
        y_preds_for_validation = y_preds_valid
    )
    model_check = model_check.model_metrics()
    metrics_dict = model_check.metrics_dict

    feature_names = list(X_train.columns) if isinstance(X_train, pd.DataFrame) else [f"feature_{i}" for i in range(X_mat.shape[1])]
    feature_df = pd.DataFrame(mnb.feature_log_prob_.T, index = feature_names, columns = [f"log_prob_class_{c}" for c in classes])

    if ControlVars.show_results:
        print("=" * 80)
        print(f"MULTINOMIAL NAIVE BAYES CLASSIFIER (Smoothing alpha = {alpha})")
        print("=" * 80)
        print(f"Classes: {classes}")
        print("\nEmpirical Log Probabilities of Features given Class:")
        try:
            from IPython.display import display
            display(feature_df)
        except Exception:
            print(feature_df.to_string())

    return mnb, metrics_dict, feature_df, classes_dict


def bernoulli_naive_bayes(
    X_train,
    y_train,
    alpha = 1.0,
    binarize = 0.0,
    fit_prior = True,
    X_test = None,
    y_test = None,
    X_valid = None,
    y_valid = None,
    column_map_dict = None
):
    """
    bernoulli_naive_bayes:
    Fits a Naive Bayes classifier for multivariate Bernoulli models (binary/boolean feature vectors).

    : param: X_train: features (binary or continuous thresholded by binarize).
    : param: y_train: target labels.
    : param: alpha: additive Laplace/Lidstone smoothing parameter (default 1.0).
    : param: binarize: threshold for binarizing features (default 0.0). If None, input is assumed already binary.
    : return: tuple (model, metrics_dict, feature_importance_df, classes_dict).
    """
    if X_train is None or y_train is None:
        raise InvalidInputsError("X_train and y_train must not be None.")

    y_arr = np.asarray(y_train).ravel()
    X_mat = X_train.copy(deep = True) if isinstance(X_train, pd.DataFrame) else np.asarray(X_train)

    bnb = BernoulliNB(alpha = alpha, binarize = binarize, fit_prior = fit_prior)
    bnb.fit(X_mat, y_arr)

    classes = list(bnb.classes_)
    classes_dict = {
        "list_of_classes": classes,
        "number_of_classes": len(classes),
        "class_count": list(bnb.class_count_)
    }

    y_preds_train = bnb.predict(X_mat)
    y_preds_test = bnb.predict(X_test) if (X_test is not None and y_test is not None) else None
    y_preds_valid = bnb.predict(X_valid) if (X_valid is not None and y_valid is not None) else None

    if len(classes) == 2:
        setattr(bnb, 'coef_', bnb.feature_log_prob_[1] - bnb.feature_log_prob_[0])
    else:
        setattr(bnb, 'coef_', bnb.feature_log_prob_[0])

    model_check = ModelChecking(
        model_object = bnb,
        model_type = 'classification',
        model_package = 'sklearn',
        column_map_dict = column_map_dict,
        X = X_mat,
        y_train = y_arr,
        y_preds_for_train = y_preds_train,
        y_test = y_test,
        y_preds_for_test = y_preds_test,
        y_valid = y_valid,
        y_preds_for_validation = y_preds_valid
    )
    model_check = model_check.model_metrics()
    metrics_dict = model_check.metrics_dict

    feature_names = list(X_train.columns) if isinstance(X_train, pd.DataFrame) else [f"feature_{i}" for i in range(X_mat.shape[1])]
    feature_df = pd.DataFrame(bnb.feature_log_prob_.T, index = feature_names, columns = [f"log_prob_class_{c}" for c in classes])

    if ControlVars.show_results:
        print("=" * 80)
        print(f"BERNOULLI NAIVE BAYES CLASSIFIER (Binarize Threshold = {binarize})")
        print("=" * 80)
        print(f"Classes: {classes}")

    return bnb, metrics_dict, feature_df, classes_dict


def naive_bayes_classifier(
    X_train,
    y_train,
    algorithm = 'gaussian',
    alpha = 1.0,
    binarize = 0.0,
    X_test = None,
    y_test = None,
    X_valid = None,
    y_valid = None,
    **kwargs
):
    """
    naive_bayes_classifier:
    Unified entry point for Naive Bayes classification algorithms.

    : param: algorithm: string ('gaussian', 'multinomial', 'bernoulli', or 'complement').
    """
    algo = str(algorithm).strip().lower()
    if algo == 'gaussian':
        return gaussian_naive_bayes(X_train, y_train, X_test = X_test, y_test = y_test, X_valid = X_valid, y_valid = y_valid, **kwargs)
    elif algo == 'multinomial':
        return multinomial_naive_bayes(X_train, y_train, alpha = alpha, X_test = X_test, y_test = y_test, X_valid = X_valid, y_valid = y_valid, **kwargs)
    elif algo == 'bernoulli':
        return bernoulli_naive_bayes(X_train, y_train, alpha = alpha, binarize = binarize, X_test = X_test, y_test = y_test, X_valid = X_valid, y_valid = y_valid, **kwargs)
    else:
        raise InvalidInputsError(f"Unsupported Naive Bayes algorithm '{algorithm}'. Choose from: 'gaussian', 'multinomial', 'bernoulli'.")


def bayesian_linear_regression(
    X_train,
    y_train,
    n_iter = 300,
    tol = 1e-3,
    alpha_1 = 1e-6,
    alpha_2 = 1e-6,
    lambda_1 = 1e-6,
    lambda_2 = 1e-6,
    compute_score = True,
    fit_intercept = True,
    ard = False,
    X_test = None,
    y_test = None,
    X_valid = None,
    y_valid = None,
    column_map_dict = None,
    orientation = 'vertical',
    horizontal_axis_title = None,
    vertical_axis_title = None,
    plot_title = None,
    x_axis_rotation = 70,
    y_axis_rotation = 0,
    grid = True,
    export_png = False,
    directory_to_save = None,
    file_name = None,
    png_resolution_dpi = 330
):
    """
    bayesian_linear_regression:
    Fits a Bayesian Ridge Regression or Automatic Relevance Determination (ARD) model.
    Estimates posterior distribution over weights w ~ N(0, alpha^-1 I) with precision lambda ~ Gamma.
    Provides predictive uncertainty (mean and standard deviation) for each forecast.

    : param: ard: boolean (default False). If True, uses ARDRegression with feature-specific precision parameters.
    : return: tuple (model, metrics_dict, feature_importance_df).
    """
    if X_train is None or y_train is None:
        raise InvalidInputsError("X_train and y_train must not be None.")

    y_arr = np.asarray(y_train).ravel()
    X_mat = X_train.copy(deep = True) if isinstance(X_train, pd.DataFrame) else np.asarray(X_train)
    feature_names = list(X_train.columns) if isinstance(X_train, pd.DataFrame) else [f"feature_{i}" for i in range(X_mat.shape[1])]

    if ard:
        bayes_model = ARDRegression(
            max_iter = n_iter,
            tol = tol,
            alpha_1 = alpha_1,
            alpha_2 = alpha_2,
            lambda_1 = lambda_1,
            lambda_2 = lambda_2,
            compute_score = compute_score,
            fit_intercept = fit_intercept
        )
    else:
        bayes_model = BayesianRidge(
            max_iter = n_iter,
            tol = tol,
            alpha_1 = alpha_1,
            alpha_2 = alpha_2,
            lambda_1 = lambda_1,
            lambda_2 = lambda_2,
            compute_score = compute_score,
            fit_intercept = fit_intercept
        )

    bayes_model.fit(X_mat, y_arr)

    y_preds_train = bayes_model.predict(X_mat)
    y_preds_test = bayes_model.predict(X_test) if (X_test is not None and y_test is not None) else None
    y_preds_valid = bayes_model.predict(X_valid) if (X_valid is not None and y_valid is not None) else None

    model_check = ModelChecking(
        model_object = bayes_model,
        model_type = 'regression',
        model_package = 'sklearn',
        column_map_dict = column_map_dict,
        X = X_mat,
        y_train = y_arr,
        y_preds_for_train = y_preds_train,
        y_test = y_test,
        y_preds_for_test = y_preds_test,
        y_valid = y_valid,
        y_preds_for_validation = y_preds_valid
    )
    model_check = model_check.model_metrics()
    metrics_dict = model_check.metrics_dict

    # Add Bayesian-specific attributes to metrics
    metrics_dict["alpha_weight_precision"] = float(bayes_model.alpha_) if hasattr(bayes_model, 'alpha_') and np.isscalar(bayes_model.alpha_) else None
    metrics_dict["lambda_noise_precision"] = float(bayes_model.lambda_) if hasattr(bayes_model, 'lambda_') else None
    metrics_dict["noise_variance_sigma2"] = float(1.0 / bayes_model.alpha_) if hasattr(bayes_model, 'alpha_') and np.isscalar(bayes_model.alpha_) else None

    # Feature importance ranking
    model_check = model_check.feature_importance_ranking(
        model_class = 'linear',
        orientation = orientation,
        horizontal_axis_title = horizontal_axis_title,
        vertical_axis_title = vertical_axis_title,
        plot_title = plot_title if plot_title is not None else "Bayesian Linear Regression Feature Weights",
        x_axis_rotation = x_axis_rotation,
        y_axis_rotation = y_axis_rotation,
        grid = grid,
        export_png = export_png,
        directory_to_save = directory_to_save,
        file_name = file_name,
        png_resolution_dpi = png_resolution_dpi
    )
    feature_importance_df = model_check.feature_importance_df

    if ControlVars.show_results:
        print("=" * 80)
        algo_name = "AUTOMATIC RELEVANCE DETERMINATION (ARD)" if ard else "BAYESIAN RIDGE REGRESSION"
        print(f"{algo_name} COMPLETED")
        print("=" * 80)
        if hasattr(bayes_model, 'alpha_') and np.isscalar(bayes_model.alpha_):
            print(f"Estimated Noise Precision (alpha): {bayes_model.alpha_:.4e} (sigma = {1.0 / np.sqrt(bayes_model.alpha_):.4f})")
        if hasattr(bayes_model, 'lambda_'):
            print(f"Estimated Weight Precision (lambda): {bayes_model.lambda_:.4e}")
        print("\nNote: Predict with uncertainty via: y_mean, y_std = model.predict(X, return_std=True)")

    return bayes_model, metrics_dict, feature_importance_df


def bayesian_logistic_regression(
    X_train,
    y_train,
    prior_variance = 1.0,
    max_iter = 2000,
    tol = 1e-4,
    random_state = 42,
    X_test = None,
    y_test = None,
    X_valid = None,
    y_valid = None,
    column_map_dict = None,
    orientation = 'vertical',
    horizontal_axis_title = None,
    vertical_axis_title = None,
    plot_title = None,
    x_axis_rotation = 70,
    y_axis_rotation = 0,
    grid = True,
    export_png = False,
    directory_to_save = None,
    file_name = None,
    png_resolution_dpi = 330
):
    """
    bayesian_logistic_regression:
    Fits Bayesian Logistic Regression using Gaussian prior on weights w ~ N(0, prior_variance * I),
    which corresponds to L2 MAP penalization with C = prior_variance.
    Provides calibrated posterior probabilities via predict_proba.

    : param: prior_variance: float (default 1.0), variance of the zero-mean Gaussian prior over weights.
    : return: tuple (model, metrics_dict, feature_importance_df, classes_dict).
    """
    if X_train is None or y_train is None:
        raise InvalidInputsError("X_train and y_train must not be None.")

    y_arr = np.asarray(y_train).ravel()
    X_mat = X_train.copy(deep = True) if isinstance(X_train, pd.DataFrame) else np.asarray(X_train)

    bayes_logit = LogisticRegression(
        penalty = 'l2',
        C = float(prior_variance),
        max_iter = max_iter,
        tol = tol,
        random_state = random_state,
        solver = 'lbfgs'
    )
    bayes_logit.fit(X_mat, y_arr)

    classes = list(bayes_logit.classes_)
    classes_dict = {
        "list_of_classes": classes,
        "number_of_classes": len(classes)
    }

    y_preds_train = bayes_logit.predict(X_mat)
    y_preds_test = bayes_logit.predict(X_test) if (X_test is not None and y_test is not None) else None
    y_preds_valid = bayes_logit.predict(X_valid) if (X_valid is not None and y_valid is not None) else None

    model_check = ModelChecking(
        model_object = bayes_logit,
        model_type = 'classification',
        model_package = 'sklearn',
        column_map_dict = column_map_dict,
        X = X_mat,
        y_train = y_arr,
        y_preds_for_train = y_preds_train,
        y_test = y_test,
        y_preds_for_test = y_preds_test,
        y_valid = y_valid,
        y_preds_for_validation = y_preds_valid
    )
    model_check = model_check.model_metrics()
    metrics_dict = model_check.metrics_dict

    model_check = model_check.feature_importance_ranking(
        model_class = 'linear',
        orientation = orientation,
        horizontal_axis_title = horizontal_axis_title,
        vertical_axis_title = vertical_axis_title,
        plot_title = plot_title if plot_title is not None else "Bayesian Logistic Regression MAP Coefficients",
        x_axis_rotation = x_axis_rotation,
        y_axis_rotation = y_axis_rotation,
        grid = grid,
        export_png = export_png,
        directory_to_save = directory_to_save,
        file_name = file_name,
        png_resolution_dpi = png_resolution_dpi
    )
    feature_importance_df = model_check.feature_importance_df

    if ControlVars.show_results:
        print("=" * 80)
        print("BAYESIAN LOGISTIC REGRESSION (GAUSSIAN MAP PRIOR)")
        print("=" * 80)
        print(f"Classes: {classes}")
        print(f"Prior Variance on Weights: {prior_variance}")
        print("Obtain class probabilities via: probs = model.predict_proba(X)")

    return bayes_logit, metrics_dict, feature_importance_df, classes_dict


def bayesian_model(
    X_train,
    y_train,
    model_type = 'regression',
    algorithm = 'ridge',
    X_test = None,
    y_test = None,
    X_valid = None,
    y_valid = None,
    **kwargs
):
    """
    bayesian_model:
    Unified interface for Bayesian machine learning models supporting both regression and classification.

    : param: model_type: 'regression' or 'classification'.
    : param: algorithm:
      - for regression: 'ridge' (Bayesian Ridge) or 'ard' (Automatic Relevance Determination).
      - for classification: 'gaussian' (Gaussian NB), 'multinomial' (Multinomial NB),
                            'bernoulli' (Bernoulli NB), or 'logistic' (Bayesian Logistic Regression).
    """
    m_type = str(model_type).strip().lower()
    algo = str(algorithm).strip().lower()

    if m_type == 'regression':
        ard_flag = (algo == 'ard')
        return bayesian_linear_regression(
            X_train, y_train, ard = ard_flag,
            X_test = X_test, y_test = y_test,
            X_valid = X_valid, y_valid = y_valid,
            **kwargs
        )
    elif m_type == 'classification':
        if algo == 'logistic':
            return bayesian_logistic_regression(
                X_train, y_train,
                X_test = X_test, y_test = y_test,
                X_valid = X_valid, y_valid = y_valid,
                **kwargs
            )
        else:
            return naive_bayes_classifier(
                X_train, y_train,
                algorithm = algo,
                X_test = X_test, y_test = y_test,
                X_valid = X_valid, y_valid = y_valid,
                **kwargs
            )
    else:
        raise InvalidInputsError(f"model_type must be either 'regression' or 'classification', got '{model_type}'.")
