__doc__ = """
idsw.modelling
===============
Workflow for obtaining machine learning supervised and non-supervised 
classification and regression models:

    Separate and prepare features and responses tensors;
    Splitting features and responses into train and test tensors;
    Splitting time series into train and test tensors;
    Creating a TensorFlow windowed dataset from a time series;
    Retrieving the list of classes used for training the classification models;
    Ordinary Least Squares (OLS) Linear Regression;
    Ridge Linear Regression;
    Lasso Linear Regression;
    Elastic Net Linear Regression;
    Logistic Regression (binary classification);
    Getting a general feature ranking;
    Calculating metrics for regression models;
    Calculating metrics for classification models;
    Making predictions with the models;
    Calculating probabilities associated to each class;
    Performing the SHAP feature importance analysis;
    Fitting the Random Forest Model;
    Fitting the Extreme Gradient Boosting (XGBoost) Model;
    Getting a general feature ranking;
    Scikit-learn Multi-Layer Perceptron;
    Keras Dense Artificial Neural Network (ANN);
    Converting the datasets into NumPy arrays with correct format for CNN and RNN Architectures;
    Convolutional Neural Network (CNN) Architecture;
    Simplified Long Short-Term Memory (LSTM) Recurrent Neural Network (RNN) Architecture;
    Encoder-Decoder Recurrent Neural Network (RNN) Architecture;
    CNN-LSTM Hybrid Architecture;
    Generate test datasets for sensitivity analysis;
    Using the models to predict outputs;
    Obtaining the distance matrix to find similarities;
    Applying the K-Means Elbow method to find ideal number of clusters;
    K-Means Clustering;
    Anomaly detection.
"""

from .core import *
from .utils import *
from .preparetensors import *
from .linear import *
from .trees import *
from .mlp import *
from .deep import *
from .nonsupervised import *