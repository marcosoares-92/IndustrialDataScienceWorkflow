import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf

from idsw.datafetch.core import InvalidInputsError
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

        print("\n") #line break
        print("To predict the model output y_pred for a dataframe X, declare: y_pred = logistic_reg_model.predict(X)\n")
        print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
        print("X_train = np.reshape(np.array(X_train), (-1, 1))")
        # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362

        print("To predict the probabilities associated to each class for the set X_train, use the .predict_proba(X) method:")
        print("y_pred_probabilities = logistic_reg_model.predict_proba(X_train)")

        return logistic_reg_model, metrics_dict, feature_importance_df, classes_dict
    
    else:
        print("Unable to perform logistic regression.")
        print(f"Found a total of {number_of_classes} in the training tensor: {list_of_classes}\n")
        
        return None, None, None, classes_dict
