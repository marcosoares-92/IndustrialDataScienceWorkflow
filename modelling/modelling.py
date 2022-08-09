# FUNCTIONS FROM INDUSTRIAL DATA SCIENCE WORKFLOW (IDSW) PACKAGE
# Modelling and Machine Learning

# Marco Cesar Prado Soares, Data Scientist Specialist @ Bayer Crop Science LATAM
# marcosoares.feq@gmail.com
# marco.soares@bayer.com
from dataclasses import dataclass


class model_checking:
            
    # Initialize instance attributes.
    # define the Class constructor, i.e., how are its objects:
    def __init__(self, model_object, model_type = 'regression', model_package = 'tensorflow', column_map_dict = None, training_history_dict = None, X = None, y_train = None, y_preds_for_train = None, y_test = None, y_preds_for_test = None, y_valid = None, y_preds_for_validation = None):

        import numpy as np
        import tensorflow as tf

        # Add the model:        
        self.model = model_object
        # model_type = 'regression' or 'classification'
        self.model_type = model_type
        
        # Add model package: 'tensorflow' (and keras), 'sklearn', or 'xgboost':
        self.package = model_package

        # Add the columns names:
        self.column_map_dict = column_map_dict
        # Add the training history to the class:
        self.history = training_history_dict

        # Add the y series for computing general metrics:
        # Guarantee that they are tensorflow tensors
        if (y_train is not None):
            self.y_train = tf.constant(y_train)
        else:
            self.y_train = None
        if (y_preds_for_train is not None):
            self.y_preds_for_train = tf.constant(y_preds_for_train)
        else:
            self.y_train = None
        if (y_test is not None):
            self.y_test = tf.constant(y_test)
        else:
            self.y_test = None
        if (y_preds_for_test is not None):
            self.y_preds_for_test = tf.constant(y_preds_for_test)
        else:
            self.y_preds_for_test = None
        if (y_valid is not None):
            self.y_valid = tf.constant(y_valid)
        else:
            self.y_valid = None
        if (y_preds_for_validation is not None):
            self.y_preds_for_validation = tf.constant(y_preds_for_validation)
        else:
            self.y_preds_for_validation = None

        # X can be X_train, X_test, or X_valid. 
        # We only want to obtain the total number of predictors. X.shape is like:
        # TensorShape([253, 11]). Second index [1] is the number of predictors:
        if (X is not None):
            # make sure it is a tensor:
            X = tf.constant(X)
            total_predictors = X.shape[1]
            self.total_predictors = total_predictors

        # to check the class attributes, use the __dict__ method. Examples:
        ## object.__dict__ will show all attributes from object
                
    # Define the class methods.
    # All methods must take an object from the class (self) as one of the parameters
    
    def model_metrics (self, show_confusion_matrix_values = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
        
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        import tensorflow as tf
        # https://www.tensorflow.org/api_docs/python/tf/keras/metrics?authuser=1
        import tensorflow_addons as tfa
        # https://www.tensorflow.org/addons
        from sklearn.metrics import classification_report, confusion_matrix, r2_score
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html

        # Retrieve type of problem:
        model_type = self.model_type

        # Retrieve the tensors.
        tensors_dict = {}
        tensors_dict['training'] = {'actual': self.y_train, 'predictions': self.y_preds_for_train}
        tensors_dict['testing'] = {'actual': self.y_test, 'predictions': self.y_preds_for_test}
        tensors_dict['validation'] = {'actual': self.y_valid, 'predictions': self.y_preds_for_validation}

        metrics_dict = {}

        # Loop through the keys:
        for key in tensors_dict.keys():
          
            # Retrieve the nested dictionary:
            nested_dict = tensors_dict[key]
            # Retrieve actual and predicted values:
            y_true =  nested_dict['actual']
            y_pred = nested_dict['predictions']
            # Check if there is no None value stored:
            if ((y_true is not None) & (y_pred is not None)):

                calculated_metrics = {}

                # Regression metrics:
                if (model_type == 'regression'):

                    print(f"Metrics for {key}:\n")
                    mse = tf.keras.metrics.mean_squared_error(y_true, y_pred)
                    #https://www.tensorflow.org/api_docs/python/tf/keras/metrics/mean_squared_error?authuser=1
                    # The function returns a NumPy array containing a single element. Extract it as
                    # variable:
                    try:
                        mse = mse[0]
                    except: # mse is a scalar, not an array
                        pass
                    # Print in scientific notation:
                    print(f"Mean squared error (MSE) = {mse:e}")
                    # Add to calculated metrics:
                    calculated_metrics['mse'] = mse

                    # rmse is not available as function, only class. Use numpy method to convert to value
                    # https://www.tensorflow.org/api_docs/python/tf/keras/metrics/RootMeanSquaredError?authuser=1
                    # Create the object:
                    rmse = tf.keras.metrics.RootMeanSquaredError()
                    # Update its state:
                    rmse = rmse.update_state(y_true, y_pred)
                    # Use the numpy method to retrieve only the value:
                    rmse = rmse.numpy()
                    # Here, numpy method already returns a scalar
                    # Print in scientific notation:
                    print(f"Root mean squared error (RMSE) = {rmse:e}")
                    # Add to calculated metrics:
                    calculated_metrics['rmse'] = rmse

                    # https://www.tensorflow.org/api_docs/python/tf/keras/metrics/mean_absolute_error?authuser=1
                    mae = tf.keras.metrics.mean_absolute_error(y_true, y_pred)
                    # The function returns a NumPy array containing a single element. Extract it as
                    # variable:
                    try:
                        mae = mae[0]
                    except: # mae is a scalar, not an array
                        pass
                    
                    # Print in scientific notation:
                    print(f"Mean absolute error (MAE) = {mae:e}")
                    # Add to calculated metrics:
                    calculated_metrics['mae'] = mae

                    # https://www.tensorflow.org/api_docs/python/tf/keras/metrics/mean_absolute_percentage_error?authuser=1
                    mape = tf.keras.metrics.mean_absolute_percentage_error(y_true, y_pred)
                    # The function returns a NumPy array containing a single element. Extract it as
                    # variable:
                    try:
                        mape = mape[0]
                    except: # mape is a scalar, not an array
                        pass
                    
                    # Print in scientific notation:
                    print(f"Mean absolute percentage error (MAPE) = {mape:e}")
                    # Add to calculated metrics:
                    calculated_metrics['mape'] = mape
                    
                    try:
                        # R2 and R2-adj are available only as tfa object:
                        # https://www.tensorflow.org/addons/api_docs/python/tfa/metrics/RSquare
                        # Create the object:
                        r2 = tfa.metrics.RSquare()
                        # Update its state:
                        # tfa method returns None, so we must only call the method:
                        r2.update_state(y_true, y_pred)
                        # Use the numpy method to retrieve only the value:
                        r2 = r2.result().numpy() # already a scalar
                        # for this tfa metrics, the methods result and numpy must be chained
                        # otherwise, an error will be raised.
                        print(f"Coefficient of linear correlation R² = {r2:e}")
                        # Add to calculated metrics:
                        calculated_metrics['r_squared'] = r2
                        
                    except:
                        r2 = r2_score(y_true.numpy(), y_pred.numpy())
                        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html
                        print(f"Coefficient of linear correlation R² = {r2:e}")
                        # Add to calculated metrics:
                        calculated_metrics['r_squared'] = r2
                    
                    try:
                        # Try to calculate the adjusted R² by accessing the number of predictors:
                        # This number may not be present.
                        total_predictors = self.total_predictors
                        # Create the object:
                        r2_adj = tfa.metrics.RSquare(num_regressors = total_predictors)
                        # Update its state. Again, method returns None:
                        r2_adj.update_state(y_true, y_pred)
                        # Use the numpy method to retrieve only the value:
                        r2_adj = r2_adj.result().numpy() # scalar
                        # Again, the methods result and numpy must be chained
                        print(f"Adjusted coefficient of correlation R²-adj = {r2_adj:e}")
                        # Add to calculated metrics:
                        calculated_metrics['r_squared_adj'] = r2_adj

                    except:
                        # Manually correct R²:
                        # n_size_train = number of sample size
                        # k_model = number of independent variables of the defined model
                        k_model = self.total_predictors
                        #numer of rows
                        n_size = len(y_true)
                        r2_adj = 1 - (1 - r2)*(n_size - 1)/(n_size - k_model - 1)
                        print(f"Adjusted coefficient of correlation R²-adj = {r2_adj:e}")
                        # Add to calculated metrics:
                        calculated_metrics['r_squared_adj'] = r2_adj
                    
                    print("\n")
                    # Now, add the metrics to the metrics_dict:
                    metrics_dict[key] = calculated_metrics

                else:
                    
                    print(f"Metrics for {key}:\n")
                    # https://www.tensorflow.org/api_docs/python/tf/keras/metrics/AUC
                    # Create the object:
                    auc = tf.keras.metrics.AUC()
                    # Update its state:
                    auc.update_state(y_true, y_pred)
                    # Use the numpy method to retrieve only the value:
                    auc = auc.result().numpy() # scalar
                    print(f"AUC = {auc:e}")
                    # Add to calculated metrics:
                    calculated_metrics['auc'] = auc

                    # https://www.tensorflow.org/api_docs/python/tf/keras/metrics/Accuracy
                    # Create the object:
                    acc = tf.keras.metrics.Accuracy()
                    # Update its state:
                    acc.update_state(y_true, y_pred)
                    # Use the numpy method to retrieve only the value:
                    acc = acc.result().numpy() # scalar
                    print(f"Accuracy = {acc:e}")
                    # Add to calculated metrics:
                    calculated_metrics['accuracy'] = acc

                    # https://www.tensorflow.org/api_docs/python/tf/keras/metrics/Precision
                    # Create the object:
                    precision = tf.keras.metrics.Precision()
                    # Update its state:
                    precision.update_state(y_true, y_pred)
                    # Use the numpy method to retrieve only the value:
                    precision = precision.result().numpy() # scalar
                    print(f"Precision = {precision:e}")
                    # Add to calculated metrics:
                    calculated_metrics['precision'] = precision

                    # https://www.tensorflow.org/api_docs/python/tf/keras/metrics/Recall
                    # Create the object:
                    recall = tf.keras.metrics.Recall()
                    # Update its state:
                    recall.update_state(y_true, y_pred)
                    # Use the numpy method to retrieve only the value:
                    recall = recall.result().numpy() # scalar
                    print(f"Recall = {recall:e}")
                    # Add to calculated metrics:
                    calculated_metrics['recall'] = recall
                    
                    # The method update_state returns None, so it must be called without and equality

                    # Get the classification report:
                    print("Classification Report:\n")
                    # Convert tensors to NumPy arrays
                    report = classification_report (y_true.numpy(), y_pred.numpy())
                    print(report)
                    # Add to calculated metrics:
                    calculated_metrics['classification_report'] = report
                    print("\n")

                    # Get the confusion matrix:
                    # Convert tensors to NumPy arrays
                    matrix = confusion_matrix (y_true.numpy(), y_pred.numpy())
                    # Add to calculated metrics:
                    calculated_metrics['confusion_matrix'] = report
                    print("Check the confusion matrix:\n")

                    fig, ax = plt.subplots(figsize = (12, 8))
                    # possible color schemes (cmap) for the heat map: None, 'Blues_r',
                    # "YlGnBu",
                    # https://seaborn.pydata.org/generated/seaborn.heatmap.html?msclkid=73d24a00c1b211ec8aa1e7ab656e3ff4
                    # http://seaborn.pydata.org/tutorial/color_palettes.html?msclkid=daa091f1c1b211ec8c74553348177b45
                    ax = sns.heatmap(matrix, annot = show_confusion_matrix_values, fmt = ".0f", linewidths = .5, square = True, cmap = 'Blues_r');
                    #annot = True: shows the number corresponding to each square
                    #annot = False: do not show the number
                    plot_title = f"Accuracy Score for {key} = {acc:.2f}"
                    ax.set_title(plot_title)
                    ax.set_ylabel('Actual class')
                    ax.set_xlabel('Predicted class')
                    
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
                            file_name = "confusion_matrix_" + key
                        
                        else:
                            # add the train suffix, to differentiate from the test matrix:
                            file_name = file_name + "_" + key
                        
                        #check if the user defined an image resolution. If not, set as the default 110 dpi
                        # resolution.
                        if (png_resolution_dpi is None):
                            #set as 330 dpi
                            png_resolution_dpi = 330
                        
                        #Get the new_file_path
                        new_file_path = os.path.join(directory_to_save, file_name)
                        
                        #Export the file to this new path:
                        # The extension will be automatically added by the savefig method:
                        plt.savefig(new_file_path, dpi = png_resolution_dpi, quality = 100, format = 'png', transparent = False) 
                        #quality could be set from 1 to 100, where 100 is the best quality
                        #format (str, supported formats) = 'png', 'pdf', 'ps', 'eps' or 'svg'
                        #transparent = True or False
                        # For other parameters of .savefig method, check https://indianaiproduction.com/matplotlib-savefig/
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
                    # Now, add the metrics to the metrics_dict:
                    metrics_dict[key] = calculated_metrics
          
        # Now that we finished calculating metrics for all tensors, save the
        # dictionary as a class variable (attribute) and return the object:
        self.metrics_dict = metrics_dict
        
        return self
    
    def feature_importance_ranking (self, model_class = 'linear', orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):

        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt

        # model_class = 'linear' or model_class = 'tree'
        # Retrieve the model:
        model = self.model
        # Return the mapping dictionary:
        column_map_dict = self.column_map_dict
        model_type = self.model_type

        if (model_class == 'linear'):

            if (column_map_dict is not None):
                # Retrieve the values (columns' names):
                # Set as list
                columns_list = list(column_map_dict['features'].values())
            
            # Get the list of coefficients
            reg_coefficients = model.coef_
            # This is an array containing a single array like [[coef1, coef2, ...]]
            # So, the index 0 stores the array of interest. 
            # Since coefficients may be negative, pick the absolute values from the array in index 0
            # (NumPy arrays accept vectorial operations, lists do not):
            
            try:
                reg_coefficients = abs(reg_coefficients[0])
                # Now, convert to list:
                reg_coefficients = list(reg_coefficients)
            
             
            except: # reg_coefficients[0] is a scalar, not a list
                reg_coefficients = abs(np.array(reg_coefficients))
                # Now, convert to list:
                reg_coefficients = [reg_coefficients]
                
            
            if (column_map_dict is None):
                # Retrieve the values (columns' names):
                columns_list = [i for i in range(0, len(reg_coefficients))]

            # Append the intercept coefficient to this list:
            print(f"Calculated model intercept = {model.intercept_}\n")
            
            try:
                # Create the regression dictionary:
                reg_dict = {'predictive_features': columns_list,
                          'regression_coefficients': reg_coefficients}

                # Convert it to a Pandas dataframe:
                feature_importance_df = pd.DataFrame(data = reg_dict)

                # Now sort the dataframe in descending order of coefficient, and ascending order of
                # feature (when sorting by multiple columns, we pass a list of columns to by and a 
                # list of booleans to ascending, instead of passing a simple string to by and a boolean
                # to ascending. The element on a given index from the list by corresponds to the boolean
                # with the same index in ascending):
                feature_importance_df = feature_importance_df.sort_values(by = ['regression_coefficients', 'predictive_features'], ascending = [False, True])

                # Now that the dataframe is sorted in descending order, it represents the feature
                # importance ranking.

                # Restart the indices:
                feature_importance_df = feature_importance_df.reset_index(drop = True)
            
            except:
                print("Model has number of coefficients different from number of predictors.")
                print(f"Model's coefficients = {reg_coefficients}\n")


        elif (model_class == 'tree'):

            # Set the list of the predictors:
            # Use the list attribute to guarantee that it is a list:
            
            if (column_map_dict is not None):
                # Retrieve the values (columns' names):
                columns_list = list(column_map_dict['features'].values())
            
            # Get the list of feature importances. Apply the list method to convert the
            # array from .feature_importances_ to a list:
            feature_importances = model.feature_importances_
            # This is an array containing a single array like [[coef1, coef2, ...]]
            # So, the index 0 stores the array of interest.
            # Pick the absolute values from the array in index 0
            # (NumPy arrays accept vectorial operations, lists do not):
            
            try:
                feature_importances = abs(feature_importances[0])
                # Now, convert to list:
                feature_importances = list(feature_importances)
            
            except: # feature_importances[0] is a scalar, not a list
                feature_importances = abs(np.array(feature_importances))
                # Now, convert to list:
                feature_importances = [feature_importances]
                
                
            if (column_map_dict is None):
                # Retrieve the values (columns' names):
                columns_list = [i for i in range(0, len(feature_importances))]
            
            try:
                # Create the model dictionary:
                model_dict = {'predictive_features': columns_list,
                          'feature_importances': feature_importances}

                # Convert it to a Pandas dataframe:
                feature_importance_df = pd.DataFrame(data = model_dict)
            
                # Now sort the dataframe in descending order of importance, and ascending order of
                # feature (when sorting by multiple columns, we pass a list of columns to by and a 
                # list of booleans to ascending, instead of passing a simple string to by and a boolean
                # to ascending. The element on a given index from the list by corresponds to the boolean
                # with the same index in ascending):
                feature_importance_df = feature_importance_df.sort_values(by = ['feature_importances', 'predictive_features'], ascending = [False, True])

                # Now that the dataframe is sorted in descending order, it represents the feature
                # importance ranking.

                # Restart the indices:
                feature_importance_df = feature_importance_df.reset_index(drop = True)
            
            except:
                print("Model feature importance ranking generated a total of values different from number of predictors.")
                print(f"Model's feature_importances = {feature_importances}\n")

        try:  

            try:
                print("Feature importance ranking - until 20 most important features:\n")
                # only works in Jupyter Notebook:
                from IPython.display import display
                display(feature_importance_df.head(20))

            except: # regular mode
                print("Feature importance ranking - until 20 most important features:\n")
                print(feature_importance_df.head(20))

            # Save the feature importance ranking as a class variable (attribute):
            self.feature_importance_df = feature_importance_df

            features = feature_importance_df['predictive_features']

            if (model_class == 'linear'):
                importances = feature_importance_df['regression_coefficients']

            elif (model_class == 'tree'):
                importances = feature_importance_df['feature_importances']

            data_label = "feature_importance_ranking"

            # Normalize the importances by dividing all of them by the maximum:
            max_importance = max(importances)
            importances = importances/max_importance

            # Now, limit to 10 values to plot:
            importances = importances[:10]
            features = features[:10]

            # Now, plot the bar chart
            print("\n")
            print("Check the feature importance bar chart:\n")
            # Now the data is prepared and we only have to plot 
            # categories, responses, and cum_pct:

            # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
            # so that the bars do not completely block other views.
            OPACITY = 0.95

            # Set labels and titles for the case they are None
            if (plot_title is None):

                plot_title = "feature_importance_bar_chart"

            if (horizontal_axis_title is None):

                horizontal_axis_title = "feature"

            if (vertical_axis_title is None):
                # Notice that response_var_name already has the suffix indicating the
                # aggregation function
                vertical_axis_title = "importance_score"

            fig, ax = plt.subplots(figsize = (12, 8))
            # Set image size (x-pixels, y-pixels) for printing in the notebook's cell:

            #ROTATE X AXIS IN XX DEGREES
            plt.xticks(rotation = x_axis_rotation)
            # XX = 70 DEGREES x_axis (Default)
            #ROTATE Y AXIS IN XX DEGREES:
            plt.yticks(rotation = y_axis_rotation)
            # XX = 0 DEGREES y_axis (Default)

            plt.title(plot_title)

            if (orientation == 'horizontal'):

                # invert the axes in relation to the default (vertical, below)
                ax.set_ylabel(horizontal_axis_title)
                ax.set_xlabel(vertical_axis_title, color = 'darkblue')

                # Horizontal bars used - barh method (bar horizontal):
                # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.barh.html
                # Now, the categorical variables stored in series categories must be
                # positioned as the vertical axis Y, whereas the correspondent responses
                # must be in the horizontal axis X.
                ax.barh(features, importances, color = 'darkblue', alpha = OPACITY, label = data_label)
                #.barh(y, x, ...)

            else: 

                ax.set_xlabel(horizontal_axis_title)
                ax.set_ylabel(vertical_axis_title, color = 'darkblue')
                # If None or an invalid orientation was used, set it as vertical
                # Use Matplotlib standard bar method (vertical bar):
                # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html#matplotlib.pyplot.bar

                # In this standard case, the categorical variables (categories) are positioned
                # as X, and the responses as Y:
                ax.bar(features, importances, color = 'darkblue', alpha = OPACITY, label = data_label)
                #.bar(x, y, ...)

            ax.legend()
            ax.grid(grid)

            # Notice that the .plot method is used for generating the plot for both orientations.
            # It is different from .bar and .barh, which specify the orientation of a bar; or
            # .hline (creation of an horizontal constant line); or .vline (creation of a vertical
            # constant line).

            # Now the parameters specific to the configurations are finished, so we can go back
            # to the general code:

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
                    file_name = "feature_importance_ranking"

                #check if the user defined an image resolution. If not, set as the default 110 dpi
                # resolution.
                if (png_resolution_dpi is None):
                    #set as 330 dpi
                    png_resolution_dpi = 330

                #Get the new_file_path
                new_file_path = os.path.join(directory_to_save, file_name)

                #Export the file to this new path:
                # The extension will be automatically added by the savefig method:
                plt.savefig(new_file_path, dpi = png_resolution_dpi, quality = 100, format = 'png', transparent = False) 
                #quality could be set from 1 to 100, where 100 is the best quality
                #format (str, supported formats) = 'png', 'pdf', 'ps', 'eps' or 'svg'
                #transparent = True or False
                # For other parameters of .savefig method, check https://indianaiproduction.com/matplotlib-savefig/
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
        
        except:
            print("Unable to generate plot correlating feature to its importance.\n")
            self.feature_importance_df = pd.DataFrame() # empty dataframe
        
        if (model_type == 'classification'):
            
            # Print meaning of classification metrics
            print("Metrics definitions:\n")
            print("True Positive (TP): the model correctly predicts a positive class output, i.e., it correctly predicts that the classified element belongs to that class (in binary classification, like in logistic regression, the model predicts the output 1 and the real output is also 1).")
            print("\n")
            print("True Negative (TN): the model correctly predicts a negative class output, i.e., it correctly predicts that the classified element do not belong to that class (in binary classification, the model predicts the output 0 and the real output is also 0).")
            print("\n")
            print("False Positive (FP, type 1 error): the model incorrectly predicts a positive class for a negative class-element, i.e., it predicts that the element belongs to that class, but it actually does not (in binary classification, the model predicts an output 1, but the correct output is 0).")
            print("\n")
            print("False Negative (FN, type 2 error): the model incorrectly predicts a negative class for a positive class-element, i.e., it predicts that the element does not belong to that class, but it actually does (in binary classification, the model predicts an output 0, but the correct output is 1).")
            print("\n")
            print("Naturally, the total number (TOTAL) of classifications is the sum of total correct predictions with total incorrect predictions, i.e., TOTAL = TP + TN + FP + FN")
            print("\n") # line break
            print("Accuracy: relation between the total number of correct classifications and the total number of classifications performed, i.e., Accuracy = (TP + TN)/(TOTAL)")
            print("\n")
            print("Precision: it is referrent to the attempt of answering the question: \'What is the proportion of positive identifications that were actually correct?\'.")
            print("In other words, Precision is the relation between the number of true positives and the total of positively-labelled classifications (true and false positives), i.e., Precision = (TP)/(TP + FP)")
            print("\n")
            print("Recall: it is referrent to the attempt of answering the question: \'What is the proportion of elements from positive class that were correctly classified?\'.")
            print("In other words, Recall is the relation between the number of true positives and the total of elements from the positive class (true positives and false negatives), i.e., Recall = (TP)/(TP + FN)")
            print("\n")
            print("F1: is the ROC-AUC score. In a generic classification problem, this metric is representative of the capability of the model in distinguishing classes.")     
            print("F1 =2/((1/Precision)+(1/Recall)) = (2*(Precision)*(Recall))/(Precision + Recall)")
            print("\n") # line break
            # Check:
            # https://towardsdatascience.com/how-to-evaluate-your-machine-learning-models-with-python-code-5f8d2d8d945b
                  
            print("Confusion Matrix Interpretation:\n")
            print("The confusion matrix is a table commonly used for describing the performance of a classification model (a classifier). It visually compares the model outputs with the correct data labels.")
            print("The matrix is divided into several sectors. For a binary classifier, it is divided into 4 quadrants.")
            print("\n")
            print("Each sector represents a given classification: in the vertical (Y) axis, the real observed labels are shown; whereas the predicted classes (model's outputs) are represented in the horizontal (X) axis.")
            print("Then, for each possible class, the following situations may happen: 1. The model predicted that the element belong to a given class, but it does not (incorrect prediction); or 2. The model predicted that the element belong to a given class, and it does (correct prediction).")
            print("If the output predicted y_pred (X-coordinate in the confusion matrix = y_pred) is the real label, then the Y-coordinate in the confusion matrix is also y_pred. For an element to have X and Y coordinates equal, it must be positioned on the principal diagonal of the matrix.")
            print("\n") #line break to highlight the next sentence
            print("So, we conclude that all the correct predictions of the model are positioned on the main or principal diagonal of the confusion matrix.")
            print("\n") # line break
            print("We also may conclude that an increase on model general accuracy is observed as an increase on the values shown in the main diagonal of the confusion matrix.")
            print("\n")
            print("Notice that this interpretation takes in account a matrix organized starting from the bottom to the top of Y axis (i.e., lower classes on the origin), and from the left to the right of the X-axis, with lower classes closer to the origin. If the order was the opposite, then the secondary diagonal that would contain the correct predictions.")
            print("If we have N possible classifications, than we have N values on axis X, and N values in axis Y. So, we have N x N = N2 (N squared) sectors (values) in the confusion matrix.\n")
            print("Confusion matrix for a binary classifier:\n")
            print("For a binary classifier, we have to possible outputs: 0 (the origin of the matrix) and 1. In the vertical axis, 1 is the topper value; in the horizontal axis, 1 is the value on the extreme right (the positions more distant from the origin).")
            print("Since N = 2, we have 2 x 2 = 4 quadrants (sectors or values).Starting from the origin, clockwise, we have 4 situations:")
            print("\n")
            print("Situation 1: X = 0 and Y = 0 - the model correctly predicted a negative output (it is a true negative prediction, TN).")
            print("Situation 2: X = 0 and Y = 1 - the model predicted a negative output for a positive class element (it is a false negative, FN).")
            print("Situation 3: X = 1 and Y = 1 - the model correctly predicted a positive class (TP).")
            print("Situation 4: X = 1 and Y = 0 - the model predicted a positive output for a negative class element (FP)\n")
            print("Each position of the confusion matrix represents the total of elements in each of the possible situations. Then, the sum of all values must be equal to the total of elements classified, and the relation between the sum of the main diagonal and the total of elements must be the accuracy.")
            print("So, use the confusion matrix to analyze the performance of the model in classifying each class, separately, and to observe the false negatives and false positives. Also, the confusion matrix will reveal if the classes are balanced, or ir a given class has much more elements than the other, what could impart the capability on differentiating the classes.")
            print("\n")
            print("For some models, the proportion of false positives may be very different from the proportion of false negatives. It is not a problem, though, and depend on the application of the classifier.")
            print("It is an important situation that would be masked by the general metrics that take in account all the predictions, without seggregating them through the classes.")
            print("\n")
            print("A classical example: suppose the classifier is used for predicting cancer. In this case, the model must have a proportion of false negatives much inferior than the proportion of false positives. That is because the risk associated to a false negative output is much higher.")
            print("A person who is incorrectly classified as having cancer will perform several more detailed exams to confirm the diagnosis, so the false positive may get detected without a great problem (in fact, the patient will probably feel good about it and keep taking care of the health). But a person incorrectly classified as not having cancer (when he has cancer) may feel comfortable, not taking care of his health and not making other exams (because he trusts the algorithm). Then, it may be too late when he founds out that was a false negative.")
            print("\n") # line break

            # AUC = Area under the curve
            print("AUC (Area under the curve) of the ROC (Receiver operating characteristic; default) or PR (Precision Recall) curves are quality measures of binary classifiers.\n")

        return self

    def plot_training_history (self, metrics_name = 'RootMeanSquaredError', x_axis_rotation = 0, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, metrics_vertical_axis_title = None, loss_vertical_axis_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):

        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt

        # metrics_name = 'RootMeanSquaredError', 'sparse_categorical_crossentropy', etc

        history = self.history
        # Set the validation metrics name.
        # to access the validation metrics, simply put a 'val_' prefix:
        val_metrics_name = 'val_' + metrics_name

        # Retrieve data from the history dictionary:
        # Access values for training sample:
        train_metrics = history.history[metrics_name]
        validation_metrics = history.history[val_metrics_name]
        
        # Try accessing data from validation sample (may not be present):
        has_validation = False
        # Maps if there are validation data: this variable is updated when values are present.
        
        try:
            train_loss = history.history['loss']
            validation_loss = history.history['val_loss']
            has_validation = True
        
        except: # simply pass
            pass
        
        # Notice that history is not exactly a dictionary: it is an object with attribute history.
        # This attribute is where the dictionary is actually stored.
        
        # Create list of epoch numbers correspondent to the metrics, starting from epoch 1:
        list_of_epochs = [i for i in range(1, (len(metrics) + 1))]
        # loops from i = 1 to i = (EPOCHS + 1) - 1 = EPOCHS
        
        if (horizontal_axis_title is None):
            horizontal_axis_title = "epoch"
        
        if (metrics_vertical_axis_title is None):
            metrics_vertical_axis_title = "metrics_value"
        
        if (loss_vertical_axis_title is None):
            loss_vertical_axis_title = "loss_value"

        # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
        # so that the bars do not completely block other views.
        OPACITY = 0.95
            
        #Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
        fig = plt.figure(figsize = (12, 8))
        ax1 = fig.add_subplot(211)
        #ax1.set_xlabel("Lags")
        ax1.set_ylabel(metrics_vertical_axis_title)
        
        # Scatter plot of time series:
        ax1.plot(list_of_epochs, train_metrics, linestyle = "-", marker = '', color = 'darkblue', alpha = OPACITY, label = "train_metrics")
        if (has_validation):
            # If present, plot validation data:
            ax1.plot(list_of_epochs, validation_metrics, linestyle = "-", marker = '', color = 'crimson', alpha = OPACITY, label = "validation_metrics")
        # Axes.plot documentation:
        # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html?msclkid=42bc92c1d13511eca8634a2c93ab89b5
        
        #ROTATE X AXIS IN XX DEGREES
        plt.xticks(rotation = x_axis_rotation)
        # XX = 0 DEGREES x_axis (Default)
        #ROTATE Y AXIS IN XX DEGREES:
        plt.yticks(rotation = y_axis_rotation)
        # XX = 0 DEGREES y_axis (Default)
        
        ax1.grid(grid)
        ax1.legend(loc = "upper right")
        
        ax2 = fig.add_subplot(212)
        ax2.plot(list_of_epochs, train_loss, linestyle = "-", marker = '', color = 'darkgreen', alpha = OPACITY, label = "train_loss")
        
        if (has_validation):
            # If present, plot validation data:
            ax2.plot(list_of_epochs, validation_loss, linestyle = "-", marker = '', color = 'fuchsia', alpha = OPACITY, label = "validation_loss")
        
        ax2.set_xlabel(horizontal_axis_title)
        ax2.set_ylabel(loss_vertical_axis_title)
        
        ax2.grid(grid)
        ax2.legend(loc = "upper right")

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
                file_name = "history_loss_and_metrics"

            #check if the user defined an image resolution. If not, set as the default 110 dpi
            # resolution.
            if (png_resolution_dpi is None):
                #set as 330 dpi
                png_resolution_dpi = 330

            #Get the new_file_path
            new_file_path = os.path.join(directory_to_save, file_name)

            #Export the file to this new path:
            # The extension will be automatically added by the savefig method:
            plt.savefig(new_file_path, dpi = png_resolution_dpi, quality = 100, format = 'png', transparent = False) 
            #quality could be set from 1 to 100, where 100 is the best quality
            #format (str, supported formats) = 'png', 'pdf', 'ps', 'eps' or 'svg'
            #transparent = True or False
            # For other parameters of .savefig method, check https://indianaiproduction.com/matplotlib-savefig/
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
    
    def retrieve_classes_used_for_training (self):
        
        import numpy as np
        import pandas as pd

        # Retrieve attributes:
        # Add the model:        
        model_object = self.model
        y_train = self.y_train
        
        # Use numpy.unique to collect the unique classes, in the
        # order they appear:
        # They are the unique values from series xgb_y_train
        # https://numpy.org/doc/stable/reference/generated/numpy.unique.html?msclkid=ce35d85ec24511ec82dc9f13c97be8ce
        list_of_classes = np.unique(y_train)
        
        # Now use the list attribute to convert the array to a list:
        list_of_classes = list(list_of_classes)
        number_of_classes = len(list_of_classes)
        print("\n") # line break
        print(f"Number of different classes in the training set = {number_of_classes}\n")
        print("List of classes:\n")
        print(list_of_classes)
        print("\n") # line break
        
        # Store this information as class attributes:
        self.list_of_classes = list_of_classes
        self.number_of_classes = number_of_classes

        return self


@dataclass
class modelling_workflow:

    # Prepare features and responses tensors.
    # Split into train and test tensors.
    # Define and train the model.
    # Evaluate models' metrics and feature importance.
    # Make predictions and visualize models.


    def separate_and_prepare_features_and_responses (df, features_columns, response_columns):

        import numpy as np
        import pandas as pd

        try:
            import tensorflow as tf
        except:
            pass
        # https://www.tensorflow.org/api_docs/python/tf/Tensor

        # features_columns: list of strings or string containing the names of columns
        # with predictive variables in the original dataframe. 
        # Example: features_columns = ['col1', 'col2']; features_columns = 'predictor';
        # features_columns = ['predictor'].
        # response_columns: list of strings or string containing the names of columns
        # with response variables in the original dataframe. 
        # Example: response_columns = ['col3', 'col4']; response_columns = 'response';
        # response_columns = ['response']

        # Set a local copy of the dataframe to manipulate:
        DATASET = df.copy(deep = True)

        # Check if features_columns and response_columns are lists:
        if (type(features_columns) != list):
            #put inside a list:
            features_columns = [features_columns]

        if (type(response_columns) != list):
            #put inside a list:
            response_columns = [response_columns]

        # Now, subset the dataframe:
        X = DATASET[features_columns].copy(deep = True)
        y = DATASET[response_columns].copy(deep = True)
        # since response_columns is a list, not a string, y is a DataFrame, not a Series.
        # So, the copy method accepts the argument deep = True

        # Try the conversion to tensors. Since the values should not be modified, we
        # will create the tensors as tf.constant, instead of tf.Variable:
        try:

            X = tf.constant(X)
            y = tf.constant(y)

            """
                Tensor with format as:
                <tf.Tensor: shape=(253, 12), dtype=float64, numpy=
                array([[ 1.        ,  1.        ,  1.        , ...,  4.18450387,
                    10.49874623,  2.09639084],
                ...,
                [12.        ,  4.        ,  6.        , ...,  4.40752786,
                    10.71241577,  3.30032431]])>
            """

        except:

            # Simply convert them to NumPy arrays. The arrays can be processed through
            # deep learning and do not add features names to the model information (what
            # raises error if we try to use the model to a set without names):
            X = np.array(X)
            y = np.array(y)

            """
                Array with format as:
                array([[ 1.        ,  1.        ,  1.        , ...,  4.42690937,
                    4.18450387, 10.49874623],
                ...,
                [12.        ,  4.        ,  6.        , ...,  4.43083069,
                    4.40752786, 10.71241577]])
            """

        print("Check the 5 first elements from the tensors or arrays obtained:\n")
        print("Features tensor or array:\n")
        print(X[:5])
        print("\n")
        print(f"Shape of the complete X tensor or array = {X.shape}\n")
        # shape attribute is common to tf.Tensor, pd.DataFrame, pd.Series, and np.array
        print("Responses tensor or array:\n")
        print(y[:5])
        print("\n")
        print(f"Shape of the complete y tensor or array = {y.shape}\n")

        # Notice that tensors and arrays are sliced in the same way as lists.
        # The slicing also modify the shape attribute from Tensors.
        # We can convert a tf.Tensor object named tensor to a np.array object by
        # simply making array = np.array(tensor) 

        # Now, since the arrays do not have a column header, let's create a mapping dictionary, correlating
        # the array position with the original column name:
        features_dict = {}
        responses_dict = {}

        for column_number, column in enumerate(features_columns):
            # The enumerate object created from a list can be decoupled into two values:
            # The index (number) - position in the list, and the element itself. example:
            # 0, 'first_column':
            # Add it to the features dictionary, with the column number as key:
            features_dict[column_number] = column

        # Repeat the process for the responses:
        for column_number, column in enumerate(response_columns):
            responses_dict[column_number] = column

        # Finally, add both dictionaries to a mapping dict:
        column_map_dict = {'features': features_dict, 'responses': responses_dict}
        print("The mapping of the arrays' positions with the columns original names was returned as 'column_map_dict'.")

        return X, y, column_map_dict


    def split_data_into_train_and_test (X, y, percent_of_data_used_for_model_training = 75, percent_of_training_data_used_for_model_validation = 0):
        
        import numpy as np
        import tensorflow as tf
        from sklearn.model_selection import train_test_split
        
        # X = tensor or array of predictive variables.
        # y = tensor or array of response variables.
        
        # percent_of_data_used_for_model_training: float from 0 to 100,
        # representing the percent of data used for training the model
        
        # If you want to use cross-validation, separate a percent of the training data for validation.
        # Declare this percent as percent_of_training_data_used_for_model_validation (float from 0 to 100).
        
        # Convert the percent to fraction.
        train_fraction = (percent_of_data_used_for_model_training / 100)
        # Calculate the test fraction:
        test_fraction = (1 - train_fraction)
        
        # Convert the percent of validation to fraction:
        validation_fraction = (percent_of_training_data_used_for_model_validation / 100)
        
        # Apply numpy method to convert tensors to numpy arrays (required by sklearn):
        X_train, X_test, y_train, y_test  = train_test_split (X.numpy(), y.numpy(), test_size = test_fraction, random_state = 0)
        #test_size: proportion: 0.25 used for test
        #test_size = 0.25 = 25% of data used for tests 
        #-> then, 0.75 = 75% of data used for training the Machine Learning model
        
        print(f"X and y successfully splitted into train: X_train, y_train ({percent_of_data_used_for_model_training}% of data); and test subsets: X_test, y_test ({100 - percent_of_data_used_for_model_training}% of data).")
        
        # Reconvert to Tensors before storage:
        X_train = tf.constant(X_train)
        X_test = tf.constant(X_test)
        y_train = tf.constant(y_train)
        y_test = tf.constant(y_test)
        
        split_dictionary = {'X_train': X_train, 'y_train': y_train, 'X_test': X_test, 'y_test': y_test}
        
        # Check if there is a fraction for validation
        if (validation_fraction > 0):
        
            # Apply numpy method to convert tensors to numpy arrays (required by sklearn):
            X_train, X_valid, y_train, y_valid = train_test_split (X_train.numpy(), y_train.numpy(), test_size = test_fraction, random_state = 0)
            # Convert to tensors:
            X_train, X_valid, y_train, y_valid = tf.constant(X_train), tf.constant(X_valid), tf.constant(y_train), tf.constant(y_valid)
            # Update the dictionary:
            split_dictionary['X_train'] = X_train
            split_dictionary['y_train'] = y_train
            split_dictionary['X_valid'] = X_valid
            split_dictionary['y_valid'] = y_valid
        
        for subset in split_dictionary.keys():
            
            print("\n")
            print(f"10 first rows from subset {subset}:\n")
            print(split_dictionary[subset][:10])
        
        return split_dictionary


    def time_series_train_test_split (X, y, percent_of_data_used_for_model_training = 75, percent_of_training_data_used_for_model_validation = 0):
        
        import numpy as np

        # X = tensor or array of predictive variables.
        # y = tensor or array of response variables.
        
        # percent_of_data_used_for_model_training: float from 0 to 100,
        # representing the percent of data used for training the model
        
        # If you want to use cross-validation, separate a percent of the training data for validation.
        # Declare this percent as percent_of_training_data_used_for_model_validation (float from 0 to 100).

        total_rows = X.shape[0]
        split_row = int(np.rint((percent_of_data_used_for_model_training/100)*total_rows))

        # Now, split the tensors
        X_train, X_test = X[:split_row], X[split_row:]
        y_train, y_test = y[:split_row], y[split_row:]

        split_dictionary = {'X_train': X_train, 'y_train': y_train, 'X_test': X_test, 'y_test': y_test}
        print(f"X and y successfully splitted into train: X_train, y_train ({percent_of_data_used_for_model_training}% of data); and test subsets: X_test, y_test ({100 - percent_of_data_used_for_model_training}% of data).")
        
        if (percent_of_training_data_used_for_model_validation > 0):
            training_rows = X_train.shape[0]
            # The first fraction is still used for training. So the percent saved for training is:
            # 100 - percent_of_data_for_validation
            split_valid_row = int(np.rint(((100 - percent_of_training_data_used_for_model_validation)/100)*training_rows))
            # Now, split the tensors
            X_train, X_valid = X_train[:split_valid_row], X_train[split_valid_row:]
            y_train, y_valid = y_train[:split_valid_row], y_train[split_valid_row:]
            # Update the dictionary:
            split_dictionary['X_train'] = X_train
            split_dictionary['y_train'] = y_train
            split_dictionary['X_valid'] = X_valid
            split_dictionary['y_valid'] = y_valid
        
        for subset in split_dictionary.keys():
            
            print("\n")
            print(f"10 first rows from subset {subset}:\n")
            print(split_dictionary[subset][:10])
        
        return split_dictionary


    def windowed_dataset_from_time_series (y, window_size = 20, batch_size = 32, shuffle_buffer_size = 100):
        
        import tensorflow as tf
        
        # y: tensor containing the time series to be converted.
        
        # Processing the data: you can feed the data for training by creating a dataset 
        # with the appropiate processing steps such as windowing, flattening, 
        # batching and shuffling.
        # window_size (integer): number of rows/ size of the time window used.
        # batch_size (integer): number of rows/ size of the batches used for training.
        # shuffle_buffer_size (integer): number of rows/ size used for shuffling the entries.

        # Create dataset from the series
        dataset = tf.data.Dataset.from_tensor_slices(y)
        
        # Slice the dataset into the appropriate windows
        # Window the data but only take those with the specified size
        dataset = dataset.window(window_size + 1, shift = 1, drop_remainder = True)
        
        # Flatten the dataset
        # Flatten the windows by putting its elements in a single batch
        dataset = dataset.flat_map(lambda window: window.batch(window_size + 1))
        
        # Shuffle it
        dataset = dataset.shuffle(shuffle_buffer_size)
        
        # Split it into the features and labels
        # Create tuples with features and labels 
        dataset = dataset.map(lambda window: (window[:-1], window[-1]))
        
        # Batch it
        dataset = dataset.batch(batch_size).prefetch(1)

        print("TensorFlow dataset successfully obtained:")
        print(dataset)

        return dataset


    def ols_linear_reg (X_train, y_train, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
        
        # check Scikit-learn documentation: 
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html?msclkid=636b4046c01b11ec973dee34641f67b0
        # This function runs the 'bar_chart' function. Certify that this function was properly loaded.
        
        import numpy as np
        import pandas as pd
        from sklearn.linear_model import LinearRegression
        
        # X_train = subset of predictive variables (dataframe).
        # y_train = subset of response variable (series).
        
        # Create an instance (object) from the class LinearRegression:
        # There is no parameter to pass to the constructor of this class:
        ols_linear_reg_model = LinearRegression()
        
        # Fit the model:
        ols_linear_reg_model = ols_linear_reg_model.fit(X_train, y_train)
        
        # Get predictions for training, testing, and validation:
        y_preds_for_train = ols_linear_reg_model.predict(X_train)
        
        if ((X_test is not None) & ((y_test is not None))):
            y_preds_for_test = ols_linear_reg_model.predict(X_test)
        
        else:
            y_preds_for_test = None
        
        if ((X_valid is not None) & ((y_valid is not None))):
            y_preds_for_validation = ols_linear_reg_model.predict(X_valid)
        
        else:
            y_preds_for_validation = None
        
        # instantiate the model checker object:
        model_check = model_checking(model_object = ols_linear_reg_model, model_type = 'regression', model_package = 'sklearn', column_map_dict = column_map_dict, X = X_train, y_train = y_train, y_preds_for_train = y_preds_for_train, y_test = y_test, y_preds_for_test = y_preds_for_test, y_valid = y_valid, y_preds_for_validation = y_preds_for_validation)
        
        # Calculate model metrics:
        model_check = model_check.model_metrics()
        # Retrieve model metrics:
        metrics_dict = model_check.metrics_dict
        
        # Get feature importance ranking:
        metrics_dict = model_check.feature_importance_ranking (model_class = 'linear', orientation = orientation, horizontal_axis_title = horizontal_axis_title, vertical_axis_title = vertical_axis_title, plot_title = plot_title, x_axis_rotation = x_axis_rotation, y_axis_rotation = y_axis_rotation, grid = grid, export_png = export_png, directory_to_save = directory_to_save, file_name = file_name, png_resolution_dpi = png_resolution_dpi)
        # Retrieve the feature importance ranking:
        feature_importance_df = model_check.feature_importance_df
        
        print("\n") #line break
        print("To predict the model output y_pred for a dataframe X, declare: y_pred = ols_linear_reg_model.predict(X)\n")
        print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
        print("X_train = np.reshape(np.array(X_train), (-1, 1))")
        # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362
        
        return ols_linear_reg_model, metrics_dict, feature_importance_df


    def ridge_linear_reg (X_train, y_train, alpha_hyperparameter = 1.0, maximum_of_allowed_iterations = 20000, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
        
        # check Scikit-learn documentation: 
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html#sklearn.linear_model.Ridge
        # This function runs the 'bar_chart' function. Certify that this function was properly loaded.
        
        import numpy as np
        import pandas as pd
        from sklearn.linear_model import Ridge
        
        # X_train = subset of predictive variables (dataframe).
        # y_train = subset of response variable (series).
        
        # hyperparameters: alpha = ALPHA_HYPERPARAMETER and MAXIMUM_OF_ALLOWED_ITERATIONS = max_iter

        # MAXIMUM_OF_ALLOWED_ITERATIONS = integer representing the maximum number of iterations
        # that the optimization algorithm can perform. Depending on data, convergence may not be
        # reached within this limit, so you may need to increase this hyperparameter.

        # alpha is the regularization strength and must be a positive float value. 
        # Regularization improves the conditioning of the problem and reduces the variance 
        # of the estimates. Larger values specify stronger regularization.
        
        # alpha = 0 is equivalent to an ordinary least square, solved by the LinearRegression 
        # object. For numerical reasons, using alpha = 0 is not advised. 
        # Given this, you should use the ols_linear_reg function instead.
        
        # Create an instance (object) from the class Ridge:
        # Pass the appropriate parameters to the class constructor:
        ridge_linear_reg_model = Ridge(alpha = alpha_hyperparameter, max_iter = maximum_of_allowed_iterations)
        
        # Fit the model:
        ridge_linear_reg_model = ridge_linear_reg_model.fit(X_train, y_train)
        
        print(f"Total of iterations to fit the model = {ridge_linear_reg_model.n_iter_}\n")
        
        if (ridge_linear_reg_model.n_iter_ == maximum_of_allowed_iterations):
            print("Warning! Total of iterations equals to the maximum allowed. It indicates that the convergence was not reached yet. Try to increase the maximum number of allowed iterations.\n")
        
        # Get predictions for training, testing, and validation:
        y_preds_for_train = ridge_linear_reg_model.predict(X_train)
        
        if ((X_test is not None) & ((y_test is not None))):
            y_preds_for_test = ridge_linear_reg_model.predict(X_test)
        
        else:
            y_preds_for_test = None
        
        if ((X_valid is not None) & ((y_valid is not None))):
            y_preds_for_validation = ridge_linear_reg_model.predict(X_valid)
        
        else:
            y_preds_for_validation = None
        
        # instantiate the model checker object:
        model_check = model_checking(model_object = ridge_linear_reg_model, model_type = 'regression', model_package = 'sklearn', column_map_dict = column_map_dict, X = X_train, y_train = y_train, y_preds_for_train = y_preds_for_train, y_test = y_test, y_preds_for_test = y_preds_for_test, y_valid = y_valid, y_preds_for_validation = y_preds_for_validation)
        
        # Calculate model metrics:
        model_check = model_check.model_metrics()
        # Retrieve model metrics:
        metrics_dict = model_check.metrics_dict
        
        # Get feature importance ranking:
        metrics_dict = model_check.feature_importance_ranking (model_class = 'linear', orientation = orientation, horizontal_axis_title = horizontal_axis_title, vertical_axis_title = vertical_axis_title, plot_title = plot_title, x_axis_rotation = x_axis_rotation, y_axis_rotation = y_axis_rotation, grid = grid, export_png = export_png, directory_to_save = directory_to_save, file_name = file_name, png_resolution_dpi = png_resolution_dpi)
        # Retrieve the feature importance ranking:
        feature_importance_df = model_check.feature_importance_df
        
        print("\n") #line break
        print("To predict the model output y_pred for a dataframe X, declare: y_pred = ridge_linear_reg_model.predict(X)\n")
        print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
        print("X_train = np.reshape(np.array(X_train), (-1, 1))")
        # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362
        
        return ridge_linear_reg_model, metrics_dict, feature_importance_df


    def lasso_linear_reg (X_train, y_train, alpha_hyperparameter = 1.0, maximum_of_allowed_iterations = 20000, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
        
        # check Scikit-learn documentation: 
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html#sklearn.linear_model.Lasso
        # This function runs the 'bar_chart' function. Certify that this function was properly loaded.
        
        import numpy as np
        import pandas as pd
        from sklearn.linear_model import Lasso
        
        # X_train = subset of predictive variables (dataframe).
        # y_train = subset of response variable (series).
        
        # hyperparameters: alpha = ALPHA_HYPERPARAMETER and MAXIMUM_OF_ALLOWED_ITERATIONS = max_iter

        # MAXIMUM_OF_ALLOWED_ITERATIONS = integer representing the maximum number of iterations
        # that the optimization algorithm can perform. Depending on data, convergence may not be
        # reached within this limit, so you may need to increase this hyperparameter.

        # alpha is the regularization strength and must be a positive float value. 
        # Regularization improves the conditioning of the problem and reduces the variance 
        # of the estimates. Larger values specify stronger regularization.
        
        # alpha = 0 is equivalent to an ordinary least square, solved by the LinearRegression 
        # object. For numerical reasons, using alpha = 0 is not advised. 
        # Given this, you should use the ols_linear_reg function instead.
        
        # Create an instance (object) from the class Lasso:
        # Pass the appropriate parameters to the class constructor:
        lasso_linear_reg_model = Lasso(alpha = alpha_hyperparameter, max_iter = maximum_of_allowed_iterations)
        # verbose = True to debug mode (show training status during training)
        
        # Fit the model:
        lasso_linear_reg_model = lasso_linear_reg_model.fit(X_train, y_train)
        
        print(f"Total of iterations to fit the model = {lasso_linear_reg_model.n_iter_}\n")
        
        if (lasso_linear_reg_model.n_iter_ == maximum_of_allowed_iterations):
            print("Warning! Total of iterations equals to the maximum allowed. It indicates that the convergence was not reached yet. Try to increase the maximum number of allowed iterations.\n")
        
        # Get predictions for training, testing, and validation:
        y_preds_for_train = lasso_linear_reg_model.predict(X_train)
        
        if ((X_test is not None) & ((y_test is not None))):
            y_preds_for_test = lasso_linear_reg_model.predict(X_test)
        
        else:
            y_preds_for_test = None
        
        if ((X_valid is not None) & ((y_valid is not None))):
            y_preds_for_validation = lasso_linear_reg_model.predict(X_valid)
        
        else:
            y_preds_for_validation = None
        
        # instantiate the model checker object:
        model_check = model_checking(model_object = lasso_linear_reg_model, model_type = 'regression', model_package = 'sklearn', column_map_dict = column_map_dict, X = X_train, y_train = y_train, y_preds_for_train = y_preds_for_train, y_test = y_test, y_preds_for_test = y_preds_for_test, y_valid = y_valid, y_preds_for_validation = y_preds_for_validation)
        
        # Calculate model metrics:
        model_check = model_check.model_metrics()
        # Retrieve model metrics:
        metrics_dict = model_check.metrics_dict
        
        # Get feature importance ranking:
        metrics_dict = model_check.feature_importance_ranking (model_class = 'linear', orientation = orientation, horizontal_axis_title = horizontal_axis_title, vertical_axis_title = vertical_axis_title, plot_title = plot_title, x_axis_rotation = x_axis_rotation, y_axis_rotation = y_axis_rotation, grid = grid, export_png = export_png, directory_to_save = directory_to_save, file_name = file_name, png_resolution_dpi = png_resolution_dpi)
        # Retrieve the feature importance ranking:
        feature_importance_df = model_check.feature_importance_df
        
        print("\n") #line break
        print("To predict the model output y_pred for a dataframe X, declare: y_pred = lasso_linear_reg_model.predict(X)\n")
        print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
        print("X_train = np.reshape(np.array(X_train), (-1, 1))")
        # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362
        
        return lasso_linear_reg_model, metrics_dict, feature_importance_df


    def elastic_net_linear_reg (X_train, y_train, alpha_hyperparameter = 1.0, l1_ratio_hyperparameter = 0.5, maximum_of_allowed_iterations = 20000, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
        
        # check Scikit-learn documentation: 
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNet.html#sklearn.linear_model.ElasticNet
        # This function runs the 'bar_chart' function. Certify that this function was properly loaded.
        
        import numpy as np
        import pandas as pd
        from sklearn.linear_model import ElasticNet
        
        # X_train = subset of predictive variables (dataframe).
        # y_train = subset of response variable (series).
        
        # hyperparameters: alpha = alpha_hyperparameter; maximum_of_allowed_iterations = max_iter;
        # and l1_ratio_hyperparameter = l1_ratio

        # MAXIMUM_OF_ALLOWED_ITERATIONS = integer representing the maximum number of iterations
        # that the optimization algorithm can perform. Depending on data, convergence may not be
        # reached within this limit, so you may need to increase this hyperparameter.

        # alpha is the regularization strength and must be a positive float value. 
        # Regularization improves the conditioning of the problem and reduces the variance 
        # of the estimates. Larger values specify stronger regularization.
        
        # l1_ratio is The ElasticNet mixing parameter (float), with 0 <= l1_ratio <= 1. 
        # For l1_ratio = 0 the penalty is an L2 penalty. For l1_ratio = 1 it is an L1 penalty. 
        # For 0 < l1_ratio < 1, the penalty is a combination of L1 and L2.
        
        # alpha = 0 and l1_ratio = 0 is equivalent to an ordinary least square, solved by 
        # the LinearRegression object. For numerical reasons, using alpha = 0 and 
        # l1_ratio = 0 is not advised. Given this, you should use the ols_linear_reg function instead.
        
        # Create an instance (object) from the class ElasticNet:
        # Pass the appropriate parameters to the class constructor:
        elastic_net_linear_reg_model = ElasticNet(alpha = alpha_hyperparameter, l1_ratio = l1_ratio_hyperparameter, max_iter = maximum_of_allowed_iterations)
        # verbose = True to debug mode (show training status during training)
        
        # Fit the model:
        elastic_net_linear_reg_model = elastic_net_linear_reg_model.fit(X_train, y_train)
        
        print(f"Total of iterations to fit the model = {elastic_net_linear_reg_model.n_iter_}\n")
        
        if (elastic_net_linear_reg_model.n_iter_ == maximum_of_allowed_iterations):
            print("Warning! Total of iterations equals to the maximum allowed. It indicates that the convergence was not reached yet. Try to increase the maximum number of allowed iterations.\n")
        
        # Get predictions for training, testing, and validation:
        y_preds_for_train = elastic_net_linear_reg_model.predict(X_train)
        
        if ((X_test is not None) & ((y_test is not None))):
            y_preds_for_test = elastic_net_linear_reg_model.predict(X_test)
        
        else:
            y_preds_for_test = None
        
        if ((X_valid is not None) & ((y_valid is not None))):
            y_preds_for_validation = elastic_net_linear_reg_model.predict(X_valid)
        
        else:
            y_preds_for_validation = None
        
        # instantiate the model checker object:
        model_check = model_checking(model_object = elastic_net_linear_reg_model, model_type = 'regression', model_package = 'sklearn', column_map_dict = column_map_dict, X = X_train, y_train = y_train, y_preds_for_train = y_preds_for_train, y_test = y_test, y_preds_for_test = y_preds_for_test, y_valid = y_valid, y_preds_for_validation = y_preds_for_validation)
        
        # Calculate model metrics:
        model_check = model_check.model_metrics()
        # Retrieve model metrics:
        metrics_dict = model_check.metrics_dict
        
        # Get feature importance ranking:
        metrics_dict = model_check.feature_importance_ranking (model_class = 'linear', orientation = orientation, horizontal_axis_title = horizontal_axis_title, vertical_axis_title = vertical_axis_title, plot_title = plot_title, x_axis_rotation = x_axis_rotation, y_axis_rotation = y_axis_rotation, grid = grid, export_png = export_png, directory_to_save = directory_to_save, file_name = file_name, png_resolution_dpi = png_resolution_dpi)
        # Retrieve the feature importance ranking:
        feature_importance_df = model_check.feature_importance_df
        
        print("\n") #line break
        print("To predict the model output y_pred for a dataframe X, declare: y_pred = elastic_net_linear_reg_model.predict(X)\n")
        print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
        print("X_train = np.reshape(np.array(X_train), (-1, 1))")
        # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362
        
        return elastic_net_linear_reg_model, metrics_dict, feature_importance_df


    def logistic_reg (X_train, y_train, maximum_of_allowed_iterations = 20000, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
        
        # check Scikit-learn documentation: 
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html?msclkid=6bede8a8c1a011ecad332ec5eb711355
        # This function runs the 'bar_chart' function. Certify that this function was properly loaded.
        
        import numpy as np
        import pandas as pd
        from sklearn.linear_model import LogisticRegression
        
        # X_train = subset of predictive variables (dataframe).
        # y_train = subset of response variable (series).

        # MAXIMUM_OF_ALLOWED_ITERATIONS = integer representing the maximum number of iterations
        # that the optimization algorithm can perform. Depending on data, convergence may not be
        # reached within this limit, so you may need to increase this hyperparameter.
        
        print("Attention: logistic regression is a binary classifier. It results in probabilities, instead of on scalar (real numbers) like other regression algorithms from linear models class.\n")
        
        # Pass the appropriate parameters to the class constructor:
        logistic_reg_model = LogisticRegression(max_iter = maximum_of_allowed_iterations)
        # verbose = 1 to debug mode is not available for 'saga' solver
        
        # Fit the model:
        # Sklearn logistic regression requires a 1-dimensional vector for training. So, let's
        # reshape the y_train tensor accordingly:
        reshaped_y_train = y_train.numpy().reshape(1, -1)
        # This array has format([[val1, val2, ...]]) - i.e., it has two dimensions. Let's pick
        # only the first array:
        reshaped_y_train = reshaped_y_train[0]
        
        logistic_reg_model = logistic_reg_model.fit(X_train, reshaped_y_train)
        print(f"Total of iterations to fit the model = {logistic_reg_model.n_iter_}\n")
        
        if (logistic_reg_model.n_iter_ == maximum_of_allowed_iterations):
            print("Warning! Total of iterations equals to the maximum allowed. It indicates that the convergence was not reached yet. Try to increase the maximum number of allowed iterations.\n")
        
        # Get predictions for training, testing, and validation:
        y_preds_for_train = logistic_reg_model.predict(X_train)
        
        if ((X_test is not None) & ((y_test is not None))):
            y_preds_for_test = logistic_reg_model.predict(X_test)
        
        else:
            y_preds_for_test = None
        
        if ((X_valid is not None) & ((y_valid is not None))):
            y_preds_for_validation = logistic_reg_model.predict(X_valid)
            
        else:
            y_preds_for_validation = None
        
        # instantiate the model checker object:
        model_check = model_checking(model_object = logistic_reg_model, model_type = 'classification', model_package = 'sklearn', column_map_dict = column_map_dict, X = X_train, y_train = y_train, y_preds_for_train = y_preds_for_train, y_test = y_test, y_preds_for_test = y_preds_for_test, y_valid = y_valid, y_preds_for_validation = y_preds_for_validation)
        
        # Check total of classes:
        model_check = model_check.retrieve_classes_used_for_training()
        
        # Calculate model metrics:
        model_check = model_check.model_metrics()
        # Retrieve model metrics:
        metrics_dict = model_check.metrics_dict
        
        # Get feature importance ranking:
        metrics_dict = model_check.feature_importance_ranking (model_class = 'linear', orientation = orientation, horizontal_axis_title = horizontal_axis_title, vertical_axis_title = vertical_axis_title, plot_title = plot_title, x_axis_rotation = x_axis_rotation, y_axis_rotation = y_axis_rotation, grid = grid, export_png = export_png, directory_to_save = directory_to_save, file_name = file_name, png_resolution_dpi = png_resolution_dpi)
        # Retrieve the feature importance ranking:
        feature_importance_df = model_check.feature_importance_df
        
        print("\n") #line break
        print("To predict the model output y_pred for a dataframe X, declare: y_pred = logistic_reg_model.predict(X)\n")
        print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
        print("X_train = np.reshape(np.array(X_train), (-1, 1))")
        # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362
        
        print("To predict the probabilities associated to each class for the set X_train, use the .predict_proba(X) method:")
        print("y_pred_probabilities = logistic_reg_model.predict_proba(X_train)")
        
        return logistic_reg_model, metrics_dict, feature_importance_df

