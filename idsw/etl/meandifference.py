import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from idsw.datafetch.core import InvalidInputsError


def column_general_statistics (df, column_to_analyze):
    """
    column_general_statistics (df, column_to_analyze)

    : param: df: dataframe to be analyzed.
    
    : param: column_to_analyze: name of the new column. e.g. column_to_analyze = 'col1'
      will analyze column named as 'col1'
    """

    analyzed_series = df[column_to_analyze].copy()
    #Drop missing values. Dropping them with describe method is deprecated and may raise errors.
    analyzed_series = analyzed_series.dropna()
    
    general_stats = analyzed_series.describe()
    print(f"General descriptive statistics from variable {column_to_analyze}, ignoring missing values:\n") 
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(general_stats)
            
    except: # regular mode
        print(general_stats)
    
    interpretation_df = pd.DataFrame(
    
        data = {
            'statistic': ["count", "mean", "std", "min", "25% = 0.25",
                        "50% = 0.50", "75% = 0.75", "max"],
            'interpretation': ["total of values evaluated (number of entries)",
                            "mean value of the series", "standard deviation of the series",
                            "minimum value observed",
                            "1st-quartile: 25% of data <= this value",
                            "2nd-quartile: 50% of data <= this value", 
                            "3rd-quartile: 75% of data <= this value",
                            "maximum value observed"
                            ]}
    )
    interpretation_df.set_index('statistic', inplace = True)
    
    print("\n") #line break
    print("Interpretation (missing values ignored):")
    
    try:
        display(interpretation_df)        
    except:
        print(interpretation_df)
    
    print("\n")
    print("ATTENTION: This function shows the general statistics only for numerical variables.")
    print("The results were returned as the dataframe general_stats.\n")
    
    # Return only the dataframe
    return general_stats


def get_quantiles_for_column (df, column_to_analyze):
    """
    get_quantiles_for_column (df, column_to_analyze)

    : param: df: dataframe to be analyzed.
    
    : param: column_to_analyze: name of the new column. e.g. column_to_analyze = 'col1'
      will analyze column named as 'col1'
    """

    analyzed_series = df[column_to_analyze].copy()
    #Drop missing values. Dropping them with describe method is deprecated and may raise errors.
    analyzed_series = analyzed_series.dropna()
    
    list_of_quantiles = []
    list_of_pcts = []
    list_of_values = []
    list_of_interpretation = []
    
    #First element: minimum
    list_of_quantiles.append(0.0)
    list_of_pcts.append(0)
    list_of_values.append(analyzed_series.min())
    list_of_interpretation.append(f"minimum {column_to_analyze}")
    
    i = 5
    #Start from the 5% quantile
    while (i < 100):
        
        list_of_quantiles.append(i/100)
        list_of_pcts.append(i)
        list_of_values.append(analyzed_series.quantile(i/100))
        list_of_interpretation.append(f"{i}% of data <= this value")
        
        i = i + 5
    
    # Last element: maximum value
    list_of_quantiles.append(1.0)
    list_of_pcts.append(100)
    list_of_values.append(analyzed_series.max())
    list_of_interpretation.append(f"maximum {column_to_analyze}")
    
    # Summarize the lists as a dataframe:
    
    quantiles_summ_df = pd.DataFrame(data = {"quantile": list_of_quantiles, 
                                            "%": list_of_pcts,
                                            column_to_analyze: list_of_values,
                                            "interpretation": list_of_interpretation})
    quantiles_summ_df.set_index(['quantile', "%", column_to_analyze], inplace = True)
    
    print("Quantiles returned as dataframe quantiles_summ_df. Check it below:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(quantiles_summ_df)
            
    except: # regular mode
        print(quantiles_summ_df)
    
    return quantiles_summ_df


def get_p_percent_quantile_lim_for_column (df, column_to_analyze, p_percent = 100):
    """
    get_p_percent_quantile_lim_for_column (df, column_to_analyze, p_percent = 100)

    : param: df: dataframe to be analyzed.
    
    : param: column_to_analyze: name of the new column. e.g. column_to_analyze = 'col1'
      will analyze column named as 'col1'
    
    : param: p_percent: float value from 0 to 100 representing the percent of the quantile
      if p_percent = 31.2, then 31.2% of the data will fall below the returned value
      if p_percent = 75, then 75% of the data will fall below the returned value
      if p_percent = 0, the minimum value is returned.
      if p_percent = 100, the maximum value is returned.
    """

    analyzed_series = df[column_to_analyze].copy()
    #Drop missing values. Dropping them with describe method is deprecated and may raise errors.
    analyzed_series = analyzed_series.dropna()
    
    #convert the quantile to fraction
    quantile_fraction = p_percent/100.0 #.0 to guarantee a float result
    
    if (quantile_fraction < 0):
        raise InvalidInputsError ("Invalid percent value - it cannot be lower than zero.")
    
    elif (quantile_fraction == 0):
        #get the minimum value
        quantile_lim = analyzed_series.min()
        print(f"Minimum value of {column_to_analyze} =")
        print("%.4f" %(quantile_lim))
    
    elif (quantile_fraction == 1):
        #get the maximum value
        quantile_lim = analyzed_series.max()
        print(f"Maximum value of {column_to_analyze} =")
        print("%.4f" %(quantile_lim))
        
    else:
        #get the quantile
        quantile_lim = analyzed_series.quantile(quantile_fraction)
        print(f"{quantile_fraction}-quantile: {p_percent}% of data <=")
        print("%.4f" %(quantile_lim))
    
    return quantile_lim


def label_dataframe_subsets (df, list_of_labels = [{'filter': None, 'value_to_apply': None, 'new_column_name': None}, {'filter': None, 'value_to_apply': None, 'new_column_name': None}, {'filter': None, 'value_to_apply': None, 'new_column_name': None}, {'filter': None, 'value_to_apply': None, 'new_column_name': None}, {'filter': None, 'value_to_apply': None, 'new_column_name': None}, {'filter': None, 'value_to_apply': None, 'new_column_name': None}, {'filter': None, 'value_to_apply': None, 'new_column_name': None}, {'filter': None, 'value_to_apply': None, 'new_column_name': None}, {'filter': None, 'value_to_apply': None, 'new_column_name': None}, {'filter': None, 'value_to_apply': None, 'new_column_name': None}]):
    """
    label_dataframe_subsets (df, list_of_labels = [{'filter': None, 'value_to_apply': None, 'new_column_name': None}, {'filter': None, 'value_to_apply': None, 'new_column_name': None}, {'filter': None, 'value_to_apply': None, 'new_column_name': None}, {'filter': None, 'value_to_apply': None, 'new_column_name': None}, {'filter': None, 'value_to_apply': None, 'new_column_name': None}, {'filter': None, 'value_to_apply': None, 'new_column_name': None}, {'filter': None, 'value_to_apply': None, 'new_column_name': None}, {'filter': None, 'value_to_apply': None, 'new_column_name': None}, {'filter': None, 'value_to_apply': None, 'new_column_name': None}, {'filter': None, 'value_to_apply': None, 'new_column_name': None}]):
    
    This function selects subsets of the dataframe by applying a list
     of row filters, and then it labels each one of the filtered subsets.
    
    : param: df: dataframe to be analyzed.
    
    : param: list_of_labels = [{'filter': None, 'value_to_apply': None, 'new_column_name': None}]
      list_of_labels is as a list of dictionaries. It must be declared as a list, in brackets,
      even if there is a single dictionary.
      Use always the same keys: 'filter' for one of the boolean filters that will be applied; 
      'value_to_apply' the value that will be used for labelling that specific subset selected
      from the boolean filter (it may be either a string or a value); and
      'new_column_name': a string or variable to be the name of the new column created. If None,
      a standard name will be applied.
    
    ATTENTION: If you want the labels to be applied to a same column, declare the exact same value
     for the key 'new_column_name'. Also, if you want the value to be applied to an existing column,
     declare the existing column's name in 'new_column_name'.
    
     If you want, you can remove elements (dictionaries) from the list to declare fewer elements;
     and you can also add more elements (dictionaries) to the lists, if you need to plot more series.
     Simply put a comma after the last element from the list and declare a new dictionary, keeping the
     same keys: {'filter': filter, 'value_to_apply': value, 'new_column_name': name}, where 
     filter, value, and name represent the boolean filter, the value for labelling, and the new
     column name (you can pass 'value_to_apply': None, 'new_column_name': None, but if 
     'filter' is None, the new dictionary will be ignored).
    
     define the filters and only them define the filters list
    
    EXAMPLES OF BOOLEAN FILTERS TO COMPOSE THE LIST
      boolean_filter1 = ((None) & (None)) 
      (condition1 AND (&) condition2)
      boolean_filter2 = ((None) | (None)) 
      condition1 OR (|) condition2
    
    boolean filters result into boolean values True or False.
    Examples of filters:
     filter1 = (condition 1) & (condition 2)
     filter1 = (df['column1'] > = 0) & (df['column2']) < 0)
     filter2 = (condition)
     filter2 = (df['column3'] <= 2.5)
     filter3 = (df['column4'] > 10.7)
     filter3 = (condition 1) | (condition 2)
     filter3 = (df['column5'] != 'string1') | (df['column5'] == 'string2')

    comparative operators: > (higher); >= (higher or equal); < (lower); 
     <= (lower or equal); == (equal); != (different)

    concatenation operators: & (and): the filter is True only if the 
     two conditions concatenated through & are True
     | (or): the filter is True if at least one of the two conditions concatenated
     through | are True.
     ~ (not): inverts the boolean, i.e., True becomes False, and False becomes True. 

    separate conditions with parentheses. Use parentheses to define a order
     of definition of the conditions:
     filter = ((condition1) & (condition2)) | (condition3)
     Here, firstly ((condition1) & (condition2)) = subfilter is evaluated. 
     Then, the resultant (subfilter) | (condition3) is evaluated.

    Pandas .isin method: you can also use this method to filter rows belonging to
     a given subset (the row that is in the subset is selected). The syntax is:
     is_black_or_brown = dogs["color"].isin(["Black", "Brown"])
     or: filter = (dataframe_column_series).isin([value1, value2, ...])
     The negative of this condition may be acessed with ~ operator:
     filter = ~(dataframe_column_series).isin([value1, value2, ...])
     Also, you may use isna() method as filter for missing values:
     filter = (dataframe_column_series).isna()
     or, for not missing: ~(dataframe_column_series).isna()
    
    Warning: the sequence of filtering dictionaries must be correspondent to the sequence of labels. 
     Rows selected from the first filter are labelled with the first item from the labels
     list; rows selected by the 2nd filter are labelled with the 2nd element, and so on.
    """

    print("Attention: this function selects subsets from the dataframe and label them, allowing the seggregation of the data.\n")
    print("If you want to filter the dataframe to eliminate non-selected rows, use the function apply_row_filters_list\n")
    
    # Set a local copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    
    numeric_dtypes = [np.int16, np.int32, np.int64, np.float16, np.float32, np.float64]
    
    # List of new columns:
    new_cols_list = []
    
    # Loop through all dictionaries in list_of_labels:
    for dictionary in list_of_labels:
        
        # Check if the 'filter' key is not None:
        boolean_filter = dictionary['filter']
        
        if (boolean_filter is not None):
            
            if (dictionary['value_to_apply'] is None):
                label = np.nan
            
            else:
                label = dictionary['value_to_apply']
            
            if (dictionary['new_column_name'] is None):
                
                new_column = "labelled_column_" + str(list_of_labels.index(dictionary))
            
            else:
                new_column = str(dictionary['new_column_name'])
            
            #Apply the filter to select a group of rows, and apply the correspondent label
            # to the selected rows

            # syntax: dataset.loc[dataset['column_filtered'] <= 0.87, 'labelled_column'] = 1
            # which is equivalent to dataset.loc[(filter), 'labelled_column'] = label
            DATASET.loc[(boolean_filter), new_column] = label
            
            # If the new_column is not in the list of new_Columns, append it:
            if (new_column not in new_cols_list):
                new_cols_list.append(new_column)
            
    # If new_column in numeric types, try to convert it to strings.
    # It is important for the box and violin plots:
    
    for new_column in new_cols_list:
        
        if (DATASET[new_column].dtypes in numeric_dtypes):
            try:
                DATASET[new_column] = (DATASET[new_column]).astype(str)
                
            except: #simply pass
                pass
    
    # Reset index:
    DATASET = DATASET.reset_index(drop = True)
    
    print("Successfully labelled the dataframe. Check its 10 first rows:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(DATASET.head(10))
            
    except: # regular mode
        print(DATASET.head(10))
    
    return DATASET


def estimate_sample_size (target_mean_or_proportion, current_mean_or_proportion = None, current_standard_deviation = None, what_to_test = 'proportion', confidence_level_pct = 95, test_power_pct = 20, perform_two_sided_test = True, df = None, variable_to_analyze = None):
    
    """
    estimate_sample_size (target_mean_or_proportion, current_mean_or_proportion = None, current_standard_deviation = None, what_to_test = 'proportion', confidence_level_pct = 95, test_power_pct = 20, perform_two_sided_test = True, df = None, variable_to_analyze = None):
    
    Evaluate the sample size required to get a significant result out of your AB or ANOVA test. 
    
    **Example: you are working for a food delivery app to determine if a new feature which provides custom suggestions to each user 
    based on their preferences will increase the `conversion rate` of the app. This rate measures the rate of users who "converted" or 
    placed an order using the app. The current CVR of the app is 12% and the stakeholders would like the new feature to increase it 
    up to a 14%**. Given this expectation you can compute the required sample size.

    - For comparison of proportions of success on binary (categorical) results, the compared column must have been labelled with 0 
    for failure and 1 for success.
    
    Main reference: Luis Serrano with DeepLearning.AI (Coursera): Probability & Statistics for Machine Learning & Data Science
     https://www.coursera.org/learn/machine-learning-probability-and-statistics

    
    : param: target_mean_or_proportion is a numeric value correspondent to the mean or proportion that the user wants to observe.
      If it is a proportion, p must be input as a fraction. For example, if the user wants to perform a test to verify
      a modification of conversion rate from 12 to 14%, then the target proportion is 0.14, i.e., target_mean_or_proportion = 0.14.
      If the target is a mean, any real number may be input. For instance, if user wants to verify a decrease of 200 to 150ºC
      of temperature, target_mean_or_proportion = 150.

    : param: current_mean_or_proportion is a numeric value correspondent to the mean or proportion that the user observes now.
      User may directly input it or the value can be retrieved from the response column on the dataset. To calculate from the
      response on dataset, keep current_mean_or_proportion = None

    IN CASE OF INPUT OF PARAMETER CURRENT_MEAN_OR_PROPORTION
      If it is a proportion, p must be input as a fraction. For example, if the user wants to perform a test to verify
      a modification of conversion rate from 12 to 14%, then the current proportion is 0.12, i.e., current_mean_or_proportion = 0.12.
      If the target is a mean, any real number may be input. For instance, if user wants to verify a decrease of 200 to 150ºC
      of temperature, current_mean_or_proportion = 200.

    ATTENTION: If a manual input is provided as current_mean_or_proportion, the dataframe will not be evaluated in terms of
      mean or proportion, even if the dataframe and its column are provided.

    : param: current_standard_deviation = None - numeric (real) value representing the current standard deviation of the response variable.
      If user wants to retrieve the information from the response column on the dataset, current_standard_deviation is kept as None.
      If user wants to input the current mean value as current_mean_or_proportion (manual input) to check difference of mean,
      a real number representing the current standard deviation must be also input. Example: current_standard_deviation = 2.51
      Notice that this parameter only matters for the tests of mean difference, and is ignored when evaluating different proportions.
      If no value is provided, but a column and a dataset are pointed, then the function will try to retrieve the value from the 
      dataframe, even if a manual value of mean is provided.

    : param: what_to_test = 'proportion' for verifying differences between proportions.
      what_to_test = 'mean' for verifying differences between mean values.

    : param: confidence_level_pct = 95 = 95% confidence
      It is the percent of confidence for the analysis.
      Set confidence_level_pct = 90 to get 0.90 = 90% confidence in the analysis.
      Notice that, when less trust is needed, we can reduce confidence_level_pct
      to get less restrictive results.
      alpha = 1 - (confidence_level_pct/100)

    : param: test_power_pct = 20 = 20% power
      It is the percent of power of the test.
      Set test_power_pct = 20 to get 0.20 = 20% power in the analysis.
      Notice that, when less trust is needed, we can reduce the power
      to get less restrictive results.
      beta = 1 - (test_power_pct/100)

    : param: perform_two_sided_test = True. Wether or not to perform a two-sided test. Keep it
      True to use the 2-sided test, which will evaluate if there is a significant difference (higher
      or lower). This is the recommended configuration
      If PERFORM_TWO_SIDED_TEST = False, a one-sided test will be used instead (not recommended configuration).

    IN CASE A MANUAL INPUT OF CURRENT MEAN OR PROPORTION WAS NOT PROVIDED:
    : param: df
     A dataframe object must be input as df. Example: df = dataset
     Also the column containing the current values of the variable to analyze must be provided as 
     variable_to_analyze.
     df is an object, so do not declare it in quotes. 
    
    : param:variable_to_analyze is a string, so declare it in quotes.
     Example: variable_to_analyze = 'response'
     If manual inputs are provided, you may keep df = None and variable_to_analyze = None
    """
    
    import math
    import scipy.stats as stats
    
    alpha = 1 - (confidence_level_pct/100)
    beta = 1 - (test_power_pct/100)

    # Define subfunctions to calculate the sample size:
    def sample_size_diff_proportions(p1, p2, alpha = 0.05, beta = 0.20, two_sided = True):
        
        """
        EVALUATING DIFFERENCES OF PROPORTIONS
        Sample Size Needed to Compare Two Binomial Proportions Using a Two-Sided Test with Significance Level $\alpha$ and 
        Power $1 - \beta$ Where One Sample $(n_2)$ is $k$ times as Large as the Other Sample $(n_1)$ (Independent-Sample Case)

        To test the hypothesis $H_0:p_1 = p_2$ vs. $H_1: p_1 \neq p_2$ for the specific alternative 
        $\mid p_1 - p_2 \mid = \Delta$, with significance level $\alpha$ and power $1 - \beta$, for the following sample size is required

        $$n_1 = \frac{\left[\sqrt{\bar{p}\bar{q}\left(1 + \frac{1}{k} \right)}z_{1- \alpha/2} + \sqrt{p_1 q_1 + \frac{p_2q_2}{k}}z_{1-\beta}\right]^2}{\Delta^2}$$
        $$n_2 = k n_1$$
        where $p_1,p_2 = $ projected true probabilities of success in the two groups
        $$q_1,q_2 = 1 - p_1, 1 - p_2$$
        $$\Delta  = \mid p_2 - p_1 \mid$$
        $$\overline{p} = \frac{p_1 + kp_2}{1+ k}$$
        """

        k = 1

        q1, q2 = (1 - p1), (1 - p2)
        p_bar = (p1 + k * p2) / (1 + k)
        q_bar = 1 - p_bar
        delta = abs(p2 - p1)

        if two_sided:
            alpha = alpha / 2

        n = np.square(
            np.sqrt(p_bar * q_bar * (1 + (1 / k))) * stats.norm.ppf(1 - (alpha))
            + np.sqrt((p1 * q1) + (p2 * q2 / k)) * stats.norm.ppf(1 - beta)
        ) / np.square(delta)

        return math.ceil(n)

    def sample_size_diff_means(mu1, mu2, sigma, alpha = 0.05, beta = 0.20, two_sided = True):

        """
        EVALUATING DIFFERENCES OF MEANS
        Sample Size Needed for Comparing the Means of Two Normally Distributed Samples of Equal Size Using a Two-Sided Test with 
        Significance Level $\alpha$ and Power $1 - \beta$.

        $$ n = \frac{\left(\sigma_{1}^{2} + \sigma_{2}^2 \right) \left(z_{1-\alpha/2} + z_{1-\beta} \right)^2}{\Delta^2} = 
        \text{sample size for each group}$$

        where $\Delta = \mid \mu_{2} - \mu_{1} \mid$. 
        The means and variances of the two representative groups are $(\mu_1,\sigma_{1}^2)$ and $(\mu_2,\sigma_{2}^2)$.
        """
        
        delta = abs(mu2 - mu1)

        if two_sided:
            alpha = alpha / 2

        n = (
            (np.square(sigma) + np.square(sigma))
            * np.square(stats.norm.ppf(1 - alpha) + stats.norm.ppf(1 - beta))
        ) / np.square(delta)

        return math.ceil(n)

    # check if a manual input was not provided:
    if (current_mean_or_proportion is None):
        # There is no manual input. Try to retrieve from the dataframe
        # Check if there is a column and a dataframe:
        
        if ((df is not None) & (variable_to_analyze is not None)):
            # Save the column as a NumPy array to manipulate it independently from the dataframe
            if (what_to_test == 'mean'):
                current_mean_or_proportion = np.mean(np.array(df[variable_to_analyze]))
            
            elif (what_to_test == 'proportion'):
                current_mean_or_proportion = np.sum(np.array(df[variable_to_analyze]))/len(np.array(df[variable_to_analyze]))

        else:
            raise InvalidInputsError ("Manually input a mean or proportion or add a dataframe with a column name as string to perform the analysis.")


    if (what_to_test == 'mean'):

        # Check if a standard deviation value was input
        if (current_standard_deviation is None):
        # There is no manual input. Try to retrieve from the dataframe
        # Check if there is a column and a dataframe:
        
            if ((df is not None) & (variable_to_analyze is not None)):
                # Save the column as a NumPy array to manipulate it independently from the dataframe
                current_standard_deviation = np.std(np.array(df[variable_to_analyze]))
                # Standard deviation will only be effectly used when the mean is tested.
            
            else:
                raise InvalidInputsError ("Manually input a standard deviation or add a dataframe with a column name as string to perform the analysis.")

        required_sample_size = sample_size_diff_means(mu1 = current_mean_or_proportion, mu2 = target_mean_or_proportion, sigma = current_standard_deviation, alpha = alpha, beta = beta, two_sided = perform_two_sided_test)
    

    elif (what_to_test == 'proportion'):

        if (target_mean_or_proportion > 1):
            raise InvalidInputsError (f"The target proportion must be input as a fraction. Not as a percent. Suggestion: input target_mean_or_proportion = {target_mean_or_proportion/100} instead of {target_mean_or_proportion}.")
    
        required_sample_size = sample_size_diff_proportions(p1 = current_mean_or_proportion, p2 = target_mean_or_proportion, alpha = alpha, beta = beta, two_sided = perform_two_sided_test)

    print("Finished estimation. The sample size was returned as the variable 'required_sample_size'.")
    print(f"At least {required_sample_size} samples are needed to verify a modification of {what_to_test} from {current_mean_or_proportion:.2f} to {target_mean_or_proportion}.\n")

    return required_sample_size


def anova_box_violin_plot (plot_type = 'box', confidence_level_pct = 95, orientation = 'vertical', reference_value = None, data_in_same_column = False, df = None, column_with_labels_or_groups = None, variable_to_analyze = None, list_of_dictionaries_with_series_to_analyze = [{'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}], obtain_boxplot_with_filled_boxes = True, obtain_boxplot_with_notched_boxes = False, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    anova_box_violin_plot (plot_type = 'box', confidence_level_pct = 95, orientation = 'vertical', reference_value = None, data_in_same_column = False, df = None, column_with_labels_or_groups = None, variable_to_analyze = None, list_of_dictionaries_with_series_to_analyze = [{'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}], obtain_boxplot_with_filled_boxes = True, obtain_boxplot_with_notched_boxes = False, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
      
    : param: plot_type = 'box' to plot a boxplot.
      plot_type = 'violin' to plot a violinplot.
      If plot_type = None, or plot_type = 'only_anova', only the anova analysis will be performed.
      https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.boxplot.html
      https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.violinplot.html
        
    : param: confidence_level_pct = 95 = 95% confidence
      It is the percent of confidence for the analysis.
      Set confidence_level_pct = 90 to get 0.90 = 90% confidence in the analysis.
      Notice that, when less trust is needed, we can reduce confidence_level_pct
      to get less restrictive results.
      alpha_anova = 1 - (confidence_level_pct/100)
    
    : param: orientation = 'vertical' for vertical plots; 
      or orientation = 'horizontal', for horizontal plots.
      Manipulate the parameter vert (boolean).
        
    : param: reference_value: keep it as None or add a float value.
      This reference value will be shown as a red constant line to be compared
      with the plots. e.g. reference_value = 1.0 will plot a red line passing through
      VARIABLE_TO_ANALYZE = 1.0
    
    : param: data_in_same_column: set as True if all the values to plot are in a same column.
      If data_in_same_column = True, you must specify the dataframe containing the data as df;
      the column containing the label or group indication as column_with_labels_or_groups; and the column 
      containing the variable to analyze as variable_to_analyze.
      If column_with_labels_or_groups is None, the ANOVA analysis will not be performed and 
      the plot will be obtained for the whole series.
    
    : param: df is an object, so do not declare it in quotes. The other three arguments (columns' names) 
      are strings, so declare in quotes. 
    
      Example: suppose you have a dataframe saved as dataset, and two groups A and B to compare. 
      All the results for both groups are in a column named 'results'. If the result is for
      an entry from group A, then a column named 'group' has the value 'A'. If it is for group B,
      column 'group' shows the value 'B'. In this example:
      data_in_same_column = True,
      df = dataset,
      column_with_labels_or_groups = 'group',
      variable_to_analyze = 'results'.
      If you want to declare a list of dictionaries, keep data_in_same_column = False and keep
      df = None (the other arguments may be set as None, but it is not mandatory: 
      column_with_labels_or_groups = None, variable_to_analyze = None).
    
    Parameter to input when DATA_IN_SAME_COLUMN = False:
    : param: list_of_dictionaries_with_series_to_analyze {'values_to_analyze': None, 'label': None}:
      if data is already converted to series, lists or arrays, provide them as a list of dictionaries. 
      It must be declared as a list, in brackets, even if there is a single dictionary.
      Use always the same keys: 'values_to_analyze' for values that will be analyzed, and 'label' for
      the label or group correspondent to the series (may be a number or a string). 
      If you do not want to declare a series, simply keep as None, but do not remove or rename a 
      key (ALWAYS USE THE KEYS SHOWN AS MODEL).
      If you want, you can remove elements (dictionaries) from the list to declare fewer elements;
      and you can also add more elements (dictionaries) to the lists, if you need to plot more series.
      Simply put a comma after the last element from the list and declare a new dictionary, keeping the
      same keys: {'values_to_analyze': y, 'label': 'series_y'}, where y represents the values
      to analyze, and 'series_y' is the label 
      (you can pass 'label': None, but if values_to_analyze' is None, the new 
      dictionary will be ignored).
    
      Examples:
      list_of_dictionaries_with_series_to_analyze = 
        [{'values_to_analyze': y, 'label': 0}]
      will plot a single variable. In turns:
      list_of_dictionaries_with_series_to_analyze = 
       [{'values_to_analyze': DATASET['Y1'], 'label': 'label1'}, 
        {'values_to_analyze': DATASET['Y2'], 'label': 'label2'}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}]
      will plot two series, Y1 and Y2.
      Notice that all dictionaries where 'values_to_analyze' is None are automatically ignored.
      If None is provided to 'label', an automatic label will be generated.
    
    Parameters with effect only for boxplots (plot_type = 'box'):
    : param: obtain_boxplot_with_filled_boxes = True
      Manipulate parameter patch_artist (boolean, default: False)
      If obtain_boxplot_with_filled_boxes = True, the boxes are created filled. 
      If obtain_boxplot_with_filled_boxes = False, only the contour of the boxes are shown
      (obtain void white boxes).
    
    : param: obtain_boxplot_with_notched_boxes = False
      Manipulate parameter notch (boolean, default: False) from the boxplot object
      Whether to draw a notched boxplot (obtain_boxplot_with_notched_boxes = True), 
      or a rectangular boxplot (obtain_boxplot_with_notched_boxes = False). 
      The notches represent the confidence interval (CI) around the median. 
    
      https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.boxplot.html
    """

    print ("If an error message is shown, update statsmodels to a version >= 0.13.2. To update to this version, declare and run a cell as the following command; or run it on command line without magic character '!':")
    print ("!pip install statsmodels==0.13.2 --upgrade")
    print ("Also, update matplotlib to a version >= 3.5.2 by running:")
    print ("!pip install matplotlib==3.5.2 --upgrade\n")
    import random
    from statsmodels.stats.oneway import anova_oneway
        
    alpha_anova = 1 - (confidence_level_pct/100)
 
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
        
        elif (variable_to_analyze is None):
            
            print("Please, input a valid column name as variable_to_analyze.\n")
            list_of_dictionaries_with_series_to_analyze = []
        
        else:
            
            # set a local copy of the dataframe:
            DATASET = df.copy(deep = True)
            
            if (column_with_labels_or_groups is None):
            
                print("Using the whole series (column).\n")
                column_with_labels_or_groups = 'whole_series_' + variable_to_analyze
                DATASET[column_with_labels_or_groups] = column_with_labels_or_groups
            
            # sort DATASET; by column_with_labels_or_groups; and by variable_to_analyze,
            # all in Ascending order
            # Since we sort by label (group), it is easier to separate the groups.
            DATASET = DATASET.sort_values(by = [column_with_labels_or_groups, variable_to_analyze], ascending = [True, True])
            
            # Drop rows containing missing values in column_with_labels_or_groups or variable_to_analyze:
            DATASET = DATASET.dropna(how = 'any', subset = [column_with_labels_or_groups, variable_to_analyze])
            
            # Reset indices:
            DATASET = DATASET.reset_index(drop = True)
            
            # Get a series of unique values of the labels, and save it as a list using the
            # list attribute:
            unique_labels = list(DATASET[column_with_labels_or_groups].unique())
            print(f"{len(unique_labels)} different labels detected: {unique_labels}.\n")
            
            # Start a list to store the dictionaries containing the keys:
            # 'values_to_analyze' and 'label'
            list_of_dictionaries_with_series_to_analyze = []
            
            # Loop through each possible label:
            for lab in unique_labels:
                # loop through each element from the list unique_labels, referred as lab
                
                # Set a filter for the dataset, to select only rows correspondent to that
                # label:
                boolean_filter = (DATASET[column_with_labels_or_groups] == lab)
                
                # Create a copy of the dataset, with entries selected by that filter:
                ds_copy = (DATASET[boolean_filter]).copy(deep = True)
                # Sort again by X and Y, to guarantee the results are in order:
                ds_copy = ds_copy.sort_values(by = [column_with_labels_or_groups, variable_to_analyze], ascending = [True, True])
                # Restart the index of the copy:
                ds_copy = ds_copy.reset_index(drop = True)
                
                # Re-extract the analyzed series and convert it to NumPy array: 
                # (these arrays will be important later in the function):
                y = np.array(ds_copy[variable_to_analyze])
            
                # Then, create the dictionary:
                dict_of_values = {'values_to_analyze': y, 'label': lab}
                
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
            
            # access 'values_to_analyze' and 'label' keys from the dictionary:
            values_to_analyze = dictionary['values_to_analyze']
            lab = dictionary['label']
            # Remember that all this variables are series from a dataframe, so we can apply
            # the astype function:
            # https://www.askpython.com/python/built-in-methods/python-astype?msclkid=8f3de8afd0d411ec86a9c1a1e290f37c
            
            # check if at least values_to_analyze is not None:
            if (values_to_analyze is not None):
            
                # Possibly, series is a not ordered Pandas series, and may contain missing values.
                # Let's order it and clean it, if it is a Pandas object:
                try:
                    # Create a local copy to manipulate
                    series = values_to_analyze.copy(deep = True)
                    series = series.sort_values(ascending = True)
                    series = series.dropna()
                
                except:
                    # It is not a Pandas object. Simply copy to use the same variable name:
                    series = values_to_analyze
                
                # Re-extract Y series and convert it to NumPy array 
                # (these arrays will be important later in the function):
                y = np.array(series)
                
                # check if label is None:
                if (lab is None):
                    # input a default label.
                    # Use the str attribute to convert the integer to string, allowing it
                    # to be concatenated
                    lab = "series_" + str(i)
                    
                # Then, create the dictionary:
                dict_of_values = {'values_to_analyze': y, 'label': lab}
                
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
        
        # For performing the ANOVA, we must store all series into an array of arrays,
        # and must create a correspondent array of labels: each label will correspond to one
        # series (one element from the array of arrays).
        # Create the lists (d represents a dictionary):
        list_of_arrays = [list(d['values_to_analyze']) for d in list_of_dictionaries_with_series_to_analyze]
        list_of_labels = [d['label'] for d in list_of_dictionaries_with_series_to_analyze]
        
        # Calculate and store the means and medians for each label:
        # https://numpy.org/doc/stable/reference/generated/numpy.mean.html
        # https://numpy.org/doc/stable/reference/generated/numpy.median.html
        list_of_means = [np.mean(array) for array in list_of_arrays]
        list_of_medians = [np.median(array) for array in list_of_arrays]
        list_of_min = [min(array) for array in list_of_arrays]
        list_of_max = [max(array) for array in list_of_arrays]
        
        # Store the total of valid series:
        total_series = len(list_of_labels)
        # Let's pad the series by eliminating random elements until all series have the
        # same lengths:
        
        # If there are 2 or more series to analyze, perform the ANOVA:
        if (total_series <= 1):
            print("There is a single valid series, so the analysis of variance (ANOVA) will not be performed.\n")
            # An empty ANOVA dictionary will be returned:
            anova_summary_dict = {}
        
        else:
            print(f"Analysis of variance (ANOVA) for the {total_series} detected series:\n")
            
    
            # Let's get the minimum length for the lists above:
            min_length = min(len(list_of_values) for list_of_values in list_of_arrays)

            # start a supporting list:
            support_list = []

            print("p-value: probability of verifying the tested event, given that the null hypothesis H0 is correct.\n")

            for list_of_values in list_of_arrays:
                
                while (min_length < len(list_of_values)):
                    
                    # Let's randomly select len_difference indices to delete:
                    list_indices = range(0, len(list_of_values))
                    
                    # Randomly select len_difference elements:
                    # Function random.choices(input_sequence, k = number_of_samples):
                    # randomly select k elements from the sequence input_sequence. This function is
                    # newer than random.sample
                    
                    # Select an index to delete
                    deleted_index = random.choices(list_indices, k = 1)
                    # Now, delete this element:
                    # The pop function is safer and returns the deleted elements, but cannot do
                    # it in a single call.
                    # Even though del can process a list, we cannot pass a list comprehension like
                    # del [list_of_values[i] for i in deleted_indices]
                    # deleted_index is a 1-element list. Pick only the first
                    deleted_element = list_of_values.pop(deleted_index[0])
                
                # Now, convert it to NumPy array:
                list_of_values = np.array(list_of_values)
                # Append it to the support list:
                support_list.append(list_of_values)
            
            # Make the support_list the list_of_arrays itself:
            list_of_arrays = support_list
            # Now all lists are padded and are represented by padded arrays.
            
            #Now, we can pass the arrays as arguments for the one-way Anova:
            anova_one_way_summary = anova_oneway(list_of_arrays)
            # https://www.statsmodels.org/stable/generated/statsmodels.stats.oneway.anova_oneway.html

            # The information is stored in a tuple (f_statistic, p-value)
            # f_statistic: Test statistic for k-sample mean comparison which is approximately 
            # F-distributed.
            # p-value: If use_var="bf", then the p-value is based on corrected degrees of freedom following Mehrotra 1997.
            f_statistic = anova_one_way_summary[0]
            p_value = anova_one_way_summary[1]
            
            anova_summary_dict = {'groups_length':min_length, 'F_statistic': f_statistic, 'p_value': p_value}
            
            print(f"Total of samples in each group used for ANOVA (after padding): {min_length}\n")
            print(f"Probability that the means of the groups are the same = {100*p_value:.2f}% (p-value = {p_value:e})\n")
            print(f"Calculated F-statistic for the variances = {f_statistic:e}\n")
            
            # start a statistics list:
            statistics_list = []
            
            print("Statistics for each detected label:\n")
            
            # If we apply the function zip(list_of_labels, list_of_means, list_of_medians, list_of_min, list_of_max), 
            # we obtain a series of tuples. The i-th tuple contains the i-th element from list_of_labels, 
            # the i-th from list_of_means, the i-th from list_of_medians, the i-th from list_of_min, and
            # the i-th from list_of_max in this order. So, we can iterate through the 5 lists simultaneously, 
            # without declaring a counter variable by decoupling the zip:
            for label, mean, median, minimum, maximum in zip(list_of_labels, list_of_means, list_of_medians, list_of_min, list_of_max):
                
                label_dict = {'label': label, 'mean': mean, 'median': median, 'min': minimum, 'max': maximum}
                statistics_list.append(label_dict)
                
                print(f"Mean value of label '{label}' = {mean:e}")
                print(f"Median value of label '{label}' = {median:e}")
                print(f"Minimum value of label '{label}' = {minimum:e}")
                print(f"Maximum value of label '{label}' = {maximum:e}\n")
            
            # Add the statistics list to the anova_summary_dict:
            anova_summary_dict['statistics'] = statistics_list
            
            # :e indicates the scientific notation

            if (p_value <= alpha_anova):
                print(f"For a confidence level of {confidence_level_pct:.2f}%, we can reject the null hypothesis.")
                print(f"The means are different for a {confidence_level_pct:.2f}% confidence level.")

            else:
                print(f"For a confidence level of {confidence_level_pct}%, we can accept the null hypothesis.")
                print(f"The means are equal for a {confidence_level_pct}% confidence level.")
                

        if ((plot_type is not None) & (plot_type != 'only_anova')):

            # Now, let's obtain the plots:
            # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
            # so that the bars do not completely block other views.
            OPACITY = 0.95

            # Manipulate the parameter vert (boolean, default: True)
            # If True, draws vertical boxes. If False, draw horizontal boxes.
            if (orientation == 'horizontal'):
                VERT = False

                if (horizontal_axis_title is None):
                    # Set horizontal axis title
                    horizontal_axis_title = "analyzed_series"

                if (vertical_axis_title is None):
                    # Set vertical axis title
                    vertical_axis_title = "group_or_label"

            else:
                VERT = True

                if (horizontal_axis_title is None):
                    # Set horizontal axis title
                    horizontal_axis_title = "group_or_label"

                if (vertical_axis_title is None):
                    # Set vertical axis title
                    vertical_axis_title = "analyzed_series"

            if (obtain_boxplot_with_filled_boxes is None):
                obtain_boxplot_with_filled_boxes = True

            if (obtain_boxplot_with_notched_boxes is None):
                obtain_boxplot_with_notched_boxes = False

            if (plot_title is None):
                # Set graphic title
                plot_title = f"{plot_type}_plot"

            # Now, let's obtain the boxplot
            fig, ax = plt.subplots(figsize = (12, 8))

            if (plot_type == 'box'):
                # rectangular box plot
                # The arrays of each group are the elements of the list humongous_list
                plot_returned_dict = ax.boxplot(list_of_arrays, labels = list_of_labels, notch = obtain_boxplot_with_notched_boxes, vert = VERT, patch_artist = obtain_boxplot_with_filled_boxes)

                # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.boxplot.html

                # plot_returned_dict: A dictionary mapping each component of the boxplot to 
                # a list of the Line2D instances created. That dictionary has the following keys 
                # (assuming vertical boxplots):
                # boxes: the main body of the boxplot showing the quartiles and the median's 
                # confidence intervals if enabled.
                # medians: horizontal lines at the median of each box.
                # whiskers: the vertical lines extending to the most extreme, non-outlier data 
                # points.
                # caps: the horizontal lines at the ends of the whiskers.
                # fliers: points representing data that extend beyond the whiskers (fliers).
                # means: points or lines representing the means.

                # boxplot contains only lists (iterable collections) of objects
                # (matplotlib.lines.Line2D objects):
                # Each object on the list corresponds to one series being plot. For setting
                # different colors, the parameters must be different for each object from one list.

                for whisker in plot_returned_dict['whiskers']:
                    whisker.set_color('crimson')
                    whisker.set_alpha(OPACITY)

                for cap in plot_returned_dict['caps']:
                    cap.set_color('crimson')
                    cap.set_alpha(OPACITY)

                for flier in plot_returned_dict['fliers']:
                    flier.set_color('crimson')
                    flier.set_alpha(OPACITY)

                for mean in plot_returned_dict['means']:
                    mean.set_color('crimson')
                    mean.set_alpha(OPACITY)

                for median in plot_returned_dict['medians']:
                    median.set_color('crimson')
                    median.set_alpha(OPACITY)

                # Set the boxes configuration for each case, where it should be filled or not:
                if (obtain_boxplot_with_filled_boxes):
                    for box in plot_returned_dict['boxes']:
                        box.set_color('lightgrey')
                        box.set_alpha(0.5)
                else: # only the contour of the box
                    for box in plot_returned_dict['boxes']:
                        box.set_color('black')
                        box.set_alpha(1.0)

            if (plot_type == 'violin'):
                # violin plot, estimate of the statistical distribution
                # The arrays of each group are the elements of the list humongous_list
                plot_returned_dict = ax.violinplot(list_of_arrays, vert = VERT, showmeans = True, showextrema = True, showmedians = True)

                # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.violinplot.html

                # plot_returned_dict: A dictionary mapping each component of the violinplot to a list of 
                # the corresponding collection instances created. The dictionary has the following keys:
                # bodies: A list of the PolyCollection instances containing the filled area of each 
                # violin.
                # cmeans: A LineCollection instance that marks the mean values of each of the violin's 
                # distribution.
                # cmins: A LineCollection instance that marks the bottom of each violin's distribution.
                # cmaxes: A LineCollection instance that marks the top of each violin's distribution.
                # cbars: A LineCollection instance that marks the centers of each violin's distribution.
                # cmedians: A LineCollection instance that marks the median values of each of the violin's distribution.
                # cquantiles: A LineCollection instance created to identify the quantile values of each 
                # of the violin's distribution.

                # Here, the labels must be defined manually:
                if (orientation == 'horizontal'):
                    ax.set_yticks(np.arange(1, len(list_of_labels) + 1), labels = list_of_labels)

                else:
                    ax.set_xticks(np.arange(1, len(list_of_labels) + 1), labels = list_of_labels)
                    # np.arange(1, len(list_of_labels) + 1) is the same list of numbers that the violinplot
                    # associates to each sequence.

                # https://matplotlib.org/stable/gallery/statistics/customized_violin.html#sphx-glr-gallery-statistics-customized-violin-py

                # Violinplot contains line objects and lists (iterable collections) of objects
                # matplotlib.collections.LineCollection objects: not iterable
                # These are specific from violin plots:
                plot_returned_dict['cmeans'].set_facecolor('crimson')
                plot_returned_dict['cmeans'].set_edgecolor('crimson')
                plot_returned_dict['cmeans'].set_alpha(OPACITY)

                plot_returned_dict['cmedians'].set_facecolor('crimson')
                plot_returned_dict['cmedians'].set_edgecolor('crimson')
                plot_returned_dict['cmedians'].set_alpha(OPACITY)

                plot_returned_dict['cmaxes'].set_facecolor('crimson')
                plot_returned_dict['cmaxes'].set_edgecolor('crimson')
                plot_returned_dict['cmaxes'].set_alpha(OPACITY)

                plot_returned_dict['cmins'].set_facecolor('crimson')
                plot_returned_dict['cmins'].set_edgecolor('crimson')
                plot_returned_dict['cmins'].set_alpha(OPACITY)

                plot_returned_dict['cbars'].set_facecolor('crimson')
                plot_returned_dict['cbars'].set_edgecolor('crimson')
                plot_returned_dict['cbars'].set_alpha(OPACITY)

                # 'bodies': list of matplotlib.collections.PolyCollection objects (iterable)
                # Each object on the list corresponds to one series being plot. For setting
                # different colors, the parameters must be different for each object from one list.
                for body in plot_returned_dict['bodies']:
                    body.set_facecolor('lightgrey')
                    body.set_edgecolor('black')
                    body.set_alpha(0.5)

            ax.set_title(plot_title)
            ax.set_xlabel(horizontal_axis_title)
            ax.set_ylabel(vertical_axis_title)
            ax.grid(grid)

            if (orientation == 'vertical'):
                # generate vertically-oriented plot

                if not (reference_value is None):
                    # Add an horizontal reference_line to compare against the boxes:
                    # If the boxplot was horizontally-oriented, this line should be vertical instead.
                    ax.axhline(reference_value, color = 'black', linestyle = 'dashed', label = 'reference', alpha = OPACITY)
                    # axhline generates an horizontal (h) line on ax

            else:

                if not (reference_value is None):
                    # Add an horizontal reference_line to compare against the boxes:
                    # If the boxplot was horizontally-oriented, this line should be vertical instead.
                    ax.axvline(reference_value, color = 'black', linestyle = 'dashed', label = 'reference', alpha = OPACITY)
                    # axvline generates a vertical (v) line on ax

            #ROTATE X AXIS IN XX DEGREES
            plt.xticks(rotation = x_axis_rotation)
            # XX = 70 DEGREES x_axis (Default)
            #ROTATE Y AXIS IN XX DEGREES:
            plt.yticks(rotation = y_axis_rotation)
            # XX = 0 DEGREES y_axis (Default)

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
                    file_name = f"{plot_type}_plot"

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
        
        else:
            print(f"Plot type set as {plot_type}. So, no plot was obtained.\n")
        
        print("\n") #line break
        print("Successfully returned 2 dictionaries: anova_summary_dict (dictionary storing ANOVA F-test and p-value); and plot_returned_dict (dictionary mapping each component of the plot).\n")
        
        if (plot_type == 'box'):
        
            print("Boxplot interpretation:\n")
            print("Boxplot presents the following key visual components:\n")
            
            print("Main box")
            print("The main box represents the Interquartile Range (IQR).")
            print("It represents the data that is from quartile Q1 to quartile Q3.\n")
            
            print("Q1 = 1st quartile of the dataset")
            print("25% of values lie below this level (i.e., it is the 0.25-quantile or percentile).\n")
            
            print("Q2 = 2nd quartile of the dataset")
            print("50% of values lie above and below this level (i.e., it is the 0.50-quantile or percentile).\n")
            
            print("Q3 = 3rd quartile of the dataset")
            print("75% of values lie below and 25% lie above this level (i.e., it is the 0.75-quantile or percentile).\n")
            
            print("Median line")
            print("Boxplot main box (the IQR) is divided by an horizontal line if it is vertically-oriented; or by a vertical line if it is horizontally-oriented.")
            print("This line represents the median: it is the midpoint of the dataset.\n")
            
            print("Limit lines")      
            print("There are lines extending beyond the main boxes limits.")
            print("These lines end in horizontal limits, if the boxplot is vertically oriented; or in vertical limits, for an horizontal plot.\n")
            
            print("Minimum limit")
            print("Given that Ymin is the lowest value assumed by the variable, the minimum limit of the boxplot (inferior whisker) is defined as:")
            print("Minimum between Q1 - (1.5) x (IQR width) = Q1 - 1.5*(Q3-Q1) and Ymin")
            print("The whisker must not be below Ymin.\n")
            
            print("Maximum limit")
            print("Given that Ymax is the highest value assumed by the variable, the maximum limit of the boxplot (superior whisker) is defined as:")
            print("Maximum between Q3 + (1.5) x (IQR width) = Q3 + 1.5*(Q3-Q1) and Ymax")
            print("The whisker must not be above Ymax.\n")
            
            print("Outliers")
            print("Finally, there are isolated points (circles) on the plot.")
            print("These points lie below the minimum bar, or above the maximum bar line (beyound the whiskers).")
            print("They are defined as outliers.\n")
            
            print("Application of the plot")        
            print("Like violin plots, box plots are used to represent comparison of a variable distribution (or sample distribution) across different 'categories'.") 
            print("Examples: temperature distribution compared between day and night; or distribution of car prices compared across different car makers.\n")
            # https://nickmccullum.com/python-visualization/boxplot/
        
        elif (plot_type == 'violin'):
            
            print("Violin plot interpretation:\n")
            
            print("A violin plot is similar to a box plot, with the addition of a rotated kernel density plot on each side of the violin.\n")
            print("So, this plot also shows the probability density of the data at different values, usually smoothed by a kernel density estimator.\n")
            print("Typically a violin plot will include all the data that is in a box plot.\n")
            print("It includes a filled area extending to represent the entire data range; with lines at the mean, the median, the minimum, and the maximum.\n")
            
            print("So, let's firstly check the box plot components.")
            print("Notice that the interquartile range represented by the main box will not be present.")
            print("The violin plot replaces this box region by the density distribution itself.\n")
            
            print("Main box")
            print("The main box represents the Interquartile Range (IQR).")
            print("It represents the data that is from quartile Q1 to quartile Q3.\n")
            
            print("Q1 = 1st quartile of the dataset")
            print("25% of values lie below this level (i.e., it is the 0.25-quantile or percentile).\n")
            
            print("Q2 = 2nd quartile of the dataset")
            print("50% of values lie above and below this level (i.e., it is the 0.50-quantile or percentile).\n")
            
            print("Q3 = 3rd quartile of the dataset")
            print("75% of values lie below and 25% lie above this level (i.e., it is the 0.75-quantile or percentile).\n")
            
            print("Median line")
            print("Boxplot main box (the IQR) is divided by an horizontal line if it is vertically-oriented; or by a vertical line if it is horizontally-oriented.")
            print("This line represents the median: it is the midpoint of the dataset.\n")
            
            print("Limit lines")      
            print("There are lines extending beyond the main boxes limits.")
            print("These lines end in horizontal limits, if the boxplot is vertically oriented; or in vertical limits, for an horizontal plot.\n")
            
            print("Minimum limit")
            print("Given that Ymin is the lowest value assumed by the variable, the minimum limit of the boxplot (inferior whisker) is defined as:")
            print("Minimum between Q1 - (1.5) x (IQR width) = Q1 - 1.5*(Q3-Q1) and Ymin")
            print("The whisker must not be below Ymin.\n")
            
            print("Maximum limit")
            print("Given that Ymax is the highest value assumed by the variable, the maximum limit of the boxplot (superior whisker) is defined as:")
            print("Maximum between Q3 + (1.5) x (IQR width) = Q3 + 1.5*(Q3-Q1) and Ymax")
            print("The whisker must not be above Ymax.\n")
            
            print("Outliers")
            print("Finally, there are isolated points (circles) on the plot.")
            print("These points lie below the minimum bar, or above the maximum bar line (beyound the whiskers).")
            print("They are defined as outliers.\n")
            
            print("ATTENTION:")
            print("Since the probability density is shown, these isolated outlier points are not represented in the violin plot.\n")
            
            print("Presence on multiple peaks in the violin plot")
            print("A violin plot is more informative than a plain box plot.")
            print("While a box plot only shows summary statistics such as mean/median and interquartile ranges, the violin plot shows the full distribution of the data.")
            print("This difference is particularly useful when the data distribution is multimodal (more than one peak).")
            print("In this case, a violin plot shows the presence of different peaks, their positions and relative amplitudes.\n")
            
            print("Application of the plot")
            print("Like box plots, violin plots are used to represent comparison of a variable distribution (or sample distribution) across different 'categories'.")
            print("Examples: temperature distribution compared between day and night; or distribution of car prices compared across different car makers.\n")
            
            print("Presence of multiple layers")
            print("A violin plot can have multiple layers. For instance, the outer shape represents all possible results.")
            print("The next layer inside might represent the values that occur 95% of the time.")
            print("The next layer (if it exists) inside might represent the values that occur 50% of the time.\n")
            
            print("Alternative to this plot")
            print("Although more informative than box plots, they are less popular.")
            print("Because of their unpopularity, they may be harder to understand for readers not familiar with them.")
            print("In this case, a more accessible alternative is to plot a series of stacked histograms or kernel density distributions (KDE plots).\n")
            # https://en.wikipedia.org/wiki/Violin_plot#:~:text=A%20violin%20plot%20is%20a%20method%20of%20plotting,values%2C%20usually%20smoothed%20by%20a%20kernel%20density%20estimator.
            
        return anova_summary_dict, plot_returned_dict


def AB_testing (what_to_compare = 'mean', confidence_level_pct = 95, data_in_same_column = False, df = None, column_with_labels_or_groups = None, variable_to_analyze = None, list_of_dictionaries_with_series_to_analyze = [{'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}]):

    """
    AB_testing (what_to_compare = 'mean', confidence_level_pct = 95, data_in_same_column = False, df = None, column_with_labels_or_groups = None, variable_to_analyze = None, list_of_dictionaries_with_series_to_analyze = [{'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}]):

    - Compare if different groups present significant difference of means or proportions using t-test.
    - For comparison of proportions of success on binary (categorical) results, the compared column must have been 
    labelled with 0 for failure and 1 for success.
    - Only compare 2 series.
    
    Main reference: Luis Serrano with DeepLearning.AI (Coursera): Probability & Statistics for Machine Learning & Data Science
     https://www.coursera.org/learn/machine-learning-probability-and-statistics
    
    https://sphweb.bumc.bu.edu/otlt/mph-modules/bs/bs704_confidence_intervals/bs704_confidence_intervals_print.html

    : param: what_to_compare = 'mean' for comparing differences between mean values.
      what_to_compare = 'proportion' for comparing differences between proportions.

    : param: confidence_level_pct = 95 = 95% confidence
      It is the percent of confidence for the analysis.
      Set confidence_level_pct = 90 to get 0.90 = 90% confidence in the analysis.
      Notice that, when less trust is needed, we can reduce confidence_level_pct
      to get less restrictive results.
      alpha = 1 - (confidence_level_pct/100)

    : param: data_in_same_column: set as True if all the values to plot are in a same column.
      If data_in_same_column = True, you must specify the dataframe containing the data as df;
      the column containing the label or group indication as column_with_labels_or_groups; and the column 
      containing the variable to analyze as variable_to_analyze.
      If column_with_labels_or_groups is None, the analysis will not be performed.
    
    : param: df is an object, so do not declare it in quotes. The other three arguments (columns' names) 
      are strings, so declare in quotes. 
    
      Example: suppose you have a dataframe saved as dataset, and two groups A and B to compare. 
      All the results for both groups are in a column named 'results'. If the result is for
      an entry from group A, then a column named 'group' has the value 'A'. If it is for group B,
      column 'group' shows the value 'B'. In this example:
      data_in_same_column = True,
      df = dataset,
      column_with_labels_or_groups = 'group',
      variable_to_analyze = 'results'.
      If you want to declare a list of dictionaries, keep data_in_same_column = False and keep
      df = None (the other arguments may be set as None, but it is not mandatory: 
      column_with_labels_or_groups = None, variable_to_analyze = None).
    
    Parameter to input when DATA_IN_SAME_COLUMN = False:
    : param: list_of_dictionaries_with_series_to_analyze {'values_to_analyze': None, 'label': None}:
      if data is already converted to series, lists or arrays, provide them as a list of dictionaries. 
      It must be declared as a list, in brackets, even if there is a single dictionary.
      Use always the same keys: 'values_to_analyze' for values that will be analyzed, and 'label' for
      the label or group correspondent to the series (may be a number or a string). 
      If you do not want to declare a series, simply keep as None, but do not remove or rename a 
      key (ALWAYS USE THE KEYS SHOWN AS MODEL).
      If you want, you can remove elements (dictionaries) from the list to declare fewer elements;
      and you can also add more elements (dictionaries) to the lists, if you need to plot more series.
      Simply put a comma after the last element from the list and declare a new dictionary, keeping the
      same keys: {'values_to_analyze': y, 'label': 'series_y'}, where y represents the values
      to analyze, and 'series_y' is the label 
      (you can pass 'label': None, but if values_to_analyze' is None, the new 
      dictionary will be ignored).
    
      Example:
      list_of_dictionaries_with_series_to_analyze = 
       [{'values_to_analyze': DATASET['Y1'], 'label': 'label1'}, 
        {'values_to_analyze': DATASET['Y2'], 'label': 'label2'}]
      will test two series, Y1 and Y2.
      Always use only two dictionaries
    """

    import scipy.stats as stats
    

    alpha = 1 - (confidence_level_pct/100)
    
    if (data_in_same_column == True):
        
        print("Data in a same column.\n")
        
        if (df is None):
            
            print("Please, input a valid dataframe as df.\n")
            list_of_dictionaries_with_series_to_analyze = []
            # The code will check the size of this list on the next block.
            # If it is zero, code is simply interrupted.
            # Instead of returning an error, we use this code structure that can be applied
            # on other graphic functions that do not return a summary (and so we should not
            # return a value like 'error' to interrupt the function).
        
        elif (variable_to_analyze is None):
            
            print("Please, input a valid column name as variable_to_analyze.\n")
            list_of_dictionaries_with_series_to_analyze = []
        
        else:
            
            # set a local copy of the dataframe:
            DATASET = df.copy(deep = True)
            
            if (column_with_labels_or_groups is None):
            
                print("Please, input a valid column name as column_with_labels_or_groups.\n")
                list_of_dictionaries_with_series_to_analyze = []
            
            # sort DATASET; by column_with_labels_or_groups; and by variable_to_analyze,
            # all in Ascending order
            # Since we sort by label (group), it is easier to separate the groups.
            DATASET = DATASET.sort_values(by = [column_with_labels_or_groups, variable_to_analyze], ascending = [True, True])
            
            # Drop rows containing missing values in column_with_labels_or_groups or variable_to_analyze:
            DATASET = DATASET.dropna(how = 'any', subset = [column_with_labels_or_groups, variable_to_analyze])
            
            # Reset indices:
            DATASET = DATASET.reset_index(drop = True)
            
            # Get a series of unique values of the labels, and save it as a list using the
            # list attribute:
            unique_labels = list(DATASET[column_with_labels_or_groups].unique())
            print(f"{len(unique_labels)} different labels detected: {unique_labels}.\n")
            
            # Start a list to store the dictionaries containing the keys:
            # 'values_to_analyze' and 'label'
            list_of_dictionaries_with_series_to_analyze = []
            
            # Loop through each possible label:
            for lab in unique_labels:
                # loop through each element from the list unique_labels, referred as lab
                
                # Set a filter for the dataset, to select only rows correspondent to that
                # label:
                boolean_filter = (DATASET[column_with_labels_or_groups] == lab)
                
                # Create a copy of the dataset, with entries selected by that filter:
                ds_copy = (DATASET[boolean_filter]).copy(deep = True)
                # Sort again by X and Y, to guarantee the results are in order:
                ds_copy = ds_copy.sort_values(by = [column_with_labels_or_groups, variable_to_analyze], ascending = [True, True])
                # Restart the index of the copy:
                ds_copy = ds_copy.reset_index(drop = True)
                
                # Re-extract the analyzed series and convert it to NumPy array: 
                # (these arrays will be important later in the function):
                y = np.array(ds_copy[variable_to_analyze])
            
                # Then, create the dictionary:
                dict_of_values = {'values_to_analyze': y, 'label': lab}
                
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
            
            # access 'values_to_analyze' and 'label' keys from the dictionary:
            values_to_analyze = dictionary['values_to_analyze']
            lab = dictionary['label']
            # Remember that all this variables are series from a dataframe, so we can apply
            # the astype function:
            # https://www.askpython.com/python/built-in-methods/python-astype?msclkid=8f3de8afd0d411ec86a9c1a1e290f37c
            
            # check if at least values_to_analyze is not None:
            if (values_to_analyze is not None):
            
                # Possibly, series is a not ordered Pandas series, and may contain missing values.
                # Let's order it and clean it, if it is a Pandas object:
                try:
                    # Create a local copy to manipulate
                    series = values_to_analyze.copy(deep = True)
                    series = series.sort_values(ascending = True)
                    series = series.dropna()
                
                except:
                    # It is not a Pandas object. Simply copy to use the same variable name:
                    series = values_to_analyze
                
                # Re-extract Y series and convert it to NumPy array 
                # (these arrays will be important later in the function):
                y = np.array(series)
                
                # check if label is None:
                if (lab is None):
                    # input a default label.
                    # Use the str attribute to convert the integer to string, allowing it
                    # to be concatenated
                    lab = "series_" + str(i)
                    
                # Then, create the dictionary:
                dict_of_values = {'values_to_analyze': y, 'label': lab} 
                                
                # Now, append dict_of_values to support list:
                support_list.append(dict_of_values)
        
        # Now, support_list contains only the dictionaries with valid entries, as well
        # as labels for each collection of data. The values are independent from their origin,
        # and now they are ordered and in the same format of the data extracted directly from
        # the dataframe.
        # So, make the list_of_dictionaries_with_series_to_analyze the support_list itself:
        list_of_dictionaries_with_series_to_analyze = support_list
        # Pick only the first 2, since test AB compares only two series
        list_of_dictionaries_with_series_to_analyze = list_of_dictionaries_with_series_to_analyze[:2]
        # Slice list until index 2, excluding index 2 (3rd element)

        print(f"Attention! Since test AB compares 2 series, only the two first series are considered here.\n")

        
    # Now that both methods of input resulted in the same format of list, we can process both
    # with the same code.
    
    # Each dictionary in list_of_dictionaries_with_series_to_analyze represents a series to
    # plot. So, the total of series to plot is:
    total_of_series = len(list_of_dictionaries_with_series_to_analyze)
    
    if (total_of_series != 2):
        
        print("There are not 2 series to compare. Please, provide valid arguments.\n")
    
    else:
                
        """
        When computing the standard deviation be sure to compute the sample one instead of the population one. 
        To accomplish this you can set the parameter ddof=1 within the np.std function. 
        This ensures that the denominator of the expression for the standard deviation is N-1 rather than N.
        """

        y1, y2 = np.array(list_of_dictionaries_with_series_to_analyze[0]['y']), np.array(list_of_dictionaries_with_series_to_analyze[1]['y'])
        lab1, lab2 = np.array(list_of_dictionaries_with_series_to_analyze[0]['label']), np.array(list_of_dictionaries_with_series_to_analyze[1]['label'])
        
        summary_dict = {'alpha': alpha}
        # Perform the t-test

        p_meaning = "p-value: probability of verifying the tested event, given that the null hypothesis H0 is correct.\n"

        if (what_to_compare == 'mean'):

            h0 = "There is no difference between the mean values obtained for each tested subgroup."
            summary_dict['comparison'] = what_to_compare
            summary_dict['h0'] = h0

            """
            Perform a hypothesis test to know if there is a significant difference between the **means** of these two segments. 
            You can do this by computing the t-statistic and using the null hypothesis that there is **not** a statistically significant 
            difference between the means of the two samples:

            $$t = \frac{(\bar{x}_{1} - \bar{x}_{2}) - (\mu_1 - \mu_2)}{\sqrt{\frac{s_{1}^2}{n_1} + \frac{s_{2}^2}{n_2}}}$$

            Notice that by computing the metric at a row level you ensure that the independence criteria is met since each row is 
            independent of one another. Also, although even if the data is not strictly normal you might have a large enough sample size 
            to justify the use of the t-test.
            """

            n1, xbar1, s1 = len(y1), np.mean(y1), np.std(y1, ddof = 1)
            n2, xbar2, s2 = len(y2), np.mean(y2), np.std(y2, ddof = 1)
            
            dict1 = {'n': n1, 'xbar': xbar1, 's': s1}
            dict2 = {'n': n2, 'xbar': xbar2, 's': s2}

            # Calculate degrees of freedom
            """
            Another important piece of information when performing a t-test is the degrees of freedom, which can be computed as follows:

            $$\text{Degrees of freedom } = \frac{\left[\frac{s_{1}^2}{n_1} + \frac{s_{2}^2}{n_2} \right]^2}{\frac{(s_{1}^2/n_1)^2}{n_1-1} + \frac{(s_{2}^2/n_2)^2}{n_2-1}}$$
            """
            
            dof = (np.square(np.square(s1)/n1 + np.square(s2)/n2))/(np.square(np.square(s1)/n1)/(n1 - 1) + np.square(np.square(s2)/n2)/(n2 - 1))
            
            summary_dict['degrees_of_freedom'] = dof

            # t-statistic difference of means
            """
            Now you have everything you need to perform the hypothesis testing. 
            Complete the `t_statistic_diff_means` which given two samples should return the t-statistic, which should be computed like this:

            $$t = \frac{(\bar{x}_{1} - \bar{x}_{2}) - (\mu_1 - \mu_2)}{\sqrt{\frac{s_{1}^2}{n_1} + \frac{s_{2}^2}{n_2}}}$$

            - The value for the difference of $(\mu_1 - \mu_2)$ should be replaced by the value of this difference under the null hypothesis.
            """
            # NULL HYPOTHESIS: the means are the same. So, mu1 - mu2 = 0

            t_statistic = (xbar1 - xbar2)/np.sqrt(np.square(s1)/n1 + np.square(s2)/n2)

            summary_dict['t_statistic'] = t_statistic

            """
            With the ability to calculate the t-statistic now you need a way to determine if you should reject (or not) the null hypothesis. 
            This function should return whether to reject (or not) the null hypothesis by using the p-value method given the value of the 
            t-statistic, the degrees of freedom and a level of significance. 
            
            **This should be a two-sided test.**

            In this case the p-value represents the probability of obtaining a value of the t-statistic as extreme (or more extreme) 
            as the observed value under the null hypothesis. You can use the fact that the `CDF` of a distribution provides the probability 
            of getting a value as extreme or less extreme than the one provided, so the p-value can be computed as `1 - CDF(current_value)`. 
            If you are conducting a two-sided test, you must use the absolute value of the current value since the "extreme" condition can 
            be attained by either side. In this case you must also multiply said probability by 2 so you can compare against $\alpha$ rather 
            than against $\frac{\alpha}{2}$.

            - You can use the `cdf` method from the [stats.t](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.t.html) class 
            to compute the p-value given the degrees of freedom. Don't forget to multiply your result by 2 since this is a two-sided test.
            
            - When passing the value of the t-statistic to the `cdf` function, you should provide the absolute value. 
            You can achieve this by using Python's built-in `abs` function.

            - If the p-value is lower to `alpha` then you should reject the null hypothesis.
            """

            reject = False
            p_value = 2*(1 - stats.t.cdf(abs(t_statistic), dof))
            
            if (p_value < alpha):
                reject = True

            summary_dict['p_value'] = p_value
            summary_dict['reject_H0'] = reject

            # Calculate confidence intervals for each group
            """
            You would like to create confidence intervals for each one of the two groups. 
            You can compute such interval for a proportion like this:
            
            Xbar +- t.s/(sqrt(n))

            - You can use the `ppf` method from the [stats.t](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.t.html) 
            class to compute the value of t

            """
            # ppf(q, df, loc=0, scale=1) - Percent point function (inverse of cdf — percentiles).
            # Example: t.ppf(0.01, df)
            # https://statcalculators.com/t-distribution-table/
            
            distance1 = (stats.t.ppf((1 - alpha/2), df = (n1 - 1)))*s1/(np.sqrt(n1))
            lower1 = xbar1 - distance1
            upper1 = xbar1 + distance1
            ci1 = np.array([lower1, upper1])

            """
            alpha = 0.05
            n1 = 12
            stats.t.ppf((1 - alpha/2), df = (n1 - 1))
            >> 2.200985160082949

            https://statcalculators.com/t-distribution-table/
            In this table, we see that this is indeed the result of the 95% confidence interval around the mean (the 2-tail test).
            That is because there is only 5% (2.5% in each tail side) out of the mean confidence interval. These 5% are limited by
            the t points in each tail.
            """
            
            distance2 = (stats.t.ppf((1 - alpha/2), df = (n2 - 1)))*s2/(np.sqrt(n2))
            lower2 = xbar2 - distance2
            upper2 = xbar2 + distance2
            ci2 = np.array([lower2, upper2])

            dict1['confidence_interval'] = ci1
            dict2['confidence_interval'] = ci2
            summary_dict[lab1] = dict1
            summary_dict[lab2] = dict2
        

        elif (what_to_compare == 'proportion'):

            h0 = "There is no difference between the proportions obtained for each tested subgroup."
            summary_dict['comparison'] = what_to_compare
            summary_dict['h0'] = h0

            """
            Perform a hypothesis test to know if there is a significant difference between the **rates (proportions)** of these two 
            segments. You can do this by computing the z-statistic:

            $$ z = \frac{\hat{p}_1 - \hat{p}_2}{\sqrt{\hat{p}(1-\hat{p})\left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}$$

            where $\hat{p}$ is the pooled proportion: $\hat{p} = \frac{x_1 + x_2}{n_1 + n_2}$
            """

            n1, x1, p1 = len(y1), np.sum(y1), np.sum(y1)/len(y1)
            n2, x2, p2 = len(y2), np.sum(y2), np.sum(y2)/len(y2)
            
            dict1 = {'n': n1, 'x': x1, 'p': p1}
            dict2 = {'n': n2, 'x': x2, 'p': p2}

            # Pooled proportion
            """
            The pooled proportiohe pooled proportion can be computed like this: 

            $\hat{p} = \frac{x_1 + x_2}{n_1 + n_2}$
            """
            
            pp = (x1 + x2)/(n1 + n2)

            summary_dict['pooled_proportion'] = pp

            #Z-statistic for different proportions
            """
            Calculate the z-statistic for the difference between proportions. Remember that this statistic can be computed like this:

            $$ z = \frac{\hat{p}_1 - \hat{p}_2}{\sqrt{\hat{p}(1-\hat{p})\left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}$$

            where $\hat{p}$ is the pooled proportion: $\hat{p} = \frac{x_1 + x_2}{n_1 + n_2}$
            """

            z_statistic = (p1 - p2)/np.sqrt(pp*(1 - pp)*(1/n1 + 1/n2))

            summary_dict['z_statistic'] = z_statistic

            """
            Decide whether to reject (or not) the null hypothesis by using the p-value method given the value of the z-statistic and 
            a level of significance. This should be a two-sided test.

            You can use the cdf method from the stats.norm class to compute the p-value. Don't forget to multiply your result by 
            2 since this is a two-sided test.
            When passing the value of the z-statistic to the cdf function, you should provide the absolute value. 
            You can achieve this by using Python's built-in abs function.
            If the p-value is lower to alpha then you should reject the null hypothesis.
            """

            reject = False
            p_value = 2*(1 - stats.norm.cdf(abs(z_statistic)))
            
            if (p_value < alpha):
                reject = True
            
            summary_dict['p_value'] = p_value
            summary_dict['reject_H0'] = reject

            # Calculate confidence intervals for each group
            """
            You would like to create confidence intervals for each one of the two groups. 
            You can compute such interval for a proportion like this:

            $$ \hat{p} \pm z_{1-\alpha/2} \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$$

            - You can use the `ppf` method from the [stats.norm](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html) 
            class to compute the value of $z$
            """

            distance1 = (stats.norm.ppf(1 - alpha/2))*np.sqrt(p1*(1 - p1)/n1)
            lower1 = p1 - distance1
            upper1 = p1 + distance1
            ci1 = np.array([lower1, upper1])
            
            distance2 = (stats.norm.ppf(1 - alpha/2))*np.sqrt(p2*(1 - p2)/n2)
            lower2 = p2 - distance2
            upper2 = p2 + distance2
            ci2 = np.array([lower2, upper2])
            
            dict1['confidence_interval'] = ci1
            dict2['confidence_interval'] = ci2
            summary_dict[lab1] = dict1
            summary_dict[lab2] = dict2

        print("Finished AB Testing. Check the full analysis on the returned summary dictionary.")
        print(f"Compared difference between {what_to_compare}.")
        print(f"Null hypothesis H0: {h0}.")
        print(p_meaning)
        print("\n")
        print(f"Calculated p-value for the test: {p_value:e} = {(p_value)*100:.2f}%")
        print("\n")

        if (reject):
            print(f"For the set significance level (alpha = {alpha:.2f}), there is no sufficient evidence to support H0.")
            print("Recommendation: REJECT the null hypothesis H0.")
        
        else:
           print(f"For the set significance level (alpha = {alpha:.2f}), there is no sufficient evidence to reject H0.")
           print("Recommendation: ACCEPT the null hypothesis H0.")
        
        return summary_dict
