def make_model_predictions (model_object, X, dataframe_for_concatenating_predictions = None, column_with_predictions_suffix = None, function_used_for_fitting_dl_model = 'get_deep_learning_tf_model', architecture = None, list_of_responses = []):
    """
    make_model_predictions (model_object, X, dataframe_for_concatenating_predictions = None, column_with_predictions_suffix = None, function_used_for_fitting_dl_model = 'get_deep_learning_tf_model', architecture = None, list_of_responses = []):
    
      The function will automatically detect if it is dealing with lists, NumPy arrays
      or Pandas dataframes. If X is a list or a single-dimension array, predict_for
      will be set as 'single_entry'. If X is a multi-dimension NumPy array (as the
      outputs for preparing data - even single_entry - for deep learning models), or if
      it is a Pandas dataframe, the function will set predict_for = 'subset'
    
    : param: X = subset of predictive variables (dataframe, NumPy array, or list).
    : param: If PREDICT_FOR = 'single_entry', X should be a list of parameters values.
      e.g. X = [1.2, 3, 4] (dot is the decimal case separator, comma separate values). 
      Notice that the list should contain only the numeric values, in the same order of the
      correspondent columns.
      If PREDICT_FOR = 'subset' (prediction for multiple entries), X should be a dataframe 
      (subset) or a multi-dimensional NumPy array of the parameters values, as usual.
    
    : param: model_object: object containing the model that will be analyzed. e.g.
      model_object = elastic_net_linear_reg_model
    
    : param: dataframe_for_concatenating_predictions: if you want to concatenate the predictions
      to a dataframe, pass it here:
      e.g. dataframe_for_concatenating_predictions = df
      If the dataframe must be the same one passed as X, repeat the dataframe object here:
      X = dataset, dataframe_for_concatenating_predictions = dataset.
      Alternatively, if dataframe_for_concatenating_predictions = None, 
      the prediction will be returned as a series or NumPy array, depending on the input format.
      Notice that the concatenated predictions will be added as a new column.
    
    : param: column_with_predictions_suffix = None. If the predictions are added as a new column
      of the dataframe dataframe_for_concatenating_predictions, you can declare this
      parameter as string with a suffix for identifying the model. If no suffix is added, the new
      column will be named 'y_pred'.
      e.g. column_with_predictions_suffix = '_keras' will create a column named "y_pred_keras". This
      parameter is useful when working with multiple models. Always start the suffix with underscore
      "_" so that no blank spaces are added; the suffix will not be merged to the column; and there
      will be no confusion with the dot (.) notation for methods, JSON attributes, etc.
    
    : param: function_used_for_fitting_dl_model: the function you used for obtaining the deep learning model.
      Example: 'get_deep_learning_tf_model' or 'get_siamese_networks_model'
    
    : param: architecture: some models require inputs in a proper format. Declare here if you are using
      one of these architectures. Example: architecture = 'cnn_lstm' from class TfModels require
      a special reshape before getting predictions. You can keep None or put the name of the
      architecture, if no special reshape is needed.
    
    : param: list_of_responses = []. This parameter is obbligatory for multi-response models, such as the ones obtained from
      function 'get_siamese_networks_model'. It must contain a list with the same order of the output responses.
      Example: suppose your siamese model outputs 4 responses: 'temperature', 'pressure', 'flow_rate', and 'ph', in
      this order. The list of responses must be declared as: 
      list_of_responses = ['temperature', 'pressure', 'flow_rate', 'ph']
      tuples and numpy arrays are also acceptable: list_of_responses = ('temperature', 'pressure', 'flow_rate', 'ph')
      Attention: the number of responses must be exactly the number of elements in list_of_responses, or an error will
      be raised.
    """
    import tensorflow as tf
    
    # Create functions for specific reshaping
    def reshaper(architecture):
        # Use the str function in case user input None or a number as architecture
        if (str(architecture) == 'cnn_lstm'):
            return (lambda x: np.array(x).reshape(x.shape[0], 2, 2, 1))
        elif ((str(architecture) == 'cnn')|(str(architecture) == 'lstm')|(str(architecture) == 'encoder_decoder')):
            return (lambda x: np.array(x).reshape(x.shape[0], x.shape[1], 1))
        else: # includes architecture is None
            # return the array itself:
            return (lambda x: np.array(x))
    
    
    # Put the arrays in the correct shape for the particular architecture
    reshape_function = reshaper(architecture)
    try:
        X = reshape_function(X)
    except:
        pass
    
    # start a response dictionary:
    response_dict = {}

    """
    # Check the type of input: if we are predicting the output for a subset (NumPy array reshaped
        for deep learning models or Pandas dataframe); or predicting for a single entry (single-
        dimension NumPy array or Python list).
    
    1. Check if a list was input. Lists do not have the attribute shape, present in dataframes
         and NumPy arrays. Accessing the attribute shape from a list will raise the Exception error
         named AttributeError
         Try to access the attribute shape. If the error AttributeError is raised, it is a list, so
         set predict_for = 'single_entry':
    """
    # Run even if it come from list or tuple:
    if (len(X.shape) == 1):
        # If X.shape has len == 1, it is a tuple like (4,)
        # Convert the numpy array to the correct shape. It runs even if the list or tuple was
        # converted.
        X = X.reshape(1, -1)
        # generates an array like array([[1, 2, 3, 4]])
        # The reshape (-1, 1) generates an array like ([1], [2], ...) with format for the y-vector
        # used for training.
    
    # Total of entries in the dataset:
    # Get the total of values for the first response, by isolating the index 0 of 2nd dimension
    total_data = len(X)
    
    if (len(list_of_responses) == 0):
        total_of_responses = 1
    else:
        total_of_responses = len(list_of_responses)
        
    print(f"Predicting {total_of_responses} responses for a total of {total_data} entries.\n")
    
    # prediction for a subset
    y_pred = np.array(model_object.predict(X))
    print("Attention: for classification with Keras/TensorFlow and other deep learning frameworks, this output will not be a class, but an array of probabilities correspondent to the probability that the entry belongs to each class. In this case, it is better to use the function calculate_class_probability below, setting model_type == \'deep_learning\'. This function will result into dataframes containing the classes as columns and the probabilities in the respective row.\n")
    print("The output class from the deep learning model is the class with higher probability indicated by the predict method. Again, the order of classes is the order they appear in the training dataset. For instance, when using the ImageDataGenerator, the 1st class is the name of the 1st read directory, the 2nd class is the 2nd directory, and so on.\n")
    
    total_dimensions = len(y_pred.shape)
    last_dim = y_pred.shape[(total_dimensions - 1)] # indexing starts from zero
    
    # If y_pred came from a RNN with the parameter return_sequences = True and/or
    # return_states = True, then the hidden and/or cell states from the LSTMs
    # were returned. So, the returned array has at least one extra dimensions (two
    # if both parameters are True). On the other hand, we want only the first dimension,
    # correspondent to the actual output.
        
    # Remember that, due to the reshapes for preparing data for deep learning models,
    # y_pred must have at least 2 dimensions: (N, 1), where N is the number of rows of
    # the original dataset. But y_pred returned from a model with return_sequences = True
    # or return_states = True will be of dimension (N, N, 1). If both parameters are True,
    # the dimension is (N, N, N, 1), since there are extra arrays for both the hidden and
    # cell states.
        
    # The conclusion is that there is a third dimension only for models where return_sequences
    # = True or return_states = True
    
    if (function_used_for_fitting_dl_model == 'get_siamese_networks_model'):
        
        y_pred_array = y_pred # save in another variable for re-using later
        
        # If the prediction was generated from a 3D-tensor, it may have 4 dimensions, with the last dimension
        # equals to 1. So, let's check this possibility (y_pred_array.shape is a tuple):
        try:
            if ((len(y_pred_array.shape) == 4) & (y_pred_array.shape[3] == 1)):
                    # Pick only first index from last dimension:
                    y_pred_array = y_pred_array[:,:,:,0]
        except:
            pass
            
        try:
            # Either if it was processed through previous if-statement or if it came from a 2D-tensor, 
            # it may have a third dimension equals to 1:
            if ((len(y_pred_array.shape) == 3) & (y_pred_array.shape[2] == 1)):
                # Pick only first index from last dimension:
                y_pred_array = y_pred_array[:,:,0]
        except:
            pass
            
        try:
            y_pred_array = y_pred_array.reshape(total_data, total_of_responses)
            dim = 1
                # the variable dim maps the position of the shape tuple correspondent to the total of responses
        except:
            # let's assume that the first dimension (index 0) is the total_of_responses
            dim = 0
                
            # check the dimension correspondent to the total of responses, and correct it if it
            # is not zero:
            for tuple_index, tuple_value in enumerate(y_pred_array.shape):
                if(tuple_value == total_of_responses):
                    dim = tuple_index
        
        if (architecture == 'encoder_decoder'):
            # Since return_sequences = True, the model returns arrays containing two elements. We must pick only
            # the first position (index 0) of 2nd dimension
            # This array has dimensions like (4, 48, 2, 1) for a 4-response model output.
            # Notice that the 3rd dimension contains 2 dimensions, due to the parameter return_sequences = True.
            # We want only the first value correspondent to this dimension.
            # Also, notice that a single response model would have dimensions as (48, 2, 1), and the extra dimension
            # correspondent to return_sequences = True would be the 2nd dim.
            # Pick only the first value from third dimension:
            y_pred_array = y_pred_array[:,:,0]
        

        # Now, loop through each response:
        for index, response in enumerate(list_of_responses):
            
            if (dim == 1):
                y_pred = y_pred_array[:, index]
            
            elif (dim == 0):
                y_pred = y_pred_array[index]
            
            # add it to the dictionary as the key response:
            response_dict[('y_pred_' + response)] = y_pred

    else: # general case
        
        if (function_used_for_fitting_dl_model == 'get_deep_learning_tf_model'):
            
            if (architecture == 'encoder_decoder'):
                # Since return_sequences = True, the model returns arrays containing two elements. We must pick only
                # the first position (index 0) of 2nd dimension
                y_pred = y_pred[:,0]
                total_dimensions = len(y_pred.shape)
                last_dim = y_pred.shape[(total_dimensions - 1)]
            
            if (last_dim == 1): # remove last dimension
                if (total_dimensions == 4):
                    y_pred = y_pred[:,:,:,0]
                elif (total_dimensions == 3):
                    y_pred = y_pred[:,:,0]
                elif (total_dimensions == 2):
                    y_pred = y_pred[:,0]
        
        if list_of_responses is not None:
            # The column may have been added as the list of responses
            if type(list_of_responses) == str:
                column_with_predictions_suffix = list_of_responses
            
            if len(list_of_responses) == 1:
                column_with_predictions_suffix = str(list_of_responses[0])

        # check if there is a suffix:
        if not (column_with_predictions_suffix is None):
            # There is a suffix declared
            # Since there is a suffix, concatenate it to 'y_pred':
            response_dict[( "y_pred_" + column_with_predictions_suffix)] = y_pred
            
        else:
            # Create the column name as the standard.
            # The name of the new column is simply 'y_pred'
            response_dict["y_pred"] = y_pred
    
    # Check if there is a dataframe to concatenate the predictions
    if not (dataframe_for_concatenating_predictions is None):
            
        # there is a dataframe for concatenating the predictions    
        # concatenate the predicted values with dataframe_for_concatenating_predictions.
        # Add the predicted values as a column:
            
        # Set a local copy of the dataframe to manipulate:
        X_copy = dataframe_for_concatenating_predictions.copy(deep = True)
            
        # Add the predictions as the new column named col_name:
        # If y is a tensor, convert to NumPy array before adding. The numpy.array function
        # has no effect in numpy arrays, but is equivalent to the .numpy method for tensors
        
        for col_name, y_pred in response_dict.items():
            X_copy[col_name] = y_pred
            
        print(f"The prediction was added as the new columns {list(response_dict.keys())} of the dataframe, and this dataframe was returned. Check its 10 first rows:\n")
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(X_copy.head(10))
                    
        except: # regular mode
            print(X_copy.head(10))
            
        return X_copy
        
    else:
        
        # Convert the response_dict into a pandas DataFrame:
        predictions_df = pd.DataFrame(data = response_dict)
        print("Returning only the predicted values. Check the 10 first values of predictions dataframe:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(predictions_df.head(10))
                    
        except: # regular mode
            print(predictions_df.head(10))
            
        return predictions_df


def calculate_class_probability (model_object, X, list_of_classes, type_of_model = 'other', dataframe_for_concatenating_predictions = None, architecture = None):
    """
    calculate_class_probability (model_object, X, list_of_classes, type_of_model = 'other', dataframe_for_concatenating_predictions = None, architecture = None):

    : param: predict_for = 'subset' or predict_for = 'single_entry'
      The function will automatically detect if it is dealing with lists, NumPy arrays
      or Pandas dataframes. If X is a list or a single-dimension array, predict_for
      will be set as 'single_entry'. If X is a multi-dimension NumPy array (as the
      outputs for preparing data - even single_entry - for deep learning models), or if
      it is a Pandas dataframe, the function will set predict_for = 'subset'
    
    : param: X = subset of predictive variables (dataframe, NumPy array, or list).
      If PREDICT_FOR = 'single_entry', X should be a list of parameters values.
      e.g. X = [1.2, 3, 4] (dot is the decimal case separator, comma separate values). 
      Notice that the list should contain only the numeric values, in the same order of the
      correspondent columns.
      If PREDICT_FOR = 'subset' (prediction for multiple entries), X should be a dataframe 
      (subset) or a multi-dimensional NumPy array of the parameters values, as usual.
    
    : param: model_object: object containing the model that will be analyzed. e.g.
      model_object = elastic_net_linear_reg_model
    
    : param: list_of_classes is the list of classes effectively used for training
      the model. Set this parameter as the object returned from function
      retrieve_classes_used_to_train
    
    : param: type_of_model = 'other' or type_of_model = 'deep_learning'
    
      Notice that the output will be an array of probabilities, where each
      element corresponds to a possible class, in the order classes appear.
    
    : param: dataframe_for_concatenating_predictions: if you want to concatenate the predictions
      to a dataframe, pass it here:
      e.g. dataframe_for_concatenating_predictions = df
      If the dataframe must be the same one passed as X, repeat the dataframe object here:
      X = dataset, dataframe_for_concatenating_predictions = dataset.
      Alternatively, if dataframe_for_concatenating_predictions = None, 
      the prediction will be returned as a series or NumPy array, depending on the input format.
      Notice that the concatenated predictions will be added as a new column.
    
    : param: architecture: some models require inputs in a proper format. Declare here if you are using
      one of these architectures. Example: architecture = 'cnn_lstm' from class TfModels require
      a special reshape before getting predictions. You can keep None or put the name of the
      architecture, if no special reshape is needed.
    
      All of the new columns (appended or not) will have the prefix "prob_class_" followed
      by the correspondent class name to identify them.
    """
    import tensorflow as tf
    
    predict_for = 'subset'
    # map if we are dealing with a subset or single entry
    
    
    # 1. Check if a list was input. Lists do not have the attribute shape, present in dataframes
    # and NumPy arrays. Accessing the attribute shape from a list will raise the Exception error
    # named AttributeError
    # Try to access the attribute shape. If the error AttributeError is raised, it is a list, so
    # set predict_for = 'single_entry':

    if ((type(X) == list) | (type(X) == tuple)):
        # Single entry as list or tuple
        # Convert it to NumPy array:
        X = np.array(X)
    
    # Run even if it come from list or tuple:
    if ((type(X) == np.ndarray) & (len(X.shape) == 1)):
        # If X.shape has len == 1, it is a tuple like (4,)
        # Convert the numpy array to the correct shape. It runs even if the list or tuple was
        # converted.
        X = X.reshape(1, -1)
        # generates an array like array([[1, 2, 3, 4]])
        # The reshape (-1, 1) generates an array like ([1], [2], ...) with format for the y-vector
        # used for training.
        
        # Update the predict_for variable:
        predict_for = 'single_entry'      
    
    # Finally, convert to Tensor:
    X = tf.constant(X)
    
    if (architecture == 'cnn_lstm'):
        # Get the hybrid cnn-lstm time series model from class TfModels:
        X = (lambda x: tf.constant(((x.numpy()).reshape(x.numpy().shape[0], 2, 2, 1))))(X)
    
        
    # Check if it is a keras or other deep learning framework; or if it is a sklearn or xgb model:
    boolean_check = (type_of_model == 'deep_learning')
    
    if (boolean_check): # run if it is True
        print("The predictions (outputs) from deep learning models are themselves the probabilities associated to each possible class.")
        print("\n") #line break
        print("The output will be an array of float values: each float represents the probability of one class, in the order the classes appear. For a binary classifier, the first element will correspond to class 0; and the second element will be the probability of class 1.")
    
    
    if (predict_for == 'single_entry'):
        
        print("Calculating probabilities for a single entry X.\n")
    
        if (boolean_check): 
            # Use the predict method itself for deep learning models.
            # These models do not have the predict_proba method.
            # Their output is itself the probability for each class.
            y_pred_probabilities = model_object.predict(X)
        
        else:
            # use the predict_proba method from sklearn and xgboost:
            y_pred_probabilities = model_object.predict_proba(X.numpy())
        
        print("Probabilities calculated using the entry parameters.") 
        print(f"Probabilities calculated for each one of the classes {list_of_classes} (in the order of classes) = {y_pred_probabilities}\n")
        
        # create a dictionary with the possible classes and the correspondent probabilities:
        # Use the list attribute to guarantee that the probabilities are
        # retrieved as a list:
        probability_dict = {'class': list_of_classes,
                            'probability': list(y_pred_probabilities)}
            
        # Convert it to a Pandas dataframe:
        probabilities_df = pd.DataFrame(data = probability_dict)
            
        print("Returning a dataframe containing the classes and the probabilities calculated for the entry to belong to each class. Check it below:")
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(probabilities_df)
                
        except: # regular mode
            print(probabilities_df)
            
        return probabilities_df
    
    
    else:
        
        # prediction for a subset
        
        if (boolean_check): 
            # Use the predict method itself for deep learning models.
            # These models do not have the predict_proba method.
            # Their output is itself the probability for each class.
            y_pred_probabilities = model_object.predict(X)
            
            # If y_pred_probabilities came from a RNN with the parameter return_sequences = True 
            # and/or return_states = True, then the hidden and/or cell states from the LSTMs
            # were returned. So, the returned array has at least one extra dimensions (two
            # if both parameters are True). On the other hand, we want only the first dimension,
            # correspondent to the actual output.

            # Remember that, due to the reshapes for preparing data for deep learning models,
            # y_pred_probabilities must have at least 2 dimensions: (N, 1), where N is the number 
            # of rows of the original dataset. But y_pred_probabilities returned from a model 
            # with return_sequences = True or return_states = True will be of dimension (N, N, 1). 
            # If both parameters are True, the dimension is (N, N, N, 1), since there are extra 
            # arrays for both the hidden and cell states.

            # The conclusion is that there is a third dimension only for models where 
            # return_sequences = True or return_states = True

            # Check if y_pred_probabilities is a numpy array, instead of a Pandas dataframe:

            if (len(y_pred_probabilities.shape) > 2):
                
                # The shape is a tuple containing 3 or more dimensions
                # If we could access the third_dimension, than return_states and
                # or return_sequences = True

                # We want only the values stored as the 1st dimension
                # y_pred_probabilities is an array where each element is an array with 
                # two elements. To get only the first elements:
                # (slice the arrays: get all values only for dimension 0, the 1st dim):
                y_pred_probabilities = y_pred_probabilities[:,0]
                # if we used y_pred_probabilities[:,1] we would get the second element, 
                # which is the hidden state h (input of the next LSTM unit).
                # It happens because of the parameter return_sequences = True. 
                # If return_states = True, there would be a third element, corresponding 
                # to the cell state c.
                # Notice that we want only the 1st dimension (0), no matter the case.
        
        else:
            # use the predict_proba method from sklearn and xgboost:
            y_pred_probabilities = model_object.predict_proba(X.numpy())
        
        # y_pred_probabilities is a column containing arrays of probabilities
        # Let's create a dataframe separating each element of the array into
        # a separate column
        
        # Get the size of each array. It is the total of elements from
        # list_of_classes (total of possible classes):
        total_of_classes = len(list_of_classes)
        
        # Starts a dictionary. This dictionary will have the class as the
        # key and a list of the probabilities that the element belong to that
        # class as the value (in the dataframe, the class will be column,
        # with its calculated probability in each row):
        probability_dict = {}
        
        # Loop through each possible class:
        for class_name in list_of_classes:
            
            # Let's concatenate the prefix "prob_class_" to this strings.
            # This string will be used as column name, so it will be clear 
            # in the output dataframe that the column is referrent to the 
            # probability calculated for the class. Since the elements may 
            # have been saved as numbers use the str attribute to guarantee 
            # that the element was read as a string, and concatenate the
            # prefix to its left:
            class_name = "prob_class_" + str(class_name)
            # Get the index in the list:
            class_index = list_of_class.index(class_name)
            
            # Start a list of probabilities:
            prob_list = []
            
            # Now loop through each row j from the dataframe
            # to retrieve the array in the column y_pred_probabilities:
            
            for i in range(len(y_pred_probabilities)):
                # goes from j = 0 (first row of the dataframe) to
                # j = y_pred_probabilities - 1, index of the last row
                # Get the array of probabilities for that row:
                # If y is a tensor, convert to NumPy array before adding. The numpy.array function
                # has no effect in numpy arrays, but is equivalent to the .numpy method for tensors
                prob_array = np.array(y_pred_probabilities[i])
                
                # Append the (class_index)-th element of that array in prob_list
                # The (class_index)-th position of the array is the probability
                # of the class being analyzed in the i-th iteration of
                # the main loop
                prob_list.append(prob_array[(class_index)])
            
            # Now that the probabilities for the class correspondent to
            # each row were retrieved as the list prob_list, update the
            # dictionary. Use the class name saved as class_name as the
            # key, and put the prob_list as the correspondent value:
            probability_dict[class_name] = prob_list
        
        # Now that we finished the loop, the probability dictionary contains
        # each one of the classes as its keys, and the list of probabilities
        # for each row as the correspondent values. 
        # Also, the keys are identified with the prefix 'prob_class' to
        # indicate that they are referrent to the probability of belonging to
        # one class. Let's convert this dictionary to a Pandas dataframe:
        
        probabilities_df = pd.DataFrame(data = probability_dict)
        
        # Check if there is a dataframe to concatenate the predictions
        if not (dataframe_for_concatenating_predictions is None):
            
            # there is a dataframe for concatenating the predictions.
            
            # Set a local copy of the dataframe to manipulate:
            X_copy = X.copy(deep = True)
            
            # Append the columns from probabilities_df with Pandas concat
            # method, setting axis = 1 (axis = 0  appends rows)
            # Use the pandas 'inner' join, which removes entries without
            # correspondence. It is the same strategy used for concatenating
            # the dataframe obtained from One-Hot Encoding transformation in the
            # ETL Workflow (3_Dataset_Transformation)
            X_copy = pd.concat([X_copy, probabilities_df], axis = 1, join = "inner")
    
            print(f"The dataframe X was concatenated to the probabilities calculated for each class and returned. Check its first 10 entries:\n")
            try:
                # only works in Jupyter Notebook:
                from IPython.display import display
                display(X_copy.head(10))
                    
            except: # regular mode
                print(X_copy.head(10))
            
            return X_copy
        
        else:
            
            print("Returning only the dataframe with the probabilities calculated for each class. Check its first 10 entries:\n")
            try:
                # only works in Jupyter Notebook:
                from IPython.display import display
                display(probabilities_df.head(10))
                    
            except: # regular mode
                print(probabilities_df.head(10))
            
            return probabilities_df


def shap_feature_analysis (model_object, X_train, model_type = 'linear', total_of_shap_points = 40):
    """
    shap_feature_analysis (model_object, X_train, model_type = 'linear', total_of_shap_points = 40):
   
    An introduction to explainable AI with Shapley values:
      https://shap.readthedocs.io/en/latest/example_notebooks/overviews/An%20introduction%20to%20explainable%20AI%20with%20Shapley%20values.html
    
    : param: model_object: object containing the model that will be analyzed. e.g.
      model_object = elastic_net_linear_reg_model
    : param: X_train = subset of predictive variables (dataframe).
    
    : param: total_of_shap_points (integer): number of points from the 
      subset X_train that will be randomly selected for the SHAP 
      analysis. If the kernel is taking too long, reduce this value.
    
    : param: MODEL_TYPE = 'general' for the general case, including artificial neural networks.
      MODEL_TYPE = 'linear' for Sklearn linear models (OLS, Ridge, Lasso, ElasticNet,
      Logistic Regression).
      MODEL_TYPE = 'tree' for tree-based models (Random Forest and XGBoost).
      MODEL_TYPE = 'deep' for Deep Learning TensorFlow model.
      Actually, any string different from 'linear', 'tree', or 'deep' (including blank string)
      will apply the general case.
    
      If clustering is used, it is possible to plot the dendogram with
      the bar chart: shap.plots.bar(shap_values, clustering=clustering, clustering_cutoff=1.8)
      Also, SHAP can be used for text analysis (in the next example, it
      is used to analyze the first sentence - index 0):
      shap.plots.text(shap_values[0])
    
    : param: MAX_NUMBER_OF_FEATURES_SHOWN = 10: (integer) limiting the number
      of features shown in the plot.
    """

    import shap

    # Convert tensor to NumPy array:
    X_train = np.array(X_train)

    # Start SHAP:
    shap.initjs()
    
    print(f"Randomly sampling {total_of_shap_points} points from the dataset to perform SHAP analysis.")
    print("If the kernel takes too long, cancel the application and reduce the integer value input as \'total_of_shap_points\'. On the other hand, if it is possible, increase the value to obtain higher precision on the analysis.")
    
    # sample the number of points passed as total_of_shap_points
    # from the dataset X_train, and store these points as X_shap:
    X_shap = shap.sample(X_train, total_of_shap_points)
    
    if (model_type == 'linear'):
        
        print("Analyzing Scikit-learn linear model.")
        
        # Create an object from the Linear explainer class:
        shap_explainer = shap.LinearExplainer(model_object, np.array(X_shap))
        # Documentation:
        # https://shap-lrjball.readthedocs.io/en/latest/generated/shap.LinearExplainer.html
        # https://shap.readthedocs.io/en/latest/example_notebooks/tabular_examples/linear_models/Math%20behind%20LinearExplainer%20with%20correlation%20feature%20perturbation.html
        # https://shap.readthedocs.io/en/latest/example_notebooks/tabular_examples/linear_models/Sentiment%20Analysis%20with%20Logistic%20Regression.html
        
        # Apply .shap_values method to obtain the shap values:
        shap_vals = shap_explainer.shap_values(X_shap)
        # shap_vals is a list or array of calculated values.
        
    elif (model_type == 'tree'):
        
        print("Analyzing tree-based Scikit-learn or XGBoost model.")
    
        # Create an object from the Tree explainer class:
        shap_explainer = shap.TreeExplainer(model_object, np.array(X_shap))
        # 
        # Documentation:
        # https://shap.readthedocs.io/en/latest/generated/shap.explainers.Tree.html#shap.explainers.Tree
        # Apply .shap_values method to obtain the shap values:
        shap_vals = shap_explainer.shap_values(X_shap)
        # shap_vals is a list or array of calculated values.
 
    elif (model_type == 'deep'):
        
        print("Analyzing Deep Learning TensorFlow model with Deep Explainer.")
    
        # https://shap-lrjball.readthedocs.io/en/latest/generated/shap.DeepExplainer.html#shap.DeepExplainer
        shap_explainer = shap.DeepExplainer(model_object, np.array(X_shap))
        shap_vals = shap_explainer.shap_values(X_shap)

        
        """
        For some deep computer vision models you may use the Gradient Explainer structure as in:
        https://shap-lrjball.readthedocs.io/en/latest/example_notebooks/gradient_explainer/Explain%20an%20Intermediate%20Layer%20of%20VGG16%20on%20ImageNet.html
        elif (model_type == 'gradient_tf'):
            
            print("Analyzing TensorFlow model with Gradient Explainer (using expected gradients, an extension of integrated gradients).")

            # https://shap-lrjball.readthedocs.io/en/latest/generated/shap.GradientExplainer.html
            shap_explainer = shap.GradientExplainer(model_object, pd.DataFrame(np.array(X_shap)))

            - After obtaining the explainer with this code, follow the examples. This class requires a pd.DataFrame as second
            argument, since it access some attributes from this particular class.
        """

    else:
        # In any other case, use the KernelExplainer
        # Create an object from KernelExplainer class:
        shap_explainer = shap.KernelExplainer(model_object.predict, np.array(X_shap))
        # https://shap.readthedocs.io/en/latest/example_notebooks/tabular_examples/neural_networks/Census%20income%20classification%20with%20Keras.html
        # Alternatively: model_object.predict(X)
        # Apply .shap_values method to obtain the shap values:
        shap_vals = shap_explainer.shap_values(X_shap)
        # shap_vals is a list or array of calculated values.
     
    shap.summary_plot(shap_vals, X_shap)
    
    # Create a dictionary with the explainer and the shap_vals:
    shap_dict = {
        'SHAP_kernel_explainer': shap_explainer,
        'SHAP_values': shap_vals
    }
    
    print("\n") # line break
    print("Dictionary with SHAP explainer and SHAP values returned as \'shap_dict\'.")
    
    print("\n") # line break
    print("SHAP Interpretation:")
    print("SHAP returns us a SHAP value that represents the relative importance.")
    print("The features are displayed in order of importance, from the most important (top of the plot) to the less important (bottom of the plot).")
    print("A feature which is shown on the right side of the plot results in positive impact on the model, whereas a feature on the left results into a negative impact in the response.")
    print("The relative impact is shown by the color scale: a tone closer to red indicates a higher impact, whereas the proximity to blue indicates low relative impact.")
        
    return shap_dict
