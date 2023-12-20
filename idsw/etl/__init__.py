__doc__ = """
idsw.etl
===============
Workflow for extraction, transformation, characterization and load of data.
Use it to conduct a full statistical and time series characterization (and modelling), as well as a complete
Exploratory Data Analysis (EDA):

    Applying a list of row filters;
    Merging on timestamp;
    Merging (joining) dataframes on given keys; and sorting the merged table;
    Record linkage: fuzzy merging (joining) of dataframes on similar strings;
    Concatenating (SQL Union/Stacking/Appending) dataframes;
    Dataframe general characterization;
    Dropping specific columns or rows from the dataframe;
    Removing duplicate rows from the dataframe;
    Removing all columns and rows that contain only missing values;
    Grouping by timestamp;
    Grouping by a given variable;
    Extracting timestamp information;
    Calculating differences between successive timestamps (delays);
    Calculating timedeltas;
    Adding or subtracting timedeltas;
    Slicing the dataframe (selecting a specific subset of rows);
    Visualizing and characterizing distribution of missing values;
    Visualizing missingness across a variable, and comparing it to another variable (both numeric);
    Dealing with missing values;
    Visualizing time series;
    Visualizing histograms;
    Plotting bar charts;
    Testing normality and visualizing the probability plot;
    Testing and visualizing probability plots for different statistical distributions;
    Calculating cumulative statistics;
    Obtaining the correlation plot;
    Obtaining the covariance matrix;
    Obtaining Variance Inflation Factors (VIFs);
    Obtaining scatter plots and simple linear regressions;
    Performing the polynomial fitting;
    Filtering (selecting); ordering; or renaming columns from the dataframe;
    Renaming specific columns from the dataframe; or cleaning columns' labels;
    Removing trailing or leading white spaces or characters (trim) from string variables, and modifying the variable type;
    Capitalizing or lowering case of string variables (string homogenizing);
    Adding contractions to the contractions library;
    Correcting contracted strings;
    Substituting (replacing) substrings on string variables;
    Inverting the order of the string characters;
    Slicing the strings;
    Getting the leftest characters from the strings (retrieve last characters);
    Getting the rightest characters from the strings (retrieve first characters);
    Joining strings from a same column into a single string;
    Joining several string columns into a single string column;
    Splitting strings into a list of strings;
    Substituting (replacing or switching) whole strings by different text values (on string variables);
    Replacing strings with Machine Learning: finding similar strings and replacing them by standard strings;
    Searching for Regular Expression (RegEx) within a string column;
    Replacing a Regular Expression (RegEx) from a string column;
    Applying Fast Fourier Transform;
    Generating columns with frequency information;
    Transforming the dataset and reverse transforms: log-transform;
    Exponential transform;
    Box-Cox transform;
    Square-root transform;
    Cube-root transform;
    General power transform;
    One-Hot Encoding;
    Ordinal Encoding;
    Feature scaling;
    Lag-diagnosis: obtaining autocorrelation (ACF) and partial autocorrelation function (PACF) plots of the time series;
    Obtaining the 'd' parameter of ARIMA (p, q, d) model;
    Obtaining the best ARIMA (p, q, d) model;
    Forecasting with ARIMA model;
    Forecasting with Facebook Prophet model;
    Obtaining rolling window statistics of the dataframe;
    Decomposing seasonality and trend of the time series;
    Calculating general statistics for a given column;
    Getting data quantiles for a given column;
    Getting a particular P-percent quantile limit for a given column;
    Selecting subsets from a dataframe (using row filters) and labelling these subsets;
    Estimating ideal sample size for tests;
    Performing Analysis of Variance (ANOVA); and obtaining box plots or violin plots;
    Performing AB-Tests;
    Obtaining Statistical Process Control (SPC) charts;
    Evaluating the Process Capability (in relation to specifications).
"""

from .core import *
from .timestamps import *
from .joinandgroup import *
from .cleansing import *
from .characterize import *
from .strings import *
from .transform import *
from .timeseries import *
from .meandifference import *
from .procdiagnosis import *
