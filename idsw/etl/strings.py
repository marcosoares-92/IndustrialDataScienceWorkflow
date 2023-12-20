import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from idsw.datafetch.core import InvalidInputsError
from .core import RegexHelp


def trim_spaces_or_characters (df, column_to_analyze, new_variable_type = None, method = 'trim', substring_to_eliminate = None, create_new_column = True, new_column_suffix = "_trim"):
    """
    trim_spaces_or_characters (df, column_to_analyze, new_variable_type = None, method = 'trim', substring_to_eliminate = None, create_new_column = True, new_column_suffix = "_trim"):
    
    : param: column_to_analyze: string (inside quotes), 
      containing the name of the column that will be analyzed. 
      e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    : param: new_variable_type = None. String (in quotes) that represents a given data type for the column
      after transformation. Set:
      - new_variable_type = 'int' to convert the column to integer type after the transform;
      - new_variable_type = 'float' to convert the column to float (decimal number);
      - new_variable_type = 'datetime' to convert it to date or timestamp;
      - new_variable_type = 'category' to convert it to Pandas categorical variable.
    
    : param: method = 'trim' will eliminate trailing and leading white spaces from the strings in
      column_to_analyze.
      method = 'substring' will eliminate a defined trailing and leading substring from
      column_to_analyze.
    
    : param: substring_to_eliminate = None. Set as a string (in quotes) if method = 'substring'.
      e.g. suppose column_to_analyze contains time information: each string ends in " min":
      "1 min", "2 min", "3 min", etc. If substring_to_eliminate = " min", this portion will be
      eliminated, resulting in: "1", "2", "3", etc. If new_variable_type = None, these values will
      continue to be strings. By setting new_variable_type = 'int' or 'float', the series will be
      converted to a numeric type.
    
    : param: create_new_column = True
      Alternatively, set create_new_column = True to store the transformed data into a new
      column. Or set create_new_column = False to overwrite the existing column.
    
    : param: new_column_suffix = "_trim"
      This value has effect only if create_new_column = True.
      The new column name will be set as column + new_column_suffix. Then, if the original
      column was "column1" and the suffix is "_trim", the new column will be named as
      "column1_trim".
      Alternatively, input inside quotes a string with the desired suffix. Recommendation:
      start the suffix with "_" to separate it from the original name.
    """

    # Set a local copy of dataframe to manipulate
    DATASET = df.copy(deep = True)
    # Guarantee that the column to analyze was read as string:
    DATASET[column_to_analyze] = (DATASET[column_to_analyze]).astype(str)
    new_series = DATASET[column_to_analyze].copy()
    
    if (method == 'substring'):
        
        if (substring_to_eliminate is None):
            
            method = 'trim'
            print("No valid substring input. Modifying method to \'trim\'.\n")
    
    if (method == 'substring'):
        
        print("ATTENTION: Operations of string strip (removal) or replacement are all case-sensitive. There must be correct correspondence between cases and spaces for the strings being removed or replaced.\n")
        # For manipulating strings, call the str attribute and, then, the method to be applied:
        new_series = new_series.str.strip(substring_to_eliminate)
    
    else:
        
        new_series = new_series.str.strip()
    
    # Check if a the series type should be modified:
    if (new_variable_type is not None):
        
        if (new_variable_type == 'int'):

            new_type = np.int64

        elif (new_variable_type == 'float'):
            
            new_type = np.float64
        
        elif (new_variable_type == 'datetime'):
            
            new_type = 'datetime64[ns]'
        
        elif (new_variable_type == 'category'):
            
            new_type = new_variable_type
        
        # Try converting the type:
        try:
            new_series = new_series.astype(new_type)
            print(f"Successfully converted the series to the type {new_variable_type}.\n")
        
        except:
            pass

    if (create_new_column):
        
        if (new_column_suffix is None):
            new_column_suffix = "_trim"
                
        new_column_name = column_to_analyze + new_column_suffix
        DATASET[new_column_name] = new_series
            
    else:
        
        DATASET[column_to_analyze] = new_series
    
    # Now, we are in the main code.
    print("Finished removing leading and trailing spaces or characters (substrings).")
    print("Check the 10 first elements from the series:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(new_series.head(10))
            
    except: # regular mode
        print(new_series.head(10))
    
    return DATASET


def capitalize_or_lower_string_case (df, column_to_analyze, method = 'lowercase', create_new_column = True, new_column_suffix = "_homogenized"):
    """
    capitalize_or_lower_string_case (df, column_to_analyze, method = 'lowercase', create_new_column = True, new_column_suffix = "_homogenized"):
    
    : param: column_to_analyze: string (inside quotes), 
      containing the name of the column that will be analyzed. 
      e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    : param: method = 'capitalize' will capitalize all letters from the input string 
      (turn them to upper case).
      method = 'lowercase' will make the opposite: turn all letters to lower case.
      e.g. suppose column_to_analyze contains strings such as 'String One', 'STRING 2',  and
      'string3'. If method = 'capitalize', the output will contain the strings: 
      'STRING ONE', 'STRING 2', 'STRING3'. If method = 'lowercase', the outputs will be:
      'string one', 'string 2', 'string3'.
    
    : param: create_new_column = True
      Alternatively, set create_new_columns = True to store the transformed data into a new
      column. Or set create_new_column = False to overwrite the existing column.
    
    : param: new_column_suffix = "_homogenized"
      This value has effect only if create_new_column = True.
      The new column name will be set as column + new_column_suffix. Then, if the original
      column was "column1" and the suffix is "_homogenized", the new column will be named as
      "column1_homogenized".
      Alternatively, input inside quotes a string with the desired suffix. Recommendation:
      start the suffix with "_" to separate it from the original name.
    """
    
    # Set a local copy of dataframe to manipulate
    DATASET = df.copy(deep = True)
    # Guarantee that the column to analyze was read as string:
    DATASET[column_to_analyze] = (DATASET[column_to_analyze]).astype(str)
    new_series = DATASET[column_to_analyze].copy()
    
    if (method == 'capitalize'):
        
        print("Capitalizing the string (moving all characters to upper case).\n")
        # For manipulating strings, call the str attribute and, then, the method to be applied:
        new_series = new_series.str.upper()
    
    else:
        
        print("Lowering the string case (moving all characters to lower case).\n")
        new_series = new_series.str.lower()
        
    if (create_new_column):
        
        if (new_column_suffix is None):
            new_column_suffix = "_homogenized"
                
        new_column_name = column_to_analyze + new_column_suffix
        DATASET[new_column_name] = new_series
            
    else:
        
        DATASET[column_to_analyze] = new_series
    
    # Now, we are in the main code.
    print(f"Finished homogenizing the string case of {column_to_analyze}, giving value consistency.")
    print("Check the 10 first elements from the series:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(new_series.head(10))
            
    except: # regular mode
        print(new_series.head(10))
    
    return DATASET


def add_contractions_to_library (list_of_contractions = [{'contracted_expression': None, 'correct_expression': None}, {'contracted_expression': None, 'correct_expression': None}, {'contracted_expression': None, 'correct_expression': None}, {'contracted_expression': None, 'correct_expression': None}]):
    """
    add_contractions_to_library (list_of_contractions = [{'contracted_expression': None, 'correct_expression': None}, {'contracted_expression': None, 'correct_expression': None}, {'contracted_expression': None, 'correct_expression': None}, {'contracted_expression': None, 'correct_expression': None}]):
    
    contractions library: https://github.com/kootenpv/contractions
    
    : param: list_of_contractions = 
      [{'contracted_expression': None, 'correct_expression': None}]
      This is a list of dictionaries, where each dictionary contains two key-value pairs:
      the first one contains the form as the contraction is usually observed; and the second one 
      contains the correct (full) string that will replace it.
      Since contractions can cause issues when processing text, we can expand them with these functions.
    
      The object list_of_contractions must be declared as a list, 
      in brackets, even if there is a single dictionary.
      Use always the same keys: 'contracted_expression' for the contraction; and 'correct_expression', 
      for the strings with the correspondent correction.
    
      If you want, you can remove elements (dictionaries) from the list to declare fewer elements;
      and you can also add more elements (dictionaries) to the lists, if you want to add more elements
      to the contractions library.
      Simply put a comma after the last element from the list and declare a new dictionary, keeping the
      same keys: {'contracted_expression': original_str, 'correct_expression': new_str}, 
      where original_str and new_str represent the contracted and expanded strings
      (If one of the keys contains None, the new dictionary will be ignored).
    
      Example:
      list_of_contractions = [{'contracted_expression': 'mychange', 'correct_expression': 'my change'}]
    """

    import contractions
    
    
    for dictionary in list_of_contractions:
        
        contraction = dictionary['contracted_expression']
        correction = dictionary['correct_expression']
        
        if ((contraction is not None) & (correction is not None)):
    
            contractions.add(contraction, correction)
            print(f"Successfully included the contracted expression {contraction} to the contractions library.")

    print("Now, the function for contraction correction will be able to process it within the strings.\n")


def correct_contracted_strings (df, column_to_analyze, create_new_column = True, new_column_suffix = "_contractionsFixed"):
    """
    correct_contracted_strings (df, column_to_analyze, create_new_column = True, new_column_suffix = "_contractionsFixed"):
    
    contractions library: https://github.com/kootenpv/contractions
    
    : param: column_to_analyze: string (inside quotes), 
      containing the name of the column that will be analyzed. 
      e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.

    : param: create_new_column = True
      Alternatively, set create_new_columns = True to store the transformed data into a new
      column. Or set create_new_column = False to overwrite the existing column.
    
    : param: new_column_suffix = "_contractionsFixed"
      This value has effect only if create_new_column = True.
      The new column name will be set as column + new_columns_suffix. Then, if the original
      column was "column1" and the suffix is "_contractionsFixed", the new column will be named as
      "column1_contractionsFixed".
      Alternatively, input inside quotes a string with the desired suffix. Recommendation:
      start the suffix with "_" to separate it from the original name.
    """

    import contractions
    
    # Set a local copy of dataframe to manipulate
    DATASET = df.copy(deep = True)
    DATASET[column_to_analyze] = (DATASET[column_to_analyze]).astype(str)
    new_series = DATASET[column_to_analyze].copy()
    
    # Contractions operate at one string at once:
    correct_contractions_list = [contractions.fix(new_series[i], slang = True) for i in range (0, len(DATASET))]
    
    # Make this list the new_series itself:
    new_series = pd.Series(correct_contractions_list)
    
    if (create_new_column):
            
        if (new_column_suffix is None):
            new_column_suffix = "_contractionsFixed"

        new_column_name = column_to_analyze + new_column_suffix
        DATASET[new_column_name] = new_series
            
    else:

        DATASET[column_to_analyze] = new_series

    # Now, we are in the main code.
    print(f"Finished correcting the contracted strings from column {column_to_analyze}.")
    print("Check the 10 first elements (10 lists) from the series:\n")

    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(new_series.head(10))

    except: # regular mode
        print(new_series.head(10))

    return DATASET


def replace_substring (df, column_to_analyze, substring_to_be_replaced = None, new_substring_for_replacement = '', create_new_column = True, new_column_suffix = "_substringReplaced"):
    """
    replace_substring (df, column_to_analyze, substring_to_be_replaced = None, new_substring_for_replacement = '', create_new_column = True, new_column_suffix = "_substringReplaced"):
    
    : param: column_to_analyze: string (inside quotes), 
      containing the name of the column that will be analyzed. 
      e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    : param: substring_to_be_replaced = None; new_substring_for_replacement = ''. 
      Strings (in quotes): when the sequence of characters substring_to_be_replaced was
      found in the strings from column_to_analyze, it will be substituted by the substring
      new_substring_for_replacement. If None is provided to one of these substring arguments,
      it will be substituted by the empty string: ''
      e.g. suppose column_to_analyze contains the following strings, with a spelling error:
      "my collumn 1", 'his collumn 2', 'her column 3'. We may correct this error by setting:
      substring_to_be_replaced = 'collumn' and new_substring_for_replacement = 'column'. The
      function will search for the wrong group of characters and, if it finds it, will substitute
      by the correct sequence: "my column 1", 'his column 2', 'her column 3'.
    
    : param: create_new_column = True
      Alternatively, set create_new_columns = True to store the transformed data into a new
      column. Or set create_new_column = False to overwrite the existing column.
    
    : param: new_column_suffix = "_substringReplaced"
      This value has effect only if create_new_column = True.
      The new column name will be set as column + new_column_suffix. Then, if the original
      column was "column1" and the suffix is "_substringReplaced", the new column will be named as
      "column1_substringReplaced".
      Alternatively, input inside quotes a string with the desired suffix. Recommendation:
      start the suffix with "_" to separate it from the original name.
    """
    
    # Set a local copy of dataframe to manipulate
    DATASET = df.copy(deep = True)
    # Guarantee that the column to analyze was read as string:
    DATASET[column_to_analyze] = (DATASET[column_to_analyze]).astype(str)
    new_series = DATASET[column_to_analyze].copy()
    
    print("ATTENTION: Operations of string strip (removal) or replacement are all case-sensitive. There must be correct correspondence between cases and spaces for the strings being removed or replaced.\n")
        
    # If one of the input substrings is None, make it the empty string:
    if (substring_to_be_replaced is None):
        substring_to_be_replaced = ''
    
    if (new_substring_for_replacement is None):
        new_substring_for_replacement = ''
    
    # Guarantee that both were read as strings (they may have been improperly read as 
    # integers or floats):
    substring_to_be_replaced = str(substring_to_be_replaced)
    new_substring_for_replacement = str(new_substring_for_replacement)
    
    # For manipulating strings, call the str attribute and, then, the method to be applied:
    new_series = new_series.str.replace(substring_to_be_replaced, new_substring_for_replacement)
        
    if (create_new_column):
        
        if (new_column_suffix is None):
            new_column_suffix = "_substringReplaced"
                
        new_column_name = column_to_analyze + new_column_suffix
        DATASET[new_column_name] = new_series
            
    else:
        
        DATASET[column_to_analyze] = new_series
    
    # Now, we are in the main code.
    print(f"Finished replacing the substring {substring_to_be_replaced} by {new_substring_for_replacement}.")
    print("Check the 10 first elements from the series:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(new_series.head(10))
            
    except: # regular mode
        print(new_series.head(10))
    
    return DATASET


def invert_strings (df, column_to_analyze, create_new_column = True, new_column_suffix = "_stringInverted"):
    """
    invert_strings (df, column_to_analyze, create_new_column = True, new_column_suffix = "_stringInverted"):
    
    : param: column_to_analyze: string (inside quotes), 
      containing the name of the column that will be analyzed. 
      e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    : param: create_new_column = True
      Alternatively, set create_new_columns = True to store the transformed data into a new
      column. Or set create_new_column = False to overwrite the existing column.
    
    : param: new_column_suffix = "_stringInverted"
      This value has effect only if create_new_column = True.
      The new column name will be set as column + new_columns_suffix. Then, if the original
      column was "column1" and the suffix is "_stringInverted", the new column will be named as
      "column1_stringInverted".
      Alternatively, input inside quotes a string with the desired suffix. Recommendation:
      start the suffix with "_" to separate it from the original name.
    """
    
    # Set a local copy of dataframe to manipulate
    DATASET = df.copy(deep = True)
    # Guarantee that the column to analyze was read as string:
    DATASET[column_to_analyze] = (DATASET[column_to_analyze]).astype(str)
    new_series = DATASET[column_to_analyze].copy()
    
    # Pandas slice: start from -1 (last character) and go to the last element with -1 step
    # walk through the string 'backwards':
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.slice.html
    
    new_series = new_series.str.slice(start = -1, step = -1)
    
    if (create_new_column):
            
        if (new_column_suffix is None):
            new_column_suffix = "_stringInverted"

        new_column_name = column_to_analyze + new_column_suffix
        DATASET[new_column_name] = new_series
            
    else:

        DATASET[column_to_analyze] = new_series

    # Now, we are in the main code.
    print(f"Finished inversion of the strings.")
    print("Check the 10 first elements from the series:\n")

    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(new_series.head(10))

    except: # regular mode
        print(new_series.head(10))

    return DATASET


def slice_strings (df, column_to_analyze, first_character_index = None, last_character_index = None, step = 1, create_new_column = True, new_column_suffix = "_slicedString"):
    """
    slice_strings (df, column_to_analyze, first_character_index = None, last_character_index = None, step = 1, create_new_column = True, new_column_suffix = "_slicedString"):
    
    : param: column_to_analyze: string (inside quotes), 
      containing the name of the column that will be analyzed. 
      e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    : param: create_new_column = True
      Alternatively, set create_new_columns = True to store the transformed data into a new
      column. Or set create_new_column = False to overwrite the existing column.
    
    : param: new_column_suffix = "_slicedString"
      This value has effect only if create_new_column = True.
      The new column name will be set as column + new_columns_suffix. Then, if the original
      column was "column1" and the suffix is "_slicedString", the new column will be named as
      "column1_slicedString".
      Alternatively, input inside quotes a string with the desired suffix. Recommendation:
      start the suffix with "_" to separate it from the original name.
    
    : param: first_character_index = None - integer representing the index of the first character to be
      included in the new strings. If None, slicing will start from first character.
      Indexing of strings always start from 0. The last index can be represented as -1, the index of
      the character before as -2, etc (inverse indexing starts from -1).
      example: consider the string "idsw", which contains 4 characters. We can represent the indices as:
      'i': index 0; 'd': 1, 's': 2, 'w': 3. Alternatively: 'w': -1, 's': -2, 'd': -3, 'i': -4.
    
    : param: last_character_index = None - integer representing the index of the last character to be
      included in the new strings. If None, slicing will go until the last character.
      Attention: this is effectively the last character to be added, and not the next index after last
      character.
    
      in the 'idsw' example, if we want a string as 'ds', we want the first_character_index = 1 and
      last_character_index = 2.
    
    : param: step = 1 - integer representing the slicing step. If step = 1, all characters will be added.
      If step = 2, then the slicing will pick one element of index i and the element with index (i+2)
      (1 index will be 'jumped'), and so on.
      If step is negative, then the order of the new strings will be inverted.
      
      Example: step = -1, and the start and finish indices are None: the output will be the inverted
      string, 'wsdi'.
      first_character_index = 1, last_character_index = 2, step = 1: output = 'ds';
      first_character_index = None, last_character_index = None, step = 2: output = 'is';
      first_character_index = None, last_character_index = None, step = 3: output = 'iw';
      first_character_index = -1, last_character_index = -2, step = -1: output = 'ws';
      first_character_index = -1, last_character_index = None, step = -2: output = 'wd';
      first_character_index = -1, last_character_index = None, step = 1: output = 'w'
      In this last example, the function tries to access the next element after the character of index
      -1. Since -1 is the last character, there are no other characters to be added.
      first_character_index = -2, last_character_index = -1, step = 1: output = 'sw'.
    """
    
    # Set a local copy of dataframe to manipulate
    DATASET = df.copy(deep = True)
    # Guarantee that the column to analyze was read as string:
    DATASET[column_to_analyze] = (DATASET[column_to_analyze]).astype(str)
    new_series = DATASET[column_to_analyze].copy()
    
    # Pandas slice:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.slice.html
    
    
    if (step is None):
        # set as 1
        step = 1
    
    if (last_character_index is not None):
        if (last_character_index == -1):
            # In this case, we cannot sum 1, because it would result in index 0 (1st character).
            # So, we will proceed without last index definition, to stop only at the end.
            last_character_index = None
    
    # Now, make the checking again:
            
    if ((first_character_index is None) & (last_character_index is None)):
        
        new_series = new_series.str.slice(step = step)
        
    elif (first_character_index is None):
        # Only this is None:
        new_series = new_series.str.slice(stop = (last_character_index + 1), step = step)
    
    elif (last_character_index is None):
        
        new_series = new_series.str.slice(start = first_character_index, step = step)
    
    else:
        
        new_series = new_series.str.slice(start = first_character_index, stop = (last_character_index + 1), step = step)
    
    # Slicing from index i to index j includes index i, but does not include 
    # index j (ends in j-1). So, we add 1 to the last index to include it.
    # automatically included.

    if (create_new_column):
            
        if (new_column_suffix is None):
            new_column_suffix = "_slicedString"

        new_column_name = column_to_analyze + new_column_suffix
        DATASET[new_column_name] = new_series
            
    else:

        DATASET[column_to_analyze] = new_series

    # Now, we are in the main code.
    print(f"Finished slicing the strings from character {first_character_index} to character {last_character_index}.")
    print("Check the 10 first elements from the series:\n")

    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(new_series.head(10))

    except: # regular mode
        print(new_series.head(10))

    return DATASET


def left_characters (df, column_to_analyze, number_of_characters_to_retrieve = 1, new_variable_type = None, create_new_column = True, new_column_suffix = "_leftChars"):
    """
    left_characters (df, column_to_analyze, number_of_characters_to_retrieve = 1, new_variable_type = None, create_new_column = True, new_column_suffix = "_leftChars"):
    
    : param: column_to_analyze: string (inside quotes), 
      containing the name of the column that will be analyzed. 
      e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    : param: create_new_column = True
      Alternatively, set create_new_columns = True to store the transformed data into a new
      column. Or set create_new_column = False to overwrite the existing column.
    
    : param: new_column_suffix = "_leftChars"
      This value has effect only if create_new_column = True.
      The new column name will be set as column + new_columns_suffix. Then, if the original
      column was "column1" and the suffix is "_leftChars", the new column will be named as
      "column1_leftChars".
      Alternatively, input inside quotes a string with the desired suffix. Recommendation:
      start the suffix with "_" to separate it from the original name.
    
    : param: number_of_characters_to_retrieve = 1 - integer representing the total of characters that will
      be retrieved. Here, we will retrieve the leftest characters. If number_of_characters_to_retrieve = 1,
      only the leftest (last) character will be retrieved.
      Consider the string 'idsw'.
      number_of_characters_to_retrieve = 1 - output: 'w';
      number_of_characters_to_retrieve = 2 - output: 'sw'.
    
    : param: new_variable_type = None. String (in quotes) that represents a given data type for the column
      after transformation. Set:
      - new_variable_type = 'int' to convert the extracted column to integer;
      - new_variable_type = 'float' to convert the column to float (decimal number);
      - new_variable_type = 'datetime' to convert it to date or timestamp;
      - new_variable_type = 'category' to convert it to Pandas categorical variable.
    
      So, if the last part of the strings is a number, you can use this argument to directly extract
      this part as numeric variable.
    """
    
    # Set a local copy of dataframe to manipulate
    DATASET = df.copy(deep = True)
    # Guarantee that the column to analyze was read as string:
    DATASET[column_to_analyze] = (DATASET[column_to_analyze]).astype(str)
    new_series = DATASET[column_to_analyze].copy()
    
    # Pandas slice:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.slice.html
    
    if (number_of_characters_to_retrieve is None):
        # set as 1
        number_of_characters_to_retrieve = 1
    
    # last_character_index = -1 would be the index of the last character.
    # If we want the last N = 2 characters, we should go from index -2 to -1, -2 = -1 - (N-1);
    # If we want the last N = 3 characters, we should go from index -3 to -1, -2 = -1 - (N-1);
    # If we want only the last (N = 1) character, we should go from -1 to -1, -1 = -1 - (N-1).
    
    # N = number_of_characters_to_retrieve
    first_character_index = -1 - (number_of_characters_to_retrieve - 1)
    
    # Perform the slicing without setting the limit, to slice until the end of the string:
    new_series = new_series.str.slice(start = first_character_index, step = 1)
    
    # Check if a the series type should be modified:
    if (new_variable_type is not None):
        
        if (new_variable_type == 'int'):

            new_type = np.int64

        elif (new_variable_type == 'float'):
            
            new_type = np.float64
        
        elif (new_variable_type == 'datetime'):
            
            new_type = 'datetime64[ns]'
        
        elif (new_variable_type == 'category'):
            
            new_type = new_variable_type
        
        # Try converting the type:
        try:
            new_series = new_series.astype(new_type)
            print(f"Successfully converted the series to the type {new_variable_type}.\n")
        
        except:
            pass
    
    
    if (create_new_column):
            
        if (new_column_suffix is None):
            new_column_suffix = "_leftChars"

        new_column_name = column_to_analyze + new_column_suffix
        DATASET[new_column_name] = new_series
            
    else:

        DATASET[column_to_analyze] = new_series

    # Now, we are in the main code.
    print(f"Finished extracting the {number_of_characters_to_retrieve} leftest characters.")
    print("Check the 10 first elements from the series:\n")

    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(new_series.head(10))

    except: # regular mode
        print(new_series.head(10))

    return DATASET


def right_characters (df, column_to_analyze, number_of_characters_to_retrieve = 1, new_variable_type = None, create_new_column = True, new_column_suffix = "_rightChars"):
    """
    right_characters (df, column_to_analyze, number_of_characters_to_retrieve = 1, new_variable_type = None, create_new_column = True, new_column_suffix = "_rightChars"):
    
    : param: column_to_analyze: string (inside quotes), 
      containing the name of the column that will be analyzed. 
      e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    : param: create_new_column = True
      Alternatively, set create_new_columns = True to store the transformed data into a new
      column. Or set create_new_column = False to overwrite the existing column.
    
    : param: new_column_suffix = "_rightChars"
      This value has effect only if create_new_column = True.
      The new column name will be set as column + new_columns_suffix. Then, if the original
      column was "column1" and the suffix is "_rightChars", the new column will be named as
      "column1_rightChars".
      Alternatively, input inside quotes a string with the desired suffix. Recommendation:
      start the suffix with "_" to separate it from the original name.
    
    : param: number_of_characters_to_retrieve = 1 - integer representing the total of characters that will
      be retrieved. Here, we will retrieve the rightest characters. If number_of_characters_to_retrieve = 1,
      only the rightest (first) character will be retrieved.
      Consider the string 'idsw'.
      number_of_characters_to_retrieve = 1 - output: 'i';
      number_of_characters_to_retrieve = 2 - output: 'id'.
    
    : param: new_variable_type = None. String (in quotes) that represents a given data type for the column
      after transformation. Set:
      - new_variable_type = 'int' to convert the extracted column to integer;
      - new_variable_type = 'float' to convert the column to float (decimal number);
      - new_variable_type = 'datetime' to convert it to date or timestamp;
      - new_variable_type = 'category' to convert it to Pandas categorical variable.
    
      So, if the first part of the strings is a number, you can use this argument to directly extract
      this part as numeric variable.
    """
    
    # Set a local copy of dataframe to manipulate
    DATASET = df.copy(deep = True)
    # Guarantee that the column to analyze was read as string:
    DATASET[column_to_analyze] = (DATASET[column_to_analyze]).astype(str)
    new_series = DATASET[column_to_analyze].copy()
    
    # Pandas slice:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.slice.html
    
    if (number_of_characters_to_retrieve is None):
        # set as 1
        number_of_characters_to_retrieve = 1
    
    # first_character_index = 0 would be the index of the first character.
    # If we want the last N = 2 characters, we should go from index 0 to 1, 1 = (N-1);
    # If we want the last N = 3 characters, we should go from index 0 to 2, 2 = (N-1);
    # If we want only the last (N = 1) character, we should go from 0 to 0, 0 = (N-1).
    
    # N = number_of_characters_to_retrieve
    last_character_index = number_of_characters_to_retrieve - 1
    
    # Perform the slicing without setting the limit, to slice from the 1st character:
    new_series = new_series.str.slice(stop = (last_character_index + 1), step = 1)
    
    # Check if a the series type should be modified:
    if (new_variable_type is not None):
        
        if (new_variable_type == 'int'):

            new_type = np.int64

        elif (new_variable_type == 'float'):
            
            new_type = np.float64
        
        elif (new_variable_type == 'datetime'):
            
            new_type = 'datetime64[ns]'
        
        elif (new_variable_type == 'category'):
            
            new_type = new_variable_type
        
        # Try converting the type:
        try:
            new_series = new_series.astype(new_type)
            print(f"Successfully converted the series to the type {new_variable_type}.\n")
        
        except:
            pass
    
    
    if (create_new_column):
            
        if (new_column_suffix is None):
            new_column_suffix = "_rightChars"

        new_column_name = column_to_analyze + new_column_suffix
        DATASET[new_column_name] = new_series
            
    else:

        DATASET[column_to_analyze] = new_series

    # Now, we are in the main code.
    print(f"Finished extracting the {number_of_characters_to_retrieve} rightest characters.")
    print("Check the 10 first elements from the series:\n")

    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(new_series.head(10))

    except: # regular mode
        print(new_series.head(10))

    return DATASET


def join_strings_from_column (df, column_to_analyze, separator = " "):
    """
    join_strings_from_column (df, column_to_analyze, separator = " ")

    : param: column_to_analyze: string (inside quotes), 
      containing the name of the column that will be analyzed. 
      e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    : param: separator = " " - string containing the separator. Suppose the column contains the
      strings: 'a', 'b', 'c', 'd'. If the separator is the empty string '', the output will be:
      'abcd' (no separation). If separator = " " (simple whitespace), the output will be 'a b c d'
    """
    
    if (separator is None):
        # make it a whitespace:
        separator = " "
    
    # Set a local copy of dataframe to manipulate
    DATASET = df.copy(deep = True)
    # Guarantee that the column to analyze was read as string:
    DATASET[column_to_analyze] = (DATASET[column_to_analyze]).astype(str)
    new_series = DATASET[column_to_analyze].copy()
    
    concat_string = separator.join(new_series)
    # sep.join(list_of_strings) method: join all the strings, separating them by sep.

    # Now, we are in the main code.
    print(f"Finished joining strings from column {column_to_analyze}.")
    print("Check the 10 first characters from the new string:\n")

    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(concat_string[:10])

    except: # regular mode
        print(concat_string[:10])

    return concat_string


def join_string_columns (df, list_of_columns_to_join, separator = " ", new_column_suffix = "_stringConcat"):
    """
    join_string_columns (df, list_of_columns_to_join, separator = " ", new_column_suffix = "_stringConcat")

    : param: list_of_columns_to_join: list of strings (inside quotes), 
      containing the name of the columns with strings to be joined.
      Attention: the strings will be joined row by row, i.e. only strings in the same rows will
      be concatenated. To join strings from the same column, use function join_strings_from_column
      e.g. list_of_columns_to_join = ["column1", "column2"] will join strings from "column1" with
      the correspondent strings from "column2".
      Notice that you can concatenate any kind of columns: numeric, dates, texts ,..., but the output
      will be a string column.
    
    : param: separator = " " - string containing the separator. Suppose the columns contain the
      strings: 'a', 'b', 'c', 'd' on a given row. If the separator is the empty string '', 
      the output will be: 'abcd' (no separation). If separator = " " (simple whitespace), 
      the output will be 'a b c d'
    
    : param: new_column_suffix = "_stringConcat"
      This value has effect only if create_new_column = True.
      The new column name will be set as column + new_columns_suffix. Then, if the original
      column was "column1" and the suffix is "_stringConcat", the new column will be named as
      "column1_stringConcat".
      Alternatively, input inside quotes a string with the desired suffix. Recommendation:
      start the suffix with "_" to separate it from the original name.
    """

    if (separator is None):
        # make it a whitespace:
        separator = " "
        
    # Set a local copy of dataframe to manipulate
    DATASET = df.copy(deep = True)
    
    # Start a string pandas series from DATASET, but without connections with it. It will contain
    # only empty strings.
    second_copy_df = DATASET.copy(deep = True)
    second_copy_df['concat_string'] = ''
    # Also, create a separator series from it, and make it constant and equals to the separator:
    second_copy_df['separator'] = separator
    
    new_series = second_copy_df['concat_string']
    sep_series = second_copy_df['separator']
    
    col = list_of_columns_to_join[0]
    new_series = new_series + (DATASET[col]).astype(str)
    
    # Now, loop through the columns in the list:
    for i in range(1, len(list_of_columns_to_join)):
        # We already picked the 1st column (index 0). Now, we pick the second one and go
        # until len(list_of_columns_to_join) - 1, index of the last column of the list.
        
        col = list_of_columns_to_join[i]
        # concatenate the column with new_series, adding the separator to the left.
        # As we add the separator before, there will be no extra separator after the last string.
        # Convert the columns to strings for concatenation.
        new_series = new_series + sep_series + (DATASET[col]).astype(str)
        # The sep.join(list_of_strings) method can only be applied to array-like objects. It cannot
        # be used for this operation.
            
    if (new_column_suffix is None):
        new_column_suffix = "_stringConcat"

    # Add the suffix to the name of the first column
    new_column_name = list_of_columns_to_join[0] + new_column_suffix
    DATASET[new_column_name] = new_series
    
    # Now, we are in the main code.
    print(f"Finished concatenating strings from columns {list_of_columns_to_join}.")
    print("Check the 10 first elements from the series:\n")

    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(new_series.head(10))

    except: # regular mode
        print(new_series.head(10))

    return DATASET


def split_strings (df, column_to_analyze, separator = " ", create_new_column = True, new_column_suffix = "_stringSplitted"):
    """
    split_strings (df, column_to_analyze, separator = " ", create_new_column = True, new_column_suffix = "_stringSplitted")

    : param: column_to_analyze: string (inside quotes), 
      containing the name of the column that will be analyzed. 
      e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.

    : param: separator = " " - string containing the separator. Suppose the column contains the
      string: 'a b c d' on a given row. If the separator is whitespace ' ', 
      the output will be a list: ['a', 'b', 'c', 'd']: the function splits the string into a list
      of strings (one list per row) every time it finds the separator.
    
    : param: create_new_column = True
      Alternatively, set create_new_columns = True to store the transformed data into a new
      column. Or set create_new_column = False to overwrite the existing column.
    
    : param: new_column_suffix = "_stringSplitted"
      This value has effect only if create_new_column = True.
      The new column name will be set as column + new_columns_suffix. Then, if the original
      column was "column1" and the suffix is "_stringSplitted", the new column will be named as
      "column1_stringSplitted".
      Alternatively, input inside quotes a string with the desired suffix. Recommendation:
      start the suffix with "_" to separate it from the original name.
    """

    if (separator is None):
        # make it a whitespace:
        separator = " "
        
    # Set a local copy of dataframe to manipulate
    DATASET = df.copy(deep = True)
    DATASET[column_to_analyze] = (DATASET[column_to_analyze]).astype(str)
    new_series = DATASET[column_to_analyze].copy()
    
    # Split the strings from new_series, getting a list of strings per column:
    new_series = new_series.str.split(separator)
    
    if (create_new_column):
            
        if (new_column_suffix is None):
            new_column_suffix = "_stringSplitted"

        new_column_name = column_to_analyze + new_column_suffix
        DATASET[new_column_name] = new_series
            
    else:

        DATASET[column_to_analyze] = new_series

    # Now, we are in the main code.
    print(f"Finished splitting strings from column {column_to_analyze}.")
    print("Check the 10 first elements (10 lists) from the series:\n")

    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(new_series.head(10))

    except: # regular mode
        print(new_series.head(10))

    return DATASET


def switch_strings (df, column_to_analyze, list_of_dictionaries_with_original_strings_and_replacements = [{'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}], create_new_column = True, new_column_suffix = "_stringReplaced"):
    """
    switch_strings (df, column_to_analyze, list_of_dictionaries_with_original_strings_and_replacements = [{'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}], create_new_column = True, new_column_suffix = "_stringReplaced"):
    
    : param: column_to_analyze: string (inside quotes), 
      containing the name of the column that will be analyzed. 
      e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    : param: list_of_dictionaries_with_original_strings_and_replacements = 
      [{'original_string': None, 'new_string': None}]
      This is a list of dictionaries, where each dictionary contains two key-value pairs:
      the first one contains the original string; and the second one contains the new string
      that will substitute the original one. The function will loop through all dictionaries in
      this list, access the values of the keys 'original_string', and search these values on the strings
      in column_to_analyze. When the value is found, it will be replaced (switched) by the correspondent
      value in key 'new_string'.
    
      The object list_of_dictionaries_with_original_strings_and_replacements must be declared as a list, 
      in brackets, even if there is a single dictionary.
      Use always the same keys: 'original_string' for the original strings to search on the column 
      column_to_analyze; and 'new_string', for the strings that will replace the original ones.
      Notice that this function will not search substrings: it will substitute a value only when
      there is perfect correspondence between the string in 'column_to_analyze' and 'original_string'.
      So, the cases (upper or lower) must be the same.
    
      If you want, you can remove elements (dictionaries) from the list to declare fewer elements;
      and you can also add more elements (dictionaries) to the lists, if you need to replace more
      values.
      Simply put a comma after the last element from the list and declare a new dictionary, keeping the
      same keys: {'original_string': original_str, 'new_string': new_str}, 
      where original_str and new_str represent the strings for searching and replacement 
      (If one of the keys contains None, the new dictionary will be ignored).
    
      Example:
      Suppose the column_to_analyze contains the values 'sunday', 'monday', 'tuesday', 'wednesday',
      'thursday', 'friday', 'saturday', but you want to obtain data labelled as 'weekend' or 'weekday'.
      Set: list_of_dictionaries_with_original_strings_and_replacements = 
      [{'original_string': 'sunday', 'new_string': 'weekend'},
      {'original_string': 'saturday', 'new_string': 'weekend'},
      {'original_string': 'monday', 'new_string': 'weekday'},
      {'original_string': 'tuesday', 'new_string': 'weekday'},
      {'original_string': 'wednesday', 'new_string': 'weekday'},
      {'original_string': 'thursday', 'new_string': 'weekday'},
      {'original_string': 'friday', 'new_string': 'weekday'}]
    
    : param: create_new_column = True
      Alternatively, set create_new_columns = True to store the transformed data into a new
      column. Or set create_new_column = False to overwrite the existing column.
    
    : param: new_column_suffix = "_stringReplaced"
      This value has effect only if create_new_column = True.
      The new column name will be set as column + new_columns_suffix. Then, if the original
      column was "column1" and the suffix is "_stringReplaced", the new column will be named as
      "column1_stringReplaced".
      Alternatively, input inside quotes a string with the desired suffix. Recommendation:
      start the suffix with "_" to separate it from the original name.
    """
    
    # Set a local copy of dataframe to manipulate
    DATASET = df.copy(deep = True)
    # Guarantee that the column to analyze was read as string:
    DATASET[column_to_analyze] = (DATASET[column_to_analyze]).astype(str)
    new_series = DATASET[column_to_analyze].copy()
    
    print("ATTENTION: Operations of string strip (removal) or replacement are all case-sensitive. There must be correct correspondence between cases and spaces for the strings being removed or replaced.\n")
    
    # Create the mapping dictionary for the str.replace method:
    mapping_dict = {}
    # The key of the mapping dict must be an string, whereas the value must be the new string
    # that will replace it.
        
    # Loop through each element on the list list_of_dictionaries_with_original_strings_and_replacements:
    
    for i in range (0, len(list_of_dictionaries_with_original_strings_and_replacements)):
        # from i = 0 to i = len(list_of_dictionaries_with_original_strings_and_replacements) - 1, index of the
        # last element from the list
            
        # pick the i-th dictionary from the list:
        dictionary = list_of_dictionaries_with_original_strings_and_replacements[i]
            
        # access 'original_string' and 'new_string' keys from the dictionary:
        original_string = dictionary['original_string']
        new_string = dictionary['new_string']
        
        # check if they are not None:
        if ((original_string is not None) & (new_string is not None)):
            
            #Guarantee that both are read as strings:
            original_string = str(original_string)
            new_string = str(new_string)
            
            # add them to the mapping dictionary, using the original_string as key and
            # new_string as the correspondent value:
            mapping_dict[original_string] = new_string
    
    # Now, the input list was converted into a dictionary with the correct format for the method.
    # Check if there is at least one key in the dictionary:
    if (len(mapping_dict) > 0):
        # len of a dictionary returns the amount of key:value pairs stored. If nothing is stored,
        # len = 0. dictionary.keys() method (no arguments in parentheses) returns an array containing
        # the keys; whereas dictionary.values() method returns the arrays of the values.
        
        new_series = new_series.replace(mapping_dict)
        # For replacing the whole strings using a mapping dictionary, do not call the str
        # attribute
    
        if (create_new_column):
            
            if (new_column_suffix is None):
                new_column_suffix = "_substringReplaced"

            new_column_name = column_to_analyze + new_column_suffix
            DATASET[new_column_name] = new_series
            
        else:

            DATASET[column_to_analyze] = new_series

        # Now, we are in the main code.
        print(f"Finished replacing the substrings accordingly to the mapping: {mapping_dict}.")
        print("Check the 10 first elements from the series:\n")

        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(new_series.head(10))

        except: # regular mode
            print(new_series.head(10))

        return DATASET
    
    else:
        print("Input at least one dictionary containing a pair of original string, in the key \'original_string\', and the correspondent new string as key \'new_string\'.")
        print("The dictionaries must be elements from the list list_of_dictionaries_with_original_strings_and_replacements.\n")
        
        return "error"


def string_replacement_ml (df, column_to_analyze, mode = 'find_and_replace', threshold_for_percent_of_similarity = 80.0, list_of_dictionaries_with_standard_strings_for_replacement = [{'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}], create_new_column = True, new_column_suffix = "_stringReplaced"):
    """
    string_replacement_ml (df, column_to_analyze, mode = 'find_and_replace', threshold_for_percent_of_similarity = 80.0, list_of_dictionaries_with_standard_strings_for_replacement = [{'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}], create_new_column = True, new_column_suffix = "_stringReplaced"):
    
    : param: column_to_analyze: string (inside quotes), 
      containing the name of the column that will be analyzed. 
      e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    : param: mode = 'find_and_replace' will find similar strings; and switch them by one of the
      standard strings if the similarity between them is higher than or equals to the threshold.
      Alternatively: mode = 'find' will only find the similar strings by calculating the similarity.
    
    : param: threshold_for_percent_of_similarity = 80.0 - 0.0% means no similarity and 100% means equal strings.
      The threshold_for_percent_of_similarity is the minimum similarity calculated from the
      Levenshtein (minimum edit) distance algorithm. This distance represents the minimum number of
      insertion, substitution or deletion of characters operations that are needed for making two
      strings equal.
    
    : param: list_of_dictionaries_with_standard_strings_for_replacement =
      [{'standard_string': None}]
      This is a list of dictionaries, where each dictionary contains a single key-value pair:
      the key must be always 'standard_string', and the value will be one of the standard strings 
      for replacement: if a given string on the column_to_analyze presents a similarity with one 
      of the standard string equals or higher than the threshold_for_percent_of_similarity, it will be
      substituted by this standard string.
      For instance, suppose you have a word written in too many ways, making it difficult to use
      the function switch_strings: "EU" , "eur" , "Europ" , "Europa" , "Erope" , "Evropa" ...
      You can use this function to search strings similar to "Europe" and replace them.
    
      The function will loop through all dictionaries in
      this list, access the values of the keys 'standard_string', and search these values on the strings
      in column_to_analyze. When the value is found, it will be replaced (switched) if the similarity
      is sufficiently high.
    
      The object list_of_dictionaries_with_standard_strings_for_replacement must be declared as a list, 
      in brackets, even if there is a single dictionary.
      Use always the same keys: 'standard_string'.
      Notice that this function performs fuzzy matching, so it MAY SEARCH substrings and strings
      written with different cases (upper or lower) when this portions or modifications make the
      strings sufficiently similar to each other.
    
      If you want, you can remove elements (dictionaries) from the list to declare fewer elements;
      and you can also add more elements (dictionaries) to the lists, if you need to replace more
      values.
      Simply put a comma after the last element from the list and declare a new dictionary, keeping the
      same key: {'standard_string': other_std_str}, 
      where other_std_str represents the string for searching and replacement 
      (If the key contains None, the new dictionary will be ignored).
    
      Example:
      Suppose the column_to_analyze contains the values 'California', 'Cali', 'Calefornia', 
      'Calefornie', 'Californie', 'Calfornia', 'Calefernia', 'New York', 'New York City', 
      but you want to obtain data labelled as the state 'California' or 'New York'.
      Set: list_of_dictionaries_with_standard_strings_for_replacement = 
      [{'standard_string': 'California'},
      {'standard_string': 'New York'}]
    
      ATTENTION: It is advisable for previously searching the similarity to find the best similarity
      threshold; set it as high as possible, avoiding incorrect substitutions in a gray area; and then
      perform the replacement. It will avoid the repetition of original incorrect strings in the
      output dataset, as well as wrong replacement (replacement by one of the standard strings which
      is not the correct one).
    
    : param: create_new_column = True
      Alternatively, set create_new_columns = True to store the transformed data into a new
      column. Or set create_new_column = False to overwrite the existing column.
    
    : param: new_column_suffix = "_stringReplaced"
      This value has effect only if create_new_column = True.
      The new column name will be set as column + new_columns_suffix. Then, if the original
      column was "column1" and the suffix is "_stringReplaced", the new column will be named as
      "column1_stringReplaced".
      Alternatively, input inside quotes a string with the desired suffix. Recommendation:
      start the suffix with "_" to separate it from the original name.
    """

    from fuzzywuzzy import process
    
    print("Performing fuzzy replacement based on the Levenshtein (minimum edit) distance algorithm.")
    print("This distance represents the minimum number of insertion, substitution or deletion of characters operations that are needed for making two strings equal.\n")
    
    print("This means that substrings or different cases (upper or higher) may be searched and replaced, as long as the similarity threshold is reached.\n")
    
    print("ATTENTION!\n")
    print("It is advisable for previously searching the similarity to find the best similarity threshold.\n")
    print("Set the threshold as high as possible, and only then perform the replacement.\n")
    print("It will avoid the repetition of original incorrect strings in the output dataset, as well as wrong replacement (replacement by one of the standard strings which is not the correct one.\n")
    
    # Set a local copy of dataframe to manipulate
    DATASET = df.copy(deep = True)
    # Guarantee that the column to analyze was read as string:
    DATASET[column_to_analyze] = (DATASET[column_to_analyze]).astype(str)
    new_series = DATASET[column_to_analyze].copy()

    # Get the unique values present in column_to_analyze:
    unique_types = new_series.unique()
    
    # Create the summary_list:
    summary_list = []
        
    # Loop through each element on the list list_of_dictionaries_with_original_strings_and_replacements:
    
    for i in range (0, len(list_of_dictionaries_with_standard_strings_for_replacement)):
        # from i = 0 to i = len(list_of_dictionaries_with_standard_strings_for_replacement) - 1, index of the
        # last element from the list
            
        # pick the i-th dictionary from the list:
        dictionary = list_of_dictionaries_with_standard_strings_for_replacement[i]
            
        # access 'standard_string' key from the dictionary:
        standard_string = dictionary['standard_string']
        
        # check if it is not None:
        if (standard_string is not None):
            
            # Guarantee that it was read as a string:
            standard_string = str(standard_string)
            
            # Calculate the similarity between each one of the unique_types and standard_string:
            similarity_list = process.extract(standard_string, unique_types, limit = len(unique_types))
            
            # Add the similarity list to the dictionary:
            dictionary['similarity_list'] = similarity_list
            # This is a list of tuples with the format (tested_string, percent_of_similarity_with_standard_string)
            # e.g. ('asiane', 92) for checking similarity with string 'asian'
            
            if (mode == 'find_and_replace'):
                
                # If an invalid value was set for threshold_for_percent_of_similarity, correct it to 80% standard:
                
                if(threshold_for_percent_of_similarity is None):
                    threshold_for_percent_of_similarity = 80.0
                
                if((threshold_for_percent_of_similarity == np.nan) | (threshold_for_percent_of_similarity < 0)):
                    threshold_for_percent_of_similarity = 80.0
                
                list_of_replacements = []
                # Let's replace the matches in the series by the standard_string:
                # Iterate through the list of matches
                for match in similarity_list:
                    # Check whether the similarity score is greater than or equal to threshold_for_percent_of_similarity.
                    # The similarity score is the second element (index 1) from the tuples:
                    if (match[1] >= threshold_for_percent_of_similarity):
                        # If it is, select all rows where the column_to_analyze is spelled as
                        # match[0] (1st Tuple element), and set it to standard_string:
                        boolean_filter = (new_series == match[0])
                        new_series.loc[boolean_filter] = standard_string
                        print(f"Found {match[1]}% of similarity between {match[0]} and {standard_string}.")
                        print(f"Then, {match[0]} was replaced by {standard_string}.\n")
                        
                        # Add match to the list of replacements:
                        list_of_replacements.append(match)
                
                # Add the list_of_replacements to the dictionary, if its length is higher than zero:
                if (len(list_of_replacements) > 0):
                    dictionary['list_of_replacements_by_std_str'] = list_of_replacements
            
            # Add the dictionary to the summary_list:
            summary_list.append(dictionary)
    
    # Now, let's replace the original column or create a new one if mode was set as replace:
    if (mode == 'find_and_replace'):
    
        if (create_new_column):
            
            if (new_column_suffix is None):
                new_column_suffix = "_substringReplaced"

            new_column_name = column_to_analyze + new_column_suffix
            DATASET[new_column_name] = new_series
            
        else:

            DATASET[column_to_analyze] = new_series

        # Now, we are in the main code.
        print(f"Finished replacing the strings by the provided standards. Returning the new dataset and a summary list.\n")
        print("In summary_list, you can check the calculated similarities in keys \'similarity_list\' from the dictionaries.\n")
        print("The similarity list is a list of tuples, where the first element is the string compared against the value on key \'standard_string\'; and the second element is the similarity score, the percent of similarity between the tested and the standard string.\n")
        print("Check the 10 first elements from the new series, with strings replaced:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(new_series.head(10))

        except: # regular mode
            print(new_series.head(10))
    
    else:
        
        print("Finished mapping similarities. Returning the original dataset and a summary list.\n")
        print("Check the similarities below, in keys \'similarity_list\' from the dictionaries.\n")
        print("The similarity list is a list of tuples, where the first element is the string compared against the value on key \'standard_string\'; and the second element is the similarity score, the percent of similarity between the tested and the standard string.\n")
        
        try:
            display(summary_list)
        except:
            print(summary_list)
    
    return DATASET, summary_list


def regex_search (df, column_to_analyze, regex_to_search = r"", show_regex_helper = False, create_new_column = True, new_column_suffix = "_regex"):
    """
    regex_search (df, column_to_analyze, regex_to_search = r"", show_regex_helper = False, create_new_column = True, new_column_suffix = "_regex"):
    
    : param: column_to_analyze: string (inside quotes), 
      containing the name of the column that will be analyzed. 
      e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    : param: regex_to_search = r"" - string containing the regular expression (regex) that will be searched
      within each string from the column. Declare it with the r before quotes, indicating that the
      'raw' string should be read. That is because the regex contain special characters, such as \,
      which should not be read as scape characters.
      example of regex: r'st\d\s\w{3,10}'
      Use the regex helper to check: basic theory and most common metacharacters; regex quantifiers;
      regex anchoring and finding; regex greedy and non-greedy search; regex grouping and capturing;
      regex alternating and non-capturing groups; regex backreferences; and regex lookaround.
    
      ATTENTION: This function returns ONLY the capturing groups from the regex, i.e., portions of the
      regex explicitly marked with parentheses (check the regex helper for more details, including how
      to convert parentheses into non-capturing groups). If no groups are marked as capturing, the
      function will raise an error.

    : param: show_regex_helper: set show_regex_helper = True to show a helper guide to the construction of
      the regular expression. After finishing the helper, the original dataset itself will be returned
      and the function will not proceed. Use it in case of not knowing or not certain on how to input
      the regex.
    
    : param: create_new_column = True
      Alternatively, set create_new_columns = True to store the transformed data into a new
      column. Or set create_new_column = False to overwrite the existing column.
    
    : param: new_column_suffix = "_regex"
      This value has effect only if create_new_column = True.
      The new column name will be set as column + new_columns_suffix. Then, if the original
      column was "column1" and the suffix is "_regex", the new column will be named as
      "column1_regex".
      Alternatively, input inside quotes a string with the desired suffix. Recommendation:
      start the suffix with "_" to separate it from the original name.
    """

    if (show_regex_helper): # run if True
        
        # Create an instance (object) from class RegexHelp:
        helper = RegexHelp()
        # Run helper object:
        helper = helper.show_screen()
        print("Interrupting the function and returning the dataframe itself.")
        print("Use the regex helper instructions to obtain the regex.")
        print("Do not forget to declare it as r'regex', with the r before quotes.")
        print("It indicates a raw expression. It is important for not reading the regex metacharacters as regular string scape characters.")
        print("Also, notice that this function returns only the capturing groups (marked with parentheses).")
        print("If no groups are marked as capturing groups (with parentheses) within the regex, the function will raise an error.\n")
        
        return df
    
    else:
        
        # Set a local copy of dataframe to manipulate
        DATASET = df.copy(deep = True)
        DATASET[column_to_analyze] = (DATASET[column_to_analyze]).astype(str)
        new_series = DATASET[column_to_analyze].copy()
        
        # Search for the regex within new_series:
        new_series = new_series.str.extract(regex_to_search, expand = True)
        
        # https://pandas.pydata.org/docs/reference/api/pandas.Series.str.extract.html
        # setting expand = True returns a dataframe with one column per capture group, if the
        # regex contains more than 1 capture group.
        
        # The shape attribute is a tuple (N,) for a Pandas Series, and (N, M) for a dataframe,
        # where N is the number of rows, and M is the number of columns.
        # Let's try to access the number of columns. It will only be possible if the object is a
        # dataframe (index 1 from shape tuple):
        try:
            
            total_new_cols = new_series.shape[1]
            
            if (new_column_suffix is None):
                new_column_suffix = "_regex"
            
            new_column_suffix = str(column_to_analyze) + new_column_suffix + "_group_"
            
            # In the regex, the group 0 is the expression itself, whereas the first group is group 1.
            # range (0, total_new_cols) goes from 0 to total_new_cols-1;
            # range (1, total_new_cols + 1) goes from group 1 to group total_new_cols
            # (both cases result in total_new_cols elements):
            
            # Create a list of columns:
            new_columns_list = [(new_column_suffix + str(i)) for i in range (1, (total_new_cols + 1))]
            
            # Make this list the new columns' names:
            new_series.columns = new_columns_list
            
            # Concatenate this dataframe to the original one (add columns to the right of DATASET):
            DATASET = pd.concat([DATASET, new_series], axis = 1, join = "inner")
        
        
        except IndexError:
            
            # There is no second dimension, because it is a series.
            # The regex finds a single group
            
            if (create_new_column):

                if (new_column_suffix is None):
                    new_column_suffix = "_regex"

                new_column_name = column_to_analyze + new_column_suffix
                DATASET[new_column_name] = new_series

            else:

                DATASET[column_to_analyze] = new_series

        # Now, we are in the main code.
        print(f"Finished searching the regex {regex_to_search} within {column_to_analyze}.")
        print("Check the 10 first elements from the output:\n")

        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(new_series.head(10))

        except: # regular mode
            print(new_series.head(10))

        return DATASET


def regex_replacement (df, column_to_analyze, regex_to_search = r"", string_for_replacement = "", show_regex_helper = False, create_new_column = True, new_column_suffix = "_regex"):
    """
    regex_replacement (df, column_to_analyze, regex_to_search = r"", string_for_replacement = "", show_regex_helper = False, create_new_column = True, new_column_suffix = "_regex"):
    
    : param: column_to_analyze: string (inside quotes), 
      containing the name of the column that will be analyzed. 
      e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    : param: regex_to_search = r"" - string containing the regular expression (regex) that will be searched
      within each string from the column. Declare it with the r before quotes, indicating that the
      'raw' string should be read. That is because the regex contain special characters, such as \,
      which should not be read as scape characters.
      example of regex: r'st\d\s\w{3,10}'
      Use the regex helper to check: basic theory and most common metacharacters; regex quantifiers;
      regex anchoring and finding; regex greedy and non-greedy search; regex grouping and capturing;
      regex alternating and non-capturing groups; regex backreferences; and regex lookaround.
    
    : param: string_for_replacement = "" - regular string that will replace the regex_to_search: 
      whenever regex_to_search is found in the string, it is replaced (substituted) by 
      string_or_regex_for_replacement. 
      Example string_for_replacement = " " (whitespace).
      If string_for_replacement = None, the empty string will be used for replacement.
    
      ATTENTION: This function process a single regex by call.
    
    : param: show_regex_helper: set show_regex_helper = True to show a helper guide to the construction of
      the regular expression. After finishing the helper, the original dataset itself will be returned
      and the function will not proceed. Use it in case of not knowing or not certain on how to input
      the regex.
    
    : param: create_new_column = True
      Alternatively, set create_new_columns = True to store the transformed data into a new
      column. Or set create_new_column = False to overwrite the existing column.
    
    : param: new_column_suffix = "_regex"
      This value has effect only if create_new_column = True.
      The new column name will be set as column + new_columns_suffix. Then, if the original
      column was "column1" and the suffix is "_regex", the new column will be named as
      "column1_regex".
      Alternatively, input inside quotes a string with the desired suffix. Recommendation:
      start the suffix with "_" to separate it from the original name.
    """

    if (show_regex_helper): # run if True
        
        # Create an instance (object) from class RegexHelp:
        helper = RegexHelp()
        # Run helper object:
        helper = helper.show_screen()
        print("Interrupting the function and returning the dataframe itself.")
        print("Use the regex helper instructions to obtain the regex.")
        print("Do not forget to declare it as r'regex', with the r before quotes.")
        print("It indicates a raw expression. It is important for not reading the regex metacharacters as regular string scape characters.\n")
        
        return df
    
    else:
        
        if (string_for_replacement is None):
            # make it the empty string
            string_for_replacement = ""
        
        # Set a local copy of dataframe to manipulate
        DATASET = df.copy(deep = True)
        DATASET[column_to_analyze] = (DATASET[column_to_analyze]).astype(str)
        new_series = DATASET[column_to_analyze].copy()
        
        new_series = new_series.str.replace(regex_to_search, string_for_replacement, regex = True)
        # set regex = True to replace a regular expression
        # https://pandas.pydata.org/docs/reference/api/pandas.Series.str.replace.html
            
        if (create_new_column):

            if (new_column_suffix is None):
                new_column_suffix = "_regex"

            new_column_name = column_to_analyze + new_column_suffix
            DATASET[new_column_name] = new_series

        else:

            DATASET[column_to_analyze] = new_series

        # Now, we are in the main code.
        print(f"Finished searching the regex {regex_to_search} within {column_to_analyze}.")
        print("Check the 10 first elements from the output:\n")

        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(new_series.head(10))

        except: # regular mode
            print(new_series.head(10))

        return DATASET
