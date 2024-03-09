import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf

from idsw import (InvalidInputsError, ControlVars)
from .core import AnomalyDetector


def distances_between_each_data_point (df_tensor_or_array, list_of_new_arrays_to_compare = None, what_to_compare = 'only_original_array', distance_metrics = 'euclidean'):
    """
    distances_between_each_data_point (df_tensor_or_array, list_of_new_arrays_to_compare = None, what_to_compare = 'only_original_array', distance_metrics = 'euclidean'):

    - Compute distances between data points.
    - Smaller distances in the n-dimensional space indicate closer (more similar) points.
    - You may compute distance between new points and the original dataset, new points themselves, or between each point from 
    the original dataset.
    - This function will return the matrix of distances between each tensor data point.

    : param: df_tensor_or_array = dataframe, array, or tensor with the data points. At least one array must be provided as 
      df_tensor_or_array
    
    : param: list_of_new_arrays_to_compare: if you want to compare new data points with the original dataset, input them as a
      collection (array-like or list) of arrays. Each value in the array is the correspondent value of a given variable for that new
      entry (i.e., a component of the vector). For example, if you have a dataset with 3 columns, 'A', 'B', and 'C' and you want to
      find the distance between the points (A, B, C) = (1, 2, 3) and (A, B, C) = (1.2, 2.4, 3.6) with each point of the original array,
      then:
      list_of_new_arrays_to_compare = [[1, 2, 3], [1.2, 2.4, 3.6]]
      If you want only to compare the data points in the original dataset, you may keep list_of_new_arrays_to_compare = None

      NOTICE THAT you may input a single array in df_tensor_or_array and a single array as list_of_new_arrays_to_compare.
      This will calculate the distance between two data points.

    : param: what_to_compare = 'only_original_array' - if what_to_compare = 'only_original_array', the function will calculate the distance
      between each point in the original dataset only (even if you input new arrays to compare).
      If what_to_compare = 'only_new_with_original' - in this case, only the comparison between new arrays input as 
      list_of_new_arrays_to_compare and the original arrays will be performed. Notice that it will not calculate the distances between
      the data points of the original dataset, except if no data was input as list_of_new_arrays_to_compare. In this case, the default
      'only_original_array' will be performed.
      If what_to_compare = 'everything', new data will be stacked on the bottom of the original array and the distance between each data
      point will be obtained.

    : param: distance_metrics = 'euclidean' - string with the distance metrics that will be used.
      The distance function can be ‘braycurtis’, ‘canberra’, ‘chebyshev’, ‘cityblock’, ‘correlation’, ‘cosine’, 
      ‘dice’, ‘euclidean’, ‘hamming’, ‘jaccard’, ‘jensenshannon’, ‘kulczynski1’, ‘mahalanobis’, ‘matching’, ‘minkowski’, 
      ‘rogerstanimoto’, ‘russellrao’, ‘seuclidean’, ‘sokalmichener’, ‘sokalsneath’, ‘sqeuclidean’, ‘yule’.
    
      ## ATTENTION: METRICS ARE CALCULATED AS DEFAULT, it is not possible to modify extra parameters of each one.
      # Explanaition of each one in:
      # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.pdist.html#scipy.spatial.distance.pdist
      # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cdist.html#scipy.spatial.distance.cdist
      # https://docs.scipy.org/doc/scipy/reference/spatial.distance.html
    """

    from scipy.spacial.distance import pdist, cdist

    df = np.array(df_tensor_or_array)

    if (list_of_new_arrays_to_compare is not None):

        if (len(list_of_new_arrays_to_compare) > 0):

            new_data = np.array(list_of_new_arrays_to_compare)

            if (what_to_compare == 'only_new_with_original'):

                distance_matrix = cdist(df, new_data, metric = distance_metrics)
                if ControlVars.show_results:
                    print("Distances between new data points and the original ones were calculated and returned as distance_matrix.\n")
            
            elif (what_to_compare == 'everything'):
                # https://numpy.org/doc/stable/reference/generated/numpy.row_stack.html
                df = np.row_stack((df, new_data))

                distance_matrix = pdist(df, metric = distance_metrics)
                if ControlVars.show_results:
                    print("New data points added to the the dataset.")
                    print("Distances between each point on the dataset were calculated and returned as distance_matrix.\n")
        
    else:
        if ControlVars.show_results:
            print(f"Mode set as what_to_compare = 'only_original_array'.")
        distance_matrix = pdist(df, metric = distance_metrics)
        if ControlVars.show_results:
            print("Distances between each point on the dataset were calculated and returned as distance_matrix.\n")

    if ControlVars.show_results:
        print("Check the 10 first rows from the returned distance matrix:\n")
        print(distance_matrix[:10])

    return distance_matrix


def kmeans_elbow_method (X_tensor, max_number_of_clusters_to_test = 100, number_of_initializations = 10, maximum_of_allowed_iterations = 20000, kmeans_algorithm = 'lloyd', tolerance = 0.0001, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    """
    kmeans_elbow_method (X_tensor, max_number_of_clusters_to_test = 100, number_of_initializations = 10, maximum_of_allowed_iterations = 20000, kmeans_algorithm = 'lloyd', tolerance = 0.0001, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):

    - Unsupervised learning method for assigning clusters to each data point.
    - Notice that the response predicted by the model is simply the cluster for a given entry.
    
    KMeans clustering requires threadpoolctl > 3.0. If it is not possible to pip install threadpoolctl --upgrade,
    you can try DBSCAN clustering algorithm: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html

    from sklearn.cluster import DBSCAN
    clustering = DBSCAN(eps=3, min_samples=2)
    clustering = clustering.fit(X)
    clustering.labels_ : array([0, 0, 0, 1, 1, 1], dtype=int64) # same attributes from KMeans object

    
    : param: X_tensor = subset of predictive variables (dataframe). Since this is a non-supervised algorithm, you may pass the full dataset.
    
    : param: max_number_of_clusters_to_test = 100 (integer). The algorithm will test 2 to the total of clusters you defined as
      max_number_of_clusters_to_test.
    
    : param: number_of_initializations = 10 (integer). Number of times the k-means algorithm is run with different centroid seeds. 
      The final results is the best output of n_init consecutive runs in terms of inertia. Several runs are recommended for 
      sparse high-dimensional problems. Manipulates the parameter n_init from KMeans Sklearn class.

    : param: MAXIMUM_OF_ALLOWED_ITERATIONS = integer representing the maximum number of iterations
      that the optimization algorithm can perform. Depending on data, convergence may not be
      reached within this limit, so you may need to increase this hyperparameter.

    : param: kmeans_algorithm = 'lloyd'. K-means algorithm to use. The classical EM-style algorithm is "lloyd". The 
      "elkan" variation can be more efficient on some datasets with well-defined clusters, by using the triangle inequality. 
      However it’s more memory intensive due to the allocation of an extra array of shape (n_samples, n_clusters).
      Options: “lloyd”, “elkan”, “auto”, “full”. Manipulates the parameter algorithm from KMeans Sklearn class.

    : param: tolerance = 0.0001. Relative tolerance with regards to Frobenius norm of the difference in the cluster centers 
      of two consecutive iterations to declare convergence. Manipulates the parameter tol from KMeans Sklearn class.
    """

    from sklearn.cluster import KMeans
    # https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
    
    RANDOM_STATE = 55 
    ## We will pass it to every sklearn call so we ensure reproducibility (i.e., a new random process)
    
    if ControlVars.show_results:
        print("Let's evaluate and compare the inertia.")
        print("Here, inertia is defined as the sum of squared distances of samples to their closest cluster center, weighted by the sample weights.")
        print("In the elbow or knee method, we plot the inertia against the number of clusters that resulted in such inertia.")
        print("The number of clusters correspondent to the knee or elbow in the plot (sudden decay of derivative) is took as the ideal number of clusters to use.")
        print("Andrew Ng in his Machine Learning Specialization (Coursera and Stanford University Online) presents several restrictions against its method, which is far from being perfect.\n")

    X = np.array(X_tensor)
    # Check if it is a single-dimension array
    if(len(X) == 1):
        #  Reshape it as a matrix
        X = X.reshape(-1,1)

    # Range of clusters to test:
    # # numpy.arange([start, ]stop, [step, ]dtype=None, *, like=None)
    # https://numpy.org/doc/stable/reference/generated/numpy.arange.html
    clusters_to_test = np.arange(2, max_number_of_clusters_to_test, 1, dtype = int)
    # Start a list to store the calculated inertia:
    inertia_list = []

    # Now, calculate the inertia for each value on clusters_to_test:

    for clusters in clusters_to_test:
        # Start K-Means object:
        kmeans_model = KMeans(n_clusters = clusters, random_state = RANDOM_STATE, n_init = number_of_initializations, max_iter = maximum_of_allowed_iterations, tol = tolerance, verbose = 1, algorithm = kmeans_algorithm)
        # Fit kmeans object to the array:
        kmeans_model = kmeans_model.fit(X)
        # Append the inertia attribute on the list:
        inertia_list.append(kmeans_model.inertia_)
    
    # Convert to NumPy array:
    inertia_list = np.array(inertia_list)
    
    if (plot_title is None):
        plot_title = "KMeans_elbow_plot"

    if (horizontal_axis_title is None):
        horizontal_axis_title = "k_number_of_clusters"
    
    if (vertical_axis_title is None):
        vertical_axis_title = "inertia"
    
    x = clusters_to_test
    y = inertia_list

    elbow_df = pd.DataFrame(data = {'k_number_of_clusters': clusters_to_test, 'inertia': inertia_list})

    # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
    # so that the bars do not completely block other views.
    if ControlVars.show_plots:
        OPACITY = 0.95
        
        print("Check the elbow plot below:\n")

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
        ax.set_xlabel(horizontal_axis_title)
        ax.set_ylabel(vertical_axis_title)

        # Scatter plot of time series:
        ax.plot(x, y, linestyle = "-", marker = 'o', color = 'crimson', alpha = OPACITY)
        # Axes.plot documentation:
        # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html?msclkid=42bc92c1d13511eca8634a2c93ab89b5
                
        # x and y are positional arguments: they are specified by their position in function
        # call, not by an argument name like 'marker'.
                
        # Matplotlib markers:
        # https://matplotlib.org/stable/api/markers_api.html?msclkid=36c5eec5d16011ec9583a5777dc39d1f
        
        # Now we finished plotting all of the series, we can set the general configuration:
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
                file_name = "KMeans_elbow_plot"

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
    
    if ControlVars.show_results:
        print("\n")
        print("Check the summary dataframe with the number of clusters and correspondent inertia:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(elbow_df)
                
        except: # regular mode
            print(elbow_df)

    return elbow_df


def kmeans_clustering (X_tensor, number_of_clusters = 8, number_of_initializations = 10, maximum_of_allowed_iterations = 20000, kmeans_algorithm = 'lloyd', tolerance = 0.0001):
    """
    kmeans_clustering (X_tensor, number_of_clusters = 8, number_of_initializations = 10, maximum_of_allowed_iterations = 20000, kmeans_algorithm = 'lloyd', tolerance = 0.0001):

    - Unsupervised learning method for assigning clusters to each data point.
    - Notice that the response predicted by the model is simply the cluster for a given entry.
    
    KMeans clustering requires threadpoolctl > 3.0. If it is not possible to pip install threadpoolctl --upgrade,
    you can try DBSCAN clustering algorithm: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html

    from sklearn.cluster import DBSCAN
    clustering = DBSCAN(eps=3, min_samples=2)
    clustering = clustering.fit(X)
    clustering.labels_ : array([0, 0, 0, 1, 1, 1], dtype=int64) # same attributes from KMeans object


    : param: X_tensor = subset of predictive variables (dataframe). Since this is a non-supervised algorithm, you may pass the full dataset.
    
    : param: number_of_clusters = 8 (integer). The number of clusters to form as well as the number of centroids to generate.
      Manipulates the parameter n_clusters from KMeans Sklearn class.
    
    : param: number_of_initializations = 10 (integer). Number of times the k-means algorithm is run with different centroid seeds. 
      The final results is the best output of n_init consecutive runs in terms of inertia. Several runs are recommended for 
      sparse high-dimensional problems. Manipulates the parameter n_init from KMeans Sklearn class.

    : param: MAXIMUM_OF_ALLOWED_ITERATIONS = integer representing the maximum number of iterations
      that the optimization algorithm can perform. Depending on data, convergence may not be
      reached within this limit, so you may need to increase this hyperparameter.

    : param: kmeans_algorithm = 'lloyd'. K-means algorithm to use. The classical EM-style algorithm is "lloyd". The 
      "elkan" variation can be more efficient on some datasets with well-defined clusters, by using the triangle inequality. 
      However it’s more memory intensive due to the allocation of an extra array of shape (n_samples, n_clusters).
      Options: “lloyd”, “elkan”, “auto”, “full”. Manipulates the parameter algorithm from KMeans Sklearn class.

    : param: tolerance = 0.0001. Relative tolerance with regards to Frobenius norm of the difference in the cluster centers 
      of two consecutive iterations to declare convergence. Manipulates the parameter tol from KMeans Sklearn class.
    """

    from sklearn.cluster import KMeans
    # https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
    
    RANDOM_STATE = 55 
    ## We will pass it to every sklearn call so we ensure reproducibility (i.e., a new random process)
    
    X = np.array(X_tensor)
    # Check if it is a single-dimension array
    if(len(X) == 1):
        #  Reshape it as a matrix
        X = X.reshape(-1,1)

    # Start K-Means object:
    kmeans_model = KMeans(n_clusters = number_of_clusters, random_state = RANDOM_STATE, n_init = number_of_initializations, max_iter = maximum_of_allowed_iterations, tol = tolerance, verbose = 1, algorithm = kmeans_algorithm)
    # Fit kmeans object to the array:
    kmeans_model = kmeans_model.fit(X)
    # Obtain the cluster correspondent to each entry:
    X_labels = kmeans_model.labels_
    # obtain clusters centroids:
    centroids = kmeans_model.cluster_centers_

    if ControlVars.show_results:
        print("Finished obtaining the K-Means cluster model.")
        print("The model object that may be used for predicting the clusters for new data was returned as kmeans_model.")
        print("The labels (clusters) correspondent to each entry in the input tensor was returned as X_labels, and the model's centroids were returned as centroids.")
        print("Notice that the response predicted by the model is simply the cluster for a given entry.\n")

        print("Check the centroids of the clusters:\n")
        print(centroids)
        print("\n")
        print("Check the 10 first entries from the dataset and the correspondent labels (clusters):\n")
        print(f"{[tuple for tuple in zip(X[:10], X_labels[:10])]}")

    return kmeans_model, X_labels, centroids


def anomaly_detection (X_tensor, defined_threshold = 0.00001, X_test = None, y_test = None):
    """
    anomaly_detection (X_tensor, defined_threshold = 0.00001, X_test = None, y_test = None)

    - Unsupervised learning method for detecting anomaly points, based on the assumption that each variable is normal and independent.
    - Data points considered anomalous are labelled as 1; non-anomalous are labelled as 0.

    : param: defined_threshold = 0.00001 - represents the minimum value of the combined probabilities for a given value
      to be considered anomalous. If no test/validation set is provided, the threshold must be defined by the user.
      If test/validation sets are provided, the best threshold will be calculated from it.
      Notice that the response set is an array containing the label 1 for anomalous (and validated) points, and 0 for
      non-anomalous ones.
    """
    
    X = np.array(X_tensor)

    # Instantiate the AnomalyDetector object:
    anomaly_detection_model = AnomalyDetector(epsilon = defined_threshold)
    # Fit the detector:
    anomaly_detection_model = anomaly_detection_model.fit(X = X)
    
    if ((X_test is not None) & (y_test is not None)):
        X_test = np.array(X_test)
        y_test = np.array(y_test)

        # Estimate the probabilities for X_test
        anomaly_detection_model = anomaly_detection_model.calculate_probabilities(X_tensor = X_test)
        anomaly_detection_model = anomaly_detection_model.select_threshold(y_val = y_test, p_val = detector.estimated_probabilities)
        array_of_outliers = np.array(anomaly_detection_model.predict(X_tensor = X))
        if ControlVars.show_results:
            print(f"Found {np.sum(outliers)} in the array X_tensor.")
            print("The outliers are the elements correspondent to label 1 in the returned array named as 'outliers'.\n")

    else:
        # Apply user defined threshold
        outliers = detector.predict(X_tensor = X_tensor)
        if ControlVars.show_results:
            print(f"Found {np.sum(outliers)} in the array X_tensor.")
            print("The outliers are the elements correspondent to label 1 in the returned array named as 'outliers'.\n")
        
    return anomaly_detection_model, outliers


def benford_outliers_detection (df, column_to_analyze, digits_to_analyze = 1, diff_alert_threshold = 20,
                       horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 0, 
                       y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, 
                       png_resolution_dpi = 330):
    """
    Check the presence of FINANCIAL OUTLIERS through Benford's Law. It may be also applied to fraud detection.
    Examples of situations to analyze: accounting transactions, credit card transactions, customer balances, death rates, 
        diameter of planets, electricity and telephone bills, Fibonacci numbers, incomes, insurance claims, 
        lengths and flow rates of rivers, loan data, numbers of newspaper articles, physical and mathematical constants, 
        populations of cities, powers of 2, purchase orders, stock and house prices.
    
    : param: df (pd.DataFrame): Dataframe with values to be analyzed.
    
    : param: column_to_analyze (str): column with the values to be analyzed.

    : param: digits_to_analyze (integer): 1, 2 or 3. If 1, only the first digit is used for the analysis. If 2,
        the analysis for the first 2 digits is performed; if 3, the first 3 digits are used.
    
    : param: difference_alert (float): percent of deviation from the curve to add an alert. Example: if difference_alert = 20,
        a difference between the percent of leading digit occurence and the expected from the curve of 20% will be sufficient
        for labelling the entry as 'potential_outlier'. Else, label will be 'below_threshold'.
    
    Returns:
        dataset containing counts of occurences of leading digits, percent of occurence, theoretical percent from Benford curve,
        difference in percent between actual and theoretical values, and label if it is a potential outlier, considering the
        threshold set as diff_alert_threshold.
        
        outliers_df, a smaller dataframe containing only the data labelled as potential outliers (digit and % of occurrence).

    
    Theory:

        https://www.journalofaccountancy.com/issues/2017/apr/excel-and-benfords-law-to-detect-fraud.html
        
        Briefly explained, Benford's Law maintains that the numeral 1 will be the leading digit in a genuine
        data set of numbers 30.1% of the time; the numeral 2 will be the leading digit 17.6% of the time; 
        and each subsequent numeral, 3 through 9, will be the leading digit with decreasing frequency. 
        This expected occurrence of leading digits can be illustrated as shown in the chart "Benford's Law."

        https://s3.amazonaws.com/assets.datacamp.com/production/course_8916/slides/chapter4.pdf

        Many datasets satisfy Benford's Law
            - data where numbers represent sizes of facts or events
            - data in which numbers have no relationship to each other
            - data sets that grow exponentially or arise from multiplicative fluctuations
            - mixtures of different data sets
            - Some well-known infinite integer sequences
            Preferably, more than 1000 numbers that go across multiple orders.

        https://repositorio.ufmg.br/bitstream/1843/BUBD-A35FFR/1/tcc___bruno_c_gomes___completo.pdf
        (page 10)
        
        - Benford law for a single digit d1:
            Probability(d1) = P(d1) = log(1 + 1/d1)
        - For 2 digits d1 and d2:
            P(d1d2) = log(1 + (1/d1d2))
            - Notice that the number formed by digit d1 followed by d2 is actually 10*d1 + d2
                e.g. 17 = 10*(1) + 7, d1 = 1, d2 = 7
        - For 3 digits d1, d2, d3:
            P(d1d2d3) = log(1 + (1/d1d2d3))
            - Notice that the number formed by digit d1 followed by d2 is actually 100*d1 + 10*d2 + d3
                e.g. 171 = 100*(1) + 10*(7) + 1, d1 = 1, d2 = 7, d3 = 1
        
        - all log are in base 10
    """
    
    import math
    # https://www.w3schools.com/python/ref_math_log.asp
    

    benford_prob = lambda x: (math.log((1 + 1/x), 10)) * 100
    """
    Calculates probabilities in percents.
        syntax: math.log(x, base), default base is e;
        - math.log(x): natural logarithm of x
        - math.log(x, 10): logarithm of x in base 10

    benford_prob is the probability of obtaining a given x. x may be a single, 2-, or 3-digit number
    """

    # total entries on the dataset
    total = len(df)
    
    if (digits_to_analyze == 1):
        # Expected Benford curve, with values in percent (key: leading digit, value: expected percent of occurrence)
        # expected_curve = {0: 0.0, 1: 30.1, 2: 17.6, 3: 12.5, 4: 9.7, 5: 7.9, 6: 6.7, 7: 5.8, 8: 5.1, 9: 4.6}
        expected_curve = {d1: benford_prob(d1) for d1 in range(1, 10)} # values from 1 to 9
    
    elif (digits_to_analyze == 2):

        possible_numbers = range(10, 100) 
        # when slicing to the second digit, we may obtain values 10, 11,..., 99
        # Naturally, 0 may be obtained.
        expected_curve = {d1d2: benford_prob(d1d2) for d1d2 in possible_numbers}
        # Here, sum of probabilities is ~99.99999999999997%
    
    elif (digits_to_analyze == 3):
        possible_numbers = range(100, 1000) 
        # when slicing to the second digit, we may obtain values 100, 101, 999
        expected_curve = {d1d2d3: benford_prob(d1d2d3) for d1d2d3 in possible_numbers}
        # Here, sum of probabilities is ~99.99999999999993%

    else:
        raise InvalidInputsError("digits_to_analyze must be an integer equals to 1, 2 or 3.")
        
    # Create a local copy of the dataset to manipulate
    dataset = df.copy(deep = True)

    # Firstly, guarantee that the column contains only integers. For that, let's eliminate the decimal separators:
    def eliminate_decimal_seps(x):
        # Get absolute values from x, so that the minus sign will not interfere:
        arr = np.absolute(x)
        # Convert to string
        arr = np.array(arr, dtype = str)
        # https://numpy.org/doc/stable/reference/generated/numpy.char.replace.html
        arr = np.char.replace(arr, '.', '') # replaces decimal separator by empty string.
        # Truncate so that there are no more than 3 characters in the string (3 is the max number to be tested)
        # So we will make the algorithm faster
        arr = pd.Series(arr).apply(lambda x: x[:3])
        # Convert to int and return as numpy array
        arr = np.array(arr, dtype = int)
        return arr

    dataset[column_to_analyze] = eliminate_decimal_seps(dataset[column_to_analyze])
    
    # Extract the first character and count the occurences
    # convert to string and apply a lambda function that extracts the first character from a str x
    if (digits_to_analyze == 1):
        dataset['leading_digits'] = dataset[column_to_analyze].astype(str).apply(lambda x: x[0])
        # Since the object is a Pandas series, the axis = 1 (rows) is implicit for the apply method.
        
        # Filter only entries with first digit different from zero:
        initial_len = len(dataset) # entries before drop.
        dataset = dataset[dataset['leading_digits'] != '0']
        
        if (initial_len != len(dataset)):
            # Entries that do not have 2 digits were dropped. Warn user.
            warning = f"""The probability calculation is based on the assumption that no leading digit is zero.
                There were {initial_len - len(dataset)} rows ({(initial_len - len(dataset))/initial_len*100 : .2f} % of the dataset)
                that had 0 as 1st digit, so they were not considered in the analysis.
                """
            print(warning)
            dataset = dataset.reset_index(drop = True)
    
    elif (digits_to_analyze == 2):
        # slice only the first two digits
        dataset['leading_digits'] = dataset[column_to_analyze].astype(str).apply(lambda x: x[:2])
        
        initial_len = len(dataset) # entries before drop.
        # Filter only entries with first digit different from zero:
        dataset = dataset[dataset['leading_digits'].apply(lambda x: x[0]) != '0']
        # Filter only entries with exactly 2 digits (strings with length == 2)
        dataset = dataset[dataset['leading_digits'].apply(len) == 2]
        
        if (initial_len != len(dataset)):
            # Entries that do not have 2 digits were dropped. Warn user.
            warning = f"""The probability calculation is based on the assumption that there are exactly 2 digits and the first digit
                is not 0. There were {initial_len - len(dataset)} rows ({(initial_len - len(dataset))/initial_len*100 : .2f} % of the dataset)
                that did not presented exactly 2 digits or had 0 as 1st digit, so they were not considered in the analysis.
                """
            print(warning)
            dataset = dataset.reset_index(drop = True)

    elif (digits_to_analyze == 3):
        # slice only the first three digits
        dataset['leading_digits'] = dataset[column_to_analyze].astype(str).apply(lambda x: x[:3])
        
        initial_len = len(dataset) # entries before drop.
        # Filter only entries with first digit different from zero:
        dataset = dataset[dataset['leading_digits'].apply(lambda x: x[0]) != '0']
        # Filter only entries with exactly 3 digits (strings with length == 3)
        dataset = dataset[dataset['leading_digits'].apply(len) == 3]
        
        if (initial_len != len(dataset)):
            # Entries that do not have 3 digits were dropped. Warn user.
            warning = f"""The probability calculation is based on the assumption that there are exactly 3 digits and the first digit
                is not 0. There were {initial_len - len(dataset)} rows ({(initial_len - len(dataset))/initial_len*100 : .2f} % of the dataset)
                that did not presented exactly 3 digits or had 0 as 1st digit, so they were not considered in the analysis.
                """
            print(warning)
            dataset = dataset.reset_index(drop = True)

    dataset = dataset.groupby(by = 'leading_digits', as_index = False, sort = True).count()
    
    dataset = dataset.rename(columns = {column_to_analyze: 'counts'})
    
    # leading digit can be reconverted to integer, to save memory on the dataframe:
    dataset['leading_digits'] = dataset['leading_digits'].astype(int)
    
    # Round to 1 digit, such as the Benford curve
    dataset['digits_pct'] = np.round((np.array(dataset.counts) / total * 100), 1)
    
    # Add a column with the expected_curve: access the index given by 'digit' and the correspondent value on the
    # dictionary expected_curve. Here, as the whole table is manipulated, parameter axis = 1 must be passed to the
    # apply method, avoiding the imputation to a whole column.
    dataset['benford_pct'] = dataset.apply(lambda x: expected_curve[x.leading_digits], axis = 1)

    # Calculate the counting of occurrences predicted by benford curve:
    dataset['benford_predicted_counts'] = np.round(dataset['benford_pct']/100 * total, 0) # 0 decimals, it is a counting
    dataset['benford_predicted_counts'] = dataset['benford_predicted_counts'].astype(int)
    
    # Calculate the difference between theoretical and actual predicted counting:
    dataset['pct_diff'] = np.round((abs(dataset['counts'] - dataset['benford_predicted_counts'])/dataset['benford_predicted_counts'] * 100), 2)
    dataset['label'] = np.where(dataset['pct_diff'] >= diff_alert_threshold, 'potential_outlier', 'below_threshold')
    
    # Let's create a outliers_df containing only data marked as potential outliers:
    outliers_df = dataset.copy(deep = True)
    # Filter potential outliers
    outliers_df = outliers_df[outliers_df['label'] == 'potential_outlier']
    # keep only the columns digit and % of occurrence
    outliers_df = outliers_df[['leading_digits', 'digits_pct']]
     
    if ControlVars.show_results:
        print("Successfully calculated and returned the dataset comparing the digits with Benford's Law, as well as a dataframe containing only data labelled as potential outliers:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(dataset)
                
        except: # regular mode
            print(dataset)
        
    
    # Now the data is prepared and we only have to plot 
    
    # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
    # so that the bars do not completely block other views.
    if ControlVars.show_plots:
        OPACITY = 0.95
        
        # Set labels and titles for the case they are None
        if (plot_title is None):
            
            plot_title = f"Percent_of_leading_digits"
        
        if (horizontal_axis_title is None):

            horizontal_axis_title = 'leading_digits'

        if (vertical_axis_title is None):
            # Notice that response_var_name already has the suffix indicating the
            # aggregation function
            vertical_axis_title = '% of occurence'
        
        fig, ax = plt.subplots(figsize = (12, 8))
        # Set image size (x-pixels, y-pixels) for printing in the notebook's cell:

        # Set xticks - scale of X-Axis:
        if (digits_to_analyze == 1):
            xtick_list = list(range(1, 10)) # every integer from 1 to 9
        
        elif (digits_to_analyze == 2):
            xtick_list = list(range(10, 100, 10)) # every integer from 10 to 99, spaced of 10 units
        
        elif (digits_to_analyze == 3):
            xtick_list = list(range(100, 1000, 100)) # every integer from 100 to 999, spaced of 100 units

        plt.xticks(xtick_list)

        #ROTATE X AXIS IN XX DEGREES
        plt.xticks(rotation = x_axis_rotation)
        # XX = 70 DEGREES x_axis (Default)
        #ROTATE Y AXIS IN XX DEGREES:
        plt.yticks(rotation = y_axis_rotation)
        # XX = 0 DEGREES y_axis (Default)
        
        plt.title(plot_title)
        
        ax.set_xlabel(horizontal_axis_title)
        ax.set_ylabel(vertical_axis_title, color = 'darkblue')

        ax.bar(dataset['leading_digits'], dataset['digits_pct'], color = 'darkblue', alpha = OPACITY, label = 'digits_pct')

        ax.plot(dataset['leading_digits'], dataset['benford_pct'], color = 'fuchsia', linestyle = 'dashed', alpha = OPACITY, label = "Benford's Law\nTheoretical Percent (%)")
        
        
        # If there are red points labelled as potential outliers, plot them above the graph
        # (plot as scatter plot, with no spline, and 100% opacity = 1.0):
        if (len(outliers_df) > 0):
            
            ax.plot(outliers_df['leading_digits'], outliers_df['digits_pct'], linestyle = '', marker = 'o', color = 'firebrick', alpha = 1.0, label = "Potential\nOutlier")
        
        ax.legend()
        ax.grid(grid) # shown if user set grid = True
        # If user wants to see the grid, it is shown only for the cumulative line.

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
                file_name = "benford_check"
            
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
    
        plt.show()
    

    if ControlVars.show_results:
        fraud_text = """
        Benford's Law for fraud detection (from DataCamp)
        Fraud is typically committed by adding invented numbers or changing real observations.
        - Benford’s Law is popular tool for fraud detection and is even legally admissible as evidence in the US.
        - It has for example been successfully applied for claims fraud, check fraud, electricity theft, forensic accounting 
        and payments fraud.
        - See also the book Benford's Law: Applications for forensic accounting, auditing, and fraud detection of Nigrini (John Wiley & Sons, 2012).
        
        Be careful!
        Note that it is always possible that data does just not conform to Benford's Law:
        - If there is lower and/or upper bound or data is concentrated in narrow interval
            e.g. hourly wage rate, height of people.
        - If numbers are used as identification numbers or labels
            e.g. social security number, flight numbers, car license plate numbers, phone numbers.
        - Additive fluctuations instead of multiplicative fluctuations
            e.g. heartbeats on a given day
        
        Check the presence of FINANCIAL OUTLIERS through Benford's Law. It may be also applied to fraud detection.
        Examples of situations to analyze: accounting transactions, credit card transactions, customer balances, death rates, 
            diameter of planets, electricity and telephone bills, Fibonacci numbers, incomes, insurance claims, 
            lengths and flow rates of rivers, loan data, numbers of newspaper articles, physical and mathematical constants, 
            populations of cities, powers of 2, purchase orders, stock and house prices.
        
        Many datasets satisfy Benford's Law
        - data where numbers represent sizes of facts or events
        - data in which numbers have no relationship to each other
        - data sets that grow exponentially or arise from multiplicative fluctuations
        - mixtures of different data sets
        - Some well-known infinite integer sequences
        Preferably, more than 1000 numbers that go across multiple orders.

        """
        print(fraud_text)
    

    return dataset, outliers_df

