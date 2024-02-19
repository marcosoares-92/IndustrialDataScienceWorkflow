import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from idsw import (InvalidInputsError, ControlVars)
from .core import (SPCChartAssistant, SPCPlot, CapabilityAnalysis)


def statistical_process_control_chart (df, column_with_variable_to_be_analyzed, timestamp_tag_column = None, column_with_labels_or_subgroups = None, column_with_event_frame_indication = None, specification_limits = {'lower_spec_lim': None, 'upper_spec_lim': None}, reference_value = None, use_spc_chart_assistant = False, chart_to_use = 'std_error', consider_skewed_dist_when_estimating_with_std = False, rare_event_indication = None, rare_event_timedelta_unit = 'day', x_axis_rotation = 70, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    statistical_process_control_chart (df, column_with_variable_to_be_analyzed, timestamp_tag_column = None, column_with_labels_or_subgroups = None, column_with_event_frame_indication = None, specification_limits = {'lower_spec_lim': None, 'upper_spec_lim': None}, reference_value = None, use_spc_chart_assistant = False, chart_to_use = 'std_error', consider_skewed_dist_when_estimating_with_std = False, rare_event_indication = None, rare_event_timedelta_unit = 'day', x_axis_rotation = 70, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):

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
    
    : param: df: dataframe to be analyzed.
    
    : param: TIMESTAMP_TAG_COLUMN: name (header) of the column containing the timestamps or the numeric scale
      used to represent time (column with floats or integers). The column name may be a string or a number.
      e.g. TIMESTAMP_TAG_COLUMN = 'date' will use the values from column 'date'
      Keep TIMESTAMP_TAG_COLUMN = None if the dataframe do not contain timestamps, so the index will be
      used.

    : param: COLUMN_WITH_VARIABLE_TO_BE_ANALYZED: name (header) of the column containing the variable
      which stability will be analyzed by the control chart. The column name may be a string or a number.
      Example: COLUMN_WITH_VARIABLE_TO_BE_ANALYZED = 'analyzed_column' will analyze a column named
      "analyzed_column", whereas COLUMN_WITH_VARIABLE_TO_BE_ANALYZED = 'col1' will evaluate column 'col1'.

    : param: COLUMN_WITH_LABELS_OR_SUBGROUPS: name (header) of the column containing the variable
      indicating the subgroups or label indication which will be used for grouping the samples. 
      Example: Suppose you want to analyze the means for 4 different subgroups: 1, 2, 3, 4. For each subgroup,
      4 or 5 samples of data (the values in COLUMN_WITH_VARIABLE_TO_BE_ANALYZED) are collected, and you
      want the average and standard deviation within the subgroups. Them, you create a column named
      'label' and store the values: 1 for samples correspondent to subgroup 1; 2 for samples from
      subgroup 2,... etc. In this case, COLUMN_WITH_LABELS_OR_SUBGROUPS = 'label'
      Notice that the samples do not need to be collected in order. The function will automatically separate
      the entries according to the subgroups. So, the entries in the dataset may be in an arbitrary order
      like: 1, 1, 2, 1, 4, 3, etc.
      The values in the COLUMN_WITH_LABELS_OR_SUBGROUPS may be strings (text) or numeric values (like
      integers), but different values will be interpreted as different subgroups.
      As an example of text, you could have a column named 'col1' with group identifications as: 
      'A', 'B', 'C', 'D', and COLUMN_WITH_LABELS_OR_SUBGROUPS = 'col1'.
      Notice the difference between COLUMN_WITH_LABELS_OR_SUBGROUPS and COLUMN_WITH_VARIABLE_TO_BE_ANALYZED:
    
    : param: COLUMN_WITH_VARIABLE_TO_BE_ANALYZED accepts only numeric values, so the binary variables must be
      converted to integers 0 and 1 before the analysis. The COLUMN_WITH_LABELS_OR_SUBGROUPS, in turns,
      accept both numeric and text (string) values.
    
    : param: COLUMN_WITH_EVENT_FRAME_INDICATION: name (header) of the column containing the variable
      indicating the stages, time windows, or event frames. The central line and the limits of natural
      variation will be independently calculated for each event frame. The indication of an event frame
      may be textual (string) or numeric. 
      For example: suppose you have a column named 'event_frames'. For half of the entries, event_frame = 
      'A'; and for the second half, event_frame = 'B'. If COLUMN_WITH_EVENT_FRAME_INDICATION = 'event_frame',
      the dataframe will be divided into two subsets: 'A', and 'B'. For each subset, the central lines
      and the limits of natural variation will be calculated independently. So, you can check if there is
      modification of the average value and of the dispersion when the time window is modified. It could
      reflect, for example, the use of different operational parameters on each event frame.
      Other possibilities of event indications: 0, 1, 2, 3, ... (sequence of integers); 'A', 'B', 'C', etc;
      'stage1', 'stage2', ..., 'treatment1', 'treatment2',....; 'frame0', 'frame1', 'frame2', etc.
      ATTENTION: Do not identify different frames with the same value. For example, if
      COLUMN_WITH_EVENT_FRAME_INDICATION has missing values for the first values, then a sequence of rows
      is identified as number 0; followed by a sequence of missing values. In this case, the two windows
      with missing values would be merged as a single window, and the mean and variation would be
      obtained for this merged subset. Then, always specify different windows with different values.
      Other example: COLUMN_WITH_EVENT_FRAME_INDICATION = 'col1' will search for event frame indications
      in column 'col1'.
    
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
    
    : param: REFERENCE_VALUE: keep it as None or add a float value.
      This reference value will be shown as a red constant line to be compared
      with the plots. e.g. REFERENCE_VALUE = 1.0 will plot a line passing through
      VARIABLE_TO_ANALYZE = 1.0
    
    : param: USE_SPC_CHART_ASSISTANT = False. Set USE_SPC_CHART_ASSISTANT = True to open the 
      visual flow chart assistant that will help you select the appropriate parameters; 
      as well as passing the data in the correct format. If the assistant is open, many of the 
      arguments of the function will be filled when using it.

    : param: chart_to_use = '3s_as_natural_variation', 'std_error', 'i_mr', 'xbar_s', 'np', 'p', 
      'u', 'c', 'g', 't'
      The type of chart that will be obtained, as well as the methodology used for estimating the
      natural variation of the process. Notice that it may be strongly dependent on the statistical
      distribution. So, if you are not sure about the distribution, or simply want to apply a more
      general (less restrictive) methodology, set:

        CHART_TO_USE = '3s_as_natural_variation' to estimate the natural variation as 3 times the
         standard deviation (s); or
        CHART_TO_USE = 'std_error' for estimating it as 3 times the standard error, where 
         standard error = s/(n**0.5) = s/sqrt(n), n = number of samples (that may be the number of 
         individual data samples collected, or the number of subgroups or labels); sqrt is the square root.
        
        https://en.wikipedia.org/wiki/Standard_error
     
     CHART_TO_USE = '3s_as_natural_variation' and CHART_TO_USE = 'std_error' are the only ones available
     for both individual and grouped data.
    
     ATTENTION: Do not group the variables before using the function. It will perform the automatic
     grouping in accordance to the values specified as COLUMN_WITH_LABELS_OR_SUBGROUPS.
     Other values allowed for CHART_TO_USE:
     CHART_TO_USE = 'i_mr', for individual values of a numeric (continuous) variable which follows the
      NORMAL distribution.
     CHART_TO_USE = 'xbar_s', for grouped values (by mean) of a numeric variable, where the mean values
      of labels or subgroups follow a NORMAL distribution.
     CHART_TO_USE = 'np', for grouped binary variables (allowed values: 0 or 1). This is the
      control chart for proportion of defectives. - Original data must follow the BINOMIAL distribution.
     CHART_TO_USE = 'p', for grouped binary variables (allowed values: 0 or 1). This is the
      control chart for count of defectives. - Original data must follow the BINOMIAL distribution.
    
     Attention: an error will be raised if CHART_TO_USE = 'np' or 'p' and the variable was not converted
     to a numeric binary, with values 0 or 1. This function do not perform the automatic ordinal or
     One-Hot encoding of the categorical features.
    
     CHART_TO_USE = 'u', for counts of occurrences per unit. - Original data must follow the POISSON
      distribution (special case of the gamma distribution).
     CHART_TO_USE = 'c', for average occurrence per unit. - Original data must follow the POISSON
      distribution (special case of the gamma distribution).
    
     CHARTS FOR ANALYZING RARE EVENTS
      CHART_TO_USE = 'g', for analyzing count of events between successive rare events occurrences 
       (data follow the GEOMETRIC distribution).
      CHART_TO_USE = 't', for analyzing time interval between successive rare events occurrences.
    
    : param: consider_skewed_dist_when_estimating_with_std.
      Whether the distribution of data to be analyzed present high skewness or kurtosis.
      If CONSIDER_SKEWED_DISTRIBUTION_WHEN_ESTIMATING_STD = False, the central lines will be estimated
      as the mean values of the analyzed variable. 
      If CONSIDER_SKEWED_DISTRIBUTION_WHEN_ESTIMATING_STD = True, the central lines will be estimated 
      as the median of the analyzed variable, which is a better alternative for skewed data such as the 
      ones that follow geometric or lognormal distributions (median = mean × 0.693).
      Notice that this argument has effect only when CHART_TO_USE = '3s_as_natural_variation' or 
      CHART_TO_USE = 'std_error'.

    : param: RARE_EVENT_INDICATION = None. String (in quotes), float or integer. If you want to analyze a
      rare event through 'g' or 't' control charts, this parameter is obbligatory. Also, notice that:
      COLUMN_WITH_VARIABLE_TO_BE_ANALYZED must be the column which contains an indication of the rare
      event occurrence, and the RARE_EVENT_INDICATION is the value of the column COLUMN_WITH_VARIABLE_TO_BE_ANALYZED
      when a rare event takes place.
      For instance, suppose RARE_EVENT_INDICATION = 'shutdown'. It means that column COLUMN_WITH_VARIABLE_TO_BE_ANALYZED
      has the value 'shutdown' when the rare event occurs, i.e., for timestamps when the system
      stopped. Other possibilities are RARE_EVENT_INDICATION = 0, or RARE_EVENT_INDICATION = -1,
      indicating that when COLUMN_WITH_VARIABLE_TO_BE_ANALYZED = 0 (or -1), we know that
      a rare event occurred. The most important thing here is that the value given to the rare event
      should be assigned ONLY to the rare events.

      You do not need to assign values for the other timestamps when no rare event took place. But it is
      important to keep all timestamps in the dataframe. That is because the rare events charts will
      compare the rare event occurrence against all other events and timestamps.
      If you are not analyzing rare events with 'g' or 't' charts, keep RARE_EVENT_INDICATION = None.
    
    : param: RARE_EVENT_TIMEDELTA_UNIT: 'day', 'second', 'nanosecond', 'minute', 'hour',
      'month', 'year' - This is the unit of time that will be used to plot the time interval
      (timedelta) between each successive rare events. If None or invalid value used, timedelta
      will be given in days.
      Notice that this parameter is referrent only to the rare events analysis with 'g' or 't' charts.
      Also, it is valid only when the timetag column effectively stores a timestamp. If the timestamp
      column stores a float or an integer (numeric) value, then the final dataframe and plot will be
      obtained in the same numeric scale of the original data, not in the unit indicated as
      RARE_EVENT_TIMEDELTA_UNIT.
    

    ## CONTROL CHARTS CALCULATION

    # References: 
    # Douglas C. Montgomery. Introduction to Statistical Quality Control. 6th Edition. John Wiley and Sons, 2009.
    # Jacob Anhoej. Control Charts with qicharts for R. 2021-04-20. In: https://cran.r-project.org/web/packages/qicharts/vignettes/controlcharts.html

    CENTER LINE = m (mean)
    s = std deviation
    
    General equation of the control limits:
     UCL = upper control limit = m + L*s
     LCL = lower control limit = m - L*s
     where L is a measurement of distance from central line.
    
    for a subgroup of data collected for a continuous variable X:
     x_bar_1 = mean value for subgroup 1,..., x_bar_n = mean for subgroup n.
     x_bar_bar = (x_bar_1 + ... + x_bar_n)/n
    
    On the other hand, the range R between two collected values is defined as: R = x_max - x_min
     If R1, ... Rm are the ranges for m subgroups (which may be of size 2),
     we have R_bar = (R1 + R2 + ... + Rm)/m
    
    Analogously, if s_i is the standard deviation for a subgroup i and there are m subgroups:
     s_bar = (s_1 +... +s_m)/m
    
    ## INDIVIDUAL MEASUREMENTS (Montgomery, pg.259, section 6.4)
    
    For individual measurements, we consider subgroups formed by two consecutive measurements, so
     m = 2, and R = abs(x_i - x_(i-1)), where abs function calculates the absolute value of the
     difference between two successive subgroups.
     UCL =  x_bar_bar + 3*(1/d2)*R_bar
     LCL =  x_bar_bar - 3*(1/d2)*R_bar
     Center line = x_bar_bar
        
    # CONTROL CHARTS FOR SUBGROUPS 
            
    X-bar-S (continuous variables) - (Montgomery, pg.253, section 6.3.1):
    For subgroups with m elements:
      UCL = x_bar_bar + A3*s_bar
      Center line = x_bar_bar
      LCL = x_bar_bar - A3*s_bar
    
    # CONTROL CHARTS FOR CATEGORICAL VARIABLES
    
    P-chart - (Montgomery, pg.291, section 7.2.1):
     The sample fraction nonconforming is defined as the ratio of the number of nonconforming units 
     in the sample D to the sample size n:
     p = D/n. For a subgroup i containing n elements: p_i = D_i/n, i = 1,... m subgroups
     From the binomial distribution, the mean should be estimated as p, and the variance s² 
     as p(1-p)/n. The average of p is:
     p_bar = (p_1 + ... + p_m)/m
    
     UCL = p_bar + 3((p_bar(1-p_bar)/n)**(0.5))
     Center line = p_bar
     LCL = p_bar - 3((p_bar(1-p_bar)/n)**(0.5)), whereas n is the size of a given subgroup
     Therefore, the width of control limits here vary with the size of the subgroups (it is
     a function of the size of each subgroup)
    
    np-chart - (Montgomery, pg.300, section 7.2.1):
     UCL = np + 3((np(1-p))**(0.5))
     Center line = np_bar
     LCL = np - 3((np(1-p))**(0.5))
     where np is the total sum of nonconforming, considering all subgroups, and p is the
     propoertion for each individual subgroup, as previously defined.
     Then, again the control limits depend on the subgroup (label) size.
    
    C-chart - (Montgomery, pg.309, section 7.3.1):
     In Poisson distribution, mean and variance are both equal to c.
     UCL = c_bar + 3(c_bar**(0.5))
     Center line = c_bar
     LCL = c_bar + 3(c_bar**(0.5))
     where c_bar is the mean c among all subgroups (labels)
    
    U-chart - (Montgomery, pg.314, section 7.3.1):
     If we find x total nonconformities in a sample of n inspection units, then the average 
     number of nonconformities per inspection unit is: u = x/n
     UCL = u_bar + 3((u_bar/n)**(0.5))
     Center line = u_bar
     LCL = u_bar + 3((u_bar/n)**(0.5))
     where u_bar is the mean u among all subgroups (labels), but n is the individual subgroup size,
     making the chart limit not-constant depending on the subgroups' sizes

    # RARE EVENTS
    ATTENTION: Due not group data in this case. Since events are rare, they are likely to be 
     eliminated during aggregation.
     Usually, similarly to what is observed for the log-normal, data that follow the geometric
     distribution is highly skewed, so the mean is not a good estimator for the central line.
     Usually, it is better to apply the median = 0.693 x mean.
    
    G-Chart: counts of total occurences between successive rare events occurences.
     https://www.spcforexcel.com/knowledge/attribute-control-charts/g-control-chart
     (Montgomery, pg.317, section 7.3.1)
    
     e.g. total of patients between patient with ulcer.
     The probability model that they use for the geometric distribution is p(x) = p(1-p)**(x-a)
     where a is the known minimum possible number of events.
     The number of units between defectives is modelled by the geometric distribution.
     So, the G-control chart plots counting of occurrence by number, time unit, or timestamp.
     Geometric distribution is highly skewed, thus the median is a better representation of the 
     process centre to be used with the runs analysis.

     Let y = total count of events between successive occurences of the rare event.
    
     g_bar = median(y) = 0.693 x mean(y)
     One can estimate the control limits as g_bar + 3(((g_bar)*(g_bar+1))**(0.5)) and
     g_bar - 3(((g_bar)*(g_bar+1))**(0.5)), and central line = g_bar.
     A better approach takes into account the probabilities associated to the geometric (g)
     distribution.
    
     In the probability approach, we start by calculating the value of p, which is an event
     probability:
     p = (1/(g_bar + 1))*((N-1)/N), where N is the total of individual values of counting between
     successive rare events. So, if we have 3 rare events, A, B, and C, we have two values of 
     counting between rare events, from A to B, and from B to C. In this case, since we have two
     values that follow the G distribution, N = 2.
     Let alpha_UCL a constant dependent on the number of sigma limits for the control limits. For
     the usual 3 sigma limits, the value of alpha_UCL = 0.00135. With this constant, we can
     calculate the control limits and central line
    
     UCL = ((ln(0.00135))/(ln(1 - p))) - 1
     Center line = ((ln(0.5))/(ln(1 - p))) - 1
     LCL = max(0, (((ln(1 - 0.00135))/(ln(1 - p))) - 1))
     where max represent the maximum among the two values in parentheses; and ln is the natural
     logarithm (base e), sometimes referred as log (inverse of the exponential): ln(exp(x)) = x
     = log(exp(x)) = x
    
    t-chart: timedelta between rare events.
     (Montgomery, pg.324, section 7.3.5):
     https://www.qimacros.com/control-chart-formulas/t-chart-formula/
    
     But instead of displaying the number of cases between events (defectives) it displays 
     the time between events.
    
     Nelson (1994) has suggested solving this problem by transforming the exponential random
     variable to a Weibull random variable such that the resulting Weibull distribution is well
     approximated by the normal distribution. 
     If y represents the original exponential random variable (timedelta between successive rare
     event occurence), the appropriate transformation is:
     x = y**(1/3.6)= y**(0.2777)
     where x is treated as a normal distributed variable, and the control chart for x is the I-MR.
     So: 1. transform y into x;
     2. Calculate the control limits for x as if it was a chart for individuals;
     reconvert the values to the original scale doing: y = x**(3.6)
    
     We calculate for the transformed values x the moving ranges R and the mean of the 
     mean values calculated for the 2-elements consecutive subgroups x_bar_bar, in the exact same way
     we would do for any I-MR chart
     UCL_transf =  x_bar_bar + 3*(1/d2)*R_bar
     LCL_transf =  x_bar_bar - 3*(1/d2)*R_bar
     Center line_transf = x_bar_bar
    
     These values are in the transformed scale. So, we must reconvert them to the original scale for
     obtaining the control limits and central line:
     UCL = (UCL_transf)**(3.6)
     LCL = (LCL_transf)**(3.6)
     Center line = (Center line_transf)**(3.6)
    
     Notice that this procedure naturally corrects the deviations caused by the skewness of the 
     distribution. Actually, log and exponential transforms tend to reduce the skewness and to 
     normalize the data.
    """

    from scipy import stats
    

    numeric_dtypes = [np.int16, np.int32, np.int64, np.float16, np.float32, np.float64]
    
    if ControlVars.show_plots: # the upper context is dominant
        if (use_spc_chart_assistant == True):
            
            # Run if it is True. Requires TensorFlow to load. Load the extra library only
            # if necessary:
            # To show the Python class attributes, use the __dict__ method:
            # http://www.learningaboutelectronics.com/Articles/How-to-display-all-attributes-of-a-class-or-instance-of-a-class-in-Python.php#:~:text=So%20the%20__dict__%20method%20is%20a%20very%20useful,other%20data%20type%20such%20as%20a%20class%20itself.

            # instantiate the object
            assistant = SPCChartAssistant()
            # Download the images:
            assistant = assistant.download_assistant_imgs()

            # Run the assistant:
            while (assistant.keep_assistant_on == True):

                # Run the wrapped function until the user tells you to stop:
                # Notice that both variables are True for starting the first loop:
                assistant = assistant.open_chart_assistant_screen()

            # Delete the images
            assistant.delete_assistant_imgs()
            # Select the chart and the parameters:
            chart_to_use, column_with_labels_or_subgroups, consider_skewed_dist_when_estimating_with_std, column_with_variable_to_be_analyzed, timestamp_tag_column, column_with_event_frame_indication, rare_event_timedelta_unit, rare_event_indication = assistant.chart_selection()

    # Back to the main code, independently on the use of the assistant:    
    # set a local copy of the dataframe:
    DATASET = df.copy(deep = True)

    # Start a list unique_labels containing only element 0:
    unique_labels = [0]
    # If there is a column of labels or subgroups, this list will be updated. So we can control
    # the chart selection using the length of this list: if it is higher than 1, we have subgroups,
    # not individual values.

    if (timestamp_tag_column is None):

        # use the index itself:
        timestamp_tag_column = 'index'
        DATASET[timestamp_tag_column] = DATASET.index

    elif (DATASET[timestamp_tag_column].dtype not in numeric_dtypes):

        # The timestamp_tag_column was read as an object, indicating that it is probably a timestamp.
        # Try to convert it to datetime64:
        try:
            DATASET[timestamp_tag_column] = (DATASET[timestamp_tag_column]).astype('datetime64[ns]')
            print(f"Variable {timestamp_tag_column} successfully converted to datetime64[ns].\n")

        except:
            # Simply ignore it
            pass
        
        
    # Check if there are subgroups or if values are individuals. Also, check if there is no selected
    # chart:
    if ((column_with_labels_or_subgroups is None) & (chart_to_use is None)):
            
        print("There are only individual observations and no valid chart selected, so using standard error as natural variation (control limits).\n")
        # values are individual, so set it as so:
        chart_to_use = 'std_error'
        
    elif ((chart_to_use is None) | (chart_to_use not in ['std_error', '3s_as_natural_variation', 'i_mr', 'xbar_s', 'np', 'p', 'u', 'c', 'g', 't'])):
            
        print("No valid chart selected, so using standard error as natural variation (control limits).\n")
        # values are individual, so set it as so:
        chart_to_use = 'std_error'
        
    elif (chart_to_use in ['g', 't']):
            
        if (rare_event_timedelta_unit is None):
            print("No valid timedelta unit provided, so selecting \'day\' for analysis of rare events.\n")
            rare_event_timedelta_unit = 'day'
        elif (rare_event_timedelta_unit not in ['day', 'second', 'nanosecond', 'millisecond', 'hour', 'week', 'month', 'year']):
            print("No valid timedelta unit provided, so selecting \'day\' for analysis of rare events.\n")
            rare_event_timedelta_unit = 'day'
            
        if (rare_event_indication is None):
            print("No rare event indication provided, so changing the plot to \'std_error\'.\n")
            chart_to_use = 'std_error'
                
    # Now, a valid chart_to_use was selected and is saved as chart_to_use.
    # We can sort the dataframe according to the columns present:
        
    if ((column_with_labels_or_subgroups is not None) & (column_with_event_frame_indication is not None)):
        # There are time windows to consider and labels.
        # Update the list of unique labels:
        unique_labels = list(DATASET[column_with_labels_or_subgroups].unique())
        
        # sort DATASET by timestamp_tag_column, column_with_labels_or_subgroups, 
        # column_with_event_frame_indication, and column_with_variable_to_be_analyzed,
        # all in Ascending order:
        DATASET = DATASET.sort_values(by = [timestamp_tag_column, column_with_labels_or_subgroups, column_with_event_frame_indication, column_with_variable_to_be_analyzed], ascending = [True, True, True, True])
        
    elif (column_with_event_frame_indication is not None):
        # We already tested the simultaneous presence of both. So, to reach this condition, 
        # there is no column_with_labels_or_subgroups, but there is column_with_event_frame_indication
            
        # sort DATASET by timestamp_tag_column, column_with_event_frame_indication, 
        # and column_with_variable_to_be_analyzed, all in Ascending order:
        DATASET = DATASET.sort_values(by = [timestamp_tag_column, column_with_event_frame_indication, column_with_variable_to_be_analyzed], ascending = [True, True, True])
        
    elif (column_with_labels_or_subgroups is not None):
        # We already tested the simultaneous presence of both. So, to reach this condition, 
        # there is no column_with_event_frame_indication, but there is column_with_labels_or_subgroups
        # Update the list of unique labels:
        unique_labels = list(DATASET[column_with_labels_or_subgroups].unique())
        
        # sort DATASET by timestamp_tag_column, column_with_labels_or_subgroups, 
        # and column_with_variable_to_be_analyzed, all in Ascending order:
        DATASET = DATASET.sort_values(by = [timestamp_tag_column, column_with_labels_or_subgroups, column_with_variable_to_be_analyzed], ascending = [True, True, True])
        
    else:
        # There is neither column_with_labels_or_subgroups, nor column_with_event_frame_indication
        # sort DATASET by timestamp_tag_column, and column_with_variable_to_be_analyzed, 
        # both in Ascending order:
        DATASET = DATASET.sort_values(by = [timestamp_tag_column, column_with_variable_to_be_analyzed], ascending = [True, True])
        
    # Finally, reset indices:
    DATASET = DATASET.reset_index(drop = True)
    
    # Start a list of dictionaries to store the dataframes and subdataframes that will be analyzed:
    list_of_dictionaries_with_dfs = []
    # By now, dictionaries will contain a key 'event_frame' storing an integer identifier for the
    # event frame, starting from 0 (the index of the event in the list of unique event frames), or
    # zero, for the cases where there is a single event; a key 'df' storing the dataframe object, 
    # a key 'mean', storing the mean value of column_with_variable_to_be_analyzed; keys 'std' and
    # 'var', storing the standard deviation and the variance for column_with_variable_to_be_analyzed;
    # and column 'count', storing the counting of rows. 
    # After obtaining the control limits, they will also get a key 'list_of_points_out_of_cl'. 
    # This key will store a list of dictionaries (nested JSON), where each dictionary 
    # will have two keys, 'x', and 'y', with the coordinates of the point outside control 
    # limits as the values.
    
    if ((column_with_event_frame_indication is not None) & (chart_to_use not in ['g', 't'])):
        
        # Get a series of unique values of the event frame indications, and save it as a list 
        # using the list attribute:
        unique_event_indication = list(DATASET[column_with_event_frame_indication].unique())
        
        print(f"{len(unique_event_indication)} different values of event frame indication detected: {unique_event_indication}.\n")
        
        if (len(unique_event_indication) > 0):
            
            # There are more than one event frame to consider. Let's loop through the list of
            # event frame indication, where each element is referred as 'event_frame':
            for event_frame in unique_event_indication:
                
                # Define a boolean filter to select only the rows correspondent to event_frame:
                boolean_filter = (DATASET[column_with_event_frame_indication] == event_frame)
                
                # Create a copy of the dataset, with entries selected by that filter:
                ds_copy = (DATASET[boolean_filter]).copy(deep = True)
                # Sort again by timestamp_tag_column and column_with_variable_to_be_analyzed, 
                # to guarantee the results are in order:
                ds_copy = ds_copy.sort_values(by = [timestamp_tag_column, column_with_variable_to_be_analyzed], ascending = [True, True])
                # Restart the index of the copy:
                ds_copy = ds_copy.reset_index(drop = True)
                
                # Store ds_copy in a dictionary of values. Put the index of event_frame
                # in the list unique_event_indication as the value in key 'event_frame', to numerically
                # identify the dictionary according to the event frame.
                # Also, store the 'mean', 'sum,' 'std', 'var', and 'count' aggregates for the column
                # column_with_variable_to_be_analyzed from ds_copy:
                
                dict_of_values = {
                                    'event_frame': unique_event_indication.index(event_frame),
                                    'df': ds_copy, 
                                    'center': ds_copy[column_with_variable_to_be_analyzed].mean(),
                                    'sum': ds_copy[column_with_variable_to_be_analyzed].sum(),
                                    'std': ds_copy[column_with_variable_to_be_analyzed].std(),
                                    'var': ds_copy[column_with_variable_to_be_analyzed].var(),
                                    'count': ds_copy[column_with_variable_to_be_analyzed].count()
                                }
                
                # append dict_of_values to the list:
                list_of_dictionaries_with_dfs.append(dict_of_values)
                
                # Now, the loop will pick the next event frame.
        
        else:
            
            # There is actually a single time window. The only dataframe 
            # stored in the dictionary is DATASET itself, which is stored with 
            # the aggregate statistics calculated for the whole dataframe. Since
            # there is a single dataframe, the single value in 'event_frame' is 0.
            dict_of_values = {
                                'event_frame': 0,
                                'df': DATASET, 
                                'center': DATASET[column_with_variable_to_be_analyzed].mean(),
                                'sum': DATASET[column_with_variable_to_be_analyzed].sum(),
                                'std': DATASET[column_with_variable_to_be_analyzed].std(),
                                'var': DATASET[column_with_variable_to_be_analyzed].var(),
                                'count': DATASET[column_with_variable_to_be_analyzed].count()
                            }
            
            # append dict_of_values to the list:
            list_of_dictionaries_with_dfs.append(dict_of_values)
    
    else:
        # The other case where there is a single time window or 'g' or 't' charts. 
        # So, the only dataframe stored in the dictionary is DATASET itself, which is stored with 
        # the aggregate statistics calculated for the whole dataframe. Since
        # there is a single dataframe, the single value in 'event_frame' is 0.
        dict_of_values = {
                            'event_frame': 0,
                            'df': DATASET, 
                            'center': DATASET[column_with_variable_to_be_analyzed].mean(),
                            'sum': DATASET[column_with_variable_to_be_analyzed].sum(),
                            'std': DATASET[column_with_variable_to_be_analyzed].std(),
                            'var': DATASET[column_with_variable_to_be_analyzed].var(),
                            'count': DATASET[column_with_variable_to_be_analyzed].count()
                        }
            
        # append dict_of_values to the list:
        list_of_dictionaries_with_dfs.append(dict_of_values)
    
    # Now, data is sorted, timestamps were converted to datetime objects, and values collected
    # for different timestamps were separated into dictionaries (elements) from the list
    # list_of_dictionaries_with_dfs. Each dictionary contains a key 'df' used to access the
    # dataframe, as well as keys storing the aggregate statistics: 'mean', 'std', 'var', and
    # 'count'.
    
    # Now, we can process the different control limits calculations.
    
    # Start a support list:
    support_list = []
    
    ## INDIVIDUAL VALUES
    # Use the unique_labels list to guarantee that there have to be more than 1 subgroup
    # to not treat data as individual values. If there is a single subgroup, unique_labels
    # will have a single element.
    if ((column_with_labels_or_subgroups is None) | (len(unique_labels) <= 1)):
        
        if (chart_to_use == 'i_mr'):
            
            print("WARNING: the I-MR control limits are based on the strong hypothesis that data follows a normal distribution. If it is not the case, do not use this chart.")
            print("If you are not confident about the statistical distribution, select chart_to_use = \'3s_as_natural_variation\' to use 3 times the standard deviation as estimator for the natural variation (the control limits); or chart_to_use = \'std_error\' to use 3 times the standard error as control limits.\n")
            
            for dictionary in list_of_dictionaries_with_dfs:
                
                # Create an instance (object) from SPCPlot class:
                plot = SPCPlot (dictionary = dictionary, column_with_variable_to_be_analyzed = column_with_variable_to_be_analyzed, timestamp_tag_column = timestamp_tag_column, chart_to_use = chart_to_use, column_with_labels_or_subgroups = column_with_labels_or_subgroups, consider_skewed_dist_when_estimating_with_std = consider_skewed_dist_when_estimating_with_std, rare_event_indication = rare_event_indication, rare_event_timedelta_unit = rare_event_timedelta_unit)
                # Apply the method
                plot = plot.chart_i_mr()
                # Append the updated dictionary to the support_list (access the dictionary attribute):
                support_list.append(plot.dictionary)
            
            # Now that we finished looping through dictionaries, make list_of_dictionaries_with_dfs
            # the support_list itself:
            list_of_dictionaries_with_dfs = support_list
        
        elif (chart_to_use in ['g', 't']):
            
            print(f"Analyzing occurence of rare event {rare_event_indication} through chart {chart_to_use}.\n")
            
            for dictionary in list_of_dictionaries_with_dfs:
                
                # Create an instance (object) from SPCPlot class:
                plot = SPCPlot (dictionary = dictionary, column_with_variable_to_be_analyzed = column_with_variable_to_be_analyzed, timestamp_tag_column = timestamp_tag_column, chart_to_use = chart_to_use, column_with_labels_or_subgroups = column_with_labels_or_subgroups, consider_skewed_dist_when_estimating_with_std = consider_skewed_dist_when_estimating_with_std, rare_event_indication = rare_event_indication, rare_event_timedelta_unit = rare_event_timedelta_unit)
                # Apply the method
                plot = plot.rare_events_chart()
                # Append the updated dictionary to the support_list (access the dictionary attribute):
                support_list.append(plot.dictionary)
            
            # Now that we finished looping through dictionaries, make list_of_dictionaries_with_dfs
            # the support_list itself:
            list_of_dictionaries_with_dfs = support_list
            
        elif (chart_to_use == '3s_as_natural_variation'):
            
            print("Using 3s (3 times the standard deviation) as estimator of the natural variation (control limits).\n")
            
            for dictionary in list_of_dictionaries_with_dfs:
                
                # Create an instance (object) from SPCPlot class:
                plot = SPCPlot (dictionary = dictionary, column_with_variable_to_be_analyzed = column_with_variable_to_be_analyzed, timestamp_tag_column = timestamp_tag_column, chart_to_use = chart_to_use, column_with_labels_or_subgroups = column_with_labels_or_subgroups, consider_skewed_dist_when_estimating_with_std = consider_skewed_dist_when_estimating_with_std, rare_event_indication = rare_event_indication, rare_event_timedelta_unit = rare_event_timedelta_unit)
                # Apply the method
                plot = plot.chart_3s()
                # Append the updated dictionary to the support_list (access the dictionary attribute):
                support_list.append(plot.dictionary)
            
            # Now that we finished looping through dictionaries, make list_of_dictionaries_with_dfs
            # the support_list itself:
            list_of_dictionaries_with_dfs = support_list
        
        else:
            
            print("Using 3 times the standard error as estimator of the natural variation (control limits).\n")
            
            for dictionary in list_of_dictionaries_with_dfs:
                
                # Create an instance (object) from SPCPlot class:
                plot = SPCPlot (dictionary = dictionary, column_with_variable_to_be_analyzed = column_with_variable_to_be_analyzed, timestamp_tag_column = timestamp_tag_column, chart_to_use = chart_to_use, column_with_labels_or_subgroups = column_with_labels_or_subgroups, consider_skewed_dist_when_estimating_with_std = consider_skewed_dist_when_estimating_with_std, rare_event_indication = rare_event_indication, rare_event_timedelta_unit = rare_event_timedelta_unit)
                # Apply the method
                plot = plot.chart_std_error()
                # Append the updated dictionary to the support_list (access the dictionary attribute):
                support_list.append(plot.dictionary)
            
            # Now that we finished looping through dictionaries, make list_of_dictionaries_with_dfs
            # the support_list itself:
            list_of_dictionaries_with_dfs = support_list
    
    ## DATA IN SUBGROUPS
    else:
        
        # Loop through each dataframe:
        for dictionary in list_of_dictionaries_with_dfs:
            
            # Create an instance (object) from SPCPlot class:
            plot = SPCPlot (dictionary = dictionary, column_with_variable_to_be_analyzed = column_with_variable_to_be_analyzed, timestamp_tag_column = timestamp_tag_column, chart_to_use = chart_to_use, column_with_labels_or_subgroups = column_with_labels_or_subgroups, consider_skewed_dist_when_estimating_with_std = consider_skewed_dist_when_estimating_with_std, rare_event_indication = rare_event_indication, rare_event_timedelta_unit = rare_event_timedelta_unit)
            # Apply the method
            plot = plot.create_grouped_df()
                
            # Now, dataframe is ready for the calculation of control limits.
            # Let's select the appropriate chart:
        
            if (chart_to_use == '3s_as_natural_variation'):

                plot = plot.chart_3s()
                # Append the updated dictionary to the support_list (access the dictionary attribute):
                support_list.append(plot.dictionary)
            
            elif (chart_to_use == 'std_error'):

                plot = plot.chart_std_error()
                # Append the updated dictionary to the support_list (access the dictionary attribute):
                support_list.append(plot.dictionary)
                
            elif (chart_to_use == 'xbar_s'):
                
                plot = plot.chart_x_bar_s()
                # Append the updated dictionary to the support_list (access the dictionary attribute):
                support_list.append(plot.dictionary)
            
            elif (chart_to_use == 'p'):
                
                plot = plot.chart_p()
                # Append the updated dictionary to the support_list (access the dictionary attribute):
                support_list.append(plot.dictionary)

            elif (chart_to_use == 'np'):
            
                plot = plot.chart_np()
                # Append the updated dictionary to the support_list (access the dictionary attribute):
                support_list.append(plot.dictionary)

            elif (chart_to_use == 'c'):
                
                plot = plot.chart_c()
                # Append the updated dictionary to the support_list (access the dictionary attribute):
                support_list.append(plot.dictionary)
                
            elif (chart_to_use == 'u'):
                
                plot = plot.chart_u()
                # Append the updated dictionary to the support_list (access the dictionary attribute):
                support_list.append(plot.dictionary)

            else:

                raise InvalidInputsError(f"Select a valid control chart: {['3s_as_natural_variation', 'std_error', 'i_mr', 'xbar_s', 'np', 'p', 'u', 'c', 'g', 't']}.\n")
            
            # Go to the next element (dictionary) from the list list_of_dictionaries_with_dfs
        
        # Now that we finished looping through dictionaries, make list_of_dictionaries_with_dfs
        # the support_list itself:
        list_of_dictionaries_with_dfs = support_list
        
        # Now we finished looping, we can print the warnings
        if (chart_to_use == '3s_as_natural_variation'):
    
            print("Using 3s (3 times the standard deviation) as estimator of the natural variation (control limits). Remember that we are taking the standard deviation from the subgroup (label) aggregates.\n")
        
        elif (chart_to_use == 'xbar_s'):
            
            print("WARNING: the X-bar-S control limits are based on the strong hypothesis that the mean values from the subgroups follow a normal distribution. If it is not the case, do not use this chart.")
            print("If you are not confident about the statistical distribution, select chart_to_use = \'3s_as_natural_variation\' to use 3 times the standard deviation as estimator for the natural variation (the control limits).\n")
            print("Use this chart for analyzing mean values from multiple data collected together in groups (or specific labels), usually in close moments.\n")
        
        elif (chart_to_use == 'np'):
            print("WARNING: the U control limits are based on the strong hypothesis that the counting of values from the subgroups follow a Poisson distribution (Poisson is a case from the Gamma distribution). If it is not the case, do not use this chart.")
            
        
        elif (chart_to_use == 'p'):
            print("WARNING: the U control limits are based on the strong hypothesis that the counting of values from the subgroups follow a Poisson distribution (Poisson is a case from the Gamma distribution). If it is not the case, do not use this chart.")
            
        
        elif (chart_to_use == 'u'):
            
            print("WARNING: the U control limits are based on the strong hypothesis that the counting of values from the subgroups follow a Poisson distribution (Poisson is a case from the Gamma distribution). If it is not the case, do not use this chart.")
            print("If you are not confident about the statistical distribution, select chart_to_use = \'3s_as_natural_variation\' to use 3 times the standard deviation as estimator for the natural variation (the control limits).\n")
        
        else:
            # chart_to_use == 'c'
            print("WARNING: the C control limits are based on the strong hypothesis that the counting of values from the subgroups follow a Poisson distribution (Poisson is a case from the Gamma distribution). If it is not the case, do not use this chart.")
            print("If you are not confident about the statistical distribution, select chart_to_use = \'3s_as_natural_variation\' to use 3 times the standard deviation as estimator for the natural variation (the control limits).\n")
        
        
    # Now, we have all the control limits calculated, and data aggregated when it is the case.
    # Let's merge (append - SQL UNION) all the dataframes stored in the dictionaries (elements)
    # from the list list_of_dictionaries_with_dfs. Pick the first dictionary, i.e., element of
    # index 0 from the list:
    
    dictionary = list_of_dictionaries_with_dfs[0]
    # access the dataframe:
    df = dictionary['df']
    
    # Also, start a list for storing the timestamps where the event frames start:
    time_of_event_frame_start = []
    # Let's pick the last element from df[timestamp_tag_column]: it is the time
    # when the time window (event frame) is changing. We can convert it to a list
    # and slice the list from its last element (index -1; the immediately before is -2,
    # etc).
    timestamp_tag_value = list(df[timestamp_tag_column])[-1:]
    # Now concatenate this 1-element list with time_of_event_frame_start:
    time_of_event_frame_start = time_of_event_frame_start + timestamp_tag_value
    # When concatenating lists, the elements from the right list are sequentially added to the
    # first one: list1 = ['a', 'b'], list2 = ['c', 'd'], list1 + list2 = ['a', 'b', 'c', 'd'] 
    
    # Now, let's loop through each one of the other dictionaries from the list:
    
    for i in range (1, len(list_of_dictionaries_with_dfs)):
        
        # start from i = 1, index of the second element (we already picked the first one),
        # and goes to the index of the last dictionary, len(list_of_dictionaries_with_dfs) - 1:
        
        # access element (dictionary) i from the list:
        dictionary_i = list_of_dictionaries_with_dfs[i]
        # access the dataframe i:
        df_i = dictionary_i['df']
        
        # Again, pick the last timestamp from this window:
        timestamp_tag_value = list(df[timestamp_tag_column])[-1:]
        # Now concatenate this 1-element list with time_of_event_frame_start:
        time_of_event_frame_start = time_of_event_frame_start + timestamp_tag_value
        
        # Append df_i to df (SQL UNION - concatenate or append rows):
        # Save in df itself:
        df = pd.concat([df, df_i], axis = 0, ignore_index = True, sort = True, join = 'inner')
        # axis = 0 to append rows; 'inner' join removes missing values
    
    # Now, reset the index of the final concatenated dataframe, containing all the event frames
    # separately processed, and containing the control limits and mean values for each event:
    df = df.reset_index(drop = True)
    
    # Now, add a column to inform if each point is in or out of the control limits.
    # apply a filter to select each situation:
    # (syntax: dataset.loc[dataset['column_filtered'] <= 0.87, 'labelled_column'] = 1)
    # Start the new column as 'in_control_lim' (default case):
    df['control_limits_check'] = 'in_control_limits'
    
    # Get the control limits:
    lower_cl = df['lower_cl']
    upper_cl = df['upper_cl']
    
    # Now modify only points which are out of the control ranges:
    df.loc[(df[column_with_variable_to_be_analyzed] < lower_cl), 'control_limits_check'] = 'below_lower_control_limit'
    df.loc[(df[column_with_variable_to_be_analyzed] > upper_cl), 'control_limits_check'] = 'above_upper_control_limit'
                
    # Let's also create the 'red_df' containing only the values outside of the control limits.
    # This dataframe will be used to highlight the values outside the control limits
    
    # copy the dataframe:
    red_df = df.copy(deep = True)
    # Filter red_df to contain only the values outside the control limits:
    boolean_filter = ((red_df[column_with_variable_to_be_analyzed] < lower_cl) | (red_df[column_with_variable_to_be_analyzed] > upper_cl))
    red_df = red_df[boolean_filter]
    # Reset the index of this dataframe:
    red_df = red_df.reset_index(drop = True)
    

    if (len(red_df) > 0):
        
        # There is at least one row outside the control limits.
        print("Attention! Point outside of natural variation (control limits).")
        print("Check the red_df dataframe returned for details on values outside the control limits.")
        
        if ControlVars.show_results: 
            print("They occur at the following time values:\n")
            
            try:
                # only works in Jupyter Notebook:
                from IPython.display import display
                display(red_df)

            except: # regular mode
                print(list(red_df[timestamp_tag_column]))
        
            print("\n")
    
    # specification_limits = {'lower_spec_lim': value1, 'upper_spec_lim': value2}
    
    # Check if there is a lower specification limit:
    if (specification_limits['lower_spec_lim'] is not None):
        
        lower_spec_lim = specification_limits['lower_spec_lim']
        
        # Now, add a column to inform if each point is in or out of the specification limits.
        # apply a filter to select each situation:

        # Start the new column as 'in_spec_lim' (default case):
        df['spec_limits_check'] = 'in_spec_lim'
        # Now modify only points which are below the specification limit:
        df.loc[(df[column_with_variable_to_be_analyzed] < lower_spec_lim), 'spec_limits_check'] = 'below_lower_spec_lim'
    
        if (len(df[(df[column_with_variable_to_be_analyzed] < lower_spec_lim)]) > 0):
            
            print("Attention! Point below lower specification limit.")
            print("Check the returned dataframe df to obtain more details.\n")
        
        # Check if there is an upper specification limit too:
        if (specification_limits['upper_spec_lim'] is not None):

            upper_spec_lim = specification_limits['upper_spec_lim']

            # Now modify only points which are above the specification limit:
            df.loc[(df[column_with_variable_to_be_analyzed] > upper_spec_lim), 'spec_limits_check'] = 'above_upper_spec_lim'

            if (len(df[(df[column_with_variable_to_be_analyzed] > upper_spec_lim)]) > 0):

                print("Attention! Point above upper specification limit.")
                print("Check the returned dataframe df to obtain more details.\n")
    
    # Check the case where there is no lower, but there is a specification limit:
    elif (specification_limits['upper_spec_lim'] is not None):
        
        upper_spec_lim = specification_limits['upper_spec_lim']
        
        # Start the new column as 'in_spec_lim' (default case):
        df['spec_limits_check'] = 'in_spec_lim'
        
        # Now modify only points which are above the specification limit:
        df.loc[(df[column_with_variable_to_be_analyzed] > upper_spec_lim), 'spec_limits_check'] = 'above_upper_spec_lim'

        if (len(df[(df[column_with_variable_to_be_analyzed] > upper_spec_lim)]) > 0):

            print("Attention! Point above upper specification limit.")
            print("Check the returned dataframe df to obtain more details.\n")
    
    
    # Now, we have the final dataframe containing analysis regarding the control and specification
    # limits, and the red_df, that will be used to plot red points for values outside the control
    # range. Then, we can plot the graph.
    
    # Now, we can plot the figure.
    # we set alpha = 0.95 (opacity) to give a degree of transparency (5%), 
    # so that one series do not completely block the visualization of the other.
        
    # Matplotlib linestyle:
    # https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html?msclkid=68737f24d16011eca9e9c4b41313f1ad

    if ControlVars.show_plots:  
        if (plot_title is None):
            
            if (chart_to_use == 'g'):
                plot_title = f"{chart_to_use}_for_count_of_events_between_rare_occurence"
            
            elif (chart_to_use == 't'):
                plot_title = f"{chart_to_use}_for_timedelta_between_rare_occurence"
            
            else:
                plot_title = f"{chart_to_use}_for_{column_with_variable_to_be_analyzed}"
        
        if ((column_with_labels_or_subgroups is None) | (len(unique_labels) <= 1)):
            
            # 'i_mr' or, 'std_error', or '3s_as_natural_variation' (individual measurements)
            
            LABEL = column_with_variable_to_be_analyzed
            
            if (chart_to_use == 'i_mr'):
                LABEL_MEAN = 'mean'
                
            elif ((chart_to_use == '3s_as_natural_variation')|(chart_to_use == 'std_error')):
                if(consider_skewed_dist_when_estimating_with_std):
                    LABEL_MEAN = 'median'

                else:
                    LABEL_MEAN = 'mean'
            
            else:
                
                if (chart_to_use == 'g'):
                    LABEL = 'count_between\nrare_events'
                    LABEL_MEAN = 'median'
                
                elif (chart_to_use == 't'):
                    LABEL = 'timedelta_between\nrare_events'
                    LABEL_MEAN = 'central_line'
                    
        else:
            if ((chart_to_use == '3s_as_natural_variation')|(chart_to_use == 'std_error')):
                
                LABEL = "mean_value\nby_label"
                
                if(consider_skewed_dist_when_estimating_with_std):
                    LABEL_MEAN = 'median'
                else:
                    LABEL_MEAN = 'mean'
            
            elif (chart_to_use == 'xbar_s'):
                
                LABEL = "mean_value\nby_label"
                LABEL_MEAN = 'mean'
                
            elif (chart_to_use == 'np'):
                
                LABEL = "total_occurences\nby_label"
                LABEL_MEAN = 'sum_of_ocurrences'
                
            elif (chart_to_use == 'p'):
                
                LABEL = "mean_value\ngrouped_by_label"
                LABEL_MEAN = 'mean'
            
            elif (chart_to_use == 'u'):
                
                LABEL = "mean_value\ngrouped_by_label"
                LABEL_MEAN = 'mean'
                
            else:
                # chart_to_use == 'c'
                LABEL = "total_occurences\nby_label"
                LABEL_MEAN = 'average_sum\nof_ocurrences'
        
        x = df[timestamp_tag_column]
        
        y = df[column_with_variable_to_be_analyzed]  
        upper_control_lim = df['upper_cl']
        lower_control_lim = df['lower_cl']
        mean_line = df['center']
        
        if (specification_limits['lower_spec_lim'] is not None):
            
            lower_spec_lim = specification_limits['lower_spec_lim']
        
        else:
            lower_spec_lim = None
        
        if (specification_limits['upper_spec_lim'] is not None):
            
            upper_spec_lim = specification_limits['upper_spec_lim']
        
        else:
            upper_spec_lim = None
        
        if (len(red_df) > 0):
            
            red_x = red_df[timestamp_tag_column]
            red_y = red_df[column_with_variable_to_be_analyzed]
            
        # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
        # so that the bars do not completely block other views.
        OPACITY = 0.95
            
        #Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
        fig = plt.figure(figsize = (12, 8))
        ax = fig.add_subplot()
        
        #ROTATE X AXIS IN XX DEGREES
        plt.xticks(rotation = x_axis_rotation)
        # XX = 0 DEGREES x_axis (Default)
        #ROTATE Y AXIS IN XX DEGREES:
        plt.yticks(rotation = y_axis_rotation)
        # XX = 0 DEGREES y_axis (Default)
        
        # Set graphic title
        ax.set_title(plot_title) 

        if not (horizontal_axis_title is None):
            # Set horizontal axis title
            ax.set_xlabel(horizontal_axis_title)

        if not (vertical_axis_title is None):
            # Set vertical axis title
            ax.set_ylabel(vertical_axis_title)

        # Scatter plot of time series:
        ax.plot(x, y, linestyle = "-", marker = '', color = 'darkblue', alpha = OPACITY, label = LABEL)
        # Axes.plot documentation:
        # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html?msclkid=42bc92c1d13511eca8634a2c93ab89b5
                
        # x and y are positional arguments: they are specified by their position in function
        # call, not by an argument name like 'marker'.
                
        # Matplotlib markers:
        # https://matplotlib.org/stable/api/markers_api.html?msclkid=36c5eec5d16011ec9583a5777dc39d1f
        
        # Plot the mean line as a step function (values connected by straight splines, forming steps):
        ax.step(x, y = mean_line, color = 'fuchsia', linestyle = 'dashed', label = LABEL_MEAN, alpha = OPACITY)
        
        # Plot the control limits as step functions too:
        ax.step(x, y = upper_control_lim, color = 'crimson', linestyle = 'dashed', alpha = OPACITY, label = 'control\nlimit')
        ax.step(x, y = lower_control_lim, color = 'crimson', linestyle = 'dashed', alpha = OPACITY)
        
        # If there are specifications or reference values, plot as horizontal constant lines (axhlines):
        if (lower_spec_lim is not None):
            
            ax.axhline(lower_spec_lim, color = 'black', linestyle = 'dashed', label = 'specification\nlimit', alpha = OPACITY)
        
        if (upper_spec_lim is not None):
            
            ax.axhline(upper_spec_lim, color = 'black', linestyle = 'dashed', label = 'specification\nlimit', alpha = OPACITY)
        
        if (reference_value is not None):
            
            ax.axhline(reference_value, color = 'darkgreen', linestyle = 'dashed', label = 'reference\nvalue', alpha = OPACITY)   
        
        # If there are red points outside of control limits to highlight, plot them above the graph
        # (plot as scatter plot, with no spline, and 100% opacity = 1.0):
        if (len(red_df) > 0):
            
            ax.plot(red_x, red_y, linestyle = '', marker = 'o', color = 'firebrick', alpha = 1.0)
        
        # If the length of list time_of_event_frame_start is higher than zero,
        # loop through each element on the list and add a vertical constant line for the timestamp
        # correspondent to the beginning of an event frame:
        
        if (len(time_of_event_frame_start) > 0):
            
            for timestamp in time_of_event_frame_start:
                # add timestamp as a vertical line (axvline):
                ax.axvline(timestamp, color = 'aqua', linestyle = 'dashed', label = 'event_frame\nchange', alpha = OPACITY)
                
        # Now we finished plotting all of the series, we can set the general configuration:
        ax.grid(grid) # show grid or not
        ax.legend(loc = "lower left")

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
                file_name = f"control_chart_{chart_to_use}"

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
    
    return df, red_df


def process_capability (df, column_with_variable_to_be_analyzed, specification_limits = {'lower_spec_lim': None, 'upper_spec_lim': None}, reference_value = None, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    process_capability (df, column_with_variable_to_be_analyzed, specification_limits = {'lower_spec_lim': None, 'upper_spec_lim': None}, reference_value = None, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    : param: COLUMN_WITH_VARIABLE_TO_BE_ANALYZED: name (header) of the column containing the variable
      which stability will be analyzed by the control chart. The column name may be a string or a number.
      Example: COLUMN_WITH_VARIABLE_TO_BE_ANALYZED = 'analyzed_column' will analyze a column named
      "analyzed_column", whereas COLUMN_WITH_VARIABLE_TO_BE_ANALYZED = 'col1' will evaluate column 'col1'.

    : param: SPECIFICATION_LIMITS = {'lower_spec_lim': None, 'upper_spec_lim': None}
      If there are specification limits, input them in this dictionary. Do not modify the keys,
      simply substitute None by the lower and/or the upper specification.
      e.g. Suppose you have a tank that cannot have more than 10 L. So:
      SPECIFICATION_LIMITS = {'lower_spec_lim': None, 'upper_spec_lim': 10}, there is only
      an upper specification equals to 10 (do not add units);
      Suppose a temperature cannot be lower than 10 ºC, but there is no upper specification. So,
      SPECIFICATION_LIMITS = {'lower_spec_lim': 10, 'upper_spec_lim': None}. Finally, suppose
      a liquid which pH must be between 6.8 and 7.2:
      SPECIFICATION_LIMITS = {'lower_spec_lim': 6.8, 'upper_spec_lim': 7.2}

    : param: REFERENCE_VALUE: keep it as None or add a float value.
      This reference value will be shown as a red constant line to be compared
      with the plots. e.g. REFERENCE_VALUE = 1.0 will plot a line passing through
      VARIABLE_TO_ANALYZE = 1.0
    """

    from scipy import stats
    
    
    print("WARNING: this capability analysis is based on the strong hypothesis that data follows the normal (Gaussian) distribution.\n")
        
    # Set a local copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    
    # Sort by the column to analyze (ascending order) and reset the index:
    DATASET = DATASET.sort_values(by = column_with_variable_to_be_analyzed, ascending = True)
    
    DATASET = DATASET.reset_index(drop = True)
    
    # Create an instance (object) from class CapabilityAnalysis:
    capability_obj = CapabilityAnalysis(df = DATASET, column_with_variable_to_be_analyzed = column_with_variable_to_be_analyzed, specification_limits = specification_limits)
    
    # Check data normality:
    capability_obj = capability_obj.check_data_normality()
    # Attribute .normality_dict: dictionary with results from normality tests
    
    # Get histogram array:
    capability_obj = capability_obj.get_histogram_array()
    # Attribute .histogram_dict: dictionary with keys 'list_of_bins' and 'list_of_counts'.
    
    # Get desired normal:
    capability_obj = capability_obj.get_desired_normal()
    # Now the .specification_limits attribute contains the nested dict desired_normal = {'x': x_of_normal, 'y': y_normal}
    # in key 'desired_normal'.
    
    # Get the actual probability density function (PDF):
    capability_obj = capability_obj.get_actual_pdf()
    # Now the dictionary in the attribute .specification_limits has the nested dict actual_pdf = {'x': array_to_analyze, 'y': array_of_probs}
    # in key 'actual_pdf'.
    
    # Get capability indicators:
    capability_obj = capability_obj.get_capability_indicators()
    # Now the attribute capability_dict has a dictionary with the indicators, already in the format
    # for pandas DataFrame constructor.
    
    # Retrieve general statistics:
    stats_dict = {
        
        'sample_size': capability_obj.sample_size,
        'mu': capability_obj.mu,
        'median': capability_obj.median,
        'sigma': capability_obj.sigma,
        'lowest': capability_obj.lowest,
        'highest': capability_obj.highest
    }
    
    # Retrieve the normality summary:
    normality_dict = capability_obj.normality_dict
    # Nest this dictionary in stats_dict:
    stats_dict['normality_dict'] = normality_dict
    
    # Retrieve the histogram dict:
    histogram_dict = capability_obj.histogram_dict
    # Nest this dictionary in stats_dict:
    stats_dict['histogram_dict'] = histogram_dict
    
    # Retrieve the specification limits dictionary updated:
    specification_limits = capability_obj.specification_limits
    # Retrieve the desired normal and actual PDFs dictionaries:
    desired_normal = specification_limits['desired_normal']
    # Nest this dictionary in stats_dict:
    stats_dict['desired_normal'] = desired_normal
    
    actual_pdf = specification_limits['actual_pdf']
    # Nest this dictionary in stats_dict:
    stats_dict['actual_pdf'] = actual_pdf
    
    # Retrieve the capability dictionary:
    capability_dict = capability_obj.capability_dict
    # Create a capability dataframe:
    capability_df = pd.DataFrame(data = capability_dict)
    # Set column 'indicator' as index:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.set_index.html
    capability_df.set_index('indicator', inplace = True)
    # Nest this dataframe in stats_dict:
    stats_dict['capability_df'] = capability_df
    
    if ControlVars.show_results: 
        print("\n")
        print("Check the capability summary dataframe:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(capability_df)
                
        except: # regular mode
            print(capability_df)
    
    # Print the indicators' interpretation:
    capability_obj.capability_interpretation()
    
    if ControlVars.show_plots: 
        string_for_title = " - $\mu = %.2f$, $\sigma = %.2f$" %(stats_dict['mu'], stats_dict['sigma'])
        
        if (plot_title is not None):
            plot_title = plot_title + string_for_title
            
        else:
            # Set graphic title
            plot_title = f"Process Capability" + string_for_title

        if (horizontal_axis_title is None):
            # Set horizontal axis title
            horizontal_axis_title = column_with_variable_to_be_analyzed

        if (vertical_axis_title is None):
            # Set vertical axis title
            vertical_axis_title = "Counting/Frequency"
            
        y_hist = DATASET[column_with_variable_to_be_analyzed]
        number_of_bins = histogram_dict['number_of_bins']
        
        upper_spec = specification_limits['upper_spec_lim']
        lower_spec = specification_limits['lower_spec_lim']
        target = (upper_spec + lower_spec)/2 # center of the specification range
        
        # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
        # so that the bars do not completely block other views.
        OPACITY = 0.95
        
        # Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
        fig = plt.figure(figsize = (12, 8))
        ax = fig.add_subplot()
        
        #STANDARD MATPLOTLIB METHOD:
        #bins = number of bins (intervals) of the histogram. Adjust it manually
        #increasing bins will increase the histogram's resolution, but height of bars
        
        ax.hist(y_hist, bins = number_of_bins, alpha = OPACITY, label = f'counting_of\n{column_with_variable_to_be_analyzed}', color = 'darkblue')
        
        # desired_normal = {'x': x_of_normal, 'y': y_normal}
        # actual_pdf = {'x': array_to_analyze, 'y': array_of_probs}
        
        # Plot the probability density function for the data:
        pdf_x = actual_pdf['x']
        pdf_y = actual_pdf['y']
        
        ax.plot(pdf_x, pdf_y, color = 'darkgreen', linestyle = '-', alpha = OPACITY, label = 'probability\ndensity')
        
        # Check if a normal curve was obtained:
        x_of_normal = desired_normal['x']
        y_normal = desired_normal['y']
        
        if (len(x_of_normal) > 0):
            # Non-empty list, add the normal curve:
            ax.plot(x_of_normal, y_normal, color = 'crimson', linestyle = 'dashed', alpha = OPACITY, label = 'expected\nnormal_curve')
        
        # Add the specification limits and target vertical lines (axvline):
        ax.axvline(upper_spec, color = 'black', linestyle = 'dashed', label = 'specification\nlimit', alpha = OPACITY)
        ax.axvline(lower_spec, color = 'black', linestyle = 'dashed', alpha = OPACITY)
        ax.axvline(target, color = 'aqua', linestyle = 'dashed', label = 'target\nvalue', alpha = OPACITY)

        # If there is a reference value, plot it as a vertical line:
        if (reference_value is not None):
            ax.axvline(reference_value, color = 'fuchsia', linestyle = 'dashed', label = 'reference\nvalue', alpha = OPACITY)
        
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
                file_name = "capability_plot"

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

    return stats_dict
