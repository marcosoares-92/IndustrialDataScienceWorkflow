def separate_and_prepare_features_and_responses (df, features_columns, response_columns):
    """
    separate_and_prepare_features_and_responses (df, features_columns, response_columns):

    https://www.tensorflow.org/api_docs/python/tf/Tensor

    : param: features_columns: list of strings or string containing the names of columns
      with predictive variables in the original dataframe. 
      Example: features_columns = ['col1', 'col2']; features_columns = 'predictor';
      features_columns = ['predictor'].
    : param: response_columns: list of strings or string containing the names of columns
      with response variables in the original dataframe. 
      Example: response_columns = ['col3', 'col4']; response_columns = 'response';
      response_columns = ['response']
    """

    try:
        import tensorflow as tf
    except:
        pass

    # Set a local copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)

    # Check if features_columns and response_columns are lists:
    if ((type(features_columns) != list) & (type(features_columns) != tuple)):
        #put inside a list:
        features_columns = [features_columns]
    
    elif (type(features_columns) == tuple):
        features_columns = list(features_columns)

    if ((type(response_columns) != list) & (type(response_columns) != tuple)):
        #put inside a list:
        response_columns = [response_columns]
    
    elif (type(response_columns) == tuple):
        response_columns = list(response_columns)

    # Now, subset the dataframe:
    X = DATASET[features_columns].copy(deep = True)
    y = DATASET[response_columns].copy(deep = True)
    # since response_columns is a list, not a string, y is a DataFrame, not a Series.
    # So, the copy method accepts the argument deep = True

    # Try the conversion to tensors. Since the values should not be modified, we
    # will create the tensors as tf.constant, instead of tf.Variable:
    try:

        X = tf.constant(X)
        y = tf.constant(y)

        """
            Tensor with format as:
            <tf.Tensor: shape=(253, 12), dtype=float64, numpy=
            array([[ 1.        ,  1.        ,  1.        , ...,  4.18450387,
                10.49874623,  2.09639084],
            ...,
            [12.        ,  4.        ,  6.        , ...,  4.40752786,
                10.71241577,  3.30032431]])>
        """

    except:

        # Simply convert them to NumPy arrays. The arrays can be processed through
        # deep learning and do not add features names to the model information (what
        # raises error if we try to use the model to a set without names):
        X = np.array(X)
        y = np.array(y)

        """
            Array with format as:
            array([[ 1.        ,  1.        ,  1.        , ...,  4.42690937,
                4.18450387, 10.49874623],
            ...,
            [12.        ,  4.        ,  6.        , ...,  4.43083069,
                4.40752786, 10.71241577]])
        """

    print("Check the 5 first elements from the tensors or arrays obtained:\n")
    print("Features tensor or array:\n")
    print(X[:5])
    print("\n")
    print(f"Shape of the complete X tensor or array = {X.shape}\n")
    # shape attribute is common to tf.Tensor, pd.DataFrame, pd.Series, and np.array
    print("Responses tensor or array:\n")
    print(y[:5])
    print("\n")
    print(f"Shape of the complete y tensor or array = {y.shape}\n")

    # Notice that tensors and arrays are sliced in the same way as lists.
    # The slicing also modify the shape attribute from Tensors.
    # We can convert a tf.Tensor object named tensor to a np.array object by
    # simply making array = np.array(tensor) 

    # Now, since the arrays do not have a column header, let's create a mapping dictionary, correlating
    # the array position with the original column name:
    features_dict = {}
    responses_dict = {}

    for column_number, column in enumerate(features_columns):
        # The enumerate object created from a list can be decoupled into two values:
        # The index (number) - position in the list, and the element itself. example:
        # 0, 'first_column':
        # Add it to the features dictionary, with the column number as key:
        features_dict[column_number] = column

    # Repeat the process for the responses:
    for column_number, column in enumerate(response_columns):
        responses_dict[column_number] = column

    # Finally, add both dictionaries to a mapping dict:
    column_map_dict = {'features': features_dict, 'responses': responses_dict}
    print("The mapping of the arrays' positions with the columns original names was returned as 'column_map_dict'.")

    return X, y, column_map_dict


def convert_to_tensor (df_or_array_to_convert, columns_to_convert = None, columns_to_exclude = None):
    """
    convert_to_tensor (df_or_array_to_convert, columns_to_convert = None, columns_to_exclude = None)

    # https://www.tensorflow.org/api_docs/python/tf/Tensor

    : param: columns_to_convert: list of strings or string containing the names of columns
      that you want to convert. Use this if you want to convert only a subset of the dataframe. 
      Example: columns_to_convert = ['col1', 'col2']; columns_to_convert = 'predictor';
      columns_to_convert = ['predictor'] will create a tensor with only the specified columns;
      If None, the whole dataframe will be converted.
      ATTENTION: This argument only works for Pandas dataframes.
    
    : param: columns_to_exclude: Alternative parameter. 
      list of strings or string containing the names of columns that you want to exclude from the
      returned tensor. Use this if you want to convert only a subset of the dataframe. 
      Example: columns_to_exclude = ['col1', 'col2']; columns_to_exclude = 'predictor';
      columns_to_exclude = ['predictor'] will create a tensor with all columns from the dataframe
      except the specified ones. This argument will only be used if the previous one was not.
      ATTENTION: This argument only works for Pandas dataframes.
    """

    try:
        import tensorflow as tf
    except:
        pass
    
    try:
        # Set a local copy of the dataframe to manipulate:
        DATASET = df_or_array_to_convert.copy(deep = True)

        if (columns_to_convert is not None):
            # Subset the dataframe:
            # Check if features_columns and response_columns are lists:
            if ((type(columns_to_convert) != list) & (type(columns_to_convert) != tuple)):
                #put inside a list:
                columns_to_convert = [columns_to_convert]
            
            elif (type(columns_to_convert) == tuple):
                columns_to_convert = list(columns_to_convert)

            # Now, filter the dataframe:
            DATASET = DATASET[columns_to_convert]

        elif (columns_to_exclude is not None):
            # Run only if the dataframe was not subset:
            if ((type(columns_to_exclude) != list) & (type(columns_to_exclude) != tuple)):
                #put inside a list:
                columns_to_exclude = [columns_to_exclude]
            
            elif (type(columns_to_exclude) == tuple):
                columns_to_exclude = list(columns_to_exclude)
            
            # Drop the columns:
            DATASET = DATASET.drop(columns_to_exclude, axis = 1)
    
    except:
        # It is an array or iterable:
        DATASET = np.array(df_or_array_to_convert)
        
        if (len(DATASET.shape) == 1):
            # It is a tuple like (1,) - array like [1, 2, 3,...]
            DATASET =  DATASET.reshape(-1, 1)
            # Now, its format is like [[1], [2], [3],...] - shape like (4, 1)

    # Try the conversion to tensor. Since the values should not be modified, we
    # will create the tensors as tf.constant, instead of tf.Variable:
    try:

        X = tf.constant(DATASET)

        """
            Tensor with format as:
            <tf.Tensor: shape=(253, 12), dtype=float64, numpy=
            array([[ 1.        ,  1.        ,  1.        , ...,  4.18450387,
                10.49874623,  2.09639084],
            ...,
            [12.        ,  4.        ,  6.        , ...,  4.40752786,
                10.71241577,  3.30032431]])>
        """

    except:

        # Simply convert them to NumPy arrays. The arrays can be processed through
        # deep learning and do not add features names to the model information (what
        # raises error if we try to use the model to a set without names):
        X = np.array(DATASET)
        
    print("Check the 5 first elements from the tensor or array obtained:\n")
    print(X[:5])
    print("\n")
    print(f"Shape of the complete X tensor or array = {X.shape}\n")
    # shape attribute is common to tf.Tensor, pd.DataFrame, pd.Series, and np.array

    # Notice that tensors and arrays are sliced in the same way as lists.
    # The slicing also modify the shape attribute from Tensors.
    # We can convert a tf.Tensor object named tensor to a np.array object by
    # simply making array = np.array(tensor) 

    # Now, since the arrays do not have a column header, let's create a mapping dictionary, correlating
    # the array position with the original column name:
    column_map_dict = {}
    try:
        
        for column_number, column in enumerate(list(DATASET.columns)):
            # The enumerate object created from a list can be decoupled into two values:
            # The index (number) - position in the list, and the element itself. example:
            # 0, 'first_column':
            # Add it to the features dictionary, with the column number as key:
            column_map_dict[column_number] = column

        print("The mapping of the arrays' positions with the columns original names was returned as 'column_map_dict'.")
    
    except:
        pass
    
    return X, column_map_dict


def split_data_into_train_and_test (X, y, percent_of_data_used_for_model_training = 75, percent_of_training_data_used_for_model_validation = 0):
    """
    split_data_into_train_and_test (X, y, percent_of_data_used_for_model_training = 75, percent_of_training_data_used_for_model_validation = 0):
    
    : param: X = tensor or array of predictive variables.
    : param: y = tensor or array of response variables.
    
    : param: percent_of_data_used_for_model_training: float from 0 to 100,
      representing the percent of data used for training the model
    
      If you want to use cross-validation, separate a percent of the training data for validation.
      Declare this percent as percent_of_training_data_used_for_model_validation (float from 0 to 100).
    """

    import random
    import tensorflow as tf
    
    # Convert to tuples to save memory:
    X = tuple(np.array(X))
    y = tuple(np.array(y))
    
    # Convert the percent to fraction.
    train_fraction = (percent_of_data_used_for_model_training / 100)
    
    if (train_fraction > 1):
        train_fraction = 1
    
    elif (train_fraction < 0):
        train_fraction = 0
    
    # Convert the percent of validation to fraction:
    validation_fraction = (percent_of_training_data_used_for_model_validation / 100)
    if (validation_fraction > 1):
        validation_fraction = 1
    
    elif (validation_fraction < 0):
        validation_fraction = 0
    
    # Calculate the test fraction:
    test_fraction = (1 - train_fraction - validation_fraction)
    
    try:
        assert test_fraction >= 0
        assert train_fraction + test_fraction + validation_fraction == 1
    
    except:
        if ((train_fraction + validation_fraction) > 1):
            if (train_fraction == 1):
                validation_fraction = 0
                test_fraction = 0
            
            else:
                test_fraction = (1 - train_fraction)
                validation_fraction = 0
    
    if (train_fraction == 1):
        X_train, y_train = np.array(X), np.array(y)
        X_test, y_test = np.array([]), np.array([])
        X_valid, y_valid = np.array([]), np.array([])
    
    elif (validation_fraction == 0):
        X_valid, y_valid = np.array([]), np.array([])
    
    if (train_fraction < 1):
        # Create a list of indices:
        indices = [i for i in range(0, len(X))]
        # Shuffle the indices:
        random.shuffle(indices)

        total_indices = len(indices)
        total_for_training = int(np.rint(train_fraction*total_indices))

        # Set the indexes used for training:
        train_idx, other_idx = indices[:total_for_training], indices[total_for_training:]
        if (validation_fraction == 0):
            test_idx = other_idx
            valid_idx = []

        else:
            total_for_testing = int(np.rint(test_fraction*total_indices))
            test_idx, valid_idx = other_idx[:total_for_testing], indices[total_for_testing:]
    
        
        # Now, create the lists of splitted elements
        # [element for ... if ...]
        X_train = [X[i] for i in train_idx]
        y_train = [y[i] for i in train_idx]
        X_train, y_train = np.array(X_train), np.array(y_train)
        X_train, y_train = tf.constant(X_train), tf.constant(y_train)
        
        X_test = [X[i] for i in test_idx]
        y_test = [y[i] for i in test_idx]
        X_test, y_test = np.array(X_test), np.array(y_test)
        X_test, y_test = tf.constant(X_test), tf.constant(y_test)
        
        if (len(valid_idx) > 0):
            X_valid = [X[i] for i in valid_idx]
            y_valid = [y[i] for i in valid_idx]
            X_valid, y_valid = np.array(X_valid), np.array(y_valid)
            X_valid, y_valid = tf.constant(X_valid), tf.constant(y_valid)
            
    
    print(f"X and y successfully splitted into train: X_train, y_train ({train_fraction*100:.1f}% of data); test: X_test, y_test ({test_fraction*100:.1f}% of data); and validation subsets: X_valid, y_valid ({validation_fraction*100:.1f}% of data).")
    
    split_dictionary = {'X_train': X_train, 'y_train': y_train, 'X_test': X_test, 'y_test': y_test, 'X_valid': X_valid, 'y_valid': y_valid}
    
    for subset in split_dictionary.keys():
        
        print("\n")
        print(f"10 first rows from subset {subset}:\n")
        print(split_dictionary[subset][:10])
    
    return split_dictionary


def time_series_train_test_split (X, y, percent_of_data_used_for_model_training = 75, percent_of_training_data_used_for_model_validation = 0):
    """
    time_series_train_test_split (X, y, percent_of_data_used_for_model_training = 75, percent_of_training_data_used_for_model_validation = 0):
    
    : param: X = tensor or array of predictive variables.
    : param: y = tensor or array of response variables.
    
    : param: percent_of_data_used_for_model_training: float from 0 to 100,
      representing the percent of data used for training the model
    
      If you want to use cross-validation, separate a percent of the training data for validation.
      Declare this percent as percent_of_training_data_used_for_model_validation (float from 0 to 100).
    """
    
    total_rows = X.shape[0]
    split_row = int(np.rint((percent_of_data_used_for_model_training/100)*total_rows))

    # Now, split the tensors
    X_train, X_test = X[:split_row], X[split_row:]
    y_train, y_test = y[:split_row], y[split_row:]

    split_dictionary = {'X_train': X_train, 'y_train': y_train, 'X_test': X_test, 'y_test': y_test}
    print(f"X and y successfully splitted into train: X_train, y_train ({percent_of_data_used_for_model_training}% of data); and test subsets: X_test, y_test ({100 - percent_of_data_used_for_model_training}% of data).")
    
    if (percent_of_training_data_used_for_model_validation > 0):
        training_rows = X_train.shape[0]
        # The first fraction is still used for training. So the percent saved for training is:
        # 100 - percent_of_data_for_validation
        split_valid_row = int(np.rint(((100 - percent_of_training_data_used_for_model_validation)/100)*training_rows))
        # Now, split the tensors
        X_train, X_valid = X_train[:split_valid_row], X_train[split_valid_row:]
        y_train, y_valid = y_train[:split_valid_row], y_train[split_valid_row:]
        # Update the dictionary:
        split_dictionary['X_train'] = X_train
        split_dictionary['y_train'] = y_train
        split_dictionary['X_valid'] = X_valid
        split_dictionary['y_valid'] = y_valid
    
    for subset in split_dictionary.keys():
        
        print("\n")
        print(f"10 first rows from subset {subset}:\n")
        print(split_dictionary[subset][:10])
    
    return split_dictionary


def windowed_dataset_from_time_series (y, window_size = 20, batch_size = 32, shuffle_buffer_size = 100):
    """
    windowed_dataset_from_time_series (y, window_size = 20, batch_size = 32, shuffle_buffer_size = 100):
    
    : param: y: tensor containing the time series to be converted.
    
      Processing the data: you can feed the data for training by creating a dataset 
      with the appropiate processing steps such as windowing, flattening, 
      batching and shuffling.
    : param: window_size (integer): number of rows/ size of the time window used.
    : param: batch_size (integer): number of rows/ size of the batches used for training.
    : param: shuffle_buffer_size (integer): number of rows/ size used for shuffling the entries.
    """

    import tensorflow as tf
    
    # Create dataset from the series
    dataset = tf.data.Dataset.from_tensor_slices(y)
    
    # Slice the dataset into the appropriate windows
    # Window the data but only take those with the specified size
    dataset = dataset.window(window_size + 1, shift = 1, drop_remainder = True)
    
    # Flatten the dataset
    # Flatten the windows by putting its elements in a single batch
    dataset = dataset.flat_map(lambda window: window.batch(window_size + 1))
    
    # Shuffle it
    dataset = dataset.shuffle(shuffle_buffer_size)
    
    # Split it into the features and labels
    # Create tuples with features and labels 
    dataset = dataset.map(lambda window: (window[:-1], window[-1]))
    
    # Batch it
    dataset = dataset.batch(batch_size).prefetch(1)

    print("TensorFlow dataset successfully obtained:")
    print(dataset)

    return dataset


def multi_columns_time_series_tensors (df, response_columns, sequence_stride = 1, sampling_rate = 1, shift = 1, use_past_responses_for_prediction = True, percent_of_data_used_for_model_training = 70, percent_of_training_data_used_for_model_validation = 10):
    """
    multi_columns_time_series_tensors (df, response_columns, sequence_stride = 1, sampling_rate = 1, shift = 1, 
        use_past_responses_for_prediction = True, percent_of_data_used_for_model_training = 70, 
        percent_of_training_data_used_for_model_validation = 10):

    original algorithm: 
      https://www.tensorflow.org/tutorials/structured_data/time_series?hl=en&%3Bauthuser=1&authuser=1
    
    
    : param: response_columns: string or list of strings with the response columns
    
      The time series may be represented as a sequence of times like: t = 0, t = 1, t = 2, ..., t = N.
      When preparing the dataset, we pick a given number of 'times' (indexes), and use them for
      predicting a time in the future.
      So, the input_width represents how much times will be used for prediction. If input_width = 6,
      we use 6 values for prediction, e.g., t = 0, t = 1, ..., t = 5 will be a prediction window.
      In turns, if input_width = 3, 3 values are used: t = 0, t = 1, t = 2; if input_width = N, N
      consecutive values will be used: t = 0, t = 1, t = 2, ..., t = N. And so on.
      label_width, in turns, represent how much times will be predicted. If label_width = 1, a single
      value will be predicted. If label_width = 2, two consecutive values are predicted; if label_width =
      N, N consecutive values are predicted; and so on.
    
    : params: shift, sampling_rate, and sequence_stride: integers
    
      shift represents the offset, i.e., given the input values, which value in the time sequence will
      be predicted. So, suppose input_width = 6 and label_width = 1
      If shift = 1, the label, i.e., the predicted value, will be the first after the sequence used for
      prediction. So, if  t = 0, t = 1, ..., t = 5 will be a prediction window and t = 6 will be the
      predicted value. Notice that the complete window has a total width = 7: t = 0, ..., t = 7. 
      If label_width = 2, then t = 6 and t = 7 will be predicted (total width = 8).
      Another example: suppose input_width = 24. So the predicted window is: t = 0, t = 1, ..., t = 23.
      If shift = 24, the 24th element after the prediction sequence will be used as label, i.e., will
      be predicted. So, t = 24 is the 1st after the sequence, t = 25 is the second, ... t = 47 is the
      24th after. If label_with = 1, then the sequence t = 0, t = 1, ..., t = 23 will be used for
      predicting t = 47. Naturally, the total width of the window = 47 in this case.
    
      Also, notice that the label is used by the model as the response (predicted) variable.
    
      So for a given shift: the sequence of timesteps i, i+1, ... will be used for predicting the
      timestep i + shift
      If a sequence starts in index i, the next sequence will start from i + sequence_stride.
      The sequence will be formed by timesteps i, i + sampling_rate, i + 2* sampling_rate, ...
      Example: Consider indices [0, 1, ... 99]. With sequence_length=10, sampling_rate=2, 
      sequence_stride=3, the dataset will yield batches of sequences composed of the following 
      indices:
      First sequence:  [0  2  4  6  8 10 12 14 16 18]
      Second sequence: [3  5  7  9 11 13 15 17 19 21]
      Third sequence:  [6  8 10 12 14 16 18 20 22 24]
      ...
      Last sequence:   [78 80 82 84 86 88 90 92 94 96]

    : param: percent_of_data_used_for_model_training: float from 0 to 100,
      representing the percent of data used for training the model
    
      If you want to use cross-validation, separate a percent of the training data for validation.
      Declare this percent as percent_of_training_data_used_for_model_validation (float from 0 to 100).
    
      If PERCENT_OF_DATA_USED_FOR_MODEL_TRAINING = 70, and 
      PERCENT_OF_TRAINING_DATA_USED_FOR_MODEL_VALIDATION = 10, 
      training dataset slice goes from 0 to 0.7 (70%) of the dataset;
      testing slicing goes from 0.7 x dataset to ((1 - 0.1) = 0.9) x dataset
      validation slicing goes from 0.9 x dataset to the end of the dataset.
      Here, consider the time sequence t = 0, t = 1, ... , t = N, for a dataset with length N:
      training: from t = 0 to t = (0.7 x N); testing: from t = ((0.7 x N) + 1) to (0.9 x N);
      validation: from t = ((0.9 x N) + 1) to N (the fractions 0.7 x N and 0.9 x N are rounded to
      the closest integer).
    
    : param: use_past_responses_for_prediction: True if the past responses will be used for predicting their
      value in the future; False if you do not want to use them.
    """
    
    import tensorflow as tf
    
    # Create a local copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    
    # Instantiate an object from WindowGenerator class:
    w = WindowGenerator (dataset = DATASET, shift = shift, use_past_responses_for_prediction = use_past_responses_for_prediction, sequence_stride = sequence_stride, sampling_rate = sampling_rate, label_columns = response_columns, train_pct = percent_of_data_used_for_model_training, val_pct = percent_of_training_data_used_for_model_validation)
    # Make the tensors:
    w = w.make_tensors()
    # Retrieve tensors dictionary:
    tensors_dict = w.tensors_dict

    print("Finished preparing the time series datasets for training, testing, and validation. Check their shapes.\n")
    
    for key in tensors_dict.keys():
        
        print(f"{key}-tensors obtained:")
        nested_dict = tensors_dict[key]
        print(f"Inputs tensor shape = {nested_dict['inputs'].shape}")
        print(f"Labels tensor shape = {nested_dict['labels'].shape}\n")
    
    return tensors_dict


def union_1_dim_tensors (list_of_tensors_or_arrays):
    """
    union_1_dim_tensors (list_of_tensors_or_arrays)
    
    : param: list of tensors: list containing the 1-dimensional tensors or arrays that the function will union.
      the operation will be performed in the order that the tensors are declared.
      One-dimensional tensors have shape (X,), where X is the number of elements. Example: a column
      of the dataframe with elements 1, 2, 3 in this order may result in an array like array([1, 2, 3])
      and a Tensor with shape (3,). With we union it with the tensor from the column with elements
      4, 5, 6, the output will be array([[1,4], [2,5], [3,6]]). Alternatively, this new array could
      be converted into a Pandas dataframe where each column would be correspondent to one individual
      tensor.
    """
    
    import tensorflow as tf
    
    # Convert each element from the list to a numpy array, in case they are tensors:
    list_of_arrays = [np.array(tensor) for tensor in list_of_tensors_or_arrays]
    
    # Now, stack all elements from list_of_arrays into a single array, using the columns' axis
    # (axis = 1).
    # https://numpy.org/doc/stable/reference/generated/numpy.stack.html
    
    """
    Example: suppose a = np.array([1, 2, 3]), b = np.array([4, 5, 6]), c = np.array([7, 8, 9])
    If we do np.stack([a,b,c], axis = 1), the resultant will be array([[1, 4, 7],[2, 5, 8],[3, 6, 9]]),
    what would be converted into a dataframe where each original tensor would correspond to a column.
    
    On the other hand, by doing np.stack([a,b,c], axis = 0), the resultant would be array([[1, 2, 3],
    [4, 5, 6],[7, 8, 9]]) - in a dataframe originated from this array, each original tensor would
    correspond to a row.
    """
    stacked_array = np.stack(list_of_arrays, axis = 1)
    
    # Finally, convert it to tensor and return it:
    tensors_union = tf.constant(stacked_array)
    
    # Notice that this operation is equivalent to firstly converting all to tensors and then performing:
    # tf.stack([a,b,c], axis = 1), where [a, b, c] is a list of tensors a, b, c (substitute it by
    # list_of_tensors).
    
    print("Tensors union complete. Check the resulting tensor below:\n")
    print(tensors_union)
    
    return tensors_union
