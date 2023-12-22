import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from idsw.datafetch.core import InvalidInputsError
from .joinandgroup import union_dataframes
from .timestamps import calculate_delay


def lag_diagnosis (df, column_to_analyze, number_of_lags = 40, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    lag_diagnosis (df, column_to_analyze, number_of_lags = 40, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
 
    : param: df: the whole dataframe to be processed.
    
    : param: column_to_analyze: string (inside quotes), 
      containing the name of the column that will be analyzed. 
      e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    : param:number_of_lags: integer value. e.g. number_of_lags = 50
      represents how much lags will be tested, and the length of the horizontal axis.
    """

    import statsmodels.api as sm
   
    # Set a copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    
    #Define the series to be analyzed:
    y = DATASET[column_to_analyze]
    
    #Create the figure:
    fig = plt.figure(figsize = (12, 8)) 
    ax1 = fig.add_subplot(211)
    #ax1.set_xlabel("Lags")
    ax1.set_ylabel("Autocorrelation_Function_ACF")
    
    #ROTATE X AXIS IN XX DEGREES
    plt.xticks(rotation = x_axis_rotation)
    # XX = 0 DEGREES x_axis (Default)
    #ROTATE Y AXIS IN XX DEGREES:
    plt.yticks(rotation = y_axis_rotation)
    # XX = 0 DEGREES y_axis (Default)
    
    ax1.grid(grid)
    
    fig = sm.graphics.tsa.plot_acf(y.values.squeeze(), lags = number_of_lags, ax = ax1, color = 'darkblue')
    ax2 = fig.add_subplot(212)
    fig = sm.graphics.tsa.plot_pacf(y, lags = number_of_lags, ax = ax2, color = 'darkblue', method = 'ywm')
    ax2.set_xlabel("Lags")
    ax2.set_ylabel("Partial_Autocorrelation_Function_PACF")
        
    #ROTATE X AXIS IN XX DEGREES
    plt.xticks(rotation = x_axis_rotation)
    # XX = 0 DEGREES x_axis (Default)
    #ROTATE Y AXIS IN XX DEGREES:
    plt.yticks(rotation = y_axis_rotation)
    # XX = 0 DEGREES y_axis (Default)
    
    ax2.grid(grid)
        
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
            file_name = "lag_diagnosis"

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
    
    #fig.tight_layout()

    ## Show an image read from an image file:
    ## import matplotlib.image as pltimg
    ## img=pltimg.imread('mydecisiontree.png')
    ## imgplot = plt.imshow(img)
    ## See linkedIn Learning course: "Supervised machine learning and the technology boom",
    ##  Ex_Files_Supervised_Learning, Exercise Files, lesson '03. Decision Trees', '03_05', 
    ##  '03_05_END.ipynb'
    plt.show()
    
    #Print background and interpretation of the graphic:
    print("\n") #line break
    print("Use this plot to define the parameters (p, q) for testing ARIMA and ARMA models.\n")
    print("p defines the order of the autoregressive part (AR) of the time series.")
    print("p = lags correspondent to the spikes of PACF plot (2nd plot) that are outside the error (blue region).\n")
    print("For instance, if there are spikes in both lag = 1 and lag = 2, then p = 2, or p = 1\n")
    print("q defines the order of the moving average part (MA) of the time series.")
    print("q = lags correspondent to the spikes of ACF plot that are outside blue region.\n")
    print("For instance, if all spikes until lag = 6 are outside the blue region, then q = 1, 2, 3, 4, 5, 6.\n")
    print("WARNING: do not test the ARIMA/ARMA model for p = 0, or q = 0.")
    print("For lag = 0, the correlation and partial correlation coefficients are always equal to 1, because the data is always perfectly correlated to itself.") 
    print("Therefore, ignore the first spikes (lag = 0) from ACF and PACF plots.")


def test_d_parameters (df, column_to_analyze, number_of_lags = 40, max_tested_d = 2, confidence_level = 0.95, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    test_d_parameters (df, column_to_analyze, number_of_lags = 40, max_tested_d = 2, confidence_level = 0.95, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):

    : param: df: the whole dataframe to be processed.
    
    : param: column_to_analyze: string (inside quotes), 
      containing the name of the column that will be analyzed. 
      e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    : param: max_tested_d: differential order (integer value)
      change the integer if you want to test other cases. By default, max_tested_d = 2, meaning
      that the values d = 0, 1, and 2 will be tested.
      If max_tested_d = 1, d = 0 and 1 will be tested.
      If max_tested_d = 3, d = 0, 1, 2, and 3 will be tested, and so on.
    
    : param: CONFIDENCE_LEVEL = 0.95 = 95% confidence
      Set CONFIDENCE_LEVEL = 0.90 to get 0.90 = 90% confidence in the analysis.
      Notice that, when less trust is needed, we can reduce CONFIDENCE_LEVEL 
      to get less restrictive results.
    
    : param: number_of_lags: integer value. e.g. number_of_lags = 50
      represents how much lags will be tested, and the length of the horizontal axis.
    """

    import statsmodels.api as sm
    from statsmodels.tsa.stattools import adfuller
    
    
    # Set a copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    
    #Define the series to be analyzed:
    time_series = DATASET[column_to_analyze]
    
    # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
    # so that the bars do not completely block other views.
    OPACITY = 0.95
    
    #Create the figure:
    # Original Series
    fig, axes = plt.subplots((max_tested_d + 1), 2, sharex = True, figsize = (12, 8)) 
    # sharex = share axis X
    # number of subplots equals to the total of orders tested (in this case, 2)
    # If max_tested_d = 2, we must have a subplot for d = 0, d = 1 and d = 2, i.e.,
    # wer need 3 subplots = max_tested_d + 1
    axes[0, 0].plot(time_series, color = 'darkblue', alpha = OPACITY); axes[0, 0].set_title('Original Series')
    sm.graphics.tsa.plot_acf(time_series, lags = number_of_lags, ax = axes[0, 1], color = 'darkblue', alpha = 0.30)
    
    #ROTATE X AXIS IN XX DEGREES
    plt.xticks(rotation = x_axis_rotation)
    # XX = 0 DEGREES x_axis (Default)
    #ROTATE Y AXIS IN XX DEGREES:
    plt.yticks(rotation = y_axis_rotation)
    # XX = 0 DEGREES y_axis (Default)
    
    axes[0, 0].grid(grid)
    
    # Create a subplot for each possible 'd'.
    # Notice that d = 0 was already tested.
    for i in range(1, (max_tested_d + 1)):
        # This loop goes from i = 1 to i = (max_tested_d + 1) - 1 = max_tested_d.
        # If max_tested_d = 2, this loop goes from i = 1 to i = 2.
        # If only one value was declared in range(X), then the loop would start from 0.
        
        # Difference the time series:
        time_series = time_series.diff()
        
        #the indexing of the list d goes from zero to len(d) - 1
        # 1st Differencing
        axes[i, 0].plot(time_series, color = 'darkblue', alpha = OPACITY); axes[i, 0].set_title('%d Order Differencing' %(i))
        sm.graphics.tsa.plot_acf(time_series.diff().dropna(), lags = number_of_lags, ax = axes[i, 1], color = 'darkblue', alpha = 0.30)
                
        #ROTATE X AXIS IN XX DEGREES
        plt.xticks(rotation = x_axis_rotation)
        # XX = 0 DEGREES x_axis (Default)
        #ROTATE Y AXIS IN XX DEGREES:
        plt.yticks(rotation = y_axis_rotation)
        # XX = 0 DEGREES y_axis (Default)

        axes[i, 0].grid(grid)
    
        print('ADF Statistic for %d Order Differencing' %(i))
        result = adfuller(time_series.dropna())
        print('ADF Statistic: %f' % result[0])
        print('p-value: %f' % result[1])
        print("Interpretation:")
        print("p-value: probability of verifying the tested event, given that the null hypothesis H0 is correct.")
        print("H0: the process is non-stationary.")

        if (result[1] < (1-confidence_level)):
            print("For a %.2f confidence level, the %d Order Difference is stationary." %(confidence_level, i))
            print("You may select d = %d\n" %(i))

        else:
            print("For a %.2f confidence level, the %d Order Difference is non-stationary.\n" %(confidence_level, i))
        
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
            file_name = "test_d_parameters"

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
    print("d = differentiation order for making the process stationary.\n")
    print("If d = N, then we have to make N successive differentiations.")
    print("A differentiation consists on substracting a signal Si from its previous signal Si-1.\n")
    print("Example: 1st-order differentiating consists on taking the differences on the original time series.")
    print("The 2nd-order, in turns, consists in differentiating the 1st-order differentiation series.")


def best_arima_model (df, column_to_analyze, p_vals, d, q_vals, timestamp_tag_column = None, confidence_level = 0.95, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    best_arima_model (df, column_to_analyze, p_vals, d, q_vals, timestamp_tag_column = None, confidence_level = 0.95, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    https://www.statsmodels.org/stable/generated/statsmodels.tsa.arima.model.ARIMAResults.html#statsmodels.tsa.arima.model.ARIMAResults
    https://www.statsmodels.org/stable/examples/notebooks/generated/tsa_arma_1.html?highlight=statsmodels%20graphics%20tsaplots%20plot_predict
    
    param: df: the whole dataframe to be processed.
    
    param: column_to_analyze: string (inside quotes), 
      containing the name of the column that will be analyzed. 
      e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    param: timestamp_tag_column = None - keep it as None if you do not want to inform the timestamps
      Alternatively, declare a string (inside quotes), 
      containing the name of the column containing the time information. 
      e.g. timestamp_tag_column = "DATE" will take the timestamps from column 'DATE'.
      If no column is provided, the index in the dataframe will be used.
    
    param: p_vals: list of integers correspondent to the lags (spikes) in the PACF plot.
      From function lag_diagnosis
    param: q_vals: list of integers correspondent to the lags (spikes) in ACF plot
      From function lag_diagnosis
    param: d = difference for making the process stationary
      From function test_d_parameters
    
    order = (p, d, q) - these are the parameters of the autoregression (p = 2), 
     integration (d = parameter selected in previous analysis), and
     moving average (q = 1, 2, 3, 4, 5, etc)
    d = 0 corresponds to the ARMA model
    
    WARNING: do not test the ARIMA/ARMA model for p = 0, or q = 0.
     For lag = 0, the correlation and partial correlation coefficients 
     are always equal to 1, because the data is perfectly correlated to itself. 
     Therefore, ignore the first spikes (lag = 0) of ACF and PACF plots.
    
    ALPHA = 1 - confidence_level
    param: CONFIDENCE_LEVEL = 0.95 = 95% confidence
      Set CONFIDENCE_LEVEL = 0.90 to get 0.90 = 90% confidence in the analysis.
      Notice that, when less trust is needed, we can reduce CONFIDENCE_LEVEL 
      to get less restrictive results.
    """

    import statsmodels as sm
    from statsmodels.graphics.tsaplots import plot_predict
    #this model is present only in the most recent versions of statsmodels

    from statsmodels.tsa.arima.model import ARIMA, ARIMAResults
    

    ALPHA = 1 - confidence_level
    
    # Set a copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    
    #x: timestamp or index series, if no timestamp is provided:
    if (timestamp_tag_column is None):
        #Use the indices of the dataframe
        x = DATASET.index
    
    else:
        #Use the timestamp properly converted to datetime (as in the graphics functions):
        x = (DATASET[timestamp_tag_column]).astype('datetime64[ns]')
        DATASET[timestamp_tag_column] = x
        # To pass the date to ARIMA model, we must specify it as the index, and also pass the
        # start and end dates
        DATASET = DATASET.set_index(timestamp_tag_column)
    
    #y: tested variable series
    y = DATASET[column_to_analyze]
    
    # date to start the plot (the second element from series x - we will ignore the first one):
    start_date = x[1]
    # last date to plot (last element from the series)
    end_date = x[(len(x) - 1)]
    print(f"ARIMA model from date (or measurement) = {start_date}; to date (or measurement) = {end_date}.\n")
    
    #calculate the first aic and bic
    #first argument = time series y
    
    returned_p = p_vals[0]
    returned_q = q_vals[0]
    returned_d = d
    #use the d-value selected in the non-stationary analysis.
    #set the integration in 
    #at this moment, the function simply returns the first elements.
    
    ARIMA_model = ARIMA(y, order = (returned_p, returned_d, returned_q))

    #order = (p, d, q) - these are the parameters of the autoregression (p = 2), 
    #integration (d = parameter selected in previous analysis), and
    #moving average (q = 1, 2, 3, 4, 5, etc)

    ARIMA_Results = ARIMA_model.fit()
    aic_val = ARIMA_Results.aic
    #AIC value for the first combination.
    bic_val = ARIMA_Results.bic
    #BIC value for the first combination, to start the loops.
    
    # Mean absolute error:
    mae = ARIMA_Results.mae
    # log likelihood calculated:
    loglikelihood = ARIMA_Results.llf
    
    returned_ARIMA_Results = ARIMA_Results
    #returned object
    
    for p in p_vals:
        #test each possible value for p (each d, p combination)
        #each p in p_vals list is used.
        for q in q_vals:
            #test each possible value for q (each p, d, q combination)
            #each q in q_vals list is used.
                
            ARIMA_model = ARIMA(y, order = (p, returned_d, q))
            ARIMA_Results = ARIMA_model.fit()
            aic_tested = ARIMA_Results.aic
            bic_tested = ARIMA_Results.bic
            mae_tested = ARIMA_Results.mae
            loglikelihood_tested = ARIMA_Results.llf
            
            if ((mae_tested < mae) & (abs(loglikelihood_tested) > abs(loglikelihood))):
                
                # Check if the absolute error was reduced and the likelihood was increased
                
                #if better parameters were found, they should be used
                #update AIC, BIC; the p, d, q returned values;
                #and the ARIMA_Results from the ARIMA:
                aic_val = aic_tested
                bic_val = bic_tested
                mae = mae_tested
                loglikelihood = loglikelihood_tested
                returned_p = p

                returned_q = q
                #return the Statsmodels object:
                returned_ARIMA_Results = ARIMA_Results
    
    #Create a dictionary containing the best parameters and the metrics AIC and BIC
    arima_summ_dict = {"p": returned_p, "d": returned_d, "q": returned_q,
                "AIC": returned_ARIMA_Results.aic, "BIC": returned_ARIMA_Results.bic,
                    "MAE": returned_ARIMA_Results.mae, "log_likelihood": returned_ARIMA_Results.llf}
    
    #Show ARIMA results:
    print(returned_ARIMA_Results.summary())
    print("\n")
    #Break the line and show the combination
    print("Best combination found: (p, d, q) = (%d, %d, %d)\n" %(returned_p, returned_d, returned_q))
    #Break the line and print the next indication:
    print(f"Time series, values predicted by the model, and the correspondent {confidence_level * 100}% Confidence interval for the predictions:\n")
    #Break the line and print the ARIMA graphic:
    
    # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
    # so that the bars do not completely block other views.
    OPACITY = 0.95
    
    #Start the figure:
    fig, ax = plt.subplots(figsize = (12, 8))
    # Add line of the actual values:
    ax.plot(x, y, linestyle = '-', marker = '', color = 'darkblue', label = column_to_analyze)
    # Use the name of the analyzed column as the label
    fig = plot_predict(returned_ARIMA_Results, start = start_date, end = end_date,  ax = ax, alpha = ALPHA)
    ## https://www.statsmodels.org/v0.12.2/generated/statsmodels.tsa.arima_model.ARIMAResults.plot_predict.html
    # ax = ax to plot the arima on the original plot of the time series
    # start = x[1]: starts the ARIMA graphic from the second point of the series x
    # if x is the index, then it will be from the second x; if x is a time series, then
    # x[1] will be the second timestamp
    #We defined the start in x[1], instead of index = 0, because the Confidence Interval for the 
    #first point is very larger than the others (there is perfect autocorrelation for lag = 0). 
    #Therefore, it would have resulted in the need for using a very broader y-scale, what
    #would compromise the visualization.
    # We could set another index or even a timestamp to start:
    # start=pd.to_datetime('1998-01-01')
    
    ax.set_alpha(OPACITY)
    
    if not (plot_title is None):
        #graphic's title
        ax.set_title(plot_title)
    
    else:
        #set a default title:
        ax.set_title("ARIMA_model")
    
    if not (horizontal_axis_title is None):
        #X-axis title
        ax.set_xlabel(horizontal_axis_title)
    
    else:
        #set a default title:
        ax.set_xlabel("Time")
    
    if not (vertical_axis_title is None):
        #Y-axis title
        ax.set_ylabel(vertical_axis_title)
    
    else:
        #set a default title:
        ax.set_ylabel(column_to_analyze)
    
    #ROTATE X AXIS IN XX DEGREES
    plt.xticks(rotation = x_axis_rotation)
    # XX = 70 DEGREES x_axis (Default)
    #ROTATE Y AXIS IN XX DEGREES:
    plt.yticks(rotation = y_axis_rotation)
    # XX = 0 DEGREES y_axis (Default)
    
    ax.grid(grid)
    ax.legend(loc = "upper left")
    
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
            file_name = "arima_model"

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
    
    #fig.tight_layout()

    ## Show an image read from an image file:
    ## import matplotlib.image as pltimg
    ## img=pltimg.imread('mydecisiontree.png')
    ## imgplot = plt.imshow(img)
    ## See linkedIn Learning course: "Supervised machine learning and the technology boom",
    ##  Ex_Files_Supervised_Learning, Exercise Files, lesson '03. Decision Trees', '03_05', 
    ##  '03_05_END.ipynb'
    plt.show()
    
    # Get dataframe with the predictions and confidence intervals
    arima_predictions = returned_ARIMA_Results.get_prediction(start = x[0], end = None, dynamic = False, full_results = True, alpha = ALPHA)
    # Here, we started in start = x[0] to obtain a correspondent full dataset, and did not set an end.
    # The start can be an integer representing the index of the data in the dataframe,
    # or a timestamp. Check:
    # https://www.statsmodels.org/devel/generated/statsmodels.tsa.arima.model.ARIMAResults.get_prediction.html#statsmodels.tsa.arima.model.ARIMAResults.get_prediction
    # Again, no matter if x is an index or a time series, x[0] starts from the first element
    # You could set another index or a oparticular timestamp to start, like:
    # start=pd.to_datetime('1998-01-01')
    # The dynamic = False argument ensures that we produce one-step ahead forecasts, 
    # meaning that forecasts at each point are generated using the full history up 
    # to that point.
    predicted_mean_vals = arima_predictions.predicted_mean
    predicted_conf_intervals = arima_predictions.conf_int(alpha = ALPHA)
    # predicted_conf_intervals has two columns: first one is the inferior confidence limit
    # second one is the superior confidence limit
    # each column from this dataframe gets a name derived from the name of the original series.
    # So, let's rename them:
    predicted_conf_intervals.columns = ['lower_cl', 'upper_cl']
    
    # let's create a copy of the dataframe to be returned with the new information:
    # This will avoid manipulating the df:
    arima_df = DATASET.copy(deep = True)
    # This DATASET already contains the timestamp column as the index, so it is adequate for
    # obtaining predictions associated to the correct time values.
    
    #create a column for the predictions:
    arima_df['arima_predictions'] = predicted_mean_vals
    
    #create a column for the inferior (lower) confidence interval.
    # Copy all the rows from the column 0 of predicted_conf_intervals
    arima_df['lower_cl'] = predicted_conf_intervals['lower_cl']
    
    #create a column for the superior (upper) confidence interval.
    # Copy all the rows from the column 1 of predicted_conf_intervals
    arima_df['upper_cl'] = predicted_conf_intervals['upper_cl']
    
    # Let's turn again the timestamps into a column, restart the indices and re-order the columns,
    # so that the last column will be the response, followed by ARIMA predictions
    
    ordered_columns_list = []
    
    if (timestamp_tag_column is not None):
        #Use the indices of the dataframe
        ordered_columns_list.append(timestamp_tag_column)
        # Create a timestamp_tag_column in the dataframe containing the values in the index:
        arima_df[timestamp_tag_column] = np.array(arima_df.index)
        # Reset the indices from the dataframe:
        arima_df = arima_df.reset_index(drop = True)
    
    # create a list of columns with fixed position:
    fixed_columns_list = [column_to_analyze, 'arima_predictions', 'lower_cl', 'upper_cl']
    
    # Now, loop through all the columns:
    for column in list(arima_df.columns):
        
        # If the column is not one from fixed_columns_list, and it is not on ordered_columns_list
        # yet, add it to ordered_columns_list (timestamp_tag_column may be on the list):
        if ((column not in fixed_columns_list) & (column not in ordered_columns_list)):
            ordered_columns_list.append(column)
    
    # Now, concatenate ordered_columns_list to fixed_columns_list. 
    # If a = ['a', 'b'] and b = ['c', 'd'], a + b = ['a', 'b', 'c', 'd'] and b + a = [ 'c', 'd', 'a', 'b']
    ordered_columns_list = ordered_columns_list + fixed_columns_list
    
    # Finally, select the columns from arima_df passing this list as argument:
    arima_df = arima_df[ordered_columns_list]
    print("\n")
    print("Check the dataframe containing the ARIMA predictions:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(arima_df)
            
    except: # regular mode
        print(arima_df)
    
    print("\n") #line break
    print("Notice that the presence of data outside the confidence interval limits of the ARIMA forecast is a strong indicative of outliers or of untrust time series.\n")
    print("For instance: if you observe a very sharp and sudden deviation from the predictive time series, it can be an indicative of incomplete information or outliers presence.\n")
    print("A famous case is the pandemic data: due to lags or latencies on the time needed for consolidating the information in some places, the data could be incomplete in a given day, leading to a sharp decrease that did not actually occurred.")
    
    print("\n")
    print("REMEMBER: q represents the moving average (MA) part of the time series.")
    print(f"Then, it is interesting to group the time series {column_to_analyze} by each q = {returned_q} periods when modelling or analyzing it.")
    print("For that, you can use moving window or rolling functions.\n")
    
    return returned_ARIMA_Results, arima_summ_dict, arima_df


def arima_forecasting (arima_model_object, df = None, column_to_forecast = None, timestamp_tag_column = None, time_unit = None, number_of_periods_to_forecast = 7, confidence_level = 0.95, plot_predicted_time_series = True, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    arima_forecasting (arima_model_object, df = None, column_to_forecast = None, timestamp_tag_column = None, time_unit = None, number_of_periods_to_forecast = 7, confidence_level = 0.95, plot_predicted_time_series = True, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):

    : param: arima_model_object : object containing the ARIMA model previously obtained.
      e.g. arima_model_object = returned_ARIMA_Results if the model was obtained as returned_ARIMA_Results
      do not declare in quotes, since it is an object, not a string.
    
    : param: time_unit: Unit of the new column. If no value is provided, the unit will be considered as nanoseconds. 
      Alternatively: keep it None, for the results in nanoseconds, or input time_unit = 
      'year', 'month', 'day', 'hour', 'minute', or 'second' (keep these inside quotes).
      It will be the input for the functions calculate_delay and add_timedelta.
    
    : param: number_of_periods_to_forecast = 7
      integer value representing the total of periods to forecast. The periods will be in the
      unit (dimension) of the original dataset. If 1 period = 1 day, 7 periods will represent
      seven days.
    
    Keep: 
    : param: plot_predicted_time_series = True to see the graphic of the predicted values.
      Alternatively, set plot_predicted_time_series = True not to show the plot.
    
      df = None, column_to_analyze = None - keep it as None if you do not want to show
      the ARIMA predictions combined to the original data; or if you do not want to append
      the ARIMA predictions to the original dataframe.
      Alternatively, set:
      df: the whole dataframe to be processed.
    
    : param: column_to_forecast: string (inside quotes), 
      containing the name of the column that will be analyzed.
      Keep it as None if the graphic of the predictions will not be shown with the
      responses or if the combined dataset will not be returned.
      e.g. column_to_forecast = "column1" will analyze and forecast values for 
      the column named as 'column1'.
    
    : param: timestamp_tag_column: string (inside quotes), 
      containing the name of the column containing timestamps.
      Keep it as None if the graphic of the predictions will not be shown with the
      responses or if the combined dataset will not be returned.
      e.g. timestamp_tag_column = "column1" will analyze the column named as 'column1'.
    
    ARIMA predictions:
      The .forecast and .predict methods only produce point predictions:
       y_forecast = ARIMA_Results.forecast(7) results in a group of values (7 predictions)
       without the confidence intervals
       On the other hand, the .get_forecast and .get_prediction methods 
       produce full results including prediction intervals.

       In our example, we can do:
       forecast = ARIMA_Results.get_forecast(123)
       yhat = forecast.predicted_mean
       yhat_conf_int = forecast.conf_int(alpha=0.05)
       If your data is a Pandas Series, then yhat_conf_int will be a DataFrame with 
       two columns, lower <name> and upper <name>, where <name> is the name of the Pandas 
       Series.
       If your data is a numpy array (or Python list), then yhat_conf_int will be an 
       (n_forecasts, 2) array, where the first column is the lower part of the interval 
       and the second column is the upper part.
    
    ALPHA = 1 - confidence_level
    : param: CONFIDENCE_LEVEL = 0.95 = 95% confidence
      Set CONFIDENCE_LEVEL = 0.90 to get 0.90 = 90% confidence in the analysis.
      Notice that, when less trust is needed, we can reduce CONFIDENCE_LEVEL 
      to get less restrictive results.
    """

    import statsmodels as sm
    from statsmodels.graphics.tsaplots import plot_predict
    #this model is present only in the most recent versions of statsmodels

    from statsmodels.tsa.arima.model import ARIMA, ARIMAResults
    

    numeric_data_types = [np.float16, np.float32, np.float64, np.int16, np.int32, np.int64]
    
    ALPHA = 1 - confidence_level
    
    # Calculate the predictions:
    # It does not depend on the presence of a dataframe df
    # https://www.statsmodels.org/devel/generated/statsmodels.tsa.arima.model.ARIMAResults.get_forecast.html#statsmodels.tsa.arima.model.ARIMAResults.get_forecast
    
    arima_forecasts = arima_model_object.get_forecast(number_of_periods_to_forecast, dynamic = False, full_results = True, alpha = ALPHA)
    
    forecast_mean_vals = arima_forecasts.predicted_mean
    forecast_conf_intervals = arima_forecasts.conf_int(alpha = ALPHA)
    # forecast_conf_intervals has two columns: first one is the inferior confidence limit
    # second one is the superior confidence limit
    # each column from this dataframe gets a name derived from the name of the original series.
    # So, let's rename them:
    forecast_conf_intervals.columns = ['lower_cl', 'upper_cl']
    
    #create a series for the inferior confidence interval.
    lower_cl = forecast_conf_intervals['lower_cl'].copy(deep = True)
    #create a series for the superior confidence interval.
    upper_cl = forecast_conf_intervals['upper_cl'].copy(deep = True)
    
    # If there is no df, we can already obtain a X series, that will be a series of indices
    # starting from period 1 (the first forecast. Period zero corresponds to the last actual value):
    if (df is None):
        
        x_forecast = []
        
        for j in range (1, (number_of_periods_to_forecast + 1)):
            #Goes from j = 1, the first forecast period; to j = (number_of_periods_to_forecast+1)-1
            # = number_of_periods_to_forecast, which must be the last forecast.
            x_forecast.append(j)
        
        # Now, create the dictionary of forecasts:
        forecast_dict = {
            
            "x": x_forecast,
            "forecast_mean_vals": forecast_mean_vals,
            "lower_cl": lower_cl,
            "upper_cl": upper_cl,
            'source': 'forecast'
        }
        
        # Convert it to a dataframe:
        forecast_df = pd.DataFrame(data = forecast_dict)
        x_forecast_series = forecast_df['x']
        y_forecast_series = forecast_df['forecast_mean_vals']
        lcl_series = forecast_df['lower_cl']
        ucl_series = forecast_df['upper_cl']
    
    
    # If there is a dataframe df, we must combine the original data from df
    # with the new predictions:
    else:
        
        # Start a dataset copy to manipulate:
        DATASET = df.copy(deep = True)
        
        # Create a column with a label indicating that the data in DATASET (before concatenation 
        # with predictions) is from the original dataframe:
        DATASET['source'] = 'input_dataframe'
        # In turns, The source column in the dataframe from the forecasts will 
        # be labelled with the string 'forecast'
        
        # Check if a column_to_forecast was indicated in the input dataframe:
        if not (column_to_forecast is None):
            
            # If there is a response column indicated, then the forecast column of the 
            # generated predictions must be stored in a column with the exact same name, so that
            # the columns can be correctly appended
            y_forecast_label = column_to_forecast
            # Also, create a separate series for the original data, that will be used for
            # differentiating between data and forecasts on the plot:
            y_original_series = DATASET[column_to_forecast].copy(deep = True)
        
        # If no column was indicated, set a default column name for the forecasts:
        else:
            # Set the default name:
            y_forecast_label = "y_forecast"
        
        
        # Check if a timestamp_tag_column was input. If not, use the indices themselves as times.
        # Create a new standard name for the column in forecasts:
        if (timestamp_tag_column is None):
            
            # Let's set an index series as the index of the dataframe:
            DATASET['index_series'] = DATASET.index
            # Check if this series contains an object. If it has, then, user set the timestamps
            # as the indices
            index_series_type = DATASET['index_series'].dtype
            
            # If it is an object, the user may be trying to pass the date as index. 
            # So, let's try to convert it to datetime:
            if ((index_series_type not in numeric_data_types) | (index_series_type == 'O') | (index_series_type == 'object')):
                
                try:
                    DATASET['index_series'] = (DATASET['index_series']).astype('datetime64[ns]')
                    
                    # Rename column 'index_series':
                    # https://www.statology.org/pandas-rename-columns/
                    DATASET.rename(columns = {'index_series': 'timestamp'}, inplace = True)
                    # Set 'timestamp' as the timestamp_tag_column:
                    timestamp_tag_column = 'timestamp'
                    
                except:
                    # A variable that is not neither numeric nor date was passed. Reset the index:
                    DATASET = DATASET.reset_index(drop = True)
                    # Update the index series
                    DATASET['index_series'] = DATASET.index
                    
            # Now, try to manipulate the 'index_series'. An exception will be raised in case
            # the name was changed because the index contains a timestamp
            try:
                
                # convert the 'index_series' to the default name for column X:
                x_forecast_label  = "x_forecast"
                DATASET.rename(columns = {'index_series': x_forecast_label}, inplace = True)
                x_original_series = DATASET[x_forecast_label].copy(deep = True)
            
                # Let's create the series for forecasted X. Simply add more values to x
                # until reaching the number_of_periods_to_forecast:
            
                # Get the value of the last X of the dataframe
                # index start from zero, so the last one is length - 1
                last_x = x_original_series[(len(x_original_series) - 1)]

                #Start the list
                x_forecast = []

                #Append its first value: last X plus 1 period
                x_forecast.append(last_x + 1)
            
                j = 1
                while (j < number_of_periods_to_forecast):
                    #Last cycle occurs when j == number_of_periods_to_forecast - 1
                    # Since indexing starts from zero, there will be number_of_periods_to_forecast
                    # elements in the list.
                    # Also, we already added the first period, so we are starting from the 2nd
                    # forecast period, j = 1.
                    x_forecast.append((x_forecast[(j - 1)] + 1))

                    #Go to next iteration:
                    j = j + 1
                
                # Now, x_forecast stores the next indices for the situation where no timestamp
                # was provided initially.
            
            except:
                #simply pass
                pass
        
        
        # Again, check if timestamp_tag_column is None. It may have changed, since we created a value
        # for the case where a timestamp is in the index. So, we will not use else: the else would
        # ignore the modification in the first if:
        
        if not (timestamp_tag_column is None):
            # Use the timestamp properly converted to datetime (as in the graphics functions).
            # The labels must be the same for when the dataframes are merged.
            x_forecast_label  = timestamp_tag_column
            
            # Check if it is an object or is not a numeric variable (e.g. if it is a timestamp):
            if ((DATASET[timestamp_tag_column].dtype not in numeric_data_types) | (DATASET[timestamp_tag_column].dtype == 'O') | (DATASET[timestamp_tag_column].dtype == 'object')):
                
                # Try to convert it to np.datetime64
                try:

                    DATASET[timestamp_tag_column] = (DATASET[timestamp_tag_column]).astype('datetime64[ns]')
                
                except:
                    pass
                
            # Now, timestamp is either a numeric column or a datetime column.
            # Again, create a separate series for the original data, that will be used for
            # differentiating between data and forecasts on the plot:
            x_original_series = DATASET[timestamp_tag_column].copy(deep = True)
            
            # Get the last X of the dataframe
            # index start from zero, so the last one is length - 1
            last_x = x_original_series[(len(x_original_series) - 1)]
            
            # Check the case where it is a timestamp:
            if (type(np.array(x_original_series)[0]) == np.datetime64):
                
                # Let's obtain the mean value of the timedeltas between each measurement:
                TIMESTAMP_TAG_COLUMN = timestamp_tag_column
                NEW_TIMEDELTA_COLUMN_NAME = None
                RETURNED_TIMEDELTA_UNIT = time_unit
                # If it is none, the value will be returned in nanoseconds.
                # keep it None, for the results in nanoseconds
                RETURN_AVG_DELAY = True
                _, avg_delay = calculate_delay (df = DATASET, timestamp_tag_column = TIMESTAMP_TAG_COLUMN, new_timedelta_column_name  = NEW_TIMEDELTA_COLUMN_NAME, returned_timedelta_unit = RETURNED_TIMEDELTA_UNIT, return_avg_delay = RETURN_AVG_DELAY)
                # The underscore indicates that we will not keep the returned dataframe
                # only the average time delay in nanoseconds.
                print("\n")
                print(f"Average delay on the original time series, used for obtaining times of predicted values = {avg_delay}.\n")

                # Now, avg_delay stores the mean time difference between successive measurements from the
                # original dataset.
            
                # Now, let's create the prediction timestamps, by adding the avg_delay to
                # the last X.
                # Firstly, convert last_x to a Pandas timestamp, so that we can add a pandas
                # timedelta:
                last_x = pd.Timestamp(last_x, unit = 'ns')
            
                # Now, let's create a pandas timedelta object correspondent to avg_delay
                # 1. Check units:
                if (time_unit is None):
                    time_unit = 'ns'
            
                # Notice that calculate_delay and add_timedelta update the unit for us, but
                # such functions deal with a dataframe, not with a single value. So, we are
                # using a small piece from add_timedelta function to operate with a single
                # timestamp.

                #2. Create the pandas timedelta object:
                timedelta = pd.Timedelta(avg_delay, time_unit)
            
                #3. Let's create the values of timestamps correspondent to the forecast
                x_forecast = []
                # The number of elements of this list is number_of_periods_to_forecast
                # if number_of_periods_to_forecast, we will forecast a single period further,
                # then we need to sum timedelta once. If number_of_periods_to_forecast = 3,
                # we will sum timedelta 3 times, and so on.
            
                # Append the first element (last element + timedelta) - first value forecast
                x_forecast.append((last_x + timedelta))
            
                j = 1
                while (j < number_of_periods_to_forecast):
                    #Last cycle occurs when j == number_of_periods_to_forecast - 1
                    # Since indexing starts from zero, there will be number_of_periods_to_forecast
                    # elements in the list.
                    # Also, we already added the first period, so we are starting from the 2nd
                    # forecast period, j = 1.

                    # append the previous element + timedelta.
                    # If j = 1, (j - 1) = 0, the first element
                    x_forecast.append((x_forecast[(j - 1)] + timedelta))
                
                    #Go to next iteration:
                    j = j + 1
        
                # Now, x_forecast stores the values of timestamps correspondent to
                # the forecasts.
                # Convert x_forecast to Pandas Series, so that it will be possible to perform vectorial
                # operations:
                x_forecast = pd.Series(x_forecast)
                # Convert it to datetime64:
                x_forecast = (x_forecast).astype('datetime64[ns]')
            
            else:
                # We have a numerical variable used as time. We have to calculate the average 'delay' between
                # Successive values. For that, we can again use Pandas.diff method, which may be applied to
                # Series or DataFrames
                # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.diff.html
                # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.diff.html#pandas.Series.diff
                
                x_diff_series = x_original_series.copy(deep = True)
                x_diff_series = x_diff_series.diff(periods = 1)
                # periods - int, default 1 - Periods to shift for calculating difference, accepts negative values.
                
                # Now, get the average delay as the mean value from series x_diff_series:
                avg_delay = x_diff_series.mean()
                print("\n")
                print(f"Average delay on the original time series, used for obtaining times of predicted values = {avg_delay}.\n")
                
                # Let's create the values of times correspondent to the forecast
                x_forecast = []
                # The number of elements of this list is number_of_periods_to_forecast
                # if number_of_periods_to_forecast, we will forecast a single period further,
                # then we need to sum timedelta once. If number_of_periods_to_forecast = 3,
                # we will sum timedelta 3 times, and so on.
            
                # Append the first element (last element + avg_delay) - first value forecast
                x_forecast.append((last_x + avg_delay))
            
                j = 1
                while (j < number_of_periods_to_forecast):
                    #Last cycle occurs when j == number_of_periods_to_forecast - 1
                    # Since indexing starts from zero, there will be number_of_periods_to_forecast
                    # elements in the list.
                    # Also, we already added the first period, so we are starting from the 2nd
                    # forecast period, j = 1.

                    # append the previous element + timedelta.
                    # If j = 1, (j - 1) = 0, the first element
                    x_forecast.append((x_forecast[(j - 1)] + avg_delay))
                
                    #Go to next iteration:
                    j = j + 1
                
        # Notice that all these steps are possible only when the timestamps were
        # given, and so they should not be executed if the values are not provided.
        
        
        # Now, steps are the same for all cases where there is a dataframe (Main Else node that we are evaluating): 
        # create the dictionary of forecasts:
        forecast_dict = {

            x_forecast_label: x_forecast,
            y_forecast_label: forecast_mean_vals,
            "lower_cl": lower_cl,
            "upper_cl": upper_cl,
            'source': 'forecast'
        }

        # Convert it to a dataframe:
        forecast_df = pd.DataFrame(data = forecast_dict)
        x_forecast_series = forecast_df[x_forecast_label]
        y_forecast_series = forecast_df[y_forecast_label]
        lcl_series = forecast_df['lower_cl']
        ucl_series = forecast_df['upper_cl']

        # Now, let's concatenate the new dataframe to the old one.
        # The use of the variables 'source', x_ and y_forecast_label guarantees that the new
        # columns have the same name as the ones of the original dataframe, so that
        # the concatenation is performed correctly.

        # Now, merge the dataframes:
        LIST_OF_DATAFRAMES = [DATASET, forecast_df]
        IGNORE_INDEX_ON_UNION = True
        SORT_VALUES_ON_UNION = True
        UNION_JOIN_TYPE = None
        forecast_df = union_dataframes (list_of_dataframes = LIST_OF_DATAFRAMES, ignore_index_on_union = IGNORE_INDEX_ON_UNION, sort_values_on_union = SORT_VALUES_ON_UNION, union_join_type = UNION_JOIN_TYPE)
        
        # Full series, with input data and forecasts:
        x = forecast_df[x_forecast_label]
        y = forecast_df[y_forecast_label]
        
        # Now, let's re-order the dataframe, putting the x_forecast_label as the first column
        # and y_forecast_label: forecast_mean_vals, "lower_cl", "upper_cl", and 'source'
        # as the last ones.
        
        # Set a list of the last columns (fixed positions):
        fixed_columns_list = [y_forecast_label, 'lower_cl', 'upper_cl', 'source']
        
        # Start the list with only x_forecast_label:
        ordered_columns_list = [x_forecast_label]
        
        # Now, loop through all the columns:
        for column in list(forecast_df.columns):

            # If the column is not one from fixed_columns_list, and it is not on ordered_columns_list
            # yet, add it to ordered_columns_list (timestamp_tag_column may be on the list):
            if ((column not in fixed_columns_list) & (column not in ordered_columns_list)):
                ordered_columns_list.append(column)
        
        # Now, concatenate ordered_columns_list to fixed_columns_list. 
        # If a = ['a', 'b'] and b = ['c', 'd'], a + b = ['a', 'b', 'c', 'd'] and b + a = [ 'c', 'd', 'a', 'b']
        ordered_columns_list = ordered_columns_list + fixed_columns_list
        
        # Finally, pass ordered_columns_list as argument for column filtering and re-order:
        forecast_df = forecast_df[ordered_columns_list]

        
    # We are finally in the general case, after obtaining the dataframe through all possible ways:
    print(f"Finished the obtention of the forecast dataset. Check the 10 last rows of the forecast dataset:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(forecast_df.tail(10))
            
    except: # regular mode
        print(forecast_df.tail(10))
        
    
    # Now, let's create the graphics
    if (plot_predicted_time_series == True):
        
        LINE_STYLE = '-'
        MARKER = ''
        
        if (plot_title is None):
            # Set graphic title
            plot_title = f"ARIMA_forecasts"

        if (horizontal_axis_title is None):
            # Set horizontal axis title
            if (timestamp_tag_column is None):
                horizontal_axis_title = "timestamp"
            else:
                horizontal_axis_title = timestamp_tag_column

        if (vertical_axis_title is None):
            if (column_to_forecast is None):
                vertical_axis_title = "time_series"
            else:
                vertical_axis_title = column_to_forecast
        
        # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
        # so that the bars do not completely block other views.
        OPACITY = 0.95
        
        #Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
        fig = plt.figure(figsize = (12, 8))
        ax = fig.add_subplot()
        
        if ((df is not None) & ((column_to_forecast is not None))):
            
            # Plot the original data series:
            ax.plot(x, y, linestyle = LINE_STYLE, marker = MARKER, color = 'darkblue', alpha = OPACITY, label = 'input_dataframe')
        
        # Plot the predictions (completely opaque, so that the input data series will not be
        # visible)
        ax.plot(x_forecast_series, y_forecast_series, linestyle = LINE_STYLE, marker = MARKER, color = 'red', alpha = 1.0, label = 'forecast')
        
        # Plot the confidence limits:
        ax.plot(x_forecast_series, lcl_series, linestyle = 'dashed', marker = MARKER, color = 'magenta', alpha = 0.70, label = 'lower_confidence_limit')
        ax.plot(x_forecast_series, ucl_series, linestyle = 'dashed', marker = MARKER, color = 'magenta', alpha = 0.70, label = 'upper_confidence_limit')    
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
        ax.legend(loc = "upper right")
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
                file_name = "arima_forecast"

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
    
    print("\nARIMA Forecasting completed.\n")
    
    return forecast_df


def get_prophet_model (df, column_to_analyze, timestamp_tag_column, list_of_predictors = None, confidence_level_pct = 95.0):
    """
    get_prophet_model (df, column_to_analyze, timestamp_tag_column, list_of_predictors = None, confidence_level_pct = 95.0):

    https://facebook.github.io/prophet/docs/quick_start.html#python-api
    https://machinelearningmastery.com/time-series-forecasting-with-prophet-in-python/
    https://medium.com/mlearning-ai/multivariate-time-series-forecasting-using-fbprophet-66147f049e66
    https://search.r-project.org/CRAN/refmans/prophet/html/add_regressor.html
    https://www.bing.com/ck/a?!&&p=9de08ba28924217dJmltdHM9MTY5NDU2MzIwMCZpZ3VpZD0zMmUyZmQwMC1lMzIzLTYwZTYtMWRkOS1lZjU1ZTI0ODYxN2QmaW5zaWQ9NTQ3NA&ptn=3&hsh=3&fclid=32e2fd00-e323-60e6-1dd9-ef55e248617d&psq=prophet+add+regressor+standardize&u=a1aHR0cHM6Ly9jcmFuLnItcHJvamVjdC5vcmcvd2ViL3BhY2thZ2VzL3Byb3BoZXQvcHJvcGhldC5wZGYjOn46dGV4dD1UaGUlMjBkYXRhZnJhbWUlMjBwYXNzZWQlMjB0byUyMCVFMiU4MCU5OGZpdCVFMiU4MCU5OCUyMGFuZCUyMCVFMiU4MCU5OHByZWRpY3QlRTIlODAlOTglMjB3aWxsLERlY3JlYXNpbmclMjB0aGUlMjBwcmlvciUyMHNjYWxlJTIwd2lsbCUyMGFkZCUyMGFkZGl0aW9uYWwlMjByZWd1bGFyaXphdGlvbi4&ntb=1
    https://facebook.github.io/prophet/docs/seasonality,_holiday_effects,_and_regressors.html
    https://facebook.github.io/prophet/docs/uncertainty_intervals.html

    : param: df: the whole dataframe to be processed.
    
    : param: column_to_analyze: string (inside quotes), 
      containing the name of the column that will be analyzed. 
      e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    : param: timestamp_tag_column declare a string (inside quotes), 
      containing the name of the column containing the time information. 
      e.g. timestamp_tag_column = "DATE" will take the timestamps from column 'DATE'.

    : param: list_of_predictors = None
      If the response variable will not be used to predict itself, but instead other variable(s) will be
      used as predictor(s) (regressors), declare such variables inside a list of strings or as a string.
      Example: list_of_predictors = ['col1', 'col2', 'col3'] will use columns named as 'col1', 'col2', and
      'col3' to predict the response variable.
      ATTENTION: There is a maximum number of regressors allowed by Prophet. When using more than the 53-predictors
      limit, an error will be raised.

    : param: confidence_level_pct = 95.0 represents the level of confidence for the calculated intervals.
      If confidence_level_pct = 95.0, then 95% confidence intervals will be obtained. If confidence_level_pct = 90.0,
      90% confidence intervals are obtained.
    """

    from prophet import Prophet
    

    if (confidence_level_pct is None):
        confidence_level_pct = 95.0
    
    confidence = confidence_level_pct/100
    
    # Set a copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    
    #Use the timestamp properly converted to datetime (as in the graphics functions):
    x = (DATASET[timestamp_tag_column]).astype('datetime64[ns]')
    DATASET[timestamp_tag_column] = x
    
    # Create a dataframe in the format required by Prophet:

    if (list_of_predictors is None):
        
        DATASET = DATASET[[timestamp_tag_column, column_to_analyze]]
        DATASET.columns = ['ds', 'y']
    
    else:

        try:
            # Check if the len function may be applied (it is an iterable):
            a = len(list_of_predictors)
            if (type(list_of_predictors) == str):
                #Put the string inside a list
                list_of_predictors = [list_of_predictors]
        
        except:
            # The column name is actually a number
            list_of_predictors = [str(list_of_predictors)]


        list_of_columns = [timestamp_tag_column, column_to_analyze] + list_of_predictors
        DATASET = DATASET[list_of_columns]
        # Labels required by Prophet: 'ds' for datetimes, 'y' for the response
        list_of_columns = ['ds', 'y'] + list_of_predictors
        DATASET.columns = list_of_columns

    # Instantiate the Prophet object
    model = Prophet(interval_width = confidence)
    
    if (list_of_predictors is not None):
        for predictor in list_of_predictors:
            # https://python.hotexamples.com/examples/fbprophet/Prophet/add_regressor/python-prophet-add_regressor-method-examples.html
            model.add_regressor(predictor, standardize = 'auto')
    
    # Fit it to the dataframe:
    model.fit(DATASET)
    
    print("Facebook Prophet model successfully fitted to the time series and returned as \'model\'.")
    print("Prophet is designed to automatically find a good set of hyperparameters for the model in an effort to make skillful forecasts for data with trends and seasonal structure by default.")
    print("Prophet implements a procedure for forecasting time series data based on an additive model where non-linear trends are fit with yearly, weekly, and daily seasonality, plus holiday effects.\n")
    
    return model


def prophet_forecasting (prophet_model_object, number_of_periods_to_forecast = 365, X = None, timestamp_column = None, make_future_forecasts_with_multi_regressors = True, forecasts_based_on = 'mean', plot_predicted_time_series = True, get_interactive_plot = True, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    prophet_forecasting (prophet_model_object, number_of_periods_to_forecast = 365, X = None, timestamp_column = None, make_future_forecasts_with_multi_regressors = True, forecasts_based_on = 'mean', plot_predicted_time_series = True, get_interactive_plot = True, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    : param: prophet_model_object : object containing the Prophet model previously obtained.
      e.g. prophet_model_object = prophet_model if the model was obtained as prophet_model
      do not declare in quotes, since it is an object, not a string.

    : param: number_of_periods_to_forecast = 7
      integer value representing the total of periods to forecast. The periods will be in the
      unit (dimension) of the original dataset. If 1 period = 1 day, 7 periods will represent
      seven days.

    : params: X, timestamp_column, make_future_forecasts_with_multi_regressors, forecasts_based_on: 
      parameters for making predictions for models with more than 1 predictor.
      X is the dataframe object that will be used for making the predictions, and must be filled in this case. 
      e.g. X = dataset. The columns must be in the exact same order they were used for training the model.
      If the first column (timestamp) is not input as "ds", the column name must be input as a string in timestamp_column.
      Example: timestamp_column = 'timestamp'.

    : param: make_future_forecasts_with_multi_regressors = True - If True, the future forecasts will be performed for the dataframe X. 
      If False, only X will be used for predictions.
    
    : param: forecasts_based_on = 'mean' - For the case we are making forecasts based on multiple regressors, the values of the regressors
      must be set. You may use forecasts_based_on = 'mean' for applying the mean historical value; forecasts_based_on = 'ffill'
      to copy the nearest element on the dataset (forward-filling); or forecasts_based_on = 'mode' to use
      the mode (most common value) to perform missing value imputation. 
    
    Keep: 
    : param: plot_predicted_time_series = True to see the graphic of the predicted values.
      Alternatively, set plot_predicted_time_series = False not to show the plot.
    
    : param: get_interactive_plot = True will show the interactive Plotly version of the model predictions.
      If False, the matplotlib static figure will be shown.
    
    THE IMAGE MANIPULATION PARAMETERS ARE ONLY VALID IF get_interactive_plot = False        
    """

    from scipy import stats
    from prophet import Prophet
    
    # Create a dataframe containing the dates used for training Prophet with the dates that will be
    # predicted.
    model = prophet_model_object

    if (X is not None):
        # Set a copy of the dataframe to manipulate:
        DATASET = X.copy(deep = True)
        
        if ('ds' not in list(X.columns)):
            if (timestamp_column is None):
                # Try using first column as the timestamp one
                first_col = list(X.columns)[0]
                DATASET = DATASET.rename(columns = {first_col:'ds'})
            else:
                DATASET = DATASET.rename(columns = {timestamp_column:'ds'})

        if (make_future_forecasts_with_multi_regressors):
            # Add forecasts for future time
            # Create column with current datetimes and datetimes on the future:
            future = model.make_future_dataframe(periods = number_of_periods_to_forecast)
            #Concatenate this column of datetimes with the dataset
            DATASET = pd.concat([DATASET, future], axis = 0)
            # Guarantee that all datetimes are of the same type, so that equal timestamps will be
            # Interpreted as duplicates:
            DATASET['ds'] = DATASET['ds'].astype('datetime64[ns]')
            # Drop duplicated timestamps, keeping only the first (from DATASET, not from future).
            # Then, reset index
            DATASET = DATASET.drop_duplicates(subset = ['ds'], keep = 'first')
            DATASET = DATASET.reset_index(drop = True)

            # This dataset contain missing values for the non-timestamp columns, corresponding to timestamps in the
            # future. We must fill them before making the predictions
            # Set a list without timestamps - columns from the 2nd element (index 1)
            non_timestamp_cols = list(DATASET.columns)[1:]

            # If no imputation mode was defined, use the mean value:
            if (forecasts_based_on is None):
                forecasts_based_on = 'mean'
            
            # Start a filling dictionary:
            fill_dict = {}
            if (forecasts_based_on == 'mean'):
                for column in non_timestamp_cols:
                    # add column as the key, and the mean as the value:
                    fill_dict[column] = DATASET[column].mean()
                
                # Fill missing values:
                DATASET = DATASET.fillna(value = fill_dict)
            
            elif (forecasts_based_on == 'ffill'):
                DATASET = DATASET.fillna(method = 'ffill')
            
            elif (forecasts_based_on == 'mode'):
                for column in non_timestamp_cols:
                            
                    # The function stats.mode(X) returns an array as: 
                    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mode.html
                    # ModeResult(mode=3, count=5) ac, axis = None, cess mode attribute       
                    # which will return a string like 'a':
                    try:
                        fill_dict[column] = stats.mode(np.array(DATASET[column]), axis = None, keepdims = False).mode
                        
                    except:
                        try:
                            fill_dict[column] = stats.mode(np.array(DATASET[column]), axis = None, keepdims = False)[0]
                        except:
                            try:
                                if ((stats.mode(np.array(DATASET[column]), axis = None, keepdims = False) != np.nan) & (stats.mode(np.array(DATASET[column]), axis = None, keepdims = False) is not None)):
                                    fill_dict[column] = stats.mode(np.array(DATASET[column]), axis = None, keepdims = False)
                                else:
                                    fill_dict[column] = np.nan
                            except:
                                fill_dict[column] = np.nan
                    
                # Fill missing values:
                DATASET = DATASET.fillna(value = fill_dict)

        # Finally, make the predictions
        forecast_df = model.predict(DATASET)


    else:
        # Only forecasts for the single time-series column will be performed:
        future = model.make_future_dataframe(periods = number_of_periods_to_forecast)
        # Make the predictions for the future dataframe:
        forecast_df = model.predict(future)
        
    
    # Rename columns to give more meaninful names:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html
    forecast_df = forecast_df.rename(columns = {'ds': 'timestamp', 'yhat': 'y_forecasts',
                                                'yhat_lower': 'lower_cl', 'yhat_upper': 'upper_cl'})
    
    x_forecast_series = forecast_df['timestamp']
    y_forecast_series = forecast_df['y_forecasts']
    lcl_series = forecast_df['lower_cl']
    ucl_series = forecast_df['upper_cl']
    trend_series = forecast_df['trend']
        
    # We are finally in the general case, after obtaining the dataframe through all possible ways:
    print(f"Finished the obtention of the forecast dataset. Check the 10 last rows of the forecast dataset:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(forecast_df.tail(10))
            
    except: # regular mode
        print(forecast_df.tail(10))
        
    
    # Now, let's create the graphics
    if (plot_predicted_time_series == True):
        
        if (get_interactive_plot == True):
            
            from prophet.plot import plot_plotly, plot_components_plotly
            # Methods require the dataframe in the original format 'y' x 'ds'
            plot_plotly(model, model.predict(future))
            plot_components_plotly(model, model.predict(future))
        
        else:

            LINE_STYLE = '-'
            MARKER = ''

            if (plot_title is None):
                # Set graphic title
                plot_title = f"Prophet_forecasts"

            if (horizontal_axis_title is None):
                # Set horizontal axis title
                horizontal_axis_title = "timestamp"

            if (vertical_axis_title is None):
                vertical_axis_title = "time_series"

            # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
            # so that the bars do not completely block other views.
            OPACITY = 0.95

            #Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
            fig = plt.figure(figsize = (12, 8))
            ax = fig.add_subplot()

            # Plot the predictions (completely opaque, so that the input data series will not be
            # visible)
            ax.plot(x_forecast_series, y_forecast_series, linestyle = LINE_STYLE, marker = MARKER, color = 'darkblue', alpha = 1.0, label = 'forecast')
            # Plot the trend:
            ax.plot(x_forecast_series, trend_series, linestyle = LINE_STYLE, marker = MARKER, color = 'red', alpha = OPACITY, label = 'trend')
            
            # Plot the confidence limits:
            ax.plot(x_forecast_series, lcl_series, linestyle = 'dashed', marker = MARKER, color = 'lightgrey', alpha = 0.70, label = 'lower_confidence_limit')
            ax.plot(x_forecast_series, ucl_series, linestyle = 'dashed', marker = MARKER, color = 'lightgrey', alpha = 0.70, label = 'upper_confidence_limit')    
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
            ax.legend(loc = "upper right")
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
                    file_name = "prophet_forecast"

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

    print("\nProphet Forecasting completed.\n")
    
    return forecast_df


def df_rolling_window_stats (df, window_size = 2, window_statistics = 'mean', min_periods_required = None, window_center = False, window_type = None, window_on = None, row_accross = 'rows', how_to_close_window = None, drop_missing_values = True):
    """
    df_rolling_window_stats (df, window_size = 2, window_statistics = 'mean', min_periods_required = None, window_center = False, window_type = None, window_on = None, row_accross = 'rows', how_to_close_window = None, drop_missing_values = True):
    
    Check Pandas rolling statistics documentation:
     https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rolling.html
     https://pandas.pydata.org/pandas-docs/stable/user_guide/window.html#window-generic
     https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.diff.html
    
    : param: df: the whole dataframe to be processed.
    
    : param: window_statistics = 'mean', 'std', 'sum', or 'difference'
      'difference' will perform the first discrete difference of element: Yn - Yn-1
    
    : param: window_size: integer value or offset time.
      Manipulate parameter window of the .rolling method; or the parameter
      periods of the .diff method.
    
    : params: window = window_size; or periods = window_size.
      Size of the moving window. If an integer, the fixed number of observations 
      used for each window. If an offset, the time period of each window. 
      Each window will be a variable sized based on the observations included in the 
      time-period. This is only valid for datetime-like indexes. 
    
    : param: min_periods_required = None. Alternatively, set as an integer value.
      Manipulate parameter min_periods of .rolling method
      min_periods = min_periods_required
      Minimum number of observations in window required to have a value; otherwise, 
      result is np.nan. For a window that is specified by an offset, min_periods will 
      default to 1. For a window that is specified by an integer, min_periods will default 
      to the size of the window.
    
    : param: window_center = False.
      Manipulate parameter center of .rolling method
      center = window_center
      If False, set the window labels as the right edge of the window index.
      If True, set the window labels as the center of the window index.
    
    : param: window_type = None
      Manipulate parameter win_type of .rolling method
      win_type = window_type
      If None, all points are evenly weighted. If a string, it must be a valid 
      scipy.signal window function:
      https://docs.scipy.org/doc/scipy/reference/signal.windows.html#module-scipy.signal.windows
      Certain Scipy window types require additional parameters to be passed in the 
      aggregation function. The additional parameters must match the keywords specified 
      in the Scipy window type method signature.
    
    : param: window_on = None
      Manipulate parameter on of .rolling method
      on = window_on
      string; For a DataFrame, a column label or Index level on which to calculate 
      the rolling window, rather than the DataFrame’s index. Provided integer column is 
      ignored and excluded from result since an integer index is not used to calculate 
      the rolling window.
    
    : param: row_accross = 'rows'. Alternatively, row_accross = 'columns'
      manipulate the parameter axis of .rolling method:
      if row_accross = 'rows', axis = 0; if row_accross = 'columns', axis = 1.
      If axis = 0 or 'index', roll across the rows.
      If 1 or 'columns', roll across the columns.
    
    : param: how_to_close_window = None
      Manipulate parameter closed of .rolling method
      closed = how_to_close_window
      String: If 'right', the first point in the window is excluded from calculations.
      If 'left', the last point in the window is excluded from calculations.
      If 'both', the no points in the window are excluded from calculations.
      If 'neither', the first and last points in the window are excluded from calculations.
      Default None ('right').
    
    : param: drop_missing_values = True will remove all missing values created by the methods (all
      rows containing missing values). 
      If drop_missing_values = False, the positions containing NAs will be kept.
    """

    DATASET = df.copy(deep = True)
    WINDOW = window_size
    MIN_PERIODS = min_periods_required
    CENTER = window_center
    WIN_TYPE = window_type
    ON = window_on
    
    numeric_data_types = [np.float16, np.float32, np.float64, np.int16, np.int32, np.int64]
    
    # Variable to map if the timestamp was correctly parsed. It will be set of True
    # only when it happens:
    date_parser_marker = False
    
    try:
        if (type(DATASET[ON][0]) not in numeric_data_types):
            # Try to Parse the date:
            try:
                
                DATASET[ON] = (DATASET[ON]).astype('datetime64[ns]')
                # Change the value of the marker to map that the date was correctly parsed:
                date_parser_marker = True
                print(f"Column {ON} successfully converted to numpy.datetime64[ns].\n")     
            
            except:
                pass
    except:
        pass
    
    
    if (row_accross == 'columns'):
        
        AXIS = 1
    
    else:
        # 'rows' or an invalid value was set, so set to 'rows' (Axis = 0)
        AXIS = 0
    
    CLOSED = how_to_close_window
    
    # Now all the parameters for the rolling method are set. Calculate the dataframe
    # for the selected statistic:
    
    if (window_statistics == 'mean'):
        
        rolling_window_df = DATASET.rolling(window = WINDOW, min_periods = MIN_PERIODS, center = CENTER, win_type = WIN_TYPE, on = ON, axis = AXIS, closed = CLOSED).mean()
        print(f"Calculated rolling mean for a window size of {WINDOW}. Returning the rolling \'mean\' dataframe.\n")
    
    elif (window_statistics == 'std'):
        
        rolling_window_df = DATASET.rolling(window = WINDOW, min_periods = MIN_PERIODS, center = CENTER, win_type = WIN_TYPE, on = ON, axis = AXIS, closed = CLOSED).std()
        print(f"Calculated rolling standard deviation for a window size of {WINDOW}. Returning the rolling \'std\' dataframe.\n")
    
    elif (window_statistics == 'sum'):
        
        rolling_window_df = DATASET.rolling(window = WINDOW, min_periods = MIN_PERIODS, center = CENTER, win_type = WIN_TYPE, on = ON, axis = AXIS, closed = CLOSED).sum()
        print(f"Calculated rolling sum for a window size of {WINDOW}. Returning the rolling \'sum\' dataframe.\n")
    
    elif (window_statistics == 'difference'):
        
        # Create a list of the columns that can be differentiated and of those that cannot be.
        diff_columns = []
        excluded_columns = []
        for column in list(DATASET.columns):
            
            if (type(DATASET[column][0]) in numeric_data_types):
                diff_columns.append(column)
            
            else:
                
                if ((column == ON) & (date_parser_marker == True)):
                    # This is the column we converted to date. Set it as the index.
                    # It will allow us to calculate the differences without losing this
                    # information
                    DATASET = DATASET.set_index(column)
                
                else:
                    excluded_columns.append(column)
        
        # Select only the columns in diff_columns:
        DATASET= DATASET[diff_columns]
        
        if (len(excluded_columns) > 0):
            print(f"It is not possible to calculate the differences for columns in {excluded_columns}, so they were removed.\n")
        
        rolling_window_df = DATASET.diff(periods = WINDOW, axis = AXIS)
        print(f"Calculated discrete differences ({WINDOW} periods). Returning the differentiated dataframe.\n")
    
    else:
        raise InvalidInputsError ("Please, select a valid rolling window function: \'mean\', \'std\', \'sum\', or \'difference\'.")
    
    # drop missing values generated:
    if (drop_missing_values):
        # Run of it is True. Do not reset index for mode 'difference'.
        # In this mode, the index was set as the date.
        rolling_window_df.dropna(axis = 0, how = 'any', inplace = True)
        
        if (window_statistics != 'difference'):
            rolling_window_df.reset_index(drop = True, inplace = True)
    
    print("Check the rolling dataframe:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(rolling_window_df)
            
    except: # regular mode
        print(rolling_window_df)
    
    print('\n')
    print("ATTENTION: depending on the window size, the windowed dataset may be considerable smaller than the original dataframe, with several missing values indicated by NA.\n")
    print("For understanding it, consider a dataframe containing daily new cases of an illness, where we want to obtain the 7-day rolling average.")
    print("Here, we will obtain 6 rows containing only missing values. The reason is that it is not possible to calculate the 7-periods average for the first 6 rows.")
    print("In the first row, we have only 1 data; in the second row, we have only two, the day and the day before; ..., and so on.")
    print("We can only calculate a 7-period average from the 7th day, when we have that day and the 6 days before it.")
    print("Once it is not possible to obtain the rolling statistic for some rows, missing values are generated.")
    print("So, even if the rolling statistic was calculated for only 2 consecutive periods, there would be a row with missing values, since it is not possible to calculate the window statistic for a single entry.\n")
    print(f"Naturally, this examples suppose that the user set how_to_close_window = {'right'}, when the first point in the window is excluded from calculations.")
    print(f"If how_to_close_window = {'left'}, then the last point in the window would be excluded from calculations, so the missing values would appear at the end of the dataset.")
    print("Even though it is not so intuitive, in this case we would take an entry and the next ones for calculating the statistic. For instance, the 7-day rolling average would be calculated as the average between a day and the next 6 days.")
    print(f"Finally, if how_to_close_window = {'both'}, we would have a centralized window, where the some of the values come from the times before; and some come from the times after.")
    print("In this last case, the 7-day rolling average would be calculated as the average between a day; the 3 days before; and the 3 next days.")
    print("So, missing values would appear in both the beginning and the end of the dataframe.\n")
    
    print("For this function, the default is how_to_close_window = {'right'}, i.e., statistics are calculated from the row and the values before it.\n")
    
    return rolling_window_df


def seasonal_decomposition (df, response_column_to_analyze, column_with_timestamps = None, decomposition_mode = "additive", maximum_number_of_cycles_or_periods_to_test = 100, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    seasonal_decomposition (df, response_column_to_analyze, column_with_timestamps = None, decomposition_mode = "additive", maximum_number_of_cycles_or_periods_to_test = 100, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):

    Check seasonal_decompose and DecomposeResult documentations:
     https://www.statsmodels.org/dev/generated/statsmodels.tsa.seasonal.seasonal_decompose.html
     https://www.statsmodels.org/dev/generated/statsmodels.tsa.seasonal.DecomposeResult.html#statsmodels.tsa.seasonal.DecomposeResult
    seasonal_decompose results in an object from class DecomposeResult.
      Check the documentation of the .plot method for DecomposeResult objects:
      https://www.statsmodels.org/dev/generated/statsmodels.tsa.seasonal.DecomposeResult.plot.html#statsmodels.tsa.seasonal.DecomposeResult.plot
    
    : param: number_of_periods_to_forecast = 7
      integer value representing the total of periods to forecast. The periods will be in the
      unit (dimension) of the original dataset. If 1 period = 1 day, 7 periods will represent
      seven days.
    
    : param: df: the whole dataframe to be processed.
    
    : param: response_column_to_analyze: string (inside quotes), 
      containing the name of the column that will be analyzed.
      e.g. response_column_to_analyze = "column1" will analyze the column named as 'column1'.
      WARNING: This must be the response variable
    
    : param: column_with_timestamps: string (inside quotes), 
      containing the name of the column containing timestamps.
      Keep it as None if you want to set the index as the time.
      e.g. response_column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    : param: MAXIMUM_NUMBER_OF_CYCLES_OR_PERIODS_TO_TEST = integer (minimum value is 2) representing
      the total of cycles or periods that may be present on time series. The function will loop through
      2 to MAXIMUM_NUMBER_OF_CYCLES_OR_PERIODS_TO_TEST to find the number that minimizes the sum of
      modules (absolute values) of the residues.
      e.g. MAXIMUM_NUMBER_OF_CYCLES_OR_PERIODS_TO_TEST = 4 will test 2, 3 and 4 cycles on the time series.

    : param: decomposition_mode = "additive" - manipulate the parameter 'model' from seasonal_decompose.
      model = decomposition_mode
      Alternatively, set decomposition_mode = "multiplicative" for decomposing as a multiplicative time series.
    
      'additive' model: An additive model suggests that the components are added together as: 
      y(t) = Level + Trend + Seasonality + Noise
      An additive model is linear where changes over time are consistently made by the same amount. A linear trend is 
      a straight line. A linear seasonality has the same frequency (width of cycles) and amplitude (height of cycles).
    
      'multiplicative' model: A multiplicative model suggests that the components are multiplied together as:
      y(t) = Level * Trend * Seasonality * Noise
      A multiplicative model is nonlinear, such as quadratic or exponential. Changes increase or decrease over time.
      A nonlinear trend is a curved line. A non-linear seasonality has an increasing or decreasing frequency 
      and/or amplitude over time.
      https://machinelearningmastery.com/decompose-time-series-data-trend-seasonality/#:~:text=The%20statsmodels%20library%20provides%20an%20implementation%20of%20the,careful%20to%20be%20critical%20when%20interpreting%20the%20result.
    """

    import statsmodels as sm
    from statsmodels.tsa.seasonal import DecomposeResult
    from statsmodels.tsa.seasonal import seasonal_decompose
    
    # Set a local copy of the dataframe to manipulate?
    DATASET = df.copy(deep = True)
    
    #Check if there is a column with the timestamps:
    if not (column_with_timestamps is None):
        
        DATASET = DATASET.sort_values(by = column_with_timestamps)
        
        x = DATASET[column_with_timestamps].copy()
        
        # try to convert it to datetime:
        try:
            x = x.astype('datetime64[ns]')
        
        except:
            pass
        
        # Set it as index to include it in the seasonal decomposition model:
        DATASET = DATASET.set_index(column_with_timestamps)
    
    else:
        #the index will be used to plot the charts:
        x = DATASET.index
        
    # Extract the time series from the dataframe:
    Y = DATASET[response_column_to_analyze]
    
    # Set the parameters for modelling:
    MODEL = decomposition_mode
    MAXIMUM_NUMBER_OF_CYCLES_OR_PERIODS_TO_TEST = maximum_number_of_cycles_or_periods_to_test

    if (Y.isna().sum() > 0):
        print(f"There are {Y.isna().sum()} missing values.")
        print("Since this function cannot deal with missing values, the missing entries will be dropped.\n")
        Y = Y.dropna()

    # Check if the arguments are valid:
    if MODEL not in ["additive", "multiplicative"]:
        # set model as 'additive'
        MODEL = "additive"
    
    print(f"Testing {MODEL} model for seasonal decomposition.\n")
    
    try:
        MAXIMUM_NUMBER_OF_CYCLES_OR_PERIODS_TO_TEST = int(MAXIMUM_NUMBER_OF_CYCLES_OR_PERIODS_TO_TEST)
        # If it is lower than 2, make it equals to 2:
        if (MAXIMUM_NUMBER_OF_CYCLES_OR_PERIODS_TO_TEST < 2):
            MAXIMUM_NUMBER_OF_CYCLES_OR_PERIODS_TO_TEST = 2
        
        print(f"Testing the presence of until {MAXIMUM_NUMBER_OF_CYCLES_OR_PERIODS_TO_TEST} periods or cycles in the time series.\n")
    
    except:
        raise InvalidInputsError ("Input a valid MAXIMUM_NUMBER_OF_CYCLES_OR_PERIODS_TO_TEST. It must be an integer higher or equal to 2, representing the maximum possible number of cycles or periods present in time series.\n")
    
    # Now, let's loop through the possible number of cycles and periods:
    # Start a dictionary to store the number of cycles and the correspondent sum of 
    # absolute values of the residues:
    residues_dict = {}
    
    # Multiplicative seasonality is not appropriate for zero and negative values. Trying to use it will raise a ValueError
    if (MODEL == "multiplicative"):
        if (Y[Y < 0].count() > 0):
            print(f"There are {Y[Y < 0].count()} zero or negative values.")
            print("Multiplicative seasonality is not appropriate for zero and negative values.")
            print("The model will be changed to 'additive'.\n")
            MODEL = "additive"


    for TOTAL_OF_CYCLES in range (2, (MAXIMUM_NUMBER_OF_CYCLES_OR_PERIODS_TO_TEST + 1)):
        
        # TOTAL_OF_CYCLES is an integer looping from TOTAL_OF_CYCLES = 2 to
        # TOTAL_OF_CYCLES = (MAXIMUM_NUMBER_OF_CYCLES_OR_PERIODS_TO_TEST + 1) - 1 = (MAXIMUM_NUMBER_OF_CYCLES_OR_PERIODS_TO_TEST)
        
        try:
            
            y = Y.copy(deep = True)
            # Start an instance (object) from class DecomposeResult
            # Set this object as the resultant from seasonal_decompose
            decompose_res_obj = seasonal_decompose(y, model = MODEL, period = TOTAL_OF_CYCLES, two_sided = True)
            # decompose_res_obj is an instance (object) from class DecomposeResult
            """
            two_sided = True
            The moving average method used in filtering. If True (default), a centered moving average is computed 
            using the filt. If False, the filter coefficients are for past values only.
            """
            # Get the array of the residues. Convert it to NumPy array to guarantee the vectorial operations:
            residues_array = np.array(decompose_res_obj.resid)
            # Convert the values in the array to the absolute values:
            residues_array = abs(residues_array)
            # Get the sum of the absolute residues:
            sum_of_abs_residues = np.sum(residues_array)

            # Store it in the dictionary (value correspondent to the key TOTAL_OF_CYCLES):
            residues_dict[TOTAL_OF_CYCLES] = sum_of_abs_residues
        
        except:
            # There are no sufficient measurements to test this total of cycles
            pass
    
    # get the list of dictionary's values:
    dict_vals = list(residues_dict.values())
    # Get the minimum value on the list:
    minimum_residue = min(dict_vals)
    # Get the index of minimum_residue on the list:
    minimum_residue_index = dict_vals.index(minimum_residue)
    
    # Now, retrieve OPTIMAL_TOTAL_CYCLES. It will be the value with index minimum_residue_index
    # in the list of keys:
    list_of_keys = list(residues_dict.keys())
    OPTIMAL_TOTAL_CYCLES = list_of_keys[minimum_residue_index]
    
    print(f"Number of total cycles or periods in time series: {OPTIMAL_TOTAL_CYCLES}.\n")
    
    # Start an instance (object) from class DecomposeResult
    # Set this object as the resultant from seasonal_decompose
    decomposition_obj = seasonal_decompose(Y, model = MODEL, period = OPTIMAL_TOTAL_CYCLES, two_sided = True)
    # decompose_res_obj is an instance (object) from class DecomposeResult
    
    # Create a dictionary with the resultants from the seasonal decompose:
    # These resultants are obtained as attributes of the decompose_res_obj
    
    number_of_observations_used = decomposition_obj.nobs
    print(f"Seasonal decomposition concluded using {number_of_observations_used} observations.\n")
    
    decompose_dict = {
        
        'timestamp': np.array(x),
        "observed_data": np.array(decomposition_obj.observed),
        "seasonal_component": np.array(decomposition_obj.seasonal),
        "trend_component": np.array(decomposition_obj.trend),
        "residuals": np.array(decomposition_obj.resid)
    }
    
    # Convert it into a returned dataframe:
    seasonal_decompose_df = pd.DataFrame(data = decompose_dict)
    
    print("Check the first 10 rows of the seasonal decompose dataframe obtained:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(seasonal_decompose_df.head(10))
            
    except: # regular mode
        print(seasonal_decompose_df.head(10))
    
    print("\n") # line break
    print(f"Check the time series decomposition graphics for the {MODEL} model:\n")
    
    # Plot parameters:
    x = decompose_dict['timestamp']
    try:
        y1 = decompose_dict['observed_data']
        lab1 = "observed_data"
    except:
        pass
    
    try:
        y2 = decompose_dict['seasonal_component']
        lab2 = 'seasonal_component'
    except:
        pass
    
    try:    
        y3 = decompose_dict['trend_component']
        lab3 = 'trend_component'
    except:
        pass
    
    try:
        y4 = decompose_dict['residuals']
        lab4 = 'residuals'
    except:
        pass
    
    plot_title = "seasonal_decomposition_for_" + response_column_to_analyze
    
    # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
    # so that the bars do not completely block other views.
    OPACITY = 0.95
    
    # Now, let's obtain the graphic:
    # Create the figure:
    fig, ax = plt.subplots(4, 1, sharex = True, figsize = (12, 8)) 
    # sharex = share axis X
    # number of subplots equals to the total of series to plot (in this case, 4)
    try:
        ax[0].plot(x, y1, linestyle = '-', marker = '', color = 'darkblue', alpha = OPACITY, label = lab1)
        # Set title only for this subplot:
        ax[0].set_title(plot_title)
        ax[0].grid(grid)
        ax[0].legend(loc = 'upper right')
        # position options: 'upper right'; 'upper left'; 'lower left'; 'lower right';
        # 'right', 'center left'; 'center right'; 'lower center'; 'upper center', 'center'
        # https://www.statology.org/matplotlib-legend-position/
    except:
        pass

    try:  
        ax[1].plot(x, y2, linestyle = '-', marker = '', color = 'crimson', alpha = OPACITY, label = lab2)
        # Add the y-title only for this subplot:
        ax[1].set_ylabel(response_column_to_analyze)
        ax[1].grid(grid)
        ax[1].legend(loc = 'upper right')
    except:
        pass
    
    try:
        ax[2].plot(x, y3, linestyle = '-', marker = '', color = 'darkgreen', alpha = OPACITY, label = lab3)
        ax[2].grid(grid)
        ax[2].legend(loc = 'upper right')
    except:
        pass
    
    try:
        ax[3].plot(x, y4, linestyle = '', marker = 'o', color = 'red', alpha = OPACITY, label = lab4)
        # Add an horizontal line in y = zero:
        ax[3].axhline(0, color = 'black', linestyle = 'dashed', alpha = OPACITY)
        # Set the x label only for this subplot
        ax[3].set_xlabel('timestamp')
        ax[3].grid(grid)
        ax[3].legend(loc = 'upper right')
    except:
        pass
    
    #ROTATE X AXIS IN XX DEGREES
    plt.xticks(rotation = x_axis_rotation)
    # XX = 0 DEGREES x_axis (Default)
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
            file_name = "seasonal_decomposition"

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
    
        #fig.tight_layout()

    ## Show an image read from an image file:
    ## import matplotlib.image as pltimg
    ## img=pltimg.imread('mydecisiontree.png')
    ## imgplot = plt.imshow(img)
    ## See linkedIn Learning course: "Supervised machine learning and the technology boom",
    ##  Ex_Files_Supervised_Learning, Exercise Files, lesson '03. Decision Trees', '03_05', 
    ##  '03_05_END.ipynb'
    plt.show()
    
    #Finally, return the full dataframe:
    print("The full dataframe obtained from the decomposition, as well as the Statsmodels decomposition object were returned.")
    
    return seasonal_decompose_df, decomposition_obj
