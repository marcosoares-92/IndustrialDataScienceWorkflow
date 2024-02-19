""" FUNCTIONS FROM INDUSTRIAL DATA SCIENCE WORKFLOW (IDSW) PACKAGE
Modelling and Machine Learning

Prepare features and responses tensors.
Split into train and test tensors.
Define and train the model.
Evaluate models' metrics and feature importance.
Make predictions and visualize models.


Marco Cesar Prado Soares, Data Scientist Specialist @ Bayer Crop Science LATAM
marcosoares.feq@gmail.com
marco.soares@bayer.com"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf

from idsw import (InvalidInputsError, ControlVars)


class ModelChecking:
    """
    Class for checking models' metrics and performance.
    
    def __init__(self, model_object = None, model_type = 'regression', 
        model_package = 'tensorflow', column_map_dict = None, training_history_object = None, 
        X = None, y_train = None, y_preds_for_train = None, y_test = None, y_preds_for_test = None, 
        y_valid = None, y_preds_for_validation = None):
    """

    # Initialize instance attributes.
    # define the Class constructor, i.e., how are its objects:
    def __init__ (self, model_object = None, model_type = 'regression', model_package = 'tensorflow', column_map_dict = None, training_history_object = None, X = None, y_train = None, y_preds_for_train = None, y_test = None, y_preds_for_test = None, y_valid = None, y_preds_for_validation = None):

        # Add the model:        
        self.model = model_object
        # It can be None: user can firstly call the object to retrieve the total classes, and
        # then call it again with the model adjusted for that amount of classes.
        
        # model_type = 'regression' or 'classification'
        self.model_type = model_type
        
        if (model_type == 'regression'):
            self.metrics_name = 'mean_absolute_error'
        
        else:
            self.metrics_name = 'acc'
        
        # Add model package: 'tensorflow' (and keras), 'sklearn', or 'xgboost':
        self.package = model_package

        # Add the columns names:
        self.column_map_dict = column_map_dict
        # Add the training history to the class:
        self.history = training_history_object

        # Add the y series for computing general metrics:
        # Guarantee that they are tensorflow tensors
        if (y_train is not None):
            if (len(y_train) > 0):
                self.y_train = tf.constant(y_train)
            else:
                self.y_train = None
        else:
            self.y_train = None
        if (y_preds_for_train is not None):
            if (len(y_preds_for_train) > 0):
                self.y_preds_for_train = tf.constant(y_preds_for_train)
            else:
                self.y_train = None
        else:
            self.y_train = None
        if (y_test is not None):
            if (len(y_test) > 0):
                self.y_test = tf.constant(y_test)
            else:
                self.y_test = None
        else:
            self.y_test = None
        if (y_preds_for_test is not None):
            if (len(y_preds_for_test) > 0):
                self.y_preds_for_test = tf.constant(y_preds_for_test)
            else:
                self.y_preds_for_test = None
        else:
            self.y_preds_for_test = None
        if (y_valid is not None):
            if (len(y_valid) > 0):
                self.y_valid = tf.constant(y_valid)
            else:
                self.y_valid = None
        else:
            self.y_valid = None
        if (y_preds_for_validation is not None):
            if (len(y_preds_for_validation) > 0):
                self.y_preds_for_validation = tf.constant(y_preds_for_validation)
            else:
                self.y_preds_for_validation = None
        else:
            self.y_preds_for_validation = None

        # X can be X_train, X_test, or X_valid. 
        # We only want to obtain the total number of predictors. X.shape is like:
        # TensorShape([253, 11]). Second index [1] is the number of predictors:
        if (X is not None):
            if (len(X) > 0):
                # make sure it is a tensor:
                X = tf.constant(X)
                total_predictors = X.shape[1]
                self.total_predictors = total_predictors
            else:
                X = None

        # to check the class attributes, use the __dict__ method or the vars function. Examples:
        ## object.__dict__ will show all attributes from object
        ## vars(object) shows the same.
                
    # Define the class methods.
    # All methods must take an object from the class (self) as one of the parameters
    

    def model_metrics (self, show_confusion_matrix_values = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
        # https://www.tensorflow.org/api_docs/python/tf/keras/metrics?authuser=1
        from sklearn.metrics import classification_report, confusion_matrix, r2_score
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html#sklearn.metrics.r2_score
        from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html#sklearn.metrics.mean_squared_error
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_error.html#sklearn.metrics.mean_absolute_error
        from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html#sklearn.metrics.roc_auc_score
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html#sklearn.metrics.accuracy_score
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html#sklearn.metrics.precision_score
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html#sklearn.metrics.recall_score
        

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
                
                y_true = np.array(y_true)
                y_pred = np.array(y_pred)
                
                try:
                
                    # Regression metrics:
                    if (model_type == 'regression'):
                        if ControlVars.show_results:
                            print(f"Metrics for {key}:\n")
                        mse = mean_squared_error(y_true, y_pred)

                        # Print in scientific notation:
                        if ControlVars.show_results:
                            try:
                                print(f"Mean squared error (MSE) = {mse:e}")
                            except:
                                print(f"Mean squared error (MSE) = {mse}")
                        # Add to calculated metrics:
                        calculated_metrics['mse'] = mse

                        rmse = mse**(1/2)

                        if ControlVars.show_results:
                            try:
                                print(f"Root mean squared error (RMSE) = {rmse:e}")
                            except:
                                print(f"Root mean squared error (RMSE) = {rmse}")
                        # Add to calculated metrics:
                        calculated_metrics['rmse'] = rmse

                        mae = mean_absolute_error(y_true, y_pred)

                        # Print in scientific notation:
                        if ControlVars.show_results:
                            try:
                                print(f"Mean absolute error (MAE) = {mae:e}")
                            except:
                                print(f"Mean absolute error (MAE) = {mae}")
                        # Add to calculated metrics:
                        calculated_metrics['mae'] = mae

                        # Mean absolute percentage error: non-stable Sklearn function
                        # y_true and y_pred must be already numpy arrays:
                        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

                        # Print in scientific notation:
                        if ControlVars.show_results:
                            try:
                                print(f"Mean absolute percentage error (MAPE) = {mape:e}")
                            except:
                                print(f"Mean absolute percentage error (MAPE) = {mape}")
                        # Add to calculated metrics:
                        calculated_metrics['mape'] = mape

                        r2 = r2_score(y_true, y_pred)
                        
                        if ControlVars.show_results:
                            try:
                                print(f"Coefficient of linear correlation R² = {r2:e}")
                            except:
                                print(f"Coefficient of linear correlation R² = {r2}")
                        # Add to calculated metrics:
                        calculated_metrics['r_squared'] = r2

                        # Manually correct R²:
                        # n_size_train = number of sample size
                        # k_model = number of independent variables of the defined model
                        k_model = self.total_predictors
                        #numer of rows
                        n_size = len(y_true)
                        r2_adj = 1 - (1 - r2)*(n_size - 1)/(n_size - k_model - 1)

                        if ControlVars.show_results:
                            try:
                                print(f"Adjusted coefficient of correlation R²-adj = {r2_adj:e}")
                            except:
                                print(f"Adjusted coefficient of correlation R²-adj = {r2_adj}")

                        # Add to calculated metrics:
                        calculated_metrics['r_squared_adj'] = r2_adj

                        explained_var = explained_variance_score(y_true, y_pred)
                        # Print in scientific notation:
                        if ControlVars.show_results:
                            try:
                                print(f"Explained variance = {explained_var:e}")

                            except:
                                print(f"Explained variance = {explained_var}")

                        # Explained variance is similar to the R² score, goes from 0 to 1, with the notable 
                        # difference that it does not account for systematic offsets in the prediction.
                        calculated_metrics['explained_variance'] = explained_var

                        print("\n")
                        # Now, add the metrics to the metrics_dict:
                        metrics_dict[key] = calculated_metrics

                    else:

                        # y_true and y_pred should be converted to integers to represent the classes
                        # so that there will be no compatibility issues resulting in erros when calculating
                        # the metrics.
                        y_true = y_true.astype('int64')
                        y_pred = y_pred.astype('int64')

                        if ControlVars.show_results:
                            print(f"Metrics for {key}:\n")

                        auc = roc_auc_score(y_true, y_pred)

                        if ControlVars.show_results:
                            try:
                                print(f"AUC = {auc:e}")
                            except:
                                print(f"AUC = {auc}")
                        # Add to calculated metrics:
                        calculated_metrics['auc'] = auc

                        acc = accuracy_score(y_true, y_pred)

                        if ControlVars.show_results:
                            try:
                                print(f"Accuracy = {acc:e}")
                            except:
                                print(f"Accuracy = {acc}")
                        # Add to calculated metrics:
                        calculated_metrics['accuracy'] = acc

                        precision = precision_score(y_true, y_pred)

                        if ControlVars.show_results:
                            try:
                                print(f"Precision = {precision:e}")
                            except:
                                print(f"Precision = {precision}")
                        # Add to calculated metrics:
                        calculated_metrics['precision'] = precision

                        recall = recall_score(y_true, y_pred)

                        if ControlVars.show_results:
                            try:
                                print(f"Recall = {recall:e}")
                            except:
                                print(f"Recall = {recall}")
                        # Add to calculated metrics:
                        calculated_metrics['recall'] = recall

                        # The method update_state returns None, so it must be called without and equality

                        # Get the classification report:
                        if ControlVars.show_results:
                            print("\n")
                            print("Classification Report:\n")
                        # Convert tensors to NumPy arrays
                        report = classification_report (y_true, y_pred)
                        if ControlVars.show_results:
                            print(report)
                        # Add to calculated metrics:
                        calculated_metrics['classification_report'] = report
                        print("\n")

                        # Get the confusion matrix:
                        # Convert tensors to NumPy arrays
                        matrix = confusion_matrix (y_true, y_pred)
                        # Add to calculated metrics:
                        calculated_metrics['confusion_matrix'] = report
                        if ControlVars.show_results:
                            print("Confusion matrix:\n")

                        if ControlVars.show_plots:
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
                                new_file_path = new_file_path + ".png"
                                # supported formats = 'png', 'pdf', 'ps', 'eps' or 'svg'
                                #Export the file to this new path:
                                plt.savefig(new_file_path, dpi = png_resolution_dpi, transparent = False) 
                                # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html
                                print (f"Figure exported as \'{new_file_path}\'. Any previous file in this root path was overwritten.")
                            
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
                
                except:
                    print(f"Unable to retrieve metrics for {key}:\n")
                    metrics_dict[key] = {'metrics': f'No metrics retrieved for {key}'}
          
        # Now that we finished calculating metrics for all tensors, save the
        # dictionary as a class variable (attribute) and return the object:
        self.metrics_dict = metrics_dict
        
        return self


    def feature_importance_ranking (self, model_class = 'linear', orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):

        # model_class = 'linear' or model_class = 'tree'
        # Retrieve the model:
        model = self.model
        # Return the mapping dictionary:
        column_map_dict = self.column_map_dict
        model_type = self.model_type

        if (model_class == 'linear'):

            # Get the list of coefficients
            reg_coefficients = model.coef_
              
            try: 
                trial_access = reg_coefficients[1]
                # If the trial succeeded, reg_coefficients is in the correct format [coef1, coef2, ...]
                
                # reg_coefficients[0] is a scalar, not an array.
                # Convert the numpy array:
                reg_coefficients = np.array(reg_coefficients)
                abs_reg_coefficients = abs(reg_coefficients)
                
            except: 
                # The trial fails when reg_coefficients is an array containing a single array like 
                # [[coef1, coef2, ...]]
                # So, the index 0 stores the array of interest. 
                # Since coefficients may be negative, pick the absolute values from the array in index 0
                # (NumPy arrays accept vectorial operations, lists do not):
                reg_coefficients = np.array(reg_coefficients[0])
                abs_reg_coefficients = abs(reg_coefficients)
                # Already numpy arrays
            
            if (column_map_dict is not None):
                # Retrieve the values (columns' names):
                # Set as list
                columns_list = list(column_map_dict['features'].values())
            
            else:
                # Retrieve the values (columns' names):
                columns_list = [i for i in range(0, len(reg_coefficients))]
            
            # Get the intercept coefficient:
            if ControlVars.show_results:
                print(f"Calculated model intercept = {model.intercept_}\n")
            
            try:
                # Create the regression dictionary:
                reg_dict = {'predictive_features': columns_list,
                          'regression_coefficients': reg_coefficients,
                           'abs_reg_coefficients': abs_reg_coefficients}

                # Convert it to a Pandas dataframe:
                feature_importance_df = pd.DataFrame(data = reg_dict)

                # Now sort the dataframe in descending order of coefficient, and ascending order of
                # feature (when sorting by multiple columns, we pass a list of columns to by and a 
                # list of booleans to ascending, instead of passing a simple string to by and a boolean
                # to ascending. The element on a given index from the list by corresponds to the boolean
                # with the same index in ascending):
                feature_importance_df = feature_importance_df.sort_values(by = ['abs_reg_coefficients', 'regression_coefficients', 'predictive_features'], ascending = [False, False, True])

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
            
            # Get the list of feature importances. Apply the list method to convert the
            # array from .feature_importances_ to a list:
            feature_importances = model.feature_importances_
                 
            try: 
                trial_access = feature_importances[1]
                # If the trial succeeded, feature_importances is in the correct format 
                # [coef1, coef2, ...]
                # feature_importances[0] is a scalar, not an array.
                feature_importances = np.array(feature_importances)
                abs_feature_importances = abs(feature_importances)
                             
            except: 
                # The trial fails when reg_coefficients is an array containing a single array like 
                # [[coef1, coef2, ...]]
                # So, the index 0 stores the array of interest. 
                # Since coefficients may be negative, pick the absolute values from the array in index 0
                # (NumPy arrays accept vectorial operations, lists do not):
                feature_importances = np.array(feature_importances[0])
                abs_feature_importances = abs(feature_importances)
                # feature_importances and abs_feature_importances are already numpy arrays
            
            if (column_map_dict is not None):
                # Retrieve the values (columns' names):
                columns_list = list(column_map_dict['features'].values())
                
            else:
                # Retrieve the values (columns' names):
                columns_list = [i for i in range(0, len(feature_importances))]
            
            try:
                # Create the model dictionary:
                model_dict = {'predictive_features': columns_list,
                            'feature_importances': feature_importances,
                            'abs_feature_importances': abs_feature_importances}

                # Convert it to a Pandas dataframe:
                feature_importance_df = pd.DataFrame(data = model_dict)
            
                # Now sort the dataframe in descending order of importance, and ascending order of
                # feature (when sorting by multiple columns, we pass a list of columns to by and a 
                # list of booleans to ascending, instead of passing a simple string to by and a boolean
                # to ascending. The element on a given index from the list by corresponds to the boolean
                # with the same index in ascending):
                feature_importance_df = feature_importance_df.sort_values(by = ['abs_feature_importances', 'feature_importances', 'predictive_features'], ascending = [False, False, True])

                # Now that the dataframe is sorted in descending order, it represents the feature
                # importance ranking.

                # Restart the indices:
                feature_importance_df = feature_importance_df.reset_index(drop = True)
            
            except:
                print("Model feature importance ranking generated a total of values different from number of predictors.")
                print(f"Model's feature_importances = {feature_importances}\n")

        try:  
            
            if ControlVars.show_results:
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
                importances = feature_importance_df['abs_reg_coefficients']

            elif (model_class == 'tree'):
                importances = feature_importance_df['abs_feature_importances']

            data_label = "feature_importance_ranking"

            # Normalize the importances by dividing all of them by the maximum:
            max_importance = max(importances)
            importances = importances/max_importance

            # Now, limit to 10 values to plot:
            importances = importances[:10]
            features = features[:10]

            if ControlVars.show_plots:
                # Now, plot the bar chart
                print("\n")
                print("Feature relative importance bar chart:\n")
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
                    new_file_path = new_file_path + ".png"
                    # supported formats = 'png', 'pdf', 'ps', 'eps' or 'svg'
                    #Export the file to this new path:
                    plt.savefig(new_file_path, dpi = png_resolution_dpi, transparent = False) 
                    # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html
                    print (f"Figure exported as \'{new_file_path}\'. Any previous file in this root path was overwritten.")
                
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
            
            if ControlVars.show_results:
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


    def plot_training_history (self, metrics_name = 'mean_absolute_error', x_axis_rotation = 0, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, metrics_vertical_axis_title = None, loss_vertical_axis_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):

        if ControlVars.show_plots:
            # metrics_name = 'mse', 'sparse_categorical_crossentropy', etc

            history = self.history
            # Set the validation metrics name.
            # to access the validation metrics, simply put a 'val_' prefix:
            val_metrics_name = 'val_' + metrics_name
            
            has_metrics = False
            has_loss = False
            
            # Notice that history is not exactly a dictionary: it is an object with attribute history.
            # This attribute is where the dictionary is actually stored.
            
            # Access the list of epochs, stored as the epoch attribute from the history object
            list_of_epochs = history.epoch
            # epochs start from zero

            # Check if the metrics data are present
            try:
                # Retrieve data from the history dictionary:
                # Access values for training sample:
                train_metrics = history.history[metrics_name]
                has_metrics = True
            except:
                pass
            
            # Check if the loss data are present
            try:
                # Retrieve data from the history dictionary:
                # Access values for training sample:
                train_loss = history.history['loss']
                has_loss = True
            except:
                pass
            
            # Try accessing data from validation sample (may not be present):
            has_validation = False
            # Maps if there are validation data: this variable is updated when values are present.
            
            try:
                validation_metrics = history.history[val_metrics_name]
                validation_loss = history.history['val_loss']
                has_validation = True
            except: # simply pass
                pass
            
            
            if (horizontal_axis_title is None):
                horizontal_axis_title = "epoch"
            
            if (metrics_vertical_axis_title is None):
                metrics_vertical_axis_title = "metrics_value"
            
            if (loss_vertical_axis_title is None):
                loss_vertical_axis_title = "loss_value"
            
            try:
                # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
                # so that the bars do not completely block other views.
                OPACITY = 0.95

                #Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
                fig = plt.figure(figsize = (12, 8))

                if (has_metrics & has_loss):
                    ax1 = fig.add_subplot(211)
                elif (has_metrics):
                    ax1 = fig.add_subplot()
                elif (has_loss):
                    ax2 = fig.add_subplot()

                if (has_metrics):
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

                if (has_metrics & has_loss):
                    # The case where both are present still do not have the ax2 configured
                    ax2 = fig.add_subplot(212)
                
                if (has_loss):
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
            
            except:
                print("Unable to plot training history.\n")
                
    
    def plot_history_multiresponses (self, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, metrics_vertical_axis_title = None, loss_vertical_axis_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):

        if ControlVars.show_plots:
            # metrics_name = 'mse', 'sparse_categorical_crossentropy', etc

            history = self.history
            
            """
            history object has a format like (2 responses, 1 epoch, metrics = 'mse'), when we apply the
            .__dict__ method or call the vars functions:

            'history': {'loss': [2.977898597717285],
            'response1_loss': [0.052497703582048416],
            'response2_loss': [2.457101345062256],
            'response1_mse': [0.052497703582048416],
            'response2_mse': [2.457101345062256],
            'val_loss': [2.007075071334839],
            'val_response1_loss': [0.02299179881811142],
            'val_response2_loss': [1.8660322427749634],
            'val_response1_mse': [0.02299179881811142],
            'val_response2_mse': [1.8660322427749634],
            'params': {'verbose': 1, 'epochs': 1, 'steps': 1},
            'epoch': [0]}

            Here, the history attribute stores a dictionary with the training history, whereas the epoch
            attribute stores the list of epochs, starting from zero.
            - Keys 'loss' and 'val_loss' store the general losses for the whole network.
            - Other keys store the metrics for the responses.

            """
            # Access the list of epochs, stored as the epoch attribute from the history object
            list_of_epochs = history.epoch
            # epochs start from zero
            
            # access history attribute to retrieve the series of metrics.
            history_dict = history.history
            
            metrics_dict = {}
            #Get the global one:
            nested_dict = {'loss': history_dict['loss']}
            
            
            # Try accessing validation information
            has_validation = False
            # Maps if there are validation data: this variable is updated when values are present.
            
            try:
                nested_dict['val_loss'] = history_dict['val_loss']
                has_validation = True
            
            except: # simply pass
                pass
            
            nested_dict['response'] = 'global'
            
            metrics_dict['global'] = nested_dict
            
            # Let's find out the metrics name
            for key in history_dict.keys():
                
                if ((key != 'loss') & (key != 'val_loss')):
                    # These are the globals, which were already saved
                    
                    # Split the string in the underscores: 'response2_loss'
                    # will generate a list of two elements ['response2', 'loss']. We pick the last element
                    # with index -1.
                    # Attention: guarantee that the key was read as a string, not as a number
                    list_of_substrings = str(key).split("_")
                    first_portion = list_of_substrings[0]
                    last_portion = list_of_substrings[-1]

                    # Get the total of characters of the last portion
                    total_characters = len(last_portion)
                    # pick the string eliminating its last portion
                    response = key[:(-1*(total_characters + 1))]
                    # if we had a string like 'response1_loss', now response = 'response1_' if we did
                    # not sum another character. By summing 1, we eliminate the last underscore
                    
                    if (first_portion == 'val'):
                        # In this case, the response variable by now stores val_response1, i.e., the first
                        # we should eliminate characters from positions 0 to 3, starting the string from
                        # character 4:
                        response = response[4:]
                    
                    # try accessing the nested dict:
                    try:
                        nested_dict = metrics_dict[response]

                    except:
                        # There is no nested_dict yet, so create one:
                        nested_dict = {'response': response}
                    
                    if (last_portion != 'loss'):
                        
                        if (first_portion != 'val'):
                            # Insert the metrics name only once:
                            nested_dict['metrics'] = last_portion
                            nested_dict[last_portion] = history_dict[key]
                        
                        else:
                            nested_dict[("val_" + last_portion)] = history_dict[key]
                    
                    else:
                        if (first_portion != 'val'):
                            # Insert the metrics name only once:
                            nested_dict['loss'] = history_dict[key]
                        
                        else:
                            nested_dict["val_loss"] = history_dict[key]
                    
                    #Update nested dictionary
                    metrics_dict[response] = nested_dict
            
            # metrics_dict keys: responses without the 'val_' and '_loss' and '_' + metrics. Stores
            # the nested dictionary.
            # nested_dict keys: 'response': name of the response variable;
            # 'metrics': name of the metrics; metrics (key with name that varies):
            # series of the metrics registered during training; "val_" + metrics (key with name that 
            # varies): series of the metrics registered during training for validation data; 'loss':
            # series of losses obtained during training; 'val_loss': losses for validation data.
            
            # Loop through the responses and nested dictionaries in the metrics_dict:
            for response, nested_dict in metrics_dict.items():
                
                # For the general case, only the loss will be available
                has_metrics = False
                has_loss = False

                try:
                    metrics_name = nested_dict['metrics']

                    # Set the validation metrics name.
                    # to access the validation metrics, simply put a 'val_' prefix:
                    val_metrics_name = 'val_' + metrics_name
                
                except:
                    pass
                
                try:
                    train_loss = nested_dict['loss']
                    
                    has_loss = True

                    if (has_validation):
                        validation_loss = nested_dict['val_loss']
                except:
                    pass
                
                try:
                    train_metrics = nested_dict[metrics_name]

                    has_metrics = True
                    
                    if (has_validation):
                        validation_metrics = nested_dict[val_metrics_name]
                except:
                    pass
                    
            
                if (horizontal_axis_title is None):
                    horizontal_axis_title = "epoch"

                if (metrics_vertical_axis_title is None):
                    metrics_vertical_axis_title = "metrics_value"

                if (loss_vertical_axis_title is None):
                    loss_vertical_axis_title = "loss_value"
                
                try:
                    # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
                    # so that the bars do not completely block other views.
                    OPACITY = 0.95

                    #Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
                    fig = plt.figure(figsize = (12, 8))
                    
                    if (has_metrics & has_loss):
                        ax1 = fig.add_subplot(211)
                    elif (has_metrics):
                        ax1 = fig.add_subplot()
                    elif (has_loss):
                        ax2 = fig.add_subplot()

                    if (has_metrics):
                        #ax1.set_xlabel("Lags")
                        ax1.set_ylabel(metrics_vertical_axis_title)

                        # Scatter plot of time series:
                        ax1.plot(list_of_epochs, train_metrics, linestyle = "-", marker = '', color = 'darkblue', alpha = OPACITY, label = ("train_metrics_" + response[:10]))
                        if (has_validation):
                            # If present, plot validation data:
                            ax1.plot(list_of_epochs, validation_metrics, linestyle = "-", marker = '', color = 'crimson', alpha = OPACITY, label = ("validation_metrics_" + response[:10]))
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
                    
                    if (has_metrics & has_loss):
                        # The case where both are present still do not have the ax2 configured
                        ax2 = fig.add_subplot(212)

                    if (has_loss):
                        ax2.plot(list_of_epochs, train_loss, linestyle = "-", marker = '', color = 'darkgreen', alpha = OPACITY, label = ("train_loss_" + response[:10]))

                        if (has_validation):
                            # If present, plot validation data:
                            ax2.plot(list_of_epochs, validation_loss, linestyle = "-", marker = '', color = 'fuchsia', alpha = OPACITY, label = ("validation_loss_" + response[:10]))

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
                            file_name = ("history_" + response[:10])

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
                    print("\n")
            
                except:
                    print(f"Unable to plot training history for {response}.\n")
            
    
    def model_metrics_multiresponses (self, output_dictionary, show_confusion_matrix_values = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
        # https://www.tensorflow.org/api_docs/python/tf/keras/metrics?authuser=1
        from sklearn.metrics import classification_report, confusion_matrix, r2_score
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html#sklearn.metrics.r2_score
        from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html#sklearn.metrics.mean_squared_error
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_error.html#sklearn.metrics.mean_absolute_error
        from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html#sklearn.metrics.roc_auc_score
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html#sklearn.metrics.accuracy_score
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html#sklearn.metrics.precision_score
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html#sklearn.metrics.recall_score
        

        # Retrieve type of problem:
        model_type = self.model_type
        
        # output_dictionary structure:
        # {'response_variable': {
        # 'type': 'regression', 'number_of_classes':}}

        list_of_responses = list((output_dictionary).keys())
        # Total of responses
        total_of_responses = len(list_of_responses)

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
            y_true_tensor =  nested_dict['actual']
            y_pred_tensor = nested_dict['predictions']
            
            y_true_array = np.array(y_true_tensor)
            
            # Reshape y_pred so that it is in the same format as the y_true tensor
            # The predictions may come in a different shape, depending on the algorithm that
            # generates them.
            
            y_pred_array = np.array(y_pred_tensor)
            
            # Total of entries in the dataset:
            # Get the total of values for the first response, by isolating the index 0 of 2nd dimension
            try:
                total_data = len(y_pred_array[:, 0])
            except:
                total_data = 0
            
            # If the prediction was generated from a 3D-tensor, it may have 4 dimensions, with the last dimension
            # equals to 1. So, let's check this possibility (y_pred_array.shape is a tuple):
            try:
                if ((len(y_pred_array.shape) == 4) & (y_pred_array.shape[3] == 1)):
                    # Pick only first index from last dimension:
                    y_pred_array = y_pred_array[:,:,:,0]
            except:
                pass
            
            try:
                # Either if it was processed through previous if-statement or if it came from a 2D-tensor, 
                # it may have a third dimension equals to 1:
                if ((len(y_pred_array.shape) == 3) & (y_pred_array.shape[2] == 1)):
                    # Pick only first index from last dimension:
                    y_pred_array = y_pred_array[:,:,0]
            except:
                pass
            
            try:
                y_pred_array = y_pred_array.reshape(total_data, total_of_responses)
                dim = 1
                # the variable dim maps the position of the shape tuple correspondent to the total of responses
            except:
                # let's assume that the first dimension (index 0) is the total_of_responses
                dim = 0
                
                # check the dimension correspondent to the total of responses, and correct it if it
                # is not zero:
                for tuple_index, tuple_value in enumerate(y_pred_array.shape):
                    if(tuple_value == total_of_responses):
                        dim = tuple_index
                
            # Check if there is no None value stored:
            if ((y_true_array is not None) & (y_pred_array is not None)):

                calculated_metrics = {}
                if ControlVars.show_results:
                    print(f"Metrics for {key}:\n")
                
                nested_metrics = {}
                
                for index, response in enumerate(list_of_responses):
                    
                    if (total_data > 0):
                    
                        # enumerate will get tuples like (0, response1), (1, response2), etc
                        if ControlVars.show_results:
                            print(f"Evaluation of metrics for response variable '{response}':\n")

                        type_of_problem = output_dictionary[response]['type']
                        # select only the arrays in position 'index' of the tensors y_true_tensor
                        # and y_pred_tensor:

                        try:
                            y_true = y_true_array[:, index]

                            if (dim == 1):
                                y_pred = y_pred_array[:, index]
                        except:
                            pass

                        if (dim == 0):
                            y_pred = y_pred_array[index]

                        # If there is still an extra dimension related to the shift, pick only first value from each
                        # array:
                        try:
                            assert (y_pred.shape == y_true.shape)
                        except:
                            try:
                                y_pred = y_pred[:, 0]
                            except:
                                pass

                        try:
                            # Regression metrics:
                            if (model_type == 'regression'):

                                if ControlVars.show_results:
                                    print(f"Metrics for {key}:\n")
                                mse = mean_squared_error(y_true, y_pred)

                                # Print in scientific notation:
                                if ControlVars.show_results:
                                    try:
                                        print(f"Mean squared error (MSE) = {mse:e}")
                                    except:
                                        print(f"Mean squared error (MSE) = {mse}")
                                # Add to calculated metrics:
                                calculated_metrics['mse'] = mse

                                rmse = mse**(1/2)

                                if ControlVars.show_results:
                                    try:
                                        print(f"Root mean squared error (RMSE) = {rmse:e}")
                                    except:
                                        print(f"Root mean squared error (RMSE) = {rmse}")
                                # Add to calculated metrics:
                                calculated_metrics['rmse'] = rmse

                                mae = mean_absolute_error(y_true, y_pred)

                                # Print in scientific notation:
                                if ControlVars.show_results:
                                    try:
                                        print(f"Mean absolute error (MAE) = {mae:e}")
                                    except:
                                        print(f"Mean absolute error (MAE) = {mae}")
                                # Add to calculated metrics:
                                calculated_metrics['mae'] = mae

                                # Mean absolute percentage error: non-stable Sklearn function
                                # y_true and y_pred must be already numpy arrays:
                                mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

                                # Print in scientific notation:
                                if ControlVars.show_results:
                                    try:
                                        print(f"Mean absolute percentage error (MAPE) = {mape:e}")
                                    except:
                                        print(f"Mean absolute percentage error (MAPE) = {mape}")
                                # Add to calculated metrics:
                                calculated_metrics['mape'] = mape

                                r2 = r2_score(y_true, y_pred)

                                if ControlVars.show_results:
                                    try:
                                        print(f"Coefficient of linear correlation R² = {r2:e}")
                                    except:
                                        print(f"Coefficient of linear correlation R² = {r2}")
                                # Add to calculated metrics:
                                calculated_metrics['r_squared'] = r2

                                # Manually correct R²:
                                # n_size_train = number of sample size
                                # k_model = number of independent variables of the defined model
                                k_model = self.total_predictors
                                #numer of rows
                                n_size = len(y_true)
                                r2_adj = 1 - (1 - r2)*(n_size - 1)/(n_size - k_model - 1)

                                if ControlVars.show_results:
                                    try:
                                        print(f"Adjusted coefficient of correlation R²-adj = {r2_adj:e}")
                                    except:
                                        print(f"Adjusted coefficient of correlation R²-adj = {r2_adj}")

                                # Add to calculated metrics:
                                calculated_metrics['r_squared_adj'] = r2_adj

                                explained_var = explained_variance_score(y_true, y_pred)
                                # Print in scientific notation:
                                if ControlVars.show_results:
                                    try:
                                        print(f"Explained variance = {explained_var:e}")

                                    except:
                                        print(f"Explained variance = {explained_var}")

                                # Explained variance is similar to the R² score, goes from 0 to 1, with the notable 
                                # difference that it does not account for systematic offsets in the prediction.
                                calculated_metrics['explained_variance'] = explained_var

                                print("\n")

                            else:

                                if ControlVars.show_results:
                                    print(f"Metrics for {key}:\n")

                                auc = roc_auc_score(y_true, y_pred)

                                if ControlVars.show_results:
                                    try:
                                        print(f"AUC = {auc:e}")
                                    except:
                                        print(f"AUC = {auc}")
                                # Add to calculated metrics:
                                calculated_metrics['auc'] = auc

                                acc = accuracy_score(y_true, y_pred)

                                if ControlVars.show_results:
                                    try:
                                        print(f"Accuracy = {acc:e}")
                                    except:
                                        print(f"Accuracy = {acc}")
                                # Add to calculated metrics:
                                calculated_metrics['accuracy'] = acc

                                precision = precision_score(y_true, y_pred)

                                if ControlVars.show_results:
                                    try:
                                        print(f"Precision = {precision:e}")
                                    except:
                                        print(f"Precision = {precision}")
                                # Add to calculated metrics:
                                calculated_metrics['precision'] = precision

                                recall = recall_score(y_true, y_pred)

                                if ControlVars.show_results:
                                    try:
                                        print(f"Recall = {recall:e}")
                                    except:
                                        print(f"Recall = {recall}")
                                # Add to calculated metrics:
                                calculated_metrics['recall'] = recall

                                # The method update_state returns None, so it must be called without and equality

                                # Get the classification report:
                                if ControlVars.show_results:
                                    print("\n")
                                    print("Classification Report:\n")
                                # Convert tensors to NumPy arrays
                                report = classification_report (y_true, y_pred)
                                if ControlVars.show_results:
                                    print(report)
                                # Add to calculated metrics:
                                calculated_metrics['classification_report'] = report
                                print("\n")

                                # Get the confusion matrix:
                                # Convert tensors to NumPy arrays
                                matrix = confusion_matrix (y_true, y_pred)
                                # Add to calculated metrics:
                                calculated_metrics['confusion_matrix'] = report
                                if ControlVars.show_results:
                                    print("Confusion matrix:\n")

                                if ControlVars.show_plots:
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
                                            file_name = "confusion_matrix_" + response

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
                                        new_file_path = new_file_path + ".png"
                                        # supported formats = 'png', 'pdf', 'ps', 'eps' or 'svg'
                                        #Export the file to this new path:
                                        plt.savefig(new_file_path, dpi = png_resolution_dpi, transparent = False) 
                                        # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html
                                        print (f"Figure exported as \'{new_file_path}\'. Any previous file in this root path was overwritten.")
                                    
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

                                nested_metrics[response] = calculated_metrics

                        except:
                            print(f"Unable to retrieve metrics for {key}:\n")
                            nested_metrics[response] = {f'metrics for {key}': f'No metrics retrieved for {response}'}

                metrics_dict[key] = nested_metrics
          
        # Now that we finished calculating metrics for all tensors, save the
        # dictionary as a class variable (attribute) and return the object:
        self.metrics_dict = metrics_dict
        
        return self
    
    
    def retrieve_classes_used_for_training (self):

        # Retrieve attributes:
        # Add the model:        
        y_train = self.y_train
        
        # Use numpy.unique to collect the unique classes, in the
        # order they appear:
        # They are the unique values from series xgb_y_train
        # https://numpy.org/doc/stable/reference/generated/numpy.unique.html?msclkid=ce35d85ec24511ec82dc9f13c97be8ce
        list_of_classes = np.unique(y_train)
        
        # Now use the list attribute to convert the array to a list:
        list_of_classes = list(list_of_classes)
        number_of_classes = len(list_of_classes)
        if ControlVars.show_results:
            print("\n") # line break
            print(f"Number of different classes in the training set = {number_of_classes}\n")
            print("List of classes:\n")
            print(list_of_classes)
            print("\n") # line break
        
        # Store this information as class attributes:
        self.list_of_classes = list_of_classes
        self.number_of_classes = number_of_classes

        return self


class WindowGenerator:
    """
    Class for creating a window for modelling time series datasets.
    def __init__(self, dataset, shift, use_past_responses_for_prediction = True, 
                 sequence_stride = 1, sampling_rate = 1, label_columns = None, 
                 train_pct = 70, val_pct = 10):
        
    original algorithm:
    https://www.tensorflow.org/tutorials/structured_data/time_series?hl=en&%3Bauthuser=1&authuser=1
    """
    
    def __init__ (self, dataset, shift, use_past_responses_for_prediction = True, 
                 sequence_stride = 1, sampling_rate = 1, label_columns = None, 
                 train_pct = 70, val_pct = 10):
        
        # Return an error if the percents are out of the allowable range:
        assert ((train_pct >= 0) & (train_pct <= 100))
        assert ((val_pct >= 0) & (val_pct <= 100))
        
        df = dataset.copy(deep = True)
        
        # Store the raw data.
        self.df = df
        self.sequence_stride = sequence_stride
        self.sampling_rate = sampling_rate
        self.shift = shift
        
        n = len(dataset)
        # Store the fractions for training and validation:
        self.train_boundary = int(n*(train_pct/100))
        self.val_boundary = int(n*(100 - val_pct)/100)
        
        
        # Set the response columns as a list, if it is a simple string:
    
        if ((type(label_columns) == tuple)|(type(label_columns) == set)):
            self.label_columns = list(label_columns)

        elif (type(label_columns) != list):
            self.label_columns = [label_columns]
        
        else:
            self.label_columns = label_columns
        
        # Set responses and features datasets
        y = (df[self.label_columns]).copy(deep = True)
        
        if (use_past_responses_for_prediction):
            # we use all the columns as predictors for the time series dataset:
            X = df
            
        else:
            # Since they will not be used, eliminate them
            X = df.drop(columns = self.label_columns)
        
        self.feature_columns = list(X.columns)
        self.num_features = X.shape[1]
        
        # Define each one of the train, test and validation dataframes as arrays:
        self.X_train = np.array(X[0:self.train_boundary])
        self.y_train = np.array(y[0:self.train_boundary])
        self.X_test = np.array(X[self.train_boundary:self.val_boundary])
        self.y_test = np.array(y[self.train_boundary:self.val_boundary])
        self.X_val = np.array(X[self.val_boundary:])
        self.y_val = np.array(y[self.val_boundary:])
              
        # In the time series TF dataset, all columns are used as predictors.
        # You can use entries on times t1, t2, t3 to predict t4, for example.
        # The predicted columns are the ones indicated as label_columns, i.e., columns that
        # will be used as the labels y.
        
        if label_columns is not None:
            
            self.label_columns_indices = {name: i for i, name in
                                        enumerate(self.label_columns)}
            
        self.column_indices = {name: i for i, name in
                                   enumerate(self.df.columns)}
        
        """
        slice object: object that defines the slicing interval. slice(x,y) is equivalent
        to defining the interval [x:y] for slicing.
        Example: a = list(range(0,99))
        b = slice(10,22)
        c = a[b] is equivalent to c = a[10:22], resulting in [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
        if b = slice(1,3), c = [1, 2], which are the indices 1 and 2 (indexing starting from 0)
        
        """
    

    def split_as_labels_and_inputs (self, X, y):
       
        shift = self.shift
        # shift: the sequence of timesteps i, i+1, ... will be used for predicting the
        # timestep i + shift
        stride = self.sequence_stride
        # if a sequence starts in index i, the next sequence will start from i + stride
        sampling = self.sampling_rate
        # the sequence will be formed by timesteps i, i + sampling_rate, i + 2* sampling_rate, ...
        """
        Example from TensorFlow documentation: 
        https://www.tensorflow.org/api_docs/python/tf/keras/utils/timeseries_dataset_from_array
        
        Consider indices [0, 1, ... 99]. With sequence_length=10, sampling_rate=2, sequence_stride=3, 
        shuffle=False, the dataset will yield batches of sequences composed of the following indices:

        First sequence:  [0  2  4  6  8 10 12 14 16 18]
        Second sequence: [3  5  7  9 11 13 15 17 19 21]
        Third sequence:  [6  8 10 12 14 16 18 20 22 24]
        ...
        Last sequence:   [78 80 82 84 86 88 90 92 94 96]
        """
        
        total_elements = len(X)
        start_index = 0
        stop_index = start_index + shift
        
        # List to store all arrays
        list_of_inputs = []
        list_of_labels = []
        
        while (start_index < total_elements):
            
            try:
                # Slice the X array from start to stop, with step = sampling
                # Array slice: [start:stop:sampling]
                added_input = X[start_index:stop_index:sampling]
                # Notice that stop_index is not added. It is actually the index to be picked from y:
                added_label = y[stop_index]
                
                # add them to the lists of arrays:
                list_of_inputs.append(np.array(added_input))
                list_of_labels.append(np.array(added_label))
                # Update the start and stop indices:
                start_index = start_index + stride
                stop_index = stop_index + stride
            
            except:
                # The elements actually finished, due to shifting and striding, so stop the loop
                break
        
        # Convert lists to arrays and then to tensors:
        inputs_tensor = np.array(list_of_inputs)
        labels_tensor = np.array(list_of_labels)
        
        inputs_tensor = tf.constant(inputs_tensor)
        labels_tensor = tf.constant(labels_tensor)
        
        return inputs_tensor, labels_tensor
    
    
    def make_tensors (self):
        
        # start a tensors dictionary
        tensors_dict = {}
        
        for group in ['train', 'test', 'val']:
            
            # Use vars function to access the correct attributes storing the desired arrays.
            # The vars function allows you to access an attribute as a string
            X = vars(self)[('X_' + group)]
            y = vars(self)[('y_' + group)]
            
            # Split into inputs and labels
            inputs_tensor, labels_tensor = self.split_as_labels_and_inputs(X = X, y = y)
            # Store them in the tensors dictionary:
            tensors_dict[group] = {'inputs': inputs_tensor, 'labels': labels_tensor}
        
        # Save the dictionary as class variable:
        self.tensors_dict = tensors_dict
        
        return self


class TfModels:
    """
    Class for creating deep learning models from TensorFlow.

    def __init__(self, X_train, y_train, X_valid = None, y_valid = None, 
        type_of_problem = 'regression', number_of_classes = 2, optimizer = None):
        
    TensorFlow models with single input, single output, or single input and possibly
    1 regression and 1 classification output.
    Use preferentially for these situations.
    """
    
    def __init__ (self, X_train, y_train, X_valid = None, y_valid = None, type_of_problem = 'regression', number_of_classes = 2, optimizer = None):
        
        # type_of_problem = 'regression', 'classification', 'both'
        # optimizer: tf.keras.optimizers.Optimizer object:
        # https://www.tensorflow.org/api_docs/python/tf/keras/optimizers
        # https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/Optimizer
        # use the object to set parameters such as learning rate and selection of the optimizer
        
        # Guarantee it is an array:
        self.X_train = np.array(X_train)
        self.y_train = np.array(y_train)
        
        # Input layer with shape given by the number of columns of the tensors. If using an image
        # it would be the number of pixels in X and Y axis, with the image depth
        # The batch (last) dimension should not be provided to the input layer
        self.input_layer = tf.keras.layers.Input(shape = (X_train.shape)[1:], name = "input_layer")
        
        if ((X_valid is not None) & (y_valid is not None)):
            if ((len(X_valid) > 0) & (len(y_valid) > 0)):
            
                self.X_valid = np.array(X_valid)
                self.y_valid = np.array(y_valid)
            else:
                self.X_valid = None
                self.y_valid = None
        
        else:
            self.X_valid = None
            self.y_valid = None
        
        self.type_of_problem = type_of_problem
        self.number_of_classes = number_of_classes
        
        if (type_of_problem == 'regression'):    
            self.metrics = [tf.keras.metrics.MeanAbsoluteError()]
            # https://www.tensorflow.org/api_docs/python/tf/keras/metrics/MeanAbsoluteError
            self.loss = 'mse'
            self.output_layer = tf.keras.layers.Dense(units = 1, name = 'output')
            self.metrics_name = 'mean_absolute_error'
        
        elif (type_of_problem == 'classification'):
            
            self.metrics = 'acc'
            self.metrics_name = 'acc'
            
            if (number_of_classes == 2):
                self.output_layer = tf.keras.layers.Dense(units = 1, activation = 'sigmoid', name = 'output')
                # Dense(1) activated through sigmoid is the logistic regression: generayes a
                # probability between 0 and 1
                self.loss = 'binary_crossentropy'
                # https://www.tensorflow.org/api_docs/python/tf/keras/metrics/BinaryCrossentropy
            else:
                self.output_layer = tf.keras.layers.Dense(units = number_of_classes, activation = 'softmax', name = 'output')
                self.loss = 'sparse_categorical_crossentropy'
                # https://www.tensorflow.org/api_docs/python/tf/keras/metrics/SparseCategoricalCrossentropy
        
        else: # both
            
            self.metrics_regression = [tf.keras.metrics.MeanAbsoluteError()]
            self.loss_regression = 'mse'
            self.output_regression_layer = tf.keras.layers.Dense(units = 1, name = 'output_regression')
            
            self.metrics_classification = 'acc'
            
            if (number_of_classes == 2):
                self.output_classification_layer = tf.keras.layers.Dense(units = 1, activation = 'sigmoid', name = 'output_classification')
                self.loss_classification = 'binary_crossentropy'
                # https://www.tensorflow.org/api_docs/python/tf/keras/metrics/BinaryCrossentropy
            else:
                self.output_classification_layer = tf.keras.layers.Dense(units = number_of_classes, activation = 'softmax', name = 'output_classification')
                self.loss_classification = 'sparse_categorical_crossentropy'
                # https://www.tensorflow.org/api_docs/python/tf/keras/metrics/SparseCategoricalCrossentropy

        # create a model attribute, and an history attribute:
        self.model = None
        self.history = None
        
        # Set the optimizer:
        if (optimizer is None):
            # use Adam with default arguments
            # https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/Adam
            optimizer = tf.keras.optimizers.Adam()
        
        # Save the optimizer as an attribute:
        self.optimizer = optimizer
    
    
    def compile_model (self):
        
        optimizer = self.optimizer
        input_layer = self.input_layer
        model = self.model
        type_of_problem = self.type_of_problem
        
        if ((type_of_problem == 'regression')|((type_of_problem == 'classification'))):
            # model = tf.keras.models.Model(inputs = [input_layer], outputs = [output_layer])
            # When declaring the metrics as an object, they must be provided to the compile
            # method within a list:
            # https://www.tensorflow.org/api_docs/python/tf/keras/metrics/RootMeanSquaredError
            # or as the attribute ._name, which contains the correspondent string
            
            output_layer = self.output_layer
            loss = self.loss
            metrics = self.metrics
            
            if ControlVars.show_plots:
                print("Check model architecture:\n")
                tf.keras.utils.plot_model(model)
                print("\n")
            
            # Compile model:
            model.compile(optimizer = optimizer,
                          loss = loss,
                          metrics = metrics)
        
        else:
            # model = tf.keras.models.Model(inputs = [input_layer], outputs = [output_regression_layer, output_classification_layer])
            
            metrics_regression = self.metrics_regression
            loss_regression = self.loss_regression
            output_regression_layer = self.output_regression_layer
            metrics_classification = self.metrics_classification
            output_classification_layer = self.output_classification_layer
            loss_classification = self.loss_classification
            
        
            """
            For multiple output layers:
            
            'wine_type' and 'wine_quality' are the 'name's of the output layers:

            model.compile(optimizer=rms, 
                           loss = {'wine_type' : 'binary_crossentropy',
                                   'wine_quality' : 'mean_squared_error'
                                  },
                           metrics = {'wine_type' : 'accuracy',
                                      'wine_quality': tf.keras.metrics.RootMeanSquaredError()
                                    }
                          )

            """
            
            
            if ControlVars.show_plots:
                print("Check model architecture:\n")
                tf.keras.utils.plot_model(model)
                print("\n")
            
            # Compile model:
            model.compile(optimizer = optimizer,
                          loss = {'output_classification': loss_classification,
                                  'output_regression': loss_regression},
                          metrics = {'output_classification': metrics_classification,
                                    'output_regression': metrics_regression})
        
        
        if ControlVars.show_results:
            print("Check model summary:\n")
            try:
                # only works in Jupyter Notebook:
                from IPython.display import display
                display(model.summary())
                        
            except: # regular mode
                print(model.summary())
        
        # Now, save the model in the attribute and return the object:
        self.model = model
        
        return self
    

    def fit_model (self, epochs = 2000, batch_size = 200, verbose = 1):
               
        # If you set verbose = 0, It will show nothing. If you set verbose = 1, It will 
        # show the output like this: Epoch 1/200 55/55[=====] - 10s 307ms/step - loss: 0.56 - 
        # accuracy: 0.4949
        
        model = self.model
        
        X_train = self.X_train
        y_train = self.y_train
        
        X_valid = self.X_valid
        y_valid = self.y_valid
        
        if ((X_valid is not None) & (y_valid is not None)):   
            has_validation = True
        
        else:
            has_validation = False
        
        # Fit the model:
        if (has_validation):
            history = model.fit(X_train, 
                                y_train,
                                batch_size = batch_size,
                                epochs = epochs,
                                verbose = verbose,
                                validation_data = (X_valid, y_valid))
        
        else: # no validation set
            history = model.fit(X_train, 
                                y_train,
                                batch_size = batch_size,
                                epochs = epochs,
                                verbose = verbose)
        
        # Update the attributes and return the object:
        self.history = history
        self.model = model
        
        return self
    

    def tf_simple_dense (self, epochs = 2000, batch_size = 200, verbose = 1):
        
        """
        Wide and deep example:

        # define inputs
        input_a = Input(shape=[1], name="Wide_Input")
        input_b = Input(shape=[1], name="Deep_Input")

        # define deep path
        hidden_1 = Dense(30, activation="relu")(input_b)
        hidden_2 = Dense(30, activation="relu")(hidden_1)

        # define merged path
        concat = concatenate([input_a, hidden_2])
        output = Dense(1, name="Output")(concat)

        # define another output for the deep path
        aux_output = Dense(1,name="aux_Output")(hidden_2)

        # build the model
        model = Model(inputs=[input_a, input_b], outputs=[output, aux_output])

        """
        input_layer = self.input_layer
        output_layer = self.output_layer
        
        # define inputs
        input_1 = input_layer
        # Creating blocks of Simple dense with the following 
        # (filters, kernel_size, repetitions) configurations:
        # tf.keras.layers.Dense(128, activation = 'relu', input_dim = INPUT_DIMENSION)
        # tf.keras.layers.Dense(1)

        # First hidden layer:
        x = tf.keras.layers.Dense(units = 128, activation = 'relu', name = 'dense_1')(input_1)
        # 'relu' = ReLU, the Rectified Linear Unit function, returns f(x) = max(0, x)
        # (i.e., if x <=0, relu(x) = 0; if (x > 0), relu(x) = 0)  
        # The integer passed as parameter for Dense is the parameter 'units' from Dense
        # layer. The number ("units") used as input for the dense function Dense(units) is a 
        # Positive integer that represents the dimensionality of the output space.
        # Here, 'units' = 100, so this first hidden-layer has 100 neurons
        
        output_1 = output_layer(x)
        
        model = tf.keras.models.Model(inputs = input_1, outputs = output_1, name = 'tf_simple_dense')
        # Update model attribute:
        self.model = model
        
        # Compile the model:
        self = self.compile_model()
        # Fit the model:
        self = self.fit_model(epochs = epochs, batch_size = batch_size, verbose = verbose)
        
        # return compiled model:
        return self
    

    def tf_double_dense (self, epochs = 2000, batch_size = 200, verbose = 1):
 
        input_layer = self.input_layer
        output_layer = self.output_layer
        
        # define inputs
        input_1 = input_layer
        # Creating blocks of Simple dense with the following 
        # (filters, kernel_size, repetitions) configurations:
        # tf.keras.layers.Dense(128, activation = 'relu', input_dim = INPUT_DIMENSION)
        # tf.keras.layers.Dense(1)

        # First hidden layer:
        x = tf.keras.layers.Dense(units = 128, activation = 'relu', name = 'dense_1')(input_1)
        # 'relu' = ReLU, the Rectified Linear Unit function, returns f(x) = max(0, x)
        # (i.e., if x <=0, relu(x) = 0; if (x > 0), relu(x) = 0)  
        # The integer passed as parameter for Dense is the parameter 'units' from Dense
        # layer. The number ("units") used as input for the dense function Dense(units) is a 
        # Positive integer that represents the dimensionality of the output space.
        # Here, 'units' = 100, so this first hidden-layer has 100 neurons
        x = tf.keras.layers.Dense(units = 128, activation = 'relu', name = 'dense_2')(x)
        
        output_1 = output_layer(x)
        
        model = tf.keras.models.Model(inputs = input_1, outputs = output_1, name = 'tf_double_dense')
        # Update model attribute:
        self.model = model
        
        # Compile the model:
        self = self.compile_model()
        # Fit the model:
        self = self.fit_model(epochs = epochs, batch_size = batch_size, verbose = verbose)
        
        return self
    

    def tf_cnn_time_series (self, epochs = 2000, batch_size = 200, verbose = 1):
        
        input_layer = self.input_layer
        output_layer = self.output_layer
        
        # define inputs
        input_1 = input_layer
        # Creating blocks of Simple dense with the following 
        # (filters, kernel_size, repetitions) configurations:
        # tf.keras.layers.Dense(128, activation = 'relu', input_dim = INPUT_DIMENSION)
        # tf.keras.layers.Dense(1)
        
        # ATTENTION: if the first layer is a Dense, we must specify
        # the parameter 'input_dim'. If it is a CNN or RNN, we
        # specify 'input_shape', instead. These parameters are only
        # specified for the first layer of the network.
        
        # First convolution:
        x = tf.keras.layers.Conv1D(filters = 64, kernel_size = 2, activation = 'relu', input_shape = (self.X_train.shape[1], 1), name = 'convolution')(input_1)
        # First Max Pooling to enhance select the characteristics highlighted by the convolution:
        x = tf.keras.layers.MaxPooling1D(pool_size = 2, name = 'pooling')(x)
        # Reduces to half the original size.
            
        # The convolutions and pooling reduce the dimensionality of the data.
        # Under the hood, TensorFlow is testing different combinations of filters until it finds
        # filters that actually highlight important characteristics.
        # On the other hand, apply too much convolutional layers may reduce too much the data, making
        # it difficult for the last dense layer to perform a good prediction.
            
        # Flatten the data for making it adequate for feeding the dense layers:
        x = tf.keras.layers.Flatten(name = 'flatten')(x)
            
        # Feed the first dense layer, with 50 neurons:
        x = tf.keras.layers.Dense(units = 50, activation = 'relu', name = 'dense_1')(x)
        # 'relu' = ReLU, the Rectified Linear Unit function, returns f(x) = max(0, x)
        # (i.e., if x <=0, relu(x) = 0; if (x > 0), relu(x) = 0)
        
        output_1 = output_layer(x)
        
        model = tf.keras.models.Model(inputs = input_1, outputs = output_1, name = 'tf_cnn_time_series')
        # Update model attribute:
        self.model = model
        
        # Compile the model:
        self = self.compile_model()
        # Fit the model:
        self = self.fit_model(epochs = epochs, batch_size = batch_size, verbose = verbose)
        
        # return compiled model:
        return self
    

    def tf_lstm_time_series (self, epochs = 2000, batch_size = 200, verbose = 1):
               
        input_layer = self.input_layer
        output_layer = self.output_layer
        # Number of columns (sequence length):
        
        # define inputs
        input_1 = input_layer
        # Creating blocks of Simple dense with the following 
        # (filters, kernel_size, repetitions) configurations:
        # tf.keras.layers.Dense(128, activation = 'relu', input_dim = INPUT_DIMENSION)
        # tf.keras.layers.Dense(1)
        
        # LSTM layer: 1 cycle per sequence element (number of iterations = 
        # SEQUENCE_LENGTH):
        # LSTM with 50 neurons:
        x = tf.keras.layers.LSTM(units = 50, activation = 'relu', input_shape = (self.X_train.shape[1], 1), name = 'lstm')(input_1)
        # 'relu' = ReLU, the Rectified Linear Unit function, returns f(x) = max(0, x)
        # (i.e., if x <=0, relu(x) = 0; if (x > 0), relu(x) = 0)
            
        # We will use one LSTM layer to process each input sub-sequence 
        # of N time steps, followed by a Dense layer to interpret the 
        # summary of the input sequence.
        
        output_1 = output_layer(x)
        
        model = tf.keras.models.Model(inputs = input_1, outputs = output_1, name = 'tf_lstm_time_series')
        # Update model attribute:
        self.model = model
        
        # Compile the model:
        self = self.compile_model()
        # Fit the model:
        self = self.fit_model(epochs = epochs, batch_size = batch_size, verbose = verbose)
        
        # return compiled model:
        return self
    

    def tf_encoder_decoder_time_series (self, epochs = 2000, batch_size = 200, verbose = 1):
               
        input_layer = self.input_layer
        output_layer = self.output_layer
        
        
        # define inputs
        input_1 = input_layer
        # Creating blocks of Simple dense with the following 
        # (filters, kernel_size, repetitions) configurations:
        # tf.keras.layers.Dense(128, activation = 'relu', input_dim = INPUT_DIMENSION)
        # tf.keras.layers.Dense(1)
        
        # LSTM layer: 1 cycle per sequence element (number of iterations = SEQUENCE_LENGTH):
        # LSTM with 100 neurons:
        # Encoder:
        x = tf.keras.layers.LSTM(units = 100, activation = 'relu', input_shape = (self.X_train.shape[1], 1), name = 'lstm_encoder')(input_1)
            
        # The encoded sequence will be repeated 2 times by the model for the two output time steps 
        # required by the model using a RepeatVector layer. These will be fed to a decoder LSTM layer 
        # before using a Dense output layer wrapped in a TimeDistributed layer that will produce one 
        # output for each step in the output sequence.
        x = tf.keras.layers.RepeatVector(2, name = 'repeat_vector')(x)
        # Decoder: LSTM with 100 neurons
        x = tf.keras.layers.LSTM(units = 100, activation = 'relu', return_sequences = True, name = 'lstm_decoder')(x)
        # return_sequences = True returns the hidden states h.
        # This generates an output with an extra dimension (output consists on an array of two values: 
        # the prediction and the hidden state).
            
        # Last dense - output layer ('linear' activation):
        # Apply a TimeDistributed layer for compatibility with the Encoder-Decoder Archictecture:
        # Wrap the output into this layer:
        output_1 = tf.keras.layers.TimeDistributed(output_layer, name = 'time_distributed_output')(x)
        
        model = tf.keras.models.Model(inputs = input_1, outputs = output_1, name = 'tf_encoder_decoder_time_series')
        # Update model attribute:
        self.model = model
        
        # Compile the model:
        self = self.compile_model()
        # Fit the model:
        self = self.fit_model(epochs = epochs, batch_size = batch_size, verbose = verbose)
        
        # return compiled model:
        return self
    

    def tf_cnn_lstm_time_series (self, epochs = 2000, batch_size = 200, verbose = 1):
        
        # NOT WORKING
     
        input_layer = self.input_layer
        output_layer = self.output_layer
                
        convolution_layer = tf.keras.layers.Conv1D(filters = 64, kernel_size = 1, activation = 'relu', input_shape = (None, 2, 1))
        # Originally: input_shape = (None, 2, 1)
        max_pooling_layer = tf.keras.layers.MaxPooling1D(pool_size = 2)
        flatten_layer = tf.keras.layers.Flatten()
        
        # define inputs
        input_1 = input_layer
        # Creating blocks of Simple dense with the following 
        # (filters, kernel_size, repetitions) configurations:
        # tf.keras.layers.Dense(128, activation = 'relu', input_dim = INPUT_DIMENSION)
        # tf.keras.layers.Dense(1)
      
        # The entire CNN model is wrapped in TimeDistributed wrapper layers so that it can be applied to 
        # each subsequence in the  sample. The results are then interpreted by the LSTM layer 
        # before the model outputs a prediction.
        
        # First time-distributed convolution (for compatibility with the LSTM):
        x  = tf.keras.layers.TimeDistributed(convolution_layer, name = 'convolution')(input_1)
        # First time distributed Max Pooling (for compatibility with the LSTM):
        # Max Pooling: enhance select the characteristics highlighted by the convolution:
        x = tf.keras.layers.TimeDistributed(max_pooling_layer, name = 'pooling')(x)
        # Reduces to half the original size.
        # The convolutions and pooling reduce the dimensionality of the data.
        # Under the hood, TensorFlow is testing different combinations of filters until it finds filters 
        # that actually highlight important characteristics.
        # On the other hand, apply too much convolutional layers may reduce too much the data, making
        # it difficult for the last dense layer to perform a good prediction.        
        # Flatten the data for making it adequate for feeding the dense layers:
        # Time distributed Flatten for compatibility with the LSTM:
        x = tf.keras.layers.TimeDistributed(flatten_layer, name = 'flatten')(x)
            
        # Now, feed the LSTM:
        # The LSTM performs 1 cycle per element of the sequence. Since each sequence now have 2 elements,
        # the LSTM will perform two iterations:
        # LSTM with 50 neurons:
        x = tf.keras.layers.LSTM(units = 50, activation = 'relu', name = 'lstm')(x)
        # 'relu' = ReLU, the Rectified Linear Unit function, returns f(x) = max(0, x)
        # (i.e., if x <=0, relu(x) = 0; if (x > 0), relu(x) = 0)
        output_1 = output_layer(x)    
       
        model = tf.keras.models.Model(inputs = input_1, outputs = output_1, name = 'tf_cnn_lstm_time_series')
        # Update model attribute:
        self.model = model
        
        # Compile the model:
        self = self.compile_model()
        # Fit the model:
        self = self.fit_model(epochs = epochs, batch_size = batch_size, verbose = verbose)
        
        # return compiled model:
        return self


class SiameseNetworks:
    """
    Class for obtaining deep learning Siamese Neural Networks models using TensorFlow.

    def __init__(self, output_dictionary, X_train, y_train, X_valid = None, y_valid = None):
    
    TensorFlow models for multiple responses. The neural networks are replicated for each one
    of the responses.
    """
    
    def __init__ (self, output_dictionary, X_train, y_train, X_valid = None, y_valid = None):
        
        # type_of_problem = 'regression', 'classification', 'both'
        # optimizer: tf.keras.optimizers.Optimizer object:
        # https://www.tensorflow.org/api_docs/python/tf/keras/optimizers
        # https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/Optimizer
        # use the object to set parameters such as learning rate and selection of the optimizer
        
        # ATTENTION, y_train, y_valid must be tensors or numpy arrays containing the responses in the
        # exact same order as the responses declared in the output dictionary

        # output_dictionary:
        # output_dictionary structure:
        # {'response_variable': {
        # 'type': 'regression', 'number_of_classes':}}
        # 'response_variable': name of the column used as response for one of the outputs. This key
        # gives access to the nested dictionary containing the following keys: 
        # 'type': type of problem. Must contain the string 'regression' or 'classification';
        # 'number_of_classes': integer. This key may not be declared for regression problems. Do not
        # include the key, set as 1, or set the number of classes used for training.
              
        self.output_dictionary = output_dictionary
        
        # Retrieve the list of responses (the keys from this dictionary)
        self.list_of_responses = list((self.output_dictionary).keys())

        # Define an internal function for reformating the data in the format needed.
        # We need a tuple formed by each one of the responses at time:
        # (response1, response2, ...)
        def format_output(data, list_of_responses):
            # Convert to NumPy array, if it is a tensor:
            data = np.array(data)
            
            # number of data columns must be equal to the total of responses
            try:
                assert data.shape[1] == len(list_of_responses)
            
            except:
                raise AssertionError (f"Response tensor contains {data.shape[1]} responses, but found only {len(list_of_responses)} responses ({list_of_responses}) in the dictionary. Check your output dictionary before running this function.\n")
            
            # Convert to Pandas dataframe:
            data = pd.DataFrame(data = data, columns = list_of_responses)
            # Start a list of tensors:
            tensors_list = []
            # Apply the pop method to return a particular column and drop it from data:
            for column in list_of_responses:
                response = data.pop(column)
                # Convert the response Pandas Series to a numpy array:
                response = np.array(response)
                # Add it to tensors list:
                tensors_list.append(response)
            # Convert the list to tuple and return it:
            return tuple(tensors_list)

        # Guarantee it is an array:
        self.X_train = np.array(X_train)
        self.y_train = format_output(data = y_train, list_of_responses = self.list_of_responses)
    
        
        if ((X_valid is not None) & (y_valid is not None)):
            if ((len(X_valid) > 0) & (len(y_valid) > 0)):
            
                self.X_valid = np.array(X_valid)
                self.y_valid = format_output(data = y_valid, list_of_responses = self.list_of_responses)
            else:
                self.X_valid = None
                self.y_valid = None
        
        else:
            self.X_valid = None
            self.y_valid = None
        
        # Input layer with shape given by the number of columns of the tensors. If using an image
        # it would be the number of pixels in X and Y axis, with the image depth
        # The batch (last) dimension should not be provided to the input layer
        input_layer = tf.keras.layers.Input(shape = (X_train.shape)[1:], name = "input_layer")
        # Save it as an attribute
        self.inputs = input_layer
    
    
    def fit_model (self, epochs = 2000, batch_size = 200, verbose = 1):
           
        # If you set verbose = 0, It will show nothing. If you set verbose = 1, It will 
        # show the output like this: Epoch 1/200 55/55[=====] - 10s 307ms/step - loss: 0.56 - 
        # accuracy: 0.4949
        
        model = self.model
        
        # There must be one copy of the input by response. So, before fitting the model, let's create
        # tuples with same size as the total of responses, where all elements of the tuple are equal
        # to the X tensor. Each element will be sequentially used by the model to fit one of the
        # responses: first element for the first branch, 2nd for the 2nd branch, and so on...
        
        # Retrieve the outputs dictionary
        output_dictionary = self.output_dictionary
        
        X_train = self.X_train
        y_train = self.y_train
        
        X_valid = self.X_valid
        y_valid = self.y_valid
        
        if ((X_valid is not None) & (y_valid is not None)):   
            has_validation = True
    
        else:
            has_validation = False
        
        # Fit the model:
        if (has_validation):
            history = model.fit(X_train, 
                                y_train,
                                batch_size = batch_size,
                                epochs = epochs,
                                verbose = verbose,
                                validation_data = (X_valid, y_valid))
        
        else: # no validation set
            history = model.fit(X_train, 
                                y_train,
                                batch_size = batch_size,
                                epochs = epochs,
                                verbose = verbose)
        
        # Update the attributes and return the object:
        self.history = history
        self.model = model
        
        return self
    
    
    def base_model_simple_dense (self, input_layer, response):
        
        # First hidden layer:
        x = tf.keras.layers.Dense(units = 128, activation = 'relu', name = ('dense_1'+ '_' + response))(input_layer)
        
        return x
    
    
    def base_model_double_dense (self, input_layer, response):
        
        # First hidden layer:
        x = tf.keras.layers.Dense(units = 128, activation = 'relu', name = ('dense_1' + '_' + response))(input_layer)
        x = tf.keras.layers.Dense(units = 128, activation = 'relu', name = ('dense_2' + '_' + response))(x)
            
        return x
    
    
    def base_model_cnn_time_series (self, input_layer, response):
        
        # First convolution:
        x = tf.keras.layers.Conv1D(filters = 64, kernel_size = 2, activation = 'relu', name = ('convolution' + '_' + response))(input_layer)
        # First Max Pooling to enhance select the characteristics highlighted by the convolution:
        x = tf.keras.layers.MaxPooling1D(pool_size = 2, name = ('pooling' + '_' + response))(x)
        # Reduces to half the original size.
            
        # The convolutions and pooling reduce the dimensionality of the data.
        # Under the hood, TensorFlow is testing different combinations of filters until it finds
        # filters that actually highlight important characteristics.
        # On the other hand, apply too much convolutional layers may reduce too much the data, making
        # it difficult for the last dense layer to perform a good prediction.
            
        # Flatten the data for making it adequate for feeding the dense layers:
        x = tf.keras.layers.Flatten(name = ('flatten' + '_' + response))(x)
            
        # Feed the first dense layer, with 50 neurons:
        x = tf.keras.layers.Dense(units = 50, activation = 'relu', name = ('dense_1' + '_' + response))(x)
        # 'relu' = ReLU, the Rectified Linear Unit function, returns f(x) = max(0, x)
        # (i.e., if x <=0, relu(x) = 0; if (x > 0), relu(x) = 0)
        
        return x
    
    
    def base_model_lstm_time_series (self, input_layer, response):
        
        # LSTM layer: 1 cycle per sequence element (number of iterations = 
        # SEQUENCE_LENGTH):
        # LSTM with 50 neurons:
        x = tf.keras.layers.LSTM(units = 50, activation = 'relu', input_shape = (self.X_train.shape[1], 1), name = ('lstm' + '_' + response))(input_layer)
        # 'relu' = ReLU, the Rectified Linear Unit function, returns f(x) = max(0, x)
        # (i.e., if x <=0, relu(x) = 0; if (x > 0), relu(x) = 0)
            
        # We will use one LSTM layer to process each input sub-sequence 
        # of N time steps, followed by a Dense layer to interpret the 
        # summary of the input sequence.
        
        return x
    
    
    def base_model_encoder_decoder_time_series (self, input_layer, response):
        
        # LSTM layer: 1 cycle per sequence element (number of iterations = SEQUENCE_LENGTH):
        # LSTM with 100 neurons:
        # Encoder:
        x = tf.keras.layers.LSTM(units = 100, activation = 'relu', input_shape = (self.X_train.shape[1], 1), name = ('lstm_encoder' + '_' + response))(input_layer)
            
        # The encoded sequence will be repeated 2 times by the model for the two output time steps 
        # required by the model using a RepeatVector layer. These will be fed to a decoder LSTM layer 
        # before using a Dense output layer wrapped in a TimeDistributed layer that will produce one 
        # output for each step in the output sequence.
        x = tf.keras.layers.RepeatVector(2, name = ('repeat_vector' + '_' + response))(x)
        # Decoder: LSTM with 100 neurons
        x = tf.keras.layers.LSTM(units = 100, activation = 'relu', return_sequences = True, name = ('lstm_decoder' + '_' + response))(x)
        # return_sequences = True returns the hidden states h.
        # This generates an output with an extra dimension (output consists on an array of two values: 
        # the prediction and the hidden state).
        
        return x
    
    
    def base_model_cnn_lstm_time_series (self, input_layer, response):
        
        # NOT WORKING

        convolution_layer = tf.keras.layers.Conv1D(filters = 64, kernel_size = 1, activation = 'relu', input_shape = (None, 2, 1))
        # Originally: input_shape = (None, 2, 1)
        max_pooling_layer = tf.keras.layers.MaxPooling1D(pool_size = 2)
        flatten_layer = tf.keras.layers.Flatten()
      
        # The entire CNN model is wrapped in TimeDistributed wrapper layers so that it can be applied to 
        # each subsequence in the  sample. The results are then interpreted by the LSTM layer 
        # before the model outputs a prediction.
        
        # First time-distributed convolution (for compatibility with the LSTM):
        x  = tf.keras.layers.TimeDistributed(convolution_layer,  name = ('convolution' + '_' + response))(input_layer)
        # First time distributed Max Pooling (for compatibility with the LSTM):
        # Max Pooling: enhance select the characteristics highlighted by the convolution:
        x = tf.keras.layers.TimeDistributed(max_pooling_layer, name = ('pooling' + '_' + response))(x)
        # Reduces to half the original size.
        # The convolutions and pooling reduce the dimensionality of the data.
        # Under the hood, TensorFlow is testing different combinations of filters until it finds filters 
        # that actually highlight important characteristics.
        # On the other hand, apply too much convolutional layers may reduce too much the data, making
        # it difficult for the last dense layer to perform a good prediction.        
        # Flatten the data for making it adequate for feeding the dense layers:
        # Time distributed Flatten for compatibility with the LSTM:
        x = tf.keras.layers.TimeDistributed(flatten_layer, name = ('flatten'+ '_' + response))(x)
            
        # Now, feed the LSTM:
        # The LSTM performs 1 cycle per element of the sequence. Since each sequence now have 2 elements,
        # the LSTM will perform two iterations:
        # LSTM with 50 neurons:
        x = tf.keras.layers.LSTM(units = 50, activation = 'relu', name = ('lstm' + '_' + response))(x)
        # 'relu' = ReLU, the Rectified Linear Unit function, returns f(x) = max(0, x)
        # (i.e., if x <=0, relu(x) = 0; if (x > 0), relu(x) = 0)
        
        return x
    
    
    def network_branch (self, response_variable, type_of_problem = 'regression', number_of_classes = 2, architecture = 'simple_dense'):
        
        # Generate a full branch from the siamese network. We will have one branch per response
        
        # architecture = 'simple_dense': base_model_simple_dense from class SiameseNetworks;
        # architecture = 'double_dense': base_model_double_dense from class SiameseNetworks;
        # architecture = 'cnn': base_model_cnn_time_series from class SiameseNetworks;
        # architecture = 'lstm': base_model_lstm_time_series from class SiameseNetworks;
        # architecture = 'encoder_decoder': base_model_encoder_decoder_time_series from class SiameseNetworks;
        # architecture = 'cnn_lstm': hybrid base_model_cnn_lstm_time_series from class SiameseNetworks.
        
        
        input_layer = self.inputs
        
        if (architecture == 'double_dense'):
            x = self.base_model_double_dense(input_layer = input_layer, response = response_variable)
            
        elif (architecture == 'cnn'):
            x = self.base_model_cnn_time_series(input_layer = input_layer, response = response_variable)
            
        elif (architecture == 'lstm'):
            x = self.base_model_lstm_time_series(input_layer = input_layer, response = response_variable)
            
        elif (architecture == 'encoder_decoder'):
            x = self.base_model_encoder_decoder_time_series(input_layer = input_layer, response = response_variable)
            
        elif (architecture == 'cnn_lstm'):
            x = self.base_model_cnn_lstm_time_series(input_layer = input_layer, response = response_variable)
            
        else:
            x = self.base_model_simple_dense(input_layer = input_layer, response = response_variable)
        
        if (type_of_problem == 'regression'):
            # Scalar output: 1 neuron with linear activation
            output = tf.keras.layers.Dense(units = 1, name = ('output_' + response_variable))
            if (architecture == 'encoder_decoder'):
                output = tf.keras.layers.TimeDistributed(output, name = ('output_' + response_variable))(x)
            else:
                    output = output(x)
           
        else:
            # Classification
            if (number_of_classes == 2):
                # 1 neuron activated through sigmoid, analogous to logistic regression
                output = tf.keras.layers.Dense(units = 1, activation = 'sigmoid', name = ('output_' + response_variable))
                if (architecture == 'encoder_decoder'):
                    output = tf.keras.layers.TimeDistributed(output, name = ('output_' + response_variable))(x)
                else:
                    output = output(x)
                
            else:
                # 1 neuron per class, activated through softmax
                output = tf.keras.layers.Dense(units = number_of_classes, activation = 'softmax', name = ('output_' + response_variable))
                if (architecture == 'encoder_decoder'):
                    output = tf.keras.layers.TimeDistributed(output, name = ('output_' + response_variable))(x)
                else:
                    output = output(x)
                    
        return output
    
    
    def compile_model (self, architecture, optimizer = None):
        
        # output_dictionary structure:
        # {'response_variable': {
        # 'type': 'regression', 'number_of_classes':}}
        
        # Retrieve the outputs dictionary
        output_dictionary = self.output_dictionary
        
        # Initialize a loss and a metrics dictionary
        loss_dict = {}
        metrics_dict = {}
        
        # Initialize a list of output layers:
        outputs_list = []
        
        # Loop through all the keys from the output_dictionary:
        for response in output_dictionary.keys():
            
            nested_dict = output_dictionary[response]
            # Retrieve the type of problem and the number of classes:
            
            type_of_problem = nested_dict['type']
            
            try:
                number_of_classes = nested_dict['number_of_classes']
            
            except:
                # The number was not passed for a regression problem
                number_of_classes = 1
            
            # Get the output layer for that branch
            output_layer = self.network_branch (response_variable = response, type_of_problem = type_of_problem, number_of_classes = number_of_classes, architecture = architecture)
            
            # Append the output_layer to the list:
            outputs_list.append(output_layer)
            
            # When declaring the metrics as an object, they must be provided to the compile
            # method within a list:
            # https://www.tensorflow.org/api_docs/python/tf/keras/metrics/RootMeanSquaredError
            # or as the attribute ._name, which contains the correspondent string
        
            if (type_of_problem == 'regression'):    
                metrics = tf.keras.metrics.MeanAbsoluteError()
                # https://www.tensorflow.org/api_docs/python/tf/keras/metrics/MeanAbsoluteError
                loss = 'mse'
                # Add it to the losses and metrics dictionaries:
                # Concatenate "output_" since the names of the output layers start as this
                loss_dict[("output_" + response)] = loss
                metrics_dict[("output_" + response)] = metrics
                
            elif (type_of_problem == 'classification'):

                metrics = 'acc'
                
                if (number_of_classes == 2):
                    loss = 'binary_crossentropy'
                    # https://www.tensorflow.org/api_docs/python/tf/keras/metrics/BinaryCrossentropy
                else:
                    loss = 'sparse_categorical_crossentropy'
                    # https://www.tensorflow.org/api_docs/python/tf/keras/metrics/SparseCategoricalCrossentropy
                
                # Add it to the losses and metrics dictionaries:
                # Concatenate "output_" since the names of the output layers start as this
                loss_dict[("output_" + response)] = loss
                metrics_dict[("output_" + response)] = metrics
        
        # Now, compile the model
        
        # Set the optimizer:
        if (optimizer is None):
            # use Adam with default arguments
            # https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/Adam
            optimizer = tf.keras.optimizers.Adam()
        
        # define the model using the input and output layers
        """
        for multiple inputs, inputs should be a list, like in:
        model = Model(inputs=[input_a, input_b], outputs=[output, aux_output])
        for a single input, it can be simply the input layer used
        """
        
        # retrieve the inputs attribute, containing the list of inputs:
        # try accessing the attribute inputs:
        inputs = self.inputs
        
        model = tf.keras.models.Model(inputs = inputs, outputs = outputs_list, name = 'siamese_neural_net')
        
        model.compile(optimizer = optimizer, 
               loss = loss_dict,
               metrics = metrics_dict)
        
        if ControlVars.show_plots:
            print("Check model architecture:\n")
            tf.keras.utils.plot_model(model)
            print("\n")
        
        if ControlVars.show_results:
            print("Check model summary:\n")
            try:
                # only works in Jupyter Notebook:
                from IPython.display import display
                display(model.summary())
                        
            except: # regular mode
                print(model.summary())
        
        # Save as class attribute:
        self.model = model
        
        return self


class AnomalyDetector:
    """
    Class for creating a non-supervised learning algorithm used for anomaly detection.
    This class uses the same Sklearn API.

    def __init__ (self, epsilon = 0.00001)

    ### Gaussian distribution
        To perform anomaly detection, you will first need to fit a model to the data’s distribution.

        * Given a training set $\{x^{(1)}, ..., x^{(m)}\}$ you want to estimate the Gaussian distribution for each
        of the features $x_i$. 

        * Recall that the Gaussian distribution is given by

        $$ p(x ; \mu,\sigma ^2) = \frac{1}{\sqrt{2 \pi \sigma ^2}}\exp^{ - \frac{(x - \mu)^2}{2 \sigma ^2} }$$

        where $\mu$ is the mean and $\sigma^2$ is the variance.
        
        * For each feature $i = 1\ldots n$, you need to find parameters $\mu_i$ and $\sigma_i^2$ that fit the data in the 
        $i$-th dimension $\{x_i^{(1)}, ..., x_i^{(m)}\}$ (the $i$-th dimension of each example).

        ### Estimating parameters for a Gaussian distribution

        You can estimate the parameters, ($\mu_i$, $\sigma_i^2$), of the $i$-th
        feature by using the following equations. To estimate the mean, you will
        use:

        $$\mu_i = \frac{1}{m} \sum_{j=1}^m x_i^{(j)}$$

        and for the variance you will use:
        $$\sigma_i^2 = \frac{1}{m} \sum_{j=1}^m (x_i^{(j)} - \mu_i)^2$$
    """

    # This class uses the same Sklearn API

    # Initialize instance attributes.
    # define the Class constructor, i.e., how are its objects:
    def __init__ (self, epsilon = 0.00001):
        
        self.epsilon = epsilon 
    

    def fit (self, X):  
        """
        Calculates mean and variance of all features 
        in the dataset
        
        Args:
            X (ndarray): (m, n) Data matrix
        
        Returns:
            mu (ndarray): (n,) Mean of all features
            var (ndarray): (n,) Variance of all features
        """

        X = np.array(X)
        # Check if it is a single-dimension array
        if(len(X) == 1):
            #  Reshape it as a matrix
            # Put every array in matrix format [arr1, arr2, ... arr_n], where each array arr_i is a matrix row.
            X = X.reshape(-1,1)

        self.X = X
        self.m, self.n = X.shape
        # m rows and n columns
        n = self.n
        
        #start lists to store the arrays
        mu = [np.mean(X[:, j]) for j in range(0, n)]
        var = [np.var(X[:, j]) for j in range (0, n)]
        # compute for all rows from column j, where j is one of the columns from the dataset
        # https://numpy.org/doc/stable/reference/generated/numpy.var.html
        
        # Convert to numpy:
        self.mu = np.array(mu)
        self.var = np.array(var)

        return self
        

    def select_threshold (self, y_val, p_val): 
        """
        Finds the best threshold to use for selecting outliers 
        based on the results from a validation set (p_val) 
        and the ground truth (y_val)
        
        Args:
            y_val (ndarray): Ground truth on validation set - ytrue
            p_val (ndarray): Results on validation set
            
        Returns:
            epsilon (float): Threshold chosen 
            F1 (float):      F1 score by choosing epsilon as threshold
        
        
        Now that you have estimated the Gaussian parameters, you can investigate which examples have a very high probability given 
        this distribution and which examples have a very low probability.  

        * The low probability examples are more likely to be the anomalies in our dataset. 
        * One way to determine which examples are anomalies is to select a threshold based on a cross validation set. 

        In this section, you select the threshold $\varepsilon$ using the $F_1$ score on a cross validation set.

        * For this, we will use a cross validation set
        $\{(x_{\rm cv}^{(1)}, y_{\rm cv}^{(1)}),\ldots, (x_{\rm cv}^{(m_{\rm cv})}, y_{\rm cv}^{(m_{\rm cv})})\}$, 
        where the label $y=1$ corresponds to an anomalous example, and $y=0$ corresponds to a normal example. 
        * For each cross validation example, we will compute $p(x_{\rm cv}^{(i)})$. The vector of all of these probabilities 
        $p(x_{\rm cv}^{(1)}), \ldots, p(x_{\rm cv}^{(m_{\rm cv})})$ is passed to `select_threshold` in the vector `p_val`. 
        * The corresponding labels $y_{\rm cv}^{(1)}, \ldots, y_{\rm cv}^{(m_{\rm cv})}$ are passed to the same function in the 
        vector `y_val`.
        
        * In the provided code `select_threshold`, there is already a loop that will try many different values of $\varepsilon$ 
        and select the best $\varepsilon$ based on the $F_1$ score. 

        * You need to calculate the F1 score from choosing `epsilon` as the threshold and place the value in `F1`. 

        * Recall that if an example $x$ has a low probability $p(x) < \varepsilon$, then it is classified as an anomaly. 
                
        * Then, you can compute precision and recall by: 
        $$\begin{aligned}
        prec&=&\frac{tp}{tp+fp}\\
        rec&=&\frac{tp}{tp+fn},
        \end{aligned}$$ where
            * $tp$ is the number of true positives: the ground truth label says it’s an anomaly and our algorithm correctly classified 
            it as an anomaly.
            * $fp$ is the number of false positives: the ground truth label says it’s not an anomaly, but our algorithm incorrectly 
            classified it as an anomaly.
            * $fn$ is the number of false negatives: the ground truth label says it’s an anomaly, but our algorithm incorrectly 
            classified it as not being anomalous.

        * The $F_1$ score is computed using precision ($prec$) and recall ($rec$) as follows:
            $$F_1 = \frac{2\cdot prec \cdot rec}{prec + rec}$$ 

        **Implementation Note:** 
        In order to compute $tp$, $fp$ and $fn$, you may be able to use a vectorized implementation rather than loop over 
        all the examples.      
        """ 
        
        from sklearn.metrics import f1_score
        # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html
        
        best_epsilon = 0
        best_F1 = 0
        F1 = 0
        
        # Put every array in matrix format [arr1, arr2, ... arr_n], where each array arr_i is a matrix row.
        if(len(y_val.shape) == 1):
            #  Reshape it as a matrix
            y_val = y_val.reshape(-1,1)

        step_size = (max(p_val) - min(p_val)) / 1000
        
        # Create a vector of epsilons to be tested
        epsilons_tested = np.arange(min(p_val), max(p_val), step_size)
        # Create an array of f1_scores
        
        for epsilon in epsilons_tested:
            
            # Make an array with the boolean when comparing p_val with the selected epsilon
            y_pred = (p_val < epsilon).astype('int')
            # It will check every value from array p_val: if p_val > epsilon, we do not have an 
            # anomaly, so the response is zero (integer). If it is lower, the response is 1 (anomaly).
            # By setting the type, we guarantee it is an integer.
            # This array is saved as the predictions array y_pred
            
            F1 = f1_score(y_val, y_pred)
            # Inside the loop, we used a vectorized implementation
            
            if F1 > best_F1:
                best_F1 = F1
                best_epsilon = epsilon
        
       
        self.epsilon = best_epsilon
        self.F1 = best_F1

        return self


    def calculate_probabilities (self, X_tensor):
        """
        # Calculate probabilities for a tensor X
        
        Computes the probability 
        density function of the examples X under the multivariate gaussian 
        distribution with parameters mu and var. If var is a matrix, it is
        treated as the covariance matrix. If var is a vector, it is treated
        as the var values of the variances in each dimension (a diagonal
        covariance matrix
        """

        X = np.array(X_tensor)
        # Check if it is a single-dimension array
        if(len(X) == 1):
            #  Reshape it as a matrix
            # Put every array in matrix format [arr1, arr2, ... arr_n], where each array arr_i is a matrix row.
            X = X.reshape(-1,1)

        mu = self.mu
        var = self.var
        
        k = len(mu)
        
        if var.ndim == 1:
            var = np.diag(var)
            
        X = X - mu
        p = (2* np.pi)**(-k/2) * np.linalg.det(var)**(-0.5) * \
            np.exp(-0.5 * np.sum(np.matmul(X, np.linalg.pinv(var)) * X, axis = 1))
        
        self.estimated_probabilities = p

        # Put every array in matrix format [arr1, arr2, ... arr_n], where each array arr_i is a matrix row.
        if(len(p.shape) == 1):
            #  Reshape it as a matrix
            p = p.reshape(-1,1)
    
        return self


    def predict (self, X_tensor):

        epsilon = self.epsilon
        # Calculate the probabilities associated to X_tensor:
        self = self.calculate_probabilities(X_tensor = X_tensor)
        # Retrieve the probabilities:
        p = self.estimated_probabilities

        # Find the outliers in the training set 
        outliers = (p < epsilon)
        # Convert to numpy array
        outliers = np.array(outliers)
        # Change type from boolean to integer:
        outliers = outliers.astype('int64')
        # Now, True values (p lower than epsilon) are labelled as 1; False (p >= epsilon) are
        # labelled as 0.

        # Return the predictions:
        return outliers


    def save (self, path_to_save):

        import pickle

        #Save the dictionary of attributes:
        attributes = vars(self)
        with open(path_to_save, 'wb') as opened_file:
            pickle.dump(attributes, opened_file)
