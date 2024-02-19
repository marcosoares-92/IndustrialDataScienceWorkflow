import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from idsw import (InvalidInputsError, ControlVars)
from .utils import (EncodeDecode, mode_retrieval)


def merge_and_sort_dataframes (df_left, df_right, left_key, right_key, how_to_join = "inner", merged_suffixes = ('_left', '_right'), sort_merged_df = False, column_to_sort = None, ascending_sorting = True):
    """
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
    
    : param: sort_merged_df = False not to sort the merged dataframe. If you want to sort it,
      set as True. If sort_merged_df = True and column_to_sort = None, the dataframe will
      be sorted by its first column.
    
    : param: column_to_sort = None. Keep it None if the dataframe should not be sorted.
      Alternatively, pass a string with a column name to sort, such as:
      column_to_sort = 'col1'; or a list of columns to use for sorting: column_to_sort = 
      ['col1', 'col2']
    
    : param: ascending_sorting = True. If you want to sort the column(s) passed on column_to_sort in
      ascending order, set as True. Set as False if you want to sort in descending order. If
      you want to sort each column passed as list column_to_sort in a specific order, pass a 
      list of booleans like ascending_sorting = [False, True] - the first column of the list
      will be sorted in descending order, whereas the 2nd will be in ascending. Notice that
      the correspondence is element-wise: the boolean in list ascending_sorting will correspond 
      to the sorting order of the column with the same position in list column_to_sort.
      If None, the dataframe will be sorted in ascending order.
    """

    # Create dataframe local copies to manipulate, avoiding that Pandas operates on
    # the original objects; or that Pandas tries to set values on slices or copies,
    # resulting in unpredictable results.
    # Use the copy method to effectively create a second object with the same properties
    # of the input parameters, but completely independent from it.
    DF_LEFT = df_left.copy(deep = True)
    DF_RIGHT = df_right.copy(deep = True)
    
    # check if the keys are the same:
    boolean_check = (left_key == right_key)
    # if boolean_check is True, we will merge using the on parameter, instead of left_on and right_on:
    
    if (boolean_check): # runs if it is True:
        
        merged_df = DF_LEFT.merge(DF_RIGHT, on = left_key, how = how_to_join, suffixes = merged_suffixes)
    
    else:
        # use left_on and right_on
        merged_df = DF_LEFT.merge(DF_RIGHT, left_on = left_key, right_on = right_key, how = how_to_join, suffixes = merged_suffixes)
    
    # Check if the dataframe should be sorted:
    if (sort_merged_df == True):
        
        # check if column_to_sort = None. If it is, set it as the first column (index 0):
        if (column_to_sort is None):
            
            column_to_sort = merged_df.columns[0]
            print(f"Sorting merged dataframe by its first column = {column_to_sort}\n")
        
        # check if ascending_sorting is None. If it is, set it as True:
        if (ascending_sorting is None):
            
            ascending_sorting = True
            print("Sorting merged dataframe in ascending order.\n")
        
        # Now, sort the dataframe according to the parameters:
        merged_df = merged_df.sort_values(by = column_to_sort, ascending = ascending_sorting)
        #sort by the first column, with index 0.
    
        # Now, reset index positions:
        merged_df = merged_df.reset_index(drop = True)
        print("Merged dataframe successfully sorted.\n")
    
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


def record_linkage (df_left, df_right, columns_to_block_as_basis_for_comparison = {'left_df_column': None, 'right_df_column': None}, columns_where_exact_matches_are_required = [{'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}], columns_where_similar_strings_should_be_found = [{'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}], threshold_for_percent_of_similarity = 80.0):
    """
    record_linkage (df_left, df_right, columns_to_block_as_basis_for_comparison = {'left_df_column': None, 'right_df_column': None}, columns_where_exact_matches_are_required = [{'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}], columns_where_similar_strings_should_be_found = [{'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}], threshold_for_percent_of_similarity = 80.0):
    
    WARNING: Only two dataframes can be merged on each call of the function.
    
    Record linkage is the act of linking data from different sources regarding the same entity.
      Generally, we clean two or more DataFrames, generate pairs of potentially matching records, 
      score these pairs according to string similarity and other similarity metrics, and link them.
      Example: we may want to merge data from different clients using the address as key, but there may
      be differences on the format used for registering the addresses.
    
    : param: df_left: dataframe to be joined as the left one.
    
    : param: df_right: dataframe to be joined as the right one
    
    : param: columns_to_block_as_basis_for_comparison = {'left_df_column': None, 'right_df_column': None}
      Dictionary of strings, in quotes. Do not change the keys. If a pair of columns should be
      blocked for being used as basis for merging declare here: in 'left_df_column', input the name
      of the column of the left dataframe. In right_df_column, input the name of the column on the right
      dataframe.
      We first want to generate pairs between both DataFrames. Ideally, we want to generate all
      possible pairs between our DataFrames.
      But, if we had big DataFrames, it is possible that we ende up having to generate millions, 
      if not billions of pairs. It would not prove scalable and could seriously hamper development time.
    
      This is where we apply what we call blocking, which creates pairs based on a matching column, 
      reducing the number of possible pairs.
    
    : param: threshold_for_percent_of_similarity = 80.0 - 0.0% means no similarity and 100% means equal strings.
      The threshold_for_percent_of_similarity is the minimum similarity calculated from the
      Levenshtein (minimum edit) distance algorithm. This distance represents the minimum number of
      insertion, substitution or deletion of characters operations that are needed for making two
      strings equal.
    
    : param: columns_where_exact_matches_are_required = [{'left_df_column': None, 'right_df_column': None}]
    : param: columns_where_similar_strings_should_be_found = [{'left_df_column': None, 'right_df_column': None}]
    
      Both of these arguments have the same structure. The single difference is that
      columns_where_exact_matches_are_required is referent to a group of columns (or a single column)
      where we require perfect correspondence between the dataframes, i.e., where no differences are
      tolerated. Example: the month and day numbers must be precisely the same.
      columns_where_similar_strings_should_be_found, in turns, is referent to the columns where there
      is no rigid standard in the dataset, so similar values should be merged as long as the similarity
      is equal or higher than threshold_for_percent_of_similarity.
    
      Let's check the structure for these arguments, using columns_where_similar_strings_should_be_found
      as example. All instructions are valid for columns_where_exact_matches_are_required.
    
      columns_where_similar_strings_should_be_found =
       [{'left_df_column': None, 'right_df_column': None}]
      This is a list of dictionaries, where each dictionary contains two key-value pairs:
      the first one contains the column name on the left dataframe; and the second one contains the 
      correspondent column on the right dataframe.
      The function will loop through all dictionaries in
      this list, access the values of the key 'left_df_column' to retrieve a column to analyze in the left 
      dataframe; and access access the key 'righ_df_column' to obtain the correspondent column in the right
      dataframe. Then, it will look for potential matches.
      For columns_where_exact_matches_are_required, only columns with perfect correspondence will be
      retrieved. For columns_where_similar_strings_should_be_found, when the algorithm finds a correspondence
      that satisfies the threshold criterium, it will assign it as a match. 
      For instance, suppose you have a word written in too many ways, in a column named 'continent' that
      should be used as key: "EU" , "eur" , "Europ" , "Europa" , "Erope" , "Evropa" ...
      Since they have sufficient similarity, they will be assigned as matching.
    
      The objects columns_where_similar_strings_should_be_found and
      columns_where_exact_matches_are_required must be declared as lists, 
      in brackets, even if there is a single dictionary.
      Use always the same keys: 'left_df_column' and 'right_df_column'.
      Notice that this function performs fuzzy matching, so it MAY SEARCH substrings and strings
      written with different cases (upper or lower) when this portions or modifications make the
      strings sufficiently similar to each other.
    
      If you want, you can remove elements (dictionaries) from the list to declare fewer elements;
      and you can also add more elements (dictionaries) to the lists, if you need to replace more
      values.
      Simply put a comma after the last element from the list and declare a new dictionary, keeping the
      same keys: {'left_df_column': df_left_column, 'right_df_column': df_right_column}, 
      where df_left_column and df_right_column represent the strings for searching and replacement 
      (If the key contains None, the new dictionary will be ignored).
    """

    import recordlinkage
    

    print("Record linkage attempts to join data sources that have similarly fuzzy duplicate values.")
    print("The object is to end up with a final DataFrame with no duplicates by using string similarity.\n")
    
    # Create dataframe local copies to manipulate, avoiding that Pandas operates on
    # the original objects; or that Pandas tries to set values on slices or copies,
    # resulting in unpredictable results.
    # Use the copy method to effectively create a second object with the same properties
    # of the input parameters, but completely independent from it.
    DF_LEFT = df_left.copy(deep = True)
    DF_RIGHT = df_right.copy(deep = True)
    
    # If an invalid value was set for threshold_for_percent_of_similarity, correct it to 80% standard:
                
    if(threshold_for_percent_of_similarity is None):
        threshold_for_percent_of_similarity = 80.0
                
    if((threshold_for_percent_of_similarity == np.nan) | (threshold_for_percent_of_similarity < 0)):
        threshold_for_percent_of_similarity = 80.0
    
    # Convert the threshold for fraction (as required by recordlinkage) and save it as THRESHOLD:
    THRESHOLD = threshold_for_percent_of_similarity/100
    
    # Before finding the pairs, let's check if the column names on the lists of dictionaries are
    # the same. If they are not, let's rename the right dataframe columns so that they are equal to
    # the left one.
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html
    
    # Start a list of valid columns for exact matches:
    valid_columns_exact_matches = []
    
    for dictionary in columns_where_exact_matches_are_required:
        
        # Access elements on keys 'left_df_column' and 'right_df_column':
        left_df_column = dictionary['left_df_column']
        right_df_column = dictionary['right_df_column']
        
        # Check if no key is None:
        if ((left_df_column is not None) & (right_df_column is not None)):
            
            # If right_df_column is different from left_df_column, rename them to
            # make them equal:
            if (left_df_column != right_df_column):
                
                DF_RIGHT.rename(columns = {right_df_column: left_df_column}, inplace = True)
            
            # Add the column to the validated list:
            valid_columns_exact_matches.append(left_df_column)
    
    # Repeat the procedure for the other list:
    # Start a list of valid columns for similar strings:
    valid_columns_similar_str = []
    for dictionary in columns_where_similar_strings_should_be_found:
        
        # Access elements on keys 'left_df_column' and 'right_df_column':
        left_df_column = dictionary['left_df_column']
        right_df_column = dictionary['right_df_column']
        
        # Check if no key is None:
        if ((left_df_column is not None) & (right_df_column is not None)):
            
            # If right_df_column is different from left_df_column, rename them to
            # make them equal:
            if (left_df_column != right_df_column):
                
                DF_RIGHT.rename(columns = {right_df_column: left_df_column}, inplace = True)         
            
            # Add the column to the validated list:
            valid_columns_similar_str.append(left_df_column)

    # Now, we can create the objects for linkage:
    
    # Create an indexer object and find possible pairs:
    indexer = recordlinkage.Index()
    
    left_block = columns_to_block_as_basis_for_comparison['left_df_column']
    
    # Check if left_block is in one of the validated columns list. If it is, right_block
    # may have been renamed, and has the same label left_block:
    if ((left_block in valid_columns_exact_matches) | (left_block in valid_columns_similar_str)):
        
        right_block = left_block
    
    else:
        # right_block was not evaluated yet
        right_block = columns_to_block_as_basis_for_comparison['right_df_column']
    
    if ((left_block is not None) & (right_block is not None)):
        # If they are different, make them equal:
        if (left_block != right_block):
                
            DF_RIGHT.rename(columns = {right_block: left_block}, inplace = True)
        
        # block pairing in this column:
        indexer.block(left_block)
    
    elif (left_block is not None):
        # Try accessing this column on right dataframe:
        try:
            column_block = DF_RIGHT[left_block]
            # If no exception was raised, the column is actually present:
            indexer.block(left_block)
        except:
            pass
    
    elif (right_block is not None):
    # Try accessing this column on left dataframe:
        try:
            column_block = DF_LEFT[right_block]
            # If no exception was raised, the column is actually present:
            indexer.block(right_block)
        except:
            pass
    
    # Now that the columns were renaimed, we can generate the pairs from the object indexer:
    # Generate pairs
    pairs = indexer.index(DF_LEFT, DF_RIGHT)
    # The resulting object, is a pandas multi index object containing pairs of row indices from both 
    # DataFrames, i.e., it is an array containing possible pairs of indices that makes it much easier 
    # to subset DataFrames on.
    
    # Comparing the DataFrames
    # Since we've already generated our pairs, it's time to find potential matches. 
    # We first start by creating a comparison object using the recordlinkage dot compare function. 
    # This is similar to the indexing object we created while generating pairs, but this one is 
    # responsible for assigning different comparison procedures for pairs. 
    # Let's say there are columns for which we want exact matches between the pairs. To do that, 
    # we use the exact method. It takes in the column name in question for each DataFrame, 
    # and a label argument which lets us set the column name in the resulting DataFrame. 
    # Now in order to compute string similarities between pairs of rows for columns that have 
    # fuzzy values, we use the dot string method, which also takes in the column names in question, 
    # the similarity cutoff point in the threshold argument, which takes in a value between 0 and 1.
    # Finally to compute the matches, we use the compute function, which takes in the possible pairs, 
    # and the two DataFrames in question. Note that you need to always have the same order of DataFrames
    # when inserting them as arguments when generating pairs, comparing between columns, 
    # and computing comparisons.
    
    # Create a comparison object
    comp_cl = recordlinkage.Compare()
    
    # Create a counter for assessing the total number of valid columns being analyzed:
    column_counter = len(valid_columns_exact_matches) + len(valid_columns_similar_str)
    
    # Find exact matches for the columns in the list columns_where_exact_matches_are_required.
    # Loop through all elements from the list:
    
    for valid_column in valid_columns_exact_matches:
            
        # set column as the label for merged column:
        LABEL = valid_column
            
        # Find the exact matches:
        comp_cl.exact(valid_column, valid_column, label = LABEL)

    # Now, let's repeat the procedure for the columns where we will look for similar strings
    # for fuzzy matching. These columns were indicated in columns_where_similar_strings_should_be_found.
    # So, loop through all elements from this list:
    for valid_column in valid_columns_similar_str:
        
        # set column as the label for merged column:
        LABEL = valid_column
            
        # Find similar matches:
        comp_cl.string(valid_column, valid_column, label = LABEL, threshold = THRESHOLD) 

    # Now, compute the comparison of the pairs by using the .compute() method of comp_cl,
    # i.e, get potential matches:
    potential_matches = comp_cl.compute(pairs, DF_LEFT, DF_RIGHT)
    # potential_matches is a multi index DataFrame, where the first index is the row index from 
    # the first DataFrame (left), and the second index is a list of all row indices in the right dataframe. 
    # The columns are the columns being compared, with values being 1 for a match, and 0 for not a match.
    
    # The columns of our potential matches are the columns we chose to link both DataFrames on, 
    # where the value is 1 for a match, and 0 otherwise.
    # The first step in linking DataFrames, is to isolate the potentially matching pairs to the ones 
    # we're pretty sure of. We can do it by subsetting the rows where the row sum is above a certain 
    # number of columns: column_counter - 1 (i.e., where the match occurs for all columns, or do not
    # happen for a single column).
    # Isolate potential matches with row sum >=column_counter - 1
    matches = potential_matches[potential_matches.sum(axis = 1) >= (column_counter - 1)]
    
    # matches is row indices between DF_LEFT and DF_RIGHT that are most likely duplicates. 
    # Our next step is to extract the one of the index columns, and subsetting its associated 
    # DataFrame to filter for duplicates.
    
    # Get values of second column index of matches (i.e., indices for DF_RIGHT only).
    # We can access a DataFrame's index using the index attribute. Since this is a multi index 
    # DataFrame, it returns a multi index object containing pairs of row indices from DF_LEFT and 
    # DF_RIGHT respectively. We want to extract all DF_RIGHT indices, so we chain it with the 
    # get_level_values method, which takes in which column index we want to extract its values. 
    # We can either input the index column's name, or its order, which is in this case 1.
    matching_indices = matches.index.get_level_values(1)

    # Subset DF_RIGHT on non-duplicate values (i.e., removing the duplicates 
    # selected as matching_indices).
    # To find the duplicates in DF_RIGHTDF_RIGHT, we can simply subset on all indices of DF_RIGHT, 
    # with the ones found through record linkage. 
    # You can choose to examine them further for similarity with their duplicates in DF_LEFT, 
    # but if you're sure of your analysis, you can go ahead and find the non duplicates with 
    # the exact same line of code, except by adding a tilde at the beginning of your subset. 
    non_dup = DF_RIGHT[~DF_RIGHT.index.isin(matching_indices)]
    # ~ is the not (invert) operator: 
    # https://stackoverflow.com/questions/21415661/logical-operators-for-boolean-indexing-in-pandas
    
    # Append non_dup to DF_LEFT.
    # Now that you have your non duplicates, all you need is a simple append 
    # using the DataFrame append method of DF_LEFT, and you have your linked Data.
    merged_df = pd.concat([DF_LEFT, DF_RIGHT], axis = 0)
    
    # Now, reset index positions:
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


def union_dataframes (list_of_dataframes, what_to_append = 'rows', ignore_index_on_union = True, sort_values_on_union = True, union_join_type = None):
    """
    union_dataframes (list_of_dataframes, what_to_append = 'rows', ignore_index_on_union = True, sort_values_on_union = True, union_join_type = None):
    
    JOIN can be 'inner' to perform an inner join, eliminating the missing values
    The default (None) is 'outer': the dataframes will be stacked on the columns with
    same names but, in case there is no correspondence, the row will present a missing
    value for the columns which are not present in one of the dataframes.
    When using the 'inner' method, only the common columns will remain
    
    : param: list_of_dataframes must be a list containing the dataframe objects
      example: list_of_dataframes = [df1, df2, df3, df4]
      Notice that the dataframes are objects, not strings. Therefore, they should not
      be declared inside quotes.
      There is no limit of dataframes. In this example, we will concatenate 4 dataframes.
      If list_of_dataframes = [df1, df2, df3] we would concatenate 3, and if
      list_of_dataframes = [df1, df2, df3, df4, df5] we would concatenate 5 dataframes.
    
    : param: what_to_append = 'rows' for appending the rows from one dataframe
      into the other; what_to_append = 'columns' for appending the columns
      from one dataframe into the other (horizontal or lateral append).
    
      When what_to_append = 'rows', Pandas .concat method is defined as
      axis = 0, i.e., the operation occurs in the row level, so the rows
      of the second dataframe are added to the bottom of the first one.
      It is the SQL union, and creates a dataframe with more rows, and
      total of columns equals to the total of columns of the first dataframe
      plus the columns of the second one that were not in the first dataframe.
      When what_to_append = 'columns', Pandas .concat method is defined as
      axis = 1, i.e., the operation occurs in the column level: the two
      dataframes are laterally merged using the index as the key, 
      preserving all columns from both dataframes. Therefore, the number of
      rows will be the total of rows of the dataframe with more entries,
      and the total of columns will be the sum of the total of columns of
      the first dataframe with the total of columns of the second dataframe.
    
    The other parameters are the same from Pandas .concat method.
    : param: ignore_index_on_union = ignore_index;
    : param: sort_values_on_union = sort
    : param: union_join_type = join
    
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.concat.html
    
    Check Datacamp course Joining Data with pandas, Chap.3, 
     Advanced Merging and Concatenating
    """
    
    # Create dataframe local copies to manipulate, avoiding that Pandas operates on
    # the original objects; or that Pandas tries to set values on slices or copies,
    # resulting in unpredictable results.
    # Use the copy method to effectively create a second object with the same properties
    # of the input parameters, but completely independent from it.

    # Start a list of copied dataframes:
    LIST_OF_DATAFRAMES = []
    
    # Loop through each element from list_of_dataframes:
    for dataframe in list_of_dataframes:
        
        # create a copy of the object:
        copied_df = dataframe.copy(deep = True)
        # Append this element to the LIST_OF_DATAFRAMES:
        LIST_OF_DATAFRAMES.append(copied_df)
    
    # Check axis:
    if (what_to_append == 'rows'):
        
        AXIS = 0
    
    elif (what_to_append == 'columns'):
        
        AXIS = 1
        
        # In this case, we must save a list of columns of each one of the dataframes, containing
        # the different column names observed. That is because the concat method eliminates the
        # original column names when AXIS = 1
        # We can start the LIST_OF_COLUMNS as the columns from the first object on the
        # LIST_OF_DATAFRAMES, eliminating one iteration cycle. Since the columns method generates
        # an array, we use the list attribute to convert the array to a regular list:
        
        i = 0
        analyzed_df = LIST_OF_DATAFRAMES[i]
        LIST_OF_COLUMNS = list(analyzed_df.columns)
        
        # Now, loop through each other element on LIST_OF_DATAFRAMES. Since index 0 was already
        # considered, start from index 1:
        for i in range (1, len(LIST_OF_DATAFRAMES)):
            
            analyzed_df = LIST_OF_DATAFRAMES[i]
            
            # Now, loop through each column, named 'col', from the list of columns of analyzed_df:
            for col in list(analyzed_df.columns):
                
                # If 'col' is not in LIST_OF_COLUMNS, append it to the list with its current name.
                # The order of the columns on the concatenated dataframe will be the same (the order
                # they appear):
                if not (col in LIST_OF_COLUMNS):
                    LIST_OF_COLUMNS.append(col)
                
                else:
                    # There is already a column with this name. So, append col with a suffix:
                    LIST_OF_COLUMNS.append(col + "_df_" + str(i))
                    
        # Now, we have a list of all column names, that we will use for retrieving the headers after
        # concatenation.
    
    else:
        print("No valid string was input to what_to_append, so appending rows (vertical append, equivalent to SQL UNION).\n")
        AXIS = 0
    
    if (union_join_type == 'inner'):
        
        print("Warning: concatenating dataframes using the \'inner\' join method, that removes missing values.\n")
        concat_df = pd.concat(LIST_OF_DATAFRAMES, axis = AXIS, ignore_index = ignore_index_on_union, sort = sort_values_on_union, join = union_join_type)
    
    else:
        
        #In case None or an invalid value is provided, use the default 'outer', by simply
        # not declaring the 'join':
        concat_df = pd.concat(LIST_OF_DATAFRAMES, axis = AXIS, ignore_index = ignore_index_on_union, sort = sort_values_on_union)
    
    if (AXIS == 1):
        # If we concatentated columns, we lost the columns' names (headers). So, use the list
        # LIST_OF_COLUMNS as the new headers for this case:
        concat_df.columns = LIST_OF_COLUMNS
    
    # Pandas .head(Y) method results in a dataframe containing the first Y rows of the 
    # original dataframe. The default .head() is Y = 5. Print first 10 rows of the 
    # new dataframe:
    if ControlVars.show_results:
        print("Dataframes successfully concatenated. Check the 10 first rows of new dataframe:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(concat_df.head(10))
                
        except: # regular mode
            print(concat_df.head(10))
    
    #Now return the concatenated dataframe:
    
    return concat_df


def group_dataframe_by_variable (df, variable_to_group_by, return_summary_dataframe = False, subset_of_columns_to_aggregate = None, aggregate_function = 'mean', add_suffix_to_aggregated_col = True, suffix = None):
    """
    group_dataframe_by_variable (df, variable_to_group_by, return_summary_dataframe = False, subset_of_columns_to_aggregate = None, aggregate_function = 'mean', add_suffix_to_aggregated_col = True, suffix = None):

    : param: df: dataframe being analyzed
    
    : param: variable_to_group_by: string (inside quotes) containing the name 
      of the column in terms of which the dataframe will be grouped by. e.g. 
      variable_to_group_by = "column1" will group the dataframe in terms of 'column1'.
      WARNING: do not use this function to group a dataframe in terms of a timestamp. To group by
      a timestamp, use function group_variables_by_timestamp instead.
    
    : param: return_summary_dataframe = False. Set return_summary_dataframe = True if you want the function
      to return a dataframe containing summary statistics (obtained with the describe method).
    
    : param: subset_of_columns_to_aggregate: list of strings (inside quotes) containing the names 
      of the columns that will be aggregated. Use this argument if you want to aggregate only a subset,
      not the whole dataframe. Declare as a list even if there is a single column to group by.
      e.g. subset_of_columns_to_aggregate = ["response_feature"] will return the column 
      'response_feature' grouped. subset_of_columns_to_aggregate = ["col1", 'col2'] will return columns
      'col1' and 'col2' grouped.
      If you want to aggregate the whole subset, keep subset_of_columns_to_aggregate = None.
    
    : param: aggregate_function = 'mean': String defining the aggregation 
      method that will be applied. Possible values:
      'median', 'mean', 'mode', 'sum', 'min', 'max', 'variance', 'count',
      'standard_deviation', 'cum_sum', 'cum_prod', 'cum_max', 'cum_min',
      '10_percent_quantile', '20_percent_quantile',
      '25_percent_quantile', '30_percent_quantile', '40_percent_quantile',
      '50_percent_quantile', '60_percent_quantile', '70_percent_quantile',
      '75_percent_quantile', '80_percent_quantile', '90_percent_quantile',
      '95_percent_quantile', 'kurtosis', 'skew', 'interquartile_range',
      'mean_standard_error', 'entropy'
      To use another aggregate function, you can use the .agg method, passing 
      the aggregate as argument, such as in:
      .agg(scipy.stats.mode), 
      where the argument is a Scipy aggregate function.
      If None or an invalid function is input, 'mean' will be used.
    
    : param: add_suffix_to_aggregated_col = True will add a suffix to the
      aggregated columns. e.g. 'responseVar_mean'. If add_suffix_to_aggregated_col 
      = False, the aggregated column will have the original column name.
    
    : param: suffix = None. Keep it None if no suffix should be added, or if
      the name of the aggregate function should be used as suffix, after
      "_". Alternatively, set it as a string. As recommendation, put the
      "_" sign in the beginning of this string to separate the suffix from
      the original column name. e.g. if the response variable is 'Y' and
      suffix = '_agg', the new aggregated column will be named as 'Y_agg'
    """

    from scipy import stats
    
    print("WARNING: Do not use this function to group the dataframe in terms of a timestamp. For this purpose, use function group_variables_by_timestamp.\n")
    
    # Create a local copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    
    # Get the list of columns:
    cols_list = list(DATASET.columns)
    
    if (subset_of_columns_to_aggregate is not None):
        
        # cols_list will be the subset list:
        cols_list = subset_of_columns_to_aggregate
    
    # Start a list of numerical columns, and a list of categorical columns, containing only the
    # column for aggregation as the first element:
    numeric_list = [variable_to_group_by]
    categorical_list = [variable_to_group_by]
    # List the possible numeric data types for a Pandas dataframe column:
    numeric_dtypes = [np.int16, np.int32, np.int64, np.float16, np.float32, np.float64]
    
    # Loop through all valid columns (cols_list)
    for column in cols_list:
        
        # Check if the column is neither in numeric_list nor in
        # categorical_list yet:
        if ((column not in numeric_list) & (column not in categorical_list)):
            
            column_data_type = DATASET[column].dtype
            
            if (column_data_type not in numeric_dtypes):
                
                # Append to categorical columns list:
                categorical_list.append(column)
            
            else:
                # Append to numerical columns list:
                numeric_list.append(column)
    
    # Create variables to map if both are present.
    is_categorical = 0
    is_numeric = 0
    
    # Before grouping, let's remove the missing values, avoiding the raising of TypeError.
    # Pandas deprecated the automatic dropna with aggregation:
    DATASET = DATASET.dropna(axis = 0)
    # It is important to drop before seggregating the dataframes, so that the rows correspondence
    # will not be lost:
    DATASET = DATASET.reset_index(drop = True)
    
    # Convert variable_to_group_by to Pandas 'category' type. If the variable is represented by
    # a number, the dataframe will be grouped in terms of an aggregation of the variable, instead
    # of as a category. It will prevents this to happen:
    DATASET[variable_to_group_by] = DATASET[variable_to_group_by].astype("category")
    
    # Create two subsets:
    if (len(categorical_list) > 1):
        
        # Has at least one column plus the variable_to_group_by:
        df_categorical = DATASET.copy(deep = True)
        df_categorical = df_categorical[categorical_list]
        is_categorical = 1
    
    if (len(numeric_list) > 1):
        
        df_numeric = DATASET.copy(deep = True)
        df_numeric = df_numeric[numeric_list]
        is_numeric = 1
        
    if (return_summary_dataframe):
        summary_agg_df = DATASET.copy(deep = True)
        summary_agg_df = summary_agg_df.groupby(by = variable_to_group_by, as_index = False, sort = True).describe()
            
    # Notice that the variables is_numeric and is_categorical have value 1 only when the subsets
    # are present.
    is_cat_num = is_categorical + is_numeric
    # is_cat_num = 0 if no valid dataset was input.
    # is_cat_num = 2 if both subsets are present.
    
    # Before calling the method, we must guarantee that the variables may be
    # used for that aggregate. Some aggregations are permitted only for numeric variables, so calling
    # the method before selecting the variables may raise warnings or errors.
    list_of_aggregates = ['median', 'mean', 'mode', 'sum', 'min', 'max', 'variance',
                        'standard_deviation', 'count', 'cum_sum', 'cum_prod', 'cum_max', 'cum_min',
                        '10_percent_quantile', '20_percent_quantile', '25_percent_quantile', 
                        '30_percent_quantile', '40_percent_quantile', '50_percent_quantile', 
                        '60_percent_quantile', '70_percent_quantile', '75_percent_quantile', 
                        '80_percent_quantile', '90_percent_quantile', '95_percent_quantile',  
                        'kurtosis', 'skew', 'interquartile_range', 'mean_standard_error', 'entropy']
    
    list_of_numeric_aggregates = ['median', 'mean', 'sum', 'min', 'max', 'variance',
                        'standard_deviation', 'cum_sum', 'cum_prod', 'cum_max', 'cum_min',
                        '10_percent_quantile', '20_percent_quantile', '25_percent_quantile', 
                        '30_percent_quantile', '40_percent_quantile', '50_percent_quantile', 
                        '60_percent_quantile', '70_percent_quantile', '75_percent_quantile', 
                        '80_percent_quantile', '90_percent_quantile', '95_percent_quantile',  
                        'kurtosis', 'skew', 'interquartile_range', 'mean_standard_error']
    
    # Check if an invalid or no aggregation function was selected:
    if ((aggregate_function not in (list_of_aggregates)) | (aggregate_function is None)):
        
        aggregate_function = 'mean'
        print("Invalid or no aggregation function input, so using the default \'mean\'.\n")
    
    # Check if a numeric aggregate was selected:
    if (aggregate_function in list_of_numeric_aggregates):
        
        print("Numeric aggregate selected. Categorical variables will be aggregated in terms of mode, the most common value.\n")
        
        numeric_aggregate = aggregate_function
        categorical_aggregate = 'mode'
    
    else:
        
        print("Categorical aggregate selected. Numeric variables will be aggregated in terms of mean.\n")
        
        categorical_aggregate = aggregate_function
        numeric_aggregate = 'mean'
    
    if (is_numeric == 1):
        # Let's aggregate the numeric subset
    
        if (numeric_aggregate == 'median'):

            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).agg('median')

        elif (numeric_aggregate == 'mean'):

            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).mean()
        
        elif (numeric_aggregate == 'sum'):
        
            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).sum()
    
        elif (numeric_aggregate == 'min'):
        
            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).min()

        elif (numeric_aggregate == 'max'):

            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).max()

        elif (numeric_aggregate == 'variance'):

            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).var()

        elif (numeric_aggregate == 'standard_deviation'):

            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).std()

        elif (numeric_aggregate == 'cum_sum'):

            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).cumsum()

        elif (numeric_aggregate == 'cum_prod'):

            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).cumprod()

        elif (numeric_aggregate == 'cum_max'):

            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).cummax()

        elif (numeric_aggregate == 'cum_min'):

            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).cummin()

        elif (numeric_aggregate == '10_percent_quantile'):

            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).quantile(0.10)

        elif (numeric_aggregate == '20_percent_quantile'):

            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).quantile(0.20)

        elif (numeric_aggregate == '25_percent_quantile'):

            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).quantile(0.25)

        elif (numeric_aggregate == '30_percent_quantile'):

            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).quantile(0.30)

        elif (numeric_aggregate == '40_percent_quantile'):

            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).quantile(0.40)

        elif (numeric_aggregate == '50_percent_quantile'):

            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).quantile(0.50)

        elif (numeric_aggregate == '60_percent_quantile'):

            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).quantile(0.60)

        elif (numeric_aggregate == '70_percent_quantile'):

            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).quantile(0.30)

        elif (numeric_aggregate == '75_percent_quantile'):

            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).quantile(0.75)

        elif (numeric_aggregate == '80_percent_quantile'):

            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).quantile(0.80)

        elif (numeric_aggregate == '90_percent_quantile'):

            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).quantile(0.90)

        elif (numeric_aggregate == '95_percent_quantile'):

            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).quantile(0.95)

        elif (numeric_aggregate == 'kurtosis'):

            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).agg(stats.kurtosis)

        elif (numeric_aggregate == 'skew'):

            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).agg(stats.skew)

        elif (numeric_aggregate == 'interquartile_range'):

            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).agg(stats.iqr)

        elif (numeric_aggregate == 'mean_standard_error'):

            df_numeric = df_numeric.groupby(by = variable_to_group_by, as_index = False, sort = True).agg(stats.sem)
        
        
        if (add_suffix_to_aggregated_col == True):
        
            # Let's add a suffix. Check if suffix is None. If it is,
            # set "_" + aggregate_function as suffix:
            if (suffix is None):
                numeric_suffix = "_" + numeric_aggregate
            
            else:
                numeric_suffix = suffix
            
            # New columns names:
            new_num_names = [(str(name) + numeric_suffix) for name in numeric_list]
            # The str attribute guarantees that the name was read as string
            # Pick only the values from the second and concatenate the correct name 
            # for the aggregation column (eliminate the first element from the list):
            new_num_names = [variable_to_group_by] + new_num_names[1:]
            # Set new_num_names as the new columns names:
            df_numeric.columns = new_num_names
    
    if (is_categorical == 1):
        # Let's aggregate the categorical subset
        # stats.mode now only works for numerically encoded variables (the previous ordinal
        # encoding is required)
        # Encode to calculate the mode:
        enc_dec_obj = EncodeDecode(df_categorical = df_categorical, categorical_list = categorical_list)
        enc_dec_obj = enc_dec_obj.encode()
        df_categorical, new_encoded_cols, ordinal_encoding_list = enc_dec_obj.df_categorical, enc_dec_obj.new_encoded_cols, enc_dec_obj.ordinal_encoding_list

        if variable_to_group_by in categorical_list:
            variable_to_group_by = variable_to_group_by + "_OrdinalEnc"

        if (categorical_aggregate == 'mode'):
            
            df_categorical = df_categorical.groupby(by = variable_to_group_by, as_index = False, sort = True).agg(stats.mode)
            
            # Loop through each categorical variable:
            for cat_var in new_encoded_cols:

                df_categorical[cat_var] = mode_retrieval(df_categorical[cat_var])

        elif (categorical_aggregate == 'count'):

            df_categorical = df_categorical.groupby(by = variable_to_group_by, as_index = False, sort = True).count()

        elif (categorical_aggregate == 'entropy'):

            df_categorical = df_categorical.groupby(by = variable_to_group_by, as_index = False, sort = True).agg(stats.entropy)
        
        # Now, reverse encoding:
        enc_dec_obj = enc_dec_obj.decode(new_df = df_categorical)
        df_categorical, cleaned_df = enc_dec_obj.df_categorical, enc_dec_obj.cleaned_df
        
        if (add_suffix_to_aggregated_col == True):
        
            # Let's add a suffix. Check if suffix is None. If it is,
            # set "_" + aggregate_function as suffix:
            if (suffix is None):
                categorical_suffix = "_" + categorical_aggregate
            
            else:
                categorical_suffix = suffix
            
            # New columns names:
            new_cat_names = [(str(name) + categorical_suffix) for name in categorical_list]
            # The str attribute guarantees that the name was read as string
            # Pick only the values from the second and concatenate the correct name 
            # for the aggregation column (eliminate the first element from the list):
            new_cat_names = [variable_to_group_by] + new_cat_names[1:]
            # Set new_num_names as the new columns names:
            df_categorical.columns = new_cat_names
    
    if (is_cat_num == 2):
        # Both subsets are present. Remove the column from df_categorical:
        df_categorical.drop(columns = variable_to_group_by, inplace = True)
        
        # Concatenate the dataframes in the columns axis (append columns):
        DATASET = pd.concat([df_numeric, df_categorical], axis = 1, join = "inner")
    
    elif (is_categorical == 1):
        # There is only the categorical subset:
        DATASET = df_categorical
    
    elif (is_numeric == 1):
        # There is only the numeric subset:
        DATASET = df_numeric
    
    else:
        print("No valid dataset provided, so returning the input dataset itself.\n")
    
    # Now, reset index positions:
    DATASET = DATASET.reset_index(drop = True)
    
    if ControlVars.show_results:
        print("Dataframe successfully grouped. Check its 10 first rows:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(DATASET.head(10))
                
        except: # regular mode
            print(DATASET.head(10))
    
    if (return_summary_dataframe == True):
        
        if ControlVars.show_results:
            print("\n")
            print("Check the summary statistics dataframe, that is also being returned:\n")
            
            try:
                # only works in Jupyter Notebook:
                from IPython.display import display
                display(summary_agg_df)

            except: # regular mode
                print(summary_agg_df)
        
        return DATASET, summary_agg_df
    
    else:
        # return only the aggregated dataframe:
        return DATASET
