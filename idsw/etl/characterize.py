def df_general_characterization (df):
    """
    df_general_characterization (df)

    : param: df - Pandas dataframe to be analyzed.
    """
    
    # Set a local copy of the dataframe:
    DATASET = df.copy(deep = True)

    # Show dataframe's header
    print("Dataframe\'s 10 first rows:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(DATASET.head(10))
            
    except: # regular mode
        print(DATASET.head(10))

    # Show dataframe's tail:
    # Line break before next information:
    print("\n")
    print("Dataframe\'s 10 last rows:\n")
    try:
        display(DATASET.tail(10))
    except:
        print(DATASET.tail(10))
    
    # Show dataframe's shape:
    # Line break before next information:
    print("\n")
    df_shape  = DATASET.shape
    print("Dataframe\'s shape = (number of rows, number of columns) =\n")
    try:
        display(df_shape)
    except:
        print(df_shape)
    
    # Show dataframe's columns:
    # Line break before next information:
    print("\n")
    df_columns_array = DATASET.columns
    print("Dataframe\'s columns =\n")
    try:
        display(df_columns_array)
    except:
        print(df_columns_array)
    
    # Show dataframe's columns types:
    # Line break before next information:
    print("\n")
    df_dtypes = DATASET.dtypes
    # Now, the df_dtypes seroes has the original columns set as index, but this index has no name.
    # Let's rename it using the .rename method from Pandas Index object:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Index.rename.html#pandas.Index.rename
    # To access the Index object, we call the index attribute from Pandas dataframe.
    # By setting inplace = True, we modify the object inplace, by simply calling the method:
    df_dtypes.index.rename(name = 'dataframe_column', inplace = True)
    # Let's also modify the series label or name:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.rename.html
    df_dtypes.rename('dtype_series', inplace = True)
    print("Dataframe\'s variables types:\n")
    try:
        display(df_dtypes)
    except:
        print(df_dtypes)
    
    # Show dataframe's general statistics for numerical variables:
    # Line break before next information:
    print("\n")
    df_general_statistics = DATASET.describe()
    print("Dataframe\'s general (summary) statistics for numeric variables:\n")
    try:
        display(df_general_statistics)
    except:
        print(df_general_statistics)
    
    # Show total of missing values for each variable:
    # Line break before next information:
    print("\n")
    total_of_missing_values_series = DATASET.isna().sum()
    # This is a series which uses the original column names as index
    proportion_of_missing_values_series = DATASET.isna().mean()
    percent_of_missing_values_series = proportion_of_missing_values_series * 100
    missingness_dict = {'count_of_missing_values': total_of_missing_values_series,
                    'proportion_of_missing_values': proportion_of_missing_values_series,
                    'percent_of_missing_values': percent_of_missing_values_series}
    
    df_missing_values = pd.DataFrame(data = missingness_dict)
    # Now, the dataframe has the original columns set as index, but this index has no name.
    # Let's rename it using the .rename method from Pandas Index object:
    df_missing_values.index.rename(name = 'dataframe_column', inplace = True)
    
    # Create a one row dataframe with the missingness for the whole dataframe:
    # Pass the scalars as single-element lists or arrays:
    one_row_data = {'dataframe_column': ['missingness_accross_rows'],
                    'count_of_missing_values': [len(DATASET) - len(DATASET.copy(deep = True).dropna(how = 'any'))],
                    'proportion_of_missing_values': [(len(DATASET) - len(DATASET.copy(deep = True).dropna(how = 'any')))/(len(DATASET))],
                    'percent_of_missing_values': [(len(DATASET) - len(DATASET.copy(deep = True).dropna(how = 'any')))/(len(DATASET))*100]
                    }
    one_row_df = pd.DataFrame(data = one_row_data)
    one_row_df.set_index('dataframe_column', inplace = True)
    
    # Append this one_row_df to df_missing_values:
    df_missing_values = pd.concat([df_missing_values, one_row_df])
    
    print("Missing values on each feature; and missingness considering all rows from the dataframe:")
    print("(note: \'missingness_accross_rows\' was calculated by: checking which rows have at least one missing value (NA); and then comparing total rows with NAs with total rows in the dataframe).\n")
    
    try:
        display(df_missing_values)
    except:
        print(df_missing_values)
    
    return df_shape, df_columns_array, df_dtypes, df_general_statistics, df_missing_values


def characterize_categorical_variables (df, timestamp_tag_column = None):
    """
    characterize_categorical_variables (df, timestamp_tag_column = None):
    
    : param: df: dataframe that will be analyzed
    
    : param: timestamp_tag_colum: name (header) of the column containing the
      timestamps. Keep timestamp_tag_column = None if the dataframe do not contain
      timestamps.
    """

    from pandas import json_normalize
    
    # pandas .loc method syntax syntax:
    # dataset.loc[dataset["CatVar"] == 'Value1', "EncodedColumn"] = 1
    # dataset.loc[boolean_filter, EncodedColumn"] = value,
    # boolean_filter = (dataset["CatVar"] == 'Value1') will be True when the 
    # equality is verified. The .loc method filters the dataframe, accesses the
    # column declared after the comma and inputs the value defined (e.g. value = 1)
    
    # Set a local copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    
    # Get the list of columns:
    cols_list = list(DATASET.columns)
    
    # Start a list of categorical columns:
    categorical_list = []
    is_categorical = 0 # start the variable
    
    # Start a timestamp list that will be empty if there is no timestamp_tag_column
    timestamp_list = []
    if (timestamp_tag_column is not None):
        timestamp_list.append(timestamp_tag_column)
    
    # List the possible numeric data types for a Pandas dataframe column:
    numeric_dtypes = [np.int16, np.int32, np.int64, np.float16, np.float32, np.float64]
    
    # Loop through all valid columns (cols_list)
    for column in cols_list:
        
        # Check if the column is neither in timestamp_list nor in
        # categorical_list yet:
        
        if ((column not in categorical_list) & (column not in timestamp_list)):
            # Notice that, since we already selected the 'timestamp_obj', we remove the original timestamps.
            column_data_type = DATASET[column].dtype
            
            if (column_data_type not in numeric_dtypes):
                
                # Append to categorical columns list:
                categorical_list.append(column)
    
    # Subset the dataframe:
    if (len(categorical_list) >= 1):
        
        DATASET = DATASET[categorical_list]
        is_categorical = 1
    
    # Start a list to store the results:
    summary_list = []
    # It will be a list of dictionaries.
    
    # Loop through all variables on the list:
    for categorical_var in categorical_list:
        
        # Get unique vals and respective counts.

        # Start dictionary that will be appended as a new element from the list:
        # The main dictionary will be an element of the list
        unique_dict = {'categorical_variable': categorical_var}
        
        # Start a list of unique values:
        unique_vals = []

        # Now, check the unique values of the categorical variable:
        unique_vals_array = DATASET[categorical_var].unique()
        # unique_vals_array is a NumPy array containing the different values from the categorical variable.

        # Total rows:
        total_rows = len(DATASET)

        # Check the total of missing values
        # Set a boolean_filter for checking if the row contains a missing value
        boolean_filter = DATASET[categorical_var].isna()

        # Calculate the total of elements when applying the filter:
        total_na = DATASET[categorical_var].isna().sum()

        # Create a dictionary for the missing values:
        na_dict = {
                    'value': np.nan, 
                    'counts_of_occurences': total_na,
                    'percent_of_occurences': ((total_na/total_rows)*100)
                    }
        
        
        # Nest this dictionary as an element from the list unique_vals.
        unique_vals.append(na_dict)
        # notice that the dictionary was nested into a list, which will be itself
        # nested as an element of the dictionary unique_dict
        
        # Now loop through each possible element on unique_vals_array
        for unique_val in unique_vals_array:

            # loop through each possible value of the array. The values are called 'unique_val'
            # Check if the value is not none:
            
            # Depending on the type of variable, the following error may be raised:
            # func 'isnan' not supported for the input types, and the inputs could not be safely coerced 
            # to any supported types according to the casting rule ''safe''
            # To avoid it, we can set the variable as a string using the str attribute and check if
            # the value is not neither 'nan' nor 'NaN'. That is because pandas will automatically convert
            # identified null values to np.nan
            
            # So, since The unique method creates the strings 'nan' or 'NaN' for the missing values,
            # if we read unique_val as string using the str attribute, we can filter out the
            # values 'nan' or 'NaN', which may be present together with the None and the float
            # np.nan:
            if ((str(unique_val) != 'nan') & (str(unique_val) != 'NaN') & (unique_val is not None)):
                # If one of these conditions is true, the value is None, 'NaN' or 'nan'
                # so this condition does not run.
                # It runs if at least one value is not a missing value
                # (only when the value is neither None nor np.nan)

                # create a filter to select only the entries where the column == unique_val:
                boolean_filter = (DATASET[categorical_var] == unique_val)
                # Calculate the total of elements when applying the filter:
                total_elements = len(DATASET[boolean_filter])

                # Create a dictionary for these values:
                # Use the same keys as before:
                cat_var_dict = {
                    
                                'value': unique_val, 
                                'counts_of_occurences': total_elements,
                                'percent_of_occurences': ((total_elements/total_rows)*100)
                    
                                }
                
                # Nest this dictionary as an element from the list unique_vals.
                unique_vals.append(cat_var_dict)
                # notice that the dictionary was nested into a list, which will be itself
                # nested as an element of the dictionary unique_dict
        
        # Nest the unique_vals list as an element of the dictionary unique_dict:
        # Set 'unique_values' as the key, and unique_vals as value
        unique_dict['unique_values'] = unique_vals
        # Notice that unique_vals is a list where each element is a dictionary with information
        # from a given unique value of the variable 'categorical_var' being analyzed.
        
        # Finally, append 'unique_dict' as an element of the list summary_list:
        summary_list.append(unique_dict)
        
    
    # We created a highly nested JSON structure with the following format:
    
    # summary_list = [
    #          {
    #            'categorical_variable': categorical_var1,
    #            'unique_values': [
    #                             {
    #                                'value': np.nan, 
    #                               'counts_of_occurences': total_na,
    #                               'percent_of_occurences': ((total_na/total_rows)*100)
    #                      },  {
    #
    #                           'value': unique_val_1, 
    #                           'counts_of_occurences': total_elements_1,
    #                           'percent_of_occurences': ((total_elements_1/total_rows)*100)
    #               
    #                     }, ... , {
    #                           'value': unique_val_N, 
    #                           'counts_of_occurences': total_elements_N,
    #                           'percent_of_occurences': ((total_elements_N/total_rows)*100)
    #               
    #                     }
    #                    ]
    #                 }, ... {
    #                        'categorical_variable': categorical_var_M,
    #                        'unique_values': [...]
    #                       }
    # ]

    if (is_categorical == 1):
        # Notice that, if !=1, the list is empty, so the previous loop is not executed.
        # Now, call the same methods used in function json_obj_to_dataframe to 
        # flat the list of dictionaries, if they are present:
    
        JSON = summary_list
        JSON_RECORD_PATH = 'unique_values'
        JSON_FIELD_SEPARATOR = "_"
        JSON_METADATA_PREFIX_LIST = ['categorical_variable']

        cat_vars_summary = json_normalize(JSON, record_path = JSON_RECORD_PATH, sep = JSON_FIELD_SEPARATOR, meta = JSON_METADATA_PREFIX_LIST)
        # JSON_METADATA_PREFIX_LIST: list of strings (in quotes). Manipulates the parameter 
        # 'meta' from json_normalize method. Fields to use as metadata for each record in resulting 
        # table. Declare here the non-nested fields, i.e., the fields in the principal JSON. They
        # will be repeated in the rows of the dataframe to give the metadata (context) of the rows.

        print("\n") # line break
        print("Finished analyzing the categorical variables. Check the summary dataframe:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(cat_vars_summary)

        except: # regular mode
            print(cat_vars_summary)
        
        return cat_vars_summary
    
    else:
        raise InvalidInputsError ("The dataframe has no categorical variables to analyze.\n")

    
def visualize_and_characterize_missing_values (df, slice_time_window_from = None, slice_time_window_to = None, aggregate_time_in_terms_of = None):
    """
    visualize_and_characterize_missing_values (df, slice_time_window_from = None, slice_time_window_to = None, aggregate_time_in_terms_of = None):

    : param: df: dataframe to be analyzed
    
    : params: slice_time_window_from and slice_time_window_to (timestamps). When analyzing time series,
      use these parameters to observe only values in a given time range.
    
      slice_time_window_from: the inferior limit of the analyzed window. If you declare this value
      and keep slice_time_window_to = None, then you will analyze all values that comes after
      slice_time_window_from.
      slice_time_window_to: the superior limit of the analyzed window. If you declare this value
      and keep slice_time_window_from = None, then you will analyze all values until
      slice_time_window_to.
      If slice_time_window_from = slice_time_window_to = None, only the standard analysis with
      the whole dataset will be performed. If both values are specified, then the specific time
      window from 'slice_time_window_from' to 'slice_time_window_to' will be analyzed.
      e.g. slice_time_window_from = 'May-1976', and slice_time_window_to = 'Jul-1976'
      Notice that the timestamps must be declares in quotes, just as strings.
    
    : param: aggregate_time_in_terms_of = None. Keep it None if you do not want to aggregate the time
      series. Alternatively, set aggregate_time_in_terms_of = 'Y' or aggregate_time_in_terms_of = 
      'year' to aggregate the timestamps in years; set aggregate_time_in_terms_of = 'M' or
      'month' to aggregate in terms of months; or set aggregate_time_in_terms_of = 'D' or 'day'
      to aggregate in terms of days.
    """

    import missingno as msno
    # misssingno package is built for visualizing missing values. 
    
    print("Possible reasons for missing data:\n")
    print("One of the obvious reasons is that data is simply missing at random.")
    print("Other reasons might be that the missingness is dependent on another variable;")
    print("or it is due to missingness of the same variables or other variables.\n")
    
    print("Types of missingness:\n")
    print("Identifying the missingness type helps narrow down the methodologies that you can use for treating missing data.")
    print("We can group the missingness patterns into 3 broad categories:\n")
    
    print("Missing Completely at Random (MCAR)\n")
    print("Missingness has no relationship between any values, observed or missing.")
    print("Example: consider you have a class of students. There are a few students absent on any given day. The students are absent just randomly for their specific reasons. This is missing completely at random.\n")
    
    print("Missing at Random (MAR)\n")
    print("There is a systematic relationship between missingness and other observed data, but not the missing data.")
    print("Example: consider the attendance in a classroom of students during winter, where many students are absent due to the bad weather. Although this might be at random, the hidden cause might be that students sitting closer might have contracted a fever.\n")
    print("Missing at random means that there might exist a relationship with another variable.")
    print("In this example, the attendance is slightly correlated to the season of the year.")
    print("It\'s important to notice that, for MAR, missingness is dependent only on the observed values; and not the other missing values.\n")
    
    print("Missing not at Random (MNAR)\n")
    print("There is a relationship between missingness and its values, missing or non-missing.")
    print("Example: in our class of students, it is Sally\'s birthday. Sally and many of her friends are absent to attend her birthday party. This is not at all random as Sally and only her friends are absent.\n")
    
    # set a local copy of the dataframe:
    DATASET = df.copy(deep = True)
    
    # Start the agg_dict, a dictionary that correlates the input aggregate_time_in_terms_of to
    # the correspondent argument that must be passed to the matrix method:
    agg_dict = {
        
        'year': 'Y',
        'Y': 'Y',
        'month': 'M',
        'M': 'M',
        'day': 'D',
        'D':'D'
    }
    
    
    if not (aggregate_time_in_terms_of is None):
        # access the frequency in the dictionary
        frequency = agg_dict[aggregate_time_in_terms_of] 
    
    df_length = len(DATASET)
    print(f"Count of rows from the dataframe =\n")
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(df_length)
            
    except: # regular mode
        print(df_length)
    
    print("\n")

    # Show total of missing values for each variable:
    total_of_missing_values_series = DATASET.isna().sum()
    # This is a series which uses the original column names as index
    proportion_of_missing_values_series = DATASET.isna().mean()
    percent_of_missing_values_series = proportion_of_missing_values_series * 100
    missingness_dict = {'count_of_missing_values': total_of_missing_values_series,
                    'proportion_of_missing_values': proportion_of_missing_values_series,
                    'percent_of_missing_values': percent_of_missing_values_series}
    
    df_missing_values = pd.DataFrame(data = missingness_dict)
    # Now, the dataframe has the original columns set as index, but this index has no name.
    # Let's rename it using the .rename method from Pandas Index object:
    df_missing_values.index.rename(name = 'dataframe_column', inplace = True)
    
    # Create a one row dataframe with the missingness for the whole dataframe:
    # Pass the scalars as single-element lists or arrays:
    one_row_data = {'dataframe_column': ['missingness_accross_rows'],
                    'count_of_missing_values': [len(DATASET) - len(DATASET.copy(deep = True).dropna(how = 'any'))],
                    'proportion_of_missing_values': [(len(DATASET) - len(DATASET.copy(deep = True).dropna(how = 'any')))/(len(DATASET))],
                    'percent_of_missing_values': [(len(DATASET) - len(DATASET.copy(deep = True).dropna(how = 'any')))/(len(DATASET))*100]
                    }
    one_row_df = pd.DataFrame(data = one_row_data)
    one_row_df.set_index('dataframe_column', inplace = True)
    
    # Append this one_row_df to df_missing_values:
    df_missing_values = pd.concat([df_missing_values, one_row_df])
    
    print("Missing values on each feature; and missingness considering all rows from the dataframe:")
    print("(note: \'missingness_accross_rows\' was calculated by: checking which rows have at least one missing value (NA); and then comparing total rows with NAs with total rows in the dataframe).\n")
    
    try:
        display(df_missing_values)    
    except:
        print(df_missing_values)
    print("\n") # line_break
    
    print("Bar chart of the missing values - Nullity bar:\n")
    msno.bar(DATASET)
    plt.show()
    print("\n")
    print("The nullity bar allows us to visualize the completeness of the dataframe.\n")
    
    print("Nullity Matrix: distribution of missing values through the dataframe:\n")
    msno.matrix(DATASET)
    plt.show()
    print("\n")
    
    if not ((slice_time_window_from is None) | (slice_time_window_to is None)):
        
        # There is at least one of these two values for slicing:
        if not ((slice_time_window_from is None) & (slice_time_window_to is None)):
                # both are present
                
                if not (aggregate_time_in_terms_of is None):
                    print("Nullity matrix for the defined time window and for the selected aggregation frequency:\n")
                    msno.matrix(DATASET.loc[slice_time_window_from:slice_time_window_to], freq = frequency)
                    
                else:
                    # do not aggregate:
                    print("Nullity matrix for the defined time window:\n")
                    msno.matrix(DATASET.loc[slice_time_window_from:slice_time_window_to])
                
                plt.show()
                print("\n")
        
        elif not (slice_time_window_from is None):
            # slice only from the start. The condition where both limits were present was already
            # checked. To reach this condition, only one is not None
            # slice from 'slice_time_window_from' to the end of dataframe
            
                if not (aggregate_time_in_terms_of is None):
                    print("Nullity matrix for the defined time window and for the selected aggregation frequency:\n")
                    msno.matrix(DATASET.loc[slice_time_window_from:], freq = frequency)
                
                else:
                    # do not aggregate:
                    print("Nullity matrix for the defined time window:\n")
                    msno.matrix(DATASET.loc[slice_time_window_from:])
        
                plt.show()
                print("\n")
            
        else:
        # equivalent to elif not (slice_time_window_to is None):
            # slice only from the beginning to the upper limit. 
            # The condition where both limits were present was already checked. 
            # To reach this condition, only one is not None
            # slice from the beginning to 'slice_time_window_to'
            
                if not (aggregate_time_in_terms_of is None):
                    print("Nullity matrix for the defined time window and for the selected aggregation frequency:\n")
                    msno.matrix(DATASET.loc[:slice_time_window_to], freq = frequency)
                
                else:
                    # do not aggregate:
                    print("Nullity matrix for the defined time window:\n")
                    msno.matrix(DATASET.loc[:slice_time_window_to])
                
                plt.show()
                print("\n")
    
    else:
        # Both slice limits are not. Let's check if we have to aggregate the dataframe:
        if not (aggregate_time_in_terms_of is None):
                print("Nullity matrix for the selected aggregation frequency:\n")
                msno.matrix(DATASET, freq = frequency)
                plt.show()
                print("\n")
    
    print("The nullity matrix allows us to visualize the location of missing values in the dataset.")
    print("The nullity matrix describes the nullity in the dataset and appears blank wherever there are missing values.")
    print("It allows us to quickly analyze the patterns in missing values.")
    print("The sparkline on the right of the matrix summarizes the general shape of data completeness and points out the row with the minimum number of null values in the dataframe.")
    print("In turns, the nullity matrix shows the total counts of columns at its bottom.")
    print("We can previously slice the dataframe for a particular interval of analysis (e.g. slice the time interval) to obtain more clarity on the amount of missingness.")
    print("Slicing will be particularly helpful when analyzing large datasets.\n")
    print("MCAR: plotting the missingness matrix plot (nullity matrix) for a MCAR variable will show values missing at random, with no correlation or clear pattern.")
    print("Correlation here implies the dependency of missing values on another variable present or absent.\n")
    print("MAR: the nullity matrix for MAR can be visualized as the presence of many missing values for a given feature. In this case, there might be a reason for the missingness that cannot be directly observed.\n")
    print("MNAR: the nullity matrix for MNAR shows a strong correlation between the missingness of two variables A and B.")
    print("This correlation is easily observable by sorting the dataframe in terms of A or B before obtaining the matrix.\n")
    
    print("Missingness Heatmap:\n")
    msno.heatmap(DATASET)
    plt.show()
    print("\n")
    
    print("The missingness heatmap describes the correlation of missingness between columns.")
    print("The heatmap is a graph of correlation of missing values between columns.")
    print("It explains the dependencies of missingness between columns.")
    print("In simple terms, if the missingness for two columns are highly correlated, then the heatmap will show high values of coefficient of correlation R2 for them.")
    print("That is because columns where the missing values co-occur the maximum are highly related and vice-versa.\n")
    print("In the graph, the redder the color, the lower the correlation between the missing values of the columns.")
    print("In turns, the bluer the color, the higher the correlation of missingness between the two variables.\n")
    print("ATTENTION: before deciding if the missing values in one variable is correlated with other, so that they would be characterized as MAR or MNAR, check the total of missing values.")
    print("Even if the heatmap shows a certain degree of correlation, the number of missing values may be too small to substantiate that.")
    print("Missingness in very small number may be considered completely random, and missing values can be eliminated.\n")
    
    print("Missingness Dendrogram:\n")
    msno.dendrogram(DATASET)
    plt.show()
    print("\n")
    
    print("A dendrogram is a tree diagram that groups similar objects in close branches.")
    print("So, the missingness dendrogram is a tree diagram of missingness that describes correlation of variables by grouping similarly missing columns together.")
    print("To interpret this graph, read it from a top-down perspective.")
    print("Cluster leaves which are linked together at a distance of zero fully predict one another\'s presence.")
    print("In other words, when two variables are grouped together in the dendogram, one variable might always be empty while another is filled (the presence of one explains the missingness of the other), or they might always both be filled or both empty, and so on (the missingness of one explains the missigness of the other).\n")
    
    return df_missing_values


def visualizing_and_comparing_missingness_across_numeric_vars (df, column_to_analyze, column_to_compare_with, show_interpreted_example = False, grid = True, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    visualizing_and_comparing_missingness_across_numeric_vars (df, column_to_analyze, column_to_compare_with, show_interpreted_example = False, grid = True, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    : params: column_to_analyze, column_to_compare_with: strings (in quotes).
      column_to_analyze is the column from the dataframe df that will be analyzed in terms of
      missingness; whereas column_to_compare_with is the column to which column_to_analyze will
      be compared.
      e.g. column_to_analyze = 'column1' will analyze 'column1' from df.
      column_to_compare_with = 'column2' will compare 'column1' against 'column2'
    
    : param: show_interpreted_example: set as True if you want to see an example of a graphic analyzed and
      interpreted.
    """

    import os
    # Two conditions require the os library, so we import it at the beginning of the function,
    # to avoid importing it twice.
    import shutil # component of the standard library to move or copy files.
    
    print("Missingness across a variable:\n")
    print("In this analysis, we will graphically analyze the relationship between missing values and non-missing values.")
    print("To do so, we will start by visualizing the missingness of a variable against another variable.")
    print("The scatter plot will show missing values in one color, and non-missing values in other color.")
    print("It will allow us to visualize how missingness of a variable changes against another variable.")
    print("Analyzing the missingness of a variable against another variable helps you determine any relationships between missing and non-missing values.")
    print("This is very similar to how you found correlations of missingness between two columns.")
    print("In summary, we will plot a scatter plot to analyze if there is any correlation of missingness in one column against another column.\n")
    
    # To create the graph, we will use the matplotlib library. 
    # However, matplotlib skips all missing values while plotting. 
    # Therefore, we would need to first create a function that fills in dummy values for all the 
    # missing values in the DataFrame before plotting.
    
    # We will create a function 'fill_dummy_values' that fill in all columns in the DataFrame.
    #The operations involve shifting and scaling the column range with a scaling factor.
        
    # We use a for loop to produce dummy values for all the columns in a given DataFrame. 
    # We can also define the scaling factor so that we can resize the range of dummy values. 
    # In addition to the previous steps of scaling and shifting the dummy values, we'll also have to 
    # create a copy of the DataFrame to fill in dummy values first. Let's now use this function to 
    # create our scatterplot.
    
    # List the possible numeric data types for a Pandas dataframe column:
    numeric_dtypes = [np.int16, np.int32, np.int64, np.float16, np.float32, np.float64]
    
    # define a subfunction for filling the dummy values.
    # In your function definition, set the default value of scaling_factor to be 0.075:
    def fill_dummy_values(df, scaling_factor = 0.075):
        
        # To generate dummy values, we can use the 'rand()' function from 'numpy.random'. 
        # We first store the number of missing values in column_to_analyze to 'num_nulls'
        # and then generate an array of random dummy values of the size 'num_nulls'. 
        # The generated dummy values appear as shown beside on the graph. 
        
        # The rand function always outputs values between 0 and 1. 
        # However, you must observe that the values of both column_to_analyze and column_to_compare_with 
        # have their own ranges, that may be different. 
        # Hence we'll need to scale and shift the generated dummy values so that they nicely fit 
        # into the graph.
        
        from numpy.random import rand
        # https://numpy.org/doc/stable/reference/random/generated/numpy.random.rand.html?msclkid=7414313ace7611eca18491dd4e7e86ae
        
        df_dummy = df.copy(deep = True)
        # Get the list of columns from df_dummy.
        # Use the list attribute to convert the array df_dummy.columns to list:
        df_cols_list = list(df_dummy.columns)
        
        # Calculate the number of missing values in each column of the dummy DataFrame.
        for col_name in df_dummy:
            
            col = df_dummy[col_name]
            # Create a column informing if the element is missing (True)
            # or not (False):
            col_null = col.isnull()
            # Calculate number of missing values in this column:
            num_nulls = col_null.sum()
            
            # Return the index j of column col_name. 
            # Use the index method from lists, setting col_name as argument. It will return
            # the index of col_name from the list of columns
            # https://www.programiz.com/python-programming/methods/list/index#:~:text=The%20list%20index%20%28%29%20method%20can%20take%20a,-%20search%20the%20element%20up%20to%20this%20index?msclkid=a690b8dacfaa11ec8e84e10a50ae45ec
            j = df_cols_list.index(col_name)
            
            # Check if the column is a text or timestamp. In this case, the type
            # of column will be 'object'
            if (col.dtype not in numeric_dtypes):
                
                # Try converting it to a datetime64 object:
                
                try:
                    
                    col = (col).astype('datetime64[ns]')
                
                except:
                    
                    # It is not a timestamp, so conversion was not possible.
                    # Simply ignore it.
                    pass
                
            # Now, try to perform the scale adjustment:
            try:
                # Calculate column range
                col_range = (col.max() - col.min())

                # Scale the random values to scaling_factor times col_range
                # Calculate random values with the size of num_nulls.
                # The rand() function takes in as argument the size of the array to be generated
                # (i.e. the number num_nulls itself):
                
                try:
                    dummy_values = (rand(num_nulls) - 2) * (scaling_factor) * (col_range) + (col.min())
                
                except:
                    # It may be a timestamp, so we cannot multiply col_range and sum.
                    dummy_values = (rand(num_nulls) - 2) * (scaling_factor) + (col.min())
                
                # We can shift the dummy values from 0 and 1 to -2 and -1 by subtracting 2, as in:
                # (rand(num_nulls) - 2)
                # By doing this, we make sure that the dummy values are always below or lesser than 
                # the actual values, as can be observed from the graph.
                # So, by subtracting 2, we guarantee that the dummy values will be below the maximum 
                # possible.

                # Next, scale your dummy values by scaling_factor and multiply them by col_range:
                #  * (scaling_factor) * (col_range)
                # Finally add the bias: the minimum observed for that column col.min():
                # + (col.min())
                # When we shift the values to the minimum (col.min()), we make sure that the dummy 
                # values are just below the actual values.

                # Therefore, the procedure results in dummy values a distance apart from the 
                # actual values.

                # Loop through the array of dummy values generated:
                # Loop through each row of the dataframe:
                
                k = 0 # first element from the array of dummy values
                for i in range (0, len(df_dummy)):

                        # Check if the position is missing:
                        boolean_filter = col_null[i]
                        if (boolean_filter):

                            # Run if it is True.
                            # Fill the position in col_name with the dummy value
                            # at the position k from the array of dummy values.
                            # This array was created with a single element for each
                            # missing value:
                            df_dummy.iloc[i,j] = dummy_values[k]
                            # go to the next element
                            k = k + 1
                
            except:
                # It was not possible, because it is neither numeric nor timestamp.
                # Simply ignore it.
                pass
                
        return df_dummy

    # We fill the dummy values to 'df_dummy' with the function `fill_dummy_values`. 
    # The graph can be plotted with 'df_dummy.plot()' of 'x=column_to_analyze', 
    # 'y=column_to_compare_with', 'kind="scatter"' and 'alpha=0.5' for transparency. 
    
    # Call the subfunction for filling the dummy values:
    df_dummy = fill_dummy_values(df)
    
    # The object 'nullity' is the sum of the nullities of column_to_analyze and column_to_compare_with. 
    # It is a series of True and False values. 
    # True implies missing, while False implies not missing.
    
    # The nullity can be used to set the color of the data points with 'cmap="rainbow"'. 
    # Thus, we obtain the graph that we require.
    
    # Set the nullity of column_to_analyze and column_to_compare_with:
    nullity = ((df[column_to_analyze].isnull()) | (df[column_to_compare_with].isnull()))
    # For setting different colors to the missing and non-missing values, you can simply add 
    # the nullity, or the sum of null values of both respective columns that you are plotting, 
    # calculated using the .isnull() method. The nullity returns a Series of True or False 
    # (i.e., a boolean filter) where:
    # True - At least one of col1 or col2 is missing.
    # False - Neither of col1 and col2 values are missing.

    if (plot_title is None):
        plot_title = "missingness_of_" + "[" + column_to_analyze + "]" + "_vs_" + "[" + column_to_compare_with + "]"
    
    #Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
    fig = plt.figure(figsize = (12, 8))
    
    # Create a scatter plot of column_to_analyze and column_to_compare_with 
    df_dummy.plot(x = column_to_analyze, y = column_to_compare_with, 
                        kind = 'scatter', alpha = 0.5,
                        # Set color to nullity of column_to_analyze and column_to_compare_with
                        # alpha: transparency. alpha = 0.5 = 50% of transparency.
                        c = nullity,
                        # The c argument controls the color of the points in the plot.
                        cmap = 'rainbow',
                        grid = grid,
                        legend = True,
                        title = plot_title)
    
    if (export_png == True):
        # Image will be exported
        
        #check if the user defined a directory path. If not, set as the default root path:
        if (directory_to_save is None):
            #set as the default
            directory_to_save = ""
        
        #check if the user defined a file name. If not, set as the default name for this
        # function.
        if (file_name is None):
            #set as the default
            file_name = "comparison_of_missing_values"
        
        #check if the user defined an image resolution. If not, set as the default 110 dpi
        # resolution.
        if (png_resolution_dpi is None):
            #set as 330 dpi
            png_resolution_dpi = 330
        
        #Get the new_file_path
        new_file_path = os.path.join(directory_to_save, file_name)
        
        #Export the file to this new path:
        # The extension will be automatically added by the savefig method:
        plt.savefig(new_file_path, dpi = png_resolution_dpi, quality = 100, format = 'png', transparent = False) 
        #quality could be set from 1 to 100, where 100 is the best quality
        #format (str, supported formats) = 'png', 'pdf', 'ps', 'eps' or 'svg'
        #transparent = True or False
        # For other parameters of .savefig method, check https://indianaiproduction.com/matplotlib-savefig/
        print (f"Figure exported as \'{new_file_path}.png\'. Any previous file in this root path was overwritten.")
    
    #fig.tight_layout()
    
    ## Show an image read from an image file:
    ## import matplotlib.image as pltimg
    ## img=pltimg.imread('mydecisiontree.png')
    ## imgplot = plt.imshow(img)
    ## See linkedIn Learning course: "Supervised machine learning and the technology boom",
    ##  Ex_Files_Supervised_Learning, Exercise Files, lesson '03. Decision Trees', '03_05', 
    ##  '03_05_END.ipynb'
    plt.show()
    print("Plot Legend:") 
    print("1 = Missing value")
    print("0 = Non-missing value")
    
    if (show_interpreted_example):
        # Run if it is True. Requires TensorFlow to load. Load the extra library only
        # if necessary:
        from html2image import Html2Image
        from tensorflow.keras.preprocessing.image import img_to_array, load_img
        # img_to_array: convert the image into its numpy array representation
        
        # Download the images to the notebook's workspace:
        
        # Alternatively, use "wget GNU" (cannot use as .py file):
        # Use the command !wget to download web content:
        #example_na1 = !wget --no-check-certificate https://github.com/marcosoares-92/img_examples_guides/raw/main/example_na1.PNG example_na1.png
        #example_na2 = !wget --no-check-certificate https://github.com/marcosoares-92/img_examples_guides/raw/main/example_na2.PNG example_na2.png
        #example_na3 = !wget --no-check-certificate https://github.com/marcosoares-92/img_examples_guides/raw/main/example_na3.PNG example_na3.png
        #example_na4 = !wget --no-check-certificate https://github.com/marcosoares-92/img_examples_guides/raw/main/example_na4.PNG example_na4.png
        # When saving the !wget calls as variables, we silent the verbosity of the Wget GNU.
        # Then, user do not see that a download has been made.
        # To check the help from !wget GNU, type and run a cell with: 
        # ! wget --help
        
        url1 = "https://github.com/marcosoares-92/img_examples_guides/raw/main/example_na1.PNG"
        url2 = "https://github.com/marcosoares-92/img_examples_guides/raw/main/example_na2.PNG"
        url3 = "https://github.com/marcosoares-92/img_examples_guides/raw/main/example_na3.PNG"
        url4 = "https://github.com/marcosoares-92/img_examples_guides/raw/main/example_na4.PNG"
        
        # Create a new folder to store the images, if the folder do not exists:
        new_dir = "tmp"
        os.makedirs(new_dir, exist_ok = True)
        # exist_ok = True creates the directory only if it does not exist.
        
        # Instantiate the class Html2Image:
        html_img = Html2Image()
        # Download the images:
        # pypi.org/project/html2image/
        img1 = html_img.screenshot(url = url1, save_as = "example_na1.PNG", size = (500, 500))
        img2 = html_img.screenshot(url = url2, save_as = "example_na2.PNG", size = (500, 500))
        img3 = html_img.screenshot(url = url3, save_as = "example_na3.PNG", size = (500, 500))
        img4 = html_img.screenshot(url = url4, save_as = "example_na4.PNG", size = (500, 500))
        # If size is omitted, the image is downloaded in the low-resolution default.
        # save_as must be a file name, a path is not accepted.
        # Make the output from the method equals to a variable eliminates its verbosity
        
        # Create the new paths for the images:
        img1_path = os.path.join(new_dir, "example_na1.PNG")
        img2_path = os.path.join(new_dir, "example_na2.PNG")
        img3_path = os.path.join(new_dir, "example_na3.PNG")
        img4_path = os.path.join(new_dir, "example_na4.PNG")
        
        # Move the image files to their new paths:
        # use shutil.move(source, destination) method to move the files:
        # pynative.com/python-move-files
        # docs.python.org/3/library/shutil.html
        shutil.move("example_na1.PNG", img1_path)
        shutil.move("example_na2.PNG", img2_path)
        shutil.move("example_na3.PNG", img3_path)
        shutil.move("example_na4.PNG", img4_path)
        
        # Load the images and save them on variables:
        sample_image1 = load_img(img1_path)
        sample_image2 = load_img(img2_path)
        sample_image3 = load_img(img3_path)
        sample_image4 = load_img(img4_path)
        
        print("\n")
        print("Example of analysis:\n")
        
        print("Consider the following \'diabetes\' dataset, where scatterplot of \'Serum_Insulin\' and \'BMI\' illustrated below shows the non-missing values in purple and the missing values in red.\n")
        
        # Image example 1:
        # show image with plt.imshow function:
        fig = plt.figure(figsize = (12, 8))
        plt.imshow(sample_image1)
        # If the image is black and white, you can color it with a cmap as 
        # fig.set_cmap('hot')
        #set axis off:
        plt.axis('off')
        plt.show()
        print("\n")
        
        print("The red points along the y-axis are the missing values of \'Serum_Insulin\' plotted against their \'BMI\' values.\n")
        # Image example 2:
        # show image with plt.imshow function:
        fig = plt.figure(figsize = (12, 8))
        plt.imshow(sample_image2)
        plt.axis('off')
        plt.show()
        print("\n")
        
        print("Likewise, the points along the x-axis are the missing values of \'BMI\' against their \'Serum_Insulin\' values.\n")
        # show image with plt.imshow function:
        fig = plt.figure(figsize = (12, 8))
        plt.imshow(sample_image3)
        plt.axis('off')
        plt.show()
        print("\n")
        
        print("The bottom-left corner represents the missing values of both \'BMI\' and \'Serum_Insulin\'.\n")
        # Image example 4:
        # show image with plt.imshow function:
        fig = plt.figure(figsize = (12, 8))
        plt.imshow(sample_image4)
        plt.axis('off')
        plt.show()
        print("\n")
        
        print("To interprete this graph, observe that the missing values of \'Serum_Insulin\' are spread throughout the \'BMI\' column.")
        print("Thus, we do not observe any specific correlation between the missingness of \'Serum_Insulin\' and \'BMI\'.\n")
        
        # Finally, before finishing the function, 
        # delete (remove) the files from the notebook's workspace.
        # The os.remove function deletes a file or directory specified.
        os.remove(img1_path)
        os.remove(img2_path)
        os.remove(img3_path)
        os.remove(img4_path)
        
        # Check if the tmp folder is empty:
        size = os.path.getsize(new_dir)
        # os.path.getsize returns the total size in Bytes from a folder or a file.
        
        # Get the list of sub-folders, files or subdirectories (the content) from the folder:
        list_of_contents = os.listdir(new_dir)
        # doc.python.org/3/library/os.html
        # It returns a list of strings representing the paths of each file or directory 
        # in the analyzed folder.
        
        # If the size is 0 and the length of the list_of_contents is also zero (i.e., there is no
        # previous sub-directory created), then remove the directory:
        if ((size == 0) & (len(list_of_contents) == 0)):
            os.rmdir(new_dir)


def handle_missing_values (df, subset_columns_list = None, drop_missing_val = True, fill_missing_val = False, eliminate_only_completely_empty_rows = False, min_number_of_non_missing_val_for_a_row_to_be_kept = None, value_to_fill = None, fill_method = "fill_with_zeros", interpolation_order = 'linear'):
    """
    handle_missing_values (df, subset_columns_list = None, drop_missing_val = True, fill_missing_val = False, eliminate_only_completely_empty_rows = False, min_number_of_non_missing_val_for_a_row_to_be_kept = None, value_to_fill = None, fill_method = "fill_with_zeros", interpolation_order = 'linear'):
    
    numpy has no function mode, but scipy's stats module has.
      https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mode.html?msclkid=ccd9aaf2cb1b11ecb57c6f4b3e03a341
    Pandas dropna method: remove rows containing missing values.
     Pandas fillna method: fill missing values.
     Pandas interpolate method: fill missing values with interpolation:
     https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.dropna.html
     https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.fillna.html
     https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.interpolate.html#pandas.DataFrame.interpolate
    
    
    : param: subset_columns_list = list of columns to look for missing values. Only missing values
      in these columns will be considered for deciding which columns to remove.
      Declare it as a list of strings inside quotes containing the columns' names to look at,
      even if this list contains a single element. e.g. subset_columns_list = ['column1']
      will check only 'column1'; whereas subset_columns_list = ['col1', 'col2', 'col3'] will
      chek the columns named as 'col1', 'col2', and 'col3'.
      ATTENTION: Subsets are considered only for dropping missing values, not for filling.
    
    : param: drop_missing_val = True to eliminate the rows containing missing values.
    
    : param: fill_missing_val = False. Set this to True to activate the mode for filling the missing
      values.
    
    : param: eliminate_only_completely_empty_rows = False - This parameter shows effect only when
      drop_missing_val = True. If you set eliminate_only_completely_empty_rows = True, then
      only the rows where all the columns are missing will be eliminated.
      If you define a subset, then only the rows where all the subset columns are missing
      will be eliminated.
    
    : param: min_number_of_non_missing_val_for_a_row_to_be_kept = None - 
      This parameter shows effect only when drop_missing_val = True. 
      If you set min_number_of_non_missing_val_for_a_row_to_be_kept equals to an integer value,
      then only the rows where at least this integer number of non-missing values will be kept
      after dropping the NAs.
      e.g. if min_number_of_non_missing_val_for_a_row_to_be_kept = 2, only rows containing at
      least two columns without missing values will be kept.
      If you define a subset, then the criterium is applied only to the subset.
    
    : param: value_to_fill = None - This parameter shows effect only when
      fill_missing_val = True. Set this parameter as a float value to fill all missing
      values with this value. e.g. value_to_fill = 0 will fill all missing values with
      the number 0. You can also pass a function call like 
      value_to_fill = np.sum(dataset['col1']). In this case, the missing values will be
      filled with the sum of the series dataset['col1']
      Alternatively, you can also input a string to fill the missing values. e.g.
      value_to_fill = 'text' will fill all the missing values with the string "text".
    
      You can also input a dictionary containing the column(s) to be filled as key(s);
      and the values to fill as the correspondent values. For instance:
      value_to_fill = {'col1': 10} will fill only 'col1' with value 10.
      value_to_fill = {'col1': 0, 'col2': 'text'} will fill 'col1' with zeros; and will
      fill 'col2' with the value 'text'
    
    : param: fill_method = "fill_with_zeros". - This parameter shows effect only 
      when fill_missing_val = True.
      Alternatively: fill_method = "fill_with_zeros" - fill all the missing values with 0
    
      fill_method = "fill_with_value_to_fill" - fill the missing values with the value
      defined as the parameter value_to_fill
    
      fill_method = "fill_with_avg_or_mode" - fill the missing values with the average value for 
      each column, if the column is numeric; or fill with the mode, if the column is categorical.
      The mode is the most commonly observed value.
    
      fill_method = "ffill" - Forward (pad) fill: propagate last valid observation forward 
      to next valid.
      fill_method = 'bfill' - backfill: use next valid observation to fill gap.
      fill_method = 'nearest' - 'ffill' or 'bfill', depending if the point is closest to the
      next or to the previous non-missing value.
    
      fill_method = "fill_by_interpolating" - fill by interpolating the previous and the 
      following value. For categorical columns, it fills the
      missing with the previous value, just as like fill_method = 'ffill'
      https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.interpolate.html#pandas.DataFrame.interpolate
    
    : param: interpolation_order: order of the polynomial used for interpolating if fill_method =
      "fill_by_interpolating". If interpolation_order = None, interpolation_order = 'linear',
      or interpolation_order = 1, a linear (1st-order polynomial) will be used.
      If interpolation_order is an integer > 1, then it will represent the polynomial order.
      e.g. interpolation_order = 2, for a 2nd-order polynomial; interpolation_order = 3 for a
      3rd-order, and so on.
    
      WARNING: if the fillna method is selected (fill_missing_val == True), but no filling
      methodology is selected, the missing values of the dataset will be filled with 0.
      The same applies when a non-valid fill methodology is selected.
      Pandas fillna method does not allow us to fill only a selected subset.
    
      WARNING: if fill_method == "fill_with_value_to_fill" but value_to_fill is None, the 
      missing values will be filled with the value 0.
    """

    from scipy import stats
    
    # Set a local copy of df to manipulate.
    # The methods used in this function can modify the original object itself. So,
    # here we apply the copy method setting deep = True
    cleaned_df = df.copy(deep = True)

    if (subset_columns_list is None):
        # all the columns are considered:
        total_columns = cleaned_df.shape[1]
    
    else:
        # Only the columns in the subset are considered.
        # Total columns is the length of the list of columns to subset:
        total_columns = len(subset_columns_list)
        
    # thresh argument of dropna method: int, optional - Require that many non-NA values.
    # This is the minimum of non-missing values that a row must have in order to be kept:
    THRESHOLD = min_number_of_non_missing_val_for_a_row_to_be_kept
    
    if ((drop_missing_val is None) & (fill_missing_val is None)):
        print("No valid input set for neither \'drop_missing_val\' nor \'fill_missing_val\'. Then, setting \'drop_missing_val\' = True and \'fill_missing_val\' = False.\n")
        drop_missing_val = True
        fill_missing_val = False
    
    elif (drop_missing_val is None):
        # The condition where both were missing was already tested. This one is tested only when the
        # the first if was not run.
        drop_missing_val = False
        fill_missing_val = True
    
    elif (fill_missing_val is None):
        drop_missing_val = True
        fill_missing_val = False
    
    elif ((drop_missing_val == True) & (fill_missing_val == True)):
        print("Both options \'drop_missing_val\' and \'fill_missing_val\' set as True. Then, selecting \'drop_missing_val\', which has preference.\n")
        fill_missing_val = False
    
    elif ((drop_missing_val == False) & (fill_missing_val == False)):
        print("Both options \'drop_missing_val\' and \'fill_missing_val\' set as False. Then, setting \'drop_missing_val\' = True.\n")
        drop_missing_val = True
    
    boolean_filter1 = (drop_missing_val == True)

    boolean_filter2 = (boolean_filter1) & (subset_columns_list is None)
    # These filters are True only if both conditions inside parentheses are True.
    # The operator & is equivalent to 'And' (intersection).
    # The operator | is equivalent to 'Or' (union).
    
    boolean_filter3 = (fill_missing_val == True) & (fill_method is None)
    # boolean_filter3 represents the situation where the fillna method was selected, but
    # no filling method was set.
    
    boolean_filter4 = (value_to_fill is None) & (fill_method == "fill_with_value_to_fill")
    # boolean_filter4 represents the situation where the fillna method will be used and the
    # user selected to fill the missing values with 'value_to_fill', but did not set a value
    # for 'value_to_fill'.
    
    if (boolean_filter1 == True):
        # drop missing values
        
        print("Dropping rows containing missing values, accordingly to the provided parameters.\n")
        
        if (boolean_filter2 == True):
            # no subset to filter
            
            if (eliminate_only_completely_empty_rows == True):
                #Eliminate only completely empty rows
                cleaned_df = cleaned_df.dropna(axis = 0, how = "all")
                # if axis = 1, dropna will eliminate each column containing missing values.
            
            elif (min_number_of_non_missing_val_for_a_row_to_be_kept is not None):
                # keep only rows containing at least the specified number of non-missing values:
                cleaned_df = cleaned_df.dropna(axis = 0, thresh = THRESHOLD)
            
            else:
                #Eliminate all rows containing missing values.
                #The only parameter is drop_missing_val
                cleaned_df = cleaned_df.dropna(axis = 0)
        
        else:
            #In this case, there is a subset for applying the Pandas dropna method.
            #Only the coluns in the subset 'subset_columns_list' will be analyzed.
                
            if (eliminate_only_completely_empty_rows == True):
                #Eliminate only completely empty rows
                cleaned_df = cleaned_df.dropna(subset = subset_columns_list, how = "all")
            
            elif (min_number_of_non_missing_val_for_a_row_to_be_kept is not None):
                # keep only rows containing at least the specified number of non-missing values:
                cleaned_df = cleaned_df.dropna(subset = subset_columns_list, thresh = THRESHOLD)
            
            else:
                #Eliminate all rows containing missing values.
                #The only parameter is drop_missing_val
                cleaned_df = cleaned_df.dropna(subset = subset_columns_list)
        
        print("Finished dropping of missing values.\n")
    
    else:
        
        print("Filling missing values.\n")
        
        # In this case, the user set a value for the parameter fill_missing_val to fill 
        # the missing data.
        
        # Check if a filling dictionary was passed as value_to_fill:
        if (type(value_to_fill) == dict):
            
            print(f"Applying the filling dictionary. Filling columns {value_to_fill.keys()} with the values {value_to_fill.values()}, respectively.\n")
            cleaned_df = cleaned_df.fillna(value = value_to_fill)
        
        elif (boolean_filter3 == True):
            # If this condition was reached, no filling dictionary was input.
            # fillna method was selected, but no filling method was set.
            # Then, filling with zero.
            print("No filling method defined, so filling missing values with 0.\n")
            cleaned_df = cleaned_df.fillna(0)
        
        elif (boolean_filter4 == True):
            # fill_method == "fill_with_value_to_fill" but value_to_fill is None.
            # Then, filling with zero.
            print("No value input for filling, so filling missing values with 0.\n")
            cleaned_df = cleaned_df.fillna(0)
        
        else:
            # A filling methodology was selected.
            if (fill_method == "fill_with_zeros"):
                print("Filling missing values with 0.\n")
                cleaned_df = cleaned_df.fillna(0)
            
            elif (fill_method == "fill_with_value_to_fill"):
                print(f"Filling missing values with {value_to_fill}.\n")
                cleaned_df = cleaned_df.fillna(value_to_fill)
            
            elif ((fill_method == "fill_with_avg_or_mode") | (fill_method == "fill_by_interpolating")):
                
                # We must separate the dataset into numerical columns and categorical columns
                # 1. Get dataframe's columns list:
                df_cols = cleaned_df.columns
                
                # 2. start a list for the numeric and a list for the text (categorical) columns:
                numeric_list = []
                categorical_list = []
                # List the possible numeric data types for a Pandas dataframe column:
                numeric_dtypes = [np.int16, np.int32, np.int64, np.float16, np.float32, np.float64]
                
                # 3. Loop through each column on df_cols, to put it in the correspondent type of column:
                for column in df_cols:
                    
                    # Check if the column is neither in numeric_list nor in
                    # categorical_list yet:
                    if ((column not in numeric_list) & (column not in categorical_list)):
                        
                        column_data_type = cleaned_df[column].dtype

                        if (column_data_type not in numeric_dtypes):

                            # Append to categorical columns list:
                            categorical_list.append(column)

                        else:
                            # Append to numerical columns list:
                            numeric_list.append(column)
                
                
                # Create variables to map if both are present.
                is_categorical = 0
                is_numeric = 0

                # Create two subsets:
                if (len(categorical_list) > 0):

                    # Has at least one column:
                    df_categorical = cleaned_df.copy(deep = True)
                    df_categorical = df_categorical[categorical_list]
                    is_categorical = 1
                    # scipy.stats.mode requires numeric values, so the ordinal encoding is necessary.
                    DATASET = df_categorical
                    SUBSET_OF_FEATURES_TO_BE_ENCODED = categorical_list
                    df_categorical, ordinal_encoding_list = OrdinalEncoding_df (df = DATASET, subset_of_features_to_be_encoded = SUBSET_OF_FEATURES_TO_BE_ENCODED)
                    # Get the new columns generated from Ordinal Encoding:
                    new_encoded_cols = [column + "_OrdinalEnc" for column in categorical_list]
                    # Remove the columns that do not have numeric variables before grouping
                    df_categorical = df_categorical.drop(columns = categorical_list)

                if (len(numeric_list) > 0):

                    df_numeric = cleaned_df.copy(deep = True)
                    df_numeric = df_numeric[numeric_list]
                    is_numeric = 1
                
                # Notice that the variables is_numeric and is_categorical have value 1 only when the subsets
                # are present.
                is_cat_num = is_categorical + is_numeric
                # is_cat_num = 0 if no valid dataset was input.
                # is_cat_num = 2 if both subsets are present.
        
                # Now, we have two subsets , one for the categoricals, other
                # for the numeric. It will avoid trying to fill categorical columns with the
                # mean values.
                
                if (fill_method == "fill_with_avg_or_mode"):
                    
                    # Start a filling dictionary:
                    fill_dict = {}
                    
                    print("Filling missing values with the average values (numeric variables); or with the modes (categorical variables). The mode is the most commonly observed value of the categorical variable.\n")
                    
                    if (is_numeric == 1):
                        
                        for column in numeric_list:
                            
                            # add column as the key, and the mean as the value:
                            fill_dict[column] = df_numeric[column].mean()
                    
                    if (is_categorical == 1):
                        
                        for column in new_encoded_cols:
                            
                            # The function stats.mode(X) returns an array as: 
                            # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mode.html
                            # ModeResult(mode=3, count=5) ac, axis = None, cess mode attribute       
                            # which will return a string like 'a':
                            try:
                                fill_dict[column] = stats.mode(np.array(df_categorical[column]), axis = None, keepdims = False).mode
                        
                            except:
                                try:
                                    fill_dict[column] = stats.mode(np.array(df_categorical[column]), axis = None, keepdims = False)[0]
                                except:
                                    try:
                                        if ((stats.mode(np.array(df_categorical[column]), axis = None, keepdims = False) != np.nan) & (stats.mode(np.array(df_categorical[column]), axis = None, keepdims = False) is not None)):
                                            fill_dict[column] = stats.mode(np.array(df_categorical[column]), axis = None, keepdims = False)
                                        else:
                                            fill_dict[column] = np.nan
                                    except:
                                        fill_dict[column] = np.nan
                    
                    # Now, fill_dict contains the mapping of columns (keys) and 
                    # correspondent values for imputation with the method fillna.
                    # It is equivalent to use:
                    # from sklearn.impute import SimpleImputer
                    # mean_imputer = SimpleImputer(strategy='mean')
                    # mode_imputer = SimpleImputer(strategy='most_frequent')
                    # as in the advanced imputation function.
                        
                    # In fillna documentation, we see that the argument 'value' must have a dictionary
                    # with this particular format as input:
                    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.fillna.html#pandas.DataFrame.fillna

                    # This dictionary correlates each column to its average value.

                    #6. Finally, use this dictionary to fill the missing values of each column
                    # with the average value of that column
                    cleaned_df = cleaned_df.fillna(value = fill_dict)
                    # The method will search the column name in fill_dict (key of the dictionary),
                    # and will use the correspondent value (average) to fill the missing values.
                

                elif (fill_method == "fill_by_interpolating"):
                    # Pandas interpolate method
                    
                    # Separate the dataframes into a dataframe for filling with interpolation (numeric
                    # variables); and a dataframe for forward filling (categorical variables).
                    
                    # Before subsetting, check if the list is not empty.
                    
                    if (is_numeric == 1):
                    
                        if (type(interpolation_order) == int):
                            # an integer number was input

                            if (interpolation_order > 1):

                                print(f"Performing interpolation of numeric variables with {interpolation_order}-degree polynomial to fill missing values.\n")
                                df_numeric = df_numeric.interpolate(method = 'polynomial', order = interpolation_order)

                            else:
                                # 1st order or invalid order (0 or negative) was used
                                print("Performing linear interpolation of numeric variables to fill missing values.\n")
                                df_numeric = df_numeric.interpolate(method = 'linear')

                        else:
                            # 'linear', None or invalid text was input:
                            print("Performing linear interpolation of numeric variables to fill missing values.\n")
                            df_numeric = df_numeric.interpolate(method = 'linear')
                    
                    # Now, we finished the interpolation of the numeric variables. Let's check if
                    # there are categorical variables to forward fill.
                    if (is_categorical == 1):
                        
                        # Now, fill missing values by forward filling:
                        print("Using forward filling to fill missing values of the categorical variables.\n")
                        df_categorical = df_categorical.fillna(method = "ffill")
                    
                    # Now, let's check if there are both a numeric_subset and a text_subset to merge
                    
                    if (is_cat_num == 2):
                        # Both subsets are present.
                        # Reverse ordinal encoding
                        DATASET = df_categorical
                        ENCODING_LIST = ordinal_encoding_list
                        # Now, reverse encoding and keep only the original column names:
                        df_categorical = reverse_OrdinalEncoding (df = DATASET, encoding_list = ENCODING_LIST)
                        df_categorical = df_categorical[categorical_list]
                        # Concatenate the dataframes in the columns axis (append columns):
                        cleaned_df = pd.concat([df_numeric, df_categorical], axis = 1, join = "inner")

                    elif (is_categorical == 1):
                        # There is only the categorical subset:
                        # Reverse ordinal encoding
                        DATASET = df_categorical
                        ENCODING_LIST = ordinal_encoding_list
                        # Now, reverse encoding and keep only the original column names:
                        df_categorical = reverse_OrdinalEncoding (df = DATASET, encoding_list = ENCODING_LIST)
                        df_categorical = df_categorical[categorical_list]
                        cleaned_df = df_categorical

                    elif (is_numeric == 1):
                        # There is only the numeric subset:
                        cleaned_df = df_numeric
                    
                    else:
                        print("No valid dataset provided, so returning the input dataset itself.\n")
            
            elif ((fill_method == "ffill") | (fill_method == "bfill")):
                # use forward or backfill
                cleaned_df = cleaned_df.fillna(method = fill_method)
            
            elif (fill_method == "nearest"):
                # nearest: applies the 'bfill' or 'ffill', depending if the point
                # is closes to the previous or to the next non-missing value.
                # It is a Pandas dataframe interpolation method, not a fillna one.
                cleaned_df = cleaned_df.interpolate(method = 'nearest')
            
            else:
                print("No valid filling methodology was selected. Then, filling missing values with 0.\n")
                cleaned_df = cleaned_df.fillna(0)
        
        
    #Reset index before returning the cleaned dataframe:
    cleaned_df = cleaned_df.reset_index(drop = True)
    
    
    print(f"Number of rows of the dataframe before cleaning = {df.shape[0]} rows.")
    print(f"Number of rows of the dataframe after cleaning = {cleaned_df.shape[0]} rows.")
    print(f"Percentual variation of the number of rows = {(df.shape[0] - cleaned_df.shape[0])/(df.shape[0]) * 100} %\n")
    print("Check the 10 first rows of the cleaned dataframe:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(cleaned_df.head(10))
            
    except: # regular mode
        print(cleaned_df.head(10))
    
    return cleaned_df


def adv_imputation_missing_values (df, column_to_fill, timestamp_tag_column = None, test_value_to_fill = None, show_imputation_comparison_plots = True):
    """
    adv_imputation_missing_values (df, column_to_fill, timestamp_tag_column = None, test_value_to_fill = None, show_imputation_comparison_plots = True):
    
    Check DataCamp course Dealing with Missing Data in Python
     https://app.datacamp.com/learn/courses/dealing-with-missing-data-in-python
    
    This function handles only one column by call, whereas handle_missing_values can process the whole
     dataframe at once.
    The strategies used for handling missing values is different here. You can use the function to
     process data that does not come from time series, but only plot the graphs for time series data.
    
    This function is more indicated for dealing with missing values on time series data than handle_missing_values.
    This function will search for the best imputer for a given column.
    It can process both numerical and categorical columns.
    
    : param: column_to_fill: string (in quotes) indicating the column with missing values to fill.
      e.g. if column_to_fill = 'col1', imputations will be performed on column 'col1'.
    
    : param: timestamp_tag_column = None. string containing the name of the column with the timestamp. 
      If timestamp_tag_column is None, the index will be used for testing different imputations.
      be the time series reference. declare as a string under quotes. This is the column from 
      which we will extract the timestamps or values with temporal information. e.g.
      timestamp_tag_column = 'timestamp' will consider the column 'timestamp' a time column.
    
    : param: test_value_to_fill: the function will test the imputation of a constant. Specify this constant here
      or the tested constant will be zero. e.g. test_value_to_fill = None will test the imputation of 0.
      test_value_to_fill = 10 will test the imputation of value zero.
    
    : param: show_imputation_comparison_plots = True. Keep it True to plot the scatter plot comparison
      between imputed and original values, as well as the Kernel density estimate (KDE) plot.
      Alternatively, set show_imputation_comparison_plots = False to omit the plots.
    
      The following imputation techniques will be tested, and the best one will be automatically
      selected: mean_imputer, median_imputer, mode_imputer, constant_imputer, linear_interpolation,
      quadratic_interpolation, cubic_interpolation, nearest_interpolation, bfill_imputation,
      ffill_imputation, knn_imputer, mice_imputer (MICE = Multiple Imputations by Chained Equations).
    
      MICE: Performs multiple regressions over random samples of the data; 
      Takes the average of multiple regression values; and imputes the missing feature value for the 
      data point.
      KNN (K-Nearest Neighbor): Selects K nearest or similar data points using all the 
      non-missing features. It takes the average of the selected data points to fill in the missing 
      feature.
      These are Machine Learning techniques to impute missing values.
      KNN finds most similar points for imputing.
      MICE performs multiple regression for imputing. MICE is a very robust model for imputation.
    """
    
    from scipy.stats import linregress
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import OrdinalEncoder
    from fancyimpute import KNN, IterativeImputer
    
    # Set a local copy of df to manipulate.
    # The methods used in this function can modify the original object itself. So,
    # here we apply the copy method setting deep = True
    cleaned_df = df.copy(deep = True)
    
    subset_columns_list = [column_to_fill] # only the column indicated.
    total_columns = 1 # keep the homogeneity with the previous function
    
    # Get the list of columns of the dataframe:
    df_cols = list(cleaned_df.columns)
    # Get the index j of the column_to_fill:
    j = df_cols.index(column_to_fill)
    print(f"Filling missing values on column {column_to_fill}. This is the column with index {j} in the original dataframe.\n")

    # Firstly, let's process the timestamp column and save it as x. 
    # That is because datetime objects cannot be directly applied to linear regressions and
    # numeric procedure. We must firstly convert it to an integer scale capable of preserving
    # the distance relationships.

    # Check if there is a timestamp_tag_column. If not, make the index the timestamp:
    if (timestamp_tag_column is None):
        
        timestamp_tag_column = column_to_fill + "_index"
        
        # Create the x array
        x = np.array(cleaned_df.index)
        
    else:
        # Run only if there was a timestamp column originally.
        # sort this dataframe by timestamp_tag_column and column_to_fill:
        cleaned_df = cleaned_df.sort_values(by = [timestamp_tag_column, column_to_fill], ascending = [True, True])
        # restart index:
        cleaned_df = cleaned_df.reset_index(drop = True)
        
        # If timestamp_tag_column is an object, the user may be trying to pass a date as x. 
        # So, let's try to convert it to datetime:
        if ((cleaned_df[timestamp_tag_column].dtype == 'O') | (cleaned_df[timestamp_tag_column].dtype == 'object')):

            try:
                cleaned_df[timestamp_tag_column] = (cleaned_df[timestamp_tag_column]).astype('datetime64[ns]')
                        
            except:
                # Simply ignore it
                pass
        
        ts_array = np.array(cleaned_df[timestamp_tag_column])
        
        # Check if the elements from array x are np.datetime64 objects. Pick the first
        # element to check:
        if (type(ts_array[0]) == np.datetime64):
            # In this case, performing the linear regression directly in X will
            # return an error. We must associate a sequential number to each time.
            # to keep the distance between these integers the same as in the original sequence
            # let's define a difference of 1 ns as 1. The 1st timestamp will be zero, and the
            # addition of 1 ns will be an addition of 1 unit. So a timestamp recorded 10 ns
            # after the time zero will have value 10. At the end, we divide every element by
            # 10**9, to obtain the correspondent distance in seconds.
                
            # start a list for the associated integer timescale. Put the number zero,
            # associated to the first timestamp:
            int_timescale = [0]
                
            # loop through each element of the array x, starting from index 1:
            for i in range(1, len(ts_array)):
                    
                # calculate the timedelta between x[i] and x[i-1]:
                # The delta method from the Timedelta class converts the timedelta to
                # nanoseconds, guaranteeing the internal compatibility:
                # The .delta attribute was replaced by .value attribute. 
                # Both return the number of nanoseconds as an integer.
                # https://pandas.pydata.org/docs/reference/api/pandas.Timedelta.html
                timedelta = pd.Timedelta(ts_array[i] - ts_array[(i-1)]).value
                    
                # Sum this timedelta (integer number of nanoseconds) to the
                # previous element from int_timescale, and append the result to the list:
                int_timescale.append((timedelta + int_timescale[(i-1)]))
                
            # Now convert the new scale (that preserves the distance between timestamps)
            # to NumPy array:
            int_timescale = np.array(int_timescale)
            
            # Divide by 10**9 to obtain the distances in seconds, reducing the order of
            # magnitude of the integer numbers (the division is allowed for arrays).
            # make it the timestamp array ts_array itself:
            ts_array = int_timescale / (10**9)
            # Now, reduce again the order of magnitude through division by (60*60)
            # It will obtain the ts_array in hour:
            ts_array = int_timescale / (60*60)
            
        # make x the ts_array itself:
        x = ts_array
    
    column_data_type = cleaned_df[column_to_fill].dtype
    
    # Pre-process the column if it is categorical
    if ((column_data_type == 'O') | (column_data_type == 'object')):
        
        # Ordinal encoding: let's associate integer sequential numbers to the categorical column
        # to apply the advanced encoding techniques. Even though the one-hot encoding could perform
        # the same task and would, in fact, better, since there may be no ordering relation, the
        # ordinal encoding is simpler and more suitable for this particular task:
        
        # Create Ordinal encoder
        ord_enc = OrdinalEncoder()
        
        # Select non-null values of the column in the dataframe:
        series_on_df = cleaned_df[column_to_fill]
        
        # Reshape series_on_df to shape (-1, 1)
        reshaped_vals = series_on_df.values.reshape(-1, 1)
        
        # Fit the ordinal encoder to the reshaped column_to_fill values:
        encoded_vals = ord_enc.fit_transform(reshaped_vals)
        
        # Finally, store the values to non-null values of the column in dataframe
        cleaned_df.iloc[:,j] = encoded_vals

        # Max and minimum of the encoded range
        max_encoded = max(encoded_vals)
        min_encoded = min(encoded_vals)


    # Start a list of imputations:
    list_of_imputations = []
    
    subset_from_cleaned_df = cleaned_df.copy(deep = True)
    subset_from_cleaned_df = subset_from_cleaned_df[subset_columns_list]

    mean_imputer = SimpleImputer(strategy = 'mean')
    list_of_imputations.append('mean_imputer')
    
    # Now, apply the fit_transform method from the imputer to fit it to the indicated column:
    mean_imputer.fit(subset_from_cleaned_df)
    # If you wanted to obtain constants for all columns, you should not specify a subset:
    # imputer.fit_transform(cleaned_df)
        
    # create a column on the dataframe as 'mean_imputer':
    cleaned_df['mean_imputer'] = mean_imputer.transform(subset_from_cleaned_df)
        
    # Create the median imputer:
    median_imputer = SimpleImputer(strategy = 'median')
    list_of_imputations.append('median_imputer')
    median_imputer.fit(subset_from_cleaned_df)
    cleaned_df['median_imputer'] = median_imputer.transform(subset_from_cleaned_df)
    
    # Create the mode imputer:
    mode_imputer = SimpleImputer(strategy = 'most_frequent')
    list_of_imputations.append('mode_imputer')
    mode_imputer.fit(subset_from_cleaned_df)
    cleaned_df['mode_imputer'] = mode_imputer.transform(subset_from_cleaned_df)
    
    # Create the constant value imputer:
    if (test_value_to_fill is None):
        test_value_to_fill = 0
    
    constant_imputer = SimpleImputer(strategy = 'constant', fill_value = test_value_to_fill)
    list_of_imputations.append('constant_imputer')
    constant_imputer.fit(subset_from_cleaned_df)
    cleaned_df['constant_imputer'] = constant_imputer.transform(subset_from_cleaned_df)
    
    # Make the linear interpolation imputation:
    linear_interpolation_df = cleaned_df[subset_columns_list].copy(deep = True)
    linear_interpolation_df = linear_interpolation_df.interpolate(method = 'linear')
    cleaned_df['linear_interpolation'] = linear_interpolation_df[column_to_fill]
    list_of_imputations.append('linear_interpolation')
        
    # Interpolate 2-nd degree polynomial:
    quadratic_interpolation_df = cleaned_df[subset_columns_list].copy(deep = True)
    quadratic_interpolation_df = quadratic_interpolation_df.interpolate(method = 'polynomial', order = 2)
    cleaned_df['quadratic_interpolation'] = quadratic_interpolation_df[column_to_fill]
    list_of_imputations.append('quadratic_interpolation')
        
    # Interpolate 3-rd degree polynomial:
    cubic_interpolation_df = cleaned_df[subset_columns_list].copy(deep = True)
    cubic_interpolation_df = cubic_interpolation_df.interpolate(method = 'polynomial', order = 3)
    cleaned_df['cubic_interpolation'] = cubic_interpolation_df[column_to_fill]
    list_of_imputations.append('cubic_interpolation')
    
    # Nearest interpolation
    # Similar to bfill and ffill, but uses the nearest
    nearest_interpolation_df = cleaned_df[subset_columns_list].copy(deep = True)
    nearest_interpolation_df = nearest_interpolation_df.interpolate(method = 'nearest')
    cleaned_df['nearest_interpolation'] = nearest_interpolation_df[column_to_fill]
    list_of_imputations.append('nearest_interpolation')
    
    # bfill and ffill:
    bfill_df = cleaned_df[subset_columns_list].copy(deep = True)
    ffill_df = cleaned_df[subset_columns_list].copy(deep = True)
    
    bfill_df = bfill_df.fillna(method = 'bfill')
    cleaned_df['bfill_imputation'] = bfill_df[column_to_fill]
    list_of_imputations.append('bfill_imputation')
    
    ffill_df = ffill_df.fillna(method = 'ffill')
    cleaned_df['ffill_imputation'] = ffill_df[column_to_fill]
    list_of_imputations.append('ffill_imputation')
    
    
    # Now, we can go to the advanced machine learning techniques:
    
    # KNN Imputer:
    # Initialize KNN
    knn_imputer = KNN()
    list_of_imputations.append('knn_imputer')
    cleaned_df['knn_imputer'] = knn_imputer.fit_transform(subset_from_cleaned_df)
    
    # Initialize IterativeImputer
    mice_imputer = IterativeImputer()
    list_of_imputations.append('mice_imputer')
    cleaned_df['mice_imputer'] = mice_imputer.fit_transform(subset_from_cleaned_df)
    
    # Now, let's create linear regressions for compare the performance of different
    # imputation strategies.
    # Firstly, start a dictionary to store
    
    imputation_performance_dict = {}

    # Now, loop through each imputation and calculate the adjusted R²:
    for imputation in list_of_imputations:
        
        y = cleaned_df[imputation]
        
        # fit the linear regression
        slope, intercept, r, p, se = linregress(x, y)
        
        # Get the adjusted R² and add it as the key imputation of the dictionary:
        imputation_performance_dict[imputation] = r**2
    
    # Select best R-squared
    best_imputation = max(imputation_performance_dict, key = imputation_performance_dict.get)
    print(f"The best imputation strategy for the column {column_to_fill} is {best_imputation}.\n")
    
    
    if (show_imputation_comparison_plots & ((column_data_type != 'O') & (column_data_type != 'object'))):
        
        # Firstly, converts the values obtained to closest integer (since we
        # encoded the categorical values as integers, we cannot reconvert
        # decimals):)): # run if it is True
    
        print("Check the Kernel density estimate (KDE) plot for the different imputations.\n")
        labels_list = ['baseline\ncomplete_case']
        y = cleaned_df[column_to_fill]
        X = cleaned_df[timestamp_tag_column] # not the converted scale

        fig = plt.figure(figsize = (12, 8))
        ax = fig.add_subplot()
        
        # Plot graphs of imputed DataFrames and the complete case
        y.plot(kind = 'kde', c = 'red', linewidth = 3)

        for imputation in list_of_imputations:
            
            labels_list.append(imputation)
            y = cleaned_df[imputation]
            y.plot(kind = 'kde')
        
        #ROTATE X AXIS IN XX DEGREES
        plt.xticks(rotation = 0)
        # XX = 0 DEGREES x_axis (Default)
        #ROTATE Y AXIS IN XX DEGREES:
        plt.yticks(rotation = 0)
        # XX = 0 DEGREES y_axis (Default)

        ax.set_title("Kernel_density_estimate_plot_for_each_imputation")
        ax.set_xlabel(column_to_fill)
        ax.set_ylabel("density")

        ax.grid(True) # show grid or not
        ax.legend(loc = 'upper left')
        # position options: 'upper right'; 'upper left'; 'lower left'; 'lower right';
        # 'right', 'center left'; 'center right'; 'lower center'; 'upper center', 'center'
        # https://www.statology.org/matplotlib-legend-position/
        plt.show()
        
        print("\n")
        print(f"Now, check the original time series compared with the values obtained through {best_imputation}:\n")
        
        fig = plt.figure(figsize = (12, 8))
        ax = fig.add_subplot()
        
        # Plot the imputed DataFrame in red dotted style
        selected_imputation = cleaned_df[best_imputation]
        ax.plot(X, selected_imputation, color = 'red', marker = 'o', linestyle = 'dotted', label = best_imputation)
        
        # Plot the original DataFrame with title
        # Put a degree of transparency (35%) to highlight the imputation.
        ax.plot(X, y, color = 'darkblue', alpha = 0.65, linestyle = '-', marker = '', label = (column_to_fill + "_original"))
        
        plt.xticks(rotation = 70)
        plt.yticks(rotation = 0)
        ax.set_title(column_to_fill + "_original_vs_imputations")
        ax.set_xlabel(timestamp_tag_column)
        ax.set_ylabel(column_to_fill)

        ax.grid(True) # show grid or not
        ax.legend(loc = 'upper left')
        # position options: 'upper right'; 'upper left'; 'lower left'; 'lower right';
        # 'right', 'center left'; 'center right'; 'lower center'; 'upper center', 'center'
        # https://www.statology.org/matplotlib-legend-position/
        plt.show()
        print("\n")
    
                
    print(f"Returning a dataframe where {best_imputation} strategy was used for filling missing values in {column_to_fill} column.\n")
    
    if (best_imputation == 'mice_imputer'):
        print("MICE = Multiple Imputations by Chained Equations")
        print("MICE: Performs multiple regressions over random samples of the data.")
        print("It takes the average of multiple regression values and imputes the missing feature value for the data point.")
        print("It is a Machine Learning technique to impute missing values.")
        print("MICE performs multiple regression for imputing and is a very robust model for imputation.\n")
    
    elif (best_imputation == 'knn_imputer'):
        print("KNN = K-Nearest Neighbor")
        print("KNN selects K nearest or similar data points using all the non-missing features.")
        print("It takes the average of the selected data points to fill in the missing feature.")
        print("It is a Machine Learning technique to impute missing values.")
        print("KNN finds most similar points for imputing.\n")
    
    # Make all rows from the column j equals to the selected imputer:
    cleaned_df.iloc[:, j] = cleaned_df[best_imputation]
    # If you wanted to make all rows from all columns equal to the imputer, you should declare:
    # cleaned_df.iloc[:, :] = imputer
    
    # Drop all the columns created for storing different imputers:
    # These columns were saved in the list list_of_imputations.
    # Notice that the selected imputations were saved in the original column.
    cleaned_df = cleaned_df.drop(columns = list_of_imputations)
    
    # Finally, let's reverse the ordinal encoding used in the beginning of the code to process object
    # columns:
    
    # List the possible numeric data types for a Pandas dataframe column:
    numeric_dtypes = [np.int16, np.int32, np.int64, np.float16, np.float32, np.float64]
    
    if (column_data_type not in numeric_dtypes):
        
        # Firstly, converts the values obtained to closest integer (since we
        # encoded the categorical values as integers, we cannot reconvert
        # decimals):
        
        cleaned_df[column_to_fill] = (np.rint(cleaned_df[column_to_fill]))
        
        # If a value is above the max_encoded, make it equals to the maximum.
        # If it is below the minimum, make it equals to the minimum:
        for k in range(0, len(cleaned_df)):

            if (cleaned_df.iloc[k,j] > max_encoded):
                cleaned_df.iloc[k,j] = max_encoded
                
            elif (cleaned_df.iloc[k,j] < min_encoded):
                cleaned_df.iloc[k,j] = min_encoded

        new_series = cleaned_df[column_to_fill]
        # We must use the int function to guarantee that the column_to_fill will store an
        # integer number (we cannot have a fraction of an encoding).
        # The int function guarantees that the variable will be stored as an integer.
        # The numpy.rint(a) function rounds elements of the array to the nearest integer.
        # https://numpy.org/doc/stable/reference/generated/numpy.rint.html
        # For values exactly halfway between rounded decimal values, 
        # NumPy rounds to the nearest even value. 
        # Thus 1.5 and 2.5 round to 2.0; -0.5 and 0.5 round to 0.0; etc.
        
        # Reshape series_not_null to shape (-1, 1)
        reshaped_vals = new_series.values.reshape(-1, 1)
        
        # Perform inverse transform of the ordinally encoded columns
        cleaned_df[column_to_fill] = ord_enc.inverse_transform(reshaped_vals)


    print("Check the 10 first rows from the cleaned dataframe:\n")
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(cleaned_df.head(10))
            
    except: # regular mode
        print(cleaned_df.head(10))
    
    return cleaned_df


def correlation_plot (df, show_masked_plot = True, responses_to_return_corr = None, set_returned_limit = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    correlation_plot (df, show_masked_plot = True, responses_to_return_corr = None, set_returned_limit = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    : param: show_masked_plot = True - keep as True if you want to see a cleaned version of the plot
      where a mask is applied.
    
    : param:responses_to_return_corr - keep as None to return the full correlation tensor.
      If you want to display the correlations for a particular group of features, input them
      as a list, even if this list contains a single element. Examples:
      responses_to_return_corr = ['response1'] for a single response
      responses_to_return_corr = ['response1', 'response2', 'response3'] for multiple
      responses. Notice that 'response1',... should be substituted by the name ('string')
      of a column of the dataset that represents a response variable.
      WARNING: The returned coefficients will be ordered according to the order of the list
      of responses. i.e., they will be firstly ordered based on 'response1'
    
    : param: set_returned_limit = None - This variable will only present effects in case you have
      provided a response feature to be returned. In this case, keep set_returned_limit = None
      to return all of the correlation coefficients; or, alternatively, 
      provide an integer number to limit the total of coefficients returned. 
      e.g. if set_returned_limit = 10, only the ten highest coefficients will be returned. 
    """

    # set a local copy of the dataset to perform the calculations:
    DATASET = df.copy(deep = True)

    # Let's remove the categorical columns
    print("ATTENTION! The analysis will be performed only for the numeric variables.")
    print("Categorical columns will be automatically ignored.\n")

    # List the possible numeric data types for a Pandas dataframe column:
    numeric_dtypes = [np.int16, np.int32, np.int64, np.float16, np.float32, np.float64]
    numeric_cols = []
    # Loop through all valid columns (cols_list)
    for column in DATASET.columns:
        
        # Check if the column is neither in timestamp_list nor in
        # categorical_list yet:
        column_data_type = DATASET[column].dtype
            
        if (column_data_type in numeric_dtypes):
            # Append to categorical columns list:
            numeric_cols.append(column)
    
    # Filter the dataset to include only numeric variables:
    DATASET = DATASET[numeric_cols]
    
    # Now, obtain the matrix
    correlation_matrix = DATASET.corr(method = 'pearson')
    
    if (show_masked_plot == False):
        #Show standard plot
        
        plt.figure(figsize = (12, 8))
        sns.heatmap((correlation_matrix)**2, annot = True, fmt = ".2f")
        
        if (export_png == True):
            # Image will be exported
            import os

            #check if the user defined a directory path. If not, set as the default root path:
            if (directory_to_save is None):
                #set as the default
                directory_to_save = ""

            #check if the user defined a file name. If not, set as the default name for this
            # function.
            if (file_name is None):
                #set as the default
                file_name = "correlation_plot"

            #check if the user defined an image resolution. If not, set as the default 110 dpi
            # resolution.
            if (png_resolution_dpi is None):
                #set as 330 dpi
                png_resolution_dpi = 330

            #Get the new_file_path
            new_file_path = os.path.join(directory_to_save, file_name)

            #Export the file to this new path:
            # The extension will be automatically added by the savefig method:
            plt.savefig(new_file_path, dpi = png_resolution_dpi, quality = 100, format = 'png', transparent = False) 
            #quality could be set from 1 to 100, where 100 is the best quality
            #format (str, supported formats) = 'png', 'pdf', 'ps', 'eps' or 'svg'
            #transparent = True or False
            # For other parameters of .savefig method, check https://indianaiproduction.com/matplotlib-savefig/
            print (f"Figure exported as \'{new_file_path}.png\'. Any previous file in this root path was overwritten.")

        plt.show()

    #Once the pandas method .corr() calculates R, we raised it to the second power 
    # to obtain R². R² goes from zero to 1, where 1 represents the perfect correlation.
    
    else:
        
        # Show masked (cleaner) plot instead of the standard one
        # Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
        plt.figure(figsize = (12, 8))
        # Mask for the upper triangle
        mask = np.zeros_like((correlation_matrix)**2)

        mask[np.triu_indices_from(mask)] = True

        # Generate a custom diverging colormap
        cmap = sns.diverging_palette(220, 10, as_cmap = True)

        # Heatmap with mask and correct aspect ratio
        sns.heatmap(((correlation_matrix)**2), mask = mask, cmap = cmap, center = 0,
                    linewidths = .5)
        
        if (export_png == True):
            # Image will be exported
            import os

            #check if the user defined a directory path. If not, set as the default root path:
            if (directory_to_save is None):
                #set as the default
                directory_to_save = ""

            #check if the user defined a file name. If not, set as the default name for this
            # function.
            if (file_name is None):
                #set as the default
                file_name = "correlation_plot"

            #check if the user defined an image resolution. If not, set as the default 110 dpi
            # resolution.
            if (png_resolution_dpi is None):
                #set as 330 dpi
                png_resolution_dpi = 330

            #Get the new_file_path
            new_file_path = os.path.join(directory_to_save, file_name)

            #Export the file to this new path:
            # The extension will be automatically added by the savefig method:
            plt.savefig(new_file_path, dpi = png_resolution_dpi, quality = 100, format = 'png', transparent = False) 
            #quality could be set from 1 to 100, where 100 is the best quality
            #format (str, supported formats) = 'png', 'pdf', 'ps', 'eps' or 'svg'
            #transparent = True or False
            # For other parameters of .savefig method, check https://indianaiproduction.com/matplotlib-savefig/
            print (f"Figure exported as \'{new_file_path}.png\'. Any previous file in this root path was overwritten.")

        plt.show()

        #Again, the method dataset.corr() calculates R within the variables of dataset.
        #To calculate R², we simply raise it to the second power: (dataset.corr()**2)
    
    #Sort the values of correlation_matrix in Descending order:
    
    if (responses_to_return_corr is not None):
        
        if (type(responses_to_return_corr) == str):
            # If a string was input, put it inside a list
            responses_to_return_corr = [responses_to_return_corr]

    else:
        # Use all columns
        responses_to_return_corr = list(DATASET.columns)

    #Select only the desired responses, by passing the list responses_to_return_corr
    # as parameter for column filtering:
    correlation_matrix = correlation_matrix[responses_to_return_corr]
    # By passing a list as argument, we assure that the output is a dataframe
    # and not a series, even if the list contains a single element.
    
    # Create a list of boolean variables == False, one False correspondent to
    # each one of the responses
    ascending_modes = [False for i in range(0, len(responses_to_return_corr))]
    
    #Now sort the values according to the responses, by passing the list
    # response
    correlation_matrix = correlation_matrix.sort_values(by = responses_to_return_corr, ascending = ascending_modes)
    
    # If a limit of coefficients was determined, apply it:
    if (set_returned_limit is not None):
            
            correlation_matrix = correlation_matrix.head(set_returned_limit)
            #Pandas .head(X) method returns the first X rows of the dataframe.
            # Here, it returns the defined limit of coefficients, set_returned_limit.
            # The default .head() is X = 5.
    
    print("ATTENTION: The correlation plots show the linear correlations R², which go from 0 (none correlation) to 1 (perfect correlation). Obviously, the main diagonal always shows R² = 1, since the data is perfectly correlated to itself.\n")
    print("The returned correlation matrix, on the other hand, presents the linear coefficients of correlation R, not R². R values go from -1 (perfect negative correlation) to 1 (perfect positive correlation).\n")
    print("None of these coefficients take non-linear relations and the presence of a multiple linear correlation in account. For these cases, it is necessary to calculate R² adjusted, which takes in account the presence of multiple preditors and non-linearities.\n")
    
    print("Correlation matrix - numeric results:\n")
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(correlation_matrix)
            
    except: # regular mode
        print(correlation_matrix)
    
    return correlation_matrix


def covariance_matrix_plot (df, show_masked_plot = True, responses_to_return_cov = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    covariance_matrix_plot (df, show_masked_plot = True, responses_to_return_cov = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    : param: show_masked_plot = True - keep as True if you want to see a cleaned version of the plot
     where a mask is applied.
    
    : param: responses_to_return_cov - keep as None to return the full covariance tensor.
      If you want to display the covariance for a particular group of features, input them
      as a list, even if this list contains a single element. Examples:
      responses_to_return_cov = ['response1'] for a single response
      responses_to_return_cov = ['response1', 'response2', 'response3'] for multiple
      responses. Notice that 'response1',... should be substituted by the name ('string')
      of a column of the dataset that represents a response variable.
      WARNING: The returned coefficients will be ordered according to the order of the list
      of responses. i.e., they will be firstly ordered based on 'response1'
    """
    
    # set a local copy of the dataset to perform the calculations:
    DATASET = df.copy(deep = True)
    
    # Let's remove the categorical columns
    print("ATTENTION! The analysis will be performed only for the numeric variables.")
    print("Categorical columns will be automatically ignored.\n")

    # List the possible numeric data types for a Pandas dataframe column:
    numeric_dtypes = [np.int16, np.int32, np.int64, np.float16, np.float32, np.float64]
    numeric_cols = []
    # Loop through all valid columns (cols_list)
    for column in DATASET.columns:
        
        # Check if the column is neither in timestamp_list nor in
        # categorical_list yet:
        column_data_type = DATASET[column].dtype
            
        if (column_data_type in numeric_dtypes):
            # Append to categorical columns list:
            numeric_cols.append(column)
    
    # Filter the dataset to include only numeric variables:
    DATASET = DATASET[numeric_cols]
    
    # Now, obtain the matrix
    covariance_matrix = DATASET.cov(min_periods = None, ddof = 1, numeric_only = False)
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.cov.html
    
    if (show_masked_plot == False):
        #Show standard plot
        
        plt.figure(figsize = (12, 8))
        sns.heatmap(covariance_matrix, annot = True, fmt = ".2f")
        
        if (export_png == True):
            # Image will be exported
            import os

            #check if the user defined a directory path. If not, set as the default root path:
            if (directory_to_save is None):
                #set as the default
                directory_to_save = ""

            #check if the user defined a file name. If not, set as the default name for this
            # function.
            if (file_name is None):
                #set as the default
                file_name = "covariance_matrix"

            #check if the user defined an image resolution. If not, set as the default 110 dpi
            # resolution.
            if (png_resolution_dpi is None):
                #set as 330 dpi
                png_resolution_dpi = 330

            #Get the new_file_path
            new_file_path = os.path.join(directory_to_save, file_name)

            #Export the file to this new path:
            # The extension will be automatically added by the savefig method:
            plt.savefig(new_file_path, dpi = png_resolution_dpi, quality = 100, format = 'png', transparent = False) 
            #quality could be set from 1 to 100, where 100 is the best quality
            #format (str, supported formats) = 'png', 'pdf', 'ps', 'eps' or 'svg'
            #transparent = True or False
            # For other parameters of .savefig method, check https://indianaiproduction.com/matplotlib-savefig/
            print (f"Figure exported as \'{new_file_path}.png\'. Any previous file in this root path was overwritten.")

        plt.show()

    else:
        
        # Show masked (cleaner) plot instead of the standard one
        # Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
        plt.figure(figsize = (12, 8))
        # Mask for the upper triangle
        mask = np.zeros_like(covariance_matrix)

        mask[np.triu_indices_from(mask)] = True

        # Generate a custom diverging colormap
        cmap = sns.diverging_palette(220, 10, as_cmap = True)

        # Heatmap with mask and correct aspect ratio
        sns.heatmap((covariance_matrix), mask = mask, cmap = cmap, center = 0,
                    linewidths = .5)
        
        if (export_png == True):
            # Image will be exported
            import os

            #check if the user defined a directory path. If not, set as the default root path:
            if (directory_to_save is None):
                #set as the default
                directory_to_save = ""

            #check if the user defined a file name. If not, set as the default name for this
            # function.
            if (file_name is None):
                #set as the default
                file_name = "covariance_matrix"

            #check if the user defined an image resolution. If not, set as the default 110 dpi
            # resolution.
            if (png_resolution_dpi is None):
                #set as 330 dpi
                png_resolution_dpi = 330

            #Get the new_file_path
            new_file_path = os.path.join(directory_to_save, file_name)

            #Export the file to this new path:
            # The extension will be automatically added by the savefig method:
            plt.savefig(new_file_path, dpi = png_resolution_dpi, quality = 100, format = 'png', transparent = False) 
            #quality could be set from 1 to 100, where 100 is the best quality
            #format (str, supported formats) = 'png', 'pdf', 'ps', 'eps' or 'svg'
            #transparent = True or False
            # For other parameters of .savefig method, check https://indianaiproduction.com/matplotlib-savefig/
            print (f"Figure exported as \'{new_file_path}.png\'. Any previous file in this root path was overwritten.")

        plt.show()

    
    #Sort the values of covariance_matrix in Descending order:
    
    if (responses_to_return_cov is not None):
        
        if (type(responses_to_return_cov) == str):
            # If a string was input, put it inside a list
            responses_to_return_cov = [responses_to_return_cov]

    else:
        # Use all columns
        responses_to_return_cov = list(DATASET.columns)

    #Select only the desired responses, by passing the list responses_to_return_cov
    # as parameter for column filtering:
    covariance_matrix = covariance_matrix[responses_to_return_cov]
    # By passing a list as argument, we assure that the output is a dataframe
    # and not a series, even if the list contains a single element.
    
    # Create a list of boolean variables == False, one False correspondent to
    # each one of the responses
    ascending_modes = [False for i in range(0, len(responses_to_return_cov))]
    
    #Now sort the values according to the responses, by passing the list
    # response
    covariance_matrix = covariance_matrix.sort_values(by = responses_to_return_cov, ascending = ascending_modes)
   
    explain = """

    Theory
    -----------------------------------------------------------------------------------------------------------------

    Given that E(X) = mu is the expectation (expected value) from a random variable X, the variance Var(X) is defined as:

        Var(X) = E(X²) - [E(X)]²
    
    Analogously, the covariance between X and Y, a statistic that reflects how they vary together, is defined by:

        Cov(X,Y) = E(X.Y) - E(X).E(Y)
    
    From these equations, we notice that Cov(X,X) = Var(X)

    Thus, the covariance matrix between X and Y is given by the matrix:

        Cov = [[Var(X) Cov(Y,X)]
                [Cov(X,Y) Var(Y)]]

        where, in general, Cov(Y,X) = Cov(X,Y)
    
    For n samples with same probability of occurrence, the covariance may be calculated as:

        Cov(X,Y) = (1/n)*SUM((Xi - Mean(X))*(Yi - Mean(Y))),
        
        where (Xi,Yi) represents a single data point. In the case of events with different probabilities,
        the formula is modified to take this effect in account. 

    ---------------------------------------------------------------------------------------------------------------------

    Interpretation of the matrix
    ---------------------------------------------------------------------------------------------------------------------

    For randomly spread data:

    1. Cov(X,Y) ~ 0 (close to zero)
        Variables are independent from each other
    
    2. Cov(X,Y) > 0
        There is a positive correlation between variables.

    3. Cov(X,Y) < 0
        There is a negative correlation between variables. 
    
    """

    print(explain)
     
    print("Covariance matrix - numeric results:\n")
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(covariance_matrix)
            
    except: # regular mode
        print(covariance_matrix)
    
    return covariance_matrix


def calculate_vif (df):
    """
    calculate_vif (df)

    https://towardsdatascience.com/collinearity-measures-6543d8597a2e
    https://www.geeksforgeeks.org/detecting-multicollinearity-with-vif-python/
    https://www.statsmodels.org/stable/generated/statsmodels.stats.outliers_influence.variance_inflation_factor.html#statsmodels-stats-outliers-influence-variance-inflation-factor

    : param: df - Pandas dataframe to be analyzed.
    """

    from statsmodels.stats.outliers_influence import variance_inflation_factor
    
    # set a local copy of the dataset to perform the calculations:
    X = df.copy(deep = True)
    
    # Let's remove the categorical columns
    print("ATTENTION! The analysis will be performed only for the numeric variables.")
    print("Categorical columns will be automatically ignored.\n")

    # List the possible numeric data types for a Pandas dataframe column:
    numeric_dtypes = [np.int16, np.int32, np.int64, np.float16, np.float32, np.float64]
    numeric_cols = []
    # Loop through all valid columns (cols_list)
    for column in X.columns:
        
        # Check if the column is neither in timestamp_list nor in
        # categorical_list yet:
        column_data_type = X[column].dtype
            
        if (column_data_type in numeric_dtypes):
            # Append to categorical columns list:
            numeric_cols.append(column)
    
    # Filter the dataset to include only numeric variables:
    X = X[numeric_cols]
    
    # Now, obtain the VIFs

    X_columns = list(X.columns)
    # Calculate VIF for each variable:
    vifs = [variance_inflation_factor(X.values, i) for i in range(len(X_columns))]
    """
    The attribute values from a dataframe stores the correspondent NumPy array, i.e., a matrix containing the data table.
    Example:
    x = pd.DataFrame(data = {'a': [1, 2], 'v':[3,4]})
    x.values returns:
    array([[1, 3],
       [2, 4]], dtype=int64)
    """

    # Obtain the dataframe
    variance_inflation_factor_matrix = pd.DataFrame(data = {'feature': X_columns, 'VIF': vifs})
    # Set the feature column as index
    variance_inflation_factor_matrix = variance_inflation_factor_matrix.set_index('feature')
    # Organize in descending order:
    variance_inflation_factor_matrix = variance_inflation_factor_matrix.sort_values(by = ['VIF'], ascending = [False])

    explain = """
    - When selecting variables for a model, we want them to be independent from each other.
    - In cases where selected predictor variables are not independent of each other, we would not be able to determine or attribute the contribution from the various predictor variables towards the target variable. 
        — Interpretability of the model coefficients becomes an issue.
    - The presence of multicollinearity can mask the importance of the respective variable contributions to the target variable.
    - Collinear variables introduce basically the same information to the model, inflating the importance of a given variable.
    - One approach to identify multicollinearity is via the Variance Inflation Factor (VIF). 
    - VIF indicates the percentage of the variance inflated for each variable’s coefficient. 
    
    In VIF method, we pick each feature and regress it against all of the other features. 
    For each regression, the factor is calculated as:

        VIF = 1/(1-R²)

    Where, R-squared is the coefficient of determination in linear regression. Its value lies between 0 and 1.

    1. VIF = 1
        - No collinearity (R² = 0).
    2. < VIF < 5
        - Moderate collinearity.
    3. VIF >= 5
        - High collinearity.
        - Some cases where high VIF would be acceptable:
            - Use of interaction terms, polynomial terms, or dummy variables (nominal variables with three or more categories).
    
    - Correlation matrices enable the identification of correlation among variable pairs. 
    - VIF enables the overall assessment of multicollinearity. 
    
    Variables showing high VIFs are usually variables with high collinearity.

    """
    
    print(explain)
     
    print("Calculated Variance Inflation Factors (VIFs):\n")
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(variance_inflation_factor_matrix)
            
    except: # regular mode
        print(variance_inflation_factor_matrix)
    
    return variance_inflation_factor_matrix


def bar_chart (df, categorical_var_name, response_var_name, aggregate_function = 'sum', add_suffix_to_aggregated_col = True, suffix = None, calculate_and_plot_cumulative_percent = True, orientation = 'vertical', limit_of_plotted_categories = None, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    bar_chart (df, categorical_var_name, response_var_name, aggregate_function = 'sum', add_suffix_to_aggregated_col = True, suffix = None, calculate_and_plot_cumulative_percent = True, orientation = 'vertical', limit_of_plotted_categories = None, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    : param: df: dataframe being analyzed
    
    : param: categorical_var_name: string (inside quotes) containing the name 
      of the column to be analyzed. e.g. 
      categorical_var_name = "column1"
    
    : param: response_var_name: string (inside quotes) containing the name 
      of the column that stores the response correspondent to the
      categories. e.g. response_var_name = "response_feature" 
    
    : param: aggregate_function = 'sum': String defining the aggregation 
      method that will be applied. Possible values:
      'median', 'mean', 'mode', 'sum', 'min', 'max', 'variance', 'count',
      'standard_deviation', '10_percent_quantile', '20_percent_quantile',
      '25_percent_quantile', '30_percent_quantile', '40_percent_quantile',
      '50_percent_quantile', '60_percent_quantile', '70_percent_quantile',
      '75_percent_quantile', '80_percent_quantile', '90_percent_quantile',
      '95_percent_quantile', 'kurtosis', 'skew', 'interquartile_range',
      'mean_standard_error', 'entropy'
      To use another aggregate function, you can use the .agg method, passing 
      the aggregate as argument, such as in:
      .agg(scipy.stats.mode), 
      where the argument is a Scipy aggregate function.
      If None or an invalid function is input, 'sum' will be used.
    
    : param: add_suffix_to_aggregated_col = True will add a suffix to the
      aggregated column. e.g. 'responseVar_mean'. If add_suffix_to_aggregated_col 
      = False, the aggregated column will have the original column name.
    
    : param: suffix = None. Keep it None if no suffix should be added, or if
      the name of the aggregate function should be used as suffix, after
      "_". Alternatively, set it as a string. As recommendation, put the
      "_" sign in the beginning of this string to separate the suffix from
      the original column name. e.g. if the response variable is 'Y' and
      suffix = '_agg', the new aggregated column will be named as 'Y_agg'
    
    : param: calculate_and_plot_cumulative_percent = True to calculate and plot
      the line of cumulative percent, or 
      calculate_and_plot_cumulative_percent = False to omit it.
      This feature is only shown when aggregate_function = 'sum', 'median',
      'mean', or 'mode'. So, it will be automatically set as False if 
      another aggregate is selected.
    
    : param: orientation = 'vertical' is the standard, and plots vertical bars
      (perpendicular to the X axis). In this case, the categories are shown
      in the X axis, and the correspondent responses are in Y axis.
      Alternatively, orientation = 'horizontal' results in horizontal bars.
      In this case, categories are in Y axis, and responses in X axis.
      If None or invalid values are provided, orientation is set as 'vertical'.
    
      Note: to obtain a Pareto chart, keep aggregate_function = 'sum',
      plot_cumulative_percent = True, and orientation = 'vertical'.
    
    : param: limit_of_plotted_categories: integer value that represents
      the maximum of categories that will be plot. Keep it None to plot
      all categories. Alternatively, set an integer value. e.g.: if
      limit_of_plotted_categories = 4, but there are more categories,
      the dataset will be sorted in descending order and: 1) The remaining
      categories will be sum in a new category named 'others' if the
      aggregate function is 'sum'; 2) Or the other categories will be simply
      omitted from the plot, for other aggregate functions. Notice that
      it limits only the variables in the plot: all of them will be
      returned in the dataframe.
      Use this parameter to obtain a cleaner plot. Notice that the remaining
      columns will be aggregated as 'others' even if there is a single column
      beyond the limit.
    """

    # Create a local copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    
    # Before calling the method, we must guarantee that the variables may be
    # used for that aggregate. Some aggregations are permitted only for numeric variables, so calling
    # the methods before selecting the variables may raise warnings or errors.
    
    
    list_of_aggregates = ['median', 'mean', 'mode', 'sum', 'min', 'max', 'variance', 'count',
                        'standard_deviation', '10_percent_quantile', '20_percent_quantile', 
                        '25_percent_quantile', '30_percent_quantile', '40_percent_quantile', 
                        '50_percent_quantile', '60_percent_quantile', '70_percent_quantile', 
                        '75_percent_quantile', '80_percent_quantile', '90_percent_quantile', 
                        '95_percent_quantile', 'kurtosis', 'skew', 'interquartile_range', 
                        'mean_standard_error', 'entropy']
    
    list_of_numeric_aggregates = ['median', 'mean', 'sum', 'min', 'max', 'variance',
                                'standard_deviation', '10_percent_quantile', '20_percent_quantile', 
                                '25_percent_quantile', '30_percent_quantile', '40_percent_quantile', 
                                '50_percent_quantile', '60_percent_quantile', '70_percent_quantile', 
                                '75_percent_quantile', '80_percent_quantile', '90_percent_quantile',
                                '95_percent_quantile', 'kurtosis', 'skew', 'interquartile_range', 
                                'mean_standard_error']
    
    # Check if an invalid or no aggregation function was selected:
    if ((aggregate_function not in (list_of_aggregates)) | (aggregate_function is None)):
        
        aggregate_function = 'sum'
        print("Invalid or no aggregation function input, so using the default \'sum\'.\n")
    
    # List the possible numeric data types for a Pandas dataframe column:
    numeric_dtypes = [np.int16, np.int32, np.int64, np.float16, np.float32, np.float64]
    
    # Check if a numeric aggregate was selected:
    if (aggregate_function in list_of_numeric_aggregates):
        
        column_data_type = DATASET[response_var_name].dtype
        
        if (column_data_type not in numeric_dtypes):
            
                # If the Pandas series was defined as an object, it means it is categorical
                # (string, date, etc).
                print("Numeric aggregate selected, but categorical variable indicated as response variable.")
                print("Setting aggregate_function = \'mode\', to make aggregate compatible with data type.\n")
                
                aggregate_function = 'mode'
    
    else: # categorical aggregate function
        
        column_data_type = DATASET[response_var_name].dtype
        
        if ((column_data_type in numeric_dtypes) & (aggregate_function != 'count')):
                # count is the only aggregate for categorical that can be used for numerical variables as well.
                
                print("Categorical aggregate selected, but numeric variable indicated as response variable.")
                print("Setting aggregate_function = \'sum\', to make aggregate compatible with data type.\n")
                
                aggregate_function = 'sum'
    
    # Before grouping, let's remove the missing values, avoiding the raising of TypeError.
    # Pandas deprecated the automatic dropna with aggregation:
    DATASET = DATASET.dropna(axis = 0)
    
    # Convert categorical_var_name to string type. If the variable is represented by
    # a number, the dataframe will be grouped in terms of an aggregation of the variable, instead
    # of as a category (bars will be shown in number ascending order). It will prevents this to happen:
    DATASET[categorical_var_name] = DATASET[categorical_var_name].astype(str)    
    
    # If an aggregate function different from 'sum', 'mean', 'median' or 'mode' 
    # is used with plot_cumulative_percent = True, 
    # set plot_cumulative_percent = False:
    # (check if aggregate function is not in the list of allowed values):
    if ((aggregate_function not in ['sum', 'mean', 'median', 'mode', 'count']) & (calculate_and_plot_cumulative_percent == True)):
        
        calculate_and_plot_cumulative_percent = False
        print("The cumulative percent is only calculated when aggregate_function = \'sum\', \'mean\', \'median\', \'mode\', or \'count\'. So, plot_cumulative_percent was set as False.")
    
    # Guarantee that the columns from the aggregated dataset have the correct names
    
    # Groupby according to the selection.
    # Here, there is a great gain of performance in not using a dictionary of methods:
    # If using a dictionary of methods, Pandas would calculate the results for each one of the methods.
    
    # Pandas groupby method documentation:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.groupby.html?msclkid=7b3531a6cff211ec9086f4edaddb94ba
    # argument as_index = False: prevents the grouper variable to be set as index of the new dataframe.
    # (default: as_index = True);
    # dropna = False: do not removes the missing values (default: dropna = True, used here to avoid
    # compatibility and version issues)
    
    if (aggregate_function == 'median'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].agg('median')

    elif (aggregate_function == 'mean'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].mean()
    
    elif (aggregate_function == 'mode'):
        
        # stats.mode now only works for numerically encoded variables (the previous ordinal
        # encoding is required)
        SUBSET_OF_FEATURES_TO_BE_ENCODED = [categorical_var_name, response_var_name]
        DATASET, ordinal_encoding_list = OrdinalEncoding_df (df = DATASET, subset_of_features_to_be_encoded = SUBSET_OF_FEATURES_TO_BE_ENCODED)
        DATASET = DATASET.drop(columns = SUBSET_OF_FEATURES_TO_BE_ENCODED)
        categorical_var_name = categorical_var_name + "_OrdinalEnc"
        response_var_name = response_var_name + "_OrdinalEnc"
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].agg(stats.mode)
        ENCODING_LIST = ordinal_encoding_list

        # Save the series as a list:
        list_of_modes_arrays = list(DATASET[response_var_name])
        # Start a list of modes:
        list_of_modes = []
            
        # Loop through each element from the list of arrays:
        for mode_array in list_of_modes_arrays:
            # try accessing the mode
            # mode array is like:
            # ModeResult(mode=calculated_mode, count=counting_of_occurrences))
            # To retrieve only the mode, we must access the element [0] from this array
            # or attribute mode:
                
            try:
                list_of_modes.append(mode_array.mode)
            
            except:
                # This error is generated when trying to access an array storing no values.
                # (i.e., with missing values). Since there is no dimension, it is not possible
                # to access the [0][0] position. In this case, simply append the np.nan 
                # the (missing value):
                try:
                    list_of_modes.append(mode_array[0])
                except:
                    try:
                        if ((mode_array != np.nan) & (mode_array is not None)):
                            list_of_modes.append(mode_array)
                        else:
                            list_of_modes.append(np.nan)
                    except:
                        list_of_modes.append(np.nan)
        
        # Make the list of modes the column itself:
        DATASET[response_var_name] = list_of_modes
        
        DATASET = reverse_OrdinalEncoding (df = DATASET, encoding_list = ENCODING_LIST)
        DATASET = DATASET.drop(columns = [categorical_var_name, response_var_name])

    elif (aggregate_function == 'sum'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].sum()
    
    elif (aggregate_function == 'count'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].count()

    elif (aggregate_function == 'min'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].min()
    
    elif (aggregate_function == 'max'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].max()
    
    elif (aggregate_function == 'variance'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].var()

    elif (aggregate_function == 'standard_deviation'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].std()
    
    elif (aggregate_function == '10_percent_quantile'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].quantile(0.10)
    
    elif (aggregate_function == '20_percent_quantile'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].quantile(0.20)
    
    elif (aggregate_function == '25_percent_quantile'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].quantile(0.25)
    
    elif (aggregate_function == '30_percent_quantile'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].quantile(0.30)
    
    elif (aggregate_function == '40_percent_quantile'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].quantile(0.40)
    
    elif (aggregate_function == '50_percent_quantile'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].quantile(0.50)

    elif (aggregate_function == '60_percent_quantile'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].quantile(0.60)
    
    elif (aggregate_function == '70_percent_quantile'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].quantile(0.30)

    elif (aggregate_function == '75_percent_quantile'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].quantile(0.75)

    elif (aggregate_function == '80_percent_quantile'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].quantile(0.80)
    
    elif (aggregate_function == '90_percent_quantile'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].quantile(0.90)
    
    elif (aggregate_function == '95_percent_quantile'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].quantile(0.95)

    elif (aggregate_function == 'kurtosis'):
        # Numeric aggregate
        SUBSET_OF_FEATURES_TO_BE_ENCODED = [categorical_var_name]
        DATASET, ordinal_encoding_list = OrdinalEncoding_df (df = DATASET, subset_of_features_to_be_encoded = SUBSET_OF_FEATURES_TO_BE_ENCODED)
        DATASET = DATASET.drop(columns = SUBSET_OF_FEATURES_TO_BE_ENCODED)
        categorical_var_name = categorical_var_name + "_OrdinalEnc"
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].agg(stats.kurtosis)
        ENCODING_LIST = ordinal_encoding_list
        DATASET = reverse_OrdinalEncoding (df = DATASET, encoding_list = ENCODING_LIST)
        DATASET = DATASET.drop(columns = categorical_var_name)

    elif (aggregate_function == 'skew'):
        # Numeric aggregate
        SUBSET_OF_FEATURES_TO_BE_ENCODED = [categorical_var_name]
        DATASET, ordinal_encoding_list = OrdinalEncoding_df (df = DATASET, subset_of_features_to_be_encoded = SUBSET_OF_FEATURES_TO_BE_ENCODED)
        DATASET = DATASET.drop(columns = SUBSET_OF_FEATURES_TO_BE_ENCODED)
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].agg(stats.skew)
        ENCODING_LIST = ordinal_encoding_list

    elif (aggregate_function == 'interquartile_range'):
        # Numeric aggregate
        SUBSET_OF_FEATURES_TO_BE_ENCODED = [categorical_var_name]
        DATASET, ordinal_encoding_list = OrdinalEncoding_df (df = DATASET, subset_of_features_to_be_encoded = SUBSET_OF_FEATURES_TO_BE_ENCODED)
        DATASET = DATASET.drop(columns = SUBSET_OF_FEATURES_TO_BE_ENCODED)
        categorical_var_name = categorical_var_name + "_OrdinalEnc"
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].agg(stats.iqr)
        ENCODING_LIST = ordinal_encoding_list
        DATASET = reverse_OrdinalEncoding (df = DATASET, encoding_list = ENCODING_LIST)
        DATASET = DATASET.drop(columns = categorical_var_name)

    elif (aggregate_function == 'mean_standard_error'):
        # Numeric aggregate
        SUBSET_OF_FEATURES_TO_BE_ENCODED = [categorical_var_name]
        DATASET, ordinal_encoding_list = OrdinalEncoding_df (df = DATASET, subset_of_features_to_be_encoded = SUBSET_OF_FEATURES_TO_BE_ENCODED)
        DATASET = DATASET.drop(columns = SUBSET_OF_FEATURES_TO_BE_ENCODED)
        categorical_var_name = categorical_var_name + "_OrdinalEnc"
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].agg(stats.sem)
        ENCODING_LIST = ordinal_encoding_list
        DATASET = reverse_OrdinalEncoding (df = DATASET, encoding_list = ENCODING_LIST)
        DATASET = DATASET.drop(columns = categorical_var_name)

    else: # entropy
        SUBSET_OF_FEATURES_TO_BE_ENCODED = [categorical_var_name]
        DATASET, ordinal_encoding_list = OrdinalEncoding_df (df = DATASET, subset_of_features_to_be_encoded = SUBSET_OF_FEATURES_TO_BE_ENCODED)
        DATASET = DATASET.drop(columns = SUBSET_OF_FEATURES_TO_BE_ENCODED)
        categorical_var_name = categorical_var_name + "_OrdinalEnc"
        response_var_name = response_var_name + "_OrdinalEnc"
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].agg(stats.entropy)
        ENCODING_LIST = ordinal_encoding_list
        DATASET = reverse_OrdinalEncoding (df = DATASET, encoding_list = ENCODING_LIST)
        DATASET = DATASET.drop(columns = [categorical_var_name, response_var_name])
    
    # List of columns of the aggregated dataset:
    list_of_columns = list(DATASET.columns) # convert to a list
    
    if (add_suffix_to_aggregated_col == True):
            
        if (suffix is None):
                
            suffix = "_" + aggregate_function
            
        new_columns = [(str(name) + suffix) for name in list_of_columns]
        # Do not consider the first element, which is the aggregate function with a suffix.
        # Concatenate the correct name with the columns from the second element of the list:
        new_columns = [categorical_var_name] + new_columns[1:]
        # Make it the new columns:
        DATASET.columns = new_columns
        # Update the list of columns:
        list_of_columns = DATASET.columns
    
          
    # the name of the response variable is now the second element from the list of column:
    response_var_name = list(DATASET.columns)[1]
    # the categorical variable name was not changed.
    
    # Let's sort the dataframe.
    
    # Order the dataframe in descending order by the response.
    # If there are equal responses, order them by category, in
    # ascending order; put the missing values in the first position
    # To pass multiple columns and multiple types of ordering, we use
    # lists. If there was a single column to order by, we would declare
    # it as a string. If only one order of ascending was used, we would
    # declare it as a simple boolean
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html
    
    DATASET = DATASET.sort_values(by = [response_var_name, categorical_var_name], ascending = [False, True], na_position = 'first')
    
    # Now, reset index positions:
    DATASET = DATASET.reset_index(drop = True)
    
    if (aggregate_function == 'count'):
        
        # Here, the column represents the counting, no matter the variable set as response.
        DATASET.columns = [categorical_var_name, 'count_of_entries']
        response_var_name = 'count_of_entries'
    
    # plot_cumulative_percent = True, create a column to store the
    # cumulative percent:
    if (calculate_and_plot_cumulative_percent): 
        # Run the following code if the boolean value is True (implicity)
        # Only calculates cumulative percent in case aggregate is 'sum' or 'mode'
        
        # Create a column series for the cumulative sum:
        cumsum_col = response_var_name + "_cumsum"
        DATASET[cumsum_col] = DATASET[response_var_name].cumsum()
        
        # total sum is the last element from this series
        # (i.e. the element with index len(DATASET) - 1)
        total_sum = DATASET[cumsum_col][(len(DATASET) - 1)]
        
        # Now, create a column for the accumulated percent
        # by dividing cumsum_col by total_sum and multiplying it by
        # 100 (%):
        cum_pct_col = response_var_name + "_cum_pct"
        DATASET[cum_pct_col] = (DATASET[cumsum_col])/(total_sum) * 100
        print(f"Successfully calculated cumulative sum and cumulative percent correspondent to the response variable {response_var_name}.")
    
    print("Successfully aggregated and ordered the dataset to plot. Check the 10 first rows of this returned dataset:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(DATASET.head(10))
            
    except: # regular mode
        print(DATASET.head(10))
    
    # Check if the total of plotted categories is limited:
    if not (limit_of_plotted_categories is None):
        
        # Since the value is not None, we have to limit it
        # Check if the limit is lower than or equal to the length of the dataframe.
        # If it is, we simply copy the columns to the series (there is no need of
        # a memory-consuming loop or of applying the head method to a local copy
        # of the dataframe):
        df_length = len(DATASET)
            
        if (df_length <= limit_of_plotted_categories):
            # Simply copy the columns to the graphic series:
            categories = DATASET[categorical_var_name]
            responses = DATASET[response_var_name]
            # If there is a cum_pct column, copy it to a series too:
            if (calculate_and_plot_cumulative_percent):
                cum_pct = DATASET[cum_pct_col]
        
        else:
            # The limit is lower than the total of categories,
            # so we actually have to limit the size of plotted df:
        
            # If aggregate_function is not 'sum', we simply apply
            # the head method to obtain the first rows (number of
            # rows input as parameter; if no parameter is input, the
            # number of 5 rows is used):
            
            # Limit to the number limit_of_plotted_categories:
            # create another local copy of the dataframe not to
            # modify the returned dataframe object:
            plotted_df = DATASET.copy(deep = True).head(limit_of_plotted_categories)

            # Create the series of elements to plot:
            categories = list(plotted_df[categorical_var_name])
            responses = list(plotted_df[response_var_name])
            # If the cumulative percent was obtained, create the series for it:
            if (calculate_and_plot_cumulative_percent):
                cum_pct = list(plotted_df[cum_pct_col])
            
            # Start variable to store the aggregates from the others:
            other_responses = 0
            
            # Loop through each row from DATASET:
            for i in range(0, len(DATASET)):
                
                # Check if the category is not in categories:
                category = DATASET[categorical_var_name][i]
                
                if (category not in categories):
                    
                    # sum the value in the response variable to other_responses:
                    other_responses = other_responses + DATASET[response_var_name][i]
            
            # Now we finished the sum of the other responses, let's add these elements to
            # the lists:
            categories.append("others")
            responses.append(other_responses)
            # If there is a cumulative percent, append 100% to the list:
            if (calculate_and_plot_cumulative_percent):
                cum_pct.append(100)
                # The final cumulative percent must be the total, 100%
            
            else:

                # Firstly, copy the elements that will be kept to x, y and (possibly) cum_pct
                # lists.
                # Start the lists:
                categories = []
                responses = []
                if (calculate_and_plot_cumulative_percent):
                    cum_pct = [] # start this list only if its needed to save memory

                for i in range (0, limit_of_plotted_categories):
                    # i goes from 0 (first index) to limit_of_plotted_categories - 1
                    # (index of the last category to be kept):
                    # copy the elements from the DATASET to the list
                    # category is the 1st column (column 0); response is the 2nd (col 1);
                    # and cumulative percent is the 4th (col 3):
                    categories.append(DATASET.iloc[i, 0])
                    responses.append(DATASET.iloc[i, 1])
                    
                    if (calculate_and_plot_cumulative_percent):
                        cum_pct.append(DATASET.iloc[i, 3]) # only if there is something to iloc
                    
                # Now, i = limit_of_plotted_categories - 1
                # Create a variable to store the sum of other responses
                other_responses = 0
                # loop from i = limit_of_plotted_categories to i = df_length-1, index
                # of the last element. Notice that this loop may have a single call, if there
                # is only one element above the limit:
                for i in range (limit_of_plotted_categories, (df_length - 1)):
                    
                    other_responses = other_responses + (DATASET.iloc[i, 1])
                
                # Now, add the last elements to the series:
                # The last category is named 'others':
                categories.append('others')
                # The correspondent aggregated response is the value 
                # stored in other_responses:
                responses.append(other_responses)
                # The cumulative percent is 100%, since this must be the sum of all
                # elements (the previous ones plus the ones aggregated as 'others'
                # must totalize 100%).
                # On the other hand, the cumulative percent is stored only if needed:
                cum_pct.append(100)
    
    else:
        # This is the situation where there is no limit of plotted categories. So, we
        # simply copy the columns to the plotted series (it is equivalent to the 
        # situation where there is a limit, but the limit is equal or inferior to the
        # size of the dataframe):
        categories = DATASET[categorical_var_name]
        responses = DATASET[response_var_name]
        # If there is a cum_pct column, copy it to a series too:
        if (calculate_and_plot_cumulative_percent):
            cum_pct = DATASET[cum_pct_col]
    
    
    # Now the data is prepared and we only have to plot 
    # categories, responses, and cum_pct:
    
    # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
    # so that the bars do not completely block other views.
    OPACITY = 0.95
    
    # Set labels and titles for the case they are None
    if (plot_title is None):
        
        if (aggregate_function == 'count'):
            # The graph is the same count, no matter the response
            plot_title = f"Bar_chart_count_of_{categorical_var_name}"
        
        else:
            plot_title = f"Bar_chart_for_{response_var_name}_by_{categorical_var_name}"
    
    if (horizontal_axis_title is None):

        horizontal_axis_title = categorical_var_name

    if (vertical_axis_title is None):
        # Notice that response_var_name already has the suffix indicating the
        # aggregation function
        vertical_axis_title = response_var_name
    
    fig, ax1 = plt.subplots(figsize = (12, 8))
    # Set image size (x-pixels, y-pixels) for printing in the notebook's cell:

    #ROTATE X AXIS IN XX DEGREES
    plt.xticks(rotation = x_axis_rotation)
    # XX = 70 DEGREES x_axis (Default)
    #ROTATE Y AXIS IN XX DEGREES:
    plt.yticks(rotation = y_axis_rotation)
    # XX = 0 DEGREES y_axis (Default)
    
    plt.title(plot_title)
    
    if (orientation == 'horizontal'):
        
        # invert the axes in relation to the default (vertical, below)
        ax1.set_ylabel(horizontal_axis_title)
        ax1.set_xlabel(vertical_axis_title, color = 'darkblue')
        
        # Horizontal bars used - barh method (bar horizontal):
        # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.barh.html
        # Now, the categorical variables stored in series categories must be
        # positioned as the vertical axis Y, whereas the correspondent responses
        # must be in the horizontal axis X.
        ax1.barh(categories, responses, color = 'darkblue', alpha = OPACITY, label = categorical_var_name)
        #.barh(y, x, ...)
        
        if (calculate_and_plot_cumulative_percent):
            # Let's plot the line for the cumulative percent
            # Set the grid for the bar chart as False. If it is True, there will
            # be to grids, one for the bars and other for the percents, making 
            # the image difficult to interpretate:
            ax1.grid(False)
            
            # Create the twin plot for the cumulative percent:
            # for the vertical orientation, we use the twinx. Here, we use twiny
            ax2 = ax1.twiny()
            # Here, the x axis must be the cum_pct value, and the Y
            # axis must be categories (it must be correspondent to the
            # bar chart)
            ax2.plot(cum_pct, categories, '-ro', label = "cumulative\npercent")
            #.plot(x, y, ...)
            ax2.tick_params('x', color = 'red')
            ax2.set_xlabel("Cumulative Percent (%)", color = 'red')
            ax2.legend()
            ax2.grid(grid) # shown if user set grid = True
            # If user wants to see the grid, it is shown only for the cumulative line.
        
        else:
            # There is no cumulative line, so the parameter grid must control 
            # the bar chart's grid
            ax1.legend()
            ax1.grid(grid)
        
    else: 
        
        ax1.set_xlabel(horizontal_axis_title)
        ax1.set_ylabel(vertical_axis_title, color = 'darkblue')
        # If None or an invalid orientation was used, set it as vertical
        # Use Matplotlib standard bar method (vertical bar):
        # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html#matplotlib.pyplot.bar
        
        # In this standard case, the categorical variables (categories) are positioned
        # as X, and the responses as Y:
        ax1.bar(categories, responses, color = 'darkblue', alpha = OPACITY, label = categorical_var_name)
        #.bar(x, y, ...)
        
        if (calculate_and_plot_cumulative_percent):
            # Let's plot the line for the cumulative percent
            # Set the grid for the bar chart as False. If it is True, there will
            # be to grids, one for the bars and other for the percents, making 
            # the image difficult to interpretate:
            ax1.grid(False)
            
            # Create the twin plot for the cumulative percent:
            ax2 = ax1.twinx()
            ax2.plot(categories, cum_pct, '-ro', label = "cumulative\npercent")
            #.plot(x, y, ...)
            ax2.tick_params('y', color = 'red')
            ax2.set_ylabel("Cumulative Percent (%)", color = 'red', rotation = 270)
            # rotate the twin axis so that its label is inverted in relation to the main
            # vertical axis.
            ax2.legend()
            ax2.grid(grid) # shown if user set grid = True
            # If user wants to see the grid, it is shown only for the cumulative line.
        
        else:
            # There is no cumulative line, so the parameter grid must control 
            # the bar chart's grid
            ax1.legend()
            ax1.grid(grid)
    
    # Notice that the .plot method is used for generating the plot for both orientations.
    # It is different from .bar and .barh, which specify the orientation of a bar; or
    # .hline (creation of an horizontal constant line); or .vline (creation of a vertical
    # constant line).
    
    # Now the parameters specific to the configurations are finished, so we can go back
    # to the general code:
    
    if (export_png == True):
        # Image will be exported
        import os
        
        #check if the user defined a directory path. If not, set as the default root path:
        if (directory_to_save is None):
            #set as the default
            directory_to_save = ""
        
        #check if the user defined a file name. If not, set as the default name for this
        # function.
        if (file_name is None):
            #set as the default
            file_name = "bar_chart"
        
        #check if the user defined an image resolution. If not, set as the default 110 dpi
        # resolution.
        if (png_resolution_dpi is None):
            #set as 330 dpi
            png_resolution_dpi = 330
        
        #Get the new_file_path
        new_file_path = os.path.join(directory_to_save, file_name)
        
        #Export the file to this new path:
        # The extension will be automatically added by the savefig method:
        plt.savefig(new_file_path, dpi = png_resolution_dpi, quality = 100, format = 'png', transparent = False) 
        #quality could be set from 1 to 100, where 100 is the best quality
        #format (str, supported formats) = 'png', 'pdf', 'ps', 'eps' or 'svg'
        #transparent = True or False
        # For other parameters of .savefig method, check https://indianaiproduction.com/matplotlib-savefig/
        print (f"Figure exported as \'{new_file_path}.png\'. Any previous file in this root path was overwritten.")
    
    #fig.tight_layout()
    
    ## Show an image read from an image file:
    ## import matplotlib.image as pltimg
    ## img=pltimg.imread('mydecisiontree.png')
    ## imgplot = plt.imshow(img)
    ## See linkedIn Learning course: "Supervised machine learning and the technology boom",
    ##  Ex_Files_Supervised_Learning, Exercise Files, lesson '03. Decision Trees', '03_05', 
    ##  '03_05_END.ipynb'
    plt.show()
    
    return DATASET


def calculate_cumulative_stats (df, column_to_analyze, cumulative_statistic = 'sum', new_cum_stats_col_name = None):
    """
    calculate_cumulative_stats (df, column_to_analyze, cumulative_statistic = 'sum', new_cum_stats_col_name = None):
    
    : param: df: the whole dataframe to be processed.
    
    : param: column_to_analyze: string (inside quotes), 
      containing the name of the column that will be analyzed. 
      e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    : param: cumulative_statistic: the statistic that will be calculated. The cumulative
      statistics allowed are: 'sum' (for cumulative sum, cumsum); 'product' 
      (for cumulative product, cumprod); 'max' (for cumulative maximum, cummax);
      and 'min' (for cumulative minimum, cummin).
    
    : param: new_cum_stats_col_name = None or string (inside quotes), 
      containing the name of the new column created for storing the cumulative statistic
      calculated. 
      e.g. new_cum_stats_col_name = "cum_stats" will create a column named as 'cum_stats'.
      If its None, the new column will be named as column_to_analyze + "_" + [selected
      cumulative function] ('cumsum', 'cumprod', 'cummax', 'cummin')
    
    WARNING: Use this function to a analyze a single column from a dataframe.
    """

    if ((cumulative_statistic not in ['sum', 'product', 'max', 'min']) | (cumulative_statistic is None)):
        
        raise InvalidInputsError ("Please, select a valid method for calculating the cumulative statistics: sum, product, max, or min.")
    
    else:
        
        if (new_cum_stats_col_name is None):
            # set the standard name
            # column_to_analyze + "_" + [selected cumulative function] 
            # ('cumsum', 'cumprod', 'cummax', 'cummin')
            # cumulative_statistic variable stores ['sum', 'product', 'max', 'min']
            # we must concatenate "cum" to the left of this string:
            new_cum_stats_col_name = column_to_analyze + "_" + "cum" + cumulative_statistic
        
        # create a local copy of the dataframe to manipulate:
        DATASET = df.copy(deep = True)
        # The series to be analyzed is stored as DATASET[column_to_analyze]
        
        # Now apply the correct method
        # the dictionary dict_of_methods correlates the input cumulative_statistic to the
        # correct Pandas method to be applied to the dataframe column
        dict_of_methods = {
            
            'sum': DATASET[column_to_analyze].cumsum(),
            'product': DATASET[column_to_analyze].cumprod(),
            'max': DATASET[column_to_analyze].cummax(),
            'min': DATASET[column_to_analyze].cummin()
        }
        
        # To access the value (method) correspondent to a given key (input as 
        # cumulative_statistic): dictionary['key'], just as if accessing a column from
        # a dataframe. In this case, the method is accessed as:
        # dict_of_methods[cumulative_statistic], since cumulative_statistic is itself the key
        # of the dictionary of methods.
        
        # store the resultant of the method in a new column of DATASET 
        # named as new_cum_stats_col_name
        DATASET[new_cum_stats_col_name] = dict_of_methods[cumulative_statistic]
        
        print(f"The cumulative {cumulative_statistic} statistic was successfully calculated and added as the column \'{new_cum_stats_col_name}\' of the returned dataframe.\n")
        print("Check the new dataframe's 10 first rows:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(DATASET.head(10))

        except: # regular mode
            print(DATASET.head(10))
        
        return DATASET


def scatter_plot_lin_reg (data_in_same_column = False, df = None, column_with_predict_var_x = None, column_with_response_var_y = None, column_with_labels = None, list_of_dictionaries_with_series_to_analyze = [{'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}], x_axis_rotation = 70, y_axis_rotation = 0, show_linear_reg = True, grid = True, add_splines_lines = False, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330): 
    """
    scatter_plot_lin_reg (data_in_same_column = False, df = None, column_with_predict_var_x = None, column_with_response_var_y = None, column_with_labels = None, list_of_dictionaries_with_series_to_analyze = [{'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}], x_axis_rotation = 70, y_axis_rotation = 0, show_linear_reg = True, grid = True, add_splines_lines = False, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330): 
    
    matplotlib.colors documentation:
     https://matplotlib.org/3.5.0/api/colors_api.html?msclkid=94286fa9d12f11ec94660321f39bf47f
    
    Matplotlib list of colors:
     https://matplotlib.org/stable/gallery/color/named_colors.html?msclkid=0bb86abbd12e11ecbeb0a2439e5b0d23
    Matplotlib colors tutorial:
     https://matplotlib.org/stable/tutorials/colors/colors.html
    Matplotlib example of Python code using matplotlib.colors:
     https://matplotlib.org/stable/_downloads/0843ee646a32fc214e9f09328c0cd008/colors.py
    Same example as Jupyter Notebook:
     https://matplotlib.org/stable/_downloads/2a7b13c059456984288f5b84b4b73f45/colors.ipynb
    
        
    : param: data_in_same_column = False: set as True if all the values to plot are in a same column.
      If data_in_same_column = True, you must specify the dataframe containing the data as df;
      the column containing the predict variable (X) as column_with_predict_var_x; the column 
      containing the responses to plot (Y) as column_with_response_var_y; and the column 
      containing the labels (subgroup) indication as column_with_labels. 
    : param: df is an object, so do not declare it in quotes. The other three arguments (columns' names) 
      are strings, so declare in quotes. 
    
      Example: suppose you have a dataframe saved as dataset, and two groups A and B to compare. 
      All the results for both groups are in a column named 'results', wich will be plot against
      the time, saved as 'time' (X = 'time'; Y = 'results'). If the result is for
      an entry from group A, then a column named 'group' has the value 'A'. If it is for group B,
      column 'group' shows the value 'B'. In this example:
      data_in_same_column = True,
      df = dataset,
    
    : param: column_with_predict_var_x = 'time',
    : param: column_with_response_var_y = 'results', 
    : param: column_with_labels = 'group'
      If you want to declare a list of dictionaries, keep data_in_same_column = False and keep
      df = None (the other arguments may be set as None, but it is not mandatory: 
      column_with_predict_var_x = None, column_with_response_var_y = None, column_with_labels = None).
    
    Parameter to input when DATA_IN_SAME_COLUMN = False:
    : param: list_of_dictionaries_with_series_to_analyze: if data is already converted to series, lists
      or arrays, provide them as a list of dictionaries. It must be declared as a list, in brackets,
      even if there is a single dictionary.
      Use always the same keys: 'x' for the X-series (predict variables); 'y' for the Y-series
      (response variables); and 'lab' for the labels. If you do not want to declare a series, simply
      keep as None, but do not remove or rename a key (ALWAYS USE THE KEYS SHOWN AS MODEL).
      If you want, you can remove elements (dictionaries) from the list to declare fewer elements;
      and you can also add more elements (dictionaries) to the lists, if you need to plot more series.
      Simply put a comma after the last element from the list and declare a new dictionary, keeping the
      same keys: {'x': x_series, 'y': y_series, 'lab': label}, where x_series, y_series and label
      represents the series and label of the added dictionary (you can pass 'lab': None, but if 
      'x' or 'y' are None, the new dictionary will be ignored).
    
      Examples:
      list_of_dictionaries_with_series_to_analyze = 
      [{'x': DATASET['X'], 'y': DATASET['Y'], 'lab': 'label'}]
      will plot a single variable. In turns:
      list_of_dictionaries_with_series_to_analyze = 
      [{'x': DATASET['X'], 'y': DATASET['Y1'], 'lab': 'label'}, {'x': DATASET['X'], 'y': DATASET['Y2'], 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}]
      will plot two series, Y1 x X and Y2 x X.
      Notice that all dictionaries where 'x' or 'y' are None are automatically ignored.
      If None is provided to 'lab', an automatic label will be generated.
    """

    import random
    # Python Random documentation:
    # https://docs.python.org/3/library/random.html?msclkid=9d0c34b2d13111ec9cfa8ddaee9f61a1
    import matplotlib.colors as mcolors
    from scipy import stats
    
    # List the possible numeric data types for a Pandas dataframe column:
    numeric_dtypes = [np.int16, np.int32, np.int64, np.float16, np.float32, np.float64]
    
    if (data_in_same_column == True):
        
        print("Data to be plotted in a same column.\n")
        
        if (df is None):
            
            print("Please, input a valid dataframe as df.\n")
            list_of_dictionaries_with_series_to_analyze = []
            # The code will check the size of this list on the next block.
            # If it is zero, code is simply interrupted.
            # Instead of returning an error, we use this code structure that can be applied
            # on other graphic functions that do not return a summary (and so we should not
            # return a value like 'error' to interrupt the function).
        
        elif (column_with_predict_var_x is None):
            
            print("Please, input a valid column name as column_with_predict_var_x.\n")
            list_of_dictionaries_with_series_to_analyze = []
        
        elif (column_with_response_var_y is None):
            
            print("Please, input a valid column name as column_with_response_var_y.\n")
            list_of_dictionaries_with_series_to_analyze = []
        
        else:
            
            # set a local copy of the dataframe:
            DATASET = df.copy(deep = True)
            
            if (column_with_labels is None):
            
                print("Using the whole series (column) for correlation.\n")
                column_with_labels = 'whole_series_' + column_with_response_var_y
                DATASET[column_with_labels] = column_with_labels
            
            # sort DATASET; by column_with_predict_var_x; by column column_with_labels
            # and by column_with_response_var_y, all in Ascending order
            # Since we sort by label (group), it is easier to separate the groups.
            DATASET = DATASET.sort_values(by = [column_with_predict_var_x, column_with_labels, column_with_response_var_y], ascending = [True, True, True])
            
            # Reset indices:
            DATASET = DATASET.reset_index(drop = True)
            
            # If column_with_predict_var_x is an object, the user may be trying to pass a date as x. 
            # So, let's try to convert it to datetime:
    
            if ((DATASET[column_with_predict_var_x]).dtype not in numeric_dtypes):
                
                try:
                    DATASET[column_with_predict_var_x] = (DATASET[column_with_predict_var_x]).astype('datetime64[ns]')
                    print("Variable X successfully converted to datetime64[ns].\n")
                    
                except:
                    # Simply ignore it
                    pass
            
            # Get a series of unique values of the labels, and save it as a list using the
            # list attribute:
            unique_labels = list(DATASET[column_with_labels].unique())
            print(f"{len(unique_labels)} different labels detected: {unique_labels}.\n")
            
            # Start a list to store the dictionaries containing the keys:
            # 'x': list of predict variables; 'y': list of responses; 'lab': the label (group)
            list_of_dictionaries_with_series_to_analyze = []
            
            # Loop through each possible label:
            for lab in unique_labels:
                # loop through each element from the list unique_labels, referred as lab
                
                # Set a filter for the dataset, to select only rows correspondent to that
                # label:
                boolean_filter = (DATASET[column_with_labels] == lab)
                
                # Create a copy of the dataset, with entries selected by that filter:
                ds_copy = (DATASET[boolean_filter]).copy(deep = True)
                # Sort again by X and Y, to guarantee the results are in order:
                ds_copy = ds_copy.sort_values(by = [column_with_predict_var_x, column_with_response_var_y], ascending = [True, True])
                # Restart the index of the copy:
                ds_copy = ds_copy.reset_index(drop = True)
                
                # Re-extract the X and Y series and convert them to NumPy arrays 
                # (these arrays will be important later in the function):
                x = np.array(ds_copy[column_with_predict_var_x])
                y = np.array(ds_copy[column_with_response_var_y])
            
                # Then, create the dictionary:
                dict_of_values = {'x': x, 'y': y, 'lab': lab}
                
                # Now, append dict_of_values to list_of_dictionaries_with_series_to_analyze:
                list_of_dictionaries_with_series_to_analyze.append(dict_of_values)
                
            # Now, we have a list of dictionaries with the same format of the input list.
            
    else:
        
        # The user input a list_of_dictionaries_with_series_to_analyze
        # Create a support list:
        support_list = []
        
        # Loop through each element on the list list_of_dictionaries_with_series_to_analyze:
        
        for i in range (0, len(list_of_dictionaries_with_series_to_analyze)):
            # from i = 0 to i = len(list_of_dictionaries_with_series_to_analyze) - 1, index of the
            # last element from the list
            
            # pick the i-th dictionary from the list:
            dictionary = list_of_dictionaries_with_series_to_analyze[i]
            
            # access 'x', 'y', and 'lab' keys from the dictionary:
            x = dictionary['x']
            y = dictionary['y']
            lab = dictionary['lab']
            # Remember that all this variables are series from a dataframe, so we can apply
            # the astype function:
            # https://www.askpython.com/python/built-in-methods/python-astype?msclkid=8f3de8afd0d411ec86a9c1a1e290f37c
            
            # check if at least x and y are not None:
            if ((x is not None) & (y is not None)):
                
                # If column_with_predict_var_x is an object, the user may be trying to pass a date as x. 
                # So, let's try to convert it to datetime:
                if (x.dtype not in numeric_dtypes):

                    try:
                        x = (x).astype('datetime64[ns]')
                        print(f"Variable X from {i}-th dictionary successfully converted to datetime64[ns].\n")

                    except:
                        # Simply ignore it
                        pass
                
                # Possibly, x and y are not ordered. Firstly, let's merge them into a temporary
                # dataframe to be able to order them together.
                # Use the 'list' attribute to guarantee that x and y were read as lists. These lists
                # are the values for a dictionary passed as argument for the constructor of the
                # temporary dataframe. When using the list attribute, we make the series independent
                # from its origin, even if it was created from a Pandas dataframe. Then, we have a
                # completely independent dataframe that may be manipulated and sorted, without worrying
                # that it may modify its origin:
                
                temp_df = pd.DataFrame(data = {'x': list(x), 'y': list(y)})
                # sort this dataframe by 'x' and 'y':
                temp_df = temp_df.sort_values(by = ['x', 'y'], ascending = [True, True])
                # restart index:
                temp_df = temp_df.reset_index(drop = True)
                
                # Re-extract the X and Y series and convert them to NumPy arrays 
                # (these arrays will be important later in the function):
                x = np.array(temp_df['x'])
                y = np.array(temp_df['y'])
                
                # check if lab is None:
                if (lab is None):
                    # input a default label.
                    # Use the str attribute to convert the integer to string, allowing it
                    # to be concatenated
                    lab = "X" + str(i) + "_x_" + "Y" + str(i)
                    
                # Then, create the dictionary:
                dict_of_values = {'x': x, 'y': y, 'lab': lab}
                
                # Now, append dict_of_values to support list:
                support_list.append(dict_of_values)
            
        # Now, support_list contains only the dictionaries with valid entries, as well
        # as labels for each collection of data. The values are independent from their origin,
        # and now they are ordered and in the same format of the data extracted directly from
        # the dataframe.
        # So, make the list_of_dictionaries_with_series_to_analyze the support_list itself:
        list_of_dictionaries_with_series_to_analyze = support_list
        print(f"{len(list_of_dictionaries_with_series_to_analyze)} valid series input.\n")

        
    # Now that both methods of input resulted in the same format of list, we can process both
    # with the same code.
    
    # Each dictionary in list_of_dictionaries_with_series_to_analyze represents a series to
    # plot. So, the total of series to plot is:
    total_of_series = len(list_of_dictionaries_with_series_to_analyze)
    
    if (total_of_series <= 0):
        
        raise InvalidInputsError ("No valid series to plot. Please, provide valid arguments.\n")
    
    else:
        
        # Continue to plotting and calculating the fitting.
        # Notice that we sorted the all the lists after they were separated and before
        # adding them to dictionaries. Also, the timestamps were converted to datetime64 variables
        
        # Now we pre-processed the data, we can obtain a final list of dictionaries, containing
        # the linear regression information (it will be plotted only if the user asked to). Start
        # a list to store all predictions:
        list_of_dictionaries_with_series_and_predictions = []
        
        # Loop through each dictionary (element) on the list list_of_dictionaries_with_series_to_analyze:
        for dictionary in list_of_dictionaries_with_series_to_analyze:
            
            x_is_datetime = False
            # boolean that will map if x is a datetime or not. Only change to True when it is.
            
            # Access keys 'x' and 'y' to retrieve the arrays.
            x = dictionary['x']
            y = dictionary['y']
            
            # Check if the elements from array x are np.datetime64 objects. Pick the first
            # element to check:
            
            if (type(np.array(x)[0]) == np.datetime64):
                
                x_is_datetime = True
                
            if (x_is_datetime):
                # In this case, performing the linear regression directly in X will
                # return an error. We must associate a sequential number to each time.
                # to keep the distance between these integers the same as in the original sequence
                # let's define a difference of 1 ns as 1. The 1st timestamp will be zero, and the
                # addition of 1 ns will be an addition of 1 unit. So a timestamp recorded 10 ns
                # after the time zero will have value 10. At the end, we divide every element by
                # 10**9, to obtain the correspondent distance in seconds.
                
                # start a list for the associated integer timescale. Put the number zero,
                # associated to the first timestamp:
                int_timescale = [0]
                
                # loop through each element of the array x, starting from index 1:
                for i in range(1, len(x)):
                    
                    # calculate the timedelta between x[i] and x[i-1]:
                    # The delta method from the Timedelta class converts the timedelta to
                    # nanoseconds, guaranteeing the internal compatibility:
                    # The .delta attribute was replaced by .value attribute. 
                    # Both return the number of nanoseconds as an integer.
                    # https://pandas.pydata.org/docs/reference/api/pandas.Timedelta.html
                    timedelta = pd.Timedelta(x[i] - x[(i-1)]).value
                    
                    # Sum this timedelta (integer number of nanoseconds) to the
                    # previous element from int_timescale, and append the result to the list:
                    int_timescale.append((timedelta + int_timescale[(i-1)]))
                
                # Now convert the new scale (that preserves the distance between timestamps)
                # to NumPy array:
                int_timescale = np.array(int_timescale)
                
                # Divide by 10**9 to obtain the distances in seconds, reducing the order of
                # magnitude of the integer numbers (the division is allowed for arrays)
                int_timescale = int_timescale / (10**9)
                
                # Finally, use this timescale to obtain the linear regression:
                lin_reg = stats.linregress(int_timescale, y = y)
            
            else:
                # Obtain the linear regression object directly from x. Since x is not a
                # datetime object, we can calculate the regression directly on it:
                lin_reg = stats.linregress(x, y = y)
                
            # Retrieve the equation as a string.
            # Access the attributes intercept and slope from the lin_reg object:
            lin_reg_equation = "y = %.2f*x + %.2f" %((lin_reg).slope, (lin_reg).intercept)
            # .2f: float with only two decimals
                
            # Retrieve R2 (coefficient of correlation) also as a string
            r2_lin_reg = "R²_lin_reg = %.4f" %(((lin_reg).rvalue) ** 2)
            # .4f: 4 decimals. ((lin_reg).rvalue) is the coefficient R. We
            # raise it to the second power by doing **2, where ** is the potentiation.
                
            # Add these two strings to the dictionary
            dictionary['lin_reg_equation'] = lin_reg_equation
            dictionary['r2_lin_reg'] = r2_lin_reg
                
            # Now, as final step, let's apply the values x to the linear regression
            # equation to obtain the predicted series used to plot the straight line.
                
            # The lists cannot perform vector operations like element-wise sum or product, 
            # but numpy arrays can. For example, [1, 2] + 1 would be interpreted as the try
            # for concatenation of two lists, resulting in error. But, np.array([1, 2]) + 1
            # is allowed, resulting in: np.array[2, 3].
            # This and the fact that Scipy and Matplotlib are built on NumPy were the reasons
            # why we converted every list to numpy arrays.
            
            # Save the predicted values as the array y_pred_lin_reg.
            # Access the attributes intercept and slope from the lin_reg object.
            # The equation is y = (slope * x) + intercept
            
            # Notice that again we cannot apply the equation directly to a timestamp.
            # So once again we will apply the integer scale to obtain the predictions
            # if we are dealing with datetime objects:
            if (x_is_datetime):
                y_pred_lin_reg = ((lin_reg).intercept) + ((lin_reg).slope) * (int_timescale)
            
            else:
                # x is not a timestamp, so we can directly apply it to the regression
                # equation:
                y_pred_lin_reg = ((lin_reg).intercept) + ((lin_reg).slope) * (x)
            
            # Add this array to the dictionary with the key 'y_pred_lin_reg':
            dictionary['y_pred_lin_reg'] = y_pred_lin_reg
            
            if (x_is_datetime):
            
                print("For performing the linear regression, a sequence of floats proportional to the timestamps was created. In this sequence, check on the returned object a dictionary containing the timestamps and the correspondent integers, that keeps the distance proportion between successive timestamps. The sequence was created by calculating the timedeltas as an integer number of nanoseconds, which were converted to seconds. The first timestamp was considered time = 0.")
                print("Notice that the regression equation is based on the use of this sequence of floats as X.\n")
                
                dictionary['warning'] = "x is a numeric scale that was obtained from datetimes, preserving the distance relationships. It was obtained for allowing the polynomial fitting."
                dictionary['numeric_to_datetime_correlation'] = {
                    
                    'x = 0': x[0],
                    f'x = {max(int_timescale)}': x[(len(x) - 1)]
                    
                }
                
                dictionary['sequence_of_floats_correspondent_to_timestamps'] = {
                                                                                'original_timestamps': x,
                                                                                'sequence_of_floats': int_timescale
                                                                                }
                
            # Finally, append this dictionary to list support_list:
            list_of_dictionaries_with_series_and_predictions.append(dictionary)
        
        print("Returning a list of dictionaries. Each one contains the arrays of valid series and labels, and the equations, R² and values predicted by the linear regressions.\n")
        
        # Now we finished the loop, list_of_dictionaries_with_series_and_predictions 
        # contains all series converted to NumPy arrays, with timestamps parsed as datetimes, 
        # and all the information regarding the linear regression, including the predicted 
        # values for plotting.
        # This list will be the object returned at the end of the function. Since it is an
        # JSON-formatted list, we can use the function json_obj_to_pandas_dataframe to convert
        # it to a Pandas dataframe.
        
        
        # Now, we can plot the figure.
        # we set alpha = 0.95 (opacity) to give a degree of transparency (5%), 
        # so that one series do not completely block the visualization of the other.
        
        # Let's retrieve the list of Matplotlib CSS colors:
        css4 = mcolors.CSS4_COLORS
        # css4 is a dictionary of colors: {'aliceblue': '#F0F8FF', 'antiquewhite': '#FAEBD7', ...}
        # Each key of this dictionary is a color name to be passed as argument color on the plot
        # function. So let's retrieve the array of keys, and use the list attribute to convert this
        # array to a list of colors:
        list_of_colors = list(css4.keys())
        
        # In 11 May 2022, this list of colors had 148 different elements
        # Since this list is in alphabetic order, let's create a random order for the colors.
        
        # Function random.sample(input_sequence, number_of_samples): 
        # this function creates a list containing a total of elements equals to the parameter 
        # "number_of_samples", which must be an integer.
        # This list is obtained by ramdomly selecting a total of "number_of_samples" elements from the
        # list "input_sequence" passed as parameter.
        
        # Function random.choices(input_sequence, k = number_of_samples):
        # similarly, randomly select k elements from the sequence input_sequence. This function is
        # newer than random.sample
        # Since we want to simply randomly sort the sequence, we can pass k = len(input_sequence)
        # to obtain the randomly sorted sequence:
        list_of_colors = random.choices(list_of_colors, k = len(list_of_colors))
        # Now, we have a random list of colors to use for plotting the charts
        
        if (add_splines_lines == True):
            LINE_STYLE = '-'

        else:
            LINE_STYLE = ''
        
        # Matplotlib linestyle:
        # https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html?msclkid=68737f24d16011eca9e9c4b41313f1ad
        
        if (plot_title is None):
            # Set graphic title
            plot_title = f"Y_x_X"

        if (horizontal_axis_title is None):
            # Set horizontal axis title
            horizontal_axis_title = "X"

        if (vertical_axis_title is None):
            # Set vertical axis title
            vertical_axis_title = "Y"
        
        # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
        # so that the bars do not completely block other views.
        OPACITY = 0.95
        
        #Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
        fig = plt.figure(figsize = (12, 8))
        ax = fig.add_subplot()

        i = 0 # Restart counting for the loop of colors
        
        # Loop through each dictionary from list_of_dictionaries_with_series_and_predictions:
        for dictionary in list_of_dictionaries_with_series_and_predictions:
            
            # Try selecting a color from list_of_colors:
            try:
                
                COLOR = list_of_colors[i]
                # Go to the next element i, so that the next plot will use a different color:
                i = i + 1
            
            except IndexError:
                
                # This error will be raised if list index is out of range, 
                # i.e. if i >= len(list_of_colors) - we used all colors from the list (at least 148).
                # So, return the index to zero to restart the colors from the beginning:
                i = 0
                COLOR = list_of_colors[i]
                i = i + 1
            
            # Access the arrays and label from the dictionary:
            X = dictionary['x']
            Y = dictionary['y']
            LABEL = dictionary['lab']
            
            # Scatter plot:
            ax.plot(X, Y, linestyle = LINE_STYLE, marker = "o", color = COLOR, alpha = OPACITY, label = LABEL)
            # Axes.plot documentation:
            # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html?msclkid=42bc92c1d13511eca8634a2c93ab89b5
            
            # x and y are positional arguments: they are specified by their position in function
            # call, not by an argument name like 'marker'.
            
            # Matplotlib markers:
            # https://matplotlib.org/stable/api/markers_api.html?msclkid=36c5eec5d16011ec9583a5777dc39d1f
            
            if (show_linear_reg == True):
                
                # Plot the linear regression using the same color.
                # Access the array of fitted Y's in the dictionary:
                Y_PRED = dictionary['y_pred_lin_reg']
                Y_PRED_LABEL = 'lin_reg_' + str(LABEL) # for the case where label is numeric
                
                ax.plot(X, Y_PRED,  linestyle = '-', marker = '', color = COLOR, alpha = OPACITY, label = Y_PRED_LABEL)

        # Now we finished plotting all of the series, we can set the general configuration:
        
        #ROTATE X AXIS IN XX DEGREES
        plt.xticks(rotation = x_axis_rotation)
        # XX = 0 DEGREES x_axis (Default)
        #ROTATE Y AXIS IN XX DEGREES:
        plt.yticks(rotation = y_axis_rotation)
        # XX = 0 DEGREES y_axis (Default)
        
        ax.set_title(plot_title)
        ax.set_xlabel(horizontal_axis_title)
        ax.set_ylabel(vertical_axis_title)

        ax.grid(grid) # show grid or not
        ax.legend(loc = 'upper left')
        # position options: 'upper right'; 'upper left'; 'lower left'; 'lower right';
        # 'right', 'center left'; 'center right'; 'lower center'; 'upper center', 'center'
        # https://www.statology.org/matplotlib-legend-position/

        if (export_png == True):
            # Image will be exported
            import os

            #check if the user defined a directory path. If not, set as the default root path:
            if (directory_to_save is None):
                #set as the default
                directory_to_save = ""

            #check if the user defined a file name. If not, set as the default name for this
            # function.
            if (file_name is None):
                #set as the default
                file_name = "scatter_plot_lin_reg"

            #check if the user defined an image resolution. If not, set as the default 110 dpi
            # resolution.
            if (png_resolution_dpi is None):
                #set as 330 dpi
                png_resolution_dpi = 330

            #Get the new_file_path
            new_file_path = os.path.join(directory_to_save, file_name)

            #Export the file to this new path:
            # The extension will be automatically added by the savefig method:
            plt.savefig(new_file_path, dpi = png_resolution_dpi, quality = 100, format = 'png', transparent = False) 
            #quality could be set from 1 to 100, where 100 is the best quality
            #format (str, supported formats) = 'png', 'pdf', 'ps', 'eps' or 'svg'
            #transparent = True or False
            # For other parameters of .savefig method, check https://indianaiproduction.com/matplotlib-savefig/
            print (f"Figure exported as \'{new_file_path}.png\'. Any previous file in this root path was overwritten.")

        #fig.tight_layout()

        ## Show an image read from an image file:
        ## import matplotlib.image as pltimg
        ## img=pltimg.imread('mydecisiontree.png')
        ## imgplot = plt.imshow(img)
        ## See linkedIn Learning course: "Supervised machine learning and the technology boom",
        ##  Ex_Files_Supervised_Learning, Exercise Files, lesson '03. Decision Trees', '03_05', 
        ##  '03_05_END.ipynb'
        plt.show()
        
        if (show_linear_reg == True):
            
            try:
                # only works in Jupyter Notebook:
                from IPython.display import display
            except:
                pass
            
            print("\nLinear regression summaries (equations and R²):\n")
            
            for dictionary in list_of_dictionaries_with_series_and_predictions:
                
                print(f"Linear regression summary for {dictionary['lab']}:\n")
                
                try:
                    display(dictionary['lin_reg_equation'])
                    display(dictionary['r2_lin_reg'])

                except: # regular mode                  
                    print(dictionary['lin_reg_equation'])
                    print(dictionary['r2_lin_reg'])
                
                print("\n")
        
        
        return list_of_dictionaries_with_series_and_predictions


def polynomial_fit (data_in_same_column = False, df = None, column_with_predict_var_x = None, column_with_response_var_y = None, column_with_labels = None, list_of_dictionaries_with_series_to_analyze = [{'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}], polynomial_degree = 6, calculate_roots = False, calculate_derivative = False, calculate_integral = False, x_axis_rotation = 70, y_axis_rotation = 0, show_polynomial_reg = True, grid = True, add_splines_lines = False, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    polynomial_fit (data_in_same_column = False, df = None, column_with_predict_var_x = None, column_with_response_var_y = None, column_with_labels = None, list_of_dictionaries_with_series_to_analyze = [{'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}], polynomial_degree = 6, calculate_roots = False, calculate_derivative = False, calculate_integral = False, x_axis_rotation = 70, y_axis_rotation = 0, show_polynomial_reg = True, grid = True, add_splines_lines = False, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    Check numpy.polynomial class API documentation for other polynomials 
     (chebyshev, legendre, hermite, etc):
     https://numpy.org/doc/stable/reference/routines.polynomials.package.html#module-numpy.polynomial
    
    : param: df: the whole dataframe to be processed.
    
    : param: data_in_same_column = False: set as True if all the values to plot are in a same column.
      If data_in_same_column = True, you must specify the dataframe containing the data as df;
      the column containing the predict variable (X) as column_with_predict_var_x; the column 
      containing the responses to plot (Y) as column_with_response_var_y; and the column 
      containing the labels (subgroup) indication as column_with_labels. 
      df is an object, so do not declare it in quotes. The other three arguments (columns' names) 
      are strings, so declare in quotes. 
    
      Example: suppose you have a dataframe saved as dataset, and two groups A and B to compare. 
      All the results for both groups are in a column named 'results', wich will be plot against
      the time, saved as 'time' (X = 'time'; Y = 'results'). If the result is for
      an entry from group A, then a column named 'group' has the value 'A'. If it is for group B,
      column 'group' shows the value 'B'. In this example:
      data_in_same_column = True,
      df = dataset,
    
    : param: column_with_predict_var_x = 'time',
    : param: column_with_response_var_y = 'results', 
    : param: column_with_labels = 'group'
      If you want to declare a list of dictionaries, keep data_in_same_column = False and keep
      df = None (the other arguments may be set as None, but it is not mandatory: 
      column_with_predict_var_x = None, column_with_response_var_y = None, column_with_labels = None).
    
    Parameter to input when DATA_IN_SAME_COLUMN = False:
    : param: list_of_dictionaries_with_series_to_analyze: if data is already converted to series, lists
      or arrays, provide them as a list of dictionaries. It must be declared as a list, in brackets,
      even if there is a single dictionary.
      Use always the same keys: 'x' for the X-series (predict variables); 'y' for the Y-series
      (response variables); and 'lab' for the labels. If you do not want to declare a series, simply
      keep as None, but do not remove or rename a key (ALWAYS USE THE KEYS SHOWN AS MODEL).
      If you want, you can remove elements (dictionaries) from the list to declare fewer elements;
      and you can also add more elements (dictionaries) to the lists, if you need to plot more series.
      Simply put a comma after the last element from the list and declare a new dictionary, keeping the
      same keys: {'x': x_series, 'y': y_series, 'lab': label}, where x_series, y_series and label
      represents the series and label of the added dictionary (you can pass 'lab': None, but if 
      'x' or 'y' are None, the new dictionary will be ignored).
    
      Examples:
      list_of_dictionaries_with_series_to_analyze = 
      [{'x': DATASET['X'], 'y': DATASET['Y'], 'lab': 'label'}]
      will plot a single variable. In turns:
      list_of_dictionaries_with_series_to_analyze = 
      [{'x': DATASET['X'], 'y': DATASET['Y1'], 'lab': 'label'}, {'x': DATASET['X'], 'y': DATASET['Y2'], 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}]
      will plot two series, Y1 x X and Y2 x X.
      Notice that all dictionaries where 'x' or 'y' are None are automatically ignored.
      If None is provided to 'lab', an automatic label will be generated.
    
    : param: polynomial_degree = integer value representing the degree of the fitted polynomial.
    
    : param: calculate_derivative = False. Alternatively, set as True to calculate the derivative of the
       fitted polynomial and add it as a column of the dataframe.
    
    : param: calculate_integral = False. Alternatively, set as True to calculate the integral of the
       fitted polynomial and add it as a column of the dataframe.
    
    : param: calculate_roots = False.  Alternatively, set as True to calculate the roots of the
       fitted polynomial and return them as a NumPy array.
    """

    import random
    # Python Random documentation:
    # https://docs.python.org/3/library/random.html?msclkid=9d0c34b2d13111ec9cfa8ddaee9f61a1
    from numpy.polynomial.polynomial import Polynomial
    import matplotlib.colors as mcolors
    

    # List the possible numeric data types for a Pandas dataframe column:
    numeric_dtypes = [np.int16, np.int32, np.int64, np.float16, np.float32, np.float64]
    
    if (data_in_same_column == True):
        
        if (df is None):
            
            print("Please, input a valid dataframe as df.\n")
            list_of_dictionaries_with_series_to_analyze = []
            # The code will check the size of this list on the next block.
            # If it is zero, code is simply interrupted.
            # Instead of returning an error, we use this code structure that can be applied
            # on other graphic functions that do not return a summary (and so we should not
            # return a value like 'error' to interrupt the function).
        
        elif (column_with_predict_var_x is None):
            
            print("Please, input a valid column name as column_with_predict_var_x.\n")
            list_of_dictionaries_with_series_to_analyze = []
        
        elif (column_with_response_var_y is None):
            
            print("Please, input a valid column name as column_with_response_var_y.\n")
            list_of_dictionaries_with_series_to_analyze = []
        
        else:
            
            # set a local copy of the dataframe:
            DATASET = df.copy(deep = True)
            
            if (column_with_labels is None):
            
                print("Using the whole series (column) for correlation.\n")
                column_with_labels = 'whole_series_' + column_with_response_var_y
                DATASET[column_with_labels] = column_with_labels
            
            # sort DATASET; by column_with_predict_var_x; by column column_with_labels
            # and by column_with_response_var_y, all in Ascending order
            # Since we sort by label (group), it is easier to separate the groups.
            DATASET = DATASET.sort_values(by = [column_with_predict_var_x, column_with_labels, column_with_response_var_y], ascending = [True, True, True])
            
            # Reset indices:
            DATASET = DATASET.reset_index(drop = True)
            
            # If column_with_predict_var_x is an object, the user may be trying to pass a date as x. 
            # So, let's try to convert it to datetime:
            if ((DATASET[column_with_predict_var_x]).dtype not in numeric_dtypes):
                
                try:
                    DATASET[column_with_predict_var_x] = (DATASET[column_with_predict_var_x]).astype('datetime64[ns]')
                    print("Variable X successfully converted to datetime64[ns].\n")
                    
                except:
                    # Simply ignore it
                    pass
            
            # Get a series of unique values of the labels, and save it as a list using the
            # list attribute:
            unique_labels = list(DATASET[column_with_labels].unique())
            print(f"{len(unique_labels)} different labels detected: {unique_labels}.\n")
            
            # Start a list to store the dictionaries containing the keys:
            # 'x': list of predict variables; 'y': list of responses; 'lab': the label (group)
            list_of_dictionaries_with_series_to_analyze = []
            
            # Loop through each possible label:
            for lab in unique_labels:
                # loop through each element from the list unique_labels, referred as lab
                
                # Set a filter for the dataset, to select only rows correspondent to that
                # label:
                boolean_filter = (DATASET[column_with_labels] == lab)
                
                # Create a copy of the dataset, with entries selected by that filter:
                ds_copy = (DATASET[boolean_filter]).copy(deep = True)
                # Sort again by X and Y, to guarantee the results are in order:
                ds_copy = ds_copy.sort_values(by = [column_with_predict_var_x, column_with_response_var_y], ascending = [True, True])
                # Restart the index of the copy:
                ds_copy = ds_copy.reset_index(drop = True)
                
                # Re-extract the X and Y series and convert them to NumPy arrays 
                # (these arrays will be important later in the function):
                x = np.array(ds_copy[column_with_predict_var_x])
                y = np.array(ds_copy[column_with_response_var_y])
            
                # Then, create the dictionary:
                dict_of_values = {'x': x, 'y': y, 'lab': lab}
                
                # Now, append dict_of_values to list_of_dictionaries_with_series_to_analyze:
                list_of_dictionaries_with_series_to_analyze.append(dict_of_values)
                
            # Now, we have a list of dictionaries with the same format of the input list.
            
    else:
        
        # The user input a list_of_dictionaries_with_series_to_analyze
        # Create a support list:
        support_list = []
        
        # Loop through each element on the list list_of_dictionaries_with_series_to_analyze:
        
        for i in range (0, len(list_of_dictionaries_with_series_to_analyze)):
            # from i = 0 to i = len(list_of_dictionaries_with_series_to_analyze) - 1, index of the
            # last element from the list
            
            # pick the i-th dictionary from the list:
            dictionary = list_of_dictionaries_with_series_to_analyze[i]
            
            # access 'x', 'y', and 'lab' keys from the dictionary:
            x = dictionary['x']
            y = dictionary['y']
            lab = dictionary['lab']
            # Remember that all this variables are series from a dataframe, so we can apply
            # the astype function:
            # https://www.askpython.com/python/built-in-methods/python-astype?msclkid=8f3de8afd0d411ec86a9c1a1e290f37c
            
            # check if at least x and y are not None:
            if ((x is not None) & (y is not None)):
                
                # If column_with_predict_var_x is an object, the user may be trying to pass a date as x. 
                # So, let's try to convert it to datetime:
                
                if (x.dtype not in numeric_dtypes):

                    try:
                        x = (x).astype('datetime64[ns]')
                        x_is_datetime = True
                        print(f"Variable X from {i}-th dictionary successfully converted to datetime64[ns].\n")

                    except:
                        # Simply ignore it
                        pass
                
                # Possibly, x and y are not ordered. Firstly, let's merge them into a temporary
                # dataframe to be able to order them together.
                # Use the 'list' attribute to guarantee that x and y were read as lists. These lists
                # are the values for a dictionary passed as argument for the constructor of the
                # temporary dataframe. When using the list attribute, we make the series independent
                # from its origin, even if it was created from a Pandas dataframe. Then, we have a
                # completely independent dataframe that may be manipulated and sorted, without worrying
                # that it may modify its origin:
                
                temp_df = pd.DataFrame(data = {'x': list(x), 'y': list(y)})
                # sort this dataframe by 'x' and 'y':
                temp_df = temp_df.sort_values(by = ['x', 'y'], ascending = [True, True])
                # restart index:
                temp_df = temp_df.reset_index(drop = True)
                
                # Re-extract the X and Y series and convert them to NumPy arrays 
                # (these arrays will be important later in the function):
                x = np.array(temp_df['x'])
                y = np.array(temp_df['y'])
                
                # check if lab is None:
                if (lab is None):
                    # input a default label.
                    # Use the str attribute to convert the integer to string, allowing it
                    # to be concatenated
                    lab = "X" + str(i) + "_x_" + "Y" + str(i)
                    
                # Then, create the dictionary:
                dict_of_values = {'x': x, 'y': y, 'lab': lab}
                
                # Now, append dict_of_values to support list:
                support_list.append(dict_of_values)
            
        # Now, support_list contains only the dictionaries with valid entries, as well
        # as labels for each collection of data. The values are independent from their origin,
        # and now they are ordered and in the same format of the data extracted directly from
        # the dataframe.
        # So, make the list_of_dictionaries_with_series_to_analyze the support_list itself:
        list_of_dictionaries_with_series_to_analyze = support_list
        print(f"{len(list_of_dictionaries_with_series_to_analyze)} valid series input.\n")

        
    # Now that both methods of input resulted in the same format of list, we can process both
    # with the same code.
    
    # Each dictionary in list_of_dictionaries_with_series_to_analyze represents a series to
    # plot. So, the total of series to plot is:
    total_of_series = len(list_of_dictionaries_with_series_to_analyze)
            
    if (total_of_series <= 0):
        
        raise InvalidInputsError ("No valid series to fit. Please, provide valid arguments.\n")
    
    else:
        
        # Continue to plotting and calculating the fitting.
        # Notice that we sorted the all the lists after they were separated and before
        # adding them to dictionaries. Also, the timestamps were converted to datetime64 variables
        
        # Now we pre-processed the data, we can obtain a final list of dictionaries, containing
        # the linear regression information (it will be plotted only if the user asked to). Start
        # a list to store all predictions:
        list_of_dictionaries_with_series_and_predictions = []
        
        # Loop through each dictionary (element) on the list list_of_dictionaries_with_series_to_analyze:
        for dictionary in list_of_dictionaries_with_series_to_analyze:
            
            x_is_datetime = False
            # boolean that will map if x is a datetime or not. Only change to True when it is.
            
            # Access keys 'x' and 'y' to retrieve the arrays.
            x = dictionary['x']
            y = dictionary['y']
            lab = dictionary['lab']
            
            # Check if the elements from array x are np.datetime64 objects. Pick the first
            # element to check:
            
            if (type(np.array(x)[0]) == np.datetime64):
                
                x_is_datetime = True
            
            if (x_is_datetime):
                # In this case, performing the linear regression directly in X will
                # return an error. We must associate a sequential number to each time.
                # to keep the distance between these integers the same as in the original sequence
                # let's define a difference of 1 ns as 1. The 1st timestamp will be zero, and the
                # addition of 1 ns will be an addition of 1 unit. So a timestamp recorded 10 ns
                # after the time zero will have value 10. At the end, we divide every element by
                # 10**9, to obtain the correspondent distance in seconds.
                
                # start a list for the associated integer timescale. Put the number zero,
                # associated to the first timestamp:
                int_timescale = [0]
                
                # loop through each element of the array x, starting from index 1:
                for i in range(1, len(x)):
                    
                    # calculate the timedelta between x[i] and x[i-1]:
                    # The delta method from the Timedelta class converts the timedelta to
                    # nanoseconds, guaranteeing the internal compatibility:
                    # The .delta attribute was replaced by .value attribute. 
                    # Both return the number of nanoseconds as an integer.
                    # https://pandas.pydata.org/docs/reference/api/pandas.Timedelta.html
                    timedelta = pd.Timedelta(x[i] - x[(i-1)]).value
                    
                    # Sum this timedelta (integer number of nanoseconds) to the
                    # previous element from int_timescale, and append the result to the list:
                    int_timescale.append((timedelta + int_timescale[(i-1)]))
                
                # Now convert the new scale (that preserves the distance between timestamps)
                # to NumPy array:
                int_timescale = np.array(int_timescale)
                
                # Divide by 10**9 to obtain the distances in seconds, reducing the order of
                # magnitude of the integer numbers (the division is allowed for arrays)
                int_timescale = int_timescale / (10**9)
                
                # Finally, use this timescale to obtain the polynomial fit;
                # Use the method .fit, passing X, Y, and degree as coefficients
                # to fit the polynomial to data:
                # Perform the least squares fit to data:
                #create an instance (object) named 'pol' from the class Polynomial:
                fitted_pol = Polynomial.fit(int_timescale, y, deg = polynomial_degree, full = False)
                
            
            else:
                # Obtain the polynomial fitting object directly from x. Since x is not a
                # datetime object, we can calculate the regression directly on it:
                fitted_pol = Polynomial.fit(x, y, deg = polynomial_degree, full = False)

            # when full = True, the [resid, rank, sv, rcond] list is returned
            # check: https://numpy.org/doc/stable/reference/generated/numpy.polynomial.polynomial.Polynomial.fit.html#numpy.polynomial.polynomial.Polynomial.fit

            # This method returned a series named 'fitted_pol', with the values of Y predicted by the
            # polynomial fitting. Now add it to the dictionary as fitted_polynomial_series:
            dictionary['fitted_polynomial'] = fitted_pol
            print(f"{polynomial_degree} degree polynomial successfully fitted to data using the least squares method. The fitting Y ({lab}) values were added to the dataframe as the column \'fitted_polynomial\'.")    
            
            # Get the polynomial coefficients array:
            if (x_is_datetime):
                coeff_array = Polynomial.fit(int_timescale, y, deg = polynomial_degree, full = False).coef
            
            else:
                coeff_array = Polynomial.fit(x, y, deg = polynomial_degree, full = False).coef
            
            # Create a coefficient dictionary:
            coeff_dict = {}
            # Loop through each element from the array, and append it to the dictionary:
            full_polynomial_format = "a0"
            
            for i in range(1, len(coeff_array)):
                
                    full_polynomial_format = full_polynomial_format + " + a" + str(i) + "*x" + str(i)
            
            coeff_dict['full_polynomial_format'] = full_polynomial_format
            
            for i in range(0, len(coeff_array)):
                
                # Create a key for the element i:
                dict_key = "a" + str(i)
                # Store the correspondent element on the array:
                coeff_dict[dict_key] = coeff_array[i]
            
            if (x_is_datetime):
                
                coeff_dict['warning'] = "x is a numeric scale that was obtained from datetimes, preserving the distance relationships. It was obtained for allowing the polynomial fitting."
                coeff_dict['numeric_to_datetime_correlation'] = {
                    
                    'x = 0': x[0],
                    f'x = {max(int_timescale)}': x[(len(x) - 1)]
                    
                }
                
                coeff_dict['sequence_of_floats_correspondent_to_timestamps'] = {
                                                                                'original_timestamps': x,
                                                                                'sequence_of_floats': int_timescale
                                                                                }
            
            print("Polynomial summary:\n")
            print(f"Polynomial format = {full_polynomial_format}\n")
            print("Polynomial coefficients:")
            
            for i in range(0, len(coeff_array)):
                print(f"{str('a') + str(i)} = {coeff_array[i]}")
            
            print(f"Fitted polynomial = {dictionary['fitted_polynomial']}")
            print("\n")
            
            if (x_is_datetime):
                print(coeff_dict['warning'])
                print(coeff_dict['numeric_to_datetime_correlation'])
                print("\n")
            
            # Add it to the main dictionary:
            dictionary['fitted_polynomial_coefficients'] = coeff_dict
            
            # Now, calculate the fitted series. Start a Pandas series as a copy from y:
            fitted_series = y.copy()
            # Make it zero:
            fitted_series = 0
            
            # Now loop through the polynomial coefficients: ai*(x**i):
            for i in range(0, len(coeff_array)):
                
                if (x_is_datetime):
                    
                    fitted_series = (coeff_array[i])*(int_timescale**(i))
                
                else:
                    fitted_series = (coeff_array[i])*(x**(i))
            
            # Add the series to the dictionary:
            dictionary['fitted_polynomial_series'] = fitted_series
            
            
            if (calculate_derivative == True):
        
                # Calculate the derivative of the polynomial:
                if (x_is_datetime):
                    pol_deriv = Polynomial.fit(int_timescale, y, deg = polynomial_degree, full = False).deriv(m = 1)
                
                else:
                    pol_deriv = Polynomial.fit(x, y, deg = polynomial_degree, full = False).deriv(m = 1)
                # m (integer): order of the derivative. If m = 2, the second order is returned.
                # This method returns a series. Check:
                # https://numpy.org/doc/stable/reference/generated/numpy.polynomial.polynomial.Polynomial.deriv.html#numpy.polynomial.polynomial.Polynomial.deriv

                #Add pol_deriv series as a new key from the dictionary:
                dictionary['fitted_polynomial_derivative'] = pol_deriv
                print("1st Order derivative of the polynomial successfully calculated and added to the dictionary as the key \'fitted_polynomial_derivative\'.\n")

            if (calculate_integral == True):

                # Calculate the integral of the polynomial:
                if (x_is_datetime):
                    pol_integral = Polynomial.fit(int_timescale, y, deg = polynomial_degree, full = False).integ(m = 1)
                
                else:
                    pol_integral = Polynomial.fit(x, y, deg = polynomial_degree, full = False).integ(m = 1)
                # m (integer): The number of integrations to perform.
                # This method returns a series. Check:
                # https://numpy.org/doc/stable/reference/generated/numpy.polynomial.polynomial.Polynomial.integ.html#numpy.polynomial.polynomial.Polynomial.integ

                #Add pol_deriv series as a new key from the dictionary:
                dictionary['fitted_polynomial_integral'] = pol_integral
                print("Integral of the polynomial successfully calculated and added to the dictionary as the key \'fitted_polynomial_integral\'.\n")

            if (calculate_roots == True):

                # Calculate the roots of the polynomial:
                if (x_is_datetime):
                    roots_array = Polynomial.fit(int_timescale, y, deg = polynomial_degree, full = False).roots()
                
                else:
                    roots_array = Polynomial.fit(x, y, deg = polynomial_degree, full = False).roots()
                # This method returns an array with the polynomial roots. Check:
                # https://numpy.org/doc/stable/reference/generated/numpy.polynomial.polynomial.Polynomial.roots.html#numpy.polynomial.polynomial.Polynomial.roots

                #Add it as the key polynomial_roots:
                dictionary['polynomial_roots'] = roots_array
                print(f"Roots of the polynomial: {roots_array}.\n")
                print("Roots added to the dictionary as the key \'polynomial_roots\'.\n")

            # Finally, append this dictionary to list support_list:
            list_of_dictionaries_with_series_and_predictions.append(dictionary)
        
        print("Returning a list of dictionaries. Each one contains the arrays of valid series and labels, as well as the regression statistics obtained.\n")
        
        # Now we finished the loop, list_of_dictionaries_with_series_and_predictions 
        # contains all series converted to NumPy arrays, with timestamps parsed as datetimes, 
        # and all the information regarding the linear regression, including the predicted 
        # values for plotting.
        # This list will be the object returned at the end of the function. Since it is an
        # JSON-formatted list, we can use the function json_obj_to_pandas_dataframe to convert
        # it to a Pandas dataframe.
        
        # Now, we can plot the figure.
        # we set alpha = 0.95 (opacity) to give a degree of transparency (5%), 
        # so that one series do not completely block the visualization of the other.
        
        # Let's retrieve the list of Matplotlib CSS colors:
        css4 = mcolors.CSS4_COLORS
        # css4 is a dictionary of colors: {'aliceblue': '#F0F8FF', 'antiquewhite': '#FAEBD7', ...}
        # Each key of this dictionary is a color name to be passed as argument color on the plot
        # function. So let's retrieve the array of keys, and use the list attribute to convert this
        # array to a list of colors:
        list_of_colors = list(css4.keys())
        
        # In 11 May 2022, this list of colors had 148 different elements
        # Since this list is in alphabetic order, let's create a random order for the colors.
        
        # Function random.sample(input_sequence, number_of_samples): 
        # this function creates a list containing a total of elements equals to the parameter 
        # "number_of_samples", which must be an integer.
        # This list is obtained by ramdomly selecting a total of "number_of_samples" elements from the
        # list "input_sequence" passed as parameter.
        
        # Function random.choices(input_sequence, k = number_of_samples):
        # similarly, randomly select k elements from the sequence input_sequence. This function is
        # newer than random.sample
        # Since we want to simply randomly sort the sequence, we can pass k = len(input_sequence)
        # to obtain the randomly sorted sequence:
        list_of_colors = random.choices(list_of_colors, k = len(list_of_colors))
        # Now, we have a random list of colors to use for plotting the charts
        
        if (add_splines_lines == True):
            LINE_STYLE = '-'

        else:
            LINE_STYLE = ''
        
        # Matplotlib linestyle:
        # https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html?msclkid=68737f24d16011eca9e9c4b41313f1ad
        
        if (plot_title is None):
            # Set graphic title
            plot_title = f"Y_x_X"

        if (horizontal_axis_title is None):
            # Set horizontal axis title
            horizontal_axis_title = "X"

        if (vertical_axis_title is None):
            # Set vertical axis title
            vertical_axis_title = "Y"
        
        # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
        # so that the bars do not completely block other views.
        OPACITY = 0.95
        
        #Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
        fig = plt.figure(figsize = (12, 8))
        ax = fig.add_subplot()

        i = 0 # Restart counting for the loop of colors
        
        # Loop through each dictionary from list_of_dictionaries_with_series_and_predictions:
        for dictionary in list_of_dictionaries_with_series_and_predictions:
            
            # Try selecting a color from list_of_colors:
            try:
                
                COLOR = list_of_colors[i]
                # Go to the next element i, so that the next plot will use a different color:
                i = i + 1
            
            except IndexError:
                
                # This error will be raised if list index is out of range, 
                # i.e. if i >= len(list_of_colors) - we used all colors from the list (at least 148).
                # So, return the index to zero to restart the colors from the beginning:
                i = 0
                COLOR = list_of_colors[i]
                i = i + 1
            
            # Access the arrays and label from the dictionary:
            X = dictionary['x']
            Y = dictionary['y']
            LABEL = dictionary['lab']
            
            # Scatter plot:
            ax.plot(X, Y, linestyle = LINE_STYLE, marker = "o", color = COLOR, alpha = OPACITY, label = LABEL)
            # Axes.plot documentation:
            # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html?msclkid=42bc92c1d13511eca8634a2c93ab89b5
            
            # x and y are positional arguments: they are specified by their position in function
            # call, not by an argument name like 'marker'.
            
            # Matplotlib markers:
            # https://matplotlib.org/stable/api/markers_api.html?msclkid=36c5eec5d16011ec9583a5777dc39d1f
            
            if (show_polynomial_reg == True):
                
                # Plot the linear regression using the same color.
                # Access the array of fitted Y's in the dictionary:
                Y_PRED = dictionary['fitted_polynomial_series']
                Y_PRED_LABEL = 'fitted_pol_' + str(LABEL) # for the case where label is numeric
                
                ax.plot(X, Y_PRED,  linestyle = '-', marker = '', color = COLOR, alpha = OPACITY, label = Y_PRED_LABEL)

        # Now we finished plotting all of the series, we can set the general configuration:
        
        #ROTATE X AXIS IN XX DEGREES
        plt.xticks(rotation = x_axis_rotation)
        # XX = 0 DEGREES x_axis (Default)
        #ROTATE Y AXIS IN XX DEGREES:
        plt.yticks(rotation = y_axis_rotation)
        # XX = 0 DEGREES y_axis (Default)
        
        ax.set_title(plot_title)
        ax.set_xlabel(horizontal_axis_title)
        ax.set_ylabel(vertical_axis_title)

        ax.grid(grid) # show grid or not
        ax.legend(loc = 'upper left')
        # position options: 'upper right'; 'upper left'; 'lower left'; 'lower right';
        # 'right', 'center left'; 'center right'; 'lower center'; 'upper center', 'center'
        # https://www.statology.org/matplotlib-legend-position/

        if (export_png == True):
            # Image will be exported
            import os

            #check if the user defined a directory path. If not, set as the default root path:
            if (directory_to_save is None):
                #set as the default
                directory_to_save = ""

            #check if the user defined a file name. If not, set as the default name for this
            # function.
            if (file_name is None):
                #set as the default
                file_name = "polynomial_fitting"

            #check if the user defined an image resolution. If not, set as the default 110 dpi
            # resolution.
            if (png_resolution_dpi is None):
                #set as 330 dpi
                png_resolution_dpi = 330

            #Get the new_file_path
            new_file_path = os.path.join(directory_to_save, file_name)

            #Export the file to this new path:
            # The extension will be automatically added by the savefig method:
            plt.savefig(new_file_path, dpi = png_resolution_dpi, quality = 100, format = 'png', transparent = False) 
            #quality could be set from 1 to 100, where 100 is the best quality
            #format (str, supported formats) = 'png', 'pdf', 'ps', 'eps' or 'svg'
            #transparent = True or False
            # For other parameters of .savefig method, check https://indianaiproduction.com/matplotlib-savefig/
            print (f"Figure exported as \'{new_file_path}.png\'. Any previous file in this root path was overwritten.")

        #fig.tight_layout()

        ## Show an image read from an image file:
        ## import matplotlib.image as pltimg
        ## img=pltimg.imread('mydecisiontree.png')
        ## imgplot = plt.imshow(img)
        ## See linkedIn Learning course: "Supervised machine learning and the technology boom",
        ##  Ex_Files_Supervised_Learning, Exercise Files, lesson '03. Decision Trees', '03_05', 
        ##  '03_05_END.ipynb'
        plt.show()
        
        return list_of_dictionaries_with_series_and_predictions


def time_series_vis (data_in_same_column = False, df = None, column_with_predict_var_x = None, column_with_response_var_y = None, column_with_labels = None, list_of_dictionaries_with_series_to_analyze = [{'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}], x_axis_rotation = 70, y_axis_rotation = 0, grid = True, add_splines_lines = True, add_scatter_dots = False, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    time_series_vis (data_in_same_column = False, df = None, column_with_predict_var_x = None, column_with_response_var_y = None, column_with_labels = None, list_of_dictionaries_with_series_to_analyze = [{'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}], x_axis_rotation = 70, y_axis_rotation = 0, grid = True, add_splines_lines = True, add_scatter_dots = False, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    matplotlib.colors documentation:
     https://matplotlib.org/3.5.0/api/colors_api.html?msclkid=94286fa9d12f11ec94660321f39bf47f
    
    Matplotlib list of colors:
     https://matplotlib.org/stable/gallery/color/named_colors.html?msclkid=0bb86abbd12e11ecbeb0a2439e5b0d23
    Matplotlib colors tutorial:
     https://matplotlib.org/stable/tutorials/colors/colors.html
    Matplotlib example of Python code using matplotlib.colors:
     https://matplotlib.org/stable/_downloads/0843ee646a32fc214e9f09328c0cd008/colors.py
    Same example as Jupyter Notebook:
     https://matplotlib.org/stable/_downloads/2a7b13c059456984288f5b84b4b73f45/colors.ipynb
    
        
    : param: data_in_same_column = False: set as True if all the values to plot are in a same column.
      If data_in_same_column = True, you must specify the dataframe containing the data as df;
      the column containing the predict variable (X) as column_with_predict_var_x; the column 
      containing the responses to plot (Y) as column_with_response_var_y; and the column 
      containing the labels (subgroup) indication as column_with_labels. 
    : param: df is an object, so do not declare it in quotes. The other three arguments (columns' names) 
      are strings, so declare in quotes. 
    
      Example: suppose you have a dataframe saved as dataset, and two groups A and B to compare. 
      All the results for both groups are in a column named 'results', wich will be plot against
      the time, saved as 'time' (X = 'time'; Y = 'results'). If the result is for
      an entry from group A, then a column named 'group' has the value 'A'. If it is for group B,
      column 'group' shows the value 'B'. In this example:
      data_in_same_column = True,
      df = dataset,
      column_with_predict_var_x = 'time',
      column_with_response_var_y = 'results', 
      column_with_labels = 'group'
      If you want to declare a list of dictionaries, keep data_in_same_column = False and keep
      df = None (the other arguments may be set as None, but it is not mandatory: 
      column_with_predict_var_x = None, column_with_response_var_y = None, column_with_labels = None).
    
    Parameter to input when DATA_IN_SAME_COLUMN = False:
    
    : param: list_of_dictionaries_with_series_to_analyze: if data is already converted to series, lists
      or arrays, provide them as a list of dictionaries. It must be declared as a list, in brackets,
      even if there is a single dictionary.
      Use always the same keys: 'x' for the X-series (predict variables); 'y' for the Y-series
      (response variables); and 'lab' for the labels. If you do not want to declare a series, simply
      keep as None, but do not remove or rename a key (ALWAYS USE THE KEYS SHOWN AS MODEL).
      If you want, you can remove elements (dictionaries) from the list to declare fewer elements;
      and you can also add more elements (dictionaries) to the lists, if you need to plot more series.
      Simply put a comma after the last element from the list and declare a new dictionary, keeping the
      same keys: {'x': x_series, 'y': y_series, 'lab': label}, where x_series, y_series and label
      represents the series and label of the added dictionary (you can pass 'lab': None, but if 
      'x' or 'y' are None, the new dictionary will be ignored).
    
      Examples:
      list_of_dictionaries_with_series_to_analyze = 
      [{'x': DATASET['X'], 'y': DATASET['Y'], 'lab': 'label'}]
      will plot a single variable. In turns:
      list_of_dictionaries_with_series_to_analyze = 
      [{'x': DATASET['X'], 'y': DATASET['Y1'], 'lab': 'label'}, {'x': DATASET['X'], 'y': DATASET['Y2'], 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}]
      will plot two series, Y1 x X and Y2 x X.
      Notice that all dictionaries where 'x' or 'y' are None are automatically ignored.
      If None is provided to 'lab', an automatic label will be generated.
    """

    import random
    # Python Random documentation:
    # https://docs.python.org/3/library/random.html?msclkid=9d0c34b2d13111ec9cfa8ddaee9f61a1
    import matplotlib.colors as mcolors
    

    # List the possible numeric data types for a Pandas dataframe column:
    numeric_dtypes = [np.int16, np.int32, np.int64, np.float16, np.float32, np.float64]
    
    if (data_in_same_column == True):
        
        print("Data to be plotted in a same column.\n")
        
        if (df is None):
            
            print("Please, input a valid dataframe as df.\n")
            list_of_dictionaries_with_series_to_analyze = []
            # The code will check the size of this list on the next block.
            # If it is zero, code is simply interrupted.
            # Instead of returning an error, we use this code structure that can be applied
            # on other graphic functions that do not return a summary (and so we should not
            # return a value like 'error' to interrupt the function).
        
        elif (column_with_predict_var_x is None):
            
            print("Please, input a valid column name as column_with_predict_var_x.\n")
            list_of_dictionaries_with_series_to_analyze = []
        
        elif (column_with_response_var_y is None):
            
            print("Please, input a valid column name as column_with_response_var_y.\n")
            list_of_dictionaries_with_series_to_analyze = []
        
        else:
            
            # set a local copy of the dataframe:
            DATASET = df.copy(deep = True)
            
            if (column_with_labels is None):
            
                print("Using the whole series (column) for correlation.\n")
                column_with_labels = 'whole_series_' + column_with_response_var_y
                DATASET[column_with_labels] = column_with_labels
            
            # sort DATASET; by column_with_predict_var_x; by column column_with_labels
            # and by column_with_response_var_y, all in Ascending order
            # Since we sort by label (group), it is easier to separate the groups.
            DATASET = DATASET.sort_values(by = [column_with_predict_var_x, column_with_labels, column_with_response_var_y], ascending = [True, True, True])
            
            # Reset indices:
            DATASET = DATASET.reset_index(drop = True)
            
            # If column_with_predict_var_x is an object, the user may be trying to pass a date as x. 
            # So, let's try to convert it to datetime:
            if ((DATASET[column_with_predict_var_x]).dtype not in numeric_dtypes):
                
                try:
                    DATASET[column_with_predict_var_x] = (DATASET[column_with_predict_var_x]).astype('datetime64[ns]')
                    print("Variable X successfully converted to datetime64[ns].\n")
                    
                except:
                    # Simply ignore it
                    pass
            
            # Get a series of unique values of the labels, and save it as a list using the
            # list attribute:
            unique_labels = list(DATASET[column_with_labels].unique())
            print(f"{len(unique_labels)} different labels detected: {unique_labels}.\n")
            
            # Start a list to store the dictionaries containing the keys:
            # 'x': list of predict variables; 'y': list of responses; 'lab': the label (group)
            list_of_dictionaries_with_series_to_analyze = []
            
            # Loop through each possible label:
            for lab in unique_labels:
                # loop through each element from the list unique_labels, referred as lab
                
                # Set a filter for the dataset, to select only rows correspondent to that
                # label:
                boolean_filter = (DATASET[column_with_labels] == lab)
                
                # Create a copy of the dataset, with entries selected by that filter:
                ds_copy = (DATASET[boolean_filter]).copy(deep = True)
                # Sort again by X and Y, to guarantee the results are in order:
                ds_copy = ds_copy.sort_values(by = [column_with_predict_var_x, column_with_response_var_y], ascending = [True, True])
                # Restart the index of the copy:
                ds_copy = ds_copy.reset_index(drop = True)
                
                # Re-extract the X and Y series and convert them to NumPy arrays 
                # (these arrays will be important later in the function):
                x = np.array(ds_copy[column_with_predict_var_x])
                y = np.array(ds_copy[column_with_response_var_y])
            
                # Then, create the dictionary:
                dict_of_values = {'x': x, 'y': y, 'lab': lab}
                
                # Now, append dict_of_values to list_of_dictionaries_with_series_to_analyze:
                list_of_dictionaries_with_series_to_analyze.append(dict_of_values)
                
            # Now, we have a list of dictionaries with the same format of the input list.
            
    else:
        
        # The user input a list_of_dictionaries_with_series_to_analyze
        # Create a support list:
        support_list = []
        
        # Loop through each element on the list list_of_dictionaries_with_series_to_analyze:
        
        for i in range (0, len(list_of_dictionaries_with_series_to_analyze)):
            # from i = 0 to i = len(list_of_dictionaries_with_series_to_analyze) - 1, index of the
            # last element from the list
            
            # pick the i-th dictionary from the list:
            dictionary = list_of_dictionaries_with_series_to_analyze[i]
            
            # access 'x', 'y', and 'lab' keys from the dictionary:
            x = dictionary['x']
            y = dictionary['y']
            lab = dictionary['lab']
            # Remember that all this variables are series from a dataframe, so we can apply
            # the astype function:
            # https://www.askpython.com/python/built-in-methods/python-astype?msclkid=8f3de8afd0d411ec86a9c1a1e290f37c
            
            # check if at least x and y are not None:
            if ((x is not None) & (y is not None)):
                
                # If column_with_predict_var_x is an object, the user may be trying to pass a date as x. 
                # So, let's try to convert it to datetime:
                if (x.dtype not in numeric_dtypes):

                    try:
                        x = (x).astype('datetime64[ns]')
                        print(f"Variable X from {i}-th dictionary successfully converted to datetime64[ns].\n")

                    except:
                        # Simply ignore it
                        pass
                
                # Possibly, x and y are not ordered. Firstly, let's merge them into a temporary
                # dataframe to be able to order them together.
                # Use the 'list' attribute to guarantee that x and y were read as lists. These lists
                # are the values for a dictionary passed as argument for the constructor of the
                # temporary dataframe. When using the list attribute, we make the series independent
                # from its origin, even if it was created from a Pandas dataframe. Then, we have a
                # completely independent dataframe that may be manipulated and sorted, without worrying
                # that it may modify its origin:
                
                temp_df = pd.DataFrame(data = {'x': list(x), 'y': list(y)})
                # sort this dataframe by 'x' and 'y':
                temp_df = temp_df.sort_values(by = ['x', 'y'], ascending = [True, True])
                # restart index:
                temp_df = temp_df.reset_index(drop = True)
                
                # Re-extract the X and Y series and convert them to NumPy arrays 
                # (these arrays will be important later in the function):
                x = np.array(temp_df['x'])
                y = np.array(temp_df['y'])
                
                # check if lab is None:
                if (lab is None):
                    # input a default label.
                    # Use the str attribute to convert the integer to string, allowing it
                    # to be concatenated
                    lab = "X" + str(i) + "_x_" + "Y" + str(i)
                    
                # Then, create the dictionary:
                dict_of_values = {'x': x, 'y': y, 'lab': lab}
                
                # Now, append dict_of_values to support list:
                support_list.append(dict_of_values)
            
        # Now, support_list contains only the dictionaries with valid entries, as well
        # as labels for each collection of data. The values are independent from their origin,
        # and now they are ordered and in the same format of the data extracted directly from
        # the dataframe.
        # So, make the list_of_dictionaries_with_series_to_analyze the support_list itself:
        list_of_dictionaries_with_series_to_analyze = support_list
        print(f"{len(list_of_dictionaries_with_series_to_analyze)} valid series input.\n")

        
    # Now that both methods of input resulted in the same format of list, we can process both
    # with the same code.
    
    # Each dictionary in list_of_dictionaries_with_series_to_analyze represents a series to
    # plot. So, the total of series to plot is:
    total_of_series = len(list_of_dictionaries_with_series_to_analyze)
    
    if (total_of_series <= 0):
        
        print("No valid series to plot. Please, provide valid arguments.\n")
    
    else:
        
        # Continue to plotting and calculating the fitting.
        # Notice that we sorted the all the lists after they were separated and before
        # adding them to dictionaries. Also, the timestamps were converted to datetime64 variables
        # Now we finished the loop, list_of_dictionaries_with_series_to_analyze 
        # contains all series converted to NumPy arrays, with timestamps parsed as datetimes.
        # This list will be the object returned at the end of the function. Since it is an
        # JSON-formatted list, we can use the function json_obj_to_pandas_dataframe to convert
        # it to a Pandas dataframe.
        
        
        # Now, we can plot the figure.
        # we set alpha = 0.95 (opacity) to give a degree of transparency (5%), 
        # so that one series do not completely block the visualization of the other.
        
        # Let's retrieve the list of Matplotlib CSS colors:
        css4 = mcolors.CSS4_COLORS
        # css4 is a dictionary of colors: {'aliceblue': '#F0F8FF', 'antiquewhite': '#FAEBD7', ...}
        # Each key of this dictionary is a color name to be passed as argument color on the plot
        # function. So let's retrieve the array of keys, and use the list attribute to convert this
        # array to a list of colors:
        list_of_colors = list(css4.keys())
        
        # In 11 May 2022, this list of colors had 148 different elements
        # Since this list is in alphabetic order, let's create a random order for the colors.
        
        # Function random.sample(input_sequence, number_of_samples): 
        # this function creates a list containing a total of elements equals to the parameter 
        # "number_of_samples", which must be an integer.
        # This list is obtained by ramdomly selecting a total of "number_of_samples" elements from the
        # list "input_sequence" passed as parameter.
        
        # Function random.choices(input_sequence, k = number_of_samples):
        # similarly, randomly select k elements from the sequence input_sequence. This function is
        # newer than random.sample
        # Since we want to simply randomly sort the sequence, we can pass k = len(input_sequence)
        # to obtain the randomly sorted sequence:
        list_of_colors = random.choices(list_of_colors, k = len(list_of_colors))
        # Now, we have a random list of colors to use for plotting the charts
        
        if (add_splines_lines == True):
            LINE_STYLE = '-'

        else:
            LINE_STYLE = ''
        
        if (add_scatter_dots == True):
            MARKER = 'o'
            
        else:
            MARKER = ''
        
        # Matplotlib linestyle:
        # https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html?msclkid=68737f24d16011eca9e9c4b41313f1ad
        
        if (plot_title is None):
            # Set graphic title
            plot_title = f"Y_x_timestamp"

        if (horizontal_axis_title is None):
            # Set horizontal axis title
            horizontal_axis_title = "timestamp"

        if (vertical_axis_title is None):
            # Set vertical axis title
            vertical_axis_title = "Y"
        
        # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
        # so that the bars do not completely block other views.
        OPACITY = 0.95
        
        #Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
        fig = plt.figure(figsize = (12, 8))
        ax = fig.add_subplot()

        i = 0 # Restart counting for the loop of colors
        
        # Loop through each dictionary from list_of_dictionaries_with_series_and_predictions:
        for dictionary in list_of_dictionaries_with_series_to_analyze:
            
            # Try selecting a color from list_of_colors:
            try:
                
                COLOR = list_of_colors[i]
                # Go to the next element i, so that the next plot will use a different color:
                i = i + 1
            
            except IndexError:
                
                # This error will be raised if list index is out of range, 
                # i.e. if i >= len(list_of_colors) - we used all colors from the list (at least 148).
                # So, return the index to zero to restart the colors from the beginning:
                i = 0
                COLOR = list_of_colors[i]
                i = i + 1
            
            # Access the arrays and label from the dictionary:
            X = dictionary['x']
            Y = dictionary['y']
            LABEL = dictionary['lab']
            
            # Scatter plot:
            ax.plot(X, Y, linestyle = LINE_STYLE, marker = MARKER, color = COLOR, alpha = OPACITY, label = LABEL)
            # Axes.plot documentation:
            # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html?msclkid=42bc92c1d13511eca8634a2c93ab89b5
            
            # x and y are positional arguments: they are specified by their position in function
            # call, not by an argument name like 'marker'.
            
            # Matplotlib markers:
            # https://matplotlib.org/stable/api/markers_api.html?msclkid=36c5eec5d16011ec9583a5777dc39d1f
            
        # Now we finished plotting all of the series, we can set the general configuration:
        
        #ROTATE X AXIS IN XX DEGREES
        plt.xticks(rotation = x_axis_rotation)
        # XX = 0 DEGREES x_axis (Default)
        #ROTATE Y AXIS IN XX DEGREES:
        plt.yticks(rotation = y_axis_rotation)
        # XX = 0 DEGREES y_axis (Default)

        ax.set_title(plot_title)
        ax.set_xlabel(horizontal_axis_title)
        ax.set_ylabel(vertical_axis_title)

        ax.grid(grid) # show grid or not
        ax.legend(loc = 'upper left')
        # position options: 'upper right'; 'upper left'; 'lower left'; 'lower right';
        # 'right', 'center left'; 'center right'; 'lower center'; 'upper center', 'center'
        # https://www.statology.org/matplotlib-legend-position/

        if (export_png == True):
            # Image will be exported
            import os

            #check if the user defined a directory path. If not, set as the default root path:
            if (directory_to_save is None):
                #set as the default
                directory_to_save = ""

            #check if the user defined a file name. If not, set as the default name for this
            # function.
            if (file_name is None):
                #set as the default
                file_name = "time_series_vis"

            #check if the user defined an image resolution. If not, set as the default 110 dpi
            # resolution.
            if (png_resolution_dpi is None):
                #set as 330 dpi
                png_resolution_dpi = 330

            #Get the new_file_path
            new_file_path = os.path.join(directory_to_save, file_name)

            #Export the file to this new path:
            # The extension will be automatically added by the savefig method:
            plt.savefig(new_file_path, dpi = png_resolution_dpi, quality = 100, format = 'png', transparent = False) 
            #quality could be set from 1 to 100, where 100 is the best quality
            #format (str, supported formats) = 'png', 'pdf', 'ps', 'eps' or 'svg'
            #transparent = True or False
            # For other parameters of .savefig method, check https://indianaiproduction.com/matplotlib-savefig/
            print (f"Figure exported as \'{new_file_path}.png\'. Any previous file in this root path was overwritten.")

        #Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
        #plt.figure(figsize = (12, 8))
        #fig.tight_layout()

        ## Show an image read from an image file:
        ## import matplotlib.image as pltimg
        ## img=pltimg.imread('mydecisiontree.png')
        ## imgplot = plt.imshow(img)
        ## See linkedIn Learning course: "Supervised machine learning and the technology boom",
        ##  Ex_Files_Supervised_Learning, Exercise Files, lesson '03. Decision Trees', '03_05', 
        ##  '03_05_END.ipynb'
        plt.show()


def histogram (df, column_to_analyze, total_of_bins = 10, normal_curve_overlay = True, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    histogram (df, column_to_analyze, total_of_bins = 10, normal_curve_overlay = True, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    : param: column_to_analyze: string with the name of the column that will be analyzed.
      column_to_analyze = 'col1' obtain a histogram from column 1.
    """
    
    # Set a local copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    
    # Sort by the column to analyze (ascending order) and reset the index:
    DATASET = DATASET.sort_values(by = column_to_analyze, ascending = True)
    
    DATASET = DATASET.reset_index(drop = True)
    
    # Create an instance (object) from class CapabilityAnalysis:
    capability_obj = CapabilityAnalysis(df = DATASET, column_with_variable_to_be_analyzed = column_to_analyze, specification_limits = {'lower_spec_lim': None, 'upper_spec_lim': None}, total_of_bins = total_of_bins)
    
    # Get histogram array:
    capability_obj = capability_obj.get_histogram_array()
    # Attribute .histogram_dict: dictionary with keys 'list_of_bins' and 'list_of_counts'.
    
    # Get fitted normal:
    capability_obj = capability_obj.get_fitted_normal()
    # Now the .specification_limits attribute contains the nested dict desired_normal = {'x': x_of_normal, 'y': y_normal}
    # in key 'fitted_normal'.
    
    # Get the actual probability density function (PDF):
    capability_obj = capability_obj.get_actual_pdf()
    # Now the dictionary in the attribute .specification_limits has the nested dict actual_pdf = {'x': array_to_analyze, 'y': array_of_probs}
    # in key 'actual_pdf'.
    
    # Retrieve general statistics:
    stats_dict = {
        
        'sample_size': capability_obj.sample_size,
        'mu': capability_obj.mu,
        'median': capability_obj.median,
        'sigma': capability_obj.sigma,
        'lowest': capability_obj.lowest,
        'highest': capability_obj.highest
    }
    
    # Retrieve the histogram dict:
    histogram_dict = capability_obj.histogram_dict
    
    # Retrieve the specification limits dictionary updated:
    specification_limits = capability_obj.specification_limits
    # Retrieve the desired normal and actual PDFs dictionaries:
    fitted_normal = specification_limits['fitted_normal']
    actual_pdf = specification_limits['actual_pdf']
    
    string_for_title = " - $\mu = %.2f$, $\sigma = %.2f$" %(stats_dict['mu'], stats_dict['sigma'])
    
    if not (plot_title is None):
        plot_title = plot_title + string_for_title
        # %.2f: the number between . and f indicates the number of printed decimal cases
        # the notation $\ - Latex code for printing formatted equations and symbols.
    
    else:
        # Set graphic title
        plot_title = f"histogram_of_{column_to_analyze}" + string_for_title

    if (horizontal_axis_title is None):
        # Set horizontal axis title
        horizontal_axis_title = column_to_analyze

    if (vertical_axis_title is None):
        # Set vertical axis title
        vertical_axis_title = "Counting/Frequency"
        
    # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
    # so that the bars do not completely block other views.
    OPACITY = 0.95
    
    y_hist = DATASET[column_to_analyze]
    
    # Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
    fig = plt.figure(figsize = (12, 8))
    ax = fig.add_subplot()
    
    #STANDARD MATPLOTLIB METHOD:
    #bins = number of bins (intervals) of the histogram. Adjust it manually
    #increasing bins will increase the histogram's resolution, but height of bars
    
    ax.hist(y_hist, bins = total_of_bins, alpha = OPACITY, label = f'counting_of\n{column_to_analyze}', color = 'darkblue')
    #ax.hist(y, bins=20, width = bar_width, label=xlabel, color='blue')
    #IF GRAPHIC IS NOT SHOWN: THAT IS BECAUSE THE DISTANCES BETWEEN VALUES ARE LOW, AND YOU WILL
    #HAVE TO USE THE STANDARD HISTOGRAM METHOD FROM MATPLOTLIB.
    #TO DO THAT, UNMARK LINE ABOVE: ax.hist(y, bins=20, width = bar_width, label=xlabel, color='blue')
    #AND MARK LINE BELOW AS COMMENT: ax.bar(xhist, yhist, width = bar_width, label=xlabel, color='blue')
    
    #IF YOU WANT TO CREATE GRAPHIC AS A BAR CHART BASED ON THE CALCULATED DISTRIBUTION TABLE, 
    #MARK THE LINE ABOVE AS COMMENT AND UNMARK LINE BELOW:
    #ax.bar(x_hist, y_hist, label = f'counting_of\n{column_to_analyze}', color = 'darkblue')
    #ajuste manualmente a largura, width, para deixar as barras mais ou menos proximas
    
    # Plot the probability density function for the data:
    pdf_x = actual_pdf['x']
    pdf_y = actual_pdf['y']
    
    ax.plot(pdf_x, pdf_y, color = 'darkgreen', linestyle = '-', alpha = OPACITY, label = 'probability\ndensity')
    
    if (normal_curve_overlay == True):
        
        # Check if a normal curve was obtained:
        x_of_normal = fitted_normal['x']
        y_normal = fitted_normal['y']

        if (len(x_of_normal) > 0):
            # Non-empty list, add the normal curve:
            ax.plot(x_of_normal, y_normal, color = 'crimson', linestyle = 'dashed', alpha = OPACITY, label = 'expected\nnormal_curve')

    #ROTATE X AXIS IN XX DEGREES
    plt.xticks(rotation = x_axis_rotation)
    # XX = 0 DEGREES x_axis (Default)
    #ROTATE Y AXIS IN XX DEGREES:
    plt.yticks(rotation = y_axis_rotation)
    # XX = 0 DEGREES y_axis (Default)

    ax.set_title(plot_title)
    ax.set_xlabel(horizontal_axis_title)
    ax.set_ylabel(vertical_axis_title)

    ax.grid(grid) # show grid or not
    ax.legend(loc = 'upper right')
    # position options: 'upper right'; 'upper left'; 'lower left'; 'lower right';
    # 'right', 'center left'; 'center right'; 'lower center'; 'upper center', 'center'
    # https://www.statology.org/matplotlib-legend-position/

    if (export_png == True):
        # Image will be exported
        import os

        #check if the user defined a directory path. If not, set as the default root path:
        if (directory_to_save is None):
            #set as the default
            directory_to_save = ""

        #check if the user defined a file name. If not, set as the default name for this
        # function.
        if (file_name is None):
            #set as the default
            file_name = "histogram"

        #check if the user defined an image resolution. If not, set as the default 110 dpi
        # resolution.
        if (png_resolution_dpi is None):
            #set as 330 dpi
            png_resolution_dpi = 330

        #Get the new_file_path
        new_file_path = os.path.join(directory_to_save, file_name)

        #Export the file to this new path:
        # The extension will be automatically added by the savefig method:
        plt.savefig(new_file_path, dpi = png_resolution_dpi, quality = 100, format = 'png', transparent = False) 
        #quality could be set from 1 to 100, where 100 is the best quality
        #format (str, supported formats) = 'png', 'pdf', 'ps', 'eps' or 'svg'
        #transparent = True or False
        # For other parameters of .savefig method, check https://indianaiproduction.com/matplotlib-savefig/
        print (f"Figure exported as \'{new_file_path}.png\'. Any previous file in this root path was overwritten.")

    #Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
    #plt.figure(figsize = (12, 8))
    #fig.tight_layout()

    ## Show an image read from an image file:
    ## import matplotlib.image as pltimg
    ## img=pltimg.imread('mydecisiontree.png')
    ## imgplot = plt.imshow(img)
    ## See linkedIn Learning course: "Supervised machine learning and the technology boom",
    ##  Ex_Files_Supervised_Learning, Exercise Files, lesson '03. Decision Trees', '03_05', 
    ##  '03_05_END.ipynb'
    plt.show()
    
    stats_dict = {
                'statistics': ['mean', 'median', 'standard_deviation', f'lowest_{column_to_analyze}', 
                                f'highest_{column_to_analyze}', 'count_of_values', 'number_of_bins', 
                                'bin_size', 'bin_of_max_proba', 'count_on_bin_of_max_proba'],
                'value': [stats_dict['mu'], stats_dict['median'], stats_dict['sigma'], 
                            stats_dict['lowest'], stats_dict['highest'], stats_dict['sample_size'], 
                            histogram_dict['number_of_bins'], histogram_dict['bin_size'], 
                            histogram_dict['bin_of_max_proba'], histogram_dict['max_count']]
                }
    
    # Convert it to a Pandas dataframe setting the list 'statistics' as the index:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
    general_stats = pd.DataFrame(data = stats_dict)
    
    # Set the column 'statistics' as the index of the dataframe, using set_index method:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.set_index.html
    
    # If inplace = True, modifies the DataFrame in place (do not create a new object).
    # Then, we do not create an object equal to the expression. We simply apply the method (so,
    # None is returned from the method):
    general_stats.set_index(['statistics'], inplace = True)
    
    print("Check the general statistics from the analyzed variable:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(general_stats)
            
    except: # regular mode
        print(general_stats)
    
    print("\n")
    print("Check the frequency table:\n")
    
    freq_table = histogram_dict['df']
    
    try:    
        display(freq_table)    
    except:
        print(freq_table)

    return general_stats, freq_table


def test_data_normality (df, column_to_analyze, column_with_labels_to_test_subgroups = None, alpha = 0.10, show_probability_plot = True, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    test_data_normality (df, column_to_analyze, column_with_labels_to_test_subgroups = None, alpha = 0.10, show_probability_plot = True, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):

    Check https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.probplot.html#scipy.stats.probplot
    Check https://docs.scipy.org/doc/scipy/tutorial/stats.html
    Check https://docs.scipy.org/doc/scipy-1.8.0/html-scipyorg/reference/generated/scipy.stats.normaltest.html
    
    WARNING: The statistical tests require at least 20 samples
    
    : param: column_to_analyze: column (variable) of the dataset that will be tested. Declare as a string,
      in quotes.
      e.g. column_to_analyze = 'col1' will analyze a column named 'col1'.
    
    : param: column_with_labels_to_test_subgroups: if there is a column with labels or
      subgroup indication, and the normality should be tested separately for each label, indicate
      it here as a string (in quotes). e.g. column_with_labels_to_test_subgroups = 'col2' 
      will retrieve the labels from 'col2'.
      Keep column_with_labels_to_test_subgroups = None if a single series (the whole column)
      will be tested.
    
    : param: alpha. Confidence level = 1 - ALPHA. For ALPHA = 0.10, we get a 0.90 = 90% confidence
      Set ALPHA = 0.05 to get 0.95 = 95% confidence in the analysis.
      Notice that, when less trust is needed, we can increase ALPHA to get less restrictive
      results.
    """

    from statsmodels.stats import diagnostic
    from scipy import stats
    
    print("WARNING: The statistical tests require at least 20 samples.\n")
    print("Interpretation:")
    print("p-value: probability of verifying the tested event, given that the null hypothesis H0 is correct.")
    print("H0: that data is described by the normal distribution.")
    print("Criterion: the series is not described by normal if p < alpha = %.3f." %(alpha))
    
    # Set a local copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    
    # Start a list to store the different Pandas series to test:
    list_of_dicts = []
    
    if not (column_with_labels_to_test_subgroups is None):
        
        # 1. Get the unique values from column_with_labels_to_test_subgroups
        # and save it as the list labels_list:
        labels_list = list(DATASET[column_with_labels_to_test_subgroups].unique())
        
        # 2. Loop through each element from labels_list:
        for label in labels_list:
            
            # 3. Create a copy of the DATASET, filtering for entries where 
            # column_with_labels_to_test_subgroups == label:
            filtered_df = (DATASET[DATASET[column_with_labels_to_test_subgroups] == label]).copy(deep = True)
            # 4. Reset index of the copied dataframe:
            filtered_df = filtered_df.reset_index(drop = True)
            # 5. Create a dictionary, with an identification of the series, and the series
            # that will be tested:
            series_dict = {'series_id': (column_to_analyze + "_" + label), 
                        'series': filtered_df[column_to_analyze],
                        'total_elements_to_test': len(filtered_df[column_to_analyze])}
            
            # 6. Append this dictionary to the list of series:
            list_of_dicts.append(series_dict)
        
    else:
        # In this case, the only series is the column itself. So, let's create a dictionary with
        # same structure:
        series_dict = {'series_id': column_to_analyze, 'series': DATASET[column_to_analyze],
                    'total_elements_to_test': len(DATASET[column_to_analyze])}
        
        # Append this dictionary to the list of series:
        list_of_dicts.append(series_dict)
    
    
    # Now, loop through each element from the list of series:
    
    for series_dict in list_of_dicts:
        
        # start a support list:
        support_list = []
        
        # Check if there are at least 20 samples to test:
        series_id = series_dict['series_id']
        total_elements_to_test = series_dict['total_elements_to_test']
        
        # Create an instance (object) from class capability_analysis:
        capability_obj = CapabilityAnalysis(df = DATASET, column_with_variable_to_be_analyzed = series_id, specification_limits = {'lower_spec_lim': None, 'upper_spec_lim': None}, alpha = alpha)
        
        # Check data normality:
        capability_obj = capability_obj.check_data_normality()
        # Attribute .normality_dict: dictionary with results from normality tests
        
        # Retrieve the normality dictionary:
        normality_dict = capability_obj.normality_dict
        # Nest it in series_dict:
        series_dict['normality_dict'] = normality_dict
        
        # Finally, append the series dictionary to the support list:
        support_list.append(series_dict)
        
        if ((total_elements_to_test >= 20) & (show_probability_plot == True)):
            
            y = series_dict['series']
        
            print("\n")
            #Obtain the probability plot  
            fig, ax = plt.subplots(figsize = (12, 8))

            ax.set_title(f"probability_plot_of_{series_id}_for_normal_distribution")
            
            plot_results = stats.probplot(y, dist = 'norm', fit = True, plot = ax)
            #This function resturns a tuple, so we must store it into res
            
            ax.grid(grid)
            #ROTATE X AXIS IN XX DEGREES
            plt.xticks(rotation = x_axis_rotation)
            # XX = 70 DEGREES x_axis (Default)
            #ROTATE Y AXIS IN XX DEGREES:
            plt.yticks(rotation = y_axis_rotation)
            # XX = 0 DEGREES y_axis (Default)   
            
            # Other distributions to check, see scipy Stats documentation. 
            # you could test dist=stats.loggamma, where stats was imported from scipy
            # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.probplot.html#scipy.stats.probplot

            if (export_png == True):
                # Image will be exported
                import os

                #check if the user defined a directory path. If not, set as the default root path:
                if (directory_to_save is None):
                    #set as the default
                    directory_to_save = ""

                #check if the user defined a file name. If not, set as the default name for this
                # function.
                if (file_name is None):
                    #set as the default
                    file_name = "probability_plot_normal"

                #check if the user defined an image resolution. If not, set as the default 110 dpi
                # resolution.
                if (png_resolution_dpi is None):
                    #set as 330 dpi
                    png_resolution_dpi = 330

                #Get the new_file_path
                new_file_path = os.path.join(directory_to_save, file_name)

                #Export the file to this new path:
                # The extension will be automatically added by the savefig method:
                plt.savefig(new_file_path, dpi = png_resolution_dpi, quality = 100, format = 'png', transparent = False) 
                #quality could be set from 1 to 100, where 100 is the best quality
                #format (str, supported formats) = 'png', 'pdf', 'ps', 'eps' or 'svg'
                #transparent = True or False
                # For other parameters of .savefig method, check https://indianaiproduction.com/matplotlib-savefig/
                print (f"Figure exported as \'{new_file_path}.png\'. Any previous file in this root path was overwritten.")

            #Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
            #plt.figure(figsize = (12, 8))
            #fig.tight_layout()
            ## Show an image read from an image file:
            ## import matplotlib.image as pltimg
            ## img=pltimg.imread('mydecisiontree.png')
            ## imgplot = plt.imshow(img)
            ## See linkedIn Learning course: "Supervised machine learning and the technology boom",
            ##  Ex_Files_Supervised_Learning, Exercise Files, lesson '03. Decision Trees', '03_05', 
            ##  '03_05_END.ipynb'
            plt.show()
                
            print("\n")
            
    # Now we left the for loop, make the list of dicts support list itself:
    list_of_dicts = support_list
    
    print("\n")
    print("Finished normality tests. Returning a list of dictionaries, where each dictionary contains the series analyzed and the p-values obtained.\n")
    print("Now, check general statistics of the data distribution:\n")
    
    # Now, let's obtain general statistics for all of the series, even those without the normality
    # test results.
    
    # start a support list:
    support_list = []
    
    for series_dict in list_of_dicts:
        
        y = series_dict['series']
        # Guarantee it is still a pandas series:
        y = pd.Series(y)
        # Calculate data skewness and kurtosis
    
        # Skewness
        data_skew = stats.skew(y)
        # skewness = 0 : normally distributed.
        # skewness > 0 : more weight in the left tail of the distribution.
        # skewness < 0 : more weight in the right tail of the distribution.
        # https://www.geeksforgeeks.org/scipy-stats-skew-python/

        # Kurtosis
        data_kurtosis = stats.kurtosis(y, fisher = True)
        # scipy.stats.kurtosis(array, axis=0, fisher=True, bias=True) function 
        # calculates the kurtosis (Fisher or Pearson) of a data set. It is the the fourth 
        # central moment divided by the square of the variance. 
        # It is a measure of the “tailedness” i.e. descriptor of shape of probability 
        # distribution of a real-valued random variable. 
        # In simple terms, one can say it is a measure of how heavy tail is compared 
        # to a normal distribution.
        # fisher parameter: fisher : Bool; Fisher’s definition is used (normal 0.0) if True; 
        # else Pearson’s definition is used (normal 3.0) if set to False.
        # https://www.geeksforgeeks.org/scipy-stats-kurtosis-function-python/
        print("A normal distribution should present no skewness (distribution distortion); and no kurtosis (long-tail).\n")
        print("For the data analyzed:\n")
        print(f"skewness = {data_skew}")
        print(f"kurtosis = {data_kurtosis}\n")

        if (data_skew < 0):

            print(f"Skewness = {data_skew} < 0: more weight in the left tail of the distribution.")

        elif (data_skew > 0):

            print(f"Skewness = {data_skew} > 0: more weight in the right tail of the distribution.")

        else:

            print(f"Skewness = {data_skew} = 0: no distortion of the distribution.")
                

        if (data_kurtosis == 0):

            print("Data kurtosis = 0. No long-tail effects detected.\n")

        else:

            print(f"The kurtosis different from zero indicates long-tail effects on the distribution.\n")

        #Calculate the mode of the distribution:
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mode.html
        # ModeResult(mode=3, count=5) access mode attribute
        try:
            data_mode = stats.mode(y, axis = None, keepdims = False).mode
        except:
            try:
                data_mode = stats.mode(y, axis = None, keepdims = False)[0]
            except:
                try:
                    if ((stats.mode(y, axis = None, keepdims = False) != np.nan) & (stats.mode(y, axis = None, keepdims = False) is not None)):
                        data_mode = stats.mode(y, axis = None, keepdims = False)
                    else:
                        data_mode = np.nan
                except:
                    data_mode = np.nan
        
        #Create general statistics dictionary:
        general_statistics_dict = {

            "series_mean": y.mean(),
            "series_variance": y.var(),
            "series_standard_deviation": y.std(),
            "series_skewness": data_skew,
            "series_kurtosis": data_kurtosis,
            "series_mode": data_mode

        }
        
        # Add this dictionary to the series dictionary:
        series_dict['general_statistics'] = general_statistics_dict
        
        # Append the dictionary to support list:
        support_list.append(series_dict)
    
    # Now, make the list of dictionaries support_list itself:
    list_of_dicts = support_list

    return list_of_dicts


def test_stat_distribution (df, column_to_analyze, column_with_labels_to_test_subgroups = None, statistical_distribution_to_test = 'lognormal'):
    """
    test_stat_distribution (df, column_to_analyze, column_with_labels_to_test_subgroups = None, statistical_distribution_to_test = 'lognormal'):

    Check https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.probplot.html#scipy.stats.probplot
    Check https://docs.scipy.org/doc/scipy/tutorial/stats.html
    Check https://docs.scipy.org/doc/scipy-1.8.0/html-scipyorg/reference/generated/scipy.stats.normaltest.html
    
    : param: column_to_analyze: column (variable) of the dataset that will be tested. Declare as a string,
      in quotes.
      e.g. column_to_analyze = 'col1' will analyze a column named 'col1'.
    
    : param: column_with_labels_to_test_subgroups: if there is a column with labels or
      subgroup indication, and the normality should be tested separately for each label, indicate
      it here as a string (in quotes). e.g. column_with_labels_to_test_subgroups = 'col2' 
      will retrieve the labels from 'col2'.
      Keep column_with_labels_to_test_subgroups = None if a single series (the whole column)
      will be tested.
    
      Attention: if you want to test a normal distribution, use the function 
      test_data_normality. Function test_data_normality tests normality through 4 methods 
      and compare them: D’Agostino and Pearson’s; Shapiro-Wilk; Lilliefors; 
      and Anderson-Darling tests.
      The calculus of the p-value from the Anderson-Darling statistic is available only 
      for some distributions. The function specific for the normality calculates these 
      probabilities of following the normal.
      Here, the function is destined to test a variety of distributions, and so only the 
      Anderson-Darling test is performed.
        
    : param: statistical_distribution: string (inside quotes) containing the tested statistical 
      distribution.
      Notice: if data Y follow a 'lognormal', log(Y) follow a normal
      Poisson is a special case from 'gamma' distribution.
      There are 91 accepted statistical distributions:
      'alpha', 'anglit', 'arcsine', 'beta', 'beta_prime', 'bradford', 'burr', 'burr12', 
      'cauchy', 'chi', 'chi-squared', 'cosine', 'double_gamma', 
      'double_weibull', 'erlang', 'exponential', 'exponentiated_weibull', 'exponential_power',
      'fatigue_life_birnbaum-saunders', 'fisk_log_logistic', 'folded_cauchy', 'folded_normal',
      'F', 'gamma', 'generalized_logistic', 'generalized_pareto', 'generalized_exponential', 
      'generalized_extreme_value', 'generalized_gamma', 'generalized_half-logistic', 
      'generalized_inverse_gaussian', 'generalized_normal', 
      'gilbrat', 'gompertz_truncated_gumbel', 'gumbel', 'gumbel_left-skewed', 'half-cauchy', 
      'half-normal', 'half-logistic', 'hyperbolic_secant', 'gauss_hypergeometric', 
      'inverted_gamma', 'inverse_normal', 'inverted_weibull', 'johnson_SB', 'johnson_SU', 
      'KSone', 'KStwobign', 'laplace', 'left-skewed_levy', 
      'levy', 'logistic', 'log_laplace', 'log_gamma', 'lognormal', 'log-uniform', 'maxwell', 
      'mielke_Beta-Kappa', 'nakagami', 'noncentral_chi-squared', 'noncentral_F', 
      'noncentral_t', 'normal', 'normal_inverse_gaussian', 'pareto', 'lomax', 
      'power_lognormal', 'power_normal', 'power-function', 'R', 'rayleigh', 'rice', 
      'reciprocal_inverse_gaussian', 'semicircular', 't-student', 
      'triangular', 'truncated_exponential', 'truncated_normal', 'tukey-lambda',
      'uniform', 'von_mises', 'wald', 'weibull_maximum_extreme_value', 
      'weibull_minimum_extreme_value', 'wrapped_cauchy'
    """

    from statsmodels.stats import diagnostic
    from scipy import stats
    
    
    print("WARNING: The statistical tests require at least 20 samples.\n")
    print("Attention: if you want to test a normal distribution, use the function test_data_normality.")
    print("Function test_data_normality tests normality through 4 methods and compare them: D’Agostino and Pearson’s; Shapiro-Wilk; Lilliefors; and Anderson-Darling tests.")
    print("The calculus of the p-value from the Anderson-Darling statistic is available only for some distributions.")
    print("The function which specifically tests the normality calculates these probabilities that data follows the normal.")
    print("Here, the function is destined to test a variety of distributions, and so only the Anderson-Darling test is performed.\n")
    
    print("If a compilation error is shown below, please update your Scipy version. Declare and run the following code into a separate cell:")
    print("! pip install scipy --upgrade\n")
    
    # Lets define the statistic distributions:
    # This are the callable Scipy objects which can be tested through Anderson-Darling test:
    # They are listed and explained in: 
    # https://docs.scipy.org/doc/scipy/tutorial/stats/continuous.html
    
    # There are 91 possible statistical distributions
    
    # Set a local copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    
    # Start a list to store the different Pandas series to test:
    list_of_dicts = []
    
    if not (column_with_labels_to_test_subgroups is None):
        
        # 1. Get the unique values from column_with_labels_to_test_subgroups
        # and save it as the list labels_list:
        labels_list = list(DATASET[column_with_labels_to_test_subgroups].unique())
        
        # 2. Loop through each element from labels_list:
        for label in labels_list:
            
            # 3. Create a copy of the DATASET, filtering for entries where 
            # column_with_labels_to_test_subgroups == label:
            filtered_df = (DATASET[DATASET[column_with_labels_to_test_subgroups] == label]).copy(deep = True)
            # 4. Reset index of the copied dataframe:
            filtered_df = filtered_df.reset_index(drop = True)
            # 5. Create a dictionary, with an identification of the series, and the series
            # that will be tested:
            series_dict = {'series_id': (column_to_analyze + "_" + label), 
                        'series': filtered_df[column_to_analyze],
                        'total_elements_to_test': filtered_df[column_to_analyze].count()}
            
            # 6. Append this dictionary to the list of series:
            list_of_dicts.append(series_dict)
        
    else:
        # In this case, the only series is the column itself. So, let's create a dictionary with
        # same structure:
        series_dict = {'series_id': column_to_analyze, 'series': DATASET[column_to_analyze],
                    'total_elements_to_test': DATASET[column_to_analyze].count()}
        
        # Append this dictionary to the list of series:
        list_of_dicts.append(series_dict)
    
    
    # Now, loop through each element from the list of series:
    
    for series_dict in list_of_dicts:
        
        # start a support list:
        support_list = []
        
        # Check if there are at least 20 samples to test:
        series_id = series_dict['series_id']
        total_elements_to_test = series_dict['total_elements_to_test']
        
        if (total_elements_to_test < 20):
            
            print(f"Unable to test series {series_id}: at least 20 samples are needed, but found only {total_elements_to_test} entries for this series.\n")
            # Add a warning to the dictionary:
            series_dict['WARNING'] = "Series without the minimum number of elements (20) required to test the normality."
            # Append it to the support list:
            support_list.append(series_dict)
            
        else:
            # Let's test the series.
            y = series_dict['series']
            
            # Calculate data skewness and kurtosis
            # Skewness
            data_skew = stats.skew(y)
            # skewness = 0 : normally distributed.
            # skewness > 0 : more weight in the left tail of the distribution.
            # skewness < 0 : more weight in the right tail of the distribution.
            # https://www.geeksforgeeks.org/scipy-stats-skew-python/

            # Kurtosis
            data_kurtosis = stats.kurtosis(y, fisher = True)
            # scipy.stats.kurtosis(array, axis=0, fisher=True, bias=True) function 
            # calculates the kurtosis (Fisher or Pearson) of a data set. It is the the fourth 
            # central moment divided by the square of the variance. 
            # It is a measure of the “tailedness” i.e. descriptor of shape of probability 
            # distribution of a real-valued random variable. 
            # In simple terms, one can say it is a measure of how heavy tail is compared 
            # to a normal distribution.
            # fisher parameter: fisher : Bool; Fisher’s definition is used (normal 0.0) if True; 
            # else Pearson’s definition is used (normal 3.0) if set to False.
            # https://www.geeksforgeeks.org/scipy-stats-kurtosis-function-python/
            print("A normal distribution should present no skewness (distribution distortion); and no kurtosis (long-tail).\n")
            print("For the data analyzed:\n")
            print(f"skewness = {data_skew}")
            print(f"kurtosis = {data_kurtosis}\n")

            if (data_skew < 0):

                print(f"Skewness = {data_skew} < 0: more weight in the left tail of the distribution.")

            elif (data_skew > 0):

                print(f"Skewness = {data_skew} > 0: more weight in the right tail of the distribution.")

            else:

                print(f"Skewness = {data_skew} = 0: no distortion of the distribution.")
                

            if (data_kurtosis == 0):

                print("Data kurtosis = 0. No long-tail effects detected.\n")

            else:

                print(f"The kurtosis different from zero indicates long-tail effects on the distribution.\n")

            #Calculate the mode of the distribution:
            # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mode.html
            # ModeResult(mode=3, count=5) access mode attribute
            try:
                data_mode = stats.mode(y, axis = None, keepdims = False).mode
            except:
                try:
                    data_mode = stats.mode(y, axis = None, keepdims = False)[0]
                except:
                    try:
                        if ((stats.mode(y, axis = None, keepdims = False) != np.nan) & (stats.mode(y, axis = None, keepdims = False) is not None)):
                            data_mode = stats.mode(y, axis = None, keepdims = False)
                        else:
                            data_mode = np.nan
                    except:
                        data_mode = np.nan
            
            # Access the object correspondent to the distribution provided. To do so,
            # simply access dict['key1'], where 'key1' is a key from a dictionary dict ={"key1": 'val1'}
            # Access just as accessing a column from a dataframe.

            anderson_darling_statistic = diagnostic.anderson_statistic(y, dist = (callable_statistical_distributions_dict[statistical_distribution_to_test]), fit = True)
            
            print(f"Anderson-Darling statistic for the distribution {statistical_distribution_to_test} = {anderson_darling_statistic}\n")
            print("The Anderson–Darling test assesses whether a sample comes from a specified distribution.")
            print("It makes use of the fact that, when given a hypothesized underlying distribution and assuming the data does arise from this distribution, the cumulative distribution function (CDF) of the data can be assumed to follow a uniform distribution.")
            print("Then, data can be tested for uniformity using an appropriate distance test (Shapiro 1980).\n")
            # source: https://en.wikipedia.org/wiki/Anderson%E2%80%93Darling_test

            # Fit the distribution and get its parameters
            # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_continuous.fit.html

            if(statistical_distribution_to_test == 'alpha'):
                distribution_parameters = stats.alpha.fit(y)
            elif(statistical_distribution_to_test == 'anglit'):
                distribution_parameters = stats.anglit.fit(y)
            elif(statistical_distribution_to_test == 'arcsine'):
                distribution_parameters = stats.arcsine.fit(y)
            elif(statistical_distribution_to_test == 'beta'):
                distribution_parameters = stats.beta.fit(y)
            elif(statistical_distribution_to_test == 'beta_prime'):
                distribution_parameters = stats.betaprime.fit(y)
            elif(statistical_distribution_to_test == 'bradford'):
                distribution_parameters = stats.bradford.fit(y)
            elif(statistical_distribution_to_test == 'burr'):
                distribution_parameters = stats.burr.fit(y)
            elif(statistical_distribution_to_test == 'burr12'):
                distribution_parameters = stats.burr12.fit(y)
            elif(statistical_distribution_to_test == 'cauchy'):
                distribution_parameters = stats.cauchy.fit(y)
            elif(statistical_distribution_to_test == 'chi'):
                distribution_parameters = stats.chi.fit(y)
            elif(statistical_distribution_to_test == 'chi-squared'):
                distribution_parameters = stats.chi2.fit(y)
            elif(statistical_distribution_to_test == 'cosine'):
                distribution_parameters = stats.cosine.fit(y)
            elif(statistical_distribution_to_test == 'double_gamma'):
                distribution_parameters = stats.dgamma.fit(y)
            elif(statistical_distribution_to_test == 'double_weibull'):
                distribution_parameters = stats.dweibull.fit(y)
            elif(statistical_distribution_to_test == 'erlang'):
                distribution_parameters = stats.erlang.fit(y)
            elif(statistical_distribution_to_test == 'exponential'):
                distribution_parameters = stats.expon.fit(y)
            elif(statistical_distribution_to_test == 'exponentiated_weibull'):
                distribution_parameters = stats.exponweib.fit(y)
            elif(statistical_distribution_to_test == 'exponential_power'):
                distribution_parameters = stats.exponpow.fit(y)
            elif(statistical_distribution_to_test == 'fatigue_life_birnbaum-saunders'):
                distribution_parameters = stats.fatiguelife.fit(y)
            elif(statistical_distribution_to_test == 'fisk_log_logistic'):
                distribution_parameters = stats.fisk.fit(y)
            elif(statistical_distribution_to_test == 'folded_cauchy'):
                distribution_parameters = stats.foldcauchy.fit(y)
            elif(statistical_distribution_to_test == 'folded_normal'):
                distribution_parameters = stats.foldnorm.fit(y)
            elif(statistical_distribution_to_test == 'F'):
                distribution_parameters = stats.f.fit(y)
            elif(statistical_distribution_to_test == 'gamma'):
                distribution_parameters = stats.gamma.fit(y)
            elif(statistical_distribution_to_test == 'generalized_logistic'):
                distribution_parameters = stats.genlogistic.fit(y)
            elif(statistical_distribution_to_test == 'generalized_pareto'):
                distribution_parameters = stats.genpareto.fit(y)
            elif(statistical_distribution_to_test == 'generalized_exponential'):
                distribution_parameters = stats.genexpon.fit(y)
            elif(statistical_distribution_to_test == 'generalized_extreme_value'):
                distribution_parameters = stats.genextreme.fit(y)
            elif(statistical_distribution_to_test == 'generalized_gamma'):
                distribution_parameters = stats.gengamma.fit(y)
            elif(statistical_distribution_to_test == 'generalized_half-logistic'):
                distribution_parameters = stats.genhalflogistic.fit(y)
            elif(statistical_distribution_to_test == 'generalized_inverse_gaussian'):
                distribution_parameters = stats.geninvgauss.fit(y)
            elif(statistical_distribution_to_test == 'generalized_normal'):
                distribution_parameters = stats.gennorm.fit(y)
            elif(statistical_distribution_to_test == 'gilbrat'):
                distribution_parameters = stats.gilbrat.fit(y)
            elif(statistical_distribution_to_test == 'gompertz_truncated_gumbel'):
                distribution_parameters = stats.gompertz.fit(y)
            elif(statistical_distribution_to_test == 'gumbel'):
                distribution_parameters = stats.gumbel_r.fit(y)
            elif(statistical_distribution_to_test == 'gumbel_left-skewed'):
                distribution_parameters = stats.gumbel_l.fit(y)
            elif(statistical_distribution_to_test == 'half-cauchy'):
                distribution_parameters = stats.halfcauchy.fit(y)
            elif(statistical_distribution_to_test == 'half-normal'):
                distribution_parameters = stats.halfnorm.fit(y)
            elif(statistical_distribution_to_test == 'half-logistic'):
                distribution_parameters = stats.halflogistic.fit(y)
            elif(statistical_distribution_to_test == 'hyperbolic_secant'):
                distribution_parameters = stats.hypsecant.fit(y)
            elif(statistical_distribution_to_test == 'gauss_hypergeometric'):
                distribution_parameters = stats.gausshyper.fit(y)
            elif(statistical_distribution_to_test == 'inverted_gamma'):
                distribution_parameters = stats.invgamma.fit(y)
            elif(statistical_distribution_to_test == 'inverse_normal'):
                distribution_parameters = stats.invgauss.fit(y)
            elif(statistical_distribution_to_test == 'inverted_weibull'):
                distribution_parameters = stats.invweibull.fit(y)
            elif(statistical_distribution_to_test == 'johnson_SB'):
                distribution_parameters = stats.johnsonsb.fit(y)
            elif(statistical_distribution_to_test == 'johnson_SU'):
                distribution_parameters = stats.johnsonsu.fit(y)
            elif(statistical_distribution_to_test == 'KSone'):
                distribution_parameters = stats.ksone.fit(y)
            elif(statistical_distribution_to_test == 'KStwobign'):
                distribution_parameters = stats.kstwobign.fit(y)
            elif(statistical_distribution_to_test == 'laplace'):
                distribution_parameters = stats.laplace.fit(y)
            elif(statistical_distribution_to_test == 'left-skewed_levy'):
                distribution_parameters = stats.levy_l.fit(y)
            elif(statistical_distribution_to_test == 'levy'):
                distribution_parameters = stats.levy.fit(y)
            elif(statistical_distribution_to_test == 'logistic'):
                distribution_parameters = stats.logistic.fit(y)
            elif(statistical_distribution_to_test == 'log_laplace'):
                distribution_parameters = stats.loglaplace.fit(y)
            elif(statistical_distribution_to_test == 'log_gamma'):
                distribution_parameters = stats.loggamma.fit(y)
            elif(statistical_distribution_to_test == 'lognormal'):
                distribution_parameters = stats.lognorm.fit(y)
            elif(statistical_distribution_to_test == 'log-uniform'):
                distribution_parameters = stats.loguniform.fit(y)
            elif(statistical_distribution_to_test == 'maxwell'):
                distribution_parameters = stats.maxwell.fit(y)
            elif(statistical_distribution_to_test == 'mielke_Beta-Kappa'):
                distribution_parameters = stats.mielke.fit(y)
            elif(statistical_distribution_to_test == 'nakagami'):
                distribution_parameters = stats.nakagami.fit(y)
            elif(statistical_distribution_to_test == 'noncentral_chi-squared'):
                distribution_parameters = stats.ncx2.fit(y)
            elif(statistical_distribution_to_test == 'noncentral_F'):
                distribution_parameters = stats.ncf.fit(y)
            elif(statistical_distribution_to_test == 'noncentral_t'):
                distribution_parameters = stats.nct.fit(y)
            elif(statistical_distribution_to_test == 'normal'):
                distribution_parameters = stats.norm.fit(y)
            elif(statistical_distribution_to_test == 'normal_inverse_gaussian'):
                distribution_parameters = stats.norminvgauss.fit(y)
            elif(statistical_distribution_to_test == 'pareto'):
                distribution_parameters = stats.pareto.fit(y)            
            elif(statistical_distribution_to_test == 'lomax'):
                distribution_parameters = stats.lomax.fit(y)
            elif(statistical_distribution_to_test == 'power_lognormal'):
                distribution_parameters = stats.powerlognorm.fit(y)
            elif(statistical_distribution_to_test == 'power_normal'):
                distribution_parameters = stats.powernorm.fit(y)
            elif(statistical_distribution_to_test == 'power-function'):
                distribution_parameters = stats.powerlaw.fit(y)
            elif(statistical_distribution_to_test == 'R'):
                distribution_parameters = stats.rdist.fit(y)
            elif(statistical_distribution_to_test == 'rayleigh'):
                distribution_parameters = stats.rayleigh.fit(y)
            elif(statistical_distribution_to_test == 'rice'):
                distribution_parameters = stats.rice.fit(y)
            elif(statistical_distribution_to_test == 'reciprocal_inverse_gaussian'):
                distribution_parameters = stats.recipinvgauss.fit(y)
            elif(statistical_distribution_to_test == 'semicircular'):
                distribution_parameters = stats.semicircular.fit(y)
            elif(statistical_distribution_to_test == 't-student'):
                distribution_parameters = stats.t.fit(y)
            elif(statistical_distribution_to_test == 'triangular'):
                distribution_parameters = stats.triang.fit(y)
            elif(statistical_distribution_to_test == 'truncated_exponential'):
                distribution_parameters = stats.truncexpon.fit(y)            
            elif(statistical_distribution_to_test == 'truncated_normal'):
                distribution_parameters = stats.truncnorm.fit(y)
            elif(statistical_distribution_to_test == 'tukey-lambda'):
                distribution_parameters = stats.tukeylambda.fit(y)
            elif(statistical_distribution_to_test == 'uniform'):
                distribution_parameters = stats.uniform.fit(y)
            elif(statistical_distribution_to_test == 'vonmises'):
                distribution_parameters = stats.vonmises.fit(y)
            elif(statistical_distribution_to_test == 'wald'):
                distribution_parameters = stats.wald.fit(y)
            elif(statistical_distribution_to_test == 'weibull_maximum_extreme_value'):
                distribution_parameters = stats.weibull_max.fit(y)
            elif(statistical_distribution_to_test == 'weibull_minimum_extreme_value'):
                distribution_parameters = stats.weibull_min.fit(y)
            elif(statistical_distribution_to_test == 'wrapped_cauchy'):
                distribution_parameters = stats.wrapcauchy.fit(y)
            else:
                raise InvalidInputsError (f"Please, select a valid statistical distribution to test: {list_of_dictionary_keys}")

            # With method="MLE" (default), the fit is computed by minimizing the negative 
            # log-likelihood function. A large, finite penalty (rather than infinite negative 
            # log-likelihood) is applied for observations beyond the support of the distribution. 
            # With method="MM", the fit is computed by minimizing the L2 norm of the relative errors 
            # between the first k raw (about zero) data moments and the corresponding distribution 
            # moments, where k is the number of non-fixed parameters. 

            # distribution_parameters: Estimates for any shape parameters (if applicable), 
            # followed by those for location and scale.
            print(f"Distribution shape parameters calculated for {statistical_distribution_to_test} = {distribution_parameters}\n")
            
            print("ATTENTION:\n")
            print("The critical values for the Anderson-Darling test are dependent on the specific distribution that is being tested.")
            print("Tabulated values and formulas have been published (Stephens, 1974, 1976, 1977, 1979) for a few specific distributions: normal, lognormal, exponential, Weibull, logistic, extreme value type 1.")
            print("The test consists on an one-sided test of the hypothesis that the distribution is of a specific form.")
            print("The hypothesis is rejected if the test statistic, A, is greater than the critical value for that particular distribution.")
            print("Note that, for a given distribution, the Anderson-Darling statistic may be multiplied by a constant which usually depends on the sample size, n).")
            print("These constants are given in the various papers by Stephens, and may be simply referred as the \'adjusted Anderson-Darling statistic\'.")
            print("This adjusted statistic is what should be compared against the critical values.")
            print("Also, be aware that different constants (and therefore critical values) have been published.")
            print("Therefore, you just need to be aware of what constant was used for a given set of critical values (the needed constant is typically given with the correspondent critical values).")
            print("To learn more about the Anderson-Darling statistics and the check the full references of Stephens, go to the webpage from the National Institute of Standards and Technology (NIST):\n")
            print("https://itl.nist.gov/div898/handbook/eda/section3/eda3e.htm")
            print("\n")
            
            #Create general statistics dictionary:
            general_statistics_dict = {

                "series_mean": y.mean(),
                "series_variance": y.var(),
                "series_standard_deviation": y.std(),
                "series_skewness": data_skew,
                "series_kurtosis": data_kurtosis,
                "series_mode": data_mode,
                "AndersonDarling_statistic_A": anderson_darling_statistic,
                "distribution_parameters": distribution_parameters

            }

            # Add this dictionary to the series dictionary:
            series_dict['general_statistics'] = general_statistics_dict

            # Now, append the series dictionary to the support list:
            support_list.append(series_dict)
        
    # Now we left the for loop, make the list of dicts support list itself:
    list_of_dicts = support_list
    
    print("General statistics successfully returned in the list \'list_of_dicts\'.\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(list_of_dicts)
            
    except: # regular mode
        print(list_of_dicts)
    
    print("\n")
    
    print("Note: the obtention of the probability plot specific for each distribution requires shape parameters.")
    print("Check Scipy documentation for additional information:")
    print("https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.probplot.html")
    
    return list_of_dicts


def fast_fourier_transform (df, column_to_analyze, average_frequency_of_data_collection = 'hour', x_axis_rotation = 0, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    fast_fourier_transform (df, column_to_analyze, average_frequency_of_data_collection = 'hour', x_axis_rotation = 0, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):

    Real-valued fast Fourier transform: https://www.tensorflow.org/api_docs/python/tf/signal/rfft?authuser=1
    2D real-valued fast Fourier transform: https://www.tensorflow.org/api_docs/python/tf/signal/rfft2d?authuser=1
    3D real-valued fast Fourier transform: https://www.tensorflow.org/api_docs/python/tf/signal/rfft3d?authuser=1
    Short-time Fourier Transform: https://www.tensorflow.org/api_docs/python/tf/signal/stft?authuser=1
    
    : param: average_frequency_of_data_collection = 'hour' or 'h' for hours; 'day' or 'd' for days;
      'minute' or 'min' for minutes; 'seconds' or 's' for seconds; 'ms' for milliseconds; 'ns' for
      nanoseconds; 'year' or 'y' for years; 'month' or 'm' for months.
    """

    import tensorflow as tf

    
    average_frequency_of_data_collection = str(average_frequency_of_data_collection).lower()
    
    if ((average_frequency_of_data_collection == 'year')|(average_frequency_of_data_collection == 'y')):
        count_per_year = 1
        xtick_list = [1]
        labels_list = ['1/year']
    
    elif ((average_frequency_of_data_collection == 'month')|(average_frequency_of_data_collection == 'm')):
        count_per_year = 12
        xtick_list = [1, count_per_year]
        labels_list = ['1/year', '1/month']
    
    elif ((average_frequency_of_data_collection == 'day')|(average_frequency_of_data_collection == 'd')):
        count_per_year = 365.2524
        xtick_list = [1, count_per_year]
        labels_list = ['1/year', '1/day']
    
    elif ((average_frequency_of_data_collection == 'hour')|(average_frequency_of_data_collection == 'h')):
        count_per_year = 24 * 365.2524
        xtick_list = [1, 365.2524, count_per_year]
        labels_list = ['1/year', '1/day', '1/h']
    
    elif ((average_frequency_of_data_collection == 'minute')|(average_frequency_of_data_collection == 'min')):
        count_per_year = 60 * 24 * 365.2524
        xtick_list = [1, 365.2524, (24 * 365.2524), count_per_year]
        labels_list = ['1/year', '1/day', '1/h', '1/min']
    
    elif ((average_frequency_of_data_collection == 'second')|(average_frequency_of_data_collection == 's')):
        count_per_year = 60 * 60 * 24 * 365.2524
        xtick_list = [1, 365.2524, (24 * 365.2524), (60 * 24 * 365.2524), count_per_year]
        labels_list = ['1/year', '1/day', '1/h', '1/min', '1/s']
    
    elif (average_frequency_of_data_collection == 'ms'):
        count_per_year = 60 * 60 * 24 * 365.2524 * (10**3)
        xtick_list = [1, 365.2524, (24 * 365.2524), (60 * 24 * 365.2524), (60 * 60 * 24 * 365.2524), count_per_year]
        labels_list = ['1/year', '1/day', '1/h', '1/min', '1/s', '1/ms']
    
    elif (average_frequency_of_data_collection == 'ns'):
        count_per_year = 60 * 60 * 24 * 365.2524 * (10**9)
        xtick_list = [1, 365.2524, (24 * 365.2524), (60 * 24 * 365.2524), (60 * 60 * 24 * 365.2524), (60 * 60 * 24 * 365.2524 * (10**3)), count_per_year]
        labels_list = ['1/year', '1/day', '1/h', '1/min', '1/s', '1/ms', '1/ns']
    
    else:
        print("No valid frequency input. Considering frequency in h.\n")
        count_per_year = 24 * 365.2524
        xtick_list = [1, 365.2524, count_per_year]
        labels_list = ['1/year', '1/day', '1/h']
    
    # Start a local copy of the dataframe:
    DATASET = df.copy(deep = True)
    
    #Subtract the average value of column to analyze from each entry, to eliminate a possible offset
    avg_value = DATASET[column_to_analyze].mean()
    DATASET[column_to_analyze] = DATASET[column_to_analyze] - avg_value
    
    # Perform the Fourier transform
    fft = tf.signal.rfft(DATASET[column_to_analyze])
    f_per_dataset = np.arange(0, len(fft))

    n_samples = len(DATASET[column_to_analyze])
    years_per_dataset = n_samples/(count_per_year)

    f_per_year = f_per_dataset/years_per_dataset
    
    # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
    # so that the bars do not completely block other views.
    OPACITY = 0.95
    
    if (plot_title is None):
        # Set graphic title
        plot_title = "obtained_frequencies"

    if (horizontal_axis_title is None):
        # Set horizontal axis title
        horizontal_axis_title = "frequency_log_scale"

    if (vertical_axis_title is None):
        # Set vertical axis title
        vertical_axis_title = "abs(fft)"
    
    # fft is a complex tensor. Let's pick the absolute value of each complex:
    abs_fft = np.abs(fft)
    
    #Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
    fig = plt.figure(figsize = (12, 8))
    ax = fig.add_subplot()
    
    ax.step(f_per_year, abs_fft, color = 'crimson', linestyle = '-', alpha = OPACITY)
    
    # Set limits of the axes:
    # Y from 0 to a value 1% higher than the maximum
    # X from 0.1, close to zero, to the maximum. Zero cannot be present in log scale
    
    plt.xlim([0.1, max(plt.xlim())])
    
    plt.xscale('log')
    plt.xticks(xtick_list, labels = labels_list)
        
    #ROTATE X AXIS IN XX DEGREES
    plt.xticks(rotation = x_axis_rotation)
    # XX = 0 DEGREES x_axis (Default)
    #ROTATE Y AXIS IN XX DEGREES:
    plt.yticks(rotation = y_axis_rotation)
    # XX = 0 DEGREES y_axis (Default)

    ax.set_title(plot_title)
    ax.set_xlabel(horizontal_axis_title)
    ax.set_ylabel(vertical_axis_title)

    ax.grid(grid) # show grid or not
    
    if (export_png == True):
        # Image will be exported
        import os

        #check if the user defined a directory path. If not, set as the default root path:
        if (directory_to_save is None):
            #set as the default
            directory_to_save = ""

        #check if the user defined a file name. If not, set as the default name for this
        # function.
        if (file_name is None):
            #set as the default
            file_name = "fast_fourier_transform"

        #check if the user defined an image resolution. If not, set as the default 110 dpi
        # resolution.
        if (png_resolution_dpi is None):
            #set as 330 dpi
            png_resolution_dpi = 330

        #Get the new_file_path
        new_file_path = os.path.join(directory_to_save, file_name)

        #Export the file to this new path:
        # The extension will be automatically added by the savefig method:
        plt.savefig(new_file_path, dpi = png_resolution_dpi, quality = 100, format = 'png', transparent = False) 
        #quality could be set from 1 to 100, where 100 is the best quality
        #format (str, supported formats) = 'png', 'pdf', 'ps', 'eps' or 'svg'
        #transparent = True or False
        # For other parameters of .savefig method, check https://indianaiproduction.com/matplotlib-savefig/
        print (f"Figure exported as \'{new_file_path}.png\'. Any previous file in this root path was overwritten.")

    #Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
    #plt.figure(figsize = (12, 8))
    #fig.tight_layout()

    ## Show an image read from an image file:
    ## import matplotlib.image as pltimg
    ## img=pltimg.imread('mydecisiontree.png')
    ## imgplot = plt.imshow(img)
    ## See linkedIn Learning course: "Supervised machine learning and the technology boom",
    ##  Ex_Files_Supervised_Learning, Exercise Files, lesson '03. Decision Trees', '03_05', 
    ##  '03_05_END.ipynb'
    plt.show()
    
    print("Attention: the frequency is in counts per year: 1 count per year corresponds to 1 year; 12 counts: months per year; 365.2524 counts: days per year, etc.\n")
    print("Plot starts in 0 counts per year; goes from 0.1 to 1 per year (log scale); and grows to 365.2524 = 1 count per day; to the limit defined.\n")

    # Also, return a tuple combining the absolute value of fft with the corresponding count per year
    return fft, tuple(zip(abs_fft, f_per_year))
