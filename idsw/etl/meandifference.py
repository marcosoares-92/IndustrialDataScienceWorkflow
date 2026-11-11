import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

from idsw import (InvalidInputsError, ControlVars)


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
    
    if ControlVars.show_results:
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
    
    if ControlVars.show_results:
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
    
    list_of_quantiles = [i/100 for i in range(0, 105, 5)]
    # range(0, 105, 5): from 0 to 105 (excluding last, 105), with differences of 5 (0, 5, 10, ..., 95, 100)
    list_of_pcts = [i for i in range(0, 105, 5)]
    list_of_values = [analyzed_series.quantile(i/100) for i in range(0, 105, 5)]
    
    # Concatenate min, with the values from 5 to 95% with the maximum:
    list_of_values = [analyzed_series.min()] + [analyzed_series.quantile(i/100) for i in range(5, 100, 5)] + [analyzed_series.max()]
    list_of_interpretation = [f"minimum {column_to_analyze}"] + [f"{i}% of data <= this value" for i in range(5, 100, 5)] + [f"maximum {column_to_analyze}"]
    
    # Summarize the lists as a dataframe:
    
    quantiles_summ_df = pd.DataFrame(data = {"quantile": list_of_quantiles, 
                                            "%": list_of_pcts,
                                            column_to_analyze: list_of_values,
                                            "interpretation": list_of_interpretation})
    quantiles_summ_df.set_index(['quantile', "%", column_to_analyze], inplace = True)
    
    if ControlVars.show_results:
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
        if ControlVars.show_results:
            print(f"Minimum value of {column_to_analyze} =")
            print("%.4f" %(quantile_lim))
    
    elif (quantile_fraction == 1):
        #get the maximum value
        quantile_lim = analyzed_series.max()
        if ControlVars.show_results:
            print(f"Maximum value of {column_to_analyze} =")
            print("%.4f" %(quantile_lim))
            
    else:
        #get the quantile
        quantile_lim = analyzed_series.quantile(quantile_fraction)
        if ControlVars.show_results:
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

        if (pd.api.types.is_numeric_dtype(DATASET[new_column])):
            try:
                DATASET[new_column] = (DATASET[new_column]).astype(str)
                
            except: #simply pass
                pass
    
    # Reset index:
    DATASET = DATASET.reset_index(drop = True)
    
    if ControlVars.show_results:
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

        try:
            return math.ceil(n)
        
        except ValueError: # cannot convert float NaN to integer
            raise ValueError("Trying to convert a missing value to integer. The amount of data being tested is not sufficient.")


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

        try:
            return math.ceil(n)
        
        except ValueError: # cannot convert float NaN to integer
            raise ValueError("Trying to convert a missing value to integer. The amount of data being tested is not sufficient.")


    if ((df is not None) & (variable_to_analyze is not None)):

        # Select only the data to analyze and drop all missing values in order not to crash other subfunctions:
        X = df[variable_to_analyze]
        X = X.dropna()

    # check if a manual input was not provided:
    if (current_mean_or_proportion is None):
        # There is no manual input. Try to retrieve from the dataframe
        # Check if there is a column and a dataframe:
        
        if ((df is not None) & (variable_to_analyze is not None)):

            # Save the column as a NumPy array to manipulate it independently from the dataframe
            if (what_to_test == 'mean'):
                current_mean_or_proportion = np.mean(np.array(X))
            
            elif (what_to_test == 'proportion'):
                current_mean_or_proportion = np.sum(np.array(X))/len(np.array(X))

        else:
            raise InvalidInputsError ("Manually input a mean or proportion or add a dataframe with a column name as string to perform the analysis.")


    if (what_to_test == 'mean'):

        # Check if a standard deviation value was input
        if (current_standard_deviation is None):
        # There is no manual input. Try to retrieve from the dataframe
        # Check if there is a column and a dataframe:
        
            if ((df is not None) & (variable_to_analyze is not None)):
                # Save the column as a NumPy array to manipulate it independently from the dataframe
                current_standard_deviation = np.std(np.array(X))
                # Standard deviation will only be effectly used when the mean is tested.
            
            else:
                raise InvalidInputsError ("Manually input a standard deviation or add a dataframe with a column name as string to perform the analysis.")

        required_sample_size = sample_size_diff_means(mu1 = current_mean_or_proportion, mu2 = target_mean_or_proportion, sigma = current_standard_deviation, alpha = alpha, beta = beta, two_sided = perform_two_sided_test)
    

    elif (what_to_test == 'proportion'):

        if (target_mean_or_proportion > 1):
            raise InvalidInputsError (f"The target proportion must be input as a fraction. Not as a percent. Suggestion: input target_mean_or_proportion = {target_mean_or_proportion/100} instead of {target_mean_or_proportion}.")
    
        required_sample_size = sample_size_diff_proportions(p1 = current_mean_or_proportion, p2 = target_mean_or_proportion, alpha = alpha, beta = beta, two_sided = perform_two_sided_test)

    if ControlVars.show_results:
        print("Finished estimation. The sample size was returned as the variable 'required_sample_size'.")
        print(f"At least {required_sample_size} samples are needed to verify a modification of {what_to_test} from {current_mean_or_proportion:.2f} to {target_mean_or_proportion}.\n")

    return required_sample_size


def anova_box_violin_plot (plot_type = 'box', confidence_level_pct = 95, orientation = 'vertical', reference_value = None, data_in_same_column = False, df = None, column_with_labels_or_groups = None, variable_to_analyze = None, list_of_dictionaries_with_series_to_analyze = [{'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}], obtain_boxplot_with_filled_boxes = True, obtain_boxplot_with_notched_boxes = False, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330, non_parametric = False):
    """
    anova_box_violin_plot (plot_type = 'box', confidence_level_pct = 95, orientation = 'vertical', reference_value = None, data_in_same_column = False, df = None, column_with_labels_or_groups = None, variable_to_analyze = None, list_of_dictionaries_with_series_to_analyze = [{'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}], obtain_boxplot_with_filled_boxes = True, obtain_boxplot_with_notched_boxes = False, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330, non_parametric = False):
      
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
            
            # Convert the labels to strings:
            DATASET[column_with_labels_or_groups] = DATASET[column_with_labels_or_groups].astype(str)

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
            
            #Now, we can pass the arrays as arguments for the one-way Anova or Kruskal-Wallis:
            if non_parametric:
                kruskal_summary = stats.kruskal(*list_of_arrays)
                f_statistic = float(kruskal_summary.statistic)
                p_value = float(kruskal_summary.pvalue)
                test_name = "Kruskal-Wallis H-test"
                anova_summary_dict = {'groups_length': min_length, 'test_used': test_name, 'non_parametric': True, 'H_statistic': f_statistic, 'statistic': f_statistic, 'p_value': p_value}
                if ControlVars.show_results:
                    print(f"Non-parametric test used: {test_name}\n")
                    print(f"Total of samples in each group used (after padding): {min_length}\n")
                    print(f"Probability that the distributions/medians of the groups are the same = {100*p_value:.2f}% (p-value = {p_value:e})\n")
                    print(f"Calculated H-statistic = {f_statistic:e}\n")
            else:
                anova_one_way_summary = anova_oneway(list_of_arrays)
                f_statistic = float(anova_one_way_summary[0])
                p_value = float(anova_one_way_summary[1])
                test_name = "One-Way ANOVA (F-test)"
                anova_summary_dict = {'groups_length': min_length, 'test_used': test_name, 'non_parametric': False, 'F_statistic': f_statistic, 'statistic': f_statistic, 'p_value': p_value}
                if ControlVars.show_results:
                    print(f"Parametric test used: {test_name}\n")
                    print(f"Total of samples in each group used for ANOVA (after padding): {min_length}\n")
                    print(f"Probability that the means of the groups are the same = {100*p_value:.2f}% (p-value = {p_value:e})\n")
                    print(f"Calculated F-statistic for the variances = {f_statistic:e}\n")
                
            # start a statistics list:
            statistics_list = []
            
            if ControlVars.show_results:
                print("Statistics for each detected label:\n")
            
            # If we apply the function zip(list_of_labels, list_of_means, list_of_medians, list_of_min, list_of_max), 
            # we obtain a series of tuples. The i-th tuple contains the i-th element from list_of_labels, 
            # the i-th from list_of_means, the i-th from list_of_medians, the i-th from list_of_min, and
            # the i-th from list_of_max in this order. So, we can iterate through the 5 lists simultaneously, 
            # without declaring a counter variable by decoupling the zip:
            for label, mean, median, minimum, maximum in zip(list_of_labels, list_of_means, list_of_medians, list_of_min, list_of_max):
                
                label_dict = {'label': label, 'mean': mean, 'median': median, 'min': minimum, 'max': maximum}
                statistics_list.append(label_dict)
                
                if ControlVars.show_results:
                    print(f"Mean value of label '{label}' = {mean:e}")
                    print(f"Median value of label '{label}' = {median:e}")
                    print(f"Minimum value of label '{label}' = {minimum:e}")
                    print(f"Maximum value of label '{label}' = {maximum:e}\n")
            
            # Add the statistics list to the anova_summary_dict:
            anova_summary_dict['statistics'] = statistics_list
            
            # :e indicates the scientific notation
            if ControlVars.show_results:
                if (p_value <= alpha_anova):
                    print(f"For a confidence level of {confidence_level_pct:.2f}%, we can reject the null hypothesis.")
                    print(f"The means are different for a {confidence_level_pct:.2f}% confidence level.")

                else:
                    print(f"For a confidence level of {confidence_level_pct}%, we can accept the null hypothesis.")
                    print(f"The means are equal for a {confidence_level_pct}% confidence level.")
                

        if ((plot_type is not None) & (plot_type != 'only_anova')):

            if ControlVars.show_plots:
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
                    print (f"Figure exported as \'{new_file_path}\'. Any previous file in this root path was overwritten.")
                
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
        
        if ControlVars.show_results:
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


def AB_testing (what_to_compare = 'mean', confidence_level_pct = 95, non_parametric = False, data_in_same_column = False, df = None, column_with_labels_or_groups = None, variable_to_analyze = None, list_of_dictionaries_with_series_to_analyze = [{'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}]):

    """
    AB_testing (what_to_compare = 'mean', confidence_level_pct = 95, non_parametric = False, data_in_same_column = False, df = None, column_with_labels_or_groups = None, variable_to_analyze = None, list_of_dictionaries_with_series_to_analyze = [{'values_to_analyze': None, 'label': None}, {'values_to_analyze': None, 'label': None}]):

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
            
            raise InvalidInputsError("Please, input a valid dataframe as df.\n")
        
        elif (variable_to_analyze is None):
            
            raise InvalidInputsError("Please, input a valid column name as variable_to_analyze.\n")
        
        else:
            
            # set a local copy of the dataframe:
            DATASET = df.copy(deep = True)
            
            if (column_with_labels_or_groups is None):
            
                raise InvalidInputsError("Please, input a valid column name as column_with_labels_or_groups.\n")
            
            # Convert the labels to strings:
            DATASET[column_with_labels_or_groups] = DATASET[column_with_labels_or_groups].astype(str)
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
        
        print("There are not 2 series to compare. Please, provide valid arguments. Notice that this function compares exactly two series against each other.\n")
    
    else:
                
        """
        When computing the standard deviation be sure to compute the sample one instead of the population one. 
        To accomplish this you can set the parameter ddof=1 within the np.std function. 
        This ensures that the denominator of the expression for the standard deviation is N-1 rather than N.
        """
        # Convert to series to eliminate missing values
        series1 = pd.Series(list_of_dictionaries_with_series_to_analyze[0]['values_to_analyze'])
        series1 = series1.dropna()

        series2 = pd.Series(list_of_dictionaries_with_series_to_analyze[1]['values_to_analyze'])
        series2 = series2.dropna()

        y1, y2 = np.array(series1), np.array(series2)
        lab1, lab2 = list_of_dictionaries_with_series_to_analyze[0]['label'], list_of_dictionaries_with_series_to_analyze[1]['label']
        
        summary_dict = {'alpha': alpha}
        # Perform the t-test

        p_meaning = "p-value: probability of verifying the tested event, given that the null hypothesis H0 is correct.\n"

        if (what_to_compare == 'mean'):

            h0 = "There is no difference between the mean values obtained for each tested subgroup"
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

            if non_parametric:
                u_res = stats.mannwhitneyu(y1, y2, alternative = 'two-sided')
                u_statistic = float(u_res.statistic)
                p_value = float(u_res.pvalue)
                test_name = "Mann-Whitney U Test"
                reject = bool(p_value < alpha)
                summary_dict['test_used'] = test_name
                summary_dict['non_parametric'] = True
                summary_dict['u_statistic'] = u_statistic
                summary_dict['statistic'] = u_statistic
                summary_dict['p_value'] = p_value
                summary_dict['reject_H0'] = reject
                if ControlVars.show_results:
                    print(f"Non-parametric test used: {test_name}")
                    print(f"Mann-Whitney U statistic = {u_statistic:.4f}, p-value = {p_value:.4e}\n")
            else:
                t_statistic = (xbar1 - xbar2)/np.sqrt(np.square(s1)/n1 + np.square(s2)/n2)
                summary_dict['t_statistic'] = t_statistic
                summary_dict['statistic'] = t_statistic
                reject = False
                p_value = 2*(1 - stats.t.cdf(abs(t_statistic), dof))
                if (p_value < alpha):
                    reject = True
                summary_dict['test_used'] = "Two-Sample Independent t-Test"
                summary_dict['non_parametric'] = False
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

            h0 = "There is no difference between the proportions obtained for each tested subgroup"
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

            if non_parametric:
                table = [[int(x1), int(n1 - x1)], [int(x2), int(n2 - x2)]]
                odds_ratio, p_value = stats.fisher_exact(table, alternative = 'two-sided')
                test_name = "Fisher's Exact Test"
                reject = bool(p_value < alpha)
                summary_dict['test_used'] = test_name
                summary_dict['non_parametric'] = True
                summary_dict['odds_ratio'] = float(odds_ratio)
                summary_dict['statistic'] = float(odds_ratio)
                summary_dict['p_value'] = float(p_value)
                summary_dict['reject_H0'] = reject
                if ControlVars.show_results:
                    print(f"Non-parametric test used: {test_name}")
                    print(f"Fisher's Exact Test odds ratio = {odds_ratio:.4f}, p-value = {p_value:.4e}\n")
            else:
                z_statistic = (p1 - p2)/np.sqrt(pp*(1 - pp)*(1/n1 + 1/n2))
                summary_dict['z_statistic'] = z_statistic
                summary_dict['statistic'] = z_statistic
                reject = False
                p_value = 2*(1 - stats.norm.cdf(abs(z_statistic)))
                if (p_value < alpha):
                    reject = True
                summary_dict['test_used'] = "Two-Proportion z-Test"
                summary_dict['non_parametric'] = False
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

        if ControlVars.show_results:
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


def test_proportion_diffs (df = None, column_with_labels_or_groups = None, variable_to_analyze = None, success_label = 1, list_of_dictionaries_with_series_to_analyze = None, confidence_level_pct = 95, non_parametric = False, alternative = 'two-sided', show_plot = True, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    test_proportion_diffs (df = None, column_with_labels_or_groups = None, variable_to_analyze = None, success_label = 1, list_of_dictionaries_with_series_to_analyze = None, confidence_level_pct = 95, non_parametric = False, alternative = 'two-sided', show_plot = True, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):

    Tests for statistically significant differences in proportions (rates of success) between two or more groups.
    Supports both parametric (Two-Proportion z-Test for 2 groups, Pearson Chi-Square for >2 groups)
    and non-parametric methods (Fisher's Exact Test for 2 groups, Permutation / Randomization Chi-Square for >2 groups).
    
    : param: df: pandas DataFrame containing the dataset (optional if list_of_dictionaries_with_series_to_analyze is provided).
    : param: column_with_labels_or_groups: string, column name indicating the group/treatment label.
    : param: variable_to_analyze: string, column containing binary outcomes (e.g., 0/1, True/False, or categorical).
    : param: success_label: value considered a 'success' in variable_to_analyze (default 1).
    : param: list_of_dictionaries_with_series_to_analyze: alternative input format: list of dicts [{'values_to_analyze': series, 'label': name}, ...].
    : param: confidence_level_pct: confidence level percentage (default 95).
    : param: non_parametric: boolean (default False), whether to execute non-parametric exact/permutation tests.
    : param: alternative: string, alternative hypothesis: 'two-sided', 'larger', 'smaller' (default 'two-sided').
    : param: show_plot: boolean (default True), whether to display the proportion comparison bar plot.
    : param: x_axis_rotation: rotation angle for X-axis labels in degrees (default 0).
    : param: y_axis_rotation: rotation angle for Y-axis labels in degrees (default 0).
    : param: grid: boolean, whether to show grid lines on the plot.
    : param: export_png: boolean, whether to save the figure as a PNG file.
    : param: directory_to_save: folder path where the image will be exported.
    : param: file_name: name of the exported image file.
    : param: png_resolution_dpi: image resolution in DPI (default 330).
    : return: tuple (summary_dict, results_df).
    """

    from scipy import stats

    alpha = 1.0 - (confidence_level_pct / 100.0)

    # Extract group series
    groups = {}
    if df is not None and column_with_labels_or_groups is not None and variable_to_analyze is not None:
        if column_with_labels_or_groups not in df.columns or variable_to_analyze not in df.columns:
            raise InvalidInputsError("Specified column names not found in DataFrame.")
        DATASET = df.copy(deep = True)
        DATASET = DATASET.dropna(subset = [column_with_labels_or_groups, variable_to_analyze])
        for grp, sub_df in DATASET.groupby(column_with_labels_or_groups):
            groups[str(grp)] = (sub_df[variable_to_analyze] == success_label).astype(int).values
    elif list_of_dictionaries_with_series_to_analyze is not None:
        for item in list_of_dictionaries_with_series_to_analyze:
            if item.get('values_to_analyze') is not None:
                lbl = str(item.get('label', f"Group_{len(groups)+1}"))
                vals = pd.Series(item['values_to_analyze']).dropna()
                groups[lbl] = (vals == success_label).astype(int).values
    else:
        raise InvalidInputsError("Please provide either (df, column_with_labels_or_groups, variable_to_analyze) or list_of_dictionaries_with_series_to_analyze.")

    if len(groups) < 2:
        raise InvalidInputsError(f"At least 2 groups are required for proportion difference testing. Found {len(groups)}.")

    group_names = list(groups.keys())
    counts_success = [int(np.sum(groups[g])) for g in group_names]
    totals = [int(len(groups[g])) for g in group_names]
    proportions = [counts_success[i] / totals[i] if totals[i] > 0 else 0.0 for i in range(len(group_names))]

    # Build summary rows
    summary_rows = []
    z_crit = stats.norm.ppf(1.0 - alpha / 2.0)
    for i, g in enumerate(group_names):
        p_hat = proportions[i]
        n_i = totals[i]
        # Wilson score interval for proportions:
        denom = 1.0 + (z_crit ** 2) / n_i
        centre = (p_hat + (z_crit ** 2) / (2.0 * n_i)) / denom
        margin = (z_crit * np.sqrt((p_hat * (1.0 - p_hat) / n_i) + ((z_crit ** 2) / (4.0 * (n_i ** 2))))) / denom
        ci_lower = max(0.0, float(centre - margin))
        ci_upper = min(1.0, float(centre + margin))
        summary_rows.append({
            'Group': g,
            'Successes': counts_success[i],
            'Total': totals[i],
            'Proportion': p_hat,
            'CI_Lower': ci_lower,
            'CI_Upper': ci_upper
        })
    results_df = pd.DataFrame(summary_rows)

    summary_dict = {
        'alpha': alpha,
        'confidence_level_pct': confidence_level_pct,
        'groups': group_names,
        'proportions': proportions,
        'non_parametric': non_parametric
    }

    if len(group_names) == 2:
        # 2 groups comparison
        n1, n2 = totals[0], totals[1]
        x1, x2 = counts_success[0], counts_success[1]
        p1, p2 = proportions[0], proportions[1]
        diff = p1 - p2
        summary_dict['proportion_difference'] = float(diff)

        if non_parametric:
            test_name = "Fisher's Exact Test"
            table = [[x1, n1 - x1], [x2, n2 - x2]]
            odds_ratio, p_val = stats.fisher_exact(table, alternative = alternative)
            summary_dict['test_used'] = test_name
            summary_dict['odds_ratio'] = float(odds_ratio)
            summary_dict['statistic'] = float(odds_ratio)
            summary_dict['p_value'] = float(p_val)
            summary_dict['reject_H0'] = bool(p_val < alpha)
        else:
            test_name = "Two-Proportion z-Test"
            p_pooled = (x1 + x2) / (n1 + n2)
            se_pooled = np.sqrt(p_pooled * (1.0 - p_pooled) * (1.0 / n1 + 1.0 / n2))
            z_stat = diff / se_pooled if se_pooled > 0 else 0.0
            if alternative == 'two-sided':
                p_val = 2.0 * (1.0 - stats.norm.cdf(abs(z_stat)))
            elif alternative == 'larger':
                p_val = 1.0 - stats.norm.cdf(z_stat)
            else:
                p_val = stats.norm.cdf(z_stat)
            summary_dict['test_used'] = test_name
            summary_dict['z_statistic'] = float(z_stat)
            summary_dict['statistic'] = float(z_stat)
            summary_dict['p_value'] = float(p_val)
            summary_dict['reject_H0'] = bool(p_val < alpha)
    else:
        # Multi-group comparison (>2 groups)
        contingency_table = []
        for i in range(len(group_names)):
            contingency_table.append([counts_success[i], totals[i] - counts_success[i]])
        contingency_table = np.array(contingency_table)

        chi2_stat, p_val, dof, _ = stats.chi2_contingency(contingency_table)
        test_name = "Pearson Chi-Square Test of Homogeneity" if not non_parametric else "Chi-Square Permutation Test"
        if non_parametric:
            # Permutation approximation
            n_perms = 2000
            pooled_outcomes = np.concatenate([groups[g] for g in group_names])
            perm_stats = []
            for _ in range(n_perms):
                perm_y = np.random.permutation(pooled_outcomes)
                idx = 0
                sim_table = []
                for n_g in totals:
                    g_slice = perm_y[idx : idx + n_g]
                    sim_table.append([int(np.sum(g_slice)), int(n_g - np.sum(g_slice))])
                    idx += n_g
                sim_stat, _, _, _ = stats.chi2_contingency(sim_table)
                perm_stats.append(sim_stat)
            p_val = float(np.mean(np.array(perm_stats) >= chi2_stat))

        summary_dict['test_used'] = test_name
        summary_dict['chi2_statistic'] = float(chi2_stat)
        summary_dict['statistic'] = float(chi2_stat)
        summary_dict['degrees_of_freedom'] = int(dof)
        summary_dict['p_value'] = float(p_val)
        summary_dict['reject_H0'] = bool(p_val < alpha)

    if show_plot and ControlVars.show_plots:
        fig, ax = plt.subplots(figsize = (10, 6))
        x_pos = np.arange(len(group_names))
        err_lower = [proportions[i] - results_df['CI_Lower'].iloc[i] for i in range(len(group_names))]
        err_upper = [results_df['CI_Upper'].iloc[i] - proportions[i] for i in range(len(group_names))]
        yerr = [err_lower, err_upper]

        bars = ax.bar(x_pos, proportions, yerr = yerr, capsize = 5, color = 'steelblue', alpha = 0.85, edgecolor = 'black')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(group_names)
        ax.set_ylabel("Proportion of Success")
        ax.set_title(f"Comparison of Proportions across Groups ({summary_dict['test_used']})")
        ax.set_ylim(0, min(1.0, max(results_df['CI_Upper']) * 1.15 if len(results_df) > 0 else 1.0))
        ax.grid(grid, axis = 'y', linestyle = '--', alpha = 0.7)
        plt.xticks(rotation = x_axis_rotation)
        plt.yticks(rotation = y_axis_rotation)

        # Label proportions on top of bars
        for bar, p in zip(bars, proportions):
            height = bar.get_height()
            ax.annotate(f'{p:.2%}',
                        xy = (bar.get_x() + bar.get_width() / 2, height),
                        xytext = (0, 8),
                        textcoords = "offset points",
                        ha = 'center', va = 'bottom', fontweight = 'bold')

        if export_png:
            import os
            if directory_to_save is None:
                directory_to_save = ""
            if file_name is None:
                file_name = "proportion_difference_test"
            if png_resolution_dpi is None:
                png_resolution_dpi = 330
            new_file_path = os.path.join(directory_to_save, file_name + ".png")
            plt.savefig(new_file_path, dpi = png_resolution_dpi, transparent = False)
            if ControlVars.show_results:
                print(f"Figure exported as '{new_file_path}'. Any previous file in this root path was overwritten.")

        plt.show()

    if ControlVars.show_results:
        print(f"Proportion Difference Test: {summary_dict['test_used']}")
        print(f"Significance level: alpha = {alpha:.3f} ({confidence_level_pct}% confidence).")
        print(f"Test statistic: {summary_dict['statistic']:.4f}, p-value: {summary_dict['p_value']:.4e}")
        if summary_dict['reject_H0']:
            print("Conclusion: REJECT the null hypothesis H0. There is a statistically significant difference in proportions between groups.\n")
        else:
            print("Conclusion: ACCEPT the null hypothesis H0. There is no sufficient evidence of a difference in proportions between groups.\n")
        print("Group Breakdown:")
        try:
            from IPython.display import display
            display(results_df)
        except Exception:
            print(results_df)

    return summary_dict, results_df


def monte_carlo_simulation (simulation_function_or_equation, input_distributions, n_iterations = 10000, confidence_level_pct = 95, random_state = 42, show_plot = True, bins = 50, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    monte_carlo_simulation (simulation_function_or_equation, input_distributions, n_iterations = 10000, confidence_level_pct = 95, random_state = 42, show_plot = True, bins = 50, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):

    Conducts a general Monte Carlo simulation on an engineering, physical, or financial model/equation
    under parameter uncertainty. Supports either a callable Python function or a mathematical formula string,
    with independent stochastic input distributions. Computes key risk metrics (Value at Risk, Conditional VaR /
    Expected Shortfall), confidence intervals, percentiles, and returns simulated realizations.
    
    : param: simulation_function_or_equation: callable function accepting a dictionary/keyword arguments,
      or a mathematical formula string (e.g., "revenue - fixed_costs - variable_costs", "pressure * volume / temperature").
    : param: input_distributions: dictionary mapping parameter names to distribution tuples or scipy rv objects, e.g.:
      {'revenue': ('normal', 100000, 15000), 'fixed_costs': ('uniform', 20000, 30000), 'rate': ('beta', 2, 5)}
    : param: n_iterations: integer, number of Monte Carlo iterations (default 10000).
    : param: confidence_level_pct: confidence level percentage for interval and VaR estimation (default 95).
    : param: random_state: integer seed for reproducible random sampling (default 42).
    : param: show_plot: boolean (default True), whether to display the distribution histogram and KDE.
    : param: bins: integer, number of histogram bins (default 50).
    : param: x_axis_rotation: rotation angle for X-axis labels in degrees (default 0).
    : param: y_axis_rotation: rotation angle for Y-axis labels in degrees (default 0).
    : param: grid: boolean, whether to show grid lines on the plot.
    : param: export_png: boolean, whether to save figure as PNG file.
    : param: directory_to_save: folder path where the image will be exported.
    : param: file_name: name of the exported image file.
    : param: png_resolution_dpi: image resolution in DPI (default 330).
    : return: tuple (simulated_df, summary_dict).
    """

    from scipy import stats

    np.random.seed(random_state)
    alpha = 1.0 - (confidence_level_pct / 100.0)

    # Sample input variables
    sampled_inputs = {}
    for var_name, dist_spec in input_distributions.items():
        if callable(getattr(dist_spec, 'rvs', None)):
            sampled_inputs[var_name] = dist_spec.rvs(size = n_iterations)
        elif isinstance(dist_spec, (tuple, list)):
            dist_type = str(dist_spec[0]).lower()
            args = dist_spec[1:]
            if dist_type in ['norm', 'normal']:
                loc = args[0] if len(args) > 0 else 0.0
                scale = args[1] if len(args) > 1 else 1.0
                sampled_inputs[var_name] = np.random.normal(loc, scale, size = n_iterations)
            elif dist_type in ['uniform']:
                low = args[0] if len(args) > 0 else 0.0
                high = args[1] if len(args) > 1 else 1.0
                sampled_inputs[var_name] = np.random.uniform(low, high, size = n_iterations)
            elif dist_type in ['lognormal', 'lognorm']:
                mean = args[0] if len(args) > 0 else 0.0
                sigma = args[1] if len(args) > 1 else 1.0
                sampled_inputs[var_name] = np.random.lognormal(mean, sigma, size = n_iterations)
            elif dist_type in ['exponential', 'expon']:
                scale = args[0] if len(args) > 0 else 1.0
                sampled_inputs[var_name] = np.random.exponential(scale, size = n_iterations)
            elif dist_type in ['triangular', 'triang']:
                left, mode, right = args[0], args[1], args[2]
                sampled_inputs[var_name] = np.random.triangular(left, mode, right, size = n_iterations)
            elif dist_type in ['poisson']:
                lam = args[0] if len(args) > 0 else 1.0
                sampled_inputs[var_name] = np.random.poisson(lam, size = n_iterations)
            elif dist_type in ['beta']:
                a, b = args[0], args[1]
                sampled_inputs[var_name] = np.random.beta(a, b, size = n_iterations)
            elif dist_type in ['gamma']:
                shape, scale = args[0], args[1] if len(args) > 1 else 1.0
                sampled_inputs[var_name] = np.random.gamma(shape, scale, size = n_iterations)
            else:
                raise InvalidInputsError(f"Unsupported distribution type '{dist_type}' for variable '{var_name}'.")
        else:
            raise InvalidInputsError(f"Invalid distribution specification for variable '{var_name}'.")

    simulated_df = pd.DataFrame(sampled_inputs)

    # Evaluate equation or callable function
    if callable(simulation_function_or_equation):
        try:
            outputs = [simulation_function_or_equation({k: simulated_df[k].iloc[i] for k in simulated_df.columns}) for i in range(n_iterations)]
            simulated_df['simulation_output'] = np.array(outputs)
        except Exception:
            # Try passing DataFrame directly
            simulated_df['simulation_output'] = simulation_function_or_equation(simulated_df)
    elif isinstance(simulation_function_or_equation, str):
        try:
            simulated_df['simulation_output'] = simulated_df.eval(simulation_function_or_equation)
        except Exception as e:
            raise InvalidInputsError(f"Could not evaluate mathematical expression '{simulation_function_or_equation}': {e}")
    else:
        raise InvalidInputsError("simulation_function_or_equation must be either a callable Python function or a string expression.")

    y = simulated_df['simulation_output'].values
    mean_val = float(np.mean(y))
    std_val = float(np.std(y, ddof = 1))
    median_val = float(np.median(y))
    skew_val = float(stats.skew(y))
    kurt_val = float(stats.kurtosis(y, fisher = True))

    ci_lower = float(np.percentile(y, 100.0 * (alpha / 2.0)))
    ci_upper = float(np.percentile(y, 100.0 * (1.0 - alpha / 2.0)))

    # Risk metrics: Value at Risk (VaR) and Conditional Value at Risk (CVaR)
    var_95 = float(np.percentile(y, 5.0))
    cvar_95 = float(np.mean(y[y <= var_95])) if np.any(y <= var_95) else var_95
    var_99 = float(np.percentile(y, 1.0))
    cvar_99 = float(np.mean(y[y <= var_99])) if np.any(y <= var_99) else var_99

    summary_dict = {
        'n_iterations': n_iterations,
        'mean': mean_val,
        'standard_deviation': std_val,
        'median': median_val,
        'minimum': float(np.min(y)),
        'maximum': float(np.max(y)),
        'skewness': skew_val,
        'kurtosis': kurt_val,
        'confidence_level_pct': confidence_level_pct,
        'confidence_interval': (ci_lower, ci_upper),
        'percentiles': {
            '1%': var_99,
            '5%': var_95,
            '25%': float(np.percentile(y, 25.0)),
            '50%': median_val,
            '75%': float(np.percentile(y, 75.0)),
            '95%': float(np.percentile(y, 95.0)),
            '99%': float(np.percentile(y, 99.0))
        },
        'VaR_95': var_95,
        'CVaR_95': cvar_95,
        'VaR_99': var_99,
        'CVaR_99': cvar_99
    }

    if show_plot and ControlVars.show_plots:
        fig, ax = plt.subplots(figsize = (12, 7))
        sns.histplot(y, bins = bins, kde = True, color = 'steelblue', stat = 'density', alpha = 0.6, ax = ax)
        ax.axvline(mean_val, color = 'darkred', linestyle = '--', linewidth = 2, label = f'Mean ({mean_val:.2f})')
        ax.axvline(median_val, color = 'forestgreen', linestyle = ':', linewidth = 2, label = f'Median ({median_val:.2f})')
        ax.axvline(ci_lower, color = 'black', linestyle = '-.', linewidth = 1.5, label = f'{confidence_level_pct}% CI Lower ({ci_lower:.2f})')
        ax.axvline(ci_upper, color = 'black', linestyle = '-.', linewidth = 1.5, label = f'{confidence_level_pct}% CI Upper ({ci_upper:.2f})')
        ax.axvline(var_95, color = 'darkorange', linestyle = '-', linewidth = 2, label = f'VaR 95% ({var_95:.2f})')

        ax.set_title(f"Monte Carlo Simulation Distribution ({n_iterations:,} Iterations)")
        ax.set_xlabel("Simulated Outcome")
        ax.set_ylabel("Probability Density")
        ax.legend(loc = 'best')
        ax.grid(grid, linestyle = '--', alpha = 0.7)
        plt.xticks(rotation = x_axis_rotation)
        plt.yticks(rotation = y_axis_rotation)

        if export_png:
            import os
            if directory_to_save is None:
                directory_to_save = ""
            if file_name is None:
                file_name = "monte_carlo_simulation"
            if png_resolution_dpi is None:
                png_resolution_dpi = 330
            new_file_path = os.path.join(directory_to_save, file_name + ".png")
            plt.savefig(new_file_path, dpi = png_resolution_dpi, transparent = False)
            if ControlVars.show_results:
                print(f"Figure exported as '{new_file_path}'. Any previous file in this root path was overwritten.")

        plt.show()

    if ControlVars.show_results:
        print(f"Monte Carlo Simulation Completed ({n_iterations:,} Iterations):\n")
        print(f"Mean Outcome: {mean_val:.4f} | Std Dev: {std_val:.4f} | Median: {median_val:.4f}")
        print(f"{confidence_level_pct}% Empirical Confidence Interval: [{ci_lower:.4f}, {ci_upper:.4f}]")
        print(f"Value at Risk (VaR 95%): {var_95:.4f} | Conditional VaR (CVaR 95%): {cvar_95:.4f}")
        print(f"Skewness: {skew_val:.4f} | Kurtosis: {kurt_val:.4f}\n")

    return simulated_df, summary_dict


def generate_sampling_distribution (df, column_to_analyze, statistic = 'mean', quantile_p = 0.5, sample_size = None, n_replications = 2000, sampling_method = 'bootstrap', strata_column = None, confidence_level_pct = 95, random_state = 42, show_plot = True, bins = 40, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    generate_sampling_distribution (df, column_to_analyze, statistic = 'mean', quantile_p = 0.5, sample_size = None, n_replications = 2000, sampling_method = 'bootstrap', strata_column = None, confidence_level_pct = 95, random_state = 42, show_plot = True, bins = 40, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):

    Generates sampling and bootstrap distributions to analyze statistical estimation properties,
    demonstrate the Central Limit Theorem (CLT), quantify sampling variability, compute empirical standard errors,
    and construct bootstrap confidence intervals.
    
    : param: df: pandas DataFrame containing the population or sample data.
    : param: column_to_analyze: string, column name to analyze.
    : param: statistic: string, statistic to estimate: 'mean', 'median', 'std', 'var', 'quantile' (default 'mean').
    : param: quantile_p: float between 0 and 1 (default 0.5), used when statistic == 'quantile'.
    : param: sample_size: integer, size of each sampled subgroup (defaults to len(df) for bootstrap).
    : param: n_replications: integer, number of resamples to draw (default 2000).
    : param: sampling_method: string, 'bootstrap' (with replacement), 'simple_random' (without replacement), or 'stratified'.
    : param: strata_column: string (optional), column used for stratification when sampling_method == 'stratified'.
    : param: confidence_level_pct: confidence level percentage (default 95).
    : param: random_state: integer seed for random generator (default 42).
    : param: show_plot: boolean, whether to display the sampling distribution plot.
    : param: bins: integer, number of histogram bins (default 40).
    : param: x_axis_rotation: rotation angle for X-axis labels in degrees (default 0).
    : param: y_axis_rotation: rotation angle for Y-axis labels in degrees (default 0).
    : param: grid: boolean, whether to show grid on the plot.
    : param: export_png: boolean, whether to save figure as PNG file.
    : param: directory_to_save: folder path where the image will be exported.
    : param: file_name: name of the exported image file.
    : param: png_resolution_dpi: image resolution in DPI (default 330).
    : return: tuple (sampling_distribution_series, summary_dict).
    """

    from scipy import stats

    if not isinstance(df, pd.DataFrame):
        raise InvalidInputsError("df must be a valid pandas DataFrame.")

    if column_to_analyze not in df.columns:
        raise InvalidInputsError(f"column_to_analyze '{column_to_analyze}' was not found in DataFrame.")

    np.random.seed(random_state)
    alpha = 1.0 - (confidence_level_pct / 100.0)
    data = df[column_to_analyze].dropna()
    N = len(data)

    if sample_size is None:
        sample_size = N if sampling_method == 'bootstrap' else max(10, int(0.5 * N))

    if sampling_method == 'simple_random' and sample_size > N:
        raise InvalidInputsError("sample_size cannot exceed population size for sampling without replacement.")

    # Helper function to compute statistic
    def compute_stat(vals):
        if statistic == 'mean':
            return float(np.mean(vals))
        elif statistic == 'median':
            return float(np.median(vals))
        elif statistic == 'std':
            return float(np.std(vals, ddof = 1))
        elif statistic == 'var':
            return float(np.var(vals, ddof = 1))
        elif statistic == 'quantile':
            return float(np.percentile(vals, 100.0 * quantile_p))
        else:
            raise InvalidInputsError(f"Unsupported statistic '{statistic}'. Choose from 'mean', 'median', 'std', 'var', 'quantile'.")

    observed_stat = compute_stat(data.values)
    replicated_stats = []

    if sampling_method == 'bootstrap':
        for _ in range(n_replications):
            resample = np.random.choice(data.values, size = sample_size, replace = True)
            replicated_stats.append(compute_stat(resample))
    elif sampling_method == 'simple_random':
        for _ in range(n_replications):
            resample = np.random.choice(data.values, size = sample_size, replace = False)
            replicated_stats.append(compute_stat(resample))
    elif sampling_method == 'stratified':
        if strata_column is None or strata_column not in df.columns:
            raise InvalidInputsError("strata_column must be provided and present in df for stratified sampling.")
        clean_df = df.dropna(subset = [column_to_analyze, strata_column])
        strata_weights = clean_df[strata_column].value_counts(normalize = True)
        for _ in range(n_replications):
            sampled_parts = []
            for stratum, weight in strata_weights.items():
                stratum_data = clean_df[clean_df[strata_column] == stratum][column_to_analyze].values
                n_stratum = max(1, int(round(sample_size * weight)))
                sampled_parts.extend(np.random.choice(stratum_data, size = n_stratum, replace = True))
            replicated_stats.append(compute_stat(sampled_parts[:sample_size]))
    else:
        raise InvalidInputsError("sampling_method must be one of 'bootstrap', 'simple_random', or 'stratified'.")

    replicated_stats = np.array(replicated_stats)
    mean_stat = float(np.mean(replicated_stats))
    se_empirical = float(np.std(replicated_stats, ddof = 1))

    # Analytical SE for mean (Central Limit Theorem)
    se_analytical = float(np.std(data.values, ddof = 1) / np.sqrt(sample_size)) if statistic == 'mean' else None

    # Percentile confidence interval
    ci_lower = float(np.percentile(replicated_stats, 100.0 * (alpha / 2.0)))
    ci_upper = float(np.percentile(replicated_stats, 100.0 * (1.0 - alpha / 2.0)))

    summary_dict = {
        'statistic': statistic,
        'observed_statistic': observed_stat,
        'sampling_mean': mean_stat,
        'standard_error_empirical': se_empirical,
        'standard_error_analytical': se_analytical,
        'sampling_method': sampling_method,
        'sample_size': sample_size,
        'n_replications': n_replications,
        'confidence_level_pct': confidence_level_pct,
        'confidence_interval': (ci_lower, ci_upper)
    }

    if show_plot and ControlVars.show_plots:
        fig, ax = plt.subplots(figsize = (11, 6))
        sns.histplot(replicated_stats, bins = bins, kde = True, color = 'darkcyan', stat = 'density', alpha = 0.6, ax = ax)
        ax.axvline(observed_stat, color = 'darkred', linestyle = '--', linewidth = 2, label = f'Observed ({observed_stat:.3f})')
        ax.axvline(ci_lower, color = 'black', linestyle = ':', linewidth = 1.5, label = f'{confidence_level_pct}% CI Lower ({ci_lower:.3f})')
        ax.axvline(ci_upper, color = 'black', linestyle = ':', linewidth = 1.5, label = f'{confidence_level_pct}% CI Upper ({ci_upper:.3f})')
        ax.set_title(f"Sampling Distribution of {statistic.title()} ({sampling_method.title()}, n={sample_size}, reps={n_replications:,})")
        ax.set_xlabel(f"Sample {statistic.title()}")
        ax.set_ylabel("Density")
        ax.legend(loc = 'best')
        ax.grid(grid, linestyle = '--', alpha = 0.7)
        plt.xticks(rotation = x_axis_rotation)
        plt.yticks(rotation = y_axis_rotation)

        if export_png:
            import os
            if directory_to_save is None:
                directory_to_save = ""
            if file_name is None:
                file_name = f"sampling_distribution_{column_to_analyze}_{statistic}"
            if png_resolution_dpi is None:
                png_resolution_dpi = 330
            new_file_path = os.path.join(directory_to_save, file_name + ".png")
            plt.savefig(new_file_path, dpi = png_resolution_dpi, transparent = False)
            if ControlVars.show_results:
                print(f"Figure exported as '{new_file_path}'. Any previous file in this root path was overwritten.")

        plt.show()

    if ControlVars.show_results:
        print(f"Sampling Distribution Analysis ({sampling_method.title()}, {n_replications:,} replications):")
        print(f"Observed {statistic}: {observed_stat:.4f} | Mean of Sampling Distribution: {mean_stat:.4f}")
        print(f"Empirical Standard Error (SE): {se_empirical:.4f}")
        if se_analytical is not None:
            print(f"Analytical Standard Error (CLT: s / sqrt(n)): {se_analytical:.4f}")
        print(f"{confidence_level_pct}% Bootstrap Confidence Interval: [{ci_lower:.4f}, {ci_upper:.4f}]\n")

    return pd.Series(replicated_stats, name = f'{statistic}_sampling_distribution'), summary_dict


def bayesian_inference_analysis (model_type = 'beta_binomial', prior_alpha = 1.0, prior_beta = 1.0, prior_mean = 0.0, prior_variance = 1.0, data = None, successes = None, trials = None, likelihood_variance = None, confidence_level_pct = 95, show_plot = True, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    bayesian_inference_analysis (model_type = 'beta_binomial', prior_alpha = 1.0, prior_beta = 1.0, prior_mean = 0.0, prior_variance = 1.0, data = None, successes = None, trials = None, likelihood_variance = None, confidence_level_pct = 95, show_plot = True, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):

    Performs Bayesian inference and evidence updating using exact conjugate families:
    1. Beta-Binomial Conjugate Model: for conversion rates, failure rates, and proportions.
    2. Normal-Normal Conjugate Model: for continuous mean values under known or sample variance.
    Computes prior, likelihood, and posterior distributions, posterior point estimates (mean, mode, variance),
    and exact credible intervals.
    
    : param: model_type: string, 'beta_binomial' (for proportions/rates) or 'normal_normal' (for continuous means).
    : param: prior_alpha: float (default 1.0), alpha shape parameter for Beta prior (default uniform prior Beta(1,1)).
    : param: prior_beta: float (default 1.0), beta shape parameter for Beta prior.
    : param: prior_mean: float (default 0.0), prior mean for Normal prior.
    : param: prior_variance: float (default 1.0), prior variance for Normal prior.
    : param: data: array-like (optional), observed sample data.
    : param: successes: integer (optional), number of observed successes (for Beta-Binomial).
    : param: trials: integer (optional), total number of trials (for Beta-Binomial).
    : param: likelihood_variance: float (optional), known variance of data for Normal-Normal model (defaults to sample variance).
    : param: confidence_level_pct: credible interval percentage (default 95).
    : param: show_plot: boolean, whether to display the Prior vs Likelihood vs Posterior plot.
    : param: x_axis_rotation: rotation angle for X-axis labels in degrees (default 0).
    : param: y_axis_rotation: rotation angle for Y-axis labels in degrees (default 0).
    : param: grid: boolean, whether to show grid on the plot.
    : param: export_png: boolean, whether to save figure as PNG file.
    : param: directory_to_save: folder path where the image will be exported.
    : param: file_name: name of the exported image file.
    : param: png_resolution_dpi: image resolution in DPI (default 330).
    : return: tuple (posterior_summary_dict, plot_data_df).
    """

    from scipy import stats

    alpha_level = 1.0 - (confidence_level_pct / 100.0)

    if model_type == 'beta_binomial':
        # Derive successes and trials
        if data is not None:
            clean_data = pd.Series(data).dropna().values
            k = int(np.sum(clean_data == 1))
            n = int(len(clean_data))
        elif successes is not None and trials is not None:
            k = int(successes)
            n = int(trials)
        else:
            raise InvalidInputsError("For beta_binomial model, provide either data (binary array) or successes and trials.")

        post_alpha = prior_alpha + k
        post_beta = prior_beta + (n - k)

        post_mean = post_alpha / (post_alpha + post_beta)
        if post_alpha > 1 and post_beta > 1:
            post_mode = (post_alpha - 1.0) / (post_alpha + post_beta - 2.0)
        else:
            post_mode = post_mean
        post_var = (post_alpha * post_beta) / (((post_alpha + post_beta) ** 2) * (post_alpha + post_beta + 1.0))
        post_std = np.sqrt(post_var)

        ci_lower = float(stats.beta.ppf(alpha_level / 2.0, post_alpha, post_beta))
        ci_upper = float(stats.beta.ppf(1.0 - alpha_level / 2.0, post_alpha, post_beta))

        theta = np.linspace(0.001, 0.999, 500)
        prior_pdf = stats.beta.pdf(theta, prior_alpha, prior_beta)
        post_pdf = stats.beta.pdf(theta, post_alpha, post_beta)
        # Likelihood scaled to match density scale:
        lik_pdf = stats.binom.pmf(k, n, theta)
        lik_scaled = lik_pdf * (np.max(post_pdf) / (np.max(lik_pdf) if np.max(lik_pdf) > 0 else 1.0))

        plot_df = pd.DataFrame({
            'theta': theta,
            'Prior_PDF': prior_pdf,
            'Likelihood_Normalized': lik_scaled,
            'Posterior_PDF': post_pdf
        })

        summary_dict = {
            'model_type': 'beta_binomial',
            'prior_parameters': {'alpha': prior_alpha, 'beta': prior_beta},
            'observed_evidence': {'successes': k, 'trials': n, 'sample_rate': k / n if n > 0 else 0.0},
            'posterior_parameters': {'alpha': post_alpha, 'beta': post_beta},
            'posterior_mean': float(post_mean),
            'posterior_mode': float(post_mode),
            'posterior_variance': float(post_var),
            'posterior_std': float(post_std),
            'credible_interval_pct': confidence_level_pct,
            'credible_interval': (ci_lower, ci_upper)
        }

        xlabel_title = "Proportion / Success Probability (theta)"
        plot_title_str = f"Beta-Binomial Bayesian Updating (Successes={k}, Trials={n})"

    elif model_type == 'normal_normal':
        if data is None:
            raise InvalidInputsError("For normal_normal model, please provide observed data.")
        clean_data = pd.Series(data).dropna().values.astype(float)
        n = len(clean_data)
        if n == 0:
            raise InvalidInputsError("data contains no valid observations.")

        x_bar = float(np.mean(clean_data))
        sigma2 = float(likelihood_variance) if likelihood_variance is not None else float(np.var(clean_data, ddof = 1)) if n > 1 else 1.0

        # Normal-Normal conjugate update:
        # Precision tau = 1 / variance
        tau_0 = 1.0 / prior_variance
        tau_data = n / sigma2
        tau_post = tau_0 + tau_data

        post_var = 1.0 / tau_post
        post_std = np.sqrt(post_var)
        post_mean = (tau_0 * prior_mean + tau_data * x_bar) / tau_post
        post_mode = post_mean

        ci_lower = float(stats.norm.ppf(alpha_level / 2.0, loc = post_mean, scale = post_std))
        ci_upper = float(stats.norm.ppf(1.0 - alpha_level / 2.0, loc = post_mean, scale = post_std))

        spread = max(3.0 * np.sqrt(prior_variance), 3.0 * post_std, 3.0 * np.sqrt(sigma2 / n))
        x_grid = np.linspace(min(prior_mean, post_mean, x_bar) - spread, max(prior_mean, post_mean, x_bar) + spread, 500)
        prior_pdf = stats.norm.pdf(x_grid, loc = prior_mean, scale = np.sqrt(prior_variance))
        post_pdf = stats.norm.pdf(x_grid, loc = post_mean, scale = post_std)
        lik_pdf = stats.norm.pdf(x_grid, loc = x_bar, scale = np.sqrt(sigma2 / n))

        plot_df = pd.DataFrame({
            'mu': x_grid,
            'Prior_PDF': prior_pdf,
            'Likelihood_Normalized': lik_pdf,
            'Posterior_PDF': post_pdf
        })

        summary_dict = {
            'model_type': 'normal_normal',
            'prior_parameters': {'mean': prior_mean, 'variance': prior_variance},
            'observed_evidence': {'n_samples': n, 'sample_mean': x_bar, 'sample_variance': sigma2},
            'posterior_parameters': {'mean': float(post_mean), 'variance': float(post_var), 'std': float(post_std)},
            'posterior_mean': float(post_mean),
            'posterior_mode': float(post_mode),
            'posterior_variance': float(post_var),
            'posterior_std': float(post_std),
            'credible_interval_pct': confidence_level_pct,
            'credible_interval': (ci_lower, ci_upper)
        }

        xlabel_title = "Parameter Mean (mu)"
        plot_title_str = f"Normal-Normal Bayesian Updating (n={n}, Sample Mean={x_bar:.2f})"

    else:
        raise InvalidInputsError("model_type must be either 'beta_binomial' or 'normal_normal'.")

    if show_plot and ControlVars.show_plots:
        fig, ax = plt.subplots(figsize = (11, 6))
        x_col = plot_df.columns[0]
        ax.plot(plot_df[x_col], plot_df['Prior_PDF'], 'k--', linewidth = 1.8, label = 'Prior Distribution')
        ax.plot(plot_df[x_col], plot_df['Likelihood_Normalized'], 'g:', linewidth = 2.0, label = 'Likelihood (Normalized)')
        ax.plot(plot_df[x_col], plot_df['Posterior_PDF'], 'b-', linewidth = 2.5, label = 'Posterior Distribution')

        ax.axvline(post_mean, color = 'darkred', linestyle = '-.', label = f'Posterior Mean ({post_mean:.3f})')
        ax.fill_between(plot_df[x_col], 0, plot_df['Posterior_PDF'],
                        where = (plot_df[x_col] >= ci_lower) & (plot_df[x_col] <= ci_upper),
                        color = 'blue', alpha = 0.2, label = f'{confidence_level_pct}% Credible Interval')

        ax.set_title(plot_title_str)
        ax.set_xlabel(xlabel_title)
        ax.set_ylabel("Probability Density")
        ax.legend(loc = 'best')
        ax.grid(grid, linestyle = '--', alpha = 0.7)
        plt.xticks(rotation = x_axis_rotation)
        plt.yticks(rotation = y_axis_rotation)

        if export_png:
            import os
            if directory_to_save is None:
                directory_to_save = ""
            if file_name is None:
                file_name = f"bayesian_inference_{model_type}"
            if png_resolution_dpi is None:
                png_resolution_dpi = 330
            new_file_path = os.path.join(directory_to_save, file_name + ".png")
            plt.savefig(new_file_path, dpi = png_resolution_dpi, transparent = False)
            if ControlVars.show_results:
                print(f"Figure exported as '{new_file_path}'. Any previous file in this root path was overwritten.")

        plt.show()

    if ControlVars.show_results:
        print(f"Bayesian Analysis Completed ({model_type}):")
        print(f"Posterior Mean: {post_mean:.4f} | Posterior Std: {post_std:.4f} | Posterior Mode: {post_mode:.4f}")
        print(f"{confidence_level_pct}% Credible Interval: [{ci_lower:.4f}, {ci_upper:.4f}]\n")

    return summary_dict, plot_df


def generate_and_fit_distribution (distribution_name = 'normal', distribution_params = None, sample_size = 1000, fit_distribution = True, random_state = 42, show_plot = True, bins = 40, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    generate_and_fit_distribution (distribution_name = 'normal', distribution_params = None, sample_size = 1000, fit_distribution = True, random_state = 42, show_plot = True, bins = 40, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):

    Generates synthetic industrial / sensor data following a specified theoretical probability distribution,
    fits distribution parameters back to the generated sample, evaluates goodness of fit, and compares the
    empirical Kernel Density Estimation (KDE) directly against the theoretical Probability Density Function (PDF).
    
    : param: distribution_name: string, distribution to simulate and fit: 'normal', 'lognormal', 'exponential',
      'gamma', 'weibull', 'uniform', 'poisson', 'beta' (default 'normal').
    : param: distribution_params: dict or tuple of parameters for the distribution (e.g., {'loc': 50, 'scale': 5}).
    : param: sample_size: integer, number of samples to generate (default 1000).
    : param: fit_distribution: boolean, whether to fit the distribution back to the generated data.
    : param: random_state: integer seed for random generator (default 42).
    : param: show_plot: boolean, whether to show comparison plot between KDE and theoretical PDF.
    : param: bins: integer, number of histogram bins (default 40).
    : param: x_axis_rotation: rotation angle for X-axis labels in degrees (default 0).
    : param: y_axis_rotation: rotation angle for Y-axis labels in degrees (default 0).
    : param: grid: boolean, whether to show grid on the plot.
    : param: export_png: boolean, whether to save figure as PNG file.
    : param: directory_to_save: folder path where the image will be exported.
    : param: file_name: name of the exported image file.
    : param: png_resolution_dpi: image resolution in DPI (default 330).
    : return: tuple (generated_df, fit_summary_dict).
    """

    from scipy import stats

    np.random.seed(random_state)
    dist_clean = str(distribution_name).strip().lower()

    if distribution_params is None:
        distribution_params = {}

    # Sample generation
    if dist_clean in ['normal', 'norm']:
        loc = distribution_params.get('loc', 0.0)
        scale = distribution_params.get('scale', 1.0)
        data = np.random.normal(loc, scale, size = sample_size)
        dist_obj = stats.norm
    elif dist_clean in ['lognormal', 'lognorm']:
        s = distribution_params.get('s', distribution_params.get('sigma', 0.5))
        scale = distribution_params.get('scale', np.exp(distribution_params.get('mean', 1.0)))
        loc = distribution_params.get('loc', 0.0)
        data = stats.lognorm.rvs(s, loc = loc, scale = scale, size = sample_size, random_state = random_state)
        dist_obj = stats.lognorm
    elif dist_clean in ['exponential', 'expon']:
        scale = distribution_params.get('scale', 1.0)
        loc = distribution_params.get('loc', 0.0)
        data = np.random.exponential(scale, size = sample_size) + loc
        dist_obj = stats.expon
    elif dist_clean in ['gamma']:
        a = distribution_params.get('a', distribution_params.get('shape', 2.0))
        scale = distribution_params.get('scale', 1.0)
        loc = distribution_params.get('loc', 0.0)
        data = stats.gamma.rvs(a, loc = loc, scale = scale, size = sample_size, random_state = random_state)
        dist_obj = stats.gamma
    elif dist_clean in ['weibull', 'weibull_min']:
        c = distribution_params.get('c', distribution_params.get('shape', 1.5))
        scale = distribution_params.get('scale', 1.0)
        loc = distribution_params.get('loc', 0.0)
        data = stats.weibull_min.rvs(c, loc = loc, scale = scale, size = sample_size, random_state = random_state)
        dist_obj = stats.weibull_min
    elif dist_clean in ['uniform']:
        low = distribution_params.get('low', 0.0)
        high = distribution_params.get('high', 10.0)
        data = np.random.uniform(low, high, size = sample_size)
        dist_obj = stats.uniform
    elif dist_clean in ['poisson']:
        lam = distribution_params.get('lam', distribution_params.get('mu', 5.0))
        data = np.random.poisson(lam, size = sample_size)
        dist_obj = stats.poisson
    elif dist_clean in ['beta']:
        a = distribution_params.get('a', 2.0)
        b = distribution_params.get('b', 5.0)
        data = stats.beta.rvs(a, b, size = sample_size, random_state = random_state)
        dist_obj = stats.beta
    else:
        raise InvalidInputsError(f"Unsupported distribution_name '{distribution_name}'. Choose from 'normal', 'lognormal', 'exponential', 'gamma', 'weibull', 'uniform', 'poisson', 'beta'.")

    generated_df = pd.DataFrame({'generated_values': data})

    fit_summary_dict = {
        'distribution': distribution_name,
        'sample_size': sample_size,
        'sample_mean': float(np.mean(data)),
        'sample_std': float(np.std(data, ddof = 1)),
        'sample_median': float(np.median(data)),
        'sample_skewness': float(stats.skew(data)),
        'sample_kurtosis': float(stats.kurtosis(data, fisher = True))
    }

    fitted_params = None
    ks_stat, ks_pval = None, None
    if fit_distribution:
        if dist_clean == 'poisson':
            fit_mu = float(np.mean(data))
            fitted_params = (fit_mu,)
            fit_summary_dict['fitted_parameters'] = fitted_params
        else:
            fitted_params = dist_obj.fit(data)
            fit_summary_dict['fitted_parameters'] = fitted_params
            try:
                ks_res = stats.kstest(data, dist_obj.cdf, args = fitted_params)
                ks_stat = float(ks_res.statistic)
                ks_pval = float(ks_res.pvalue)
                fit_summary_dict['KS_statistic'] = ks_stat
                fit_summary_dict['KS_p_value'] = ks_pval
            except Exception:
                pass

    if show_plot and ControlVars.show_plots:
        fig, ax = plt.subplots(figsize = (11, 6))
        sns.histplot(data, bins = bins, stat = 'density', color = 'lightsteelblue', edgecolor = 'black', alpha = 0.5, label = 'Histogram', ax = ax)
        sns.kdeplot(data, color = 'darkblue', linewidth = 2.5, label = 'Empirical KDE', ax = ax)

        if fitted_params is not None and dist_clean != 'poisson':
            x_range = np.linspace(min(data), max(data), 400)
            pdf_theoretical = dist_obj.pdf(x_range, *fitted_params)
            ax.plot(x_range, pdf_theoretical, color = 'crimson', linestyle = '--', linewidth = 2, label = f'Theoretical Fit ({distribution_name})')

        ax.set_title(f"Empirical KDE vs Theoretical PDF for {distribution_name.title()} (n={sample_size:,})")
        ax.set_xlabel("Value")
        ax.set_ylabel("Density")
        ax.legend(loc = 'best')
        ax.grid(grid, linestyle = '--', alpha = 0.7)
        plt.xticks(rotation = x_axis_rotation)
        plt.yticks(rotation = y_axis_rotation)

        if export_png:
            import os
            if directory_to_save is None:
                directory_to_save = ""
            if file_name is None:
                file_name = f"distribution_fit_kde_{distribution_name}"
            if png_resolution_dpi is None:
                png_resolution_dpi = 330
            new_file_path = os.path.join(directory_to_save, file_name + ".png")
            plt.savefig(new_file_path, dpi = png_resolution_dpi, transparent = False)
            if ControlVars.show_results:
                print(f"Figure exported as '{new_file_path}'. Any previous file in this root path was overwritten.")

        plt.show()

    if ControlVars.show_results:
        print(f"Generated {sample_size:,} samples following '{distribution_name}' distribution.")
        print(f"Sample Mean: {fit_summary_dict['sample_mean']:.4f} | Std: {fit_summary_dict['sample_std']:.4f} | Median: {fit_summary_dict['sample_median']:.4f}")
        if fitted_params is not None:
            print(f"Fitted distribution parameters: {fitted_params}")
            if ks_pval is not None:
                print(f"Kolmogorov-Smirnov goodness of fit: stat = {ks_stat:.4f}, p-value = {ks_pval:.4f}\n")

    return generated_df, fit_summary_dict

