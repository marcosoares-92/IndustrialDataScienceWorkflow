import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf

from idsw import (InvalidInputsError, ControlVars)
from .core import (TfModels, ModelChecking, SiameseNetworks)


def get_deep_learning_tf_model (X_train, y_train, architecture = 'simple_dense', optimizer = None, X_test = None, y_test = None, X_valid = None, y_valid = None, type_of_problem = "regression", size_of_training_batch = 200, number_of_training_epochs = 2000, number_of_output_classes = 2, verbose = 1, column_map_dict = None, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, metrics_vertical_axis_title = None, loss_vertical_axis_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    get_deep_learning_tf_model (X_train, y_train, architecture = 'simple_dense', optimizer = None, X_test = None, y_test = None, X_valid = None, y_valid = None, type_of_problem = "regression", size_of_training_batch = 200, number_of_training_epochs = 2000, number_of_output_classes = 2, verbose = 1, column_map_dict = None, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, metrics_vertical_axis_title = None, loss_vertical_axis_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    : param: X_train = subset of predictive variables (dataframe).
    : param: y_train = subset of response variable (series).
    : param: X_test = subset of predictive variables (test dataframe).
    : param: y_test = subset of response variable (test series).
      The test parameters are passed as validation data, so they are necessary here.
    
    : param: architecture = 'simple_dense': tf_simple_dense model from class TfModels;
      architecture = 'double_dense': tf_double_dense model from class TfModels;
      architecture = 'cnn': tf_cnn time series model from class TfModels;
      architecture = 'lstm': tf_lstm time series model from class TfModels;
      architecture = 'encoder_decoder': encoder-decoder time series model from class TfModels;
      architecture = 'cnn_lstm': hybrid cnn-lstm time series model from class TfModels.
    
    : param: optimizer: tf.keras.optimizers.Optimizer object:
      keep it None to use the Adam optimizer.
      https://www.tensorflow.org/api_docs/python/tf/keras/optimizers
      https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/Optimizer
      use the object to set parameters such as learning rate and selection of the optimizer
    
    : param: TYPE_OF_PROBLEM = 'regression'; or TYPE_OF_PROBLEM = 'classification'
      The default is 'regression', which will be used if no type is
      provided.
    
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
    
    : param: number_of_training_epochs (integer): number of training cycles used. 
      This is the 'epochs' parameter of the algorithms.
    
    : param: number_of_output_classes = None - if TYPE_OF_PROBLEM = 'classification',
      this parameter should be specified as an integer. That is because the number of
      neurons in the output layer should be equal to the number of classes (1 neuron per
      possible class).
      If we simply took the number of different labels on the training data as the number
      of classes, there would be the risk that a given class is not present on the training
      set. So, it is safer (and less computer consuming) to input this number.
      For simplicity, you may simply set this parameter as the value
      number_of_classes returned from the function 'retrieve_classes_used_for_training'

      If there are only two classes, we use a last Dense(1) layer (only one neuron) activated
      through sigmoid: Dense(1, activation = 'sigmoid'). 
      This is equivalent to the logistic regression, generating an output between 0 and 1 
      (binary probability). The loss function, in this case, will be the 'binary_crossentropy'. 
      This is more efficient than using softmax.
    
      If there are more than two classes, then we set the number of neurons in Dense as
      number_of_output_classes, and activate the layer through 'softmax':  
      Dense(number_of_output_classes, activation = 'softmax')
      Softmax generates a probability distribution, calculates the probability for 
      each output and chooses the class with higher probability. The loss function depends on the
      number of classes. If we are working with few classes (<= 5), we can use 
      "categorical_crossentropy". If a higher number is used, we apply the 'sparse_categorical_crossentropy'
      All of the classification problems accept 'accuracy' as the metrics for training.
    
      For the regression problems, though, the output is a real value (i.e., a scalar). Then,
      the last layer should ALWAYS contain a single neuron. So, there is no meaning in
      specifying it as a parameter.
      Also, the loss used for evaluating regression problems cannot be the crossentropy.
      In these cases, we use the mean squared error (mse) instead. For the metrics,
      naturally there is no meaning in using 'accuracy'. So, we use 'RootMeanSquaredError'
      or 'mae' (mean absolute error).
    """

    # Create functions for specific reshaping
    def reshaper(architecture):
        if (architecture == 'cnn_lstm'):
            return (lambda x: np.array(x).reshape(x.shape[0], 2, 2, 1))
        elif ((architecture == 'cnn')|(architecture == 'lstm')|(architecture == 'encoder_decoder')):
            return (lambda x: np.array(x).reshape(x.shape[0], x.shape[1], 1))
        else:
            # return the array itself:
            return (lambda x: np.array(x))
    
    if (architecture == 'cnn_lstm'):
        # Get the hybrid cnn-lstm time series model from class TfModels:
        
        # Here, the sequence length or number of columns must be even: they will be grouped in pairs
        # Check if the number is even: % - remainder of the integer division
        if ((X_train.shape[1] % 2) != 0):
            # There is remainder of the division: the number of columns is not even
            print("This architecture requires the inputs to be reshape as pairs of numbers.")
            raise InvalidInputsError(f"Here, there are {X_train.shape[1]} columns or sequence elements. Drop one column to use this architecture.\n")
            
    
    # Put the arrays in the correct shape for the particular architecture
    reshape_function = reshaper(architecture)
    
    try:
        X_train = reshape_function(X_train)

        if ((X_test is not None) & (y_test is not None)):   
            X_test = reshape_function(X_test)
        if ((X_valid is not None) & (y_valid is not None)):   
            X_valid = reshape_function(X_valid)
    except:
        pass
    
    # Instantiate a TfModels object:
    tf_model_obj = TfModels(X_train = X_train, y_train = y_train, X_valid = X_test, y_valid = y_test, type_of_problem = type_of_problem, number_of_classes = number_of_output_classes, optimizer = optimizer)
    
    if (architecture == 'double_dense'):
        # Get the tf_cnn time series model from class TfModels:
        tf_model_obj = tf_model_obj.tf_double_dense(epochs = number_of_training_epochs, batch_size = size_of_training_batch, verbose = verbose)
    
    elif (architecture == 'cnn'):
        # Get the tf_cnn time series model from class TfModels:
        tf_model_obj = tf_model_obj.tf_cnn_time_series(epochs = number_of_training_epochs, batch_size = size_of_training_batch, verbose = verbose)
        
    
    elif (architecture == 'lstm'):
        # Get the tf_lstm time series model from class TfModels:
        tf_model_obj = tf_model_obj.tf_lstm_time_series(epochs = number_of_training_epochs, batch_size = size_of_training_batch, verbose = verbose)
    
    elif (architecture == 'encoder_decoder'):
        # Get the encoder-decoder time series model from class TfModels:
        tf_model_obj = tf_model_obj.tf_encoder_decoder_time_series(epochs = number_of_training_epochs, batch_size = size_of_training_batch, verbose = verbose)
    
    elif (architecture == 'cnn_lstm'):
        
        tf_model_obj = tf_model_obj.tf_cnn_lstm_time_series(epochs = number_of_training_epochs, batch_size = size_of_training_batch, verbose = verbose)
    
    else:
        # Get the tf_simple_dense model from class TfModels:
        tf_model_obj = tf_model_obj.tf_simple_dense(epochs = number_of_training_epochs, batch_size = size_of_training_batch, verbose = verbose)

    # Retrieve the model and the history:
    model = tf_model_obj.model
    history = tf_model_obj.history
    
    # Get predictions for training, testing, and validation:
    y_preds_for_train = np.array(model.predict(X_train))
    total_dimensions = len(y_preds_for_train.shape)
    
    if (architecture == 'encoder_decoder'):
        # Since return_sequences = True, the model returns arrays containing two elements. We must pick only
        # the first position (index 0) of 2nd dimension
        y_preds_for_train = y_preds_for_train[:,0]
        total_dimensions = len(y_preds_for_train.shape)
    
    last_dim = y_preds_for_train.shape[(total_dimensions - 1)] # indexing starts from zero
    if (last_dim == 1): # remove last dimension
        if (total_dimensions == 4):
            y_preds_for_train = y_preds_for_train[:,:,:,0]
        elif (total_dimensions == 3):
            y_preds_for_train = y_preds_for_train[:,:,0]
        elif (total_dimensions == 2):
            y_preds_for_train = y_preds_for_train[:,0]
    
    if ((X_test is not None) & ((y_test is not None))):
        if ((len(X_test) > 0) & ((len(y_test) >0))):
            y_preds_for_test = np.array(model.predict(X_test))
            last_dim = y_preds_for_test.shape[(total_dimensions - 1)]
            if (architecture == 'encoder_decoder'):
                y_preds_for_test = y_preds_for_test[:,0]
            if (last_dim == 1): # remove last dimension
                if (total_dimensions == 4):
                    y_preds_for_test = y_preds_for_test[:,:,:,0]
                elif (total_dimensions == 3):
                    y_preds_for_test = y_preds_for_test[:,:,0]
                elif (total_dimensions == 2):
                    y_preds_for_test = y_preds_for_test[:,0]
        
        else:
            X_test, y_test, y_preds_for_test = None, None, None

    else:
        y_preds_for_test = None

    if ((X_valid is not None) & ((y_valid is not None))):
        if ((len(X_valid) > 0) & ((len(X_valid) >0))):
            y_preds_for_validation = np.array(model.predict(X_valid))
            last_dim = y_preds_for_validation.shape[(total_dimensions - 1)]
            if (architecture == 'encoder_decoder'):
                y_preds_for_validation = y_preds_for_validation[:,0]
            if (last_dim == 1): # remove last dimension
                if (total_dimensions == 4):
                    y_preds_for_validation = y_preds_for_validation[:,:,:,0]
                elif (total_dimensions == 3):
                    y_preds_for_validation = y_preds_for_validation[:,:,0]
                elif (total_dimensions == 2):
                    y_preds_for_validation = y_preds_for_validation[:,0]
        
        else:
            X_valid, y_valid, y_preds_for_validation = None, None, None

    else:
        y_preds_for_validation = None
    
    # instantiate the model checker object:
    model_check = ModelChecking(model_object = model, model_type = type_of_problem, model_package = 'tensorflow', column_map_dict = column_map_dict, training_history_object = history, X = X_train, y_train = y_train, y_preds_for_train = y_preds_for_train, y_test = y_test, y_preds_for_test = y_preds_for_test, y_valid = y_valid, y_preds_for_validation = y_preds_for_validation)
            
    # Calculate model metrics:
    model_check = model_check.model_metrics()
    
    if ControlVars.show_results:
        try:
            # Retrieve model metrics:
            metrics_dict = model_check.metrics_dict
        
        except:
            print("Unable to retrieve metrics.\n")

        print("Check the training loss and metrics curve below:\n")
        print("Regression models: metrics = MAE; loss = MSE.")
        print("Classification models: metrics = accuracy; loss = crossentropy (binary or sparse categorical).\n")
    
    model_check = model_check.plot_training_history (metrics_name = model_check.metrics_name, x_axis_rotation = x_axis_rotation, y_axis_rotation = y_axis_rotation, grid = grid, horizontal_axis_title = horizontal_axis_title, metrics_vertical_axis_title = metrics_vertical_axis_title, loss_vertical_axis_title = loss_vertical_axis_title, export_png = export_png, directory_to_save = directory_to_save, file_name = file_name, png_resolution_dpi = png_resolution_dpi)
    if ControlVars.show_results:
        print("\n")
        
        print("Notice that:")
        print("1. If the loss did not reach a stable final baseline (a plateau), then the number of epochs should be increased. The ideal number of epochs is the minimum needed for reaching the final baseline. Increasing the number of epochs after this moment only increases the computational costs, without gain of performance.")
        print("2. A great mismatch between the curves indicates overfitting. This may be noticed as a gain of performance by the training curve (loss reduction or increase on accuracy) without correspondent improvement on the validation set performance (e.g. the validation metrics reaches a baseline very lower than the training curve).")
        print("If your data is overfitting, you can modify the sizes of training and test sets, modify the hyperparameters, or add a Dropout hidden-layer.")
        print("Adding dropout is common for image classification problems. The syntax for declaring the layer is:")
        print("tf.keras.layers.Dropout(0.5)")
        print("In this example, we added Dropout(0.5). It means that you lose 50\% of nodes. If using Dropout(0.2), you would lose 20\% of nodes.")
        print("Dropout helps avoiding overfitting because neighbor neurons can have similar weights, and thus can skew the final training.")
        print("If you set a too high dropout rate, the network will lose specialization to the effect that it would be inefficient or ineffective at learning, driving accuracy down.")
        print("\n") # line break
        
        print("\n") #line break
        print("To predict the model output y_pred for a dataframe X, declare: y_pred = model.predict(X)\n")
        print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
        print("X_train = np.reshape(np.array(X_train), (-1, 1))")
        # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362
        print("Attention: for classification with Keras/TensorFlow, this output will not be a class, but an array of probabilities correspondent to the probability that the entry belongs to each class.")
        print("The output class from the deep learning model is the class with higher probability indicated by the predict method. Again, the order of classes is the order they appear in the training dataset. For instance, when using the ImageDataGenerator, the 1st class is the name of the 1st read directory, the 2nd class is the 2nd directory, and so on.")
            
    return model, metrics_dict, history


def get_siamese_networks_model (X_train, y_train, output_dictionary, architecture = 'simple_dense', optimizer = None, X_test = None, y_test = None, X_valid = None, y_valid = None, size_of_training_batch = 200, number_of_training_epochs = 2000, verbose = 1, column_map_dict = None, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, metrics_vertical_axis_title = None, loss_vertical_axis_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    get_siamese_networks_model (X_train, y_train, output_dictionary, architecture = 'simple_dense', optimizer = None, X_test = None, y_test = None, X_valid = None, y_valid = None, size_of_training_batch = 200, number_of_training_epochs = 2000, verbose = 1, column_map_dict = None, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, metrics_vertical_axis_title = None, loss_vertical_axis_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    : param: X_train = subset of predictive variables (dataframe).
    : param: y_train = subset of response variable (series).
    : param: X_test = subset of predictive variables (test dataframe).
    : param: y_test = subset of response variable (test series).
      The test parameters are passed as validation data, so they are necessary here.
    
    : param: architecture = 'simple_dense': base_model_simple_dense from class SiameseNetworks;
      architecture = 'double_dense': base_model_double_dense from class SiameseNetworks;
      architecture = 'cnn': base_model_cnn_time_series from class SiameseNetworks;
      architecture = 'lstm': base_model_lstm_time_series from class SiameseNetworks;
      architecture = 'encoder_decoder': base_model_encoder_decoder_time_series from class SiameseNetworks;
      architecture = 'cnn_lstm': hybrid base_model_cnn_lstm_time_series from class SiameseNetworks.
    
    : param: optimizer: tf.keras.optimizers.Optimizer object:
      keep it None to use the Adam optimizer.
      https://www.tensorflow.org/api_docs/python/tf/keras/optimizers
      https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/Optimizer
      use the object to set parameters such as learning rate and selection of the optimizer
    
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
    
    : param: number_of_training_epochs (integer): number of training cycles used. 
      This is the 'epochs' parameter of the algorithms.


    : output: output_dictionary:
     output_dictionary structure:
     {'response_variable': {
     'type': 'regression', 'number_of_classes':}}
     'response_variable': name of the column used as response for one of the outputs. This key
     gives access to the nested dictionary containing the following keys: 
     'type': type of problem. Must contain the string 'regression' or 'classification';
     'number_of_classes': integer. This key may not be declared for regression problems. Do not
     include the key, set as 1, or set the number of classes used for training.
    """
    
    # Create functions for specific reshaping
    def reshaper(architecture):
        if (architecture == 'cnn_lstm'):
            return (lambda x: np.array(x).reshape(x.shape[0], 2, 2, 1))
        elif ((architecture == 'cnn')|(architecture == 'lstm')|(architecture == 'encoder_decoder')):
            return (lambda x: np.array(x).reshape(x.shape[0], x.shape[1], 1))
        else:
            # return the array itself:
            return (lambda x: np.array(x))

    if (architecture == 'cnn_lstm'):
        # Get the hybrid cnn-lstm time series model:
        
        # Here, the sequence length or number of columns must be even: they will be grouped in pairs
        # Check if the number is even: % - remainder of the integer division
        if ((X_train.shape[1] % 2) != 0):
            # There is remainder of the division: the number of columns is not even
            print("This architecture requires the inputs to be reshape as pairs of numbers.")
            raise InvalidInputsError(f"Here, there are {X_train.shape[1]} columns or sequence elements. Drop one column to use this architecture.\n")

    
    # Put the arrays in the correct shape for the particular architecture
    reshape_function = reshaper(architecture)
    
    try:
        X_train = reshape_function(X_train)

        if ((X_test is not None) & (y_test is not None)):   
            X_test = reshape_function(X_test)
        if ((X_valid is not None) & (y_valid is not None)):   
            X_valid = reshape_function(X_valid)
    except:
        pass
        
    # Instantiate a SiameseNetworks object:
    siamese_networks_obj = SiameseNetworks(output_dictionary = output_dictionary, X_train = X_train, y_train = y_train, X_valid = X_test, y_valid = y_test)
    
    # Compile the model:
    siamese_networks_obj = siamese_networks_obj.compile_model(architecture = architecture, optimizer = optimizer)
    
    # Fit the model:
    siamese_networks_obj = siamese_networks_obj.fit_model(epochs = number_of_training_epochs, batch_size = size_of_training_batch, verbose = verbose)
    
    # Retrieve model and the history from model and history attributes:
    model = siamese_networks_obj.model
    history = siamese_networks_obj.history
    
    
    # Get predictions for training, testing, and validation:
    y_preds_for_train = np.array(model.predict(X_train))
    
    total_dimensions = len(y_preds_for_train.shape)
    
    if (architecture == 'encoder_decoder'):
        # Since return_sequences = True, the model returns arrays containing two elements. We must pick only
        # the first position (index 0) of 2nd dimension
        # This array has dimensions like (4, 48, 2, 1) for a 4-response model output.
        # Notice that the 3rd dimension contains 2 dimensions, due to the parameter return_sequences = True.
        # We want only the first value correspondent to this dimension.
        # Also, notice that a single response model would have dimensions as (48, 2, 1), and the extra dimension
        # correspondent to return_sequences = True would be the 2nd dim.
        # Pick only the first value from third dimension:
        y_preds_for_train = y_preds_for_train[:,:,0]
        total_dimensions = len(y_preds_for_train.shape)
    
    last_dim = y_preds_for_train.shape[(total_dimensions - 1)] # indexing starts from zero
    if (last_dim == 1): # remove last dimension
        if (total_dimensions == 4):
            y_preds_for_train = y_preds_for_train[:,:,:,0]
        elif (total_dimensions == 3):
            y_preds_for_train = y_preds_for_train[:,:,0]
        elif (total_dimensions == 2):
            y_preds_for_train = y_preds_for_train[:,0]
    
    if ((X_test is not None) & ((y_test is not None))):
        if ((len(X_test) > 0) & ((len(y_test) >0))):
            y_preds_for_test = np.array(model.predict(X_test))
            last_dim = y_preds_for_test.shape[(total_dimensions - 1)]
            if (architecture == 'encoder_decoder'):
                y_preds_for_test = y_preds_for_test[:,:,0]
            if (last_dim == 1): # remove last dimension
                if (total_dimensions == 4):
                    y_preds_for_test = y_preds_for_test[:,:,:,0]
                elif (total_dimensions == 3):
                    y_preds_for_test = y_preds_for_test[:,:,0]
                elif (total_dimensions == 2):
                    y_preds_for_test = y_preds_for_test[:,0]
        
        else:
            X_test, y_test, y_preds_for_test = None, None, None

    else:
        y_preds_for_test = None

    if ((X_valid is not None) & ((y_valid is not None))):
        if ((len(X_valid) > 0) & ((len(X_valid) > 0))):
            y_preds_for_validation = np.array(model.predict(X_valid))
            last_dim = y_preds_for_validation.shape[(total_dimensions - 1)]
            if (architecture == 'encoder_decoder'):
                y_preds_for_validation = y_preds_for_validation[:,:,0]
            if (last_dim == 1): # remove last dimension
                if (total_dimensions == 4):
                    y_preds_for_validation = y_preds_for_validation[:,:,:,0]
                elif (total_dimensions == 3):
                    y_preds_for_validation = y_preds_for_validation[:,:,0]
                elif (total_dimensions == 2):
                    y_preds_for_validation = y_preds_for_validation[:,0]
        
        else:
            X_valid, y_valid, y_preds_for_validation = None, None, None

    else:
        y_preds_for_validation = None
    
    model_check = ModelChecking(model_object = model, model_package = 'tensorflow', column_map_dict = column_map_dict, training_history_object = history, X = X_train, y_train = y_train, y_preds_for_train = y_preds_for_train, y_test = y_test, y_preds_for_test = y_preds_for_test, y_valid = y_valid, y_preds_for_validation = y_preds_for_validation)
    
    model_check = model_check.model_metrics_multiresponses (output_dictionary = output_dictionary)
    
    try:
        # Retrieve model metrics:
        metrics_dict = model_check.metrics_dict
    except:
        print("Unable to retrieve metrics.\n")
    
    if ControlVars.show_results:
        print("Check the training loss and metrics curve below:\n")
        print("Regression models: metrics = MAE; loss = MSE.")
        print("Classification models: metrics = accuracy; loss = crossentropy (binary or sparse categorical).\n")
        
    model_check = model_check.plot_history_multiresponses (x_axis_rotation = x_axis_rotation, y_axis_rotation = y_axis_rotation, grid = grid, horizontal_axis_title = horizontal_axis_title, metrics_vertical_axis_title = metrics_vertical_axis_title, loss_vertical_axis_title = loss_vertical_axis_title, export_png = export_png, directory_to_save = directory_to_save, file_name = file_name, png_resolution_dpi = png_resolution_dpi)
    
    
    if ControlVars.show_results:
        print("\n")

        print("Notice that:")
        print("1. If the loss did not reach a stable final baseline (a plateau), then the number of epochs should be increased. The ideal number of epochs is the minimum needed for reaching the final baseline. Increasing the number of epochs after this moment only increases the computational costs, without gain of performance.")
        print("2. A great mismatch between the curves indicates overfitting. This may be noticed as a gain of performance by the training curve (loss reduction or increase on accuracy) without correspondent improvement on the validation set performance (e.g. the validation metrics reaches a baseline very lower than the training curve).")
        print("If your data is overfitting, you can modify the sizes of training and test sets, modify the hyperparameters, or add a Dropout hidden-layer.")
        print("Adding dropout is common for image classification problems. The syntax for declaring the layer is:")
        print("tf.keras.layers.Dropout(0.5)")
        print("In this example, we added Dropout(0.5). It means that you lose 50\% of nodes. If using Dropout(0.2), you would lose 20\% of nodes.")
        print("Dropout helps avoiding overfitting because neighbor neurons can have similar weights, and thus can skew the final training.")
        print("If you set a too high dropout rate, the network will lose specialization to the effect that it would be inefficient or ineffective at learning, driving accuracy down.")
        print("\n") # line break
        
        print("\n") #line break
        print("To predict the model output y_pred for a dataframe X, declare: y_pred = model.predict(X)\n")
        print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
        print("X_train = np.reshape(np.array(X_train), (-1, 1))")
        # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362
        print("Attention: for classification with Keras/TensorFlow, this output will not be a class, but an array of probabilities correspondent to the probability that the entry belongs to each class.")
        print("The output class from the deep learning model is the class with higher probability indicated by the predict method. Again, the order of classes is the order they appear in the training dataset. For instance, when using the ImageDataGenerator, the 1st class is the name of the 1st read directory, the 2nd class is the 2nd directory, and so on.")

    
    return model, metrics_dict, history
