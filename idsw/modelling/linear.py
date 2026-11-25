import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf

from idsw import (InvalidInputsError, ControlVars)
from .core import ModelChecking


def ols_linear_reg (X_train, y_train, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    ols_linear_reg (X_train, y_train, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    check Scikit-learn documentation: 
      https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html?msclkid=636b4046c01b11ec973dee34641f67b0
    
    This function runs the 'bar_chart' function.
    
    
    : param: X_train = subset of predictive variables (dataframe).
    : param: y_train = subset of response variable (series).
    """
    
    from sklearn.linear_model import LinearRegression
    
    # Create an instance (object) from the class LinearRegression:
    # There is no parameter to pass to the constructor of this class:
    ols_linear_reg_model = LinearRegression()
    
    # Sklearn requires a 1-dimensional vector for training the classifier.
    """
            y_train tensor original format:
                <tf.Tensor: shape=(87, 1), dtype=float64, numpy=
                array([[1.],
                    [0.], ....,
                    [0.]])>
            
            Reshape to unidimensional format. First step:
            y_train.numpy().reshape(1, -1)
            Now, it has format:
                array([[1., 0.,..., 0.]]), shape = (1, 87)
                (if we make reshape(-1, 1), we turn it again to the original tensor format)
            
            Notice that we want only the internal 1-dimensional array (with 87 values in the example)
            # So we make:
            y_train[0] to select only it.
    """
            
    y_train = np.array(y_train).reshape(1, -1)
    # This array has format([[val1, val2, ...]]) - i.e., it has two dimensions. Let's pick
    # only the first array:
    y_train = y_train[0]
    
    # Fit the model:
    ols_linear_reg_model = ols_linear_reg_model.fit(X_train, y_train)
    
    # Get predictions for training, testing, and validation:
    y_preds_for_train = ols_linear_reg_model.predict(X_train)
    
    if ((X_test is not None) & ((y_test is not None))):
        y_preds_for_test = ols_linear_reg_model.predict(X_test)
    
    else:
        y_preds_for_test = None
    
    if ((X_valid is not None) & ((y_valid is not None))):
        y_preds_for_validation = ols_linear_reg_model.predict(X_valid)
    
    else:
        y_preds_for_validation = None
    
    # instantiate the model checker object:
    model_check = ModelChecking(model_object = ols_linear_reg_model, model_type = 'regression', model_package = 'sklearn', column_map_dict = column_map_dict, X = X_train, y_train = y_train, y_preds_for_train = y_preds_for_train, y_test = y_test, y_preds_for_test = y_preds_for_test, y_valid = y_valid, y_preds_for_validation = y_preds_for_validation)
    
    # Calculate model metrics:
    model_check = model_check.model_metrics()
    # Retrieve model metrics:
    metrics_dict = model_check.metrics_dict
    
    # Get feature importance ranking:
    model_check = model_check.feature_importance_ranking (model_class = 'linear', orientation = orientation, horizontal_axis_title = horizontal_axis_title, vertical_axis_title = vertical_axis_title, plot_title = plot_title, x_axis_rotation = x_axis_rotation, y_axis_rotation = y_axis_rotation, grid = grid, export_png = export_png, directory_to_save = directory_to_save, file_name = file_name, png_resolution_dpi = png_resolution_dpi)
    # Retrieve the feature importance ranking:
    feature_importance_df = model_check.feature_importance_df
    
    if ControlVars.show_results:
        print("\n") #line break
        print("To predict the model output y_pred for a dataframe X, declare: y_pred = ols_linear_reg_model.predict(X)\n")
        print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
        print("X_train = np.reshape(np.array(X_train), (-1, 1))")
        # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362
        
    return ols_linear_reg_model, metrics_dict, feature_importance_df


def ridge_linear_reg (X_train, y_train, alpha_hyperparameter = 0.001, maximum_of_allowed_iterations = 20000, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    ridge_linear_reg (X_train, y_train, alpha_hyperparameter = 0.001, maximum_of_allowed_iterations = 20000, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    check Scikit-learn documentation: 
     https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html#sklearn.linear_model.Ridge
    This function runs the 'bar_chart' function. 
    
    The regularizer tends to bring the coefficients to zero: the model will behave as a constant line 
    for higher regularization terms.
    - The Regularization term can be either:
        - Lasso: absolute value of the coefficients.
            - Force the coefficients of the regression to zero.
        - Ridge: square of the coefficients.
            - Bring the coefficients of the regression closer to zero.
        - Elastic net: combination of Ridge and Lasso.

        - Both shrink the coefficients related to unimportant predictors.

    - Regularization term `alpha`:
        - `alpha = 0`: no regularization (standard regression);
        - `alpha tending to infinite`: complete regularization (all coefficients to zero).
            - Regression becomes a constant line.

        - If all coefficients are different from zero, all variables are being considered important for the prediction.
        - The regularizer may bring coefficients to zero, selecting those which are effectively the most important parameters.

    : param: X_train = subset of predictive variables (dataframe).
    : param: y_train = subset of response variable (series).
    
    : param: hyperparameters: alpha = ALPHA_HYPERPARAMETER and MAXIMUM_OF_ALLOWED_ITERATIONS = max_iter

    : param: MAXIMUM_OF_ALLOWED_ITERATIONS = integer representing the maximum number of iterations
      that the optimization algorithm can perform. Depending on data, convergence may not be
      reached within this limit, so you may need to increase this hyperparameter.

      alpha is the regularization strength and must be a positive float value. 
      Regularization improves the conditioning of the problem and reduces the variance 
      of the estimates. Larger values specify stronger regularization.
    
      alpha = 0 is equivalent to an ordinary least square, solved by the LinearRegression 
      object. For numerical reasons, using alpha = 0 is not advised. 
      Given this, you should use the ols_linear_reg function instead.
    
      The regularizer tends to bring all coefficients of the regression to zero, i.e., with higher
      regularization terms, the model can become a constant line. On the other hand, it reduces the
      impact of high-coefficient features like X^4, reducing overfitting (high variance problem).
    
      So, apply low regularizers, like 0.001, specially if the data was previously normalized. alpha=1
      may bring the equivalence to a constant line (underfitting, high bias problem).
    """

    from sklearn.linear_model import Ridge
    
    RANDOM_STATE = 55 
    ## We will pass it to every sklearn call so we ensure reproducibility (i.e., a new random process)
    
    # Create an instance (object) from the class Ridge:
    # Pass the appropriate parameters to the class constructor:
    ridge_linear_reg_model = Ridge(alpha = alpha_hyperparameter, max_iter = maximum_of_allowed_iterations, random_state = RANDOM_STATE)
    
    # Sklearn requires a 1-dimensional vector for training the classifier.
    """
            y_train tensor original format:
                <tf.Tensor: shape=(87, 1), dtype=float64, numpy=
                array([[1.],
                    [0.], ....,
                    [0.]])>
            
            Reshape to unidimensional format. First step:
            y_train.numpy().reshape(1, -1)
            Now, it has format:
                array([[1., 0.,..., 0.]]), shape = (1, 87)
                (if we make reshape(-1, 1), we turn it again to the original tensor format)
            
            Notice that we want only the internal 1-dimensional array (with 87 values in the example)
            # So we make:
            y_train[0] to select only it.
    """
            
    y_train = np.array(y_train).reshape(1, -1)
    # This array has format([[val1, val2, ...]]) - i.e., it has two dimensions. Let's pick
    # only the first array:
    y_train = y_train[0]
    
    # Fit the model:
    ridge_linear_reg_model = ridge_linear_reg_model.fit(X_train, y_train)
    
    print(f"Total of iterations to fit the model = {ridge_linear_reg_model.n_iter_}\n")
    
    if (ridge_linear_reg_model.n_iter_ == maximum_of_allowed_iterations):
        print("Warning! Total of iterations equals to the maximum allowed. It indicates that the convergence was not reached yet. Try to increase the maximum number of allowed iterations.\n")
    
    # Get predictions for training, testing, and validation:
    y_preds_for_train = ridge_linear_reg_model.predict(X_train)
    
    if ((X_test is not None) & ((y_test is not None))):
        y_preds_for_test = ridge_linear_reg_model.predict(X_test)
    
    else:
        y_preds_for_test = None
    
    if ((X_valid is not None) & ((y_valid is not None))):
        y_preds_for_validation = ridge_linear_reg_model.predict(X_valid)
    
    else:
        y_preds_for_validation = None
    
    # instantiate the model checker object:
    model_check = ModelChecking(model_object = ridge_linear_reg_model, model_type = 'regression', model_package = 'sklearn', column_map_dict = column_map_dict, X = X_train, y_train = y_train, y_preds_for_train = y_preds_for_train, y_test = y_test, y_preds_for_test = y_preds_for_test, y_valid = y_valid, y_preds_for_validation = y_preds_for_validation)
    
    # Calculate model metrics:
    model_check = model_check.model_metrics()
    # Retrieve model metrics:
    metrics_dict = model_check.metrics_dict
    
    # Get feature importance ranking:
    model_check = model_check.feature_importance_ranking (model_class = 'linear', orientation = orientation, horizontal_axis_title = horizontal_axis_title, vertical_axis_title = vertical_axis_title, plot_title = plot_title, x_axis_rotation = x_axis_rotation, y_axis_rotation = y_axis_rotation, grid = grid, export_png = export_png, directory_to_save = directory_to_save, file_name = file_name, png_resolution_dpi = png_resolution_dpi)
    # Retrieve the feature importance ranking:
    feature_importance_df = model_check.feature_importance_df
    
    if ControlVars.show_results:
        print("\n") #line break
        print("To predict the model output y_pred for a dataframe X, declare: y_pred = ridge_linear_reg_model.predict(X)\n")
        print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
        print("X_train = np.reshape(np.array(X_train), (-1, 1))")
        # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362
        
    return ridge_linear_reg_model, metrics_dict, feature_importance_df


def lasso_linear_reg (X_train, y_train, alpha_hyperparameter = 0.001, maximum_of_allowed_iterations = 20000, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    lasso_linear_reg (X_train, y_train, alpha_hyperparameter = 0.001, maximum_of_allowed_iterations = 20000, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    check Scikit-learn documentation: 
      https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html#sklearn.linear_model.Lasso
    This function runs the 'bar_chart' function.

    The regularizer tends to bring the coefficients to zero: the model will behave as a constant line 
    for higher regularization terms.
    - The Regularization term can be either:
        - Lasso: absolute value of the coefficients.
            - Force the coefficients of the regression to zero.
        - Ridge: square of the coefficients.
            - Bring the coefficients of the regression closer to zero.
        - Elastic net: combination of Ridge and Lasso.

        - Both shrink the coefficients related to unimportant predictors.

    - Regularization term `alpha`:
        - `alpha = 0`: no regularization (standard regression);
        - `alpha tending to infinite`: complete regularization (all coefficients to zero).
            - Regression becomes a constant line.

        - If all coefficients are different from zero, all variables are being considered important for the prediction.
        - The regularizer may bring coefficients to zero, selecting those which are effectively the most important parameters.
    
    : param: X_train = subset of predictive variables (dataframe).
    : param: y_train = subset of response variable (series).
    
    : param: hyperparameters: alpha = ALPHA_HYPERPARAMETER and MAXIMUM_OF_ALLOWED_ITERATIONS = max_iter

      MAXIMUM_OF_ALLOWED_ITERATIONS = integer representing the maximum number of iterations
      that the optimization algorithm can perform. Depending on data, convergence may not be
      reached within this limit, so you may need to increase this hyperparameter.

      alpha is the regularization strength and must be a positive float value. 
      Regularization improves the conditioning of the problem and reduces the variance 
      of the estimates. Larger values specify stronger regularization.
    
      alpha = 0 is equivalent to an ordinary least square, solved by the LinearRegression 
      object. For numerical reasons, using alpha = 0 is not advised. 
      Given this, you should use the ols_linear_reg function instead.
    
      The regularizer tends to bring all coefficients of the regression to zero, i.e., with higher
      regularization terms, the model can become a constant line. On the other hand, it reduces the
      impact of high-coefficient features like X^4, reducing overfitting (high variance problem).
    
      So, apply low regularizers, like 0.001, specially if the data was previously normalized. alpha=1
      may bring the equivalence to a constant line (underfitting, high bias problem).
    """
    
    from sklearn.linear_model import Lasso
    
    RANDOM_STATE = 55 
    ## We will pass it to every sklearn call so we ensure reproducibility (i.e., a new random process)
    
    # Create an instance (object) from the class Lasso:
    # Pass the appropriate parameters to the class constructor:
    lasso_linear_reg_model = Lasso(alpha = alpha_hyperparameter, max_iter = maximum_of_allowed_iterations, random_state = RANDOM_STATE)
    # verbose = True to debug mode (show training status during training)
    
    # Sklearn requires a 1-dimensional vector for training the classifier.
    """
            y_train tensor original format:
                <tf.Tensor: shape=(87, 1), dtype=float64, numpy=
                array([[1.],
                    [0.], ....,
                    [0.]])>
            
            Reshape to unidimensional format. First step:
            y_train.numpy().reshape(1, -1)
            Now, it has format:
                array([[1., 0.,..., 0.]]), shape = (1, 87)
                (if we make reshape(-1, 1), we turn it again to the original tensor format)
            
            Notice that we want only the internal 1-dimensional array (with 87 values in the example)
            # So we make:
            y_train[0] to select only it.
    """
            
    y_train = np.array(y_train).reshape(1, -1)
    # This array has format([[val1, val2, ...]]) - i.e., it has two dimensions. Let's pick
    # only the first array:
    y_train = y_train[0]
    
    # Fit the model:
    lasso_linear_reg_model = lasso_linear_reg_model.fit(X_train, y_train)
    
    print(f"Total of iterations to fit the model = {lasso_linear_reg_model.n_iter_}\n")
    
    if (lasso_linear_reg_model.n_iter_ == maximum_of_allowed_iterations):
        print("Warning! Total of iterations equals to the maximum allowed. It indicates that the convergence was not reached yet. Try to increase the maximum number of allowed iterations.\n")
    
    # Get predictions for training, testing, and validation:
    y_preds_for_train = lasso_linear_reg_model.predict(X_train)
    
    if ((X_test is not None) & ((y_test is not None))):
        y_preds_for_test = lasso_linear_reg_model.predict(X_test)
    
    else:
        y_preds_for_test = None
    
    if ((X_valid is not None) & ((y_valid is not None))):
        y_preds_for_validation = lasso_linear_reg_model.predict(X_valid)
    
    else:
        y_preds_for_validation = None
    
    # instantiate the model checker object:
    model_check = ModelChecking(model_object = lasso_linear_reg_model, model_type = 'regression', model_package = 'sklearn', column_map_dict = column_map_dict, X = X_train, y_train = y_train, y_preds_for_train = y_preds_for_train, y_test = y_test, y_preds_for_test = y_preds_for_test, y_valid = y_valid, y_preds_for_validation = y_preds_for_validation)
    
    # Calculate model metrics:
    model_check = model_check.model_metrics()
    # Retrieve model metrics:
    metrics_dict = model_check.metrics_dict
    
    # Get feature importance ranking:
    model_check = model_check.feature_importance_ranking (model_class = 'linear', orientation = orientation, horizontal_axis_title = horizontal_axis_title, vertical_axis_title = vertical_axis_title, plot_title = plot_title, x_axis_rotation = x_axis_rotation, y_axis_rotation = y_axis_rotation, grid = grid, export_png = export_png, directory_to_save = directory_to_save, file_name = file_name, png_resolution_dpi = png_resolution_dpi)
    # Retrieve the feature importance ranking:
    feature_importance_df = model_check.feature_importance_df
    
    if ControlVars.show_results:
        print("\n") #line break
        print("To predict the model output y_pred for a dataframe X, declare: y_pred = lasso_linear_reg_model.predict(X)\n")
        print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
        print("X_train = np.reshape(np.array(X_train), (-1, 1))")
        # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362
        
    return lasso_linear_reg_model, metrics_dict, feature_importance_df


def elastic_net_linear_reg (X_train, y_train, alpha_hyperparameter = 0.001, l1_ratio_hyperparameter = 0.02, maximum_of_allowed_iterations = 20000, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    elastic_net_linear_reg (X_train, y_train, alpha_hyperparameter = 0.001, l1_ratio_hyperparameter = 0.02, maximum_of_allowed_iterations = 20000, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    check Scikit-learn documentation: 
      https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNet.html#sklearn.linear_model.ElasticNet
    This function runs the 'bar_chart' function. Certify that this function was properly loaded.
    
    The regularizer tends to bring the coefficients to zero: the model will behave as a constant line 
    for higher regularization terms.
    - The Regularization term can be either:
        - Lasso: absolute value of the coefficients.
            - Force the coefficients of the regression to zero.
        - Ridge: square of the coefficients.
            - Bring the coefficients of the regression closer to zero.
        - Elastic net: combination of Ridge and Lasso.

        - Both shrink the coefficients related to unimportant predictors.

    - Regularization term `alpha`:
        - `alpha = 0`: no regularization (standard regression);
        - `alpha tending to infinite`: complete regularization (all coefficients to zero).
            - Regression becomes a constant line.

        - If all coefficients are different from zero, all variables are being considered important for the prediction.
        - The regularizer may bring coefficients to zero, selecting those which are effectively the most important parameters.
    
    : param: X_train = subset of predictive variables (dataframe).
    : param: y_train = subset of response variable (series).
    
    : param: hyperparameters: alpha = alpha_hyperparameter; maximum_of_allowed_iterations = max_iter;
      and l1_ratio_hyperparameter = l1_ratio

      MAXIMUM_OF_ALLOWED_ITERATIONS = integer representing the maximum number of iterations
      that the optimization algorithm can perform. Depending on data, convergence may not be
      reached within this limit, so you may need to increase this hyperparameter.

      alpha is the regularization strength and must be a positive float value. 
      Regularization improves the conditioning of the problem and reduces the variance 
      of the estimates. Larger values specify stronger regularization.
    
      l1_ratio is The ElasticNet mixing parameter (float), with 0 <= l1_ratio <= 1. 
      For l1_ratio = 0 the penalty is an L2 penalty. For l1_ratio = 1 it is an L1 penalty. 
      For 0 < l1_ratio < 1, the penalty is a combination of L1 and L2.
      Currently, l1_ratio <= 0.01 is not reliable, unless you supply your own sequence of alpha.
    
      alpha = 0 and l1_ratio = 0 is equivalent to an ordinary least square, solved by 
      the LinearRegression object. For numerical reasons, using alpha = 0 and 
      l1_ratio = 0 is not advised. Given this, you should use the ols_linear_reg function instead.
    
      The regularizer tends to bring all coefficients of the regression to zero, i.e., with higher
      regularization terms, the model can become a constant line. On the other hand, it reduces the
      impact of high-coefficient features like X^4, reducing overfitting (high variance problem).
        
      So, apply low regularizers, like 0.001, specially if the data was previously normalized. alpha=1
      may bring the equivalence to a constant line (underfitting, high bias problem).
    """
    
    from sklearn.linear_model import ElasticNet
    
    RANDOM_STATE = 55 
    ## We will pass it to every sklearn call so we ensure reproducibility (i.e., a new random process)
    
    # Create an instance (object) from the class ElasticNet:
    # Pass the appropriate parameters to the class constructor:
    elastic_net_linear_reg_model = ElasticNet(alpha = alpha_hyperparameter, l1_ratio = l1_ratio_hyperparameter, max_iter = maximum_of_allowed_iterations, random_state = RANDOM_STATE)
    # verbose = True to debug mode (show training status during training)
    
    # Sklearn requires a 1-dimensional vector for training the classifier.
    """
            y_train tensor original format:
                <tf.Tensor: shape=(87, 1), dtype=float64, numpy=
                array([[1.],
                    [0.], ....,
                    [0.]])>
            
            Reshape to unidimensional format. First step:
            y_train.numpy().reshape(1, -1)
            Now, it has format:
                array([[1., 0.,..., 0.]]), shape = (1, 87)
                (if we make reshape(-1, 1), we turn it again to the original tensor format)
            
            Notice that we want only the internal 1-dimensional array (with 87 values in the example)
            # So we make:
            y_train[0] to select only it.
    """
            
    y_train = np.array(y_train).reshape(1, -1)
    # This array has format([[val1, val2, ...]]) - i.e., it has two dimensions. Let's pick
    # only the first array:
    y_train = y_train[0]
    
    # Fit the model:
    elastic_net_linear_reg_model = elastic_net_linear_reg_model.fit(X_train, y_train)
    
    print(f"Total of iterations to fit the model = {elastic_net_linear_reg_model.n_iter_}\n")
    
    if (elastic_net_linear_reg_model.n_iter_ == maximum_of_allowed_iterations):
        print("Warning! Total of iterations equals to the maximum allowed. It indicates that the convergence was not reached yet. Try to increase the maximum number of allowed iterations.\n")
    
    # Get predictions for training, testing, and validation:
    y_preds_for_train = elastic_net_linear_reg_model.predict(X_train)
    
    if ((X_test is not None) & ((y_test is not None))):
        y_preds_for_test = elastic_net_linear_reg_model.predict(X_test)
    
    else:
        y_preds_for_test = None
    
    if ((X_valid is not None) & ((y_valid is not None))):
        y_preds_for_validation = elastic_net_linear_reg_model.predict(X_valid)
    
    else:
        y_preds_for_validation = None
    
    # instantiate the model checker object:
    model_check = ModelChecking(model_object = elastic_net_linear_reg_model, model_type = 'regression', model_package = 'sklearn', column_map_dict = column_map_dict, X = X_train, y_train = y_train, y_preds_for_train = y_preds_for_train, y_test = y_test, y_preds_for_test = y_preds_for_test, y_valid = y_valid, y_preds_for_validation = y_preds_for_validation)
    
    # Calculate model metrics:
    model_check = model_check.model_metrics()
    # Retrieve model metrics:
    metrics_dict = model_check.metrics_dict
    
    # Get feature importance ranking:
    model_check = model_check.feature_importance_ranking (model_class = 'linear', orientation = orientation, horizontal_axis_title = horizontal_axis_title, vertical_axis_title = vertical_axis_title, plot_title = plot_title, x_axis_rotation = x_axis_rotation, y_axis_rotation = y_axis_rotation, grid = grid, export_png = export_png, directory_to_save = directory_to_save, file_name = file_name, png_resolution_dpi = png_resolution_dpi)
    # Retrieve the feature importance ranking:
    feature_importance_df = model_check.feature_importance_df
    
    if ControlVars.show_results:
        print("\n") #line break
        print("To predict the model output y_pred for a dataframe X, declare: y_pred = elastic_net_linear_reg_model.predict(X)\n")
        print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
        print("X_train = np.reshape(np.array(X_train), (-1, 1))")
        # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362
        
    return elastic_net_linear_reg_model, metrics_dict, feature_importance_df


def logistic_reg (X_train, y_train, regularization = 'l2', l1_ratio_hyperparameter = 0.02, maximum_of_allowed_iterations = 20000, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    logistic_reg (X_train, y_train, regularization = 'l2', l1_ratio_hyperparameter = 0.02, maximum_of_allowed_iterations = 20000, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    check Scikit-learn documentation: 
      https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html?msclkid=6bede8a8c1a011ecad332ec5eb711355
    This function runs the 'bar_chart' function. Certify that this function was properly loaded.
    
    The regularizer tends to bring the coefficients to zero: the model will behave as a constant line 
    for higher regularization terms.
    - The Regularization term can be either:
        - Lasso: absolute value of the coefficients.
            - Force the coefficients of the regression to zero.
        - Ridge: square of the coefficients.
            - Bring the coefficients of the regression closer to zero.
        - Elastic net: combination of Ridge and Lasso.

        - Both shrink the coefficients related to unimportant predictors.

    - Regularization term `alpha`:
        - `alpha = 0`: no regularization (standard regression);
        - `alpha tending to infinite`: complete regularization (all coefficients to zero).
            - Regression becomes a constant line.

        - If all coefficients are different from zero, all variables are being considered important for the prediction.
        - The regularizer may bring coefficients to zero, selecting those which are effectively the most important parameters.

    : param: X_train = subset of predictive variables (dataframe).
    : param: y_train = subset of response variable (series).

    : param: MAXIMUM_OF_ALLOWED_ITERATIONS = integer representing the maximum number of iterations
      that the optimization algorithm can perform. Depending on data, convergence may not be
      reached within this limit, so you may need to increase this hyperparameter.
    : param: REGULARIZATION is the norm of the penalty:
      REGULARIZATION = None: no penalty is added; REGULARIZATION = 'l2': add a L2 penalty term and 
      it is the default choice; REGULARIZATION = 'l1': add a L1 penalty term; 
      REGULARIZATION = 'elasticnet': both L1 and L2 penalty terms are added.
    
      The regularizer tends to bring all coefficients of the regression to zero, i.e., with higher
      regularization terms, the model can become a constant line. On the other hand, it reduces the
      impact of high-coefficient features like X^4, reducing overfitting (high variance problem).        
      So, apply low regularizers, like 0.001, specially if the data was previously normalized. alpha=1
      may bring the equivalence to a constant line (underfitting, high bias problem).
      L1_RATIO_HYPERPARAMETER is The ElasticNet mixing parameter (float), with 0 <= l1_ratio <= 1. 
      For L1_RATIO_HYPERPARAMETER = 0 the penalty is an L2 penalty. For l1_ratio = 1 it is an L1 penalty. 
      For 0 < L1_RATIO_HYPERPARAMETER < 1, the penalty is a combination of L1 and L2.
    
      Currently, l1_ratio <= 0.01 is not reliable, unless you supply your own sequence of alpha.
    """

    from sklearn.linear_model import LogisticRegression
    
    print("Attention: logistic regression is a binary classifier. It results in probabilities, instead of on scalar (real numbers) like other regression algorithms from linear models class.\n")
    
    
    RANDOM_STATE = 55 
    ## We will pass it to every sklearn call so we ensure reproducibility (i.e., a new random process)
    
    # Instantiate a model checker object to verify if there are only two classes:
    check_classes = ModelChecking()
    # Use the vars function to access the attributes dictionary and set the value from y_train:
    # Make sure that it is a tensor, so that it can use .numpy method:
    vars(check_classes)['y_train'] = tf.constant(y_train)
    # Retrieve the classes:
    check_classes = check_classes.retrieve_classes_used_for_training()
    # Retrieve the attributes:
    number_of_classes = check_classes.number_of_classes
    list_of_classes = check_classes.list_of_classes
    
    # Create a dictionary to return:
    classes_dict = {'list_of_classes': list_of_classes,
                    'number_of_classes': number_of_classes}
    
    if (number_of_classes == 2):
        # Logistic regression can be obtained for only two classes.
        # Since the number of classes is correct, we can proceed.
        
        # Pass the appropriate parameters to the class constructor:
        logistic_reg_model = LogisticRegression(penalty = regularization, max_iter = maximum_of_allowed_iterations, random_state = RANDOM_STATE, l1_ratio = l1_ratio_hyperparameter)
        # verbose = 1 to debug mode is not available for 'saga' solver

        # Fit the model:
        # Sklearn logistic regression requires a 1-dimensional vector for training.
        """
        y_train tensor original format:
            <tf.Tensor: shape=(87, 1), dtype=float64, numpy=
            array([[1.],
                [0.], ....,
                [0.]])>
        
        Reshape to unidimensional format. First step:
        y_train.numpy().reshape(1, -1)
        Now, it has format:
            array([[1., 0.,..., 0.]]), shape = (1, 87)
            (if we make reshape(-1, 1), we turn it again to the original tensor format)
        
        Notice that we want only the internal 1-dimensional array (with 87 values in the example)
        # So we make:
        y_train[0] to select only it.
        """
        
        reshaped_y_train = np.array(y_train).reshape(1, -1)
        # This array has format([[val1, val2, ...]]) - i.e., it has two dimensions. Let's pick
        # only the first array:
        reshaped_y_train = reshaped_y_train[0]


        logistic_reg_model = logistic_reg_model.fit(X_train, reshaped_y_train)
        print(f"Total of iterations to fit the model = {logistic_reg_model.n_iter_}\n")

        if (logistic_reg_model.n_iter_ == maximum_of_allowed_iterations):
            print("Warning! Total of iterations equals to the maximum allowed. It indicates that the convergence was not reached yet. Try to increase the maximum number of allowed iterations.\n")

        # Get predictions for training, testing, and validation:
        y_preds_for_train = logistic_reg_model.predict(X_train)

        if ((X_test is not None) & ((y_test is not None))):
            y_preds_for_test = logistic_reg_model.predict(X_test)

        else:
            y_preds_for_test = None

        if ((X_valid is not None) & ((y_valid is not None))):
            y_preds_for_validation = logistic_reg_model.predict(X_valid)

        else:
            y_preds_for_validation = None

        # instantiate the model checker object:
        model_check = ModelChecking(model_object = logistic_reg_model, model_type = 'classification', model_package = 'sklearn', column_map_dict = column_map_dict, X = X_train, y_train = y_train, y_preds_for_train = y_preds_for_train, y_test = y_test, y_preds_for_test = y_preds_for_test, y_valid = y_valid, y_preds_for_validation = y_preds_for_validation)
        
        # Calculate model metrics:
        model_check = model_check.model_metrics()
        # Retrieve model metrics:
        metrics_dict = model_check.metrics_dict

        # Get feature importance ranking:
        model_check = model_check.feature_importance_ranking (model_class = 'linear', orientation = orientation, horizontal_axis_title = horizontal_axis_title, vertical_axis_title = vertical_axis_title, plot_title = plot_title, x_axis_rotation = x_axis_rotation, y_axis_rotation = y_axis_rotation, grid = grid, export_png = export_png, directory_to_save = directory_to_save, file_name = file_name, png_resolution_dpi = png_resolution_dpi)
        # Retrieve the feature importance ranking:
        feature_importance_df = model_check.feature_importance_df

        if ControlVars.show_results:
            print("\n") #line break
            print("To predict the model output y_pred for a dataframe X, declare: y_pred = logistic_reg_model.predict(X)\n")
            print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
            print("X_train = np.reshape(np.array(X_train), (-1, 1))")
            # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362

            print("To predict the probabilities associated to each class for the set X_train, use the .predict_proba(X) method:")
            print("y_pred_probabilities = logistic_reg_model.predict_proba(X_train)")

        return logistic_reg_model, metrics_dict, feature_importance_df, classes_dict
    
    else:
        raise InvalidInputsError(f"Unable to perform logistic regression. Found a total of {number_of_classes} in the training tensor: {list_of_classes}\n")


def glm_regression(
    X_train,
    y_train,
    distribution = 'poisson',
    link = None,
    alpha_dispersion = 1.0,
    fit_intercept = True,
    exposure = None,
    offset = None,
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
    png_resolution_dpi = 330,
    plotly = False
):
    """
    glm_regression:
    Fits a Generalized Linear Model (GLM) using statsmodels supporting count, continuous,
    and binary data with robust family distributions and link functions.

    Covers key distributions:
    - Poisson ('poisson'): for count data where variance approx equals mean.
    - Negative Binomial ('negative_binomial' / 'neg_binomial'): for overdispersed count data.
    - Gamma ('gamma'): for positive continuous right-skewed responses.
    - Gaussian ('gaussian' / 'normal'): for standard continuous responses.
    - Binomial ('binomial'): for binary or proportion responses.
    - Inverse Gaussian ('inverse_gaussian'): for positive continuous data with heavy right tails.
    - Lognormal ('lognormal' / 'log_normal'): for strictly positive lognormally distributed targets.

    : param: X_train: pandas DataFrame, Series, or array containing training features.
    : param: y_train: pandas Series, 1D DataFrame column, or array of training response values.
    : param: distribution: string (default 'poisson'), the response probability family.
    : param: link: string or statsmodels family link instance (default None for canonical link).
    : param: alpha_dispersion: float (default 1.0), dispersion parameter for Negative Binomial family.
    : param: fit_intercept: boolean (default True), whether to add a constant/intercept term.
    : param: exposure: array-like or None (default None), log-transformed exposure factor for rates.
    : param: offset: array-like or None (default None), additive offset term.
    : param: X_test: pandas DataFrame or array for test evaluation (optional).
    : param: y_test: pandas Series or array for test evaluation (optional).
    : param: X_valid: pandas DataFrame or array for validation (optional).
    : param: y_valid: pandas Series or array for validation (optional).
    : param: column_map_dict: optional dict mapping column names to human-readable labels.
    : param: orientation: string ('vertical' or 'horizontal') for feature importance bar chart.
    : param: horizontal_axis_title: title for horizontal axis.
    : param: vertical_axis_title: title for vertical axis.
    : param: plot_title: title for the plot.
    : param: x_axis_rotation: rotation angle for X-axis labels.
    : param: y_axis_rotation: rotation angle for Y-axis labels.
    : param: grid: boolean, whether to display grid lines.
    : param: export_png: boolean, whether to save feature importance plot.
    : param: directory_to_save: folder path where the image will be exported.
    : param: file_name: name of the exported image file.
    : param: png_resolution_dpi: image resolution in DPI (default 330).
    : return: tuple (glm_results, metrics_dict, coefficients_df).
    """
    import statsmodels.api as sm
    import statsmodels.genmod.families as families
    from statsmodels.genmod.families import links

    # Validate inputs
    if X_train is None or y_train is None:
        raise InvalidInputsError("X_train and y_train must not be None.")

    # Convert y_train to 1D numpy array
    y_arr = np.asarray(y_train).ravel()
    N = len(y_arr)
    if N < 3:
        raise InvalidInputsError("y_train must contain at least 3 observations to fit a GLM.")

    # Prepare feature matrix X
    if isinstance(X_train, pd.DataFrame):
        feature_names = list(X_train.columns)
        X_df = X_train.copy(deep = True)
    elif isinstance(X_train, pd.Series):
        feature_names = [X_train.name if X_train.name is not None else "feature_0"]
        X_df = pd.DataFrame(X_train.values, columns = feature_names)
    else:
        X_arr = np.asarray(X_train)
        if X_arr.ndim == 1:
            X_arr = X_arr.reshape(-1, 1)
        feature_names = [f"feature_{i}" for i in range(X_arr.shape[1])]
        X_df = pd.DataFrame(X_arr, columns = feature_names)

    # Apply column_map_dict if provided
    if column_map_dict is not None and isinstance(column_map_dict, dict):
        X_df = X_df.rename(columns = column_map_dict)
        feature_names = list(X_df.columns)

    # Add constant if requested
    if fit_intercept:
        X_design = sm.add_constant(X_df, has_constant = 'add')
        all_feature_names = ['const'] + [c for c in X_design.columns if c != 'const']
        X_design = X_design[all_feature_names]
    else:
        X_design = X_df.copy(deep = True)
        all_feature_names = list(X_design.columns)

    # Resolve link function if provided as string
    link_obj = None
    if isinstance(link, str):
        link_str = link.strip().lower()
        if link_str in ['log']:
            link_obj = links.Log()
        elif link_str in ['identity', 'linear']:
            link_obj = links.Identity()
        elif link_str in ['logit']:
            link_obj = links.Logit()
        elif link_str in ['probit']:
            link_obj = links.Probit()
        elif link_str in ['cloglog']:
            link_obj = links.CLogLog()
        elif link_str in ['inverse_power', 'reciprocal']:
            link_obj = links.InversePower()
        elif link_str in ['sqrt']:
            link_obj = links.Sqrt()
        elif link_str in ['inverse_squared']:
            link_obj = links.InverseSquared()
    elif link is not None:
        link_obj = link

    # Resolve distribution family
    dist_clean = str(distribution).strip().lower()

    if dist_clean == 'poisson':
        if np.any(y_arr < 0):
            raise InvalidInputsError("Poisson distribution requires non-negative count values (y >= 0).")
        family_obj = families.Poisson(link = link_obj if link_obj is not None else links.Log())

    elif dist_clean in ['negative_binomial', 'neg_binomial', 'nb']:
        if np.any(y_arr < 0):
            raise InvalidInputsError("Negative Binomial distribution requires non-negative count values (y >= 0).")
        family_obj = families.NegativeBinomial(alpha = alpha_dispersion, link = link_obj if link_obj is not None else links.Log())

    elif dist_clean == 'gamma':
        if np.any(y_arr <= 0):
            raise InvalidInputsError("Gamma distribution requires strictly positive values (y > 0).")
        family_obj = families.Gamma(link = link_obj if link_obj is not None else links.Log())

    elif dist_clean in ['gaussian', 'normal']:
        family_obj = families.Gaussian(link = link_obj if link_obj is not None else links.Identity())

    elif dist_clean == 'binomial':
        if np.any((y_arr < 0) | (y_arr > 1)):
            raise InvalidInputsError("Binomial distribution requires target values in range [0, 1].")
        family_obj = families.Binomial(link = link_obj if link_obj is not None else links.Logit())

    elif dist_clean == 'inverse_gaussian':
        if np.any(y_arr <= 0):
            raise InvalidInputsError("Inverse Gaussian requires strictly positive values (y > 0).")
        family_obj = families.InverseGaussian(link = link_obj if link_obj is not None else links.InverseSquared())

    elif dist_clean in ['lognormal', 'log_normal']:
        if np.any(y_arr <= 0):
            raise InvalidInputsError("Lognormal distribution requires strictly positive values (y > 0).")
        family_obj = families.Gaussian(link = link_obj if link_obj is not None else links.Log())

    else:
        raise InvalidInputsError(
            f"Unsupported distribution '{distribution}'. Choose from: 'poisson', 'negative_binomial', "
            f"'gamma', 'gaussian', 'binomial', 'inverse_gaussian', 'lognormal'."
        )

    # Fit statsmodels GLM
    glm_model = sm.GLM(
        endog = y_arr,
        exog = X_design,
        family = family_obj,
        exposure = exposure,
        offset = offset
    )
    glm_results = glm_model.fit()

    # Calculate model metrics
    y_preds_train = glm_results.predict(X_design)
    train_rmse = float(np.sqrt(np.mean((y_arr - y_preds_train) ** 2)))
    train_mae = float(np.mean(np.abs(y_arr - y_preds_train)))

    df_resid = float(glm_results.df_resid) if glm_results.df_resid > 0 else 1.0
    pearson_chi2 = float(glm_results.pearson_chi2)
    dispersion_ratio = float(pearson_chi2 / df_resid)

    deviance = float(glm_results.deviance)
    null_deviance = float(glm_results.null_deviance)
    pseudo_r2 = float(1.0 - (deviance / null_deviance)) if null_deviance != 0 else 0.0

    metrics_dict = {
        "family": family_obj.__class__.__name__,
        "link": family_obj.link.__class__.__name__,
        "AIC": float(glm_results.aic),
        "BIC": float(glm_results.bic_deviance) if hasattr(glm_results, 'bic_deviance') else float(glm_results.bic),
        "deviance": deviance,
        "null_deviance": null_deviance,
        "pseudo_r2": pseudo_r2,
        "pearson_chi2": pearson_chi2,
        "dispersion_ratio": dispersion_ratio,
        "log_likelihood": float(glm_results.llf),
        "train_rmse": train_rmse,
        "train_mae": train_mae
    }

    # Test set metrics if provided
    if X_test is not None and y_test is not None:
        y_test_arr = np.asarray(y_test).ravel()
        if isinstance(X_test, pd.DataFrame):
            X_test_df = X_test.copy(deep = True)
        else:
            X_test_arr = np.asarray(X_test)
            if X_test_arr.ndim == 1:
                X_test_arr = X_test_arr.reshape(-1, 1)
            X_test_df = pd.DataFrame(X_test_arr, columns = feature_names)

        if fit_intercept:
            X_test_design = sm.add_constant(X_test_df, has_constant = 'add')
            X_test_design = X_test_design[all_feature_names]
        else:
            X_test_design = X_test_df[all_feature_names]

        y_preds_test = glm_results.predict(X_test_design)
        metrics_dict["test_rmse"] = float(np.sqrt(np.mean((y_test_arr - y_preds_test) ** 2)))
        metrics_dict["test_mae"] = float(np.mean(np.abs(y_test_arr - y_preds_test)))

    # Build coefficients DataFrame with exponentiated values
    params = glm_results.params
    bse = glm_results.bse
    tvalues = glm_results.tvalues
    pvalues = glm_results.pvalues
    conf = glm_results.conf_int()

    coef_data = []
    for feat in all_feature_names:
        idx = feat if feat in params.index else all_feature_names.index(feat)
        b = float(params[idx])
        se = float(bse[idx])
        z = float(tvalues[idx])
        p = float(pvalues[idx])
        ci_low = float(conf.loc[idx, 0]) if isinstance(conf, pd.DataFrame) else float(conf[idx][0])
        ci_high = float(conf.loc[idx, 1]) if isinstance(conf, pd.DataFrame) else float(conf[idx][1])

        # Exponentiated coefficients (multiplicative effect / odds ratio / rate ratio)
        exp_b = float(np.exp(b)) if abs(b) < 700 else np.nan
        exp_ci_low = float(np.exp(ci_low)) if abs(ci_low) < 700 else np.nan
        exp_ci_high = float(np.exp(ci_high)) if abs(ci_high) < 700 else np.nan

        coef_data.append({
            "feature": feat,
            "coefficient": b,
            "std_err": se,
            "z_value": z,
            "p_value": p,
            "ci_lower_95": ci_low,
            "ci_upper_95": ci_high,
            "exp_coefficient": exp_b,
            "exp_ci_lower_95": exp_ci_low,
            "exp_ci_upper_95": exp_ci_high
        })

    coefficients_df = pd.DataFrame(coef_data)

    # Attach sklearn-compatible .coef_ and .intercept_ attributes to glm_results for seamless ModelChecking integration
    try:
        if fit_intercept and 'const' in all_feature_names:
            non_const_feats = [f for f in all_feature_names if f != 'const']
            setattr(glm_results, 'intercept_', float(params['const']))
            setattr(glm_results, 'coef_', np.array([float(params[f]) for f in non_const_feats]))
        else:
            setattr(glm_results, 'intercept_', 0.0)
            setattr(glm_results, 'coef_', np.array([float(params[f]) for f in all_feature_names]))
    except Exception:
        pass

    # Print summary and educational guidance
    if ControlVars.show_results:
        print("=" * 80)
        print(f"GENERALIZED LINEAR MODEL (GLM) - Family: {family_obj.__class__.__name__}, Link: {family_obj.link.__class__.__name__}")
        print("=" * 80)
        print(glm_results.summary())
        print("\n--- Model Evaluation Metrics ---")
        print(f"AIC: {metrics_dict['AIC']:.4f} | BIC: {metrics_dict['BIC']:.4f}")
        print(f"Residual Deviance: {deviance:.4f} | Null Deviance: {null_deviance:.4f} | Pseudo R-squared: {pseudo_r2:.4f}")
        print(f"Pearson Chi-Square: {pearson_chi2:.4f} | Degrees of Freedom: {df_resid:.0f}")
        print(f"Estimated Dispersion Ratio (Pearson Chi2 / df_resid): {dispersion_ratio:.4f}")
        print(f"Training RMSE: {train_rmse:.4f} | Training MAE: {train_mae:.4f}")
        if "test_rmse" in metrics_dict:
            print(f"Test RMSE: {metrics_dict['test_rmse']:.4f} | Test MAE: {metrics_dict['test_mae']:.4f}")

        # Overdispersion diagnostic
        print("\n--- Dispersion Diagnostic ---")
        if dist_clean == 'poisson':
            if dispersion_ratio > 1.25:
                print(f"[!] Warning: Evidence of OVERDISPERSION detected (ratio = {dispersion_ratio:.4f} > 1).")
                print("    In a standard Poisson model, variance is assumed to equal the mean (ratio ~ 1).")
                print("    Overdispersion leads to underestimated standard errors and falsely significant p-values.")
                print("    RECOMMENDATION: Use Negative Binomial regression ('negative_binomial') with dispersion parameter alpha.")
            elif dispersion_ratio < 0.75:
                print(f"[*] Note: Mild underdispersion observed (ratio = {dispersion_ratio:.4f} < 1).")
            else:
                print(f"[OK] Dispersion is well calibrated for Poisson distribution (ratio = {dispersion_ratio:.4f} ~ 1).")
        elif dist_clean in ['negative_binomial', 'neg_binomial', 'nb']:
            print(f"[OK] Negative Binomial model accounts for overdispersion with alpha = {alpha_dispersion}.")
            print(f"    Current dispersion ratio = {dispersion_ratio:.4f}.")

        # Exponentiated coefficients interpretation
        print("\n--- Coefficients and Multiplicative Effects (exp(beta)) ---")
        try:
            from IPython.display import display
            display(coefficients_df)
        except Exception:
            print(coefficients_df.to_string())

        print("\nInterpretation of Multiplicative Effects:")
        print("1. For log-link models (Poisson, Negative Binomial, Gamma, Log-Normal):")
        print("   - exp(beta) > 1: each 1-unit increase in X multiplies the expected response by exp(beta) (percentage change: (exp(beta) - 1) * 100%).")
        print("   - exp(beta) < 1: each 1-unit increase in X multiplies the expected response by exp(beta) (decrease).")
        print("   - exp(beta) = 1: no effect on the response.")
        print("2. For logit-link models (Binomial / Logistic):")
        print("   - exp(beta) represents the Odds Ratio (OR) associated with a 1-unit increase in X.\n")

    # Feature importance plot
    plot_df = coefficients_df[coefficients_df['feature'] != 'const'].copy()
    if len(plot_df) > 0:
        plot_df['abs_coef'] = np.abs(plot_df['coefficient'])
        plot_df = plot_df.sort_values(by = 'abs_coef', ascending = True)
        p_title = plot_title if plot_title is not None else f"GLM Feature Coefficients ({family_obj.__class__.__name__})"

        if plotly:
            import plotly.express as px
            from idsw.plotly_utils import PlotlyHandler
            if orientation == 'horizontal':
                fig_plotly = px.bar(plot_df, x = 'coefficient', y = 'feature', orientation = 'h', title = p_title,
                                    labels = {'coefficient': horizontal_axis_title if horizontal_axis_title is not None else "Coefficient Value (beta)",
                                              'feature': vertical_axis_title if vertical_axis_title is not None else "Feature"})
                fig_plotly.add_vline(x = 0, line_dash = 'dash', line_color = 'black')
            else:
                fig_plotly = px.bar(plot_df, x = 'feature', y = 'coefficient', title = p_title,
                                    labels = {'feature': horizontal_axis_title if horizontal_axis_title is not None else "Feature",
                                              'coefficient': vertical_axis_title if vertical_axis_title is not None else "Coefficient Value (beta)"})
                fig_plotly.add_hline(y = 0, line_dash = 'dash', line_color = 'black')
            fig_plotly.update_layout(template = "plotly_white")
            PlotlyHandler.show_and_export(fig_plotly, export_file = export_png, directory_to_save = directory_to_save, file_name = file_name)
        elif ControlVars.show_plots:
            fig, ax = plt.subplots(figsize = (10, max(5, int(len(plot_df) * 0.4))))

            if orientation == 'horizontal':
                bars = ax.barh(plot_df['feature'], plot_df['coefficient'], color = 'steelblue', edgecolor = 'black')
                ax.axvline(0, color = 'black', linestyle = '--', linewidth = 0.8)
                ax.set_xlabel(horizontal_axis_title if horizontal_axis_title is not None else "Coefficient Value (beta)")
                ax.set_ylabel(vertical_axis_title if vertical_axis_title is not None else "Feature")
            else:
                bars = ax.bar(plot_df['feature'], plot_df['coefficient'], color = 'steelblue', edgecolor = 'black')
                ax.axhline(0, color = 'black', linestyle = '--', linewidth = 0.8)
                ax.set_xlabel(horizontal_axis_title if horizontal_axis_title is not None else "Feature")
                ax.set_ylabel(vertical_axis_title if vertical_axis_title is not None else "Coefficient Value (beta)")
                plt.xticks(rotation = x_axis_rotation)
                plt.yticks(rotation = y_axis_rotation)

            ax.set_title(p_title)
            ax.grid(grid)

            if export_png:
                import os
                if directory_to_save is None:
                    directory_to_save = ""
                if file_name is None:
                    file_name = f"glm_coefficients_{dist_clean}"
                new_file_path = os.path.join(directory_to_save, file_name + ".png")
                plt.savefig(new_file_path, dpi = png_resolution_dpi, bbox_inches = 'tight')
                if ControlVars.show_results:
                    print(f"Feature importance plot exported to '{new_file_path}'.")

            plt.show()

    return glm_results, metrics_dict, coefficients_df


def poisson_regression(X_train, y_train, fit_intercept = True, exposure = None, offset = None, X_test = None, y_test = None, **kwargs):
    """
    poisson_regression:
    Convenience wrapper for GLM Poisson regression with log link.
    Ideal for count data (e.g. number of defects, accidents, items sold, arrivals).
    """
    return glm_regression(
        X_train = X_train,
        y_train = y_train,
        distribution = 'poisson',
        link = 'log',
        fit_intercept = fit_intercept,
        exposure = exposure,
        offset = offset,
        X_test = X_test,
        y_test = y_test,
        **kwargs
    )


def negative_binomial_regression(X_train, y_train, alpha_dispersion = 1.0, fit_intercept = True, exposure = None, offset = None, X_test = None, y_test = None, **kwargs):
    """
    negative_binomial_regression:
    Convenience wrapper for GLM Negative Binomial regression with log link.
    Solves overdispersion in count data by introducing dispersion parameter alpha.
    """
    return glm_regression(
        X_train = X_train,
        y_train = y_train,
        distribution = 'negative_binomial',
        link = 'log',
        alpha_dispersion = alpha_dispersion,
        fit_intercept = fit_intercept,
        exposure = exposure,
        offset = offset,
        X_test = X_test,
        y_test = y_test,
        **kwargs
    )


def gamma_regression(X_train, y_train, link = 'log', fit_intercept = True, X_test = None, y_test = None, **kwargs):
    """
    gamma_regression:
    Convenience wrapper for GLM Gamma regression.
    Ideal for strictly positive, right-skewed continuous variables (e.g., costs, durations, asset lifetimes).
    """
    return glm_regression(
        X_train = X_train,
        y_train = y_train,
        distribution = 'gamma',
        link = link,
        fit_intercept = fit_intercept,
        X_test = X_test,
        y_test = y_test,
        **kwargs
    )


def lognormal_glm_regression(X_train, y_train, fit_intercept = True, X_test = None, y_test = None, **kwargs):
    """
    lognormal_glm_regression:
    Convenience wrapper for GLM Log-Normal regression (Gaussian family with Log link).
    Suitable for continuous positive variables that follow a lognormal distribution.
    """
    return glm_regression(
        X_train = X_train,
        y_train = y_train,
        distribution = 'lognormal',
        link = 'log',
        fit_intercept = fit_intercept,
        X_test = X_test,
        y_test = y_test,
        **kwargs
    )

