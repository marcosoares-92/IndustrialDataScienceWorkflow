import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf

from idsw import (InvalidInputsError, ControlVars)
from .core import ModelChecking


def support_vector_machines (X_train, y_train, type_of_problem = "regression", X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None):
    """
    https://scikit-learn.org/1.5/modules/generated/sklearn.svm.SVC.html#sklearn.svm.SVC
    
    : param: X_train = subset of predictive variables (dataframe).
    : param: y_train = subset of response variable (series).

    """    
    
    RANDOM_STATE = 55 
    ## We will pass it to every sklearn call so we ensure reproducibility (i.e., a new random process)
    
    # Start a summary dictionary:
    summary_dict = {}
    
    
    if (type_of_problem == "regression"):
        
        from sklearn.svm import SVR
        svm = SVR(gamma = 'auto')
        
    elif (type_of_problem == "classification"):
        
        from sklearn.svm import SVC
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
        
        # Store it in the summary dictionary:
        summary_dict['classes'] = classes_dict
        
        svm = SVC(gamma = 'auto')

        
    else:
        
        raise InvalidInputsError ("Enter a valid type of problem, \'regression\' or \'classification\'.")
    
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
        
    reshaped_y_train = np.array(y_train).reshape(1, -1)
    # This array has format([[val1, val2, ...]]) - i.e., it has two dimensions. Let's pick
    # only the first array:
    reshaped_y_train = reshaped_y_train[0]
    
    svm = svm.fit(X_train, reshaped_y_train)
    
    
    # Get predictions for training, testing, and validation:
    y_preds_for_train = svm.predict(X_train)

    if ((X_test is not None) & ((y_test is not None))):
        y_preds_for_test = svm.predict(X_test)

    else:
        y_preds_for_test = None

    if ((X_valid is not None) & ((y_valid is not None))):
        y_preds_for_validation = svm.predict(X_valid)

    else:
        y_preds_for_validation = None

    # instantiate the model checker object:
    model_check = ModelChecking(model_object = svm, model_type = type_of_problem, model_package = 'sklearn', column_map_dict = column_map_dict, X = X_train, y_train = y_train, y_preds_for_train = y_preds_for_train, y_test = y_test, y_preds_for_test = y_preds_for_test, y_valid = y_valid, y_preds_for_validation = y_preds_for_validation)
        
    # Calculate model metrics:
    model_check = model_check.model_metrics()
    # Retrieve model metrics:
    metrics_dict = model_check.metrics_dict
    
    # Store the metrics dictionary in the summary dictionary:
    summary_dict['metrics_dict'] = metrics_dict

    # Get feature importance ranking:
    model_check = model_check.feature_importance_ranking (model_class = 'tree', orientation = orientation, horizontal_axis_title = horizontal_axis_title, vertical_axis_title = vertical_axis_title, plot_title = plot_title, x_axis_rotation = x_axis_rotation, y_axis_rotation = y_axis_rotation, grid = grid, export_png = export_png, directory_to_save = directory_to_save, file_name = file_name, png_resolution_dpi = png_resolution_dpi)
    # Retrieve the feature importance ranking:
    feature_importance_df = model_check.feature_importance_df
    
    # Store the importance ranking in the summary dictionary:
    summary_dict['feature_importance_df'] = feature_importance_df
    
    if ControlVars.show_results:
      
        print("\n") #line break
        print("To predict the model output y_pred for a dataframe X, declare: y_pred = svm.predict(X)\n")
        print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
        print("X_train = np.reshape(np.array(X_train), (-1, 1))")
        # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362
        
        if (type_of_problem == 'classification'):
            
            print("To predict the probabilities associated to each class for the set X_train, use the .predict_proba(X) method:")
            print("y_pred_probabilities = svm.predict_proba(X_train)")

    return svm, summary_dict

