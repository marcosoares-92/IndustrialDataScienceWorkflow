import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from idsw import (InvalidInputsError, ControlVars)
from .utils import (EncodeDecode, mode_retrieval)


def merge_on_timestamp (df_left, df_right, left_key, right_key, how_to_join = "inner", merge_method = 'asof', merged_suffixes = ('_left', '_right'), asof_direction = 'nearest', ordered_filling = 'ffill'):
    """
    merge_on_timestamp (df_left, df_right, left_key, right_key, how_to_join = "inner", merge_method = 'asof', merged_suffixes = ('_left', '_right'), asof_direction = 'nearest', ordered_filling = 'ffill'):
    
    WARNING: Only two dataframes can be merged on each call of the function.
    
    : param: df_left: dataframe to be joined as the left one.
    
    : param: df_right: dataframe to be joined as the right one
    
    : param: left_key: (String) name of column of the left dataframe to be used as key for joining.
    
    : param: right_key: (String) name of column of the right dataframe to be used as key for joining.
    
    : param: how_to_join: joining method: "inner", "outer", "left", "right". The default is "inner".
    
    : param: merge_method: which pandas merging method will be applied:
      merge_method = 'ordered' for using the .merge_ordered method.
      merge_method = "asof" for using the .merge_asof method.
      WARNING: .merge_asof uses fuzzy matching, so the how_to_join parameter is not applicable.
    
    : param: merged_suffixes = ('_left', '_right') - tuple of the suffixes to be added to columns
      with equal names. Simply modify the strings inside quotes to modify the standard
      values. If no tuple is provided, the standard denomination will be used.
    
    : param: asof_direction: this parameter will only be used if the .merge_asof method is
      selected. The default is 'nearest' to merge the closest timestamps in both 
      directions. The other options are: 'backward' or 'forward'.
    
    : param: ordered_filling: this parameter will only be used on the merge_ordered method.
      The default is None. Input ordered_filling = 'ffill' to fill missings with the
      previous value.
    """
    
    # Create dataframe local copies to manipulate, avoiding that Pandas operates on
    # the original objects; or that Pandas tries to set values on slices or copies,
    # resulting in unpredictable results.
    # Use the copy method to effectively create a second object with the same properties
    # of the input parameters, but completely independent from it.
    DF_LEFT = df_left.copy(deep = True)
    DF_RIGHT = df_right.copy(deep = True)
    
    # Convert all the column names to strings, for running the function for the case of numeric indexes:
    DF_LEFT.columns = [str(column) for column in DF_LEFT.columns]
    DF_RIGHT.columns = [str(column) for column in DF_RIGHT.columns]
    left_key, right_key = str(left_key), str(right_key)
    
    # Firstly, let's guarantee that the keys were actually read as timestamps of the same type.
    # We will do that by converting all values to np.datetime64. If fails, then
    # try to convert to Pandas timestamps.
    
    # try parsing as np.datetime64:
    try:
        DF_LEFT[left_key] = DF_LEFT[left_key].astype('datetime64[ns]')
        DF_RIGHT[right_key] = DF_RIGHT[right_key].astype('datetime64[ns]')
    
    except:
        # Try conversion to pd.Timestamp (less efficient, involves looping)
        DF_LEFT[left_key] = [pd.Timestamp(timestamp, unit = 'ns') for timestamp in DF_LEFT[left_key]]
        DF_RIGHT[right_key] = [pd.Timestamp(timestamp, unit = 'ns') for timestamp in DF_RIGHT[right_key]]
    
    # Now, even if the dates were read as different types of variables (like string for one
    # and datetime for the other), we converted them to a same type (Pandas timestamp), avoiding
    # compatibility issues.
    
    # For performing merge 'asof', the timestamps must be previously sorted in ascending order.
    # Pandas sort_values method: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html
    # Let's sort the dataframes in ascending order of timestamps before merging:
    
    DF_LEFT = DF_LEFT.sort_values(by = left_key, ascending = True)
    DF_RIGHT = DF_RIGHT.sort_values(by = right_key, ascending = True)
    
    # Reset indices:
    DF_LEFT = DF_LEFT.reset_index(drop = True)
    DF_RIGHT = DF_RIGHT.reset_index(drop = True)
        
    
    if (merge_method == 'ordered'):
    
        if (ordered_filling == 'ffill'):
            
            merged_df = pd.merge_ordered(DF_LEFT, DF_RIGHT, left_on = left_key, right_on = right_key, how = how_to_join, suffixes = merged_suffixes, fill_method='ffill')
        
        else:
            
            merged_df = pd.merge_ordered(DF_LEFT, DF_RIGHT, left_on = left_key, right_on = right_key, how = how_to_join, suffixes = merged_suffixes)
    
    elif (merge_method == 'asof'):
        
        merged_df = pd.merge_asof(DF_LEFT, DF_RIGHT, left_on = left_key, right_on = right_key, suffixes = merged_suffixes, direction = asof_direction)
    
    else:
        
        print("You did not enter a valid merge method for this function, \'ordered\' or \'asof\'.")
        print("Then, applying the conventional Pandas .merge method, followed by .sort_values method.\n")
        
        #Pandas sort_values method: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html
        
        merged_df = DF_LEFT.merge(DF_RIGHT, left_on = left_key, right_on = right_key, how = how_to_join, suffixes = merged_suffixes)
        merged_df = merged_df.sort_values(by = merged_df.columns[0], ascending = True)
        #sort by the first column, with index 0.
    
    # Now, reset index positions of the merged dataframe:
    merged_df = merged_df.reset_index(drop = True)
    
    # Pandas .head(Y) method results in a dataframe containing the first Y rows of the 
    # original dataframe. The default .head() is Y = 5. Print first 10 rows of the 
    # new dataframe:
    
    if ControlVars.show_results:
        print("Dataframe successfully merged. Check its 10 first rows:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(merged_df.head(10))
                
        except: # regular mode
            print(merged_df.head(10))
        
    return merged_df


def group_variables_by_timestamp (df, timestamp_tag_column, subset_of_columns_to_aggregate = None, grouping_frequency_unit = 'day', number_of_periods_to_group = 1, aggregate_function = 'mean', start_time = None, offset_time = None, add_suffix_to_aggregated_col = True, suffix = None):
    """
    group_variables_by_timestamp (df, timestamp_tag_column, subset_of_columns_to_aggregate = None, grouping_frequency_unit = 'day', number_of_periods_to_group = 1, aggregate_function = 'mean', start_time = None, offset_time = None, add_suffix_to_aggregated_col = True, suffix = None):
    
    numpy has no function mode, but scipy's stats module has.
      https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mode.html?msclkid=ccd9aaf2cb1b11ecb57c6f4b3e03a341
    
    
    : param: df - dataframe/table containing the data to be grouped
    
    : param: timestamp_tag_colum: name (header) of the column containing the
      timestamps for grouping the data.
    
    : param: subset_of_columns_to_aggregate: list of strings (inside quotes) containing the names 
      of the columns that will be aggregated. Use this argument if you want to aggregate only a subset,
      not the whole dataframe. Declare as a list even if there is a single column to group by.
      e.g. subset_of_columns_to_aggregate = ["response_feature"] will return the column 
      'response_feature' grouped. subset_of_columns_to_aggregate = ["col1", 'col2'] will return columns
      'col1' and 'col2' grouped.
      If you want to aggregate the whole subset, keep subset_of_columns_to_aggregate = None.
    
    : param: grouping_frequency_unit: the frequency of aggregation. The possible values are:
      'year' (or 'y'), 'month' (or 'm'), 'week' (or 'w'), 'day' (or 'd'), 'hour' (or 'h'), 
      'minute' (or 'min'), 'second' (or 's'), 'microsecond' (or 'us'), 'nanosecond' (or 'ns').
    
     Simply provide the key: 'year', 'month', 'week',..., 'second', and this dictionary
     will convert to the Pandas coding.
     The default is 'day', so this will be inferred frequency if no value is provided.
     Since grouping_frequency_unit is variable storing a string, it should not come under
     quotes.

     https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html
     To group by business day, check the example:
     https://stackoverflow.com/questions/13019719/get-business-days-between-start-and-end-date-using-pandas
    
    : param: number_of_periods_to_group: the bin size. The default is 1, so we will group by '1day'
     if number_of_periods_to_group = 2 we would be grouping by every 2 days.
     If the unit was minute and number_of_periods_to_group = 30, we would be grouping into
     30-min bins.

    : param: aggregate_function: Pandas aggregation method: 'mean', 'median', 'std', 'sum', 'min'
      'max', 'count', etc. The default is 'mean'. Then, if no aggregate is provided, 
      the mean will be calculated.

      scipy.stats Summary statistics:
      https://docs.scipy.org/doc/scipy/reference/stats.html
    """

    from scipy import stats
    
    print("WARNING: The categorical variables will be grouped in terms of mode, i.e., as the most common value observed during the aggregated time period. This is the maximum of the statistical distribution of that variable.\n")
    
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
    
    if ((grouping_frequency_unit == 'year') | (grouping_frequency_unit == 'y')):

        frq_unit = 'YE'

    elif ((grouping_frequency_unit == 'month') | (grouping_frequency_unit == 'm')):

        frq_unit = 'ME'

    elif ((grouping_frequency_unit == 'week') | (grouping_frequency_unit == 'w')):

        frq_unit = 'W'
    
    elif ((grouping_frequency_unit == 'day') | (grouping_frequency_unit == 'd')):
        
        frq_unit = 'D'

    elif ((grouping_frequency_unit == 'hour') | (grouping_frequency_unit == 'h')):
        
        frq_unit = 'h'
    
    elif ((grouping_frequency_unit == 'minute') | (grouping_frequency_unit == 'min')):
        
        frq_unit = 'min'
            
    elif ((grouping_frequency_unit == 'second') | (grouping_frequency_unit == 's')):
        
        frq_unit = 's'
         
    elif ((grouping_frequency_unit == 'millisecond') | (grouping_frequency_unit == 'ms')):
        
        frq_unit = 'ms'
         
    elif ((grouping_frequency_unit== 'microsecond') | (grouping_frequency_unit == 'us')):
        
        frq_unit = 'us'
        
    else:

        frq_unit = 'ns'
        print("No unit or invalid unit provided for timedelta. Then, returned timedelta in nanoseconds (1s = 10^9 ns).\n")


    if (number_of_periods_to_group <= 0):
        
        print("Invalid number of periods to group. Changing to 1 period.\n")
        number_of_periods_to_group = 1
    
    if (number_of_periods_to_group == 1):
        
        #Do not put the number 1 prior to the frequency unit
        FREQ =  frq_unit
    
    else:
        #perform the string concatenation. Convert the number into a string:
        number_of_periods_to_group = str(number_of_periods_to_group)
        #Concatenate the strings:
        FREQ = number_of_periods_to_group + frq_unit
        #Expected output be like '2D' for a 2-days grouping
  
    # Convert the input into the correct aggregation function. Access the value on key
    # aggregate_function in dictionary agg_dict:
    
    if (aggregate_function in ['mean', 'sum', 'median', 'std', 'count', 'min', 'max']):
        aggregate_function = aggregate_function
    
    elif (aggregate_function == 'mode'):
        aggregate_function = stats.mode
    
    elif (aggregate_function == 'geometric_mean'):
        aggregate_function = stats.gmean
    
    elif (aggregate_function == 'harmonic_mean'):
        aggregate_function = stats.hmean
    
    elif (aggregate_function == 'kurtosis'):
        aggregate_function = stats.kurtosis
    
    elif (aggregate_function == 'skew'):
        aggregate_function = stats.skew
    
    elif (aggregate_function == 'geometric_std'):
        aggregate_function = stats.gstd
    
    elif (aggregate_function == 'interquartile_range'):
        aggregate_function = stats.iqr
    
    elif (aggregate_function == 'mean_standard_error'):
        aggregate_function = stats.sem
    
    else:
        raise InvalidInputsError (f"Select a valid aggregate function: {['mean', 'sum', 'median', 'std', 'count', 'min', 'max', 'mode', 'geometric_mean', 'harmonic_mean', 'kurtosis', 'skew', 'geometric_std', 'interquartile_range', 'mean_standard_error']}")
    
    # Now, aggregate_function actually stores the value that must be passed to the agg method.
    
    #You can pass a list of multiple aggregations, like: 
    #aggregate_function = [mean, max, sum]
    #You can also pass custom functions, like: pct30 (30-percentile), or np.mean
    #aggregate_function = pct30
    #aggregate_function = np.mean (numpy.mean)
    
    #ADJUST OF GROUPING BASED ON A FIXED TIMESTAMP
    #This parameters are set to None as default.
    #You can specify the origin (start_time) or the offset (offset_time), which are
    #equivalent. The parameter should be declared as a timestamp.
    #For instance: start_time = '2000-10-01 23:30:00'
    
    #WARNING: DECLARE ONLY ONE OF THESE PARAMETERS. DO NOT DECLARE AN OFFSET IF AN 
    #ORIGIN WAS SPECIFIED, AND VICE-VERSA.
    
    #Create a Pandas timestamp object from the timestamp_tag_column. It guarantees that
    #the timestamp manipulation methods can be correctly applied.
    #Let's create using nanoseconds resolution, so that the timestamps present the
    #maximum possible resolution:
    
    # START: CONVERT ALL TIMESTAMPS/DATETIMES/STRINGS TO pandas.Timestamp OBJECTS.
    # This will prevent any compatibility problems.
    
    #The pd.Timestamp function can handle a single timestamp per call. Then, we must
    # loop trough the series, and apply the function to each element.
    
    # Create dataframe local copy to manipulate, avoiding that Pandas operates on
    # the original object; or that Pandas tries to set values on slices or copies,
    # resulting in unpredictable results.
    # Use the copy method to effectively create a second object with the same properties
    # of the input parameters, but completely independent from it.
    df_copy = df.copy(deep = True)
    
    # try parsing as np.datetime64 (more efficient, without loops):
    try:
        df_copy['timestamp_obj'] = df_copy[timestamp_tag_column].astype('datetime64[ns]')
    
    except:
        # Obtain pd.Timestamp objects
        # 1. Start a list to store the Pandas timestamps:
        df_copy['timestamp_obj'] = [pd.Timestamp(timestamp, unit = 'ns') for timestamp in df_copy[timestamp_tag_column]]
    
    
    # Now we have a list correspondent to timestamp_tag_column, but only with
    # Pandas timestamp objects
    
    # 4. Sort the dataframe in ascending order of timestamps:
    df_copy = df_copy.sort_values(by = 'timestamp_obj', ascending = True)
    
    # Reset indices before aggregation:
    df_copy = df_copy.reset_index(drop = True)
    
    # In this function, we do not convert the Timestamp to a datetime64 object.
    # That is because the Grouper class specifically requires a Pandas Timestamp
    # object to group the dataframes.
    
    # Get the list of columns:
    cols_list = list(df_copy.columns)
    
    if (subset_of_columns_to_aggregate is not None):
        
        # cols_list will be the subset list:
        cols_list = subset_of_columns_to_aggregate
    
    # Start a list of numerical columns, and a list of categorical columns, containing only the
    # column for aggregation as the first element:
    numeric_list = ['timestamp_obj']
    categorical_list = ['timestamp_obj']
    
    # Loop through all valid columns (cols_list)
    for column in cols_list:
        
        # Check if the column is neither in numeric_list nor in
        # categorical_list yet:
        if ((column not in numeric_list) & (column not in categorical_list) & (column != timestamp_tag_column)):
            
                
            # Check if the column is numeric:
            # https://pandas.pydata.org/docs/reference/api/pandas.api.types.is_numeric_dtype.html
            
            if (pd.api.types.is_numeric_dtype(df_copy[column])):
                # Boolean returned True
                # Append to numerical columns list:
                numeric_list.append(column)
            
            else:
                # Append to numerical columns list:
                # Append to categorical columns list:
                categorical_list.append(column)
    
    # Create variables to map if both are present.
    is_categorical = 0
    is_numeric = 0
    
    # Create two subsets:
    if (len(categorical_list) > 1):
        
        # Has at least one column plus the variable_to_group_by:
        df_categorical = df_copy.copy(deep = True)
        df_categorical = df_categorical[categorical_list]
        # It is possible that a timestamp column was passed as string. To avoid conversion errors, convert each categorical column to str:
        for col in df_categorical.columns:
            df_categorical[col] = df_categorical[col].astype(str)

        is_categorical = 1
    
    if (len(numeric_list) > 1):
        
        df_numeric = df_copy.copy(deep = True)
        df_numeric = df_numeric[numeric_list]
        is_numeric = 1
    
    # Notice that the variables is_numeric and is_categorical have value 1 only when the subsets
    # are present.
    is_cat_num = is_categorical + is_numeric
    # is_cat_num = 0 if no valid dataset was input.
    # is_cat_num = 2 if both subsets are present.
        
    
    # Let's try to group the df_numeric dataframe.
    if (is_numeric == 1):
        # Guarantee that 'timestamp_obj' was correctly read as datetime for grouping:
        df_numeric['timestamp_obj'] = df_numeric['timestamp_obj'].astype('datetime64[ns]')
        
        if (start_time is not None):

            df_numeric = df_numeric.groupby(pd.Grouper(key = 'timestamp_obj' , freq = FREQ, origin = start_time), as_index = True, sort = True, observed = True).agg(aggregate_function)

        elif (offset_time is not None):

            df_numeric = df_numeric.groupby(pd.Grouper(key = 'timestamp_obj' , freq = FREQ, offset = offset_time), as_index = True, sort = True, observed = True).agg(aggregate_function)

        else:

            #Standard situation, when both start_time and offset_time are None
            df_numeric = df_numeric.groupby(pd.Grouper(key = 'timestamp_obj' , freq = FREQ), as_index = True, sort = True, observed = True).agg(aggregate_function)
            
        print (f"Numerical variables of the dataframe grouped in terms of {aggregate_function} by every {number_of_periods_to_group} {frq_unit}.\n")
        
        # Since as_index = True, the timestamp becomes the index. Let's create a column 'timestamp_grouped' to store this index:
        df_numeric['timestamp_grouped'] = df_numeric.index
        # Reset the index:
        df_numeric = df_numeric.reset_index(drop = True)
        
        # Notice that the timestamp became the last element. So, get a list grouped_num_cols
        # That is a slice from the list of columns from df_numeric containing all elements except the last one.
        grouped_num_cols = list(df_numeric.columns)[:-1]
        # The slice [i:] gets all elements from index i, whereas [:j] get all elements until index j
        # (but not including j). [:-1] gets all until the last one, [:-2] gets all until the last 2,...
        
        # Now concatenate with a list containing only the timestamp to make it the first element:
        grouped_num_cols = ['timestamp_grouped'] + grouped_num_cols
        # Select the columns in the new order by passing the list as argument:
        df_numeric = df_numeric[grouped_num_cols]
        
        if (add_suffix_to_aggregated_col == True):
        
            # Let's add a suffix. Check if suffix is None. If it is,
            # set "_" + aggregate_function as suffix:
            if (suffix is None):
                numeric_suffix = "_" + aggregate_function
            
            else:
                numeric_suffix = suffix
            
            # New columns names:
            new_num_names = [(str(name) + numeric_suffix) for name in numeric_list]
            # The str attribute guarantees that the name was read as string
            # Pick only the values from the second and concatenate the correct name 
            # for the aggregation column (eliminate the first element from the list):
            new_num_names = ['timestamp_grouped'] + new_num_names[1:]
            # Set new_num_names as the new columns names:
            df_numeric.columns = new_num_names
        
    
    #### LET'S AGGREGATE THE CATEGORICAL VARIABLES
    
    ## Check if there is a list of categorical features. If there is, run the next block of code:
    
    if (is_categorical == 1):
        # There are categorical columns to aggregate too - the list is not empty
        # Consider: a = np.array(['a', 'a', 'b'])
        # The stats.mode function stats.mode(a) returns an array as: 
        # ModeResult(mode=array(['a'], dtype='<U1'), count=array([2]))
        # If we select the first element from this array, stats.mode(a)[0], the function will 
        # return an array as array(['a'], dtype='<U1'). 
        # We want the first element from this array stats.mode(a)[0][0], 
        # which will return a string like 'a'
        
        # We can pass stats.mode as the aggregate function in agg: agg(stats.mode)
        
        # The original timestamps, already converted to Pandas timestamp objects, are stored in:
        # timestamp_list. So, we can again use this list to aggregation. It was saved as the
        # column 'timestamp_obj' from the dataframe df_copy
        
        # This will generate series where each element will be an array like:
        # series = ([mode_for_that_row], [X]), where X is the counting for that row. For example, if we
        # aggregate by week, and there is a 'categorical_value' by day, X will be 7.
        
        # to access a row from the series, for instance, row 0: series[0]. 
        # This element will be an array like:
        # ModeResult(mode=array([mode_for_that_row], dtype='<U19'), count=array([X])).
        # To access the first element of this array, we put another index: series[0][0].
        # This element will be like:
        # array([mode_for_that_row], dtype='<U19')
        # The mode is the first element from this array. To access it, we add another index:
        # series[0][0][0]. The result will be: mode_for_that_row
        
        ## Aggregate the df_categorical dataframe in terms of mode: 
        
        # stats.mode now only works for numerically encoded variables (the previous ordinal
        # encoding is required)
        # Encode to calculate the mode:
        enc_dec_obj = EncodeDecode(df_categorical = df_categorical, categorical_list = categorical_list[1:]) # Do not pick the timestamp to encode
        enc_dec_obj = enc_dec_obj.encode()
        df_categorical, new_encoded_cols, ordinal_encoding_list = enc_dec_obj.df_categorical, enc_dec_obj.new_encoded_cols, enc_dec_obj.ordinal_encoding_list
        # During the encoding procedure, the 'timestamp_obj' may have been incorrectly converted to string. 
        # Guarantee it is a timestamp for grouping:
        df_categorical['timestamp_obj'] = df_categorical['timestamp_obj'].astype('datetime64[ns]')

        if (start_time is not None):

            df_categorical = df_categorical.groupby(pd.Grouper(key = 'timestamp_obj' , freq = FREQ, origin = start_time), as_index = True, sort = True, observed = True).agg(stats.mode)

        elif (offset_time is not None):

            df_categorical = df_categorical.groupby(pd.Grouper(key = 'timestamp_obj' , freq = FREQ, offset = offset_time), as_index = True, sort = True, observed = True).agg(stats.mode)

        else:

            #Standard situation, when both start_time and offset_time are None
            df_categorical = df_categorical.groupby(pd.Grouper(key = 'timestamp_obj' , freq = FREQ), as_index = True, sort = True, observed = True).agg(stats.mode)
        
        print (f"Categorical variables of the dataframe grouped in terms of \'mode\' by every {number_of_periods_to_group} {frq_unit}.\n")
        print(f"The mode is the most common value observed (maximum of the statistical distribution) for the categorical variable when we group data in terms of {number_of_periods_to_group} {frq_unit}.\n")
        
        # delete the first value from categorical_list, which is 'timestamp_obj':
        # This step is required for not to calculate the mode of the timestamps in the next loop.
        del categorical_list[0]
        
        # Loop through each categorical variable:
        for cat_var in new_encoded_cols:
            # Make the column cat_var the list_of_modes itself:
            df_categorical[cat_var] = mode_retrieval(df_categorical[cat_var])
        
        # Again, it is not possible to set as_index = False so, the timestamp becomes the index. 
        # Let's create a column 'timestamp_grouped' to store this index:
        df_categorical['timestamp_grouped'] = df_categorical.index
        # Reset index:
        df_categorical = df_categorical.reset_index(drop = True)
        
        grouped_cat_cols = list(df_categorical.columns)[:-1]
        grouped_cat_cols = ['timestamp_grouped'] + grouped_cat_cols
        
        # Select the columns in the new order by passing the list as argument:
        df_categorical = df_categorical[grouped_cat_cols]

        # Reverse ordinal encoding
        enc_dec_obj = enc_dec_obj.decode(new_df = df_categorical)
        df_categorical, cleaned_df = enc_dec_obj.df_categorical, enc_dec_obj.cleaned_df
        
        if (add_suffix_to_aggregated_col == True):
        
            # Let's add a suffix. Check if suffix is None. If it is,
            # set "_" + aggregate_function as suffix:
            if (suffix is None):
                categorical_suffix = "_mode"
            
            else:
                categorical_suffix = suffix
            
            # New columns names:
            new_cat_names = [(str(name) + categorical_suffix) for name in categorical_list if (name != 'timestamp_grouped')]
            # Notice that we have already deleted 'timestamp_obj' from categorical_list,
            # avoiding the calculation of the timestamp modes. The condition in the list comprehension
            # avoids putting the suffix "_mode" on the timestamp column
            # So, now concatenate the correct name for the aggregation column:
            new_cat_names = ['timestamp_grouped'] + new_cat_names
            
            # Set new_num_names as the new columns names:
            df_categorical.columns = new_cat_names   
        
        
    if (is_cat_num == 2):
        # Both subsets are present. Remove the column from df_categorical:
        df_categorical.drop(columns = 'timestamp_grouped', inplace = True)
        
        # Concatenate the dataframes in the columns axis (append columns):
        DATASET = pd.concat([df_numeric, df_categorical], axis = 1, join = "inner")
    
    elif (is_categorical == 1):
        # There is only the categorical subset:
        DATASET = df_categorical
    
    elif (is_numeric == 1):
        # There is only the numeric subset:
        DATASET = df_numeric
        
    # Pandas .head(Y) method results in a dataframe containing the first Y rows of the 
    # original dataframe. The default .head() is Y = 5. Print first 10 rows of the 
    # new dataframe:
    
    if ControlVars.show_results:
        print("Dataframe successfully grouped. Check its 10 first rows (without the categorical/object variables):\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(DATASET.head(10))
                
        except: # regular mode
            print(DATASET.head(10))

    #Now return the grouped dataframe with the timestamp as the first column:
    
    return DATASET

   
def extract_timestamp_info (df, timestamp_tag_column, list_of_info_to_extract, list_of_new_column_names = None):
    """
    extract_timestamp_info (df, timestamp_tag_column, list_of_info_to_extract, list_of_new_column_names = None):
    
    : param: df: dataframe containing the timestamp.
    
    : param: timestamp_tag_column: declare as a string under quotes. This is the column from 
      which we will extract the timestamp.
    
    : param: list_of_info_to_extract: list of information to extract from the timestamp. Each information
      will be extracted as a separate column. The allowed values are:
      'year' (or 'y'), 'month' (or 'm'), 'week' (or 'w'), 'day' (or 'd'), 'hour' (or 'h'), 
      'minute' (or 'min'), 'second' (or 's'), 'microsecond' (or 'us'), 'nanosecond' (or 'ns'). 
      Declare as a list even if only one information is going to be extracted. For instance:
      list_of_info_to_extract = ['second'] extracts only the second.
      list_of_info_to_extract = ['year', 'month', 'week', 'day'] extracts year, month, week and day. 
    
    : param: list_of_new_column_names: list of names (strings) of the new created columns. 
      If no value is provided, it will be equals to extracted_info. For instance: if
      list_of_info_to_extract = ['year', 'month', 'week', 'day'] and list_of_new_column_names = None,
      the new columns will be named as 'year', 'month', 'week', and 'day'.
      WARNING: This list must contain the same number of elements of list_of_info_to_extract and both
      must be in the same order. Considering the same example of list, if list_of_new_column_names =
      ['col1', 'col2', 'col3', 'col4'], 'col1' will be referrent to 'year', 'col2' to 'month', 'col3'
      to 'week', and 'col4' to 'day'
    """
    
    # Create dataframe local copy to manipulate, avoiding that Pandas operates on
    # the original object; or that Pandas tries to set values on slices or copies,
    # resulting in unpredictable results.
    # Use the copy method to effectively create a second object with the same properties
    # of the input parameters, but completely independent from it.
    DATASET = df.copy(deep = True)
    
    # Check if the list of column names is None. If it is, make it equals to the list of extracted
    # information:
    if (list_of_new_column_names is None):
        
        list_of_new_column_names = list_of_info_to_extract
    
    # try parsing as np.datetime64 (more efficient, without loops):
    try:
        DATASET[timestamp_tag_column] = DATASET[timestamp_tag_column].astype('datetime64[ns]')
        
    except:

        DATASET[timestamp_tag_column] = [pd.Timestamp(timestamp, unit = 'ns') for timestamp in DATASET[timestamp_tag_column]]
    
    # 4. Sort the dataframe in ascending order of timestamps:
    DATASET = DATASET.sort_values(by = timestamp_tag_column, ascending = True)
    # Reset indices:
    DATASET = DATASET.reset_index(drop = True)

    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html

    #Use the extracted_info as key to access the correct command in the dictionary.
    #To access an item from a dictionary d = {'key1': item1, ...}, declare d['key1'],
    #as if you would do to access a column from a dataframe.
    
    #By doing so, you will select the extraction command from the dictionary:
    # Loop through each element of the dataset, access the timestamp, 
    # extract the information and store it in the correspondent position of the 
    # new_column. Again. The methods can only be applied to a single Timestamp object,
    # not to the series. That is why we must loop through each of them:

    # Now, loop through each one of the items from the list 'list_of_info_to_extract'.
    # For each element, we will extract the information indicated by that item.

    for extracted_info in list_of_info_to_extract:

        # name that the new column should have:
        new_column_name = extracted_info
        # The element will be referred as 'new_column_name'

        #start a list to store the values of the new column
        new_column_vals = []
        
        try: # try accessing the dt attribute:
            
            if ((extracted_info == 'year') | (extracted_info == 'y')):

                DATASET[new_column_name] = DATASET[timestamp_tag_column].dt.year
                # Check positions where one of the timestamps is not present, so the time attribute should be null too
                # Here, we cannot repeat the variable itself because the info is a float, not a date. So, we have to create a float var.
                # (np.nan) creates a float, not a missing date 'NaT'
                DATASET[new_column_name] = np.where(DATASET[timestamp_tag_column].isna(), np.nan, DATASET[new_column_name])

            elif ((extracted_info == 'month') | (extracted_info == 'm')):

                DATASET[new_column_name] = DATASET[timestamp_tag_column].dt.month
                DATASET[new_column_name] = np.where(DATASET[timestamp_tag_column].isna(), np.nan, DATASET[new_column_name])

            elif ((extracted_info == 'week') | (extracted_info == 'w')):

                DATASET[new_column_name] = DATASET[timestamp_tag_column].dt.isocalendar().week
                DATASET[new_column_name] = np.where(DATASET[timestamp_tag_column].isna(), np.nan, DATASET[new_column_name])

            elif ((extracted_info == 'day') | (extracted_info == 'd')):

                DATASET[new_column_name] = DATASET[timestamp_tag_column].dt.day
                DATASET[new_column_name] = np.where(DATASET[timestamp_tag_column].isna(), np.nan, DATASET[new_column_name])

            elif ((extracted_info == 'hour') | (extracted_info == 'h')):

                DATASET[new_column_name] = DATASET[timestamp_tag_column].dt.hour
                DATASET[new_column_name] = np.where(DATASET[timestamp_tag_column].isna(), np.nan, DATASET[new_column_name])

            elif ((extracted_info == 'minute') | (extracted_info == 'min')):

                DATASET[new_column_name] = DATASET[timestamp_tag_column].dt.minute
                DATASET[new_column_name] = np.where(DATASET[timestamp_tag_column].isna(), np.nan, DATASET[new_column_name])

            elif ((extracted_info == 'second') | (extracted_info == 's')):

                DATASET[new_column_name] = DATASET[timestamp_tag_column].dt.second
                DATASET[new_column_name] = np.where(DATASET[timestamp_tag_column].isna(), np.nan, DATASET[new_column_name])
            
            elif ((extracted_info == 'microsecond') | (extracted_info == 'us')):

                DATASET[new_column_name] = DATASET[timestamp_tag_column].dt.microsecond
                DATASET[new_column_name] = np.where(DATASET[timestamp_tag_column].isna(), np.nan, DATASET[new_column_name])
            
            elif ((extracted_info == 'nanosecond') | (extracted_info == 'ns')):

                DATASET[new_column_name] = DATASET[timestamp_tag_column].dt.nanosecond
                DATASET[new_column_name] = np.where(DATASET[timestamp_tag_column].isna(), np.nan, DATASET[new_column_name])

            else:

                raise InvalidInputsError("Invalid extracted information. Please select: year, month, week, day, hour, minute, or second.")

        except: # access the attributes from individual objects

            if ((extracted_info == 'year') | (extracted_info == 'y')):

                DATASET[new_column_name] = [pd.Timestamp(timestamp).year for timestamp in DATASET[timestamp_tag_column]]
                DATASET[new_column_name] = np.where(DATASET[timestamp_tag_column].isna(), np.nan, DATASET[new_column_name])

            elif ((extracted_info == 'month') | (extracted_info == 'm')):

                DATASET[new_column_name] = [pd.Timestamp(timestamp).month for timestamp in DATASET[timestamp_tag_column]]
                DATASET[new_column_name] = np.where(DATASET[timestamp_tag_column].isna(), np.nan, DATASET[new_column_name])

            elif ((extracted_info == 'week') | (extracted_info == 'w')):

                DATASET[new_column_name] = [pd.Timestamp(timestamp).week for timestamp in DATASET[timestamp_tag_column]]
                DATASET[new_column_name] = np.where(DATASET[timestamp_tag_column].isna(), np.nan, DATASET[new_column_name])

            elif ((extracted_info == 'day') | (extracted_info == 'd')):

                DATASET[new_column_name] = [pd.Timestamp(timestamp).day for timestamp in DATASET[timestamp_tag_column]]
                DATASET[new_column_name] = np.where(DATASET[timestamp_tag_column].isna(), np.nan, DATASET[new_column_name])

            elif ((extracted_info == 'hour') | (extracted_info == 'h')):

                DATASET[new_column_name] = [pd.Timestamp(timestamp).hour for timestamp in DATASET[timestamp_tag_column]]
                DATASET[new_column_name] = np.where(DATASET[timestamp_tag_column].isna(), np.nan, DATASET[new_column_name])

            elif ((extracted_info == 'minute') | (extracted_info == 'min')):

                DATASET[new_column_name] = [pd.Timestamp(timestamp).minute for timestamp in DATASET[timestamp_tag_column]]
                DATASET[new_column_name] = np.where(DATASET[timestamp_tag_column].isna(), np.nan, DATASET[new_column_name])

            elif ((extracted_info == 'second') | (extracted_info == 's')):

                DATASET[new_column_name] = [pd.Timestamp(timestamp).second for timestamp in DATASET[timestamp_tag_column]]
                DATASET[new_column_name] = np.where(DATASET[timestamp_tag_column].isna(), np.nan, DATASET[new_column_name])
            
            elif ((extracted_info == 'microsecond') | (extracted_info == 'us')):

                DATASET[new_column_name] = [pd.Timestamp(timestamp).microsecond for timestamp in DATASET[timestamp_tag_column]]
                DATASET[new_column_name] = np.where(DATASET[timestamp_tag_column].isna(), np.nan, DATASET[new_column_name])
            
            elif ((extracted_info == 'nanosecond') | (extracted_info == 'ns')):

                DATASET[new_column_name] = [pd.Timestamp(timestamp).nanosecond for timestamp in DATASET[timestamp_tag_column]]
                DATASET[new_column_name] = np.where(DATASET[timestamp_tag_column].isna(), np.nan, DATASET[new_column_name])

            else:

                raise InvalidInputsError("Invalid extracted information. Please select: year, month, week, day, hour, minute, or second.")

    if ControlVars.show_results:
        # Pandas .head(Y) method results in a dataframe containing the first Y rows of the 
        # original dataframe. The default .head() is Y = 5. Print first 10 rows of the 
        # new dataframe:
        print("Timestamp information successfully extracted. Check dataset\'s 10 first rows:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(DATASET.head(10))
                
        except: # regular mode
            print(DATASET.head(10))
        
        #Now that the information were retrieved from all Timestamps, return the new
        #dataframe:
    
    return DATASET


def calculate_delay (df, timestamp_tag_column, new_timedelta_column_name  = None, returned_timedelta_unit = None, return_avg_delay = True):
    """
    calculate_delay (df, timestamp_tag_column, new_timedelta_column_name  = None, returned_timedelta_unit = None, return_avg_delay = True):
    
    THIS FUNCTION CALCULATES THE DIFFERENCE (timedelta - delay) BETWEEN TWO SUCCESSIVE
     Timestamps from a same column
    
    : param: df: dataframe containing the two timestamp columns.
    : param: timestamp_tag_column: string containing the name of the column with the timestamps
    
    : param: new_timedelta_column_name: name of the new column. If no value is provided, the default
      name [timestamp_tag_column1]-[timestamp_tag_column2] will be given:
    
    : param: return_avg_delay = True will print and return the value of the average delay.
      return_avg_delay = False will omit this information
    
    Pandas Timedelta class: applicable to timedelta objects
      https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timedelta.html
      The delta method from the Timedelta class converts returns the timedelta in
      nanoseconds, guaranteeing the internal compatibility:
      https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timedelta.delta.html#pandas.Timedelta.delta
    
    : param: returned_timedelta_unit: unit of the new column. If no value is provided, the unit will be
      considered as nanoseconds. 
      POSSIBLE VALUES FOR THE TIMEDELTA UNIT:
      'year' (or 'y'), 'month' (or 'm'), 'day' (or 'd'), 'hour' (or 'h'), 'minute' (or 'min'), 
      'second' (or 's'), 'millisecond' (or 'ms'), 'microsecond' (or 'us'), 'nanosecond' (or 'ns').
    """
    
    if (new_timedelta_column_name is None):
        
        #apply the default name:
        new_timedelta_column_name = "time_delay"
    
    # START: CONVERT ALL TIMESTAMPS/DATETIMES/STRINGS TO pandas.Timestamp OBJECTS.
    # This will prevent any compatibility problems.
    
    #The pd.Timestamp function can handle a single timestamp per call. Then, we must
    # loop trough the series, and apply the function to each element.
    
    # Create dataframe local copy to manipulate, avoiding that Pandas operates on
    # the original object; or that Pandas tries to set values on slices or copies,
    # resulting in unpredictable results.
    # Use the copy method to effectively create a second object with the same properties
    # of the input parameters, but completely independent from it.
    DATASET = df.copy(deep = True)
    
    # try parsing as np.datetime64 (more efficient, without loops):
    try:
        DATASET[timestamp_tag_column] = DATASET[timestamp_tag_column].astype('datetime64[ns]')
        
        timestamp_list = list(DATASET[timestamp_tag_column])
        
    except:
        # START: CONVERT ALL TIMESTAMPS/DATETIMES/STRINGS TO pandas.Timestamp OBJECTS.
        timestamp_list = [pd.Timestamp(timestamp, unit = 'ns') for timestamp in DATASET[timestamp_tag_column]]

        # 3. Save the list as the column timestamp_tag_column itself:
        DATASET[timestamp_tag_column] = timestamp_list
    
    # 4. Sort the dataframe in ascending order of timestamps:
    DATASET = DATASET.sort_values(by = timestamp_tag_column, ascending = True)
    # Reset indices:
    DATASET = DATASET.reset_index(drop = True)
    
    # Let's create an array of timestamps:
    timestamps = np.array(DATASET[timestamp_tag_column], dtype = 'datetime64[ns]')
    # Start an empty array that will store the delayed timestamps:
    following_timestamp = np.empty(shape = timestamps.shape, dtype = 'datetime64[ns]')
    # This array contains random elements. The last element should be a missing value, since there is no future after the last timestamp
    # Example: if we had originally an array like [1 2 3 4], the delayed array must be [2 3 4 None] - it starts in the 2nd element,
    # but there is no element after 4.
    # Assign the missing value to the last index of the new array:
    following_timestamp[-1] = None
    # Now, fill the new timestamps with the old timestamps, starting from the second position. Only the last position will not be filled.
    # For that, slice the following_timestamp for picking all but the last element, and slice the old one to pick all from 2nd element:
    following_timestamp[:-1] = timestamps[1:]
     
    # Now, let's store it into a column (series) of the dataframe:
    timestamp_tag_column2 = timestamp_tag_column + "_delayed"

    DATASET[timestamp_tag_column2] = following_timestamp
    
    # Pandas Timestamps can be subtracted to result into a Pandas Timedelta.
    # We will apply the delta method from Pandas Timedeltas.
    
    # 4. Create a timedelta object as the difference between the timestamps:
    
    # NOTICE: Even though a list could not be submitted to direct operations like
    # sum, subtraction and multiplication, the series and NumPy arrays can. When we
    # copied the list as a new column on the dataframes, we converted the lists to series
    # called df[timestamp_tag_column1] and df[timestamp_tag_column2]. These two series now
    # can be submitted to direct operations.
    
    # Delay = next measurement (tag_column2, timestamp higher) - current measurement
    # (tag_column2, timestamp lower). Since we repeated the last timestamp twice,
    # in the last row it will be subtracted from itself, resulting in zero.
    # This is the expected, since we do not have a delay yet
    timedeltas = pd.Series(following_timestamp - timestamps)
    timedeltas_mask = ~timedeltas.isna() # values that are not null
    
    #This timedelta_obj is a series of timedelta64 objects. The Pandas Timedelta function
    # can process only one element of the series in each call. Then, we must loop through
    # the series to obtain the float values in nanoseconds. Even though this loop may 
    # look unecessary, it uses the Delta method to guarantee the internal compatibility.
    # Then, no errors due to manipulation of timestamps with different resolutions, or
    # due to the presence of global variables, etc. will happen. This is the safest way
    # to manipulate timedeltas.
    
    #5. Create an empty list to store the timedeltas in nanoseconds
    TimedeltaList = np.array([pd.Timedelta(timedelta_obj).value for timedelta_obj in timedeltas])
    # Keep only valid data, indicated in the boolean mask:
    TimedeltaList = np.where(timedeltas_mask, TimedeltaList, np.nan)
    
    #6. Loop through each timedelta_obj and convert it to nanoseconds using the Delta
    # method. Both pd.Timedelta function and the delta method can be applied to a 
    # a single object.
    #len(timedelta_obj) is the total of timedeltas present.
    # The .delta attribute was replaced by .value attribute. 
    # Both return the number of nanoseconds as an integer.
    # https://pandas.pydata.org/docs/reference/api/pandas.Timedelta.html
    
    #Notice that the loop is needed because Pandas cannot handle a series/list of
    #Timedelta objects simultaneously. It can manipulate a single object
    # in each call or iteration.
    
    #Now the list contains the timedeltas in nanoseconds and guarantees internal
    #compatibility.
    # The delta method converts the Timedelta object to an integer number equals to the
    # value of the timedelta in nanoseconds. Then we are now dealing with numbers, not
    # with timestamps.
    # Even though some steps seem unecessary, they are added to avoid errors and bugs
    # hard to identify, resultant from a timestamp assigned to the wrong type of
    # object.
    
    #The list is not as the series (columns) and arrays: it cannot be directly submitted to 
    # operations like sum, division, and multiplication. For doing so, we can loop through 
    # each element, what would be the case for using the Pandas Timestamp and Timedelta 
    # functions, which can only manipulate one object per call.
    # For simpler operations like division, we can convert the list to a NumPy array and
    # submit the entire array to the operation at the same time, avoiding the use of 
    # memory consuminh iterative methods.
    
    #Convert the timedelta list to a NumPy array:
    # Notice that we could have created a column with the Timedeltalist, so that it would
    # be converted to a series. On the other hand, we still did not defined the name of the
    # new column. So, it is easier to simply convert it to a NumPy array, and then copy
    # the array as a new column.
    
    #Convert the array to the desired unit by dividing it by the proper factor:
    
    if ((returned_timedelta_unit == 'year') | (returned_timedelta_unit == 'y')):
        
        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**9) #in seconds
        
        #2. Convert it to minutes (1 min = 60 s):
        TimedeltaList = TimedeltaList / 60.0 #in minutes
        
        #3. Convert it to hours (1 h = 60 min):
        TimedeltaList = TimedeltaList / 60.0 #in hours
        
        #4. Convert it to days (1 day = 24 h):
        TimedeltaList = TimedeltaList / 24.0 #in days
        
        #5. Convert it to years. 1 year = 365 days + 6 h = 365 days + 6/24 h/(h/day)
        # = (365 + 1/4) days = 365.25 days
        
        TimedeltaList = TimedeltaList / (365.25) #in years
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in years. Considered 1 year = 365 days + 6 h.\n")
    
    
    elif ((returned_timedelta_unit == 'month') | (returned_timedelta_unit == 'm')):
        
        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**9) #in seconds
        
        #2. Convert it to minutes (1 min = 60 s):
        TimedeltaList = TimedeltaList / 60.0 #in minutes
        
        #3. Convert it to hours (1 h = 60 min):
        TimedeltaList = TimedeltaList / 60.0 #in hours
        
        #4. Convert it to days (1 day = 24 h):
        TimedeltaList = TimedeltaList / 24.0 #in days
        
        #5. Convert it to months. Consider 1 month = 30 days
        
        TimedeltaList = TimedeltaList / (30.0) #in months
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in months. Considered 1 month = 30 days.\n")
        
    
    elif ((returned_timedelta_unit == 'day') | (returned_timedelta_unit == 'd')):
        
        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**9) #in seconds
        
        #2. Convert it to minutes (1 min = 60 s):
        TimedeltaList = TimedeltaList / 60.0 #in minutes
        
        #3. Convert it to hours (1 h = 60 min):
        TimedeltaList = TimedeltaList / 60.0 #in hours
        
        #4. Convert it to days (1 day = 24 h):
        TimedeltaList = TimedeltaList / 24.0 #in days
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in days.\n")


    elif ((returned_timedelta_unit == 'hour') | (returned_timedelta_unit == 'h')):
        
        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**9) #in seconds
        
        #2. Convert it to minutes (1 min = 60 s):
        TimedeltaList = TimedeltaList / 60.0 #in minutes
        
        #3. Convert it to hours (1 h = 60 min):
        TimedeltaList = TimedeltaList / 60.0 #in hours
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in hours [h].\n")
    

    elif ((returned_timedelta_unit == 'minute') | (returned_timedelta_unit == 'min')):
        
        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**9) #in seconds
        
        #2. Convert it to minutes (1 min = 60 s):
        TimedeltaList = TimedeltaList / 60.0 #in minutes
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in minutes [min].\n")
        
        
    elif ((returned_timedelta_unit == 'second') | (returned_timedelta_unit == 's')):
        
        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**9) #in seconds
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in seconds [s].\n")
         
        
    elif ((returned_timedelta_unit == 'millisecond') | (returned_timedelta_unit == 'ms')):
        
        #1. Convert the list to milliseconds (1 ms = 10**6 ns, where 10**6 represents
        #the potentiation operation in Python, i.e., 10^6. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**6) #in milliseconds
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in milliseconds [ms].\n")
         
        
    elif ((returned_timedelta_unit == 'microsecond') | (returned_timedelta_unit == 'us')):
        
        #1. Convert the list to microseconds (1 us = 10**3 ns, where 10**3 represents
        #the potentiation operation in Python, i.e., 10^3. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**3) #in microseconds
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in microseconds [us].\n")


    else:
        
        returned_timedelta_unit = 'ns'
        print("No unit or invalid unit provided for timedelta. Then, returned timedelta in nanoseconds (1s = 10^9 ns).\n")
        
        #In case None unit is provided or a non-valid value or string is provided,
        #The calculus will be in nanoseconds.
    
    #Finally, create a column in the dataframe named as new_timedelta_column_name 
    # with the elements of TimedeltaList converted to the correct unit of time:
    
    #Append the selected unit as a suffix on the new_timedelta_column_name:
    new_timedelta_column_name = new_timedelta_column_name + "_" + returned_timedelta_unit
    
    # Check positions where one of the timestamps is not present, so the time attribute should be null too
    # Here, we cannot repeat the variable itself because the info is a float, not a date. So, we have to create a float var.
    # (np.nan) creates a float, not a missing date 'NaT'
    # LAST CHECKERS - Only to confirm
    TimedeltaList = np.where(DATASET[timestamp_tag_column].isna(), np.nan, TimedeltaList)
    # Also, check if DATASET[timestamp_tag_column2] is null:
    TimedeltaList = np.where(DATASET[timestamp_tag_column2].isna(), np.nan, TimedeltaList)
    
    DATASET[new_timedelta_column_name] = TimedeltaList
    
    # Pandas .head(Y) method results in a dataframe containing the first Y rows of the 
    # original dataframe. The default .head() is Y = 5. Print first 10 rows of the 
    # new dataframe:
    
    if ControlVars.show_results:
        print("Time delays successfully calculated. Check dataset\'s 10 first rows:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(DATASET.head(10))
                
        except: # regular mode
            print(DATASET.head(10))
    
    if (return_avg_delay == True):
        
        # To calculate the mean, we firstly need to remove the null entries:
        # Filter the numpy array to the opposite of the null entries (~)
        TimedeltaList = TimedeltaList[~np.isnan(TimedeltaList)]

        # Now we calculate the average value:
        avg_delay = np.average(TimedeltaList)
        
        if ControlVars.show_results:
            print(f"Average delay = {avg_delay:.6f} {returned_timedelta_unit}\n")
        
        # Return the dataframe and the average value:
        return DATASET, avg_delay
    
    #Finally, return the dataframe with the new column:
    
    else: 
        # Return only the dataframe
        return DATASET


def calculate_timedelta (df, timestamp_tag_column1, timestamp_tag_column2, timedelta_column_name  = None, returned_timedelta_unit = None):
    """
    calculate_timedelta (df, timestamp_tag_column1, timestamp_tag_column2, timedelta_column_name  = None, returned_timedelta_unit = None):
    
    THIS FUNCTION PERFORMS THE OPERATION df[timestamp_tag_column1] - df[timestamp_tag_colum2]
     The declaration order will determine the sign of the output.
    
    : param: df: dataframe containing the two timestamp columns.
    
    : param: timestamp_tag_column1: string containing the name of the column with the timestamp
      on the left (from which the right timestamp will be subtracted).
    
    : param: timestamp_tag_column2: string containing the name of the column with the timestamp
      on the right, that will be substracted from the timestamp on the left.
    
    : param: timedelta_column_name: name of the new column. If no value is provided, the default
      name [timestamp_tag_column1]-[timestamp_tag_column2] will be given:
    
    Pandas Timedelta class: applicable to timedelta objects
      https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timedelta.html
      The delta method from the Timedelta class converts the timedelta to
      nanoseconds, guaranteeing the internal compatibility:
      https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timedelta.delta.html#pandas.Timedelta.delta
    
    : param: returned_timedelta_unit: unit of the new column. If no value is provided, the unit will be
      considered as nanoseconds. 
      POSSIBLE VALUES FOR THE TIMEDELTA UNIT:
      'year' (or 'y'), 'month' (or 'm'), 'day' (or 'd'), 'hour' (or 'h'), 'minute' (or 'min'), 
      'second' (or 's'), 'millisecond' (or 'ms'), 'microsecond' (or 'us'), 'nanosecond' (or 'ns').
    """
    
    if (timedelta_column_name is None):
        
        #apply the default name:
        timedelta_column_name = "[" + timestamp_tag_column1 + "]" + "-" + "[" + timestamp_tag_column2 + "]"
    
    # START: CONVERT ALL TIMESTAMPS/DATETIMES/STRINGS TO pandas.Timestamp OBJECTS.
    # This will prevent any compatibility problems.
    
    #The pd.Timestamp function can handle a single timestamp per call. Then, we must
    # loop trough the series, and apply the function to each element.
    
    # Create dataframe local copy to manipulate, avoiding that Pandas operates on
    # the original object; or that Pandas tries to set values on slices or copies,
    # resulting in unpredictable results.
    # Use the copy method to effectively create a second object with the same properties
    # of the input parameters, but completely independent from it.
    DATASET = df.copy(deep = True)
    
    # try parsing as np.datetime64 (more efficient, without loops):
    try:
        DATASET[timestamp_tag_column1] = DATASET[timestamp_tag_column1].astype('datetime64[ns]')
        DATASET[timestamp_tag_column2] = DATASET[timestamp_tag_column2].astype('datetime64[ns]')
        
    except:
  
        DATASET[timestamp_tag_column1] = [pd.Timestamp(timestamp, unit = 'ns') for timestamp in DATASET[timestamp_tag_column1]]
        DATASET[timestamp_tag_column2] = [pd.Timestamp(timestamp, unit = 'ns') for timestamp in DATASET[timestamp_tag_column2]]

    
    # 4. Sort the dataframe in ascending order of timestamps:
    DATASET = DATASET.sort_values(by = [timestamp_tag_column1, timestamp_tag_column2], ascending = [True, True])
    # Reset indices:
    DATASET = DATASET.reset_index(drop = True)
    
    # Pandas Timestamps can be subtracted to result into a Pandas Timedelta.
    # We will apply the delta method from Pandas Timedeltas.
    
    #5. Create a timedelta object as the difference between the timestamps:
    
    # NOTICE: Even though a list could not be submitted to direct operations like
    # sum, subtraction and multiplication, the series and NumPy arrays can. When we
    # copied the list as a new column on the dataframes, we converted the lists to series
    # called df[timestamp_tag_column1] and df[timestamp_tag_column2]. These two series now
    # can be submitted to direct operations.
    
    timedeltas = pd.Series(np.array(DATASET[timestamp_tag_column1], dtype = 'datetime64[ns]') - np.array(DATASET[timestamp_tag_column2], dtype = 'datetime64[ns]'))
    timedeltas_mask = ~timedeltas.isna() # values that are not null
    #This timedelta_obj is a series of timedelta64 objects. The Pandas Timedelta function
    # can process only one element of the series in each call. Then, we must loop through
    # the series to obtain the float values in nanoseconds. Even though this loop may 
    # look unecessary, it uses the Delta method to guarantee the internal compatibility.
    # Then, no errors due to manipulation of timestamps with different resolutions, or
    # due to the presence of global variables, etc. will happen. This is the safest way
    # to manipulate timedeltas.
    
    #5. Create an empty list to store the timedeltas in nanoseconds
    TimedeltaList = np.array([pd.Timedelta(timedelta_obj).value for timedelta_obj in timedeltas])
    # Keep only valid data, indicated in the boolean mask:
    TimedeltaList = np.where(timedeltas_mask, TimedeltaList, np.nan)
    # LAST CHECKERS - Only to confirm
    TimedeltaList = np.where(DATASET[timestamp_tag_column1].isna(), np.nan, TimedeltaList)
    # Also, check if DATASET[timestamp_tag_column2] is null:
    TimedeltaList = np.where(DATASET[timestamp_tag_column2].isna(), np.nan, TimedeltaList)

    #Notice that the loop is needed because Pandas cannot handle a series/list of
    #Timedelta objects simultaneously. It can manipulate a single object
    # in each call or iteration.
    
    #Now the list contains the timedeltas in nanoseconds and guarantees internal
    #compatibility.
    # The delta method converts the Timedelta object to an integer number equals to the
    # value of the timedelta in nanoseconds. Then we are now dealing with numbers, not
    # with timestamps.
    # Even though some steps seem unecessary, they are added to avoid errors and bugs
    # hard to identify, resultant from a timestamp assigned to the wrong type of
    # object.
    
    #The list is not as the series (columns) and arrays: it cannot be directly submitted to 
    # operations like sum, division, and multiplication. For doing so, we can loop through 
    # each element, what would be the case for using the Pandas Timestamp and Timedelta 
    # functions, which can only manipulate one object per call.
    # For simpler operations like division, we can convert the list to a NumPy array and
    # submit the entire array to the operation at the same time, avoiding the use of 
    # memory consuminh iterative methods.
    
    #Convert the timedelta list to a NumPy array:
    # Notice that we could have created a column with the Timedeltalist, so that it would
    # be converted to a series. On the other hand, we still did not defined the name of the
    # new column. So, it is easier to simply convert it to a NumPy array, and then copy
    # the array as a new column.
  
    #Convert the array to the desired unit by dividing it by the proper factor:
    
    if ((returned_timedelta_unit == 'year') | (returned_timedelta_unit == 'y')):
        
        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**9) #in seconds
        
        #2. Convert it to minutes (1 min = 60 s):
        TimedeltaList = TimedeltaList / 60.0 #in minutes
        
        #3. Convert it to hours (1 h = 60 min):
        TimedeltaList = TimedeltaList / 60.0 #in hours
        
        #4. Convert it to days (1 day = 24 h):
        TimedeltaList = TimedeltaList / 24.0 #in days
        
        #5. Convert it to years. 1 year = 365 days + 6 h = 365 days + 6/24 h/(h/day)
        # = (365 + 1/4) days = 365.25 days
        
        TimedeltaList = TimedeltaList / (365.25) #in years
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in years. Considered 1 year = 365 days + 6 h.\n")
    
    
    elif ((returned_timedelta_unit == 'month') | (returned_timedelta_unit == 'm')):
        
        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**9) #in seconds
        
        #2. Convert it to minutes (1 min = 60 s):
        TimedeltaList = TimedeltaList / 60.0 #in minutes
        
        #3. Convert it to hours (1 h = 60 min):
        TimedeltaList = TimedeltaList / 60.0 #in hours
        
        #4. Convert it to days (1 day = 24 h):
        TimedeltaList = TimedeltaList / 24.0 #in days
        
        #5. Convert it to months. Consider 1 month = 30 days
        
        TimedeltaList = TimedeltaList / (30.0) #in months
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in months. Considered 1 month = 30 days.\n")
        
    
    elif ((returned_timedelta_unit == 'day') | (returned_timedelta_unit == 'd')):
        
        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**9) #in seconds
        
        #2. Convert it to minutes (1 min = 60 s):
        TimedeltaList = TimedeltaList / 60.0 #in minutes
        
        #3. Convert it to hours (1 h = 60 min):
        TimedeltaList = TimedeltaList / 60.0 #in hours
        
        #4. Convert it to days (1 day = 24 h):
        TimedeltaList = TimedeltaList / 24.0 #in days
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in days.\n")
        
    
    elif ((returned_timedelta_unit == 'hour') | (returned_timedelta_unit == 'h')):
        
        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**9) #in seconds
        
        #2. Convert it to minutes (1 min = 60 s):
        TimedeltaList = TimedeltaList / 60.0 #in minutes
        
        #3. Convert it to hours (1 h = 60 min):
        TimedeltaList = TimedeltaList / 60.0 #in hours
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in hours [h].\n")
    

    elif ((returned_timedelta_unit == 'minute') | (returned_timedelta_unit == 'min')):
        
        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**9) #in seconds
        
        #2. Convert it to minutes (1 min = 60 s):
        TimedeltaList = TimedeltaList / 60.0 #in minutes
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in minutes [min].\n")
        
        
    elif ((returned_timedelta_unit == 'second') | (returned_timedelta_unit == 's')):
        
        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**9) #in seconds
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in seconds [s].\n")
    

    elif ((returned_timedelta_unit == 'millisecond') | (returned_timedelta_unit == 'ms')):
        
        #1. Convert the list to milliseconds (1 ms = 10**6 ns, where 10**6 represents
        #the potentiation operation in Python, i.e., 10^6. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**6) #in milliseconds
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in milliseconds [ms].\n")
         
        
    elif ((returned_timedelta_unit == 'microsecond') | (returned_timedelta_unit == 'us')):
        
        #1. Convert the list to microseconds (1 us = 10**3 ns, where 10**3 represents
        #the potentiation operation in Python, i.e., 10^3. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**3) #in microseconds
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in microseconds [us].\n")
        
        
    else:
        
        returned_timedelta_unit = 'ns'
        print("No unit or invalid unit provided for timedelta. Then, returned timedelta in nanoseconds (1s = 10^9 ns).\n")
        
        #In case None unit is provided or a non-valid value or string is provided,
        #The calculus will be in nanoseconds.
    
    #Finally, create a column in the dataframe named as timedelta_column_name 
    # with the elements of TimedeltaList converted to the correct unit of time:
    
    #Append the selected unit as a suffix on the timedelta_column_name:
    timedelta_column_name = timedelta_column_name + "_" + returned_timedelta_unit
    
    DATASET[timedelta_column_name] = TimedeltaList
    
    # Sort the dataframe in ascending order of timestamps.
    # Importance order: timestamp1, timestamp2, timedelta
    DATASET = DATASET.sort_values(by = [timestamp_tag_column1, timestamp_tag_column2, timedelta_column_name], ascending = [True, True, True])
    # Reset indices:
    DATASET = DATASET.reset_index(drop = True)
    
    # Pandas .head(Y) method results in a dataframe containing the first Y rows of the 
    # original dataframe. The default .head() is Y = 5. Print first 10 rows of the 
    # new dataframe:
    
    if ControlVars.show_results:
        print("Timedeltas successfully calculated. Check dataset\'s 10 first rows:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(DATASET.head(10))
                
        except: # regular mode
            print(DATASET.head(10))
        
        #Finally, return the dataframe with the new column:
    
    return DATASET


def add_timedelta (df, timestamp_tag_column, timedelta, new_timestamp_col  = None, timedelta_unit = None):
    """
    add_timedelta (df, timestamp_tag_column, timedelta, new_timestamp_col  = None, timedelta_unit = None):
    
    THIS FUNCTION PERFORMS THE OPERATION ADDING A FIXED TIMEDELTA (difference of time
     or offset) to a timestamp.
    
    : param: df: dataframe containing the timestamp column.
    
    : param: timestamp_tag_column: string containing the name of the column with the timestamp
      to which the timedelta will be added to.
    
    : param: timedelta: numeric value of the timedelta.
      WARNING: simply input a numeric value, not a string with unit. e.g. timedelta = 2.4
      If you want to subtract a timedelta, input a negative value. e.g. timedelta = - 2.4
    
    : param: new_timestamp_col: name of the new column containing the obtained timestamp. 
      If no value is provided, the default name [timestamp_tag_column]+[timedelta] 
      will be given (at the end of the code, after we created the timedelta object 
      with correct units)
    
    Pandas Timedelta class: applicable to timedelta objects
      https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timedelta.html
      The delta method from the Timedelta class converts returns the timedelta in
      nanoseconds, guaranteeing the internal compatibility:
      https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timedelta.delta.html#pandas.Timedelta.delta
    
    : param: timedelta_unit: unit of the timedelta interval. If no value is provided, 
      the unit will be considered 'ns' (default). Possible values are:
      day' (or 'd'), 'hour' (or 'h'), 'minute' (or 'min'), 
      'second' (or 's'), 'millisecond' (or 'ms'), 'microsecond' (or 'us'), 'nanosecond' (or 'ns').
    """

    if (timedelta_unit is None):
        
        timedelta_unit = 'ns'
    
    # Pandas do not support timedeltas in years or months, since these values may
    # be ambiguous (e.g. a month may have 30 or 31 days, so an approximation would
    # be necessary).
    
    # START: CONVERT ALL TIMESTAMPS/DATETIMES/STRINGS TO pandas.Timestamp OBJECTS.
    # This will prevent any compatibility problems.
    
    #The pd.Timestamp function can handle a single timestamp per call. Then, we must
    # loop trough the series, and apply the function to each element.
    
    # Create dataframe local copy to manipulate, avoiding that Pandas operates on
    # the original object; or that Pandas tries to set values on slices or copies,
    # resulting in unpredictable results.
    # Use the copy method to effectively create a second object with the same properties
    # of the input parameters, but completely independent from it.
    DATASET = df.copy(deep = True)
    
    # try parsing as np.datetime64 (more efficient, without loops):
    try:
        DATASET[timestamp_tag_column] = DATASET[timestamp_tag_column].astype('datetime64[ns]')
        
    except:
        # START: CONVERT ALL TIMESTAMPS/DATETIMES/STRINGS TO pandas.Timestamp OBJECTS.
        #1. Start a list to store the Pandas timestamps:
        DATASET[timestamp_tag_column] = [pd.Timestamp(timestamp, unit = 'ns') for timestamp in DATASET[timestamp_tag_column]]
    
    # The Pandas Timestamp can be directly added to a Pandas Timedelta.
    # Check the valid values:
    timedeltas_mask = ~DATASET[timestamp_tag_column].isna() # values that are not null

    #Dictionary for converting the timedelta_unit to Pandas encoding for the
    # Timedelta method. to access the element of a dictionary d = {"key": element},
    # simply declare d['key'], as if you were accessing the column of a dataframe. Here,
    # the key is the argument of the function, whereas the element is the correspondent
    # Pandas encoding for this method. With this dictionary we simplify the search for the
    # proper time encoding: actually, depending on the Pandas method the encoding may be
    # 'd', "D" or "day" for day, for instance. So, we avoid having to check the whole
    # documentation by creating a simpler common encoding for the functions in this notebook.
    
    if ((timedelta_unit == 'day') | (timedelta_unit == 'd')):
        
        timedelta_unit = 'd'
        print("Returned timedelta in days.\n")

    elif ((timedelta_unit == 'hour') | (timedelta_unit == 'h')):
        
        timedelta_unit = 'h'
        print("Returned timedelta in hours [h].\n")
    
    elif ((timedelta_unit == 'minute') | (timedelta_unit == 'min')):
        
        timedelta_unit = 'min'
        print("Returned timedelta in minutes [min].\n")
            
    elif ((timedelta_unit == 'second') | (timedelta_unit == 's')):
        
        timedelta_unit = 's'
        print("Returned timedelta in seconds [s].\n")
         
    elif ((timedelta_unit == 'millisecond') | (timedelta_unit == 'ms')):
        
        timedelta_unit = 'ms'
        print("Returned timedelta in milliseconds [ms].\n")
         
    elif ((timedelta_unit == 'microsecond') | (timedelta_unit == 'us')):
        
        timedelta_unit = 'us'
        print("Returned timedelta in microseconds [us].\n")
        
    else:
        
        timedelta_unit = 'ns'
        print("No unit or invalid unit provided for timedelta. Then, returned timedelta in nanoseconds (1s = 10^9 ns).\n")

    #Create the Pandas timedelta object from the timedelta value and the selected
    # time units:
    timedelta = pd.Timedelta(timedelta, timedelta_unit)
    
    #A pandas Timedelta object has total compatibility with a pandas
    #Timestamp, so we can simply add the Timedelta to the Timestamp to obtain a new 
    #corrected timestamp.
    # Again, notice that the timedelta can be positive (sum of time), or negative
    # (subtraction of time).
    
    #Now, add the timedelta to the timestamp, and store it into a proper list/series:
    new_timestamps = DATASET[timestamp_tag_column].copy()
    # Check positions where one of the timestamps is not present, so the time attribute should be null
    new_timestamps = new_timestamps + timedelta
    # Where it is not null, keep the right value. Otherwise, pick the null.
    # Guarantee the correct data type
    new_timestamps = np.array(np.where(timedeltas_mask, new_timestamps, None), dtype = 'datetime64[ns]')
    
    #Finally, create a column in the dataframe named as new_timestamp_col
    #and store the new timestamps into it
    
    if (new_timestamp_col is None):
        
        #apply the default name:
        new_timestamp_col = "[" + timestamp_tag_column + "]" + "+" + "[" + str(timedelta) + "]"
        #The str function converts the timedelta object to a string, so it can be
        #concatenated in this line of code.
        #Notice that we defined the name of the new column at the end of the code so
        #that we already converted the 'timedelta' to a Timedelta object containing
        #the correct units.
    
    DATASET[new_timestamp_col] = new_timestamps
    
    # Sort the dataframe in ascending order of timestamps.
    # Importance order: timestamp, new_timestamp_col
    DATASET = DATASET.sort_values(by = [timestamp_tag_column, new_timestamp_col], ascending = [True, True])
    # Reset indices:
    DATASET = DATASET.reset_index(drop = True)
    
    # Pandas .head(Y) method results in a dataframe containing the first Y rows of the 
    # original dataframe. The default .head() is Y = 5. Print first 10 rows of the 
    # new dataframe:
    
    if ControlVars.show_results:
        print("Timedeltas successfully added. Check dataset\'s 10 first rows:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(DATASET.head(10))
                
        except: # regular mode
            print(DATASET.head(10))
    
    #Finally, return the dataframe with the new column:
    
    return DATASET
