import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from idsw.datafetch.core import InvalidInputsError


def apply_row_filters_list (df, list_of_row_filters):
        """
        apply_row_filters_list (df, list_of_row_filters)

        This function applies filters to the dataframe and remove the non-selected entries.
            
        : param: df: dataframe to be analyzed.
            
        ## define the filters and only them define the filters list
        # EXAMPLES OF BOOLEAN FILTERS TO COMPOSE THE LIST
            boolean_filter1 = ((None) & (None)) 
            (condition1 AND (&) condition2)
            boolean_filter2 = ((None) | (None)) 
            condition1 OR (|) condition2
            
            # boolean filters result into boolean values True or False.

        ## Examples of filters:
            filter1 = (condition 1) & (condition 2)
            filter1 = (df['column1'] > = 0) & (df['column2']) < 0)
            filter2 = (condition)
            filter2 = (df['column3'] <= 2.5)
            filter3 = (df['column4'] > 10.7)
            filter3 = (condition 1) | (condition 2)
            filter3 = (df['column5'] != 'string1') | (df['column5'] == 'string2')

        ## comparative operators: > (higher); >= (higher or equal); < (lower); 
            <= (lower or equal); == (equal); != (different)

        ## concatenation operators: & (and): the filter is True only if the 
            two conditions concatenated through & are True
        ## | (or): the filter is True if at least one of the two conditions concatenated
            through | are True.
        ## ~ (not): inverts the boolean, i.e., True becomes False, and False becomes True. 

            separate conditions with parentheses. Use parentheses to define a order
            of definition of the conditions:
            filter = ((condition1) & (condition2)) | (condition3)
            Here, firstly ((condition1) & (condition2)) = subfilter is evaluated. 
            Then, the resultant (subfilter) | (condition3) is evaluated.

        ## Pandas .isin method: you can also use this method to filter rows belonging to
            a given subset (the row that is in the subset is selected). The syntax is:
            is_black_or_brown = dogs["color"].isin(["Black", "Brown"])
            or: filter = (dataframe_column_series).isin([value1, value2, ...])
            The negative of this condition may be acessed with ~ operator:
            filter = ~(dataframe_column_series).isin([value1, value2, ...])
        ## Also, you may use isna() method as filter for missing values:
            filter = (dataframe_column_series).isna()
            or, for not missing: ~(dataframe_column_series).isna()
            
        : param: list_of_row_filters: list of boolean filters to be applied to the dataframe
            # e.g. list_of_row_filters = [filter1]
            # applies a single filter saved as filter 1. Notice: even if there is a single
            # boolean filter, it must be declared inside brackets, as a single-element list.
            # That is because the function will loop through the list of filters.
            # list_of_row_filters = [filter1, filter2, filter3, filter4]
            # will apply, in sequence, 4 filters: filter1, filter2, filter3, and filter4.
            # Notice that the filters must be declared in the order you want to apply them.   
        """
        
        print("Warning: this function filter the rows and results into a smaller dataset, since it removes the non-selected entries.")
        print("If you want to pass a filter to simply label the selected rows, use the function label_dataframe_subsets, which do not eliminate entries from the dataframe.")
        
        # Set a local copy of the dataframe:
        DATASET = df.copy(deep = True)
        
        # Get the original index and convert it to a list
        original_index = list(DATASET.index)
        
        # Loop through the filters list, applying the filters sequentially:
        # Each element of the list is identified as 'boolean_filter'
        
        if (len(list_of_row_filters) > 0):
            
            # Start a list of indices that were removed. That is because we must
            # remove these elements from the boolean filter series before filtering, avoiding
            # the index mismatch.
            removed_indices = []
            
            # Now, loop through other rows in the list_of_row_filters:
            for boolean_series in list_of_row_filters:
                
                if (len(removed_indices) > 0):
                    # Drop rows in list removed_indices. Set inplace = True to remove by simply applying
                    # the method:
                    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop.html
                    boolean_series.drop(labels = removed_indices, axis = 0, inplace = True)
                
                # Apply the filter:
                DATASET = DATASET[boolean_series]
                
                # Finally, let's update the list of removed indices:
                for index in original_index:
                    if ((index not in list(DATASET.index)) & (index not in removed_indices)):
                        removed_indices.append(index)
        
        
        # Reset index:
        DATASET = DATASET.reset_index(drop = True)
        
        print("Successfully filtered the dataframe. Check the 10 first rows of the filtered and returned dataframe:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(DATASET.head(10))
                
        except: # regular mode
            print(DATASET.head(10))
        
        return DATASET


def drop_columns_or_rows (df, what_to_drop = 'columns', cols_list = None, row_index_list = None, reset_index_after_drop = True):
    """
    drop_columns_or_rows (df, what_to_drop = 'columns', cols_list = None, row_index_list = None, reset_index_after_drop = True):
    
    check https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop.html?highlight=drop
    
    : param: what_to_drop = 'columns' for removing the columns specified by their names (headers) 
      in cols_list (a list of strings).
      what_to_drop = 'rows' for removing the rows specified by their indices in
      row_index_list (a list of integers). Remember that the indexing starts from zero, i.e.,
      the first row is row number zero.
    
    : param: cols_list = list of strings containing the names (headers) of the columns to be removed
      For instance: cols_list = ['col1', 'col2', 'col3'] will 
      remove columns 'col1', 'col2', and 'col3' from the dataframe.
      If a single column will be dropped, you can declare it as a string (outside a list)
      e.g. cols_list = 'col1'; or cols_list = ['col1']
    
    : param: row_index_list = a list of integers containing the indices of the rows that will be dropped.
      e.g. row_index_list = [0, 1, 2] will drop the rows with indices 0 (1st row), 1 (2nd row), and
      2 (third row). Again, if a single row will be dropped, you can declare it as an integer (outside
      a list).
      e.g. row_index_list = 20 or row_index_list = [20] to drop the row with index 20 (21st row).
    
    : param: reset_index_after_drop = True. keep it True to restarting the indexing numeration after dropping.
      Alternatively, set reset_index_after_drop = False to keep the original numeration (the removed indices
      will be missing).
    """
    
    # Create dataframe local copy to manipulate, avoiding that Pandas operates on
    # the original object; or that Pandas tries to set values on slices or copies,
    # resulting in unpredictable results.
    # Use the copy method to effectively create a second object with the same properties
    # of the input parameters, but completely independent from it.
    DATASET = df.copy(deep = True)
    
    if (what_to_drop == 'columns'):
        
        if (cols_list is None):
            #check if a list was not input:
            raise InvalidInputsError ("Input a list of columns cols_list to be dropped.")
        
        else:
            #Drop the columns in cols_list:
            DATASET = DATASET.drop(columns = cols_list)
            print(f"The columns in {cols_list} headers list were successfully removed.\n")
    
    elif (what_to_drop == 'rows'):
        
        if (row_index_list is None):
            #check if a list was not input:
            raise InvalidInputsError ("Input a list of rows indices row_index_list to be dropped.")
        
        else:
            #Drop the rows in row_index_list:
            DATASET = DATASET.drop(row_index_list)
            print(f"The rows in {row_index_list} indices list were successfully removed.\n")
    
    else:
        raise InvalidInputsError ("Input a valid string as what_to_drop, rows or columns.")
    
    if (reset_index_after_drop == True):
        
        #restart the indexing
        DATASET = DATASET.reset_index(drop = True)
        print("The indices of the dataset were successfully restarted.\n")
    
    print("Check the 10 first rows from the returned dataset:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(DATASET.head(10))
            
    except: # regular mode
        print(DATASET.head(10))
    
    return DATASET


def remove_duplicate_rows (df, list_of_columns_to_analyze = None, which_row_to_keep = 'first', reset_index_after_drop = True):
    """
    remove_duplicate_rows (df, list_of_columns_to_analyze = None, which_row_to_keep = 'first', reset_index_after_drop = True):
    
    check https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop_duplicates.html
    
    : param: list_of_columns_to_analyze
      if list_of_columns_to_analyze = None, the whole dataset will be analyzed, i.e., rows
      will be removed only if they have same values for all columns from the dataset.
      Alternatively, pass a list of columns names (strings), if you want to remove rows with
      same values for that combination of columns. Pass it as a list, even if there is a single column
      being declared.
      e.g. list_of_columns_to_analyze = ['column1'] will check only 'column1'. Entries with same value
      on 'column1' will be considered duplicates and will be removed.
      list_of_columns_to_analyze = ['col1', 'col2',  'col3'] will analyze the combination of 3 columns:
      'col1', 'col2', and 'col3'. Only rows with same value for these 3 columns will be considered
      duplicates and will be removed.
    
    : param: which_row_to_keep = 'first' will keep the first detected row and remove all other duplicates. If
      None or an invalid string is input, this method will be selected.
      which_row_to_keep = 'last' will keep only the last detected duplicate row, and remove all the others.
    
    : param: reset_index_after_drop = True. keep it True to restarting the indexing numeration after dropping.
      Alternatively, set reset_index_after_drop = False to keep the original numeration (the removed indices
      will be missing).
    """

    # Create dataframe local copy to manipulate, avoiding that Pandas operates on
    # the original object; or that Pandas tries to set values on slices or copies,
    # resulting in unpredictable results.
    # Use the copy method to effectively create a second object with the same properties
    # of the input parameters, but completely independent from it.
    DATASET = df.copy(deep = True)
    
    if (which_row_to_keep == 'last'):
        
        #keep only the last duplicate.
        if (list_of_columns_to_analyze is None):
            # use the whole dataset
            DATASET = DATASET.drop_duplicates(keep = 'last')
            print(f"The rows with duplicate entries were successfully removed.")
            print("Only the last one of the duplicate entries was kept in the dataset.\n")
        
        else:
            #use the subset of columns
            if (list_of_columns_to_analyze is None):
                #check if a list was not input:
                raise InvalidInputsError ("Input a list of columns list_of_columns_to_analyze to be analyzed.")
        
            else:
                #Drop the columns in cols_list:
                DATASET = DATASET.drop_duplicates(subset = list_of_columns_to_analyze, keep = 'last')
                print(f"The rows with duplicate values for the columns in {list_of_columns_to_analyze} headers list were successfully removed.")
                print("Only the last one of the duplicate entries was kept in the dataset.\n")
    
    else:
        
        #keep only the first duplicate.
        if (list_of_columns_to_analyze is None):
            # use the whole dataset
            DATASET = DATASET.drop_duplicates()
            print(f"The rows with duplicate entries were successfully removed.")
            print("Only the first one of the duplicate entries was kept in the dataset.\n")
        
        else:
            #use the subset of columns
            if (list_of_columns_to_analyze is None):
                #check if a list was not input:
                raise InvalidInputsError ("Input a list of columns list_of_columns_to_analyze to be analyzed.")
        
            else:
                #Drop the columns in cols_list:
                DATASET = DATASET.drop_duplicates(subset = list_of_columns_to_analyze)
                print(f"The rows with duplicate values for the columns in {list_of_columns_to_analyze} headers list were successfully removed.")
                print("Only the first one of the duplicate entries was kept in the dataset.\n")
    
    if (reset_index_after_drop == True):
        
        #restart the indexing
        DATASET = DATASET.reset_index(drop = True)
        print("The indices of the dataset were successfully restarted.\n")
    
    print("Check the 10 first rows from the returned dataset:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(DATASET.head(10))
            
    except: # regular mode
        print(DATASET.head(10))
    
    return DATASET


def remove_completely_blank_rows_and_columns (df, list_of_columns_to_ignore = None):
    """
    remove_completely_blank_rows_and_columns (df, list_of_columns_to_ignore = None)

    : param: list_of_columns_to_ignore: if you do not want to check a specific column, pass its name
      (header) as an element from this list. It should be declared as a list even if it contains
      a single value.
      e.g. list_of_columns_to_ignore = ['column1'] will not analyze missing values in column named
      'column1'; list_of_columns_to_ignore = ['col1', 'col2'] will ignore columns 'col1' and 'col2'
    """

    # Create dataframe local copy to manipulate, avoiding that Pandas operates on
    # the original object; or that Pandas tries to set values on slices or copies,
    # resulting in unpredictable results.
    # Use the copy method to effectively create a second object with the same properties
    # of the input parameters, but completely independent from it.
    DATASET = df.copy(deep = True)
    
    # Get dataframe length:
    df_length = len(DATASET)
    
    # Get list of columns from the dataframe:
    df_columns = DATASET.columns
    
    # Get initial totals of rows or columns:
    total_rows = len(DATASET)
    total_cols = len(df_columns)
    
    # Get a list containing only columns to check:
    cols_to_check = []
    
    # Check if there is a list of columns to ignore:
    if not (list_of_columns_to_ignore is None):
        
        # Append all elements from df_columns that are not in the list
        # to ignore:
        for column in df_columns:
            # loop through all elements named 'column' and check if it satisfies both conditions
            if (column not in list_of_columns_to_ignore):
                cols_to_check.append(column)
        
        # create a ignored dataframe and a checked df:
        checked_df = DATASET[cols_to_check].copy(deep = True)
        # Update total columns:
        total_cols = len(checked_df.columns)
        
        ignored_df = DATASET[list_of_columns_to_ignore].copy(deep = True)
    
    else:
        # There is no column to ignore, so we must check all columns:
        checked_df = DATASET
        # Update the list of columns to check:
        cols_to_check = list(checked_df.columns)
    
    # To remove only rows or columns with only missing values, we set how = 'all' in
    # dropna method:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.dropna.html
    
    # Remove rows that contain only missing values:
    
    checked_df = checked_df.dropna(axis = 0, how = 'all')
    print(f"{total_rows - len(checked_df)} rows were completely blank and were removed.\n")
    
    # Remove columns that contain only missing values:
    checked_df = checked_df.dropna(axis = 1, how = 'all')
    print(f"{total_cols - len(checked_df.columns)} columns were completely blank and were removed.\n")
    
    # If len(cols_to_check) > 0, merge again the subsets:
    if (len(cols_to_check) > 0):

        if not (list_of_columns_to_ignore is None): # There is an ignored dataframe
        
            DATASET = pd.concat([ignored_df, checked_df], axis = 1, join = "inner")
        
        else: # Make the DATASET the checked_df itself:
            DATASET = checked_df

    # Now, reset the index:
    DATASET = DATASET.reset_index(drop = True)
    
    if (((total_rows - len(DATASET)) > 0) | ((total_cols - len(DATASET.columns)) > 0)):
        
        # There were modifications in the dataframe.
        print("Check the first 10 rows of the new returned dataframe:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(DATASET.head(10))

        except: # regular mode
            print(DATASET.head(10))
    
    else:
        print("No blank columns or rows were found. Returning the original dataframe.\n")
    
    return DATASET


def slice_dataframe (df, from_row = 'first_only', to_row = 'only', restart_index_of_the_sliced_dataframe = False):
    """
    slice_dataframe (df, from_row = 'first_only', to_row = 'only', restart_index_of_the_sliced_dataframe = False)

    : param: restart_index_of_the_sliced_dataframe = False to keep the 
      same row index of the original dataframe; or 
      restart_index_of_the_sliced_dataframe = True to reset indices 
      (start a new index, from 0 for the first row of the 
      returned dataframe).
    
    : params: from_row and to_row: integer or strings:
    
      from_row may be any integer from 0 to the last row of the dataset
      and the following strings: 'first' and 'first_only'
    
      to_row may be any integer from 0 to the last row of the dataset
      and the following strings: 'last', 'last_only', and 'only'
    
      the combination from_row = 'first', to_row = 'last' will
      return the original dataframe itself.
      The same is valid for the combination from_row = 'first_only', 
      to_row = 'last_only'; or of combinations between from_row = 0
      (index of the first row) with 'last' or the index
      of the last row; or combinations between 'first' and the index
      of the last row.
    
      These possibilities are the first checked by the code. If none
      of these special cases are present, then:
    
      from_row = 'first_only' selects a dataframe containing only the
      first row, independently of the parameter passed as to_row;
    
      to_row = 'last_only' selects a dataframe containing only the
      last row, independently of the parameter passed as from_row;
    
      if to_row = 'only', the sliced dataframe will be formed by only the
      row passed as from_row (an integer representing the row index is
      passed) - explained in the following lines
    
      These three special cases are dominant over the following ones
      (they are checked firstly, and force the modifying of slicing
      limits):
    
      Other special cases:
    
      from_row = 'first' starts slicing on the first row (index 0) -
      the 1st row from the dataframe will be the 1st row of the sliced
      dataframe too.
    
      to_row = 'last' finishes slicing in the last row - the last row
      from the dataframe will be the last row of the sliced dataframe.
    
      If i and j are integer numbers, they represent the indices of rows:
    
      from_row = i starts the sliced dataframe from the row of index i
      of the original dataframe.
      e.g. from_row = 8 starts the slicing from row with index 8. Since
      slicing starts from 0, this is the 9th row of the original dataframe.
    
      to_row = j finishes the sliced dataframe on the row of index j of
      the original dataframe. Attention: this row with index j is included,
      and will be the last_row of the sliced dataframe.
      e.g. if to_row = 21, the last row of the sliced dataframe will be the
      row with index 21 of the original dataframe. Since slicing starts
      from 0, this is the 22nd row of the original dataframe.
    
      In summary, if from_row = 8, to_row = 21, the sliced dataframe
      will be formed from the row of index 8 to the row of index 21 of
      the original dataframe, including both the row of index 8 and the row
      index 21. 
    
      from_row is effectively the first row of the new dataframe;
      and to_row is effectively the last row of the new dataframe.
    
      Notice that the use of to_row < from_row will raise an error.
    """

    # Create dataframe local copy to manipulate, avoiding that Pandas operates on
    # the original object; or that Pandas tries to set values on slices or copies,
    # resulting in unpredictable results.
    # Use the copy method to effectively create a second object with the same properties
    # of the input parameters, but completely independent from it.
    DATASET = df.copy(deep = True)
    
    # Store the total number of rows as num_rows:
    num_rows = len(DATASET)
    
    
    # Check if no from_row and to_row arguments were provided:
    if (from_row is None):
        print("No input for the argument \'from_row\'. Then, setting the start of the slice as the first row.\n")
        first_row_index = 0
    
    if (to_row is None):
        print("No input for the argument \'to_row\'. Then, setting the end of the slice as the last row.\n")
        last_row_index = (num_rows - 1)
    
    
    # Check type of the inputs (strings or integers):
    from_row_type = type(from_row)
    to_row_type = type(to_row)
    
    if (from_row_type == str):
        # It is a string
        
        if ((from_row == 'first') | (from_row == 'first_only')):
            # Set the first_row_index as the 0 (1st row index):
            first_row_index = 0
        
        else:
            print("Invalid string input for the argument \'from_row\'. Then, setting the start of the slice as the first row.\n")
            first_row_index = 0
    
    else:
        # Numeric input. Use the int attribute to guarantee that it 
        # was read as an integer. This value is itself the index of
        # the first row of the sliced dataframe:
        first_row_index = int(from_row)
    
    
    if (to_row_type == str):
        # It is a string
        
        if ((to_row == 'last') | (to_row == 'last_only')):
            # Set the last_row_index as the index of the last row of the dataframe:
            last_row_index = (num_rows - 1)
            # In the following code, we do last_row_index = last_row_index + 1 to
            # guarantee that the last row is actually included in the sliced df.
            
            # If to_row == 'last_only', we must correct first_row_index:
            # first_row_index was previously defined as 0 or as the value of the row
            # index provided. It must be the index of the last row, though:
            if (to_row == 'last_only'):
                first_row_index = last_row_index
                print("\'last_only\' argument provided, so starting the slicing from the last row of the dataframe.\n")
            
        elif (to_row == 'only'):
            # Use only the row declared as from_row
            last_row_index = first_row_index
            # In the following code, we do last_row_index = last_row_index + 1 to
            # guarantee that the last row is actually included in the sliced df.
        
        else:
            print("Invalid string input for the argument \'to_row\'. Then, setting the end of the slice as the last row.\n")
            last_row_index = (num_rows - 1)
    
    elif (from_row == 'first_only'):
        # In this case, last row index must be zero:
        last_row_index = 0
    
    else:
        # Numeric input. Use the int attribute to guarantee that it 
        # was read as an integer. This value is itself the index of
        # the last row of the sliced dataframe:
        last_row_index = int(to_row)
    
    
    # Check the special combination from = 1st row to last row
    # and return the original dataframe itself, without performing
    # operations:
    
    if ((from_row == 'first_only') & (to_row == 'last_only')):
        
        #return the dataframe without performing any operation
        print("Sliced dataframe is the original dataframe itself.")
        return DATASET
    
    elif ((first_row_index == 0) & (last_row_index == (num_rows - 1))):
        
        #return the dataframe without performing any operation
        print("Sliced dataframe is the original dataframe itself.")
        return DATASET
        
    # The two special combinations were checked, now we can back to
    # the main code
    
    
    # Slice a dataframe: df[i:j]
    # Slice the dataframe, getting only row i to row (j-1)
    # Indexing naturally starts from 0
    # Notice that the slicer defined as df[i:j] takes all columns from
    # the dataframe: it copies the dataframe structure (columns), but
    # selects only the specified rows.
    
    # first_row = df[0:1]
    # This is equivalent to df[:1] - if there is no start for the
    # slicer, the start from 0 is implicit
    # slice: get rows from row 0 to row (1-1) = 0
    # Therefore, we will obtain a copy of the dataframe, but containing
    # only the first row (row 0)
    
    # last_row = df[(num_rows - 1):(num_rows)] 
    # slice the dataframe from row (num_rows - 1), the index of the
    # last row, to row (num_rows) - 1 = (num_rows - 1)
    # Therefore, this slicer is a copy of the dataframe but containing
    # only its last row.
    
    # Slices are (fractions of) pandas dataframes, so elements must be
    # accessed through .iloc or .loc method
    
    
    # Set slicing limits:
    i = first_row_index # i is included
    j = last_row_index + 1
    # df[i:j] will include row i to row j - 1 = 
    # (last_row_index + 1) - 1 = last_row_index
    # Then, by summing 1 we guarantee that the row passed as
    # last_row_index will be actually included.
    # notice that when last_row_index = first_row_index
    # j will be the index of the next line.
    # e.g. the slice of only the first line must be df[0:1]
    # there must be a difference of 1 to include 1 line.
    
    # Now, slice the dataframe from line of index i to
    # line j-1, where line (j-1) is the last one included:
    
    sliced_df = DATASET[i:j]
    
    if (restart_index_of_the_sliced_dataframe == True):
        # Reset the index:
        sliced_df = sliced_df.reset_index(drop = True)
        print("Index of the returned dataframe was restarted.\n")
    
    print(f"Returning sliced dataframe, containing {sliced_df.shape[0]} rows and {sliced_df.shape[1]} columns.\n")
    # dataframe.shape is a tuple (N, M), where dataframe.shape[0] = N is
    # the number of rows; and dataframe.shape[1] = M is the number of columns
    # of the dataframe
    
    print("Check the dataframe below:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(sliced_df)
            
    except: # regular mode
        print(sliced_df)
    
    return sliced_df


def select_order_or_rename_columns (df, columns_list, mode = 'select_or_order_columns'):
    """
    select_order_or_rename_columns (df, columns_list, mode = 'select_or_order_columns')

    : param: MODE = 'select_or_order_columns' for filtering only the list of columns passed as columns_list,
      and setting a new column order. In this mode, you can pass the columns in any order: 
      the order of elements on the list will be the new order of columns.

      MODE = 'rename_columns' for renaming the columns with the names passed as columns_list. In this
      mode, the list must have same length and same order of the columns of the dataframe. That is because
      the columns will sequentially receive the names in the list. So, a mismatching of positions
      will result into columns with incorrect names.
    
    : param: columns_list = list of strings containing the names (headers) of the columns to select
      (filter); or to be set as the new columns' names, according to the selected mode.
      For instance: columns_list = ['col1', 'col2', 'col3'] will 
      select columns 'col1', 'col2', and 'col3' (or rename the columns with these names). 
      Declare the names inside quotes.
    """

    # Set a local copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    
    print(f"Original columns in the dataframe:\n{DATASET.columns}\n")
    
    if ((columns_list is None) | (columns_list == np.nan)):
        # empty list
        columns_list = []
    
    if (len(columns_list) == 0):
        print("Please, input a valid list of columns.\n")
        return DATASET
    
    if (mode == 'select_or_order_columns'):
        
        #filter the dataframe so that it will contain only the cols_list.
        DATASET = DATASET[columns_list]
        print("Dataframe filtered according to the list provided.\n")
        print("Check the new dataframe:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(DATASET)

        except: # regular mode
            print(DATASET)
        
    elif (mode == 'rename_columns'):
        
        # Check if the number of columns of the dataset is equal to the number of elements
        # of the new list. It will avoid raising an exception error.
        boolean_filter = (len(columns_list) == len(DATASET.columns))
        
        if (boolean_filter == False):
            #Impossible to rename, number of elements are different.
            print("The number of columns of the dataframe is different from the number of elements of the list. Please, provide a list with number of elements equals to the number of columns.\n")
            return DATASET
        
        else:
            #Same number of elements, so that we can update the columns' names.
            DATASET.columns = columns_list
            print("Dataframe columns renamed according to the list provided.\n")
            print("Warning: the substitution is element-wise: the first element of the list is now the name of the first column, and so on, ..., so that the last element is the name of the last column.\n")
            print("Check the new dataframe:\n")
            try:
                # only works in Jupyter Notebook:
                from IPython.display import display
                display(DATASET)

            except: # regular mode
                print(DATASET)
        
    else:
        print("Enter a valid mode: \'select_or_order_columns\' or \'rename_columns\'.")
        return DATASET
    
    return DATASET


def rename_or_clean_columns_labels (df, mode = 'set_new_names', substring_to_be_replaced = ' ', new_substring_for_replacement = '_', trailing_substring = None, list_of_columns_labels = [{'column_name': None, 'new_column_name': None}, {'column_name': None, 'new_column_name': None}, {'column_name': None, 'new_column_name': None}, {'column_name': None, 'new_column_name': None}, {'column_name': None, 'new_column_name': None}, {'column_name': None, 'new_column_name': None}, {'column_name': None, 'new_column_name': None}, {'column_name': None, 'new_column_name': None}]):
    """
    rename_or_clean_columns_labels (df, mode = 'set_new_names', substring_to_be_replaced = ' ', new_substring_for_replacement = '_', trailing_substring = None, list_of_columns_labels = [{'column_name': None, 'new_column_name': None}, {'column_name': None, 'new_column_name': None}, {'column_name': None, 'new_column_name': None}, {'column_name': None, 'new_column_name': None}, {'column_name': None, 'new_column_name': None}, {'column_name': None, 'new_column_name': None}, {'column_name': None, 'new_column_name': None}, {'column_name': None, 'new_column_name': None}]):
    
    Pandas .rename method:
      https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html
    
    : param: mode = 'set_new_names' will change the columns according to the specifications in
      list_of_columns_labels.
    
    : param: list_of_columns_labels = [{'column_name': None, 'new_column_name': None}]
      This is a list of dictionaries, where each dictionary contains two key-value pairs:
      the first one contains the original column name; and the second one contains the new name
      that will substitute the original one. The function will loop through all dictionaries in
      this list, access the values of the keys 'column_name', and it will be replaced (switched) 
      by the correspondent value in key 'new_column_name'.
    
      The object list_of_columns_labels must be declared as a list, 
      in brackets, even if there is a single dictionary.
      Use always the same keys: 'column_name' for the original label; 
      and 'new_column_name', for the correspondent new label.
      Notice that this function will not search substrings: it will substitute a value only when
      there is perfect correspondence between the string in 'column_name' and one of the columns
      labels. So, the cases (upper or lower) must be the same.
    
      If you want, you can remove elements (dictionaries) from the list to declare fewer elements;
      and you can also add more elements (dictionaries) to the lists, if you need to replace more
      values.
      Simply put a comma after the last element from the list and declare a new dictionary, keeping the
      same keys: {'column_name': original_col, 'new_column_name': new_col}, 
      where original_col and new_col represent the strings for searching and replacement 
      (If one of the keys contains None, the new dictionary will be ignored).
      Example: list_of_columns_labels = [{'column_name': 'col1', 'new_column_name': 'col'}] will
      rename 'col1' as 'col'.
    
    : param: mode = 'capitalize_columns' will capitalize all columns names (i.e., they will be put in
      upper case). e.g. a column named 'column' will be renamed as 'COLUMN'
    
      mode = 'lowercase_columns' will lower the case of all columns names. e.g. a column named
      'COLUMN' will be renamed as 'column'.
    
      mode = 'replace_substring' will search on the columns names (strings) for the 
    : param: substring_to_be_replaced (which may be a character or a string); and will replace it by 
    : param: new_substring_for_replacement (which again may be either a character or a string). 
      Numbers (integers or floats) will be automatically converted into strings.
      As an example, consider the default situation where we search for a whitespace ' ' 
      and replace it by underscore '_': 
      substring_to_be_replaced = ' ', new_substring_for_replacement = '_'  
      In this case, a column named 'new column' will be renamed as 'new_column'.
    
      mode = 'trim' will remove all trailing or leading whitespaces from column names.
      e.g. a column named as ' col1 ' will be renamed as 'col1'; 'col2 ' will be renamed as
      'col2'; and ' col3' will be renamed as 'col3'.
    
      mode = 'eliminate_trailing_characters' will eliminate a defined trailing and leading 
      substring from the columns' names. 
      The substring must be indicated as trailing_substring, and its default, when no value
      is provided, is equivalent to mode = 'trim' (eliminate white spaces). 
      e.g., if trailing_substring = '_test' and you have a column named 'col_test', it will be 
      renamed as 'col'.
    """
    
    # Set a local copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    # Guarantee that the columns were read as strings:
    DATASET.columns = (DATASET.columns).astype(str)
    # dataframe.columns is a Pandas Index object, so it has the dtype attribute as other Pandas
    # objects. So, we can use the astype method to set its type as str or 'object' (or "O").
    # Notice that there are situations with int Index, when integers are used as column names or
    # as row indices. So, this portion guarantees that we can call the str attribute to apply string
    # methods.
    
    if (mode == 'set_new_names'):
        
        # Start a mapping dictionary:
        mapping_dict = {}
        # This dictionary will be in the format required by .rename method: old column name as key,
        # and new name as value.

        # Loop through each element from list_of_columns_labels:
        for dictionary in list_of_columns_labels:

            # Access the values in keys:
            column_name = dictionary['column_name']
            new_column_name = dictionary['new_column_name']

            # Check if neither is None:
            if ((column_name is not None) & (new_column_name is not None)):
                
                # Guarantee that both were read as strings:
                column_name = str(column_name)
                new_column_name = str(new_column_name)

                # Add it to the mapping dictionary setting column_name as key, and the new name as the
                # value:
                mapping_dict[column_name] = new_column_name

        # Now, the dictionary is in the correct format for the method. Let's apply it:
        DATASET.rename(columns = mapping_dict, inplace = True)
    
    elif (mode == 'capitalize_columns'):
        
        DATASET.rename(str.upper, axis = 'columns', inplace = True)
    
    elif (mode == 'lowercase_columns'):
        
        DATASET.rename(str.lower, axis = 'columns', inplace = True)
    
    elif (mode == 'replace_substring'):
        
        if (substring_to_be_replaced is None):
            # set as the default (whitespace):
            substring_to_be_replaced = ' '
        
        if (new_substring_for_replacement is None):
            # set as the default (underscore):
            new_substring_for_replacement = '_'
        
        # Apply the str attribute to guarantee that numbers were read as strings:
        substring_to_be_replaced = str(substring_to_be_replaced)
        new_substring_for_replacement = str(new_substring_for_replacement)
        # Replace the substrings in the columns' names:
        substring_replaced_series = (pd.Series(DATASET.columns)).str.replace(substring_to_be_replaced, new_substring_for_replacement)
        # The Index object is not callable, and applying the str attribute to a np.array or to a list
        # will result in a single string concatenating all elements from the array. So, we convert
        # the columns index to a pandas series for performing a element-wise string replacement.
        
        # Now, convert the columns to the series with the replaced substrings:
        DATASET.columns = substring_replaced_series
        
    elif (mode == 'trim'):
        # Use the strip method from str attribute with no argument, correspondening to the
        # Trim function.
        DATASET.rename(str.strip, axis = 'columns', inplace = True)
    
    elif (mode == 'eliminate_trailing_characters'):
        
        if ((trailing_substring is None) | (trailing_substring == np.nan)):
            # Apply the str.strip() with no arguments:
            DATASET.rename(str.strip, axis = 'columns', inplace = True)
        
        else:
            # Apply the str attribute to guarantee that numbers were read as strings:
            trailing_substring = str(trailing_substring)

            # Apply the strip method:
            stripped_series = (pd.Series(DATASET.columns)).str.strip(trailing_substring)
            # The Index object is not callable, and applying the str attribute to a np.array or to a list
            # will result in a single string concatenating all elements from the array. So, we convert
            # the columns index to a pandas series for performing a element-wise string replacement.

            # Now, convert the columns to the series with the stripped strings:
            DATASET.columns = stripped_series
    
    else:
        raise InvalidInputsError ("Select a valid mode: \'set_new_names\', \'capitalize_columns\', \'lowercase_columns\', \'replace_substrings\', \'trim\', or \'eliminate_trailing_characters\'.\n")
    
    print("Finished renaming dataframe columns.\n")
    print("Check the new dataframe:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(DATASET)
            
    except: # regular mode
        print(DATASET)
        
    return DATASET
