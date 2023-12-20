import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf

from idsw.datafetch.core import InvalidInputsError
from .core import ModelChecking


def sklearn_ann (X_train, y_train, type_of_problem = "regression", number_of_hidden_layers = 1, number_of_neurons_per_hidden_layer = 64, size_of_training_batch = 200, maximum_of_allowed_iterations = 20000, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, metrics_vertical_axis_title = None, loss_vertical_axis_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    sklearn_ann (X_train, y_train, type_of_problem = "regression", number_of_hidden_layers = 1, number_of_neurons_per_hidden_layer = 64, size_of_training_batch = 200, maximum_of_allowed_iterations = 20000, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, metrics_vertical_axis_title = None, loss_vertical_axis_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    check MLPRegressor documentation on Scikit-learn:
     https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html?msclkid=b835e54ec17b11eca3d8febbc0eaeb3a
    check MLPClassifier documentation on Scikit-learn:
     https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html?msclkid=ecb380ebc17b11ec99b7b8f762c84eab
    
    : param: X_train = subset of predictive variables (dataframe).
    : param: y_train = subset of response variable (series).
    
    : param: TYPE_OF_PROBLEM = 'regression'; or TYPE_OF_PROBLEM = 'classification'
      The default is 'regression', which will be used if no type is
      provided.
    
    : param: number_of_hidden_layers = 1 - integer with the number of hidden
      layers. This number must be higher or equal to 1.
    
    : param: number_of_neurons_per_hidden_layer = 64 - integer containing the
      number of neurons in each hidden layer. Even though sklearn.neural_network
      accepts different layers sizes, passed as a list of integers where each
      value represents the neurons for one layer, this function works with layers
      of equal sizes.
    
      Scikit-learn MLPClassifier adjusts the size of the output layer to have
      a number of units (neurons) equals to the number of output classes. Then, we
      do not have to manually set this parameter.
    
    : param: size_of_training_batch (integer): amount of data used on each training cycle (epoch). 
      If we had 20000 data and size_of_training_batch = 200, then there would be 100 
      batches (cycles) using 200 data. Training is more efficient when dividing the data into 
      smaller subsets (batches) of ramdonly chosen data and separately training the model
      for each batch (in training cycles called epochs). Also, this helps preventing
      overfitting: if we use at once all data, the model is much more prone to overfit
      (memorizing effect), selecting non-general features highly specific from the data
      for the description of it. Therefore, it will have lower capability of predicting
      data for values it already did not observe.
      This is the parameter batch_size of most of the algorithms.
    
    : param: MAXIMUM_OF_ALLOWED_ITERATIONS = integer representing the maximum number of iterations
      that the optimization algorithm can perform. Depending on data, convergence may not be
      reached within this limit, so you may need to increase this hyperparameter.
    
      1. Let's configure the hidden layers. They are input as the parameter hidden_layer_sizes
      if only one value is provided, there will be only one hidden layer
      for more hidden layers, provide a list in hidden_layer_sizes. Each element
      of this list will be the number of neurons in each layer. Examples:
      hidden_layer_sizes  = 100 - a single hidden layer with 100 neurons
      hidden_layer_sizes=[100, 100] - 2 hidden layers with 100 neurons per layer
      hidden_layer_sizes=[100, 100, 100] - 3 hidden layers with 100 neurons per layer.
    """
    
    RANDOM_STATE = 55 
    ## We will pass it to every sklearn call so we ensure reproducibility (i.e., a new random process)
        
    if (number_of_hidden_layers == 1):
        
        # Simply copy the value input as number_of_neurons_per_hidden_layer
        HIDDEN_LAYER_SIZES = number_of_neurons_per_hidden_layer
        print(f"Multi-Layer Perceptron configured with a single hidden-layer containing {number_of_neurons_per_hidden_layer} neurons.")
    
    elif (number_of_hidden_layers > 1):
        
        # Start a list HIDDEN_LAYER_SIZES
        HIDDEN_LAYER_SIZES = [number_of_neurons_per_hidden_layer for i in range (0, number_of_hidden_layers)]
        # This list must have number of elements equals to number_of_hidden_layers
        # (i.e. one element per layer)
        
        print(f"Multi-Layer Perceptron configured with {number_of_hidden_layers} hidden-layers containing {number_of_neurons_per_hidden_layer} neurons.")

    else:
        
        raise InvalidInputsError ("Please, input a valid number of hidden layers. It must be an integer higher or equal to 1.")

    
    if (type_of_problem == "regression"):

        from sklearn.neural_network import MLPRegressor
        # Create an instance (object) from the class MLPRegressor()
        # Pass the appropriate parameters to the class constructor:
        mlp_model = MLPRegressor(hidden_layer_sizes = HIDDEN_LAYER_SIZES, activation = 'relu', solver = 'adam', batch_size = size_of_training_batch, max_iter = maximum_of_allowed_iterations, verbose = True, random_state = RANDOM_STATE)
        # 'relu' = ReLU, the Rectified Linear Unit function, returns f(x) = max(0, x)
        # (i.e., if x <=0, relu(x) = 0; if (x > 0), relu(x) = 0)
        # 'identity' or 'linear' is equivalent to the use of no-activation function (no-op activation)
        # It is useful to implement linear bottleneck - returns f(x) = x
        # use no activation function (in other words, 'linear' activation) for the output layer of a
        # regression problem.
        
        # verbose: sklearn default is False. Whether to print progress messages to stdout.
        
    elif (type_of_problem == "classification"):

        from sklearn.neural_network import MLPClassifier
        # Create an instance (object) from the class MLPClassifier()
        # Pass the appropriate parameters to the class constructor:
        mlp_model = MLPClassifier(hidden_layer_sizes = HIDDEN_LAYER_SIZES, activation = 'relu', solver = 'adam', batch_size = size_of_training_batch, max_iter = maximum_of_allowed_iterations, verbose = True, random_state = RANDOM_STATE)
    
    else:
        
        raise InvalidInputsError ("Enter a valid type of problem, \'Regression\' or \'Classification\'.")
    
    
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
    
    # Fit the model:
    mlp_model = mlp_model.fit(X_train, reshaped_y_train)
    
    if (mlp_model.n_iter_ == maximum_of_allowed_iterations):
        print("Warning! Total of iterations equals to the maximum allowed. It indicates that the convergence was not reached yet. Try to increase the maximum number of allowed iterations.")
    
    print(f"Finished fitting of the neural network with {mlp_model.n_layers_} after {mlp_model.n_iter_} iterations.")
    print(f"Minimum loss reached by the solver throughout fitting: mean squared error (MSE) = {mlp_model.best_loss_}.")
    print("\n")
    
    # Create the training history dictionary:
    # the MLP Regressor is trained using the mean squared error as the loss function to be optimized.
    mlp_training_history_dict = {'loss': mlp_model.loss_curve_}
    
    # Let's create a history object analogous to the one created by TensorFlow, to be used
    # for plotting the loss curve:
    class history_object:
        # Initialize instance attributes.
        # define the Class constructor, i.e., how are its objects:
        def __init__(self, history = mlp_training_history_dict):
            
            # TensorFlow creates an object with the history attribute. This attribute stores
            # the history dictionary:
            self.history = history
            # numpy.arange([start, ]stop, [step, ]dtype=None, *, like=None)
            # https://numpy.org/doc/stable/reference/generated/numpy.arange.html
            self.epoch = np.arange(0, len(history['loss']), 1, dtype = int)
            # EPOCHS START FROM ZERO
    
    # Instantiate the object:
    history = history_object(history = mlp_training_history_dict)
    # Now, it has the same format as the TensorFlow history.
    
    # Get predictions for training, testing, and validation:
    y_preds_for_train = mlp_model.predict(X_train)

    if ((X_test is not None) & ((y_test is not None))):
        y_preds_for_test = mlp_model.predict(X_test)

    else:
        y_preds_for_test = None

    if ((X_valid is not None) & ((y_valid is not None))):
        y_preds_for_validation = mlp_model.predict(X_valid)

    else:
        y_preds_for_validation = None
    
    
    # instantiate the model checker object:
    model_check = ModelChecking(model_object = mlp_model, model_type = type_of_problem, model_package = 'sklearn', column_map_dict = column_map_dict, training_history_object = history, X = X_train, y_train = y_train, y_preds_for_train = y_preds_for_train, y_test = y_test, y_preds_for_test = y_preds_for_test, y_valid = y_valid, y_preds_for_validation = y_preds_for_validation)
            
    # Calculate model metrics:
    model_check = model_check.model_metrics()
    # Retrieve model metrics:
    metrics_dict = model_check.metrics_dict

    print("\n")
    print("Check the loss curve below:\n")
    model_check = model_check.plot_training_history (metrics_name = 'mse', x_axis_rotation = x_axis_rotation, y_axis_rotation = y_axis_rotation, grid = grid, horizontal_axis_title = horizontal_axis_title, metrics_vertical_axis_title = metrics_vertical_axis_title, loss_vertical_axis_title = loss_vertical_axis_title, export_png = export_png, directory_to_save = directory_to_save, file_name = file_name, png_resolution_dpi = png_resolution_dpi)
    
    print("\n") # line break
    print("Note: If a proper number of epochs was used for training, then a final baseline (plateau) should be reached by the curve.\n")
    
    print("\n") #line break
    print("To predict the model output y_pred for a dataframe X, declare: y_pred = mlp_model.predict(X)\n")
    print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
    print("X_train = np.reshape(np.array(X_train), (-1, 1))")
    # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362
    
    if (type_of_problem == 'classification'):
        
        print("To predict the probabilities associated to each class for the set X_train, use the .predict_proba(X) method:")
        print("y_pred_probabilities = mlp_model.predict_proba(X_train)")
    
    
    return mlp_model, metrics_dict, history
