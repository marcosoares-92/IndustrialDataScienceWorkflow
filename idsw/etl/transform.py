import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from idsw.datafetch.core import InvalidInputsError


def get_frequency_features (df, timestamp_tag_column, important_frequencies = [{'value': 1, 'unit': 'day'}, {'value':1, 'unit': 'year'}], x_axis_rotation = 70, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, max_number_of_entries_to_plot = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    get_frequency_features (df, timestamp_tag_column, important_frequencies = [{'value': 1, 'unit': 'day'}, {'value':1, 'unit': 'year'}], x_axis_rotation = 70, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, max_number_of_entries_to_plot = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    : param: important_frequencies = [{'value': 1, 'unit': 'day'}, {'value':1, 'unit': 'year'}]
      List of dictionaries with the important frequencies to add to the model. You can remove dictionaries,
      or add extra dictionaries. The dictionaries must have always the same keys, 'value' and 'unit'.
      If the importante frequency is once a day, the value will be 1, and the unit will be 'day' or 'd'.
      The possible units are: 'ns', 'ms', 'second' or 's', 'minute' or 'min', 'day' or 'd', 'month' or 'm',
      'year' or 'y'.
    
    : param: max_number_of_entries_to_plot (integer or None): use this argument to limit the number of entries 
      to plot. If None, all the entries will be plot.
      max_number_of_entries_to_plot = 25 will plot the first 25 entries, max_number_of_entries_to_plot =
      100 will plot the 100 first entries, and so on.
    """

    # the Date Time column is very useful, but not in this string form. 
    # Start by converting it to seconds:
    
    # Start a local copy of the dataframe:
    DATASET = df.copy(deep = True)
    
    # Guarantee that the timestamp column has a datetime object, and not a string
    DATASET[timestamp_tag_column] = DATASET[timestamp_tag_column].astype('datetime64[ns]')
    
    # Return POSIX timestamp as float
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.timestamp.html#pandas.Timestamp.timestamp
    # It is a variation of UNIX timestamp]
    # Pandas Timestamp.timestamp() function return the time expressed as the number of seconds that have passed.
    # https://www.geeksforgeeks.org/python-pandas-timestamp-timestamp/
    # since January 1, 1970. That zero moment is known as the epoch.
    timestamp_s = DATASET[timestamp_tag_column].map(pd.Timestamp.timestamp)
    # the time in seconds is not a useful model input. 
    # It may have daily and yearly periodicity, for instance. 
    # To deal with periodicity, you can get usable signals by using sine and cosine transforms 
    # to clear "Time of day" and "Time of year" signals:
    
    columns_to_plot = []
    
    for freq_dict in important_frequencies:
        
        value = 1/freq_dict['value']
        # period.
        unit = freq_dict['unit']
        
        if ((value is not None) & (unit is not None)):
            
            unit = str(unit).lower()
            
            column_name1 = str(value) + "_" + unit + "_sin"
            column_name2 = str(value) + "_" + unit + "_cos"
            
            column_tuple = (column_name1, column_name2)
            columns_to_plot.append(column_tuple)
            
            if (unit == 'ns'):
                # convert to seconds:
                factor = 10 ** (-9)
            
            elif (unit == 'ms'):
                # convert to seconds:
                factor = 10 ** (-3)
            
            elif ((unit == 's')|(unit == 'second')):
                # convert to seconds:
                factor = 1
            
            elif ((unit == 'min')|(unit == 'minute')):
                # convert to seconds:
                factor = 60
            
            elif ((unit == 'hour')|(unit == 'h')):
                # convert to seconds:
                factor = 60 * 60
            
            elif ((unit == 'month')|(unit == 'm')):
                # convert to seconds, considering a (365.2425)-day year, divided by 12:
                factor = 60 * 60 * 24 * (365.2425)/12
                print(f"Attention: considering an average month of {(365.2425)/12} days.\n")
            
            elif ((unit == 'year')|(unit == 'y')):
                # convert to seconds, considering a (365.2425)-day year:
                factor = 60 * 60 * 24 * (365.2425)
            
            else:
                # unit == 'day', or 'd', the default case
                # convert to seconds:
                factor = 60 * 60 * 24
            
            # Convert to total of seconds and so use the frequency in Hertz to obtain the periodic functions.
            # Since timestamp_s is already in seconds, it is necessary to make it adimensional.
            # X days correspond to X * 60 * 60 * 24 seconds, for instance, where X == value.
            DATASET[column_name1] = np.sin(timestamp_s * (2 * np.pi / (factor * value)))
            DATASET[column_name2] = np.cos(timestamp_s * (2 * np.pi / (factor * value)))
            
            # cos(2pi* t/T), where t is the total time in seconds since Jan 1, 1970
            # T is the period, the inverse of the frequency. If the frequency is 2x a year,
            # so the period = 1/2 year. If frequency is once a year, period = 1/1 = 1 year.

    # There are 8 possible frequencies to plot, i.e, 16 possible sin and cos plots.
    # List of tuples, containing the pairs of colors to be used:
    colors = [('crimson', 'darkblue'), 
                ('fuchsia', 'black'),
                ('red', 'blue'),
                ('darkgreen', 'magenta'),
                ('aqua', 'violet'),
                ('navy', 'purple'),
                ('green', 'firebrick'),
                ('blue', 'plum')]
    
    # Slice the colors list so that it has the same amount of elements as columns_to_plot:
    colors = colors[:(len(columns_to_plot))]
    # Now, we can zip both to create an iterable containing a tuple of plots and a correspondent
    # tuple of colors.
    
    # Start an information dictionary to be returned
    timestamp_dict = {'timestamp': DATASET[timestamp_tag_column]}
    
    # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
    # so that the bars do not completely block other views.
    OPACITY = 0.95
    
    if (plot_title is None):
        # Set graphic title
        plot_title = f"frequency_signals"

    if (horizontal_axis_title is None):
        # Set horizontal axis title
        horizontal_axis_title = "timestamp"

    if (vertical_axis_title is None):
        # Set vertical axis title
        vertical_axis_title = "signal"
    
    #Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
    fig = plt.figure(figsize = (12, 8))
    ax = fig.add_subplot()
    
    # Start a list to append all the plot dictionaries
    plots_list = []
    
    for columns_tuple, colors_tuple in zip(columns_to_plot, colors):
        
        plot_dict = {'label_sin': columns_tuple[0], 'plot_sin': np.array(DATASET[columns_tuple[0]]), 'color_sin': colors_tuple[0],
                    'label_cos': columns_tuple[1], 'plot_cos': np.array(DATASET[columns_tuple[1]]), 'color_cos': colors_tuple[1]}
        
        if (max_number_of_entries_to_plot is None):
            
            x_plot = timestamp_dict['timestamp']
            sin_plot = plot_dict['plot_sin']
            cos_plot = plot_dict['plot_cos']
        
        else:
            x_plot = np.array(timestamp_dict['timestamp'])[:max_number_of_entries_to_plot]
            sin_plot = np.array(plot_dict['plot_sin'])[:max_number_of_entries_to_plot]
            cos_plot = np.array(plot_dict['plot_cos'])[:max_number_of_entries_to_plot]
        
        ax.plot(x_plot, sin_plot, linestyle = "-", marker = '', color = plot_dict['color_sin'], alpha = OPACITY, label = plot_dict['label_sin'])
        ax.plot(x_plot, cos_plot, linestyle = "-", marker = '', color = plot_dict['color_cos'], alpha = OPACITY, label = plot_dict['label_cos'])
        
        plots_list.append(plot_dict)
    
    # Add the list of plots to the returned dictionary:
    timestamp_dict['plots_list'] = plots_list
    
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
            file_name = "frequency_signals"

        #check if the user defined an image resolution. If not, set as the default 110 dpi
        # resolution.
        if (png_resolution_dpi is None):
            #set as 330 dpi
            png_resolution_dpi = 330

        #Get the new_file_path
        new_file_path = os.path.join(directory_to_save, file_name)
        new_file_path = new_file_path + ".png"
        # supported formats = 'png', 'pdf', 'ps', 'eps' or 'svg'
        #Export the file to this new path:
        plt.savefig(new_file_path, dpi = png_resolution_dpi, transparent = False) 
        # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html
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
    
    return DATASET, timestamp_dict


def log_transform (df, subset = None, create_new_columns = True, add_constant = False, constant_to_add = 0, new_columns_suffix = "_log"):
    """
    log_transform (df, subset = None, create_new_columns = True, add_constant = False, constant_to_add = 0, new_columns_suffix = "_log"):
    
    : param: subset = None
      Set subset = None to transform the whole dataset. Alternatively, pass a list with 
      columns names for the transformation to be applied. For instance:
      subset = ['col1', 'col2', 'col3'] will apply the transformation to the columns named
      as 'col1', 'col2', and 'col3'. Declare the names inside quotes.
      Declaring the full list of columns is equivalent to setting subset = None.
    
    : param: create_new_columns = True
      Alternatively, set create_new_columns = True to store the transformed data into new
      columns. Or set create_new_columns = False to overwrite the existing columns
    
    : param: add_constant = False - If True, the transformation log(x + C) where C is a constant will be applied.
      constant_to_add = 0 - float number which will be added to each value that will be transformed.
      Attention: if no constant is added, but there is a negative value, the minimum needed for making
      every value positive will be added automatically. If the constant to add results in negative or
      zero values, it will be also modified to make all values non-negative (condition for applying
      log transform).
    
    : param: new_columns_suffix = "_log"
      This value has effect only if create_new_column = True.
      The new column name will be set as column + new_columns_suffix. Then, if the original
      column was "column1" and the suffix is "_log", the new column will be named as
      "column1_log".
      Alternatively, input inside quotes a string with the desired suffix. Recommendation:
      start the suffix with "_" to separate it from the original name.
    """
    
    if (constant_to_add is None):
        constant_to_add = 0
    
    # Start a local copy of the dataframe:
    DATASET = df.copy(deep = True)
    
    # Check if a subset was defined. If so, make columns_list = subset 
    if not (subset is None):
        
        columns_list = subset
    
    else:
        #There is no declared subset. Then, make columns_list equals to the list of
        # numeric columns of the dataframe.
        columns_list = list(DATASET.columns)
        
    # Let's check if there are categorical columns in columns_list. Only numerical
    # columns should remain
    # Start a support list:
    support_list = []
    # List the possible numeric data types for a Pandas dataframe column:
    numeric_dtypes = [np.int16, np.int32, np.int64, np.float16, np.float32, np.float64]
    
    # Loop through each column in columns_list:
    for column in columns_list:
        
        # Check the Pandas series (column) data type:
        column_type = DATASET[column].dtype
            
        # If it is not categorical (object), append it to the support list:
        if (column_type in numeric_dtypes):
                
            support_list.append(column)
    
    # Finally, make the columns_list support_list itself:
    columns_list = support_list
    
    # Let's define the value of the constant that must be sum:
    minimum_values = [DATASET[column].min() for column in columns_list]
    global_min = min(minimum_values)
    
    if (add_constant == False):
        if (global_min <= 0):
            constant_to_add = (0 - global_min) + 10**(-8)
            # the increment 10**-8 guarantees that it is a very low, but positive number
            print(f"Attention! The constant {constant_to_add:.6f} was added for making the transformation, guaranteeing that all values are positive.\n")
        
        else:
            constant_to_add = 0
        
    else:
        if ((global_min + constant_to_add) <= 0):
            constant_to_add = (0 - (global_min + constant_to_add)) + 10**(-8)
            # the increment 10**-8 guarantees that it is a very low, but positive number
            print(f"Attention! The constant {constant_to_add:.6f} was added for making the transformation, guaranteeing that all values are positive.\n")
    
    #Loop through each column to apply the transform:
    for column in columns_list:
        
        #Check if a new column will be created, or if the original column should be
        # substituted.
        if (create_new_columns == True):
            # Create a new column.
            
            # The new column name will be set as column + new_columns_suffix
            new_column_name = column + new_columns_suffix
        
        else:
            # Overwrite the existing column. Simply set new_column_name as the value 'column'
            new_column_name = column
        
        # Calculate the column value as the log transform of the original series (column)
        DATASET[new_column_name] = np.log(np.array(DATASET[column]) + constant_to_add)
    
    # Reset the index:
    DATASET.reset_index(drop = True)
    
    print(f"The columns X were successfully log-transformed as log(X + {constant_to_add:.6f}). Check the 10 first rows of the new dataset:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(DATASET.head(10))
            
    except: # regular mode
        print(DATASET.head(10))
    
    return DATASET

    # One curve derived from the normal is the log-normal.
    # If the values Y follow a log-normal distribution, their log follow a normal.
    # A log normal curve resembles a normal, but with skewness (distortion); 
    # and kurtosis (long-tail).

    # Applying the log is a methodology for normalizing the variables: 
    # the sample space gets shrinkled after the transformation, making the data more 
    # adequate for being processed by Machine Learning algorithms. Preferentially apply 
    # the transformation to the whole dataset, so that all variables will be of same order 
    # of magnitude.
    # Obviously, it is not necessary for variables ranging from -100 to 100 in numerical 
    # value, where most outputs from the log transformation are.


def reverse_log_transform (df, subset = None, create_new_columns = True, added_constant = 0, new_columns_suffix = "_originalScale"):
    """
    reverse_log_transform (df, subset = None, create_new_columns = True, added_constant = 0, new_columns_suffix = "_originalScale"):
    
    : param: subset = None
      Set subset = None to transform the whole dataset. Alternatively, pass a list with 
      columns names for the transformation to be applied. For instance:
      subset = ['col1', 'col2', 'col3'] will apply the transformation to the columns named
      as 'col1', 'col2', and 'col3'. Declare the names inside quotes.
      Declaring the full list of columns is equivalent to setting subset = None.
    
    : param: create_new_columns = True
      Alternatively, set create_new_columns = True to store the transformed data into new
      columns. Or set create_new_columns = False to overwrite the existing columns
    
    : param: added_constant: constant C added for making the transformation log(x + C). Check the
      output of log transform function to verify if a constant was automatically added.
    
    : param: new_columns_suffix = "_originalScale"
      This value has effect only if create_new_column = True.
      The new column name will be set as column + new_columns_suffix. Then, if the original
      column was "column1" and the suffix is "_originalScale", the new column will be named 
      as "column1_originalScale".
      Alternatively, input inside quotes a string with the desired suffix. Recommendation:
      start the suffix with "_" to separate it from the original name.
    """

    if (added_constant is None):
        added_constant = 0
    
    # Start a local copy of the dataframe:
    DATASET = df.copy(deep = True)
    
    # Check if a subset was defined. If so, make columns_list = subset 
    if not (subset is None):
        
        columns_list = subset
    
    else:
        #There is no declared subset. Then, make columns_list equals to the list of
        # numeric columns of the dataframe.
        columns_list = list(DATASET.columns)
        
    # Let's check if there are categorical columns in columns_list. Only numerical
    # columns should remain
    # Start a support list:
    support_list = []
    # List the possible numeric data types for a Pandas dataframe column:
    numeric_dtypes = [np.int16, np.int32, np.int64, np.float16, np.float32, np.float64]

    # Loop through each column in columns_list:
    for column in columns_list:
        
        # Check the Pandas series (column) data type:
        column_type = DATASET[column].dtype
            
        # If it is not categorical (object), append it to the support list:
        if (column_type in numeric_dtypes):
                
            support_list.append(column)
    
    # Finally, make the columns_list support_list itself:
    columns_list = support_list
    
    #Loop through each column to apply the transform:
    for column in columns_list:
        #access each element in the list column_list. The element is named 'column'.
        
        # The exponential transformation can be applied to zero and negative values,
        # so we remove the boolean filter.
        
        #Check if a new column will be created, or if the original column should be
        # substituted.
        if (create_new_columns == True):
            # Create a new column.
            
            # The new column name will be set as column + new_columns_suffix
            new_column_name = column + new_columns_suffix
        
        else:
            # Overwrite the existing column. Simply set new_column_name as the value 'column'
            new_column_name = column
        
        # Calculate the column value as the log transform of the original series (column)
        DATASET[new_column_name] = np.exp(np.array(DATASET[column])) - added_constant
    
    print("The log_transform was successfully reversed through the exponential transformation. Check the 10 first rows of the new dataset:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(DATASET.head(10))
            
    except: # regular mode
        print(DATASET.head(10))
    
    return DATASET


def box_cox_transform (df, column_to_transform, add_constant = False, constant_to_add = 0, mode = 'calculate_and_apply', lambda_boxcox = None, suffix = '_BoxCoxTransf', specification_limits = {'lower_spec_lim': None, 'upper_spec_lim': None}):
    """
    box_cox_transform (df, column_to_transform, add_constant = False, constant_to_add = 0, mode = 'calculate_and_apply', lambda_boxcox = None, suffix = '_BoxCoxTransf', specification_limits = {'lower_spec_lim': None, 'upper_spec_lim': None}):
    
    This function will process a single column column_to_transform 
      of the dataframe df per call.
    
    Check https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.boxcox.html
    
    ## Box-Cox transform is given by:
       y = (x**lmbda - 1) / lmbda,  for lmbda != 0
       log(x),                      for lmbda = 0
    
    : param: column_to_transform must be a string with the name of the column.
      e.g. column_to_transform = 'column1' to transform a column named as 'column1'
    
    : param: add_constant = False - If True, the transformation log(x + C) where C is a constant will be applied.
      constant_to_add = 0 - float number which will be added to each value that will be transformed.
      Attention: if no constant is added, but there is a negative value, the minimum needed for making
      every value positive will be added automatically. If the constant to add results in negative or
      zero values, it will be also modified to make all values non-negative (condition for applying
      log transform).
    
    : param: mode = 'calculate_and_apply'
      Aternatively, mode = 'calculate_and_apply' to calculate lambda and apply Box-Cox
      transform; mode = 'apply_only' to apply the transform for a known lambda.
      To 'apply_only', lambda_box must be provided.
    
    : param: lambda_boxcox must be a float value. e.g. lamda_boxcox = 1.7
      If you calculated lambda from the function box_cox_transform and saved the
      transformation data summary dictionary as data_sum_dict, simply set:
      lambda_boxcox = data_sum_dict['lambda_boxcox']
      This will access the value on the key 'lambda_boxcox' of the dictionary, which
      contains the lambda. 
    
      Analogously, spec_lim_dict['Inf_spec_lim_transf'] access
      the inferior specification limit transformed; and spec_lim_dict['Sup_spec_lim_transf'] 
      access the superior specification limit transformed.
    
      If lambda_boxcox is None, 
      the mode will be automatically set as 'calculate_and_apply'.
    
    : param: suffix: string (inside quotes).
      How the transformed column will be identified in the returned data_transformed_df.
      If y_label = 'Y' and suffix = '_BoxCoxTransf', the transformed column will be
      identified as 'Y_BoxCoxTransf'.
      Alternatively, input inside quotes a string with the desired suffix. Recommendation:
      start the suffix with "_" to separate it from the original name
    
    : param: specification_limits = {'lower_spec_lim': None, 'upper_spec_lim': None}
      If there are specification limits, input them in this dictionary. Do not modify the keys,
      simply substitute None by the lower and/or the upper specification.
      e.g. Suppose you have a tank that cannot have more than 10 L. So:
      specification_limits = {'lower_spec_lim': None, 'upper_spec_lim': 10}, there is only
      an upper specification equals to 10 (do not add units);
      Suppose a temperature cannot be lower than 10 ºC, but there is no upper specification. So,
      specification_limits = {'lower_spec_lim': 10, 'upper_spec_lim': None}. Finally, suppose
      a liquid which pH must be between 6.8 and 7.2:
      specification_limits = {'lower_spec_lim': 6.8, 'upper_spec_lim': 7.2}
    """

    from statsmodels.stats import diagnostic
    from scipy import stats
   
    if (constant_to_add is None):
        constant_to_add = 0
        
    if not (suffix is None):
        #only if a suffix was declared
        #concatenate the column name to the suffix
        new_col = column_to_transform + suffix
    
    else:
        #concatenate the column name to the standard '_BoxCoxTransf' suffix
        new_col = column_to_transform + '_BoxCoxTransf'
    
    boolean_check = (mode != 'calculate_and_apply') & (mode != 'apply_only')
    # & is the 'and' operator. != is the 'is different from' operator.
    #Check if neither 'calculate_and_apply' nor 'apply_only' were selected
    
    if ((lambda_boxcox is None) & (mode == 'apply_only')):
        print("Invalid value set for \'lambda_boxcox'\. Setting mode to \'calculate_and_apply\'.\n")
        mode = 'calculate_and_apply'
    
    elif (boolean_check == True):
        print("Invalid value set for \'mode'\. Setting mode to \'calculate_and_apply\'.\n")
        mode = 'calculate_and_apply'
    
    
    # Start a local copy of the dataframe:
    DATASET = df.copy(deep = True)
    y = np.array(DATASET[column_to_transform])
    
    # Check the minimum value assumed by y
    global_min = min(y)
    
    if (add_constant == False):
        if (global_min <= 0):
            constant_to_add = (0 - global_min) + 10**(-8)
            # the increment 10**-8 guarantees that it is a very low, but positive number
            print(f"Attention! The constant {constant_to_add:.6f} was added for making the transformation, guaranteeing that all values are positive.")
            print(f"So, the constant {constant_to_add:.6f} was added to each value from {column_to_transform} before transforming the data.\n")
            
            # increment the variable y:
            y = y + constant_to_add
            
        else:
            if ((global_min + constant_to_add) <= 0):
                constant_to_add = (0 - (global_min + constant_to_add)) + 10**(-8)
                # the increment 10**-8 guarantees that it is a very low, but positive number
                print(f"Attention! The constant {constant_to_add:.6f} was added for making the transformation, guaranteeing that all values are positive.")
                print(f"So, the constant {constant_to_add:.6f} was added to each value from {column_to_transform} before transforming the data.\n")

            # increment the variable y:
            y = y + constant_to_add
                
        
    if (mode == 'calculate_and_apply'):
        # Calculate lambda_boxcox
        lambda_boxcox = stats.boxcox_normmax(y, method = 'pearsonr')
        #calcula o lambda da transformacao box-cox utilizando o metodo da maxima verossimilhanca
        #por meio da maximizacao do coeficiente de correlacao de pearson da funcao
        #y = boxcox(x), onde boxcox representa a transformacao
    
    # For other cases, we will apply the lambda_boxcox set as the function parameter.

    #Calculo da variavel transformada
    y_transform = stats.boxcox(y, lmbda = lambda_boxcox, alpha = None)
    #Calculo da transformada
    
    DATASET[new_col] = y_transform
    #dataframe contendo os dados transformados
    
    print("Data successfully transformed. Check the 10 first transformed rows:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(DATASET.head(10))
            
    except: # regular mode
        print(DATASET.head(10))
        
    print("\n") #line break
    
    # Start a dictionary to store the summary results of the transform and the normality
    # tests:
    data_sum_dict = {'lambda_boxcox': lambda_boxcox}
    
    data_sum_dict['added_constant'] = constant_to_add
    
    # Test normality of the transformed variable:
    # Scipy.stats’ normality test
    # It is based on D’Agostino and Pearson’s test that combines 
    # skew and kurtosis to produce an omnibus test of normality.
    _, scipystats_test_pval = stats.normaltest(y_transform) 
    # add this test result to the dictionary:
    data_sum_dict['dagostino_pearson_p_val'] = scipystats_test_pval
            
    # Scipy.stats’ Shapiro-Wilk test
    shapiro_test = stats.shapiro(y_transform)
    data_sum_dict['shapiro_wilk_p_val'] = shapiro_test[1]
    
    # Lilliefors’ normality test
    lilliefors_test = diagnostic.kstest_normal(y_transform, dist = 'norm', pvalmethod = 'table')
    data_sum_dict['lilliefors_p_val'] = lilliefors_test[1]
    
    # Anderson-Darling normality test
    ad_test = diagnostic.normal_ad(y_transform, axis = 0)
    data_sum_dict['anderson_darling_p_val'] = ad_test[1]
    
    print("Box-Cox Transformation Summary:\n")
    try:
        display(data_sum_dict)     
    except:
        print(data_sum_dict)
    
    print("\n") #line break
    
    if not ((specification_limits['lower_spec_lim'] is None) & (specification_limits['upper_spec_lim'] is None)):
        # Convert it to a list of specs:
        list_of_specs = []
        
        if not (specification_limits['lower_spec_lim'] is None):
            
            if (specification_limits['lower_spec_lim'] <= 0):
                print("Box-Cox transform can only be applied to values higher than zero. So, ignoring the lower specification.\n")
            
            else:
                list_of_specs.append(specification_limits['lower_spec_lim'])
        
        if not (specification_limits['upper_spec_lim'] is None):
            
            if (specification_limits['upper_spec_lim'] <= 0):
                print("Box-Cox transform can only be applied to values higher than zero. So, ignoring the upper specification.\n")
            
            else:
                list_of_specs.append(specification_limits['upper_spec_lim'])
        
        # Notice that the list may have 1 or 2 elements.
        
        # Convert the list of specifications into a NumPy array:
        spec_lim_array = np.array(list_of_specs)
        
        # If the array has a single element, we cannot apply stats method. So, let's transform
        # manually:
        ## y = (x**lmbda - 1) / lmbda,  for lmbda != 0
        ## log(x),                  for lmbda = 0
        if (lambda_boxcox == 0):
            
            spec_lim_array = np.log(spec_lim_array)
        
        else:
            spec_lim_array = ((spec_lim_array**lambda_boxcox) - 1)/(lambda_boxcox)
        
        # Start a dictionary to store the transformed limits:
        spec_lim_dict = {}
        
        if not (specification_limits['lower_spec_lim'] is None):
            # First element of the array is the lower specification. Add it to the
            # dictionary:
            spec_lim_dict['lower_spec_lim_transf'] = spec_lim_array[0]
            
            if not (specification_limits['upper_spec_lim'] is None):
                # Second element of the array is the upper specification. Add it to the
                # dictionary:
                spec_lim_dict['upper_spec_lim_transf'] = spec_lim_array[1]
        
        else:
            # The array contains only one element, which is the upper specification. Add
            # it to the dictionary:
            spec_lim_dict['upper_spec_lim_transf'] = spec_lim_array[0]
        
        print("New specification limits successfully obtained:\n")
        try:
            display(spec_lim_dict)     
        except:
            print(spec_lim_dict)
        
        # Add spec_lim_dict as a new element from data_sum_dict:
        data_sum_dict['spec_lim_dict'] = spec_lim_dict
    
    
    return DATASET, data_sum_dict


def reverse_box_cox (df, column_to_transform, lambda_boxcox, added_constant = 0, suffix = '_ReversedBoxCox'):
    """
    reverse_box_cox (df, column_to_transform, lambda_boxcox, added_constant = 0, suffix = '_ReversedBoxCox'):
    
    This function will process a single column column_to_transform 
      of the dataframe df per call.
    
    Check https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.boxcox.html
    
    ## Box-Cox transform is given by:
       y = (x**lmbda - 1) / lmbda,  for lmbda != 0
       log(x),                      for lmbda = 0
    
    : param: column_to_transform must be a string with the name of the column.
      e.g. column_to_transform = 'column1' to transform a column named as 'column1'
    
    : param: lambda_boxcox must be a float value. e.g. lamda_boxcox = 1.7
      If you calculated lambda from the function box_cox_transform and saved the
      transformation data summary dictionary as data_sum_dict, simply set:
      lambda_boxcox = data_sum_dict['lambda_boxcox']
      This will access the value on the key 'lambda_boxcox' of the dictionary, which
      contains the lambda. 
    
      Analogously, spec_lim_dict['Inf_spec_lim_transf'] access
      the inferior specification limit transformed; and spec_lim_dict['Sup_spec_lim_transf'] 
      access the superior specification limit transformed.
    
    : param: added_constant: constant C added for making the transformation log(x + C). Check the
      output of Box-Cox transform function to verify if a constant was automatically added.
        
    : param: suffix: string (inside quotes).
      How the transformed column will be identified in the returned data_transformed_df.
      If y_label = 'Y' and suffix = '_ReversedBoxCox', the transformed column will be
      identified as '_ReversedBoxCox'.
      Alternatively, input inside quotes a string with the desired suffix. Recommendation:
      start the suffix with "_" to separate it from the original name
    """

    if (added_constant is None):
        added_constant = 0
            
    # Start a local copy of the dataframe:
    DATASET = df.copy(deep = True)

    y = DATASET[column_to_transform]
    
    if (lambda_boxcox == 0):
        #ytransf = np.log(y), according to Box-Cox definition. Then
        #y_retransform = np.exp(y)
        #In the case of this function, ytransf is passed as the argument y.
        y_transform = np.exp(y)
    
    else:
        #apply Box-Cox function:
        #y_transf = (y**lmbda - 1) / lmbda. Then,
        #y_retransf ** (lmbda) = (y_transf * lmbda) + 1
        #y_retransf = ((y_transf * lmbda) + 1) ** (1/lmbda), where ** is the potentiation
        #In the case of this function, ytransf is passed as the argument y.
        y_transform = ((y * lambda_boxcox) + 1) ** (1/lambda_boxcox)
    
    if not (suffix is None):
        #only if a suffix was declared
        #concatenate the column name to the suffix
        new_col = column_to_transform + suffix
    
    else:
        #concatenate the column name to the standard '_ReversedBoxCox' suffix
        new_col = column_to_transform + '_ReversedBoxCox'
    
    # remove the constant from the variable y_transform:
    y_transform = y_transform - added_constant
    
    DATASET[new_col] = y_transform
    #dataframe contendo os dados transformados
    
    print("Data successfully retransformed. Check the 10 first retransformed rows:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(DATASET.head(10))
            
    except: # regular mode
        print(DATASET.head(10))
    
    print("\n") #line break

    return DATASET


def square_root_transform (df, subset = None, create_new_columns = True, add_constant = False, constant_to_add = 0, new_columns_suffix = "_sqrt"):
    """
    square_root_transform (df, subset = None, create_new_columns = True, add_constant = False, constant_to_add = 0, new_columns_suffix = "_sqrt"):
    
    : param: subset = None
      Set subset = None to transform the whole dataset. Alternatively, pass a list with 
      columns names for the transformation to be applied. For instance:
      subset = ['col1', 'col2', 'col3'] will apply the transformation to the columns named
      as 'col1', 'col2', and 'col3'. Declare the names inside quotes.
      Declaring the full list of columns is equivalent to setting subset = None.
    
    : param: create_new_columns = True
      Alternatively, set create_new_columns = True to store the transformed data into new
      columns. Or set create_new_columns = False to overwrite the existing columns
    
    : param: add_constant = False - If True, the transformation sqrt(x + C) where C is a constant will be applied.
      constant_to_add = 0 - float number which will be added to each value that will be transformed.
      Attention: if no constant is added, but there is a negative value, the minimum needed for making
      every value positive will be added automatically. If the constant to add results in negative or
      zero values, it will be also modified to make all values non-negative (condition for applying
      square root).
    
    : param: new_columns_suffix = "_sqrt"
      This value has effect only if create_new_column = True.
      The new column name will be set as column + new_columns_suffix. Then, if the original
      column was "column1" and the suffix is "_log", the new column will be named as
      "column1_log".
      Alternatively, input inside quotes a string with the desired suffix. Recommendation:
      start the suffix with "_" to separate it from the original name.
    """

    if (constant_to_add is None):
        constant_to_add = 0
    
    # Start a local copy of the dataframe:
    DATASET = df.copy(deep = True)
    
    # Check if a subset was defined. If so, make columns_list = subset 
    if not (subset is None):
        
        columns_list = subset
    
    else:
        #There is no declared subset. Then, make columns_list equals to the list of
        # numeric columns of the dataframe.
        columns_list = list(DATASET.columns)
        
    # Let's check if there are categorical columns in columns_list. Only numerical
    # columns should remain
    # Start a support list:
    support_list = []
    # List the possible numeric data types for a Pandas dataframe column:
    numeric_dtypes = [np.int16, np.int32, np.int64, np.float16, np.float32, np.float64]
    
    # Loop through each column in columns_list:
    for column in columns_list:
        
        # Check the Pandas series (column) data type:
        column_type = DATASET[column].dtype
            
        # If it is not categorical (object), append it to the support list:
        if (column_type in numeric_dtypes):
                
            support_list.append(column)
    
    # Finally, make the columns_list support_list itself:
    columns_list = support_list
    
    # Let's define the value of the constant that must be sum:
    minimum_values = [DATASET[column].min() for column in columns_list]
    global_min = min(minimum_values)
    
    if (add_constant == False):
        if (global_min <= 0):
            constant_to_add = (0 - global_min) + 10**(-8)
            # the increment 10**-8 guarantees that it is a very low, but positive number
            print(f"Attention! The constant {constant_to_add:.6f} was added for making the transformation, guaranteeing that all values are positive.\n")
        
        else:
            constant_to_add = 0
        
    else:
        if ((global_min + constant_to_add) <= 0):
            constant_to_add = (0 - (global_min + constant_to_add)) + 10**(-8)
            # the increment 10**-8 guarantees that it is a very low, but positive number
            print(f"Attention! The constant {constant_to_add:.6f} was added for making the transformation, guaranteeing that all values are positive.\n")
    
    #Loop through each column to apply the transform:
    for column in columns_list:
        
        #Check if a new column will be created, or if the original column should be
        # substituted.
        if (create_new_columns == True):
            # Create a new column.
            
            # The new column name will be set as column + new_columns_suffix
            new_column_name = column + new_columns_suffix
        
        else:
            # Overwrite the existing column. Simply set new_column_name as the value 'column'
            new_column_name = column
        
        # Calculate the column value as the log transform of the original series (column)
        DATASET[new_column_name] = np.sqrt(np.array(DATASET[column]) + constant_to_add)
    
    # Reset the index:
    DATASET.reset_index(drop = True)
    
    print(f"The columns X were successfully transformed as square_root(X + {constant_to_add:.6f}). Check the 10 first rows of the new dataset:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(DATASET.head(10))
            
    except: # regular mode
        print(DATASET.head(10))
    
    return DATASET


def reverse_square_root_transform (df, subset = None, create_new_columns = True, added_constant = 0, new_columns_suffix = "_originalScale"):
    """
    reverse_square_root_transform (df, subset = None, create_new_columns = True, added_constant = 0, new_columns_suffix = "_originalScale"):
    
    : param: subset = None
      Set subset = None to transform the whole dataset. Alternatively, pass a list with 
      columns names for the transformation to be applied. For instance:
      subset = ['col1', 'col2', 'col3'] will apply the transformation to the columns named
      as 'col1', 'col2', and 'col3'. Declare the names inside quotes.
      Declaring the full list of columns is equivalent to setting subset = None.
    
    : param: create_new_columns = True
      Alternatively, set create_new_columns = True to store the transformed data into new
      columns. Or set create_new_columns = False to overwrite the existing columns
    
    : param: added_constant: constant C added for making the transformation sqrt(x + C). Check the
      output of sqrt transform function to verify if a constant was automatically added.
    
    : param: new_columns_suffix = "_originalScale"
      This value has effect only if create_new_column = True.
      The new column name will be set as column + new_columns_suffix. Then, if the original
      column was "column1" and the suffix is "_originalScale", the new column will be named 
      as "column1_originalScale".
      Alternatively, input inside quotes a string with the desired suffix. Recommendation:
      start the suffix with "_" to separate it from the original name.
    """

    if (added_constant is None):
        added_constant = 0
    
    # Start a local copy of the dataframe:
    DATASET = df.copy(deep = True)
    
    # Check if a subset was defined. If so, make columns_list = subset 
    if not (subset is None):
        
        columns_list = subset
    
    else:
        #There is no declared subset. Then, make columns_list equals to the list of
        # numeric columns of the dataframe.
        columns_list = list(DATASET.columns)
        
    # Let's check if there are categorical columns in columns_list. Only numerical
    # columns should remain
    # Start a support list:
    support_list = []
    # List the possible numeric data types for a Pandas dataframe column:
    numeric_dtypes = [np.int16, np.int32, np.int64, np.float16, np.float32, np.float64]

    # Loop through each column in columns_list:
    for column in columns_list:
        
        # Check the Pandas series (column) data type:
        column_type = DATASET[column].dtype
            
        # If it is not categorical (object), append it to the support list:
        if (column_type in numeric_dtypes):
                
            support_list.append(column)
    
    # Finally, make the columns_list support_list itself:
    columns_list = support_list
    
    #Loop through each column to apply the transform:
    for column in columns_list:
        #access each element in the list column_list. The element is named 'column'.
        
        # The exponential transformation can be applied to zero and negative values,
        # so we remove the boolean filter.
        
        #Check if a new column will be created, or if the original column should be
        # substituted.
        if (create_new_columns == True):
            # Create a new column.
            
            # The new column name will be set as column + new_columns_suffix
            new_column_name = column + new_columns_suffix
        
        else:
            # Overwrite the existing column. Simply set new_column_name as the value 'column'
            new_column_name = column
        
        # Calculate the column value as the log transform of the original series (column)
        DATASET[new_column_name] = np.power(np.array(DATASET[column]), 2) - added_constant
    
    print("The square root transform was successfully reversed through the power transformation. Check the 10 first rows of the new dataset:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(DATASET.head(10))
            
    except: # regular mode
        print(DATASET.head(10))
    
    return DATASET


def cube_root_transform (df, subset = None, create_new_columns = True, add_constant = False, constant_to_add = 0, new_columns_suffix = "_cbrt"):
    """
    cube_root_transform (df, subset = None, create_new_columns = True, add_constant = False, constant_to_add = 0, new_columns_suffix = "_cbrt"):
    
    : param: subset = None
      Set subset = None to transform the whole dataset. Alternatively, pass a list with 
      columns names for the transformation to be applied. For instance:
      subset = ['col1', 'col2', 'col3'] will apply the transformation to the columns named
      as 'col1', 'col2', and 'col3'. Declare the names inside quotes.
      Declaring the full list of columns is equivalent to setting subset = None.
    
    : param: create_new_columns = True
      Alternatively, set create_new_columns = True to store the transformed data into new
      columns. Or set create_new_columns = False to overwrite the existing columns
    
    : param: add_constant = False - If True, the transformation cbrt(x + C) where C is a constant will be applied.
      constant_to_add = 0 - float number which will be added to each value that will be transformed.
    
    : param: new_columns_suffix = "_cbrt"
      This value has effect only if create_new_column = True.
      The new column name will be set as column + new_columns_suffix. Then, if the original
      column was "column1" and the suffix is "_log", the new column will be named as
      "column1_log".
      Alternatively, input inside quotes a string with the desired suffix. Recommendation:
      start the suffix with "_" to separate it from the original name.
    """

    if (constant_to_add is None):
        constant_to_add = 0
    
    # Start a local copy of the dataframe:
    DATASET = df.copy(deep = True)
    
    # Check if a subset was defined. If so, make columns_list = subset 
    if not (subset is None):
        
        columns_list = subset
    
    else:
        #There is no declared subset. Then, make columns_list equals to the list of
        # numeric columns of the dataframe.
        columns_list = list(DATASET.columns)
        
    # Let's check if there are categorical columns in columns_list. Only numerical
    # columns should remain
    # Start a support list:
    support_list = []
    # List the possible numeric data types for a Pandas dataframe column:
    numeric_dtypes = [np.int16, np.int32, np.int64, np.float16, np.float32, np.float64]
    
    # Loop through each column in columns_list:
    for column in columns_list:
        
        # Check the Pandas series (column) data type:
        column_type = DATASET[column].dtype
            
        # If it is not categorical (object), append it to the support list:
        if (column_type in numeric_dtypes):
                
            support_list.append(column)
    
    # Finally, make the columns_list support_list itself:
    columns_list = support_list
    
    
    #Loop through each column to apply the transform:
    for column in columns_list:
        
        #Check if a new column will be created, or if the original column should be
        # substituted.
        if (create_new_columns == True):
            # Create a new column.
            
            # The new column name will be set as column + new_columns_suffix
            new_column_name = column + new_columns_suffix
        
        else:
            # Overwrite the existing column. Simply set new_column_name as the value 'column'
            new_column_name = column
        
        # Calculate the column value as the log transform of the original series (column)
        DATASET[new_column_name] = np.cbrt(np.array(DATASET[column]) + constant_to_add)
    
    # Reset the index:
    DATASET.reset_index(drop = True)
    
    print(f"The columns X were successfully transformed as cube_root(X + {constant_to_add:.6f}). Check the 10 first rows of the new dataset:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(DATASET.head(10))
            
    except: # regular mode
        print(DATASET.head(10))
    
    return DATASET


def reverse_cube_root_transform (df, subset = None, create_new_columns = True, added_constant = 0, new_columns_suffix = "_originalScale"):
    """
    reverse_cube_root_transform (df, subset = None, create_new_columns = True, added_constant = 0, new_columns_suffix = "_originalScale"):
    
    : param: subset = None
      Set subset = None to transform the whole dataset. Alternatively, pass a list with 
      columns names for the transformation to be applied. For instance:
      subset = ['col1', 'col2', 'col3'] will apply the transformation to the columns named
      as 'col1', 'col2', and 'col3'. Declare the names inside quotes.
      Declaring the full list of columns is equivalent to setting subset = None.
    
    : param: create_new_columns = True
      Alternatively, set create_new_columns = True to store the transformed data into new
      columns. Or set create_new_columns = False to overwrite the existing columns
    
    : param: added_constant: constant C added for making the transformation cbrt(x + C). Check the
      output of cbrt transform function to verify if a constant was automatically added.
    
    : param: new_columns_suffix = "_originalScale"
      This value has effect only if create_new_column = True.
      The new column name will be set as column + new_columns_suffix. Then, if the original
      column was "column1" and the suffix is "_originalScale", the new column will be named 
      as "column1_originalScale".
      Alternatively, input inside quotes a string with the desired suffix. Recommendation:
      start the suffix with "_" to separate it from the original name.
    """

    if (added_constant is None):
        added_constant = 0
    
    # Start a local copy of the dataframe:
    DATASET = df.copy(deep = True)
    
    # Check if a subset was defined. If so, make columns_list = subset 
    if not (subset is None):
        
        columns_list = subset
    
    else:
        #There is no declared subset. Then, make columns_list equals to the list of
        # numeric columns of the dataframe.
        columns_list = list(DATASET.columns)
        
    # Let's check if there are categorical columns in columns_list. Only numerical
    # columns should remain
    # Start a support list:
    support_list = []
    # List the possible numeric data types for a Pandas dataframe column:
    numeric_dtypes = [np.int16, np.int32, np.int64, np.float16, np.float32, np.float64]

    # Loop through each column in columns_list:
    for column in columns_list:
        
        # Check the Pandas series (column) data type:
        column_type = DATASET[column].dtype
            
        # If it is not categorical (object), append it to the support list:
        if (column_type in numeric_dtypes):
                
            support_list.append(column)
    
    # Finally, make the columns_list support_list itself:
    columns_list = support_list
    
    #Loop through each column to apply the transform:
    for column in columns_list:
        #access each element in the list column_list. The element is named 'column'.
        
        # The exponential transformation can be applied to zero and negative values,
        # so we remove the boolean filter.
        
        #Check if a new column will be created, or if the original column should be
        # substituted.
        if (create_new_columns == True):
            # Create a new column.
            
            # The new column name will be set as column + new_columns_suffix
            new_column_name = column + new_columns_suffix
        
        else:
            # Overwrite the existing column. Simply set new_column_name as the value 'column'
            new_column_name = column
        
        # Calculate the column value as the log transform of the original series (column)
        DATASET[new_column_name] = np.power(np.array(DATASET[column]), 3) - added_constant
    
    print("The cube root transform was successfully reversed through the power transformation. Check the 10 first rows of the new dataset:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(DATASET.head(10))
            
    except: # regular mode
        print(DATASET.head(10))
    
    return DATASET


def power_transform (df, exponent = 2, subset = None, create_new_columns = True, add_constant = False, constant_to_add = 0, new_columns_suffix = "_pow"):
    """
    power_transform (df, exponent = 2, subset = None, create_new_columns = True, add_constant = False, constant_to_add = 0, new_columns_suffix = "_pow"):
    
    : param: subset = None
      Set subset = None to transform the whole dataset. Alternatively, pass a list with 
      columns names for the transformation to be applied. For instance:
      subset = ['col1', 'col2', 'col3'] will apply the transformation to the columns named
      as 'col1', 'col2', and 'col3'. Declare the names inside quotes.
      Declaring the full list of columns is equivalent to setting subset = None.
    
    : param: exponent = 2 - the exponent of the power function. Positive values or fractions may be used
      as exponents. Example: exponent = 10 raises X to 10th power (X^10), exponent = 0.5 raises to 0.5 
      (X^0.5 = X ^(1/2) = square root (X)). 
      exponent = 1/10 calculates the 10th root (X^(1/10))
    
    : param: create_new_columns = True
      Alternatively, set create_new_columns = True to store the transformed data into new
      columns. Or set create_new_columns = False to overwrite the existing columns
    
    : param: add_constant = False - If True, the transformation power(x + C) where C is a constant will be applied.
      constant_to_add = 0 - float number which will be added to each value that will be transformed.
      Attention: if no constant is added, but there is a negative value that makes it impossible to
      apply the power function, the minimum needed for making
      every value positive will be added automatically. If the constant to add results in negative or
      zero values, it will be also modified to make all values non-negative.
    
    : param: new_columns_suffix = "_pow"
      This value has effect only if create_new_column = True.
      The new column name will be set as column + new_columns_suffix. Then, if the original
      column was "column1" and the suffix is "_log", the new column will be named as
      "column1_log".
      Alternatively, input inside quotes a string with the desired suffix. Recommendation:
      start the suffix with "_" to separate it from the original name.
    """

    if (exponent == 0):
        exponent = 1
        print("Zero-power not allowed for this function. Exponent set to 1.\n")
    
    if (constant_to_add is None):
        constant_to_add = 0
    
    # Start a local copy of the dataframe:
    DATASET = df.copy(deep = True)
    
    # Check if a subset was defined. If so, make columns_list = subset 
    if not (subset is None):
        
        columns_list = subset
    
    else:
        #There is no declared subset. Then, make columns_list equals to the list of
        # numeric columns of the dataframe.
        columns_list = list(DATASET.columns)
        
    # Let's check if there are categorical columns in columns_list. Only numerical
    # columns should remain
    # Start a support list:
    support_list = []
    # List the possible numeric data types for a Pandas dataframe column:
    numeric_dtypes = [np.int16, np.int32, np.int64, np.float16, np.float32, np.float64]
    
    # Loop through each column in columns_list:
    for column in columns_list:
        
        # Check the Pandas series (column) data type:
        column_type = DATASET[column].dtype
            
        # If it is not categorical (object), append it to the support list:
        if (column_type in numeric_dtypes):
                
            support_list.append(column)
    
    # Finally, make the columns_list support_list itself:
    columns_list = support_list
    
    # Let's define the value of the constant that must be sum:
    minimum_values = [DATASET[column].min() for column in columns_list]
    global_min = min(minimum_values)
    
    # check if the selected power may be applied to this global_min or if it is a negative or zero-value
    # and the power do not accept such value:
    try:
        test = float(global_min**exponent)
        # if test passed (no error was raised), there are no restrictions
        # The test will fail if the operation results in a complex instead of real number
    
    except:

        if (add_constant == False):
            if (global_min <= 0):
                constant_to_add = (0 - global_min) + 10**(-8)
                # the increment 10**-8 guarantees that it is a very low, but positive number
                print(f"Attention! The constant {constant_to_add:.6f} was added for making the transformation, guaranteeing that all values are positive.\n")

            else:
                constant_to_add = 0

        else:
            if ((global_min + constant_to_add) <= 0):
                constant_to_add = (0 - (global_min + constant_to_add)) + 10**(-8)
                # the increment 10**-8 guarantees that it is a very low, but positive number
                print(f"Attention! The constant {constant_to_add:.6f} was added for making the transformation, guaranteeing that all values are positive.\n")

    #Loop through each column to apply the transform:
    for column in columns_list:
        
        #Check if a new column will be created, or if the original column should be
        # substituted.
        if (create_new_columns == True):
            # Create a new column.
            
            # The new column name will be set as column + new_columns_suffix
            new_column_name = column + new_columns_suffix
        
        else:
            # Overwrite the existing column. Simply set new_column_name as the value 'column'
            new_column_name = column
        
        # Calculate the column value as the log transform of the original series (column)
        DATASET[new_column_name] = (np.array(DATASET[column]) + constant_to_add)**exponent
    
    # Reset the index:
    DATASET.reset_index(drop = True)
    
    print(f"The columns X were successfully transformed as (X + {constant_to_add:.6f})^{exponent:.6f}. Check the 10 first rows of the new dataset:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(DATASET.head(10))
            
    except: # regular mode
        print(DATASET.head(10))
    
    return DATASET


def reverse_power_transform (df, original_exponent = 2, subset = None, create_new_columns = True, added_constant = 0, new_columns_suffix = "_originalScale"):
    """
    reverse_power_transform (df, original_exponent = 2, subset = None, create_new_columns = True, added_constant = 0, new_columns_suffix = "_originalScale"):
    
    : param: subset = None
    : param: Set subset = None to transform the whole dataset. Alternatively, pass a list with 
      columns names for the transformation to be applied. For instance:
      subset = ['col1', 'col2', 'col3'] will apply the transformation to the columns named
      as 'col1', 'col2', and 'col3'. Declare the names inside quotes.
      Declaring the full list of columns is equivalent to setting subset = None.
    
    : param: original_exponent = 2 - the exponent of the power function used for transforming. 
      Positive values or fractions may be used
      as exponents. Set the exact same number used on the original transformation in order to
      reverse it. It corresponds to apply the power function with the inverted exponent
    
    : param: create_new_columns = True
      Alternatively, set create_new_columns = True to store the transformed data into new
      columns. Or set create_new_columns = False to overwrite the existing columns
    
    : param: added_constant: constant C added for making the transformation power(x + C). Check the
      output of power transform function to verify if a constant was automatically added.
    
    : param: new_columns_suffix = "_originalScale"
      This value has effect only if create_new_column = True.
      The new column name will be set as column + new_columns_suffix. Then, if the original
      column was "column1" and the suffix is "_originalScale", the new column will be named 
      as "column1_originalScale".
      Alternatively, input inside quotes a string with the desired suffix. Recommendation:
      start the suffix with "_" to separate it from the original name.
    """

    if (original_exponent == 0):
        exponent = 1
        print("Zero-power not allowed for this function. Exponent set to 1.\n")
    else:
        # Reverse the exponent
        exponent = 1/original_exponent
    
    
    if (added_constant is None):
        added_constant = 0
    
    # Start a local copy of the dataframe:
    DATASET = df.copy(deep = True)
    
    # Check if a subset was defined. If so, make columns_list = subset 
    if not (subset is None):
        
        columns_list = subset
    
    else:
        #There is no declared subset. Then, make columns_list equals to the list of
        # numeric columns of the dataframe.
        columns_list = list(DATASET.columns)
        
    # Let's check if there are categorical columns in columns_list. Only numerical
    # columns should remain
    # Start a support list:
    support_list = []
    # List the possible numeric data types for a Pandas dataframe column:
    numeric_dtypes = [np.int16, np.int32, np.int64, np.float16, np.float32, np.float64]

    # Loop through each column in columns_list:
    for column in columns_list:
        
        # Check the Pandas series (column) data type:
        column_type = DATASET[column].dtype
            
        # If it is not categorical (object), append it to the support list:
        if (column_type in numeric_dtypes):
                
            support_list.append(column)
    
    # Finally, make the columns_list support_list itself:
    columns_list = support_list
    
    # Let's define the value of the constant that must be sum:
    minimum_values = [DATASET[column].min() for column in columns_list]
    global_min = min(minimum_values)
        
    # check if the selected power may be applied to this global_min or if it is a negative or zero-value
    # and the power do not accept such value:
    try:
        test = float(global_min**exponent)
        # if test passed (no error was raised), there are no restrictions
        # The test will fail if the operation results in a complex instead of real number
        
    except:
        print(f"Detected a value {global_min} in the data that cannot be submitted to the inversion ({exponent}-power).\n")
        
    #Loop through each column to apply the transform:
    for column in columns_list:
        #access each element in the list column_list. The element is named 'column'.
        
        # The exponential transformation can be applied to zero and negative values,
        # so we remove the boolean filter.
        
        #Check if a new column will be created, or if the original column should be
        # substituted.
        if (create_new_columns == True):
            # Create a new column.
            
            # The new column name will be set as column + new_columns_suffix
            new_column_name = column + new_columns_suffix
        
        else:
            # Overwrite the existing column. Simply set new_column_name as the value 'column'
            new_column_name = column
        
        # Calculate the column value as the log transform of the original series (column)
        DATASET[new_column_name] = (np.array(DATASET[column]))**exponent - added_constant
    
    print("The power was successfully reversed through the exponential transformation. Check the 10 first rows of the new dataset:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(DATASET.head(10))
            
    except: # regular mode
        print(DATASET.head(10))
    
    return DATASET


def OneHotEncoding_df (df, subset_of_features_to_be_encoded):
    """
    OneHotEncoding_df (df, subset_of_features_to_be_encoded)

    https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html
    
    : param: df: the whole dataframe to be processed.
    
    : param: subset_of_features_to_be_encoded: list of strings (inside quotes), 
      containing the names of the columns with the categorical variables that will be 
      encoded. If a single column will be encoded, declare this parameter as list with
      only one element e.g.subset_of_features_to_be_encoded = ["column1"] 
      will analyze the column named as 'column1'; 
      subset_of_features_to_be_encoded = ["col1", 'col2', 'col3'] will analyze 3 columns
      with categorical variables: 'col1', 'col2', and 'col3'.
    """

    from sklearn.preprocessing import OneHotEncoder
    
    #Start an encoding list empty (it will be a JSON object):
    encoding_list = []
    
    # Start a copy of the original dataframe. This copy will be updated to create the new
    # transformed dataframe. Then, we avoid manipulating the original object.
    new_df = df.copy(deep = True)
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display  
    except:
        pass
    
    #loop through each column of the subset:
    for column in subset_of_features_to_be_encoded:
        
        # Start two empty dictionaries:
        encoding_dict = {}
        nested_dict = {}
        
        # Add the column to encoding_dict as the key 'column':
        encoding_dict['column'] = column
        
        # Loop through each element (named 'column') of the list of columns to analyze,
        # subset_of_features_to_be_encoded
        
        # We could process the whole subset at once, but it could make us lose information
        # about the generated columns
        
        # set a subset of the dataframe X containing 'column' as the only column:
        # it will be equivalent to using .reshape(-1,1) to set a 1D-series
        # or array in the shape for scikit-learn:
        # For doing so, pass a list of columns for column filtering, containing
        # the object column as its single element:
        X  = df[[column]]
        
        #Start the OneHotEncoder object:
        OneHot_enc_obj = OneHotEncoder()
        
        #Fit the object to that column:
        OneHot_enc_obj = OneHot_enc_obj.fit(X)
        # Get the transformed columns as a SciPy sparse matrix: 
        transformed_columns = OneHot_enc_obj.transform(X)
        # Convert the sparse matrix to a NumPy dense array:
        transformed_columns = transformed_columns.toarray()
        
        # Now, let's retrieve the encoding information and save it:
        # Show encoded categories and store this array. 
        # It will give the proper columns' names:
        encoded_columns = OneHot_enc_obj.categories_

        # encoded_columns is an array containing a single element.
        # This element is an array like:
        # array(['cat1', 'cat2', 'cat3', 'cat4', 'cat5', 'cat6', 'cat7', 'cat8'], dtype=object)
        # Then, this array is the element of index 0 from the list encoded_columns.
        # It is represented as encoded_columns[0]

        # Therefore, we actually want the array which is named as encoded_columns[0]
        # Each element of this array is the name of one of the encoded columns. In the
        # example above, the element 'cat2' would be accessed as encoded_columns[0][1],
        # since it is the element of index [1] (second element) from the array 
        # encoded_columns[0].
        
        new_columns = encoded_columns[0]
        # To identify the column that originated these new columns, we can join the
        # string column to each element from new_columns:
        
        # Update the nested dictionary: store the new_columns as the key 'categories':
        nested_dict['categories'] = new_columns
        # Store the encoder object as the key 'OneHot_enc_obj'
        # Add the encoder object to the dictionary:
        nested_dict['OneHot_enc_obj'] = OneHot_enc_obj
        
        # Store the nested dictionary in the encoding_dict as the key 'OneHot_encoder':
        encoding_dict['OneHot_encoder'] = nested_dict
        # Append the encoding_dict as an element from list encoding_list:
        encoding_list.append(encoding_dict)

        """
            ENCODING_LIST = [

                {'column': column,
                'OneHot_encoder': {'OneHot_enc_obj': OneHot_enc_obj,
                                    'categories': new_columns}}
            ]
        """
        
        # Now we saved all encoding information, let's transform the data:
        
        # Start a support_list to store the concatenated strings:
        support_list = []
        
        for encoded_col in new_columns:
            # Use the str attribute to guarantee that the array stores only strings.
            # Add an underscore "_" to separate the strings and an identifier of the transform:
            new_column = column + "_" + str(encoded_col) + "_OneHotEnc"
            # Append it to the support_list:
            support_list.append(new_column)
            
        # Convert the support list to NumPy array, and make new_columns the support list itself:
        new_columns = np.array(support_list)
        
        # Crete a Pandas dataframe from the array transformed_columns:
        encoded_X_df = pd.DataFrame(transformed_columns)
        
        # Modify the name of the columns to make it equal to new_columns:
        encoded_X_df.columns = new_columns
        
        #Inner join the new dataset with the encoded dataset.
        # Use the index as the key, since indices are necessarily correspondent.
        # To use join on index, we apply pandas .concat method.
        # To join on a specific key, we could use pandas .merge method with the arguments
        # left_on = 'left_key', right_on = 'right_key'; or, if the keys have same name,
        # on = 'key':
        # Check Pandas merge and concat documentation:
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.merge.html
        
        new_df = pd.concat([new_df, encoded_X_df], axis = 1, join = "inner")
        # When axis = 0, the .concat operation occurs in the row level, so the rows
        # of the second dataframe are added to the bottom of the first one.
        # It is the SQL union, and creates a dataframe with more rows, and
        # total of columns equals to the total of columns of the first dataframe
        # plus the columns of the second one that were not in the first dataframe.
        # When axis = 1, the operation occurs in the column level: the two
        # dataframes are laterally merged using the index as the key, 
        # preserving all columns from both dataframes. Therefore, the number of
        # rows will be the total of rows of the dataframe with more entries,
        # and the total of columns will be the sum of the total of columns of
        # the first dataframe with the total of columns of the second dataframe.
        
        print(f"Successfully encoded column \'{column}\' and merged the encoded columns to the dataframe.\n")
        print("Check first 5 rows of the encoded table that was merged:\n")
        
        try:
            display(encoded_X_df.head())
        except: # regular mode
            print(encoded_X_df.head())
        
        # The default of the head method, when no parameter is printed, is to show 5 rows; if an
        # integer number Y is passed as argument .head(Y), Pandas shows the first Y-rows.
        print("\n")
        
    print("Finished One-Hot Encoding. Returning the new transformed dataframe; and an encoding list.\n")
    print("Each element from this list is a dictionary with the original column name as key \'column\', and a nested dictionary as the key \'OneHot_encoder\'.\n")
    print("In turns, the nested dictionary shows the different categories as key \'categories\' and the encoder object as the key \'OneHot_enc_obj\'.\n")
    print("Use the encoder object to inverse the One-Hot Encoding in the correspondent function.\n")
    print(f"For each category in the columns \'{subset_of_features_to_be_encoded}\', a new column has value 1, if it is the actual category of that row; or is 0 if not.\n")
    print("Check the first 10 rows of the new dataframe:\n")
    
    try:
        display(new_df.head(10))
    except:
        print(new_df.head(10))

    #return the transformed dataframe and the encoding dictionary:
    return new_df, encoding_list


def reverse_OneHotEncoding (df, encoding_list):
    """
    reverse_OneHotEncoding (df, encoding_list):

    https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html
    
    : param: df: the whole dataframe to be processed.
    
    : param: encoding_list: list in the same format of the one generated by OneHotEncode_df function:
      it must be a list of dictionaries where each dictionary contains two keys:
      key 'column': string with the original column name (in quotes). If it is None, a column named 
      'category_column_i', where i is the index of the dictionary in the encoding_list will be created; 
      key 'OneHot_encoder': this key must store a nested dictionary.
      Even though the nested dictionaries generates by the encoding function present
      two keys:  'categories', storing an array with the different categories;
      and 'OneHot_enc_obj', storing the encoder object, only the key 'OneHot_enc_obj' is required.
      On the other hand, a third key is needed in the nested dictionary:
      key 'encoded_columns': this key must store a list or array with the names of the columns
      obtained from Encoding.
    
        ENCODING_LIST = [

            {'column': column,
            'OneHot_encoder': {'OneHot_enc_obj': OneHot_enc_obj,
                            'categories': new_columns}}
        ]
    
      Alternatively
    
        ENCODING_LIST = [

            {'column': None,
            'OneHot_encoder': [{'category': None,
                              'encoded_column': column},]}
            ]
    
      Here, enconding_list will be a list of dictionaries, where each dictionary corresponds to one
      of the new columns to be encoded. The first key ('column') contains the name of the new column
      that will be created. If the value is None, a column named 'category_column_i', where i is the index of
      the dictionary in the encoding_list will be created.
      The second key, 'OneHot_encoder' will store a list of dictionaries. Each dictionary contains one of the
      columns obtained after the One-Hot Encoding, i.e., one of the binary columns that informs if the category
      is present or not. Each dictionary contains two keys: 'category' is the category that is encoded by such column.
      If the value is None, the category will be labeled as 'i' (string), where i is the index of the category in the
      'OneHot_encoder' list. The 'encoded_column' must contain a string indicating the name (label) of the encoded column
      in the original dataset. For instance, suppose column "label_horse" is a One-Hot Encoded column that stores value 1
      if the label is "horse", and value 0 otherwise.  In this case, 'category': 'horse, 'encoded_column': 'label_horse'.
    """

    from sklearn.preprocessing import OneHotEncoder

    # Start a copy of the original dataframe. This copy will be updated to create the new
    # transformed dataframe. Then, we avoid manipulating the original object.
    new_df = df.copy(deep = True)
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display  
    except:
        pass
    
    for encoder_dict in encoding_list:
        
        # Start a counter for the valid encoders
        i = 0
        try:
            # Check if the required arguments are present:
            if ((encoder_dict['OneHot_encoder']['OneHot_enc_obj'] is not None) & (encoder_dict['OneHot_encoder']['categories'] is not None)):
                
                if (encoder_dict['column'] is not None):
                    # Access the column name:
                    col_name = encoder_dict['column']

                else:
                    col_name = 'category_column' + str(i)
                
                try:
                    # Access the nested dictionary:
                    nested_dict = encoder_dict['OneHot_encoder']
                    # Access the encoder object on the dictionary
                    OneHot_enc_obj = nested_dict['OneHot_enc_obj']
                    # Access the list of encoded columns:
                    list_of_encoded_cols = list(encoder_dict['OneHot_encoder']['categories'])

                    # Remember that the categories may have been saved before including the alias + "_" + str(encoded_col) + "_OneHotEnc"
                    # Get a subset of the encoded columns
                    X = new_df.copy(deep = True)
                    try:
                        list_of_encoded_cols = [(col_name +  "_" + str(col) + "_OneHotEnc") for col in list_of_encoded_cols]
                        X = np.array(X[list_of_encoded_cols])
                    
                    except:
                        try:
                            X = np.array(X[list_of_encoded_cols])
                        except:
                            print("Save 'categories' with the correct name of the categories or use the same name as the columns from the function that One-Hot Encodes the dataframe.")
                            print("You may simply input the list that is output together with the One-Hot Encoded dataframe.\n")
                    
                    # Round every value to the closest integer before trying to inverse the transformation:
                    X = np.rint(X)
                        
                    # Replace values higher than max_encoded = 1 by max_encoded, and values lower than
                    # min_encoded = 0 by min_encoded, avoiding errors on the reverse operation.
                    # https://numpy.org/doc/stable/reference/generated/numpy.where.html
                    X = np.where(X > 1, 1, X)
                    # max_encoded is broadcast. If X > max_encoded, returns max_encoded = 1. 
                    # Else, returns X element itself.
                    X = np.where(X < 0, 0, X)
                    # Replaces each value lower than minimum encoded by minimum encooded itself.
                    # Avoids losing information.
                    # Reverse the encoding:
                    reversed_array = OneHot_enc_obj.inverse_transform(np.array(X))

                    # Add the reversed array as the column col_name on the dataframe:
                    new_df[col_name] = reversed_array
                    
                    print(f"Reversed the encoding for {col_name}. Check the 5 first rows of the re-transformed series:\n")
                    
                    try:
                        display(new_df[[col_name]].head())
                    except:
                        print(new_df[[col_name]].head())
                    
                    print("\n")
                    # Update the counter, since a valid encoder was accessed:
                    i = i + 1

                except:
                    print("Detected dictionary with incorrect keys or format. Unable to reverse encoding. Please, correct it.\n")
        
        except:
            
            try:

                if (len(encoder_dict['OneHot_encoder']) > 0):
                    # There is at least one dictionary stored.
                        
                    if (encoder_dict['column'] is not None):
                        # Access the column name:
                        col_name = encoder_dict['column']
                    else:
                        col_name = 'category_column' + str(i)

                    list_of_encoded_cols = []
                    list_of_categories = []
                    # Start a counter for the valid categories
                    j = 0

                    try:
                        for encoder in encoder_dict['OneHot_encoder']:
                            
                            if (encoder['encoded_column'] is not None):
                                list_of_encoded_cols.append(encoder['encoded_column'])

                                if (encoder['category'] is not None):
                                    list_of_categories.append(encoder['category'])
                                else:
                                    list_of_categories.append(str(j))
                                # Update the counter with a valid category:
                                j = j + 1
                        

                        if (len(list_of_encoded_cols) > 0):

                            X = new_df.copy(deep = True)
                            X = np.array(X[list_of_encoded_cols])
                            X = np.rint(X)
                            X = np.where(X > 1, 1, X)
                            X = np.where(X < 0, 0, X)

                            # Store the number of rows:
                            n_rows = X.shape[0]

                            # Create an array of zeros with same length as the dataset, i.e.,
                            # 1 element per row of the dataset. Use the same dtype as 
                            # The list of categories may be formed by only integers. In this case,
                            # convert it to integer type to save memory:
                            
                            try:
                                list_of_categories = np.float32(np.array(list_of_categories))
                                # The categories are numeric
                                reversed_array = np.zeros(n_rows)
                                # array of zeros with one element per row of the dataframe
                                reversed_array[:] = np.nan
                                # All elements were replaced by missing values
                            except:
                                # The categories are not numeric
                                reversed_array = np.zeros(n_rows, dtype = str)
                                # https://numpy.org/doc/stable/reference/generated/numpy.zeros.html
                                # The array is composed of empty strings
                            
                            # X is a matrix like:
                            # X = [[0, 0, 1], [1, 0, 0], [0, 1, 0]] with shape (n, m), where n is the  number
                            # of rows (internal arrays) and m is the number of columns (values per array),
                            # Suppose the 1st column (0) represents category 1. To access all rows for column zero,
                            # we do:
                            # col0 = X[:,0], obtaining an array like array([0, 1, 0]). Notice that it indicates that
                            # the category 1 is present in the row of index 1, i.e., the 2nd row. Analogously, column
                            # 2 (index 1) would be accessed as X[:,1].
                            # On the other hand, if X = [0, 0, 1], its shape is (n, ), so the second dimension is not
                            # available
                            
                            # Store the number of columns as n_cols
                            # Try accessing 2nd dimension:
                            try:
                                n_cols = X.shape[1]
                            except:
                                # single dimensional array:
                                n_cols = 1
                                X = X.reshape(-1, 1)
                                # Now, X is in the form of a matrix: X = [[0],[0],[1]] and we can slice it as X[:,k]
                            
                            for k in range(0, n_cols):
                                # Check where column k has value 1:
                                # Each encoded column corresponds to a category in the array list_of_categories
                                # So, give the reversed array the value stored as index k in list_of_categories.
                                # for the positions where the column k has value 1. X[:,k] == 1 would be a single
                                # dimension array like array([False,  True, False]), each element corresponding
                                # to one row.
                                # If the column is not 1 (i.e, it is zero), keep the original value, which is nan
                                # or empty string.
                                reversed_array = np.where((X[:,k] == 1), list_of_categories[k], reversed_array)
                        
                        # Add the reversed array as the column col_name on the dataframe:
                        new_df[col_name] = reversed_array
                        
                        print(f"Reversed the encoding for {col_name}. Check the 5 first rows of the re-transformed series:\n")
                        
                        try:
                            display(new_df[[col_name]].head())
                        except:
                            print(new_df[[col_name]].head())
                        
                        print("\n")
                            # Update the counter, since a valid encoder was accessed:
                        i = i + 1
                    
                    except:
                        print("Detected dictionary with incorrect keys or format. Unable to reverse encoding. Please, correct it.\n")
                
        
            except:
                print("Detected dictionary with incorrect keys or format. Unable to reverse encoding. Please, correct it.\n")
        

    print("Finished reversing One-Hot Encoding. Returning the new transformed dataframe.\n")
    print("Check the first 10 rows of the new dataframe:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(new_df.head(10))
            
    except: # regular mode
        print(new_df.head(10))

    #return the transformed dataframe:
    return new_df


def OrdinalEncoding_df (df, subset_of_features_to_be_encoded):
    """
    OrdinalEncoding_df (df, subset_of_features_to_be_encoded)

    Ordinal encoding: let's associate integer sequential numbers to the categorical column
      to apply the advanced encoding techniques. Even though the one-hot encoding could perform
      the same task and would, in fact, better, since there may be no ordering relation, the
      ordinal encoding is simpler and more suitable for this particular task.

    https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OrdinalEncoder.html#sklearn.preprocessing.OrdinalEncoder 
    
    : param: df: the whole dataframe to be processed.
    
    : param: subset_of_features_to_be_encoded: list of strings (inside quotes), 
      containing the names of the columns with the categorical variables that will be 
      encoded. If a single column will be encoded, declare this parameter as list with
      only one element e.g.subset_of_features_to_be_encoded = ["column1"] 
      will analyze the column named as 'column1'; 
      subset_of_features_to_be_encoded = ["col1", 'col2', 'col3'] will analyze 3 columns
      with categorical variables: 'col1', 'col2', and 'col3'.
    """

    from sklearn.preprocessing import OrdinalEncoder
    
    #Start an encoding list empty (it will be a JSON object):
    encoding_list = []
    
    # Start a copy of the original dataframe. This copy will be updated to create the new
    # transformed dataframe. Then, we avoid manipulating the original object.
    new_df = df.copy(deep = True)
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display  
    except:
        pass

    #loop through each column of the subset:
    for column in subset_of_features_to_be_encoded:
        
        # Start two empty dictionaries:
        encoding_dict = {}
        nested_dict = {}
        
        # Add the column to encoding_dict as the key 'column':
        encoding_dict['original_column_label'] = column
        
        # Loop through each element (named 'original_column_label') of the list of columns to analyze,
        # subset_of_features_to_be_encoded
        
        # We could process the whole subset at once, but it could make us lose information
        # about the generated columns
        
        # set a subset of the dataframe X containing 'column' as the only column:
        # it will be equivalent to using .reshape(-1,1) to set a 1D-series
        # or array in the shape for scikit-learn:
        # For doing so, pass a list of columns for column filtering, containing
        # the object column as its single element:
        X  = new_df[[column]]
        
        #Start the OrdinalEncoder object:
        ordinal_enc_obj = OrdinalEncoder()
        
        # Fit the ordinal encoder to the dataframe X:
        ordinal_enc_obj = ordinal_enc_obj.fit(X)
        # Get the transformed dataframe X: 
        transformed_X = ordinal_enc_obj.transform(X)
        # transformed_X is an array of arrays like: [[0.], [0.], ..., [8.]]
        # We want all the values in the first position of the internal arrays:
        transformed_X = transformed_X[:,0]
        # Get the encoded series as a NumPy array:
        encoded_series = np.array(transformed_X)
        
        # Get a name for the new encoded column:
        new_column = column + "_OrdinalEnc"
        # Add this column to the dataframe:
        new_df[new_column] = encoded_series
        
        # Now, let's retrieve the encoding information and save it:
        # Show encoded categories and store this array. 
        # It will give the proper columns' names:
        encoded_categories = ordinal_enc_obj.categories_
        
        """
            The categories_ attribute stores a list containing an array:
            [array(['apple', 'banana', 'blackgram', 'chickpea', 'coconut', 'coffee'], dtype=object)],
            To access such array, we must access the element with index 0 from this array.
            Then, we may convert it to list
        """
        encoded_categories = list(encoded_categories[0])

        # encoded_categories is an array of strings containing the information of
        # encoded categories and their values.
        
        # Update the nested dictionary: store the categories as the key 'categories':
        nested_dict['categories'] = encoded_categories
        # Store the encoder object as the key 'ordinal_enc_obj'
        # Add the encoder object to the dictionary:
        nested_dict['ordinal_enc_obj'] = ordinal_enc_obj
        nested_dict['encoded_column'] = new_column
        
        # Store the nested dictionary in the encoding_dict as the key 'ordinal_encoder':
        encoding_dict['ordinal_encoder'] = nested_dict
        # Append the encoding_dict as an element from list encoding_list:
        encoding_list.append(encoding_dict)
        
        print(f"Successfully encoded column \'{column}\' and added the encoded column to the dataframe.\n")
        print("Check first 5 rows of the encoded series that was merged:\n")
        
        try:
            display(new_df[[new_column]].head())
        except:
            print(new_df[[new_column]].head())
        
        # The default of the head method, when no parameter is printed, is to show 5 rows; if an
        # integer number Y is passed as argument .head(Y), Pandas shows the first Y-rows.
        print("\n")
        
    print("Finished Ordinal Encoding. Returning the new transformed dataframe; and an encoding list.\n")
    print("Each element from this list is a dictionary with the original column name as key \'column\', and a nested dictionary as the key \'ordinal_encoder\'.\n")
    print("In turns, the nested dictionary shows the different categories as key \'categories\' and the encoder object as the key \'ordinal_enc_obj\'.\n")
    print("Use the encoder object to inverse the Ordinal Encoding in the correspondent function.\n")
    print("Check the first 10 rows of the new dataframe:\n")
    
    try:
        display(new_df.head(10))
    except:
        print(new_df.head(10))
    
    #return the transformed dataframe and the encoding dictionary:
    return new_df, encoding_list


def reverse_OrdinalEncoding (df, encoding_list):
    """
    reverse_OrdinalEncoding (df, encoding_list)

    https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OrdinalEncoder.html#sklearn.preprocessing.OrdinalEncoder
    
    : param: df: the whole dataframe to be processed.
    
    : param: ENCODING_LIST: list in the same format of the one generated by OrdinalEncode_df function:
      it must be a list of dictionaries where each dictionary contains two keys:
      key 'original_column_label': string with the original column name (in quotes); 
      key 'ordinal_encoder': this key must store a nested dictionary.
      Even though the nested dictionaries generates by the encoding function present
      two keys:  'categories', storing an array with the different categories;
      and 'ordinal_enc_obj', storing the encoder object, only one of them is required,
      prefentially the 'categories' one.
      Exammple of array or list: 'categories': ['white', 'black', 'blue']
    
      On the other hand, a third key is needed in the nested dictionary:
      key 'encoded_column': this key must store a string with the name of the column
      obtained from Encoding.
      If 'encoded_column' is None, the name of the original column will be used.
      On the other hand, when 'original_column_label' is None, the 'encoded_column'
      will be used for both. So, at least one of them must be present for the
      element not to be ignored.
    
        ENCODING_LIST = [
                        {'original_column_label': None,
                        'ordinal_encoder': {'ordinal_enc_obj': None, 'encoded_column': None, 
                                            'categories': None}},
                        {'original_column_label': None,
                        'ordinal_encoder': {'ordinal_enc_obj': None, 'encoded_column': None}},]
    
      Alternatively, the list may have the following format:
    
        ENCODING_LIST = 
            [
                    {'original_column_label': None,
                    'encoding': [{'actual_label': None, 'encoded_value': None},]},
                    {'original_column_label': None,
                    'encoding': [{'actual_label': None, 'encoded_value': None},]},
            ]
    
      The difference is that the key 'ordinal_encoder' is replaced by the key
      'encoding', which stores a list of dictionaries with encoding information.
      You must input a dictionary by possible encoded value (as a list element). 
      Each dictionary will contain a key 'actual_label' with the real value of the 
      label, and 'encoded_val'with the correspondent encoding. For example, 
      if the category 'yellow' was encoded as value 3, then the dictionary would be: 
      {'actual_label': 'yellow', 'encoded_value': 3}
    """

    from sklearn.preprocessing import OrdinalEncoder
    
    # Start a copy of the original dataframe. This copy will be updated to create the new
    # transformed dataframe. Then, we avoid manipulating the original object.
    new_df = df.copy(deep = True)
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display  
    except:
        pass

    for encoder_dict in encoding_list:
        
        try:
            # Check if the required arguments are present:
            if ((encoder_dict['original_column_label'] is not None) | (encoder_dict['ordinal_encoder']['encoded_column'] is not None)):

                if encoder_dict['original_column_label'] is None:
                    encoder_dict['original_column_label'] = encoder_dict['ordinal_encoder']['encoded_column']
                
                if ((encoder_dict['ordinal_encoder'] is not None)):
                    
                    # Access the column name:
                    col_name = encoder_dict['original_column_label']

                    # Access the nested dictionary:
                    nested_dict = encoder_dict['ordinal_encoder']

                    if ((encoder_dict['ordinal_encoder']['categories'] is not None)):

                        categories = nested_dict['categories']
                    
                    elif ((encoder_dict['ordinal_encoder']['ordinal_enc_obj'] is not None)):
                        # Access the encoder object on the dictionary
                        ordinal_enc_obj = nested_dict['ordinal_enc_obj']
                        # Get minimum and maximum encoded values:
                        categories = ordinal_enc_obj.categories_

                        """
                            The categories_ attribute stores a list containing an array:
                            [array(['apple', 'banana', 'blackgram', 'chickpea', 'coconut', 'coffee'], dtype=object)],
                            To access such array, we must access the element with index 0 from this list
                        """
                        categories = categories[0]

                    # Access the encoded column and save it as a list:
                    encoded_col = nested_dict['encoded_column']
                    # If it is None, repeat the original colum name
                    
                    if encoded_col is None:
                        encoded_col = encoder_dict['original_column_label']

                    # Get a subset of the encoded column
                    X = new_df.copy(deep = True)
                    X = X[encoded_col]
                    X = np.array(X).reshape(-1,1) 
                    # Put the array in the form of a matrix containing one element (column) per row: [[val1], [val2], ...]
                
                    # Round every value to the closest integer before trying to inverse the transformation:
                    X = np.rint(X)

                    min_encoded = 0 # always from zero
                    max_encoded = len(categories) - 1 # counting starts from zero
                    # Replace values higher than max_encoded by max_encoded, and values lower than
                    # min_encoded by min_encoded, avoiding errors on the reverse operation.
                    # https://numpy.org/doc/stable/reference/generated/numpy.where.html
                    X = np.where(X > max_encoded, max_encoded, X)
                    # max_encoded is broadcast. If X > max_encoded, returns max_encoded. 
                    # Else, returns X element itself.
                    X = np.where(X < min_encoded, min_encoded, X)
                    # Replaces each value lower than minimum encoded by minimum encooded itself.
                    # Avoids losing information.
                    
                    try:
                        # Create an array of NAs with same dimensions as X:
                        reversed_array  =  np.where(X, np.nan, np.nan)
                        for code, category in enumerate(categories):
                            # code is the integer from categories, and category is the value:
                            # enumerate generates elements like (0, categories[0])
                            reversed_array =  np.where(X == code, category, reversed_array)
                        
                    except:
                        try:    
                            # Reverse the encoding with the encoding object:
                            reversed_array = ordinal_enc_obj.inverse_transform(X)
                        except:
                            # Make a column of missing values:
                            reversed_array = np.nan
                
                else:
                    # Try accessing the individual encoding information with format 
                    # {'column': None,
                    # 'ordinal_encoder': {'encoded_column': None, 'encoding': [{'actual_label': None, 'encoded_value': None},]}
                    # Access the column name:
                    col_name = encoder_dict['original_column_label']
                    # Access the nested dictionary:
                    nested_dict = encoder_dict['ordinal_encoder']
                    # Access the encoding list on the dictionary
                    encoding_list = nested_dict['encoding']
                    # Access the encoded column and save it as a list:
                    
                    # Pick all possible encodings
                    list_of_vals = [dictionary['encoded_value'] for dictionary in encoding_list]
                    min_encoded = min(list_of_vals)
                    max_encoded = max(list_of_vals)

                    encoded_col = nested_dict['encoded_column']
                    # If it is None, repeat the original colum name
                    
                    if encoded_col is None:
                        encoded_col = encoder_dict['original_column_label']

                    # Get a subset of the encoded column
                    X = new_df.copy(deep = True)
                    X = X[encoded_col]
                    X = np.array(X).reshape(-1,1) 
                    # Put the array in the form of a matrix containing one element (column) per row: [[val1], [val2], ...]

                    try:
                        # Round every value to the closest integer before trying to inverse the transformation:
                        X = np.rint(X)
                        X = np.where(X > max_encoded, max_encoded, X)
                        X = np.where(X < min_encoded, min_encoded, X)
                        
                        # Reverse the encoding:
                        # Pick first element from list. If X is the first encoding, replace it by the corresponding label.
                        reversed_array = np.where(X == list_of_vals[0]['encoded_value'], list_of_vals[0]['actual_label'], X)
                        # Now, loop through all possible encodings:
                        for i in range(1, len(reversed_array)):
                            # Starts from 1, since element 0 was already picked
                            reversed_array = np.where(X == list_of_vals[i]['encoded_value'], list_of_vals[i]['actual_label'], reversed_array)
                    
                    except:
                        # Make a column of missing values:
                        reversed_array = np.nan
                
                # Add the reversed array as the column col_name on the dataframe:
                new_df[col_name] = reversed_array
                        
                print(f"Reversed the encoding for {col_name}. Check the 5 first rows of the re-transformed series:\n")
                    
                try:
                    display(new_df[[col_name]].head())
                except:
                    print(new_df[[col_name]].head())

                print("\n")
        
        except:
            print("Detected dictionary with incorrect keys or format. Unable to reverse encoding. Please, correct it.\n")
    
    
    print("Finished reversing Ordinal Encoding. Returning the new transformed dataframe.\n")
    print("Check the first 10 rows of the new dataframe:\n")
    
    try:
        display(new_df.head(10))
    except:
        print(new_df.head(10))

    #return the transformed dataframe:
    return new_df


def feature_scaling (df, subset_of_features_to_scale, mode = 'min_max', scale_with_new_params = True, list_of_scaling_params = None, suffix = '_scaled'):
    """
    feature_scaling (df, subset_of_features_to_scale, mode = 'min_max', scale_with_new_params = True, list_of_scaling_params = None, suffix = '_scaled'):
    
    Scikit-learn Preprocessing data guide:
      https://scikit-learn.org/stable/modules/preprocessing.html#preprocessing-scaler
    Standard scaler documentation:
      https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html
    Min-Max scaler documentation:
      https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html#sklearn.preprocessing.MinMaxScaler.set_params
    
    ## Machine Learning algorithms are extremely sensitive to scale. 
    
    This function provides 4 methods (modes) of scaling:
    : param: mode = 'standard': applies the standard scaling, 
       which creates a new variable with mean = 0; and standard deviation = 1.
       Each value Y is transformed as Ytransf = (Y - u)/s, where u is the mean 
       of the training samples, and s is the standard deviation of the training samples.
    
      mode = 'min_max': applies min-max normalization, with a resultant feature 
      ranging from 0 to 1. each value Y is transformed as 
      Ytransf = (Y - Ymin)/(Ymax - Ymin), where Ymin and Ymax are the minimum and 
      maximum values of Y, respectively.
    
      mode = 'factor': divides the whole series by a numeric value provided as argument. 
      For a factor F, the new Y values will be Ytransf = Y/F.
    
      mode = 'normalize_by_maximum' is similar to mode = 'factor', but the factor will be selected
      as the maximum value. This mode is available only for scale_with_new_params = True. If
      scale_with_new_params = False, you should provide the value of the maximum as a division 'factor'.
    
    : param: df: the whole dataframe to be processed.
    
    : param: subset_of_features_to_be_scaled: list of strings (inside quotes), 
      containing the names of the columns with the categorical variables that will be 
      encoded. If a single column will be encoded, declare this parameter as list with
      only one element e.g.subset_of_features_to_be_scaled = ["column1"] 
      will analyze the column named as 'column1'; 
      subset_of_features_to_be_scaled = ["col1", 'col2', 'col3'] will analyze 3 columns
      with categorical variables: 'col1', 'col2', and 'col3'.
    
    : param: scale_with_new_params = True
      Alternatively, set scale_with_new_params = True if you want to calculate a new
      scaler for the data; or set scale_with_new_params = False if you want to apply 
      parameters previously obtained to the data (i.e., if you want to apply the scaler
      previously trained to another set of data; or wants to simply apply again the same
      scaler).
    
    : param: list_of_scaling_params:
      This variable has effect only when SCALE_WITH_NEW_PARAMS = False
      WARNING: The mode 'factor' demmands the input of the list of factors that will be 
      used for normalizing each column. Therefore, it can be used only 
      when scale_with_new_params = False.
    
      list_of_scaling_params is a list of dictionaries with the same format of the list returned
      from this function. Each dictionary must correspond to one of the features that will be scaled,
      but the list do not have to be in the same order of the columns - it will check one of the
      dictionary keys.
      The first key of the dictionary must be 'column'. This key must store a string with the exact
      name of the column that will be scaled.
      the second key must be 'scaler'. This key must store a dictionary. The dictionary must store
      one of two keys: 'scaler_obj' - sklearn scaler object to be used; or 'scaler_details' - the
      numeric parameters for re-calculating the scaler without the object. The key 'scaler_details', 
      must contain a nested dictionary. For the mode 'min_max', this dictionary should contain 
      two keys: 'min', with the minimum value of the variable, and 'max', with the maximum value. 
      For mode 'standard', the keys should be 'mu', with the mean value, and 'sigma', with its 
      standard deviation. For the mode 'factor', the key should be 'factor', and should contain the 
      factor for division (the scaling value. e.g 'factor': 2.0 will divide the column by 2.0.).
      Again, if you want to normalize by the maximum, declare the maximum value as any other factor for
      division.
      The key 'scaler_details' will not create an object: the transform will be directly performed 
      through vectorial operations.
    
    : param: suffix: string (inside quotes).
      How the transformed column will be identified in the returned data_transformed_df.
      If y_label = 'Y' and suffix = '_scaled', the transformed column will be
      identified as '_scaled'.
      Alternatively, input inside quotes a string with the desired suffix. Recommendation:
      start the suffix with "_" to separate it from the original name
    """

    from sklearn.preprocessing import StandardScaler
    from sklearn.preprocessing import MinMaxScaler
    
    if (suffix is None):
        #set as the default
        suffix = '_scaled'
    
    #Start a copy of the original dataframe. This copy will be updated to create the new
    # transformed dataframe. Then, we avoid manipulating the original object.
    new_df = df.copy(deep = True)
    
    #Start an scaling list empty (it will be a JSON object):
    scaling_list = []
    
    for column in subset_of_features_to_scale:
        
        # Create a dataframe X by subsetting only the analyzed column
        # it will be equivalent to using .reshape(-1,1) to set a 1D-series
        # or array in the shape for scikit-learn:
        # For doing so, pass a list of columns for column filtering, containing
        # the object column as its single element:
        X = new_df[[column]]
        
        if (scale_with_new_params == False):
            
            # Use a previously obtained scaler.
            # Loop through each element of the list:
            
            for scaling_dict in list_of_scaling_params:
                
                # check if the dictionary is from that column:
                if (scaling_dict['column'] == column):
                    
                    # We found the correct dictionary. Let's retrieve the information:
                    # retrieve the nested dictionary:
                    nested_dict = scaling_dict['scaler']
                    
                    # try accessing the scaler object:
                    try:
                        scaler = nested_dict['scaler_obj']
                        #calculate the scaled feature, and store it as new array:
                        scaled_feature = scaler.transform(X)
                        
                        # Add the parameters to the nested dictionary:
                        nested_dict['scaling_params'] = scaler.get_params(deep = True)
                        
                        if (mode == 'standard'):
                            
                            nested_dict['scaler_details'] = {
                                'mu': X[column].mean(),
                                'sigma': X[column].std()
                            }
                        
                        elif (mode == 'min_max'):
                            
                            nested_dict['scaler_details'] = {
                                'min': X[column].min(),
                                'max': X[column].max()
                            }
                    
                    except:
                        
                        try:
                            # As last alternative, let's try accessing the scaler details dict
                            scaler_details = nested_dict['scaler_details']
                                
                            if (mode == 'standard'):
                                
                                nested_dict['scaling_params'] = 'standard_scaler_manually_defined'
                                mu = scaler_details['mu']
                                sigma = scaler_details['sigma']
                                    
                                if (sigma != 0):
                                    scaled_feature = (X - mu)/sigma
                                else:
                                    scaled_feature = (X - mu)
                                
                            elif (mode == 'min_max'):
                                    
                                nested_dict['scaling_params'] = 'min_max_scaler_manually_defined'
                                minimum = scaler_details['min']
                                maximum = scaler_details['max']
                                    
                                if ((maximum - minimum) != 0):
                                    scaled_feature = (X - minimum)/(maximum - minimum)
                                else:
                                    scaled_feature = X/maximum
                                
                            elif (mode == 'factor'):
                                
                                nested_dict['scaling_params'] = 'normalization_by_factor'
                                factor = scaler_details['factor']
                                scaled_feature = X/(factor)
                                
                            else:
                                raise InvalidInputsError ("Select a valid mode: standard, min_max, or factor.\n")
                            
                        except:
                                
                            raise InvalidInputsError (f"No valid scaling dictionary was input for column {column}.\n")
            
        elif (mode == 'normalize_by_maximum'):
            
            #Start an scaling dictionary empty:
            scaling_dict = {}

            # add the column to the scaling dictionary:
            scaling_dict['column'] = column

            # Start a nested dictionary:
            nested_dict = {}
            
            factor = X[column].max()
            scaled_feature = X/(factor)
            nested_dict['scaling_params'] = 'normalization_by_factor'
            nested_dict['scaler_details'] = {'factor': factor, 'description': 'division_by_maximum_detected_value'}
    
        else:
            # Create a new scaler:
            
            #Start an scaling dictionary empty:
            scaling_dict = {}

            # add the column to the scaling dictionary:
            scaling_dict['column'] = column
            
            # Start a nested dictionary:
            nested_dict = {}
                
            #start the scaler object:
            if (mode == 'standard'):
                
                scaler = StandardScaler()
                scaler_details = {'mu': X[column].mean(), 'sigma': X[column].std()}

            elif (mode == 'min_max'):
                
                scaler = MinMaxScaler()
                scaler_details = {'min': X[column].min(), 'max': X[column].max()}
                
            # fit the scaler to the column
            scaler = scaler.fit(X)
                    
            # calculate the scaled feature, and store it as new array:
            scaled_feature = scaler.transform(X)
            # scaler.inverse_transform(X) would reverse the scaling.
                
            # Get the scaling parameters for that column:
            scaling_params = scaler.get_params(deep = True)
                    
            # scaling_params is a dictionary containing the scaling parameters.
            # Add the scaling parameters to the nested dictionary:
            nested_dict['scaling_params'] = scaling_params
                
            # add the scaler object to the nested dictionary:
            nested_dict['scaler_obj'] = scaler
            
            # Add the scaler_details dictionary:
            nested_dict['scaler_details'] = scaler_details
            
            # Now, all steps are the same for all cases, so we can go back to the main
            # for loop:
    
        # Create the new_column name:
        new_column = column + suffix
        # Create the new_column by dividing the previous column by the scaling factor:
                    
        # Set the new column as scaled_feature
        new_df[new_column] = scaled_feature
                
        # Add the nested dictionary to the scaling_dict:
        scaling_dict['scaler'] = nested_dict
                
        # Finally, append the scaling_dict to the list scaling_list:
        scaling_list.append(scaling_dict)
                    
        print(f"Successfully scaled column {column}.\n")
                
    print("Successfully scaled the dataframe. Returning the transformed dataframe and the scaling dictionary.\n")
    print("Check 10 first rows of the new dataframe:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(new_df.head(10))
            
    except: # regular mode
        print(new_df.head(10))

    return new_df, scaling_list


def reverse_feature_scaling (df, subset_of_features_to_scale, list_of_scaling_params, mode = 'min_max', suffix = '_reverseScaling'):
    """
    reverse_feature_scaling (df, subset_of_features_to_scale, list_of_scaling_params, mode = 'min_max', suffix = '_reverseScaling'):

    Scikit-learn Preprocessing data guide:
      https://scikit-learn.org/stable/modules/preprocessing.html#preprocessing-scaler
    Standard scaler documentation:
      https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html
    Min-Max scaler documentation:
      https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html#sklearn.preprocessing.MinMaxScaler.set_params
    
    : param: mode = 'standard': reverses the standard scaling, 
       which creates a new variable with mean = 0; and standard deviation = 1.
       Each value Y is transformed as Ytransf = (Y - u)/s, where u is the mean 
       of the training samples, and s is the standard deviation of the training samples.
    
      mode = 'min_max': reverses min-max normalization, with a resultant feature 
      ranging from 0 to 1. each value Y is transformed as 
      Ytransf = (Y - Ymin)/(Ymax - Ymin), where Ymin and Ymax are the minimum and 
      maximum values of Y, respectively.
      mode = 'factor': reverses the division of the whole series by a numeric value 
      provided as argument. 
      For a factor F, the new Y transformed values are Ytransf = Y/F.
      Notice that if the original mode was 'normalize_by_maximum', then the maximum value used
      must be declared as any other factor.
    
    : param: df: the whole dataframe to be processed.
    
    : param: subset_of_features_to_be_scaled: list of strings (inside quotes), 
      containing the names of the columns with the categorical variables that will be 
      encoded. If a single column will be encoded, declare this parameter as list with
      only one element e.g.subset_of_features_to_be_scaled = ["column1"] 
      will analyze the column named as 'column1'; 
      subset_of_features_to_be_scaled = ["col1", 'col2', 'col3'] will analyze 3 columns
      with categorical variables: 'col1', 'col2', and 'col3'.
    
    : param: list_of_scaling_params is a list of dictionaries with the same format of the list returned
      from this function. Each dictionary must correspond to one of the features that will be scaled,
      but the list do not have to be in the same order of the columns - it will check one of the
      dictionary keys.
      The first key of the dictionary must be 'column'. This key must store a string with the exact
      name of the column that will be scaled.
      the second key must be 'scaler'. This key must store a dictionary. The dictionary must store
      one of two keys: 'scaler_obj' - sklearn scaler object to be used; or 'scaler_details' - the
      numeric parameters for re-calculating the scaler without the object. The key 'scaler_details', 
      must contain a nested dictionary. For the mode 'min_max', this dictionary should contain 
      two keys: 'min', with the minimum value of the variable, and 'max', with the maximum value. 
      For mode 'standard', the keys should be 'mu', with the mean value, and 'sigma', with its 
      standard deviation. For the mode 'factor', the key should be 'factor', and should contain the 
      factor for division (the scaling value. e.g 'factor': 2.0 will divide the column by 2.0.).
      Again, if you want to normalize by the maximum, declare the maximum value as any other factor for
      division.
      The key 'scaler_details' will not create an object: the transform will be directly performed 
      through vectorial operations.
    
    : param: suffix: string (inside quotes).
      How the transformed column will be identified in the returned data_transformed_df.
      If y_label = 'Y' and suffix = '_reverseScaling', the transformed column will be
      identified as '_reverseScaling'.
      Alternatively, input inside quotes a string with the desired suffix. Recommendation:
      start the suffix with "_" to separate it from the original name
    """

    from sklearn.preprocessing import StandardScaler
    from sklearn.preprocessing import MinMaxScaler
    
    if (suffix is None):
        #set as the default
        suffix = '_reverseScaling'
    
    #Start a copy of the original dataframe. This copy will be updated to create the new
    # transformed dataframe. Then, we avoid manipulating the original object.
    new_df = df.copy(deep = True)
    
    #Start an scaling list empty (it will be a JSON object):
    scaling_list = []
    
    # Use a previously obtained scaler:
    
    for column in subset_of_features_to_scale:
        
        # Create a dataframe X by subsetting only the analyzed column
        # it will be equivalent to using .reshape(-1,1) to set a 1D-series
        # or array in the shape for scikit-learn:
        # For doing so, pass a list of columns for column filtering, containing
        # the object column as its single element:
        X = new_df[[column]]

        # Loop through each element of the list:
            
        for scaling_dict in list_of_scaling_params:
                
            # check if the dictionary is from that column:
            if (scaling_dict['column'] == column):
                    
                # We found the correct dictionary. Let's retrieve the information:
                # retrieve the nested dictionary:
                nested_dict = scaling_dict['scaler']
                    
                # try accessing the scaler object:
                try:
                    scaler = nested_dict['scaler_obj']
                    #calculate the reversed scaled feature, and store it as new array:
                    rev_scaled_feature = scaler.inverse_transform(X)
                        
                    # Add the parameters to the nested dictionary:
                    nested_dict['scaling_params'] = scaler.get_params(deep = True)
                        
                    if (mode == 'standard'):
                            
                        nested_dict['scaler_details'] = {
                                'mu': rev_scaled_feature.mean(),
                                'sigma': rev_scaled_feature.std()
                            }
                        
                    elif (mode == 'min_max'):
                            
                        nested_dict['scaler_details'] = {
                                'min': rev_scaled_feature.min(),
                                'max': rev_scaled_feature.max()
                            }
                    
                except:
                        
                    try:
                        # As last alternative, let's try accessing the scaler details dict
                        scaler_details = nested_dict['scaler_details']
                                
                        if (mode == 'standard'):
                                
                            nested_dict['scaling_params'] = 'standard_scaler_manually_defined'
                            mu = scaler_details['mu']
                            sigma = scaler_details['sigma']
                                    
                            if (sigma != 0):
                                # scaled_feature = (X - mu)/sigma
                                rev_scaled_feature = (X * sigma) + mu
                            else:
                                # scaled_feature = (X - mu)
                                rev_scaled_feature = (X + mu)
                                
                        elif (mode == 'min_max'):
                                    
                            nested_dict['scaling_params'] = 'min_max_scaler_manually_defined'
                            minimum = scaler_details['min']
                            maximum = scaler_details['max']
                                    
                            if ((maximum - minimum) != 0):
                                # scaled_feature = (X - minimum)/(maximum - minimum)
                                rev_scaled_feature = (X * (maximum - minimum)) + minimum
                            else:
                                # scaled_feature = X/maximum
                                rev_scaled_feature = (X * maximum)
                                
                        elif (mode == 'factor'):
                                
                            nested_dict['scaling_params'] = 'normalization_by_factor'
                            factor = scaler_details['factor']
                            # scaled_feature = X/(factor)
                            rev_scaled_feature = (X * factor)
                                
                        else:
                            raise InvalidInputsError ("Select a valid mode: standard, min_max, or factor.\n")
                            
                    except:
                                
                        raise InvalidInputsError (f"No valid scaling dictionary was input for column {column}.\n")
        
                # Create the new_column name:
                new_column = column + suffix
                # Create the new_column by dividing the previous column by the scaling factor:

                # Set the new column as rev_scaled_feature
                new_df[new_column] = rev_scaled_feature

                # Add the nested dictionary to the scaling_dict:
                scaling_dict['scaler'] = nested_dict

                # Finally, append the scaling_dict to the list scaling_list:
                scaling_list.append(scaling_dict)

                print(f"Successfully re-scaled column {column}.\n")
                
    print("Successfully re-scaled the dataframe.\n")
    print("Check 10 first rows of the new dataframe:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(new_df.head(10))
            
    except: # regular mode
        print(new_df.head(10))
                
    return new_df, scaling_list
