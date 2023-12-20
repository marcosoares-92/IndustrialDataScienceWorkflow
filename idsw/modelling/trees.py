import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf

from idsw.datafetch.core import InvalidInputsError
from .core import ModelChecking


def random_forest (X_train, y_train, type_of_problem = "regression", number_of_trees = 128, max_tree_depth = 20, min_samples_to_split_node = 2, min_samples_to_make_leaf = 2, bootstrap_samples = True, use_out_of_bag_error = True, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    random_forest (X_train, y_train, type_of_problem = "regression", number_of_trees = 128, max_tree_depth = 20, min_samples_to_split_node = 2, min_samples_to_make_leaf = 2, bootstrap_samples = True, use_out_of_bag_error = True, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330)

    - Bagging ensemble of decision trees.
    - Data is divided and sampled. Trees are trained simultaneously, giving no preference to a given subset.
        - With bagging, some instances may be subject to sampling several times in each predictor, while others may not.
        - By default, a Bagging Classifier samples m training instances with replacement (bootstrap = True), where m is the training size. It means that, on average, only 63% of training instances are sampled by each predictor.
        - The 37% remaining training instances are called out-of-bag (oob) samples, and the 37% are not the same for all predictors. Once the predictor is not exposed to such instances during training, it may be evaluated with them with no need of a separated validation set.
        - The ensemble itself may be evaluated as the average of each predictor regarding the oob evaluations.
    
    This function runs the 'bar_chart' function.
    check Random Forest documentation on Scikit-learn:
      https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html
    Check explanaining of out-of-bag error:
      https://scikit-learn.org/stable/auto_examples/ensemble/plot_ensemble_oob.html
    
    
    : param: X_train = subset of predictive variables (dataframe).
    : param: y_train = subset of response variable (series).
    
    : param: TYPE_OF_PROBLEM = 'regression'; or TYPE_OF_PROBLEM = 'classification'
      The default is 'regression', which will be used if no type is
      provided.
    
    : param: NUMBER_OF_TREES = 128 (integer) - number of trees in the forest
      it is the n_estimators parameter of the model.
      Usually, a number from 64 to 128 is used.

    : param: MAX_TREE_DEPTH = 20 - integer representing the maximum depth 
      permitted for the trees (base learners). If None, then nodes are expanded 
      until all leaves are pure or until all leaves contain less 
      than MIN_SAMPLES_TO_SPLIT_NODE samples.
      it is the max_depth parameter of the model.

    : param: MIN_SAMPLES_TO_SPLIT_NODE = 2 (integer or float). It is the 
      min_samples_split parameter of the model.
      The minimum number of samples required to split an internal node:
      If int, then consider MIN_SAMPLES_TO_SPLIT_NODE as the minimum number.
      If float, then MIN_SAMPLES_TO_SPLIT_NODE is a fraction and ceil
      (MIN_SAMPLES_TO_SPLIT_NODE * NUMBER_OF_TREES) are the minimum number 
      of samples for each split.

    : param: MIN_SAMPLES_TO_MAKE_LEAF = 2 (integer or float). It is the
      min_samples_leaf parameter of the model.
      The minimum number of samples required to be at a leaf node. 
      A split point at any depth will only be considered if it leaves at 
      least MIN_SAMPLES_TO_MAKE_LEAF training samples in each of the left and right branches. 
      This may have the effect of smoothing the model, especially in regression.
      If int, then consider MIN_SAMPLES_TO_MAKE_LEAF as the minimum number.
      If float, then MIN_SAMPLES_TO_MAKE_LEAF is a fraction and ceil
      (MIN_SAMPLES_TO_MAKE_LEAF * NUMBER_OF_TREES) are the minimum number 
      of samples for each node.
    
    : param: bootstrap_samples = True. Parameter bootstrap of the model.
      Whether bootstrap samples are used when building trees. If False, 
      the whole dataset is used to build each tree.
    
    : param: USE_OUT_OF_BAG_ERROR = True. Parameter oob_score of the model.
      Whether to use out-of-bag (OOB) samples to estimate the generalization score. 
      Only available if BOOTSTRAP_SAMPLES = True.
        
      Importantly: random forest combines several decision trees, by randomnly selecting
      variables for making the tree leafs and nodes; and ramdonly setting the depth of
      the trees. The use of out-of-bag guarantees that the data used for the construction
      of the trees is randomly selected.
      If not using, the calculated metrics will be over estimated.
      This phenomenon is characteristic from ensemble algorithms like random forests, and
      is not usually observed on linear regressions.
    """    
    
    RANDOM_STATE = 55 
    ## We will pass it to every sklearn call so we ensure reproducibility (i.e., a new random process)
    
    # Start a summary dictionary:
    summary_dict = {}
    
    # check if use_out_of_bag_error = True but bootstrap_samples is False:
    if ((bootstrap_samples == False) & (use_out_of_bag_error == True)):
        
        print("Out-of-bag errors can only be used when bootstrap is True. Then, changing the value of bootstrap_samples.")
        
        bootstrap_samples = True
    
    if (type_of_problem == "regression"):
        
        from sklearn.ensemble import RandomForestRegressor
        # Create an instance (object) from the class RandomForestRegressor()
        # Pass the appropriate parameters to the class constructor:
        rf_model = RandomForestRegressor(n_estimators = number_of_trees, random_state = RANDOM_STATE, max_depth = max_tree_depth, min_samples_split = min_samples_to_split_node, min_samples_leaf = min_samples_to_make_leaf, bootstrap = bootstrap_samples, oob_score = use_out_of_bag_error)
        # verbose = 1 for debug mode (show training process details)
        
    elif (type_of_problem == "classification"):
        
        from sklearn.ensemble import RandomForestClassifier
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
        
        # Create an instance (object) from the class RandomForestClassifier()
        # Pass the appropriate parameters to the class constructor:
        rf_model = RandomForestClassifier(n_estimators = number_of_trees, random_state = RANDOM_STATE, max_depth = max_tree_depth, min_samples_split = min_samples_to_split_node, min_samples_leaf = min_samples_to_make_leaf, bootstrap = bootstrap_samples, oob_score = use_out_of_bag_error)
        # verbose = 1 for debug mode (show training process details)

        
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
    
    rf_model = rf_model.fit(X_train, reshaped_y_train)
    
    
    if (use_out_of_bag_error): # runs only if the boolean is True
        
        print("OOB Score: score of the training dataset obtained using an out-of-bag estimate = ")
        print(rf_model.oob_score_)
        print("\n")
    
    # Get predictions for training, testing, and validation:
    y_preds_for_train = rf_model.predict(X_train)

    if ((X_test is not None) & ((y_test is not None))):
        y_preds_for_test = rf_model.predict(X_test)

    else:
        y_preds_for_test = None

    if ((X_valid is not None) & ((y_valid is not None))):
        y_preds_for_validation = rf_model.predict(X_valid)

    else:
        y_preds_for_validation = None

    # instantiate the model checker object:
    model_check = ModelChecking(model_object = rf_model, model_type = type_of_problem, model_package = 'sklearn', column_map_dict = column_map_dict, X = X_train, y_train = y_train, y_preds_for_train = y_preds_for_train, y_test = y_test, y_preds_for_test = y_preds_for_test, y_valid = y_valid, y_preds_for_validation = y_preds_for_validation)
        
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
    
    print("\n") #line break
    print("To reveal the decision path in the forest for a sample X, call the .decision_path method of the random forest model object. For example, declare:")
    print("path = rf_model.decision_path(X)")
    print("And then print path.")
    
    print("\n") #line break
    print("To predict the model output y_pred for a dataframe X, declare: y_pred = rf_model.predict(X)\n")
    print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
    print("X_train = np.reshape(np.array(X_train), (-1, 1))")
    # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362
    
    if (type_of_problem == 'classification'):
        
        print("To predict the probabilities associated to each class for the set X_train, use the .predict_proba(X) method:")
        print("y_pred_probabilities = rf_model.predict_proba(X_train)")

    return rf_model, summary_dict


def xgboost_model (X_train, y_train, type_of_problem = "regression", number_of_trees = 128, max_tree_depth = None, percent_of_training_set_to_subsample = 75, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    xgboost_model (X_train, y_train, type_of_problem = "regression", number_of_trees = 128, max_tree_depth = None, percent_of_training_set_to_subsample = 75, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330)

    - Boosting ensemble of decision trees.
    - Each new tree is trained preferentially with data for which the previous trees had difficulty on making good predictions (i.e., these data receives higher weights of importance).
    - This algorithm usally performs better than Random Forests.
    
    This function runs the 'bar_chart' function.
    check XGBoost documentation:
     https://xgboost.readthedocs.io/en/stable/python/python_api.html?highlight=xgbregressor#xgboost.XGBRegressor


    : param: X_train = subset of predictive variables (dataframe).
    : param: y_train = subset of response variable (series).
    
    : param: TYPE_OF_PROBLEM = 'regression'; or TYPE_OF_PROBLEM = 'classification'
      The default is 'regression', which will be used if no type is
      provided.
    
    : param: number_of_trees = 128 (integer) - number of gradient boosted trees. 
      Equivalent to number of boosting rounds.
      it is the n_estimators parameter of the model.
      Usually, a number from 64 to 128 is used.
    
    : param: max_tree_depth = None - integer representing the maximum depth 
      permitted for the trees (base learners).
    
    : param: percent_of_training_set_to_subsample = 75 (float or None).
      If this value is set, it defines the percent of data that will be ramdonly
      selected for training the models.
      e.g. percent_of_training_set_to_subsample = 80 uses 80% of the data. If None,
      it uses the whole training set (100%)
    
      ## When subsampling, training data is divided into several subsets, and these
         subsets are used for separately training the model.
      # Importantly: random forest and XGBoost combine several decision trees, by randomnly selecting
        variables for making the tree leafs and nodes; and ramdonly setting the depth of
        the trees. The use of this strategy guarantees that the data used for the construction
        of the trees is randomly selected.
        If not using, the model will be highly susceptive of overfitting due to the use of
        the whole dataset. Also, the calculated metrics will be over estimated.
      
      This phenomenon is characteristic from ensemble algorithms like random forests, and
      XGBoost, and is not usually observed on linear regressions.
    """
    
    RANDOM_STATE = 55 
    ## We will pass it to every sklearn call so we ensure reproducibility (i.e., a new random process)
        
    # Start a summary dictionary:
    summary_dict = {}
    
    # check if percent_of_training_set_to_subsample is between 0 and 100%:
    if (0 <= percent_of_training_set_to_subsample <= 100):
        
        # convert the percent into the fraction_to_subsample
        fraction_to_subsample = (percent_of_training_set_to_subsample)/100
    
    else:
        # None or invalid value was provided
        print("None or invalid percent of dataset to subsample was provided. Then, the whole training set will be used.")
        
        fraction_to_subsample = 1.0 #total fraction, set as float
    
    if (type_of_problem == "regression"):

        from xgboost import XGBRegressor
        # Create an instance (object) from the class RandomForestRegressor()
        # Pass the appropriate parameters to the class constructor:
        xgb_model = XGBRegressor(n_estimators = number_of_trees, random_state = RANDOM_STATE, max_depth = max_tree_depth, subsample = fraction_to_subsample)
        # verbosity = 3 for debug mode (show training details)
        
    elif (type_of_problem == "classification"):
        
        from xgboost import XGBClassifier
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
        
        # Create an instance (object) from the class RandomForestClassifier()
        # Pass the appropriate parameters to the class constructor:
        xgb_model = XGBClassifier(n_estimators = number_of_trees, random_state = RANDOM_STATE, max_depth = max_tree_depth, subsample = fraction_to_subsample)
        # verbosity = 3 for debug mode (show training details)
        
    else:
        
        raise InvalidInputsError ("Enter a valid type of problem, \'regression\' or \'classification\'.")
    
    
    # XGBoost requires a 1-dimensional vector for training the classifier.
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
    
    xgb_model = xgb_model.fit(X_train, reshaped_y_train)
    
    
    # Get predictions for training, testing, and validation:
    y_preds_for_train = xgb_model.predict(X_train)

    if ((X_test is not None) & ((y_test is not None))):
        y_preds_for_test = xgb_model.predict(X_test)

    else:
        y_preds_for_test = None

    if ((X_valid is not None) & ((y_valid is not None))):
        y_preds_for_validation = xgb_model.predict(X_valid)

    else:
        y_preds_for_validation = None

    # instantiate the model checker object:
    model_check = ModelChecking(model_object = xgb_model, model_type = type_of_problem, model_package = 'xgboost', column_map_dict = column_map_dict, X = X_train, y_train = y_train, y_preds_for_train = y_preds_for_train, y_test = y_test, y_preds_for_test = y_preds_for_test, y_valid = y_valid, y_preds_for_validation = y_preds_for_validation)
        
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
    
    
    print("\n") #line break
    print("To predict the model output y_pred for a dataframe X, declare: y_pred = xgb_model.predict(X)\n")
    print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
    print("X_train = np.reshape(np.array(X_train), (-1, 1))")
    # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362
    
    if (type_of_problem == 'classification'):
        
        print("To predict the probabilities associated to each class for the set X_train, use the .predict_proba(X) method:")
        print("y_pred_probabilities = xgb_model.predict_proba(X_train)")

    return xgb_model, summary_dict
