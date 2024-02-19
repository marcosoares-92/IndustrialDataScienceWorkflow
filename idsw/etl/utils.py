import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from idsw import (InvalidInputsError, ControlVars)
from .transform import (OrdinalEncoding_df, reverse_OrdinalEncoding)


class EncodeDecode:
    """Helper class for applying the ordinal encoding or decoding functions on situations where user only
    wants to convert the data to calculate statistics that demmand numeric values, but which are applied to
    categorical data
    
    : params df = df_categorical and 
        subset_of_features_to_be_encoded = categorical_list: parameters from OrdinalEncoding_df, reverse_OrdinalEncoding functions.
        Represent the dataframe containing only categorical variables, and a list with such variables.

    """
    def __init__ (self, df_categorical, categorical_list):
        
        self.df = df_categorical.copy(deep = True)
        self.features = categorical_list
    
    def encode(self):

        if ControlVars.show_results:
            # Silence the encoder:
            ControlVars.show_results = False
        
        df_categorical, self.ordinal_encoding_list = OrdinalEncoding_df (df = self.df, subset_of_features_to_be_encoded = self.features)
        # Get the new columns generated from Ordinal Encoding:
        self.new_encoded_cols = [column + "_OrdinalEnc" for column in self.features]
        # Remove the columns that do not have numeric variables before grouping
        self.df_categorical = df_categorical.drop(columns = categorical_list)
        
        if not ControlVars.show_results:
            # Turn-on the encoder again:
            ControlVars.show_results = True
        
        return self
    

    def decode(self, new_df = None, df_numeric = None):
        """: param: new_df - only used when a non-encoded dataframe new_df will be
        decoded using the same parameters. Example: the encoded dataframe was transformed
        and now it will be decoded.
        """

        if ControlVars.show_results:
            # Silence the encoder:
            ControlVars.show_results = False
        
        """
        Run next step if there is a new dataframe. For a variable var, syntax 
            if var:
                # is equivalent to: "run only when variable var is not None." or "run only if var is True".
        """
        if new_df:
            self.df_categorical = new_df.copy(deep = True)

        # Now, reverse encoding and keep only the original column names:
        self.df_categorical = reverse_OrdinalEncoding (df = self.df_categorical, encoding_list = self.ordinal_encoding_list)
        
        if not ControlVars.show_results:
            # Turn-on the encoder again:
            ControlVars.show_results = True
        
        try:
            # Try dropping columns with name of the features + "_OrdinalEnc":
            df_categorical = df_categorical.drop(columns = self.new_encoded_cols)
        except:
            # If impossible, simply select the original features:
            self.df_categorical = df_categorical[self.features]
        
        # Run next step if there is a numeric dataset.
        if df_numeric:
            # Concatenate the dataframes in the columns axis (append columns):
            self.cleaned_df = pd.concat([df_numeric, df_categorical], axis = 1, join = "inner")
        
        else:
            self.cleaned_df = df_categorical
        
        return self


def mode_retrieval(modes_series):
    """Helper function for retrieving only the value of mode returned from Scipy.stats
    
    : param: modes_series: Pandas series, np.array, list or iterable containing the 
    Scipy ModeResults (named tuples):
    ModeResult(mode=calculated_mode, count=counting_of_occurrences))
    # To retrieve only the mode, we must access the element [0] from this tuple
     or attribute mode.

    An error is generated when trying to access an array storing no values.
    (i.e., with missing values). Since there is no dimension, it is not possible
    to access the [0][0] position. In this case, simply append the np.nan 
    the (missing value):
    """
    
    try:
        list_of_modes = [mode_tuple.mode for mode_tuple in modes_series]
    
    except:
        try:
            list_of_modes = [mode_tuple[0] for mode_tuple in modes_series]
        
        except:
            list_of_modes = []
            for mode_tuple in modes_series:
                try:
                    if ((mode_tuple != np.nan) & (mode_tuple is not None)):
                        list_of_modes.append(mode_tuple)
                    else:
                        list_of_modes.append(mode_tuple)
                except:
                    list_of_modes.append(mode_tuple)
    
    return np.array(list_of_modes)
