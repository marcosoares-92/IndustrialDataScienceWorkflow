# FUNCTIONS FROM INDUSTRIAL DATA SCIENCE WORKFLOW (IDSW) PACKAGE
# Modelling and Machine Learning

# Marco Cesar Prado Soares, Data Scientist Specialist @ Bayer Crop Science LATAM
# marcosoares.feq@gmail.com
# marco.soares@bayer.com


class model_checking:
            
    # Initialize instance attributes.
    # define the Class constructor, i.e., how are its objects:
    def __init__(self, model_object = None, model_type = 'regression', model_package = 'tensorflow', column_map_dict = None, training_history_object = None, X = None, y_train = None, y_preds_for_train = None, y_test = None, y_preds_for_test = None, y_valid = None, y_preds_for_validation = None):
        
        import numpy as np
        import tensorflow as tf

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
        
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        import tensorflow as tf
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

                        print(f"Metrics for {key}:\n")
                        mse = mean_squared_error(y_true, y_pred)

                        # Print in scientific notation:
                        try:
                            print(f"Mean squared error (MSE) = {mse:e}")
                        except:
                            print(f"Mean squared error (MSE) = {mse}")
                        # Add to calculated metrics:
                        calculated_metrics['mse'] = mse

                        rmse = mse**(1/2)

                        try:
                            print(f"Root mean squared error (RMSE) = {rmse:e}")
                        except:
                            print(f"Root mean squared error (RMSE) = {rmse}")
                        # Add to calculated metrics:
                        calculated_metrics['rmse'] = rmse

                        mae = mean_absolute_error(y_true, y_pred)

                        # Print in scientific notation:
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
                        try:
                            print(f"Mean absolute percentage error (MAPE) = {mape:e}")
                        except:
                            print(f"Mean absolute percentage error (MAPE) = {mape}")
                        # Add to calculated metrics:
                        calculated_metrics['mape'] = mape

                        r2 = r2_score(y_true, y_pred)

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

                        try:
                            print(f"Adjusted coefficient of correlation R²-adj = {r2_adj:e}")
                        except:
                            print(f"Adjusted coefficient of correlation R²-adj = {r2_adj}")

                        # Add to calculated metrics:
                        calculated_metrics['r_squared_adj'] = r2_adj

                        explained_var = explained_variance_score(y_true, y_pred)
                        # Print in scientific notation:
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

                        print(f"Metrics for {key}:\n")

                        auc = roc_auc_score(y_true, y_pred)

                        try:
                            print(f"AUC = {auc:e}")
                        except:
                            print(f"AUC = {auc}")
                        # Add to calculated metrics:
                        calculated_metrics['auc'] = auc

                        acc = accuracy_score(y_true, y_pred)

                        try:
                            print(f"Accuracy = {acc:e}")
                        except:
                            print(f"Accuracy = {acc}")
                        # Add to calculated metrics:
                        calculated_metrics['accuracy'] = acc

                        precision = precision_score(y_true, y_pred)

                        try:
                            print(f"Precision = {precision:e}")
                        except:
                            print(f"Precision = {precision}")
                        # Add to calculated metrics:
                        calculated_metrics['precision'] = precision

                        recall = recall_score(y_true, y_pred)

                        try:
                            print(f"Recall = {recall:e}")
                        except:
                            print(f"Recall = {recall}")
                        # Add to calculated metrics:
                        calculated_metrics['recall'] = recall

                        # The method update_state returns None, so it must be called without and equality

                        # Get the classification report:
                        print("\n")
                        print("Classification Report:\n")
                        # Convert tensors to NumPy arrays
                        report = classification_report (y_true, y_pred)
                        print(report)
                        # Add to calculated metrics:
                        calculated_metrics['classification_report'] = report
                        print("\n")

                        # Get the confusion matrix:
                        # Convert tensors to NumPy arrays
                        matrix = confusion_matrix (y_true, y_pred)
                        # Add to calculated metrics:
                        calculated_metrics['confusion_matrix'] = report
                        print("Confusion matrix:\n")

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
                
                except:
                    print(f"Unable to retrieve metrics for {key}:\n")
                    metrics_dict[key] = {'metrics': f'No metrics retrieved for {key}'}
          
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

    def plot_training_history (self, metrics_name = 'mean_absolute_error', x_axis_rotation = 0, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, metrics_vertical_axis_title = None, loss_vertical_axis_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):

        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt

        # metrics_name = 'mse', 'sparse_categorical_crossentropy', etc

        history = self.history
        # Set the validation metrics name.
        # to access the validation metrics, simply put a 'val_' prefix:
        val_metrics_name = 'val_' + metrics_name

        # Retrieve data from the history dictionary:
        # Access values for training sample:
        train_metrics = history.history[metrics_name]
        
        # Try accessing data from validation sample (may not be present):
        has_validation = False
        # Maps if there are validation data: this variable is updated when values are present.
        
        try:
            validation_metrics = history.history[val_metrics_name]
            train_loss = history.history['loss']
            validation_loss = history.history['val_loss']
            has_validation = True
        
        except: # simply pass
            pass
        
        # Notice that history is not exactly a dictionary: it is an object with attribute history.
        # This attribute is where the dictionary is actually stored.
        
        # Access the list of epochs, stored as the epoch attribute from the history object
        list_of_epochs = history.epoch
        # epochs start from zero
        
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
        
        except:
            print("Unable to plot training history.\n")
            
    
    def plot_history_multiresponses (self, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, metrics_vertical_axis_title = None, loss_vertical_axis_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):

        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt

        # metrics_name = 'mse', 'sparse_categorical_crossentropy', etc

        history = self.history
        
        """
        history object has a format like (2 responses, 1 epoch, metrics = 'mse'), when we apply the
        .__dict__ method:

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
            
            try:
                metrics_name = nested_dict['metrics']

                # Set the validation metrics name.
                # to access the validation metrics, simply put a 'val_' prefix:
                val_metrics_name = 'val_' + metrics_name
            
            except:
                pass
            
            try:
                train_loss = nested_dict['loss']
                
                if (has_validation):
                    validation_loss = nested_dict['val_loss']
            except:
                pass
            
            try:
                train_metrics = nested_dict[metrics_name]
                
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
                try:
                    ax1 = fig.add_subplot(211)
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

                except:
                    pass

                try:
                    ax2 = fig.add_subplot(212)
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

                except:
                    pass

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
                print("\n")
        
            except:
                print(f"Unable to plot training history for {response}.\n")
            
    
    def model_metrics_multiresponses (self, output_dictionary, show_confusion_matrix_values = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
        
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        import tensorflow as tf
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
                print(f"Metrics for {key}:\n")
                
                nested_metrics = {}
                
                for index, response in enumerate(list_of_responses):
                    
                    if (total_data > 0):
                    
                        # enumerate will get tuples like (0, response1), (1, response2), etc
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

                                print(f"Metrics for {key}:\n")
                                mse = mean_squared_error(y_true, y_pred)

                                # Print in scientific notation:
                                try:
                                    print(f"Mean squared error (MSE) = {mse:e}")
                                except:
                                    print(f"Mean squared error (MSE) = {mse}")
                                # Add to calculated metrics:
                                calculated_metrics['mse'] = mse

                                rmse = mse**(1/2)

                                try:
                                    print(f"Root mean squared error (RMSE) = {rmse:e}")
                                except:
                                    print(f"Root mean squared error (RMSE) = {rmse}")
                                # Add to calculated metrics:
                                calculated_metrics['rmse'] = rmse

                                mae = mean_absolute_error(y_true, y_pred)

                                # Print in scientific notation:
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
                                try:
                                    print(f"Mean absolute percentage error (MAPE) = {mape:e}")
                                except:
                                    print(f"Mean absolute percentage error (MAPE) = {mape}")
                                # Add to calculated metrics:
                                calculated_metrics['mape'] = mape

                                r2 = r2_score(y_true, y_pred)

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

                                try:
                                    print(f"Adjusted coefficient of correlation R²-adj = {r2_adj:e}")
                                except:
                                    print(f"Adjusted coefficient of correlation R²-adj = {r2_adj}")

                                # Add to calculated metrics:
                                calculated_metrics['r_squared_adj'] = r2_adj

                                explained_var = explained_variance_score(y_true, y_pred)
                                # Print in scientific notation:
                                try:
                                    print(f"Explained variance = {explained_var:e}")

                                except:
                                    print(f"Explained variance = {explained_var}")

                                # Explained variance is similar to the R² score, goes from 0 to 1, with the notable 
                                # difference that it does not account for systematic offsets in the prediction.
                                calculated_metrics['explained_variance'] = explained_var

                                print("\n")

                            else:

                                print(f"Metrics for {key}:\n")

                                auc = roc_auc_score(y_true, y_pred)

                                try:
                                    print(f"AUC = {auc:e}")
                                except:
                                    print(f"AUC = {auc}")
                                # Add to calculated metrics:
                                calculated_metrics['auc'] = auc

                                acc = accuracy_score(y_true, y_pred)

                                try:
                                    print(f"Accuracy = {acc:e}")
                                except:
                                    print(f"Accuracy = {acc}")
                                # Add to calculated metrics:
                                calculated_metrics['accuracy'] = acc

                                precision = precision_score(y_true, y_pred)

                                try:
                                    print(f"Precision = {precision:e}")
                                except:
                                    print(f"Precision = {precision}")
                                # Add to calculated metrics:
                                calculated_metrics['precision'] = precision

                                recall = recall_score(y_true, y_pred)

                                try:
                                    print(f"Recall = {recall:e}")
                                except:
                                    print(f"Recall = {recall}")
                                # Add to calculated metrics:
                                calculated_metrics['recall'] = recall

                                # The method update_state returns None, so it must be called without and equality

                                # Get the classification report:
                                print("\n")
                                print("Classification Report:\n")
                                # Convert tensors to NumPy arrays
                                report = classification_report (y_true, y_pred)
                                print(report)
                                # Add to calculated metrics:
                                calculated_metrics['classification_report'] = report
                                print("\n")

                                # Get the confusion matrix:
                                # Convert tensors to NumPy arrays
                                matrix = confusion_matrix (y_true, y_pred)
                                # Add to calculated metrics:
                                calculated_metrics['confusion_matrix'] = report
                                print("Confusion matrix:\n")

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
        
        import numpy as np
        import pandas as pd

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
    
    # original algorithm:
    # https://www.tensorflow.org/tutorials/structured_data/time_series?hl=en&%3Bauthuser=1&authuser=1
  
    def __init__(self, dataset, shift, use_past_responses_for_prediction = True, 
                 sequence_stride = 1, sampling_rate = 1, label_columns = None, 
                 train_pct = 70, val_pct = 10):
        
        import numpy as np
        import pandas as pd
        import tensorflow as tf
        
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
        
        import numpy as np
        import tensorflow as tf
        
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


class tf_models:
    
    # TensorFlow models with single input, single output, or single input and possibly
    # 1 regression and 1 classification output
    # Use preferentially for these situations
    
    def __init__(self, X_train, y_train, X_valid = None, y_valid = None, type_of_problem = 'regression', number_of_classes = 2, optimizer = None):
        
        # type_of_problem = 'regression', 'classification', 'both'
        # optimizer: tf.keras.optimizers.Optimizer object:
        # https://www.tensorflow.org/api_docs/python/tf/keras/optimizers
        # https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/Optimizer
        # use the object to set parameters such as learning rate and selection of the optimizer
        
        import tensorflow as tf
        
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
    
    
    def compile_model(self):
        
        import tensorflow as tf
        
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
            
            
            print("Check model architecture:\n")
            tf.keras.utils.plot_model(model)
            print("\n")
            
            # Compile model:
            model.compile(optimizer = optimizer,
                          loss = {'output_classification': loss_classification,
                                  'output_regression': loss_regression},
                          metrics = {'output_classification': metrics_classification,
                                    'output_regression': metrics_regression})
        
        
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
    
    def fit_model(self, epochs = 2000, batch_size = 200, verbose = 1):
        
        import tensorflow as tf
        
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
        
        import tensorflow as tf

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
 
        import tensorflow as tf

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
        
        import tensorflow as tf

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
        
        import tensorflow as tf
        
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
        
        import tensorflow as tf
        
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
        
        import numpy as np
        import tensorflow as tf
        
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


class siamese_networks:
    
    # TensorFlow models for multiple responses. The neural networks are replicated for each one
    # of the responses
    
    def __init__(self, output_dictionary, X_train, y_train, X_valid = None, y_valid = None):
        
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
        
        import numpy as np
        import pandas as pd
        import tensorflow as tf
        
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
    
    
    def fit_model(self, epochs = 2000, batch_size = 200, verbose = 1):
        
        import tensorflow as tf
        
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
        
        import tensorflow as tf
        
        # First hidden layer:
        x = tf.keras.layers.Dense(units = 128, activation = 'relu', name = ('dense_1'+ '_' + response))(input_layer)
        
        return x
    
    
    def base_model_double_dense (self, input_layer, response):
        
        import tensorflow as tf
        
        # First hidden layer:
        x = tf.keras.layers.Dense(units = 128, activation = 'relu', name = ('dense_1' + '_' + response))(input_layer)
        x = tf.keras.layers.Dense(units = 128, activation = 'relu', name = ('dense_2' + '_' + response))(x)
            
        return x
    
    
    def base_model_cnn_time_series (self, input_layer, response):
        
        import tensorflow as tf
        
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
        
        import tensorflow as tf
        
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
        
        import tensorflow as tf
        
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
        
        import numpy as np
        import tensorflow as tf
        
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
        
        import tensorflow as tf
        
        # architecture = 'simple_dense': base_model_simple_dense from class siamese_networks;
        # architecture = 'double_dense': base_model_double_dense from class siamese_networks;
        # architecture = 'cnn': base_model_cnn_time_series from class siamese_networks;
        # architecture = 'lstm': base_model_lstm_time_series from class siamese_networks;
        # architecture = 'encoder_decoder': base_model_encoder_decoder_time_series from class siamese_networks;
        # architecture = 'cnn_lstm': hybrid base_model_cnn_lstm_time_series from class siamese_networks.
        
        
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
        
        import numpy as np
        import pandas as pd
        import tensorflow as tf
        
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
        
        print("Check model architecture:\n")
        tf.keras.utils.plot_model(model)
        print("\n")
        
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
    if ((type(features_columns) != list) & (type(features_columns) != tuple)):
        #put inside a list:
        features_columns = [features_columns]
    
    elif (type(features_columns) == tuple):
        features_columns = list(features_columns)

    if ((type(response_columns) != list) & (type(response_columns) != tuple)):
        #put inside a list:
        response_columns = [response_columns]
    
    elif (type(response_columns) == tuple):
        response_columns = list(response_columns)

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


def convert_to_tensor (df_or_array_to_convert, columns_to_convert = None, columns_to_exclude = None):

    import numpy as np
    import pandas as pd

    try:
        import tensorflow as tf
    except:
        pass
    # https://www.tensorflow.org/api_docs/python/tf/Tensor

    # columns_to_convert: list of strings or string containing the names of columns
    # that you want to convert. Use this if you want to convert only a subset of the dataframe. 
    # Example: columns_to_convert = ['col1', 'col2']; columns_to_convert = 'predictor';
    # columns_to_convert = ['predictor'] will create a tensor with only the specified columns;
    # If None, the whole dataframe will be converted.
    # ATTENTION: This argument only works for Pandas dataframes.
    
    # columns_to_exclude: Alternative parameter. 
    # list of strings or string containing the names of columns that you want to exclude from the
    # returned tensor. Use this if you want to convert only a subset of the dataframe. 
    # Example: columns_to_exclude = ['col1', 'col2']; columns_to_exclude = 'predictor';
    # columns_to_exclude = ['predictor'] will create a tensor with all columns from the dataframe
    # except the specified ones. This argument will only be used if the previous one was not.
    # ATTENTION: This argument only works for Pandas dataframes.

    try:
        # Set a local copy of the dataframe to manipulate:
        DATASET = df_or_array_to_convert.copy(deep = True)

        if (columns_to_convert is not None):
            # Subset the dataframe:
            # Check if features_columns and response_columns are lists:
            if ((type(columns_to_convert) != list) & (type(columns_to_convert) != tuple)):
                #put inside a list:
                columns_to_convert = [columns_to_convert]
            
            elif (type(columns_to_convert) == tuple):
                columns_to_convert = list(columns_to_convert)

            # Now, filter the dataframe:
            DATASET = DATASET[columns_to_convert]

        elif (columns_to_exclude is not None):
            # Run only if the dataframe was not subset:
            if ((type(columns_to_exclude) != list) & (type(columns_to_exclude) != tuple)):
                #put inside a list:
                columns_to_exclude = [columns_to_exclude]
            
            elif (type(columns_to_exclude) == tuple):
                columns_to_exclude = list(columns_to_exclude)
            
            # Drop the columns:
            DATASET = DATASET.drop(columns_to_exclude, axis = 1)
    
    except:
        # It is an array or iterable:
        DATASET = np.array(df_or_array_to_convert)
        
        if (len(DATASET.shape) == 1):
            # It is a tuple like (1,) - array like [1, 2, 3,...]
            DATASET =  DATASET.reshape(-1, 1)
            # Now, its format is like [[1], [2], [3],...] - shape like (4, 1)

    # Try the conversion to tensor. Since the values should not be modified, we
    # will create the tensors as tf.constant, instead of tf.Variable:
    try:

        X = tf.constant(DATASET)

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
        X = np.array(DATASET)
        
    print("Check the 5 first elements from the tensor or array obtained:\n")
    print(X[:5])
    print("\n")
    print(f"Shape of the complete X tensor or array = {X.shape}\n")
    # shape attribute is common to tf.Tensor, pd.DataFrame, pd.Series, and np.array

    # Notice that tensors and arrays are sliced in the same way as lists.
    # The slicing also modify the shape attribute from Tensors.
    # We can convert a tf.Tensor object named tensor to a np.array object by
    # simply making array = np.array(tensor) 

    # Now, since the arrays do not have a column header, let's create a mapping dictionary, correlating
    # the array position with the original column name:
    column_map_dict = {}
    try:
        
        for column_number, column in enumerate(list(DATASET.columns)):
            # The enumerate object created from a list can be decoupled into two values:
            # The index (number) - position in the list, and the element itself. example:
            # 0, 'first_column':
            # Add it to the features dictionary, with the column number as key:
            column_map_dict[column_number] = column

        print("The mapping of the arrays' positions with the columns original names was returned as 'column_map_dict'.")
    
    except:
        pass
    
    return X, column_map_dict


def split_data_into_train_and_test (X, y, percent_of_data_used_for_model_training = 75, percent_of_training_data_used_for_model_validation = 0):
    
    import random
    import numpy as np
    import tensorflow as tf
    
    # X = tensor or array of predictive variables.
    # y = tensor or array of response variables.
    
    # percent_of_data_used_for_model_training: float from 0 to 100,
    # representing the percent of data used for training the model
    
    # If you want to use cross-validation, separate a percent of the training data for validation.
    # Declare this percent as percent_of_training_data_used_for_model_validation (float from 0 to 100).
    
    # Convert to tuples to save memory:
    X = tuple(np.array(X))
    y = tuple(np.array(y))
    
    # Convert the percent to fraction.
    train_fraction = (percent_of_data_used_for_model_training / 100)
    
    if (train_fraction > 1):
        train_fraction = 1
    
    elif (train_fraction < 0):
        train_fraction = 0
    
    # Convert the percent of validation to fraction:
    validation_fraction = (percent_of_training_data_used_for_model_validation / 100)
    if (validation_fraction > 1):
        validation_fraction = 1
    
    elif (validation_fraction < 0):
        validation_fraction = 0
    
    # Calculate the test fraction:
    test_fraction = (1 - train_fraction - validation_fraction)
    
    try:
        assert test_fraction >= 0
        assert train_fraction + test_fraction + validation_fraction == 1
    
    except:
        if ((train_fraction + validation_fraction) > 1):
            if (train_fraction == 1):
                validation_fraction = 0
                test_fraction = 0
            
            else:
                test_fraction = (1 - train_fraction)
                validation_fraction = 0
    
    if (train_fraction == 1):
        X_train, y_train = np.array(X), np.array(y)
        X_test, y_test = np.array([]), np.array([])
        X_valid, y_valid = np.array([]), np.array([])
    
    elif (validation_fraction == 0):
        X_valid, y_valid = np.array([]), np.array([])
    
    if (train_fraction < 1):
        # Create a list of indices:
        indices = [i for i in range(0, len(X))]
        # Shuffle the indices:
        random.shuffle(indices)

        total_indices = len(indices)
        total_for_training = int(np.rint(train_fraction*total_indices))

        # Set the indexes used for training:
        train_idx, other_idx = indices[:total_for_training], indices[total_for_training:]
        if (validation_fraction == 0):
            test_idx = other_idx
            valid_idx = []

        else:
            total_for_testing = int(np.rint(test_fraction*total_indices))
            test_idx, valid_idx = other_idx[:total_for_testing], indices[total_for_testing:]
    
        
        # Now, create the lists of splitted elements
        # [element for ... if ...]
        X_train = [X[i] for i in train_idx]
        y_train = [y[i] for i in train_idx]
        X_train, y_train = np.array(X_train), np.array(y_train)
        X_train, y_train = tf.constant(X_train), tf.constant(y_train)
        
        X_test = [X[i] for i in test_idx]
        y_test = [y[i] for i in test_idx]
        X_test, y_test = np.array(X_test), np.array(y_test)
        X_test, y_test = tf.constant(X_test), tf.constant(y_test)
        
        if (len(valid_idx) > 0):
            X_valid = [X[i] for i in valid_idx]
            y_valid = [y[i] for i in valid_idx]
            X_valid, y_valid = np.array(X_valid), np.array(y_valid)
            X_valid, y_valid = tf.constant(X_valid), tf.constant(y_valid)
            
    
    print(f"X and y successfully splitted into train: X_train, y_train ({train_fraction*100:.1f}% of data); test: X_test, y_test ({test_fraction*100:.1f}% of data); and validation subsets: X_valid, y_valid ({validation_fraction*100:.1f}% of data).")
    
    split_dictionary = {'X_train': X_train, 'y_train': y_train, 'X_test': X_test, 'y_test': y_test, 'X_valid': X_valid, 'y_valid': y_valid}
    
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


def multi_columns_time_series_tensors (df, response_columns, sequence_stride = 1, sampling_rate = 1, shift = 1, use_past_responses_for_prediction = True, percent_of_data_used_for_model_training = 70, percent_of_training_data_used_for_model_validation = 10):

    # original algorithm: 
    # https://www.tensorflow.org/tutorials/structured_data/time_series?hl=en&%3Bauthuser=1&authuser=1
    
    import numpy as np
    import pandas as pd
    import tensorflow as tf
    
    # response_columns: string or list of strings with the response columns
    
    # The time series may be represented as a sequence of times like: t = 0, t = 1, t = 2, ..., t = N.
    # When preparing the dataset, we pick a given number of 'times' (indexes), and use them for
    # predicting a time in the future.
    # So, the input_width represents how much times will be used for prediction. If input_width = 6,
    # we use 6 values for prediction, e.g., t = 0, t = 1, ..., t = 5 will be a prediction window.
    # In turns, if input_width = 3, 3 values are used: t = 0, t = 1, t = 2; if input_width = N, N
    # consecutive values will be used: t = 0, t = 1, t = 2, ..., t = N. And so on.
    # label_width, in turns, represent how much times will be predicted. If label_width = 1, a single
    # value will be predicted. If label_width = 2, two consecutive values are predicted; if label_width =
    # N, N consecutive values are predicted; and so on.
    
    # shift, sampling_rate, and sequence_stride: integers
    
    # shift represents the offset, i.e., given the input values, which value in the time sequence will
    # be predicted. So, suppose input_width = 6 and label_width = 1
    # If shift = 1, the label, i.e., the predicted value, will be the first after the sequence used for
    # prediction. So, if  t = 0, t = 1, ..., t = 5 will be a prediction window and t = 6 will be the
    # predicted value. Notice that the complete window has a total width = 7: t = 0, ..., t = 7. 
    # If label_width = 2, then t = 6 and t = 7 will be predicted (total width = 8).
    # Another example: suppose input_width = 24. So the predicted window is: t = 0, t = 1, ..., t = 23.
    # If shift = 24, the 24th element after the prediction sequence will be used as label, i.e., will
    # be predicted. So, t = 24 is the 1st after the sequence, t = 25 is the second, ... t = 47 is the
    # 24th after. If label_with = 1, then the sequence t = 0, t = 1, ..., t = 23 will be used for
    # predicting t = 47. Naturally, the total width of the window = 47 in this case.
    
    # Also, notice that the label is used by the model as the response (predicted) variable.
    
    # So for a given shift: the sequence of timesteps i, i+1, ... will be used for predicting the
    # timestep i + shift
    # If a sequence starts in index i, the next sequence will start from i + sequence_stride.
    # The sequence will be formed by timesteps i, i + sampling_rate, i + 2* sampling_rate, ...
    # Example: Consider indices [0, 1, ... 99]. With sequence_length=10, sampling_rate=2, 
    # sequence_stride=3, the dataset will yield batches of sequences composed of the following 
    # indices:
    # First sequence:  [0  2  4  6  8 10 12 14 16 18]
    # Second sequence: [3  5  7  9 11 13 15 17 19 21]
    # Third sequence:  [6  8 10 12 14 16 18 20 22 24]
    # ...
    # Last sequence:   [78 80 82 84 86 88 90 92 94 96]

    # percent_of_data_used_for_model_training: float from 0 to 100,
    # representing the percent of data used for training the model
    
    # If you want to use cross-validation, separate a percent of the training data for validation.
    # Declare this percent as percent_of_training_data_used_for_model_validation (float from 0 to 100).
    
    # If PERCENT_OF_DATA_USED_FOR_MODEL_TRAINING = 70, and 
    # PERCENT_OF_TRAINING_DATA_USED_FOR_MODEL_VALIDATION = 10, 
    # training dataset slice goes from 0 to 0.7 (70%) of the dataset;
    # testing slicing goes from 0.7 x dataset to ((1 - 0.1) = 0.9) x dataset
    # validation slicing goes from 0.9 x dataset to the end of the dataset.
    # Here, consider the time sequence t = 0, t = 1, ... , t = N, for a dataset with length N:
    # training: from t = 0 to t = (0.7 x N); testing: from t = ((0.7 x N) + 1) to (0.9 x N);
    # validation: from t = ((0.9 x N) + 1) to N (the fractions 0.7 x N and 0.9 x N are rounded to
    # the closest integer).
    
    # use_past_responses_for_prediction: True if the past responses will be used for predicting their
    # value in the future; False if you do not want to use them.

    
    # Create a local copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    
    # Instantiate an object from WindowGenerator class:
    w = WindowGenerator (dataset = DATASET, shift = shift, use_past_responses_for_prediction = use_past_responses_for_prediction, sequence_stride = sequence_stride, sampling_rate = sampling_rate, label_columns = response_columns, train_pct = percent_of_data_used_for_model_training, val_pct = percent_of_training_data_used_for_model_validation)
    # Make the tensors:
    w = w.make_tensors()
    # Retrieve tensors dictionary:
    tensors_dict = w.tensors_dict

    print("Finished preparing the time series datasets for training, testing, and validation. Check their shapes.\n")
    
    for key in tensors_dict.keys():
        
        print(f"{key}-tensors obtained:")
        nested_dict = tensors_dict[key]
        print(f"Inputs tensor shape = {nested_dict['inputs'].shape}")
        print(f"Labels tensor shape = {nested_dict['labels'].shape}\n")
    
    return tensors_dict


def union_1_dim_tensors (list_of_tensors_or_arrays):
    
    # list of tensors: list containing the 1-dimensional tensors or arrays that the function will union.
    # the operation will be performed in the order that the tensors are declared.
    # One-dimensional tensors have shape (X,), where X is the number of elements. Example: a column
    # of the dataframe with elements 1, 2, 3 in this order may result in an array like array([1, 2, 3])
    # and a Tensor with shape (3,). With we union it with the tensor from the column with elements
    # 4, 5, 6, the output will be array([[1,4], [2,5], [3,6]]). Alternatively, this new array could
    # be converted into a Pandas dataframe where each column would be correspondent to one individual
    # tensor.
    
    import numpy as np
    import pandas as pd
    import tensorflow as tf
    
    # Convert each element from the list to a numpy array, in case they are tensors:
    list_of_arrays = [np.array(tensor) for tensor in list_of_tensors_or_arrays]
    
    # Now, stack all elements from list_of_arrays into a single array, using the columns' axis
    # (axis = 1).
    # https://numpy.org/doc/stable/reference/generated/numpy.stack.html
    
    """
    Example: suppose a = np.array([1, 2, 3]), b = np.array([4, 5, 6]), c = np.array([7, 8, 9])
    If we do np.stack([a,b,c], axis = 1), the resultant will be array([[1, 4, 7],[2, 5, 8],[3, 6, 9]]),
    what would be converted into a dataframe where each original tensor would correspond to a column.
    
    On the other hand, by doing np.stack([a,b,c], axis = 0), the resultant would be array([[1, 2, 3],
    [4, 5, 6],[7, 8, 9]]) - in a dataframe originated from this array, each original tensor would
    correspond to a row.
    """
    stacked_array = np.stack(list_of_arrays, axis = 1)
    
    # Finally, convert it to tensor and return it:
    tensors_union = tf.constant(stacked_array)
    
    # Notice that this operation is equivalent to firstly converting all to tensors and then performing:
    # tf.stack([a,b,c], axis = 1), where [a, b, c] is a list of tensors a, b, c (substitute it by
    # list_of_tensors).
    
    print("Tensors union complete. Check the resulting tensor below:\n")
    print(tensors_union)
    
    return tensors_union


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
    
    # Sklearn requires a 1-dimensional vector for training the classifier.
    """
            y_train tensor original format:
                <tf.Tensor: shape=(87, 1), dtype=float64, numpy=
                array([[1.],
                    [0.], ....,
                    [0.]])>
            
            Reshape to unidimensional format. First step:
            y_train.numpy().reshape(1, -1)
            Now, it has format:
                array([[1., 0.,..., 0.]]), shape = (1, 87)
                (if we make reshape(-1, 1), we turn it again to the original tensor format)
            
            Notice that we want only the internal 1-dimensional array (with 87 values in the example)
            # So we make:
            y_train[0] to select only it.
    """
            
    y_train = np.array(y_train).reshape(1, -1)
    # This array has format([[val1, val2, ...]]) - i.e., it has two dimensions. Let's pick
    # only the first array:
    y_train = y_train[0]
    
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
    model_check = model_check.feature_importance_ranking (model_class = 'linear', orientation = orientation, horizontal_axis_title = horizontal_axis_title, vertical_axis_title = vertical_axis_title, plot_title = plot_title, x_axis_rotation = x_axis_rotation, y_axis_rotation = y_axis_rotation, grid = grid, export_png = export_png, directory_to_save = directory_to_save, file_name = file_name, png_resolution_dpi = png_resolution_dpi)
    # Retrieve the feature importance ranking:
    feature_importance_df = model_check.feature_importance_df
    
    print("\n") #line break
    print("To predict the model output y_pred for a dataframe X, declare: y_pred = ols_linear_reg_model.predict(X)\n")
    print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
    print("X_train = np.reshape(np.array(X_train), (-1, 1))")
    # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362
    
    return ols_linear_reg_model, metrics_dict, feature_importance_df


def ridge_linear_reg (X_train, y_train, alpha_hyperparameter = 0.001, maximum_of_allowed_iterations = 20000, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    # check Scikit-learn documentation: 
    # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html#sklearn.linear_model.Ridge
    # This function runs the 'bar_chart' function. Certify that this function was properly loaded.
    
    """
    The regularizer tends to bring the coefficients to zero: the model will behave as a constant line 
    for higher regularization terms.
    - The Regularization term can be either:
        - Lasso: absolute value of the coefficients.
            - Force the coefficients of the regression to zero.
        - Ridge: square of the coefficients.
            - Bring the coefficients of the regression closer to zero.
        - Elastic net: combination of Ridge and Lasso.

        - Both shrink the coefficients related to unimportant predictors.

    - Regularization term `alpha`:
        - `alpha = 0`: no regularization (standard regression);
        - `alpha tending to infinite`: complete regularization (all coefficients to zero).
            - Regression becomes a constant line.

        - If all coefficients are different from zero, all variables are being considered important for the prediction.
        - The regularizer may bring coefficients to zero, selecting those which are effectively the most important parameters.

    """
    
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
    
    # The regularizer tends to bring all coefficients of the regression to zero, i.e., with higher
    # regularization terms, the model can become a constant line. On the other hand, it reduces the
    # impact of high-coefficient features like X^4, reducing overfitting (high variance problem).
    
    # So, apply low regularizers, like 0.001, specially if the data was previously normalized. alpha=1
    # may bring the equivalence to a constant line (underfitting, high bias problem).
    
    
    RANDOM_STATE = 55 
    ## We will pass it to every sklearn call so we ensure reproducibility (i.e., a new random process)
    
    # Create an instance (object) from the class Ridge:
    # Pass the appropriate parameters to the class constructor:
    ridge_linear_reg_model = Ridge(alpha = alpha_hyperparameter, max_iter = maximum_of_allowed_iterations, random_state = RANDOM_STATE)
    
    # Sklearn requires a 1-dimensional vector for training the classifier.
    """
            y_train tensor original format:
                <tf.Tensor: shape=(87, 1), dtype=float64, numpy=
                array([[1.],
                    [0.], ....,
                    [0.]])>
            
            Reshape to unidimensional format. First step:
            y_train.numpy().reshape(1, -1)
            Now, it has format:
                array([[1., 0.,..., 0.]]), shape = (1, 87)
                (if we make reshape(-1, 1), we turn it again to the original tensor format)
            
            Notice that we want only the internal 1-dimensional array (with 87 values in the example)
            # So we make:
            y_train[0] to select only it.
    """
            
    y_train = np.array(y_train).reshape(1, -1)
    # This array has format([[val1, val2, ...]]) - i.e., it has two dimensions. Let's pick
    # only the first array:
    y_train = y_train[0]
    
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
    model_check = model_check.feature_importance_ranking (model_class = 'linear', orientation = orientation, horizontal_axis_title = horizontal_axis_title, vertical_axis_title = vertical_axis_title, plot_title = plot_title, x_axis_rotation = x_axis_rotation, y_axis_rotation = y_axis_rotation, grid = grid, export_png = export_png, directory_to_save = directory_to_save, file_name = file_name, png_resolution_dpi = png_resolution_dpi)
    # Retrieve the feature importance ranking:
    feature_importance_df = model_check.feature_importance_df
    
    print("\n") #line break
    print("To predict the model output y_pred for a dataframe X, declare: y_pred = ridge_linear_reg_model.predict(X)\n")
    print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
    print("X_train = np.reshape(np.array(X_train), (-1, 1))")
    # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362
    
    return ridge_linear_reg_model, metrics_dict, feature_importance_df


def lasso_linear_reg (X_train, y_train, alpha_hyperparameter = 0.001, maximum_of_allowed_iterations = 20000, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    # check Scikit-learn documentation: 
    # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html#sklearn.linear_model.Lasso
    # This function runs the 'bar_chart' function. Certify that this function was properly loaded.
    
    """
    The regularizer tends to bring the coefficients to zero: the model will behave as a constant line 
    for higher regularization terms.
    - The Regularization term can be either:
        - Lasso: absolute value of the coefficients.
            - Force the coefficients of the regression to zero.
        - Ridge: square of the coefficients.
            - Bring the coefficients of the regression closer to zero.
        - Elastic net: combination of Ridge and Lasso.

        - Both shrink the coefficients related to unimportant predictors.

    - Regularization term `alpha`:
        - `alpha = 0`: no regularization (standard regression);
        - `alpha tending to infinite`: complete regularization (all coefficients to zero).
            - Regression becomes a constant line.

        - If all coefficients are different from zero, all variables are being considered important for the prediction.
        - The regularizer may bring coefficients to zero, selecting those which are effectively the most important parameters.

    """
    
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
    
    # The regularizer tends to bring all coefficients of the regression to zero, i.e., with higher
    # regularization terms, the model can become a constant line. On the other hand, it reduces the
    # impact of high-coefficient features like X^4, reducing overfitting (high variance problem).
    
    # So, apply low regularizers, like 0.001, specially if the data was previously normalized. alpha=1
    # may bring the equivalence to a constant line (underfitting, high bias problem).
    
    
    RANDOM_STATE = 55 
    ## We will pass it to every sklearn call so we ensure reproducibility (i.e., a new random process)
    
    # Create an instance (object) from the class Lasso:
    # Pass the appropriate parameters to the class constructor:
    lasso_linear_reg_model = Lasso(alpha = alpha_hyperparameter, max_iter = maximum_of_allowed_iterations, random_state = RANDOM_STATE)
    # verbose = True to debug mode (show training status during training)
    
    # Sklearn requires a 1-dimensional vector for training the classifier.
    """
            y_train tensor original format:
                <tf.Tensor: shape=(87, 1), dtype=float64, numpy=
                array([[1.],
                    [0.], ....,
                    [0.]])>
            
            Reshape to unidimensional format. First step:
            y_train.numpy().reshape(1, -1)
            Now, it has format:
                array([[1., 0.,..., 0.]]), shape = (1, 87)
                (if we make reshape(-1, 1), we turn it again to the original tensor format)
            
            Notice that we want only the internal 1-dimensional array (with 87 values in the example)
            # So we make:
            y_train[0] to select only it.
    """
            
    y_train = np.array(y_train).reshape(1, -1)
    # This array has format([[val1, val2, ...]]) - i.e., it has two dimensions. Let's pick
    # only the first array:
    y_train = y_train[0]
    
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
    model_check = model_check.feature_importance_ranking (model_class = 'linear', orientation = orientation, horizontal_axis_title = horizontal_axis_title, vertical_axis_title = vertical_axis_title, plot_title = plot_title, x_axis_rotation = x_axis_rotation, y_axis_rotation = y_axis_rotation, grid = grid, export_png = export_png, directory_to_save = directory_to_save, file_name = file_name, png_resolution_dpi = png_resolution_dpi)
    # Retrieve the feature importance ranking:
    feature_importance_df = model_check.feature_importance_df
    
    print("\n") #line break
    print("To predict the model output y_pred for a dataframe X, declare: y_pred = lasso_linear_reg_model.predict(X)\n")
    print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
    print("X_train = np.reshape(np.array(X_train), (-1, 1))")
    # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362
    
    return lasso_linear_reg_model, metrics_dict, feature_importance_df


def elastic_net_linear_reg (X_train, y_train, alpha_hyperparameter = 0.001, l1_ratio_hyperparameter = 0.02, maximum_of_allowed_iterations = 20000, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    # check Scikit-learn documentation: 
    # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNet.html#sklearn.linear_model.ElasticNet
    # This function runs the 'bar_chart' function. Certify that this function was properly loaded.
    
    """
    The regularizer tends to bring the coefficients to zero: the model will behave as a constant line 
    for higher regularization terms.
    - The Regularization term can be either:
        - Lasso: absolute value of the coefficients.
            - Force the coefficients of the regression to zero.
        - Ridge: square of the coefficients.
            - Bring the coefficients of the regression closer to zero.
        - Elastic net: combination of Ridge and Lasso.

        - Both shrink the coefficients related to unimportant predictors.

    - Regularization term `alpha`:
        - `alpha = 0`: no regularization (standard regression);
        - `alpha tending to infinite`: complete regularization (all coefficients to zero).
            - Regression becomes a constant line.

        - If all coefficients are different from zero, all variables are being considered important for the prediction.
        - The regularizer may bring coefficients to zero, selecting those which are effectively the most important parameters.

    """
    
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
    # Currently, l1_ratio <= 0.01 is not reliable, unless you supply your own sequence of alpha.
    
    # alpha = 0 and l1_ratio = 0 is equivalent to an ordinary least square, solved by 
    # the LinearRegression object. For numerical reasons, using alpha = 0 and 
    # l1_ratio = 0 is not advised. Given this, you should use the ols_linear_reg function instead.
    
    # The regularizer tends to bring all coefficients of the regression to zero, i.e., with higher
    # regularization terms, the model can become a constant line. On the other hand, it reduces the
    # impact of high-coefficient features like X^4, reducing overfitting (high variance problem).
        
    # So, apply low regularizers, like 0.001, specially if the data was previously normalized. alpha=1
    # may bring the equivalence to a constant line (underfitting, high bias problem).
    
    
    RANDOM_STATE = 55 
    ## We will pass it to every sklearn call so we ensure reproducibility (i.e., a new random process)
    
    # Create an instance (object) from the class ElasticNet:
    # Pass the appropriate parameters to the class constructor:
    elastic_net_linear_reg_model = ElasticNet(alpha = alpha_hyperparameter, l1_ratio = l1_ratio_hyperparameter, max_iter = maximum_of_allowed_iterations, random_state = RANDOM_STATE)
    # verbose = True to debug mode (show training status during training)
    
    # Sklearn requires a 1-dimensional vector for training the classifier.
    """
            y_train tensor original format:
                <tf.Tensor: shape=(87, 1), dtype=float64, numpy=
                array([[1.],
                    [0.], ....,
                    [0.]])>
            
            Reshape to unidimensional format. First step:
            y_train.numpy().reshape(1, -1)
            Now, it has format:
                array([[1., 0.,..., 0.]]), shape = (1, 87)
                (if we make reshape(-1, 1), we turn it again to the original tensor format)
            
            Notice that we want only the internal 1-dimensional array (with 87 values in the example)
            # So we make:
            y_train[0] to select only it.
    """
            
    y_train = np.array(y_train).reshape(1, -1)
    # This array has format([[val1, val2, ...]]) - i.e., it has two dimensions. Let's pick
    # only the first array:
    y_train = y_train[0]
    
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
    model_check = model_check.feature_importance_ranking (model_class = 'linear', orientation = orientation, horizontal_axis_title = horizontal_axis_title, vertical_axis_title = vertical_axis_title, plot_title = plot_title, x_axis_rotation = x_axis_rotation, y_axis_rotation = y_axis_rotation, grid = grid, export_png = export_png, directory_to_save = directory_to_save, file_name = file_name, png_resolution_dpi = png_resolution_dpi)
    # Retrieve the feature importance ranking:
    feature_importance_df = model_check.feature_importance_df
    
    print("\n") #line break
    print("To predict the model output y_pred for a dataframe X, declare: y_pred = elastic_net_linear_reg_model.predict(X)\n")
    print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
    print("X_train = np.reshape(np.array(X_train), (-1, 1))")
    # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362
    
    return elastic_net_linear_reg_model, metrics_dict, feature_importance_df


def logistic_reg (X_train, y_train, regularization = 'l2', l1_ratio_hyperparameter = 0.02, maximum_of_allowed_iterations = 20000, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    # check Scikit-learn documentation: 
    # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html?msclkid=6bede8a8c1a011ecad332ec5eb711355
    # This function runs the 'bar_chart' function. Certify that this function was properly loaded.
    
    """
    The regularizer tends to bring the coefficients to zero: the model will behave as a constant line 
    for higher regularization terms.
    - The Regularization term can be either:
        - Lasso: absolute value of the coefficients.
            - Force the coefficients of the regression to zero.
        - Ridge: square of the coefficients.
            - Bring the coefficients of the regression closer to zero.
        - Elastic net: combination of Ridge and Lasso.

        - Both shrink the coefficients related to unimportant predictors.

    - Regularization term `alpha`:
        - `alpha = 0`: no regularization (standard regression);
        - `alpha tending to infinite`: complete regularization (all coefficients to zero).
            - Regression becomes a constant line.

        - If all coefficients are different from zero, all variables are being considered important for the prediction.
        - The regularizer may bring coefficients to zero, selecting those which are effectively the most important parameters.

    """
    
    import numpy as np
    import pandas as pd
    import tensorflow as tf
    from sklearn.linear_model import LogisticRegression
    
    # X_train = subset of predictive variables (dataframe).
    # y_train = subset of response variable (series).

    # MAXIMUM_OF_ALLOWED_ITERATIONS = integer representing the maximum number of iterations
    # that the optimization algorithm can perform. Depending on data, convergence may not be
    # reached within this limit, so you may need to increase this hyperparameter.
    # REGULARIZATION is the norm of the penalty:
    # REGULARIZATION = None: no penalty is added; REGULARIZATION = 'l2': add a L2 penalty term and 
    # it is the default choice; REGULARIZATION = 'l1': add a L1 penalty term; 
    # REGULARIZATION = 'elasticnet': both L1 and L2 penalty terms are added.
    
    # The regularizer tends to bring all coefficients of the regression to zero, i.e., with higher
    # regularization terms, the model can become a constant line. On the other hand, it reduces the
    # impact of high-coefficient features like X^4, reducing overfitting (high variance problem).        
    # So, apply low regularizers, like 0.001, specially if the data was previously normalized. alpha=1
    # may bring the equivalence to a constant line (underfitting, high bias problem).
    # L1_RATIO_HYPERPARAMETER is The ElasticNet mixing parameter (float), with 0 <= l1_ratio <= 1. 
    # For L1_RATIO_HYPERPARAMETER = 0 the penalty is an L2 penalty. For l1_ratio = 1 it is an L1 penalty. 
    # For 0 < L1_RATIO_HYPERPARAMETER < 1, the penalty is a combination of L1 and L2.
    
    # Currently, l1_ratio <= 0.01 is not reliable, unless you supply your own sequence of alpha.
    
    print("Attention: logistic regression is a binary classifier. It results in probabilities, instead of on scalar (real numbers) like other regression algorithms from linear models class.\n")
    
    
    RANDOM_STATE = 55 
    ## We will pass it to every sklearn call so we ensure reproducibility (i.e., a new random process)
    
    # Instantiate a model checker object to verify if there are only two classes:
    check_classes = model_checking()
    # Use the vars function to access the attributes dictionary and set the value from y_train:
    # Make sure that it is a tensor, so that it can use .numpy method:
    vars(check_classes)['y_train'] = tf.constant(y_train)
    # Retrieve the classes:
    check_classes = check_classes.retrieve_classes_used_for_training()
    # Retrieve the attributes:
    number_of_classes = check_classes.number_of_classes
    list_of_classes = check_classes.list_of_classes
    
    # Create a dictionary to return:
    classes_dict = {'list_of_classes': list_of_classes,
                    'number_of_classes': number_of_classes}
    
    if (number_of_classes == 2):
        # Logistic regression can be obtained for only two classes.
        # Since the number of classes is correct, we can proceed.
        
        # Pass the appropriate parameters to the class constructor:
        logistic_reg_model = LogisticRegression(penalty = regularization, max_iter = maximum_of_allowed_iterations, random_state = RANDOM_STATE, l1_ratio = l1_ratio_hyperparameter)
        # verbose = 1 to debug mode is not available for 'saga' solver

        # Fit the model:
        # Sklearn logistic regression requires a 1-dimensional vector for training.
        """
        y_train tensor original format:
            <tf.Tensor: shape=(87, 1), dtype=float64, numpy=
            array([[1.],
                [0.], ....,
                [0.]])>
        
        Reshape to unidimensional format. First step:
        y_train.numpy().reshape(1, -1)
        Now, it has format:
            array([[1., 0.,..., 0.]]), shape = (1, 87)
            (if we make reshape(-1, 1), we turn it again to the original tensor format)
        
        Notice that we want only the internal 1-dimensional array (with 87 values in the example)
        # So we make:
        y_train[0] to select only it.
        """
        
        reshaped_y_train = np.array(y_train).reshape(1, -1)
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
        
        # Calculate model metrics:
        model_check = model_check.model_metrics()
        # Retrieve model metrics:
        metrics_dict = model_check.metrics_dict

        # Get feature importance ranking:
        model_check = model_check.feature_importance_ranking (model_class = 'linear', orientation = orientation, horizontal_axis_title = horizontal_axis_title, vertical_axis_title = vertical_axis_title, plot_title = plot_title, x_axis_rotation = x_axis_rotation, y_axis_rotation = y_axis_rotation, grid = grid, export_png = export_png, directory_to_save = directory_to_save, file_name = file_name, png_resolution_dpi = png_resolution_dpi)
        # Retrieve the feature importance ranking:
        feature_importance_df = model_check.feature_importance_df

        print("\n") #line break
        print("To predict the model output y_pred for a dataframe X, declare: y_pred = logistic_reg_model.predict(X)\n")
        print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
        print("X_train = np.reshape(np.array(X_train), (-1, 1))")
        # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362

        print("To predict the probabilities associated to each class for the set X_train, use the .predict_proba(X) method:")
        print("y_pred_probabilities = logistic_reg_model.predict_proba(X_train)")

        return logistic_reg_model, metrics_dict, feature_importance_df, classes_dict
    
    else:
        print("Unable to perform logistic regression.")
        print(f"Found a total of {number_of_classes} in the training tensor: {list_of_classes}\n")
        
        return None, None, None, classes_dict


def RANDOM_FOREST (X_train, y_train, type_of_problem = "regression", number_of_trees = 128, max_tree_depth = 20, min_samples_to_split_node = 2, min_samples_to_make_leaf = 2, bootstrap_samples = True, use_out_of_bag_error = True, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    # This function runs the 'bar_chart' function. Certify that this function was properly loaded.
    # check Random Forest documentation on Scikit-learn:
    # https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html
    # Check explanaining of out-of-bag error:
    # https://scikit-learn.org/stable/auto_examples/ensemble/plot_ensemble_oob.html
    
    """
    - Bagging ensemble of decision trees.
    - Data is divided and sampled. Trees are trained simultaneously, giving no preference to a given subset.
        - With bagging, some instances may be subject to sampling several times in each predictor, while others may not.
        - By default, a Bagging Classifier samples m training instances with replacement (bootstrap = True), where m is the training size. It means that, on average, only 63% of training instances are sampled by each predictor.
        - The 37% remaining training instances are called out-of-bag (oob) samples, and the 37% are not the same for all predictors. Once the predictor is not exposed to such instances during training, it may be evaluated with them with no need of a separated validation set.
        - The ensemble itself may be evaluated as the average of each predictor regarding the oob evaluations.
    """
    import numpy as np
    import pandas as pd
    
    RANDOM_STATE = 55 
    ## We will pass it to every sklearn call so we ensure reproducibility (i.e., a new random process)
    
    # X_train = subset of predictive variables (dataframe).
    # y_train = subset of response variable (series).
    
    # TYPE_OF_PROBLEM = 'regression'; or TYPE_OF_PROBLEM = 'classification'
    # The default is 'regression', which will be used if no type is
    # provided.
    
    # NUMBER_OF_TREES = 128 (integer) - number of trees in the forest
    # it is the n_estimators parameter of the model.
    # Usually, a number from 64 to 128 is used.

    # MAX_TREE_DEPTH = 20 - integer representing the maximum depth 
    # permitted for the trees (base learners). If None, then nodes are expanded 
    # until all leaves are pure or until all leaves contain less 
    # than MIN_SAMPLES_TO_SPLIT_NODE samples.
    # it is the max_depth parameter of the model.

    # MIN_SAMPLES_TO_SPLIT_NODE = 2 (integer or float). It is the 
    # min_samples_split parameter of the model.
    # The minimum number of samples required to split an internal node:
    # If int, then consider MIN_SAMPLES_TO_SPLIT_NODE as the minimum number.
    # If float, then MIN_SAMPLES_TO_SPLIT_NODE is a fraction and ceil
    # (MIN_SAMPLES_TO_SPLIT_NODE * NUMBER_OF_TREES) are the minimum number 
    # of samples for each split.

    # MIN_SAMPLES_TO_MAKE_LEAF = 2 (integer or float). It is the
    # min_samples_leaf parameter of the model.
    # The minimum number of samples required to be at a leaf node. 
    # A split point at any depth will only be considered if it leaves at 
    # least MIN_SAMPLES_TO_MAKE_LEAF training samples in each of the left and right branches. 
    # This may have the effect of smoothing the model, especially in regression.
    # If int, then consider MIN_SAMPLES_TO_MAKE_LEAF as the minimum number.
    # If float, then MIN_SAMPLES_TO_MAKE_LEAF is a fraction and ceil
    # (MIN_SAMPLES_TO_MAKE_LEAF * NUMBER_OF_TREES) are the minimum number 
    # of samples for each node.
    
    # bootstrap_samples = True. Parameter bootstrap of the model.
    # Whether bootstrap samples are used when building trees. If False, 
    # the whole dataset is used to build each tree.
    
    # USE_OUT_OF_BAG_ERROR = True. Parameter oob_score of the model.
    # Whether to use out-of-bag (OOB) samples to estimate the generalization score. 
    # Only available if BOOTSTRAP_SAMPLES = True.
        
    # Importantly: random forest combines several decision trees, by randomnly selecting
    # variables for making the tree leafs and nodes; and ramdonly setting the depth of
    # the trees. The use of out-of-bag guarantees that the data used for the construction
    # of the trees is randomly selected.
    # If not using, the calculated metrics will be over estimated.
    # This phenomenon is characteristic from ensemble algorithms like random forests, and
    # is not usually observed on linear regressions.
    
    # Start a summary dictionary:
    summary_dict = {}
    
    # check if use_out_of_bag_error = True but bootstrap_samples is False:
    if ((bootstrap_samples == False) & (use_out_of_bag_error == True)):
        
        print("Out-of-bag errors can only be used when bootstrap is True. Then, changing the value of bootstrap_samples.")
        
        bootstrap_samples = True
    
    if (type_of_problem == "regression"):
        
        from sklearn.ensemble import RandomForestRegressor
        # Create an instance (object) from the class RandomForestRegressor()
        # Pass the appropriate parameters to the class constructor:
        rf_model = RandomForestRegressor(n_estimators = number_of_trees, random_state = RANDOM_STATE, max_depth = max_tree_depth, min_samples_split = min_samples_to_split_node, min_samples_leaf = min_samples_to_make_leaf, bootstrap = bootstrap_samples, oob_score = use_out_of_bag_error)
        # verbose = 1 for debug mode (show training process details)
        
    elif (type_of_problem == "classification"):
        
        from sklearn.ensemble import RandomForestClassifier
        # Instantiate a model checker object to verify if there are only two classes:
        check_classes = model_checking()
        # Use the vars function to access the attributes dictionary and set the value from y_train:
        # Make sure that it is a tensor, so that it can use .numpy method:
        vars(check_classes)['y_train'] = tf.constant(y_train)
        # Retrieve the classes:
        check_classes = check_classes.retrieve_classes_used_for_training()
        # Retrieve the attributes:
        number_of_classes = check_classes.number_of_classes
        list_of_classes = check_classes.list_of_classes
        
        # Create a dictionary to return:
        classes_dict = {'list_of_classes': list_of_classes,
                        'number_of_classes': number_of_classes}
        
        # Store it in the summary dictionary:
        summary_dict['classes'] = classes_dict
        
        # Create an instance (object) from the class RandomForestClassifier()
        # Pass the appropriate parameters to the class constructor:
        rf_model = RandomForestClassifier(n_estimators = number_of_trees, random_state = RANDOM_STATE, max_depth = max_tree_depth, min_samples_split = min_samples_to_split_node, min_samples_leaf = min_samples_to_make_leaf, bootstrap = bootstrap_samples, oob_score = use_out_of_bag_error)
        # verbose = 1 for debug mode (show training process details)

        
    else:
        
        print ("Enter a valid type of problem, \'regression\' or \'classification\'.")
        return "error"
    
    # Sklearn requires a 1-dimensional vector for training the classifier.
    """
        y_train tensor original format:
            <tf.Tensor: shape=(87, 1), dtype=float64, numpy=
            array([[1.],
                [0.], ....,
                [0.]])>
        
        Reshape to unidimensional format. First step:
        y_train.numpy().reshape(1, -1)
        Now, it has format:
            array([[1., 0.,..., 0.]]), shape = (1, 87)
            (if we make reshape(-1, 1), we turn it again to the original tensor format)
        
        Notice that we want only the internal 1-dimensional array (with 87 values in the example)
        # So we make:
        y_train[0] to select only it.
    """
        
    reshaped_y_train = np.array(y_train).reshape(1, -1)
    # This array has format([[val1, val2, ...]]) - i.e., it has two dimensions. Let's pick
    # only the first array:
    reshaped_y_train = reshaped_y_train[0]
    
    rf_model = rf_model.fit(X_train, reshaped_y_train)
    
    
    if (use_out_of_bag_error): # runs only if the boolean is True
        
        print("OOB Score: score of the training dataset obtained using an out-of-bag estimate = ")
        print(rf_model.oob_score_)
        print("\n")
    
    # Get predictions for training, testing, and validation:
    y_preds_for_train = rf_model.predict(X_train)

    if ((X_test is not None) & ((y_test is not None))):
        y_preds_for_test = rf_model.predict(X_test)

    else:
        y_preds_for_test = None

    if ((X_valid is not None) & ((y_valid is not None))):
        y_preds_for_validation = rf_model.predict(X_valid)

    else:
        y_preds_for_validation = None

    # instantiate the model checker object:
    model_check = model_checking(model_object = rf_model, model_type = type_of_problem, model_package = 'sklearn', column_map_dict = column_map_dict, X = X_train, y_train = y_train, y_preds_for_train = y_preds_for_train, y_test = y_test, y_preds_for_test = y_preds_for_test, y_valid = y_valid, y_preds_for_validation = y_preds_for_validation)
        
    # Calculate model metrics:
    model_check = model_check.model_metrics()
    # Retrieve model metrics:
    metrics_dict = model_check.metrics_dict
    
    # Store the metrics dictionary in the summary dictionary:
    summary_dict['metrics_dict'] = metrics_dict

    # Get feature importance ranking:
    model_check = model_check.feature_importance_ranking (model_class = 'tree', orientation = orientation, horizontal_axis_title = horizontal_axis_title, vertical_axis_title = vertical_axis_title, plot_title = plot_title, x_axis_rotation = x_axis_rotation, y_axis_rotation = y_axis_rotation, grid = grid, export_png = export_png, directory_to_save = directory_to_save, file_name = file_name, png_resolution_dpi = png_resolution_dpi)
    # Retrieve the feature importance ranking:
    feature_importance_df = model_check.feature_importance_df
    
    # Store the importance ranking in the summary dictionary:
    summary_dict['feature_importance_df'] = feature_importance_df
    
    print("\n") #line break
    print("To reveal the decision path in the forest for a sample X, call the .decision_path method of the random forest model object. For example, declare:")
    print("path = rf_model.decision_path(X)")
    print("And then print path.")
    
    print("\n") #line break
    print("To predict the model output y_pred for a dataframe X, declare: y_pred = rf_model.predict(X)\n")
    print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
    print("X_train = np.reshape(np.array(X_train), (-1, 1))")
    # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362
    
    if (type_of_problem == 'classification'):
        
        print("To predict the probabilities associated to each class for the set X_train, use the .predict_proba(X) method:")
        print("y_pred_probabilities = rf_model.predict_proba(X_train)")

    return rf_model, summary_dict


def XGBOOST (X_train, y_train, type_of_problem = "regression", number_of_trees = 128, max_tree_depth = None, percent_of_training_set_to_subsample = 75, X_test = None, y_test = None, X_valid = None, y_valid = None, column_map_dict = None, orientation = 'vertical', horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    """
    - Boosting ensemble of decision trees.
    - Each new tree is trained preferentially with data for which the previous trees had difficulty on making good predictions (i.e., these data receives higher weights of importance).
    - This algorithm usally performs better than Random Forests.
    """

    # This function runs the 'bar_chart' function. Certify that this function was properly loaded.
    # check XGBoost documentation:
    # https://xgboost.readthedocs.io/en/stable/python/python_api.html?highlight=xgbregressor#xgboost.XGBRegressor

    import numpy as np
    import pandas as pd
    
    RANDOM_STATE = 55 
    ## We will pass it to every sklearn call so we ensure reproducibility (i.e., a new random process)
        
    # X_train = subset of predictive variables (dataframe).
    # y_train = subset of response variable (series).
    
    # TYPE_OF_PROBLEM = 'regression'; or TYPE_OF_PROBLEM = 'classification'
    # The default is 'regression', which will be used if no type is
    # provided.
    
    # number_of_trees = 128 (integer) - number of gradient boosted trees. 
    # Equivalent to number of boosting rounds.
    # it is the n_estimators parameter of the model.
    # Usually, a number from 64 to 128 is used.
    
    # max_tree_depth = None - integer representing the maximum depth 
    # permitted for the trees (base learners).
    
    # percent_of_training_set_to_subsample = 75 (float or None).
    # If this value is set, it defines the percent of data that will be ramdonly
    # selected for training the models.
    # e.g. percent_of_training_set_to_subsample = 80 uses 80% of the data. If None,
    # it uses the whole training set (100%)
    
    ## When subsampling, training data is divided into several subsets, and these
    # subsets are used for separately training the model.
    # Importantly: random forest and XGBoost combine several decision trees, by randomnly selecting
    # variables for making the tree leafs and nodes; and ramdonly setting the depth of
    # the trees. The use of this strategy guarantees that the data used for the construction
    # of the trees is randomly selected.
    # If not using, the model will be highly susceptive of overfitting due to the use of
    # the whole dataset. Also, the calculated metrics will be over estimated.
    # This phenomenon is characteristic from ensemble algorithms like random forests, and
    # XGBoost, and is not usually observed on linear regressions.
    
    # Start a summary dictionary:
    summary_dict = {}
    
    # check if percent_of_training_set_to_subsample is between 0 and 100%:
    if (0 <= percent_of_training_set_to_subsample <= 100):
        
        # convert the percent into the fraction_to_subsample
        fraction_to_subsample = (percent_of_training_set_to_subsample)/100
    
    else:
        # None or invalid value was provided
        print("None or invalid percent of dataset to subsample was provided. Then, the whole training set will be used.")
        
        fraction_to_subsample = 1.0 #total fraction, set as float
    
    if (type_of_problem == "regression"):

        from xgboost import XGBRegressor
        # Create an instance (object) from the class RandomForestRegressor()
        # Pass the appropriate parameters to the class constructor:
        xgb_model = XGBRegressor(n_estimators = number_of_trees, random_state = RANDOM_STATE, max_depth = max_tree_depth, subsample = fraction_to_subsample)
        # verbosity = 3 for debug mode (show training details)
        
    elif (type_of_problem == "classification"):
        
        from xgboost import XGBClassifier
        # Instantiate a model checker object to verify if there are only two classes:
        check_classes = model_checking()
        # Use the vars function to access the attributes dictionary and set the value from y_train:
        # Make sure that it is a tensor, so that it can use .numpy method:
        vars(check_classes)['y_train'] = tf.constant(y_train)
        # Retrieve the classes:
        check_classes = check_classes.retrieve_classes_used_for_training()
        # Retrieve the attributes:
        number_of_classes = check_classes.number_of_classes
        list_of_classes = check_classes.list_of_classes
        
        # Create a dictionary to return:
        classes_dict = {'list_of_classes': list_of_classes,
                        'number_of_classes': number_of_classes}
        
        # Store it in the summary dictionary:
        summary_dict['classes'] = classes_dict
        
        # Create an instance (object) from the class RandomForestClassifier()
        # Pass the appropriate parameters to the class constructor:
        xgb_model = XGBClassifier(n_estimators = number_of_trees, random_state = RANDOM_STATE, max_depth = max_tree_depth, subsample = fraction_to_subsample)
        # verbosity = 3 for debug mode (show training details)
        
    else:
        
        print ("Enter a valid type of problem, \'regression\' or \'classification\'.")
        return "error"
    
    
    # XGBoost requires a 1-dimensional vector for training the classifier.
    """
        y_train tensor original format:
            <tf.Tensor: shape=(87, 1), dtype=float64, numpy=
            array([[1.],
                [0.], ....,
                [0.]])>
        
        Reshape to unidimensional format. First step:
        y_train.numpy().reshape(1, -1)
        Now, it has format:
            array([[1., 0.,..., 0.]]), shape = (1, 87)
            (if we make reshape(-1, 1), we turn it again to the original tensor format)
        
        Notice that we want only the internal 1-dimensional array (with 87 values in the example)
        # So we make:
        y_train[0] to select only it.
    """
        
    reshaped_y_train = np.array(y_train).reshape(1, -1)
    # This array has format([[val1, val2, ...]]) - i.e., it has two dimensions. Let's pick
    # only the first array:
    reshaped_y_train = reshaped_y_train[0]
    
    xgb_model = xgb_model.fit(X_train, reshaped_y_train)
    
    
    # Get predictions for training, testing, and validation:
    y_preds_for_train = xgb_model.predict(X_train)

    if ((X_test is not None) & ((y_test is not None))):
        y_preds_for_test = xgb_model.predict(X_test)

    else:
        y_preds_for_test = None

    if ((X_valid is not None) & ((y_valid is not None))):
        y_preds_for_validation = xgb_model.predict(X_valid)

    else:
        y_preds_for_validation = None

    # instantiate the model checker object:
    model_check = model_checking(model_object = xgb_model, model_type = type_of_problem, model_package = 'xgboost', column_map_dict = column_map_dict, X = X_train, y_train = y_train, y_preds_for_train = y_preds_for_train, y_test = y_test, y_preds_for_test = y_preds_for_test, y_valid = y_valid, y_preds_for_validation = y_preds_for_validation)
        
    # Calculate model metrics:
    model_check = model_check.model_metrics()
    # Retrieve model metrics:
    metrics_dict = model_check.metrics_dict
    
    # Store the metrics dictionary in the summary dictionary:
    summary_dict['metrics_dict'] = metrics_dict

    # Get feature importance ranking:
    model_check = model_check.feature_importance_ranking (model_class = 'tree', orientation = orientation, horizontal_axis_title = horizontal_axis_title, vertical_axis_title = vertical_axis_title, plot_title = plot_title, x_axis_rotation = x_axis_rotation, y_axis_rotation = y_axis_rotation, grid = grid, export_png = export_png, directory_to_save = directory_to_save, file_name = file_name, png_resolution_dpi = png_resolution_dpi)
    # Retrieve the feature importance ranking:
    feature_importance_df = model_check.feature_importance_df
    
    # Store the importance ranking in the summary dictionary:
    summary_dict['feature_importance_df'] = feature_importance_df
    
    
    print("\n") #line break
    print("To predict the model output y_pred for a dataframe X, declare: y_pred = xgb_model.predict(X)\n")
    print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
    print("X_train = np.reshape(np.array(X_train), (-1, 1))")
    # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362
    
    if (type_of_problem == 'classification'):
        
        print("To predict the probabilities associated to each class for the set X_train, use the .predict_proba(X) method:")
        print("y_pred_probabilities = xgb_model.predict_proba(X_train)")

    return xgb_model, summary_dict


def SKLEARN_ANN (X_train, y_train, type_of_problem = "regression", number_of_hidden_layers = 1, number_of_neurons_per_hidden_layer = 64, size_of_training_batch = 200, maximum_of_allowed_iterations = 20000, X_test = None, y_test = None, X_valid = None, y_valid = None, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, metrics_vertical_axis_title = None, loss_vertical_axis_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    # check MLPRegressor documentation on Scikit-learn:
    # https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html?msclkid=b835e54ec17b11eca3d8febbc0eaeb3a
    # check MLPClassifier documentation on Scikit-learn:
    # https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html?msclkid=ecb380ebc17b11ec99b7b8f762c84eab
    
    import numpy as np
    import pandas as pd
    
    # X_train = subset of predictive variables (dataframe).
    # y_train = subset of response variable (series).
    
    # TYPE_OF_PROBLEM = 'regression'; or TYPE_OF_PROBLEM = 'classification'
    # The default is 'regression', which will be used if no type is
    # provided.
    
    # number_of_hidden_layers = 1 - integer with the number of hidden
    # layers. This number must be higher or equal to 1.
    
    # number_of_neurons_per_hidden_layer = 64 - integer containing the
    # number of neurons in each hidden layer. Even though sklearn.neural_network
    # accepts different layers sizes, passed as a list of integers where each
    # value represents the neurons for one layer, this function works with layers
    # of equal sizes.
    
    # Scikit-learn MLPClassifier adjusts the size of the output layer to have
    # a number of units (neurons) equals to the number of output classes. Then, we
    # do not have to manually set this parameter.
    
    # size_of_training_batch (integer): amount of data used on each training cycle (epoch). 
    # If we had 20000 data and size_of_training_batch = 200, then there would be 100 
    # batches (cycles) using 200 data. Training is more efficient when dividing the data into 
    # smaller subsets (batches) of ramdonly chosen data and separately training the model
    # for each batch (in training cycles called epochs). Also, this helps preventing
    # overfitting: if we use at once all data, the model is much more prone to overfit
    # (memorizing effect), selecting non-general features highly specific from the data
    # for the description of it. Therefore, it will have lower capability of predicting
    # data for values it already did not observe.
    # This is the parameter batch_size of most of the algorithms.
    
    # MAXIMUM_OF_ALLOWED_ITERATIONS = integer representing the maximum number of iterations
    # that the optimization algorithm can perform. Depending on data, convergence may not be
    # reached within this limit, so you may need to increase this hyperparameter.
    
    
    # 1. Let's configure the hidden layers. They are input as the parameter hidden_layer_sizes
    # if only one value is provided, there will be only one hidden layer
    # for more hidden layers, provide a list in hidden_layer_sizes. Each element
    # of this list will be the number of neurons in each layer. Examples:
    # hidden_layer_sizes  = 100 - a single hidden layer with 100 neurons
    # hidden_layer_sizes=[100, 100] - 2 hidden layers with 100 neurons per layer
    # hidden_layer_sizes=[100, 100, 100] - 3 hidden layers with 100 neurons per layer.
    
    RANDOM_STATE = 55 
    ## We will pass it to every sklearn call so we ensure reproducibility (i.e., a new random process)
        
    
    if (number_of_hidden_layers == 1):
        
        # Simply copy the value input as number_of_neurons_per_hidden_layer
        HIDDEN_LAYER_SIZES = number_of_neurons_per_hidden_layer
        print(f"Multi-Layer Perceptron configured with a single hidden-layer containing {number_of_neurons_per_hidden_layer} neurons.")
    
    elif (number_of_hidden_layers > 1):
        
        # Start a list HIDDEN_LAYER_SIZES
        HIDDEN_LAYER_SIZES = [number_of_neurons_per_hidden_layer for i in range (0, number_of_hidden_layers)]
        # This list must have number of elements equals to number_of_hidden_layers
        # (i.e. one element per layer)
        
        print(f"Multi-Layer Perceptron configured with {number_of_hidden_layers} hidden-layers containing {number_of_neurons_per_hidden_layer} neurons.")

    else:
        
        print("Please, input a valid number of hidden layers. It must be an integer higher or equal to 1.")
        return "error"
    
    
    if (type_of_problem == "regression"):

        from sklearn.neural_network import MLPRegressor
        # Create an instance (object) from the class MLPRegressor()
        # Pass the appropriate parameters to the class constructor:
        mlp_model = MLPRegressor(hidden_layer_sizes = HIDDEN_LAYER_SIZES, activation = 'relu', solver = 'adam', batch_size = size_of_training_batch, max_iter = maximum_of_allowed_iterations, verbose = True, random_state = RANDOM_STATE)
        # 'relu' = ReLU, the Rectified Linear Unit function, returns f(x) = max(0, x)
        # (i.e., if x <=0, relu(x) = 0; if (x > 0), relu(x) = 0)
        # 'identity' or 'linear' is equivalent to the use of no-activation function (no-op activation)
        # It is useful to implement linear bottleneck - returns f(x) = x
        # use no activation function (in other words, 'linear' activation) for the output layer of a
        # regression problem.
        
        # verbose: sklearn default is False. Whether to print progress messages to stdout.
        
    elif (type_of_problem == "classification"):

        from sklearn.neural_network import MLPClassifier
        # Create an instance (object) from the class MLPClassifier()
        # Pass the appropriate parameters to the class constructor:
        mlp_model = MLPClassifier(hidden_layer_sizes = HIDDEN_LAYER_SIZES, activation = 'relu', solver = 'adam', batch_size = size_of_training_batch, max_iter = maximum_of_allowed_iterations, verbose = True, random_state = RANDOM_STATE)
    
    else:
        
        print ("Enter a valid type of problem, \'Regression\' or \'Classification\'.")
        return "error"
    
    
    # Sklearn requires a 1-dimensional vector for training the classifier.
    """
            y_train tensor original format:
                <tf.Tensor: shape=(87, 1), dtype=float64, numpy=
                array([[1.],
                    [0.], ....,
                    [0.]])>
            
            Reshape to unidimensional format. First step:
            y_train.numpy().reshape(1, -1)
            Now, it has format:
                array([[1., 0.,..., 0.]]), shape = (1, 87)
                (if we make reshape(-1, 1), we turn it again to the original tensor format)
            
            Notice that we want only the internal 1-dimensional array (with 87 values in the example)
            # So we make:
            y_train[0] to select only it.
    """
            
    reshaped_y_train = np.array(y_train).reshape(1, -1)
    # This array has format([[val1, val2, ...]]) - i.e., it has two dimensions. Let's pick
    # only the first array:
    reshaped_y_train = reshaped_y_train[0]
    
    # Fit the model:
    mlp_model = mlp_model.fit(X_train, reshaped_y_train)
    
    if (mlp_model.n_iter_ == maximum_of_allowed_iterations):
        print("Warning! Total of iterations equals to the maximum allowed. It indicates that the convergence was not reached yet. Try to increase the maximum number of allowed iterations.")
    
    print(f"Finished fitting of the neural network with {mlp_model.n_layers_} after {mlp_model.n_iter_} iterations.")
    print(f"Minimum loss reached by the solver throughout fitting = {mlp_model.best_loss_}")
    
    
    # Create the training history dictionary:
    mlp_training_history_dict = {'loss': mlp_model.loss_curve_,
                                'rmse': []}
    
    # Let's create a history object analogous to the one created by TensorFlow, to be used
    # for plotting the loss curve:
    class history_object:
        # Initialize instance attributes.
        # define the Class constructor, i.e., how are its objects:
        def __init__(self, history = mlp_training_history_dict):
            
            # TensorFlow creates an object with the history attribute. This attribute stores
            # the history dictionary:
            self.history = history
    
    # Instantiate the object:
    history = history_object(history = mlp_training_history_dict)
    # Now, it has the same format as the TensorFlow history.
    
    # Get predictions for training, testing, and validation:
    y_preds_for_train = mlp_model.predict(X_train)

    if ((X_test is not None) & ((y_test is not None))):
        y_preds_for_test = mlp_model.predict(X_test)

    else:
        y_preds_for_test = None

    if ((X_valid is not None) & ((y_valid is not None))):
        y_preds_for_validation = mlp_model.predict(X_valid)

    else:
        y_preds_for_validation = None
    
    
    # instantiate the model checker object:
    model_check = model_checking(model_object = mlp_model, model_type = type_of_problem, model_package = 'sklearn', column_map_dict = column_map_dict, training_history_object = history, X = X_train, y_train = y_train, y_preds_for_train = y_preds_for_train, y_test = y_test, y_preds_for_test = y_preds_for_test, y_valid = y_valid, y_preds_for_validation = y_preds_for_validation)
            
    # Calculate model metrics:
    model_check = model_check.model_metrics()
    # Retrieve model metrics:
    metrics_dict = model_check.metrics_dict

    print("Check the loss curve below:\n")
    model_check = model_check.plot_training_history (metrics_name = 'rmse', x_axis_rotation = x_axis_rotation, y_axis_rotation = y_axis_rotation, grid = grid, horizontal_axis_title = horizontal_axis_title, metrics_vertical_axis_title = metrics_vertical_axis_title, loss_vertical_axis_title = loss_vertical_axis_title, export_png = export_png, directory_to_save = directory_to_save, file_name = file_name, png_resolution_dpi = png_resolution_dpi)
    
    print("\n") # line break
    print("Note: If a proper number of epochs was used for training, then a final baseline (plateau) should be reached by the curve.\n")
    
    print("\n") #line break
    print("To predict the model output y_pred for a dataframe X, declare: y_pred = mlp_model.predict(X)\n")
    print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
    print("X_train = np.reshape(np.array(X_train), (-1, 1))")
    # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362
    
    if (type_of_problem == 'classification'):
        
        print("To predict the probabilities associated to each class for the set X_train, use the .predict_proba(X) method:")
        print("y_pred_probabilities = mlp_model.predict_proba(X_train)")
    
    
    return mlp_model, metrics_dict, history


def get_deep_learning_tf_model (X_train, y_train, architecture = 'simple_dense', optimizer = None, X_test = None, y_test = None, X_valid = None, y_valid = None, type_of_problem = "regression", size_of_training_batch = 200, number_of_training_epochs = 2000, number_of_output_classes = 2, verbose = 1, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, metrics_vertical_axis_title = None, loss_vertical_axis_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    import numpy as np
    import pandas as pd
    import tensorflow as tf
    
    # X_train = subset of predictive variables (dataframe).
    # y_train = subset of response variable (series).
    # X_test = subset of predictive variables (test dataframe).
    # y_test = subset of response variable (test series).
    # The test parameters are passed as validation data, so they are necessary here.
    
    # architecture = 'simple_dense': tf_simple_dense model from class tf_models;
    # architecture = 'double_dense': tf_double_dense model from class tf_models;
    # architecture = 'cnn': tf_cnn time series model from class tf_models;
    # architecture = 'lstm': tf_lstm time series model from class tf_models;
    # architecture = 'encoder_decoder': encoder-decoder time series model from class tf_models;
    # architecture = 'cnn_lstm': hybrid cnn-lstm time series model from class tf_models.
    
    # optimizer: tf.keras.optimizers.Optimizer object:
    # keep it None to use the Adam optimizer.
    # https://www.tensorflow.org/api_docs/python/tf/keras/optimizers
    # https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/Optimizer
    # use the object to set parameters such as learning rate and selection of the optimizer
    
    # TYPE_OF_PROBLEM = 'regression'; or TYPE_OF_PROBLEM = 'classification'
    # The default is 'regression', which will be used if no type is
    # provided.
    
    # size_of_training_batch (integer): amount of data used on each training cycle (epoch). 
    # If we had 20000 data and size_of_training_batch = 200, then there would be 100 
    # batches (cycles) using 200 data. Training is more efficient when dividing the data into 
    # smaller subsets (batches) of ramdonly chosen data and separately training the model
    # for each batch (in training cycles called epochs). Also, this helps preventing
    # overfitting: if we use at once all data, the model is much more prone to overfit
    # (memorizing effect), selecting non-general features highly specific from the data
    # for the description of it. Therefore, it will have lower capability of predicting
    # data for values it already did not observe.
    # This is the parameter batch_size of most of the algorithms.
    
    # number_of_training_epochs (integer): number of training cycles used. 
    # This is the 'epochs' parameter of the algorithms.
    
    # number_of_output_classes = None - if TYPE_OF_PROBLEM = 'classification',
    # this parameter should be specified as an integer. That is because the number of
    # neurons in the output layer should be equal to the number of classes (1 neuron per
    # possible class).
    # If we simply took the number of different labels on the training data as the number
    # of classes, there would be the risk that a given class is not present on the training
    # set. So, it is safer (and less computer consuming) to input this number.
    # For simplicity, you may simply set this parameter as the value
    # number_of_classes returned from the function 'retrieve_classes_used_for_training'

    # If there are only two classes, we use a last Dense(1) layer (only one neuron) activated
    # through sigmoid: Dense(1, activation = 'sigmoid'). 
    # This is equivalent to the logistic regression, generating an output between 0 and 1 
    # (binary probability). The loss function, in this case, will be the 'binary_crossentropy'. 
    # This is more efficient than using softmax.
    
    # If there are more than two classes, then we set the number of neurons in Dense as
    # number_of_output_classes, and activate the layer through 'softmax':  
    # Dense(number_of_output_classes, activation = 'softmax')
    # Softmax generates a probability distribution, calculates the probability for 
    # each output and chooses the class with higher probability. The loss function depends on the
    # number of classes. If we are working with few classes (<= 5), we can use 
    # "categorical_crossentropy". If a higher number is used, we apply the 'sparse_categorical_crossentropy'
    # All of the classification problems accept 'accuracy' as the metrics for training.
    
    # For the regression problems, though, the output is a real value (i.e., a scalar). Then,
    # the last layer should ALWAYS contain a single neuron. So, there is no meaning in
    # specifying it as a parameter.
    # Also, the loss used for evaluating regression problems cannot be the crossentropy.
    # In these cases, we use the mean squared error (mse) instead. For the metrics,
    # naturally there is no meaning in using 'accuracy'. So, we use 'RootMeanSquaredError'
    # or 'mae' (mean absolute error).
    
    # Create functions for specific reshaping
    def reshaper(architecture):
        if (architecture == 'cnn_lstm'):
            return (lambda x: np.array(x).reshape(x.shape[0], 2, 2, 1))
        elif ((architecture == 'cnn')|(architecture == 'lstm')|(architecture == 'encoder_decoder')):
            return (lambda x: np.array(x).reshape(x.shape[0], x.shape[1], 1))
        else:
            # return the array itself:
            return (lambda x: np.array(x))
    
    if (architecture == 'cnn_lstm'):
        # Get the hybrid cnn-lstm time series model from class tf_models:
        
        # Here, the sequence length or number of columns must be even: they will be grouped in pairs
        # Check if the number is even: % - remainder of the integer division
        if ((X_train.shape[1] % 2) != 0):
            # There is remainder of the division: the number of columns is not even
            print("This architecture requires the inputs to be reshape as pairs of numbers.")
            print(f"Here, there are {X_train.shape[1]} columns or sequence elements. Drop one column to use this architecture.\n")
            
            return None, None, None
    
    # Put the arrays in the correct shape for the particular architecture
    reshape_function = reshaper(architecture)
    
    try:
        X_train = reshape_function(X_train)

        if ((X_test is not None) & (y_test is not None)):   
            X_test = reshape_function(X_test)
        if ((X_valid is not None) & (y_valid is not None)):   
            X_valid = reshape_function(X_valid)
    except:
        pass
    
    # Instantiate a tf_models object:
    tf_model_obj = tf_models(X_train = X_train, y_train = y_train, X_valid = X_test, y_valid = y_test, type_of_problem = type_of_problem, number_of_classes = number_of_output_classes, optimizer = optimizer)
    
    if (architecture == 'double_dense'):
        # Get the tf_cnn time series model from class tf_models:
        tf_model_obj = tf_model_obj.tf_double_dense(epochs = number_of_training_epochs, batch_size = size_of_training_batch, verbose = verbose)
    
    elif (architecture == 'cnn'):
        # Get the tf_cnn time series model from class tf_models:
        tf_model_obj = tf_model_obj.tf_cnn_time_series(epochs = number_of_training_epochs, batch_size = size_of_training_batch, verbose = verbose)
        
    
    elif (architecture == 'lstm'):
        # Get the tf_lstm time series model from class tf_models:
        tf_model_obj = tf_model_obj.tf_lstm_time_series(epochs = number_of_training_epochs, batch_size = size_of_training_batch, verbose = verbose)
    
    elif (architecture == 'encoder_decoder'):
        # Get the encoder-decoder time series model from class tf_models:
        tf_model_obj = tf_model_obj.tf_encoder_decoder_time_series(epochs = number_of_training_epochs, batch_size = size_of_training_batch, verbose = verbose)
    
    elif (architecture == 'cnn_lstm'):
        
        tf_model_obj = tf_model_obj.tf_cnn_lstm_time_series(epochs = number_of_training_epochs, batch_size = size_of_training_batch, verbose = verbose)
    
    else:
        # Get the tf_simple_dense model from class tf_models:
        tf_model_obj = tf_model_obj.tf_simple_dense(epochs = number_of_training_epochs, batch_size = size_of_training_batch, verbose = verbose)

    # Retrieve the model and the history:
    model = tf_model_obj.model
    history = tf_model_obj.history
    
    # Get predictions for training, testing, and validation:
    y_preds_for_train = np.array(model.predict(X_train))
    total_dimensions = len(y_preds_for_train.shape)
    
    if (architecture == 'encoder_decoder'):
        # Since return_sequences = True, the model returns arrays containing two elements. We must pick only
        # the first position (index 0) of 2nd dimension
        y_preds_for_train = y_preds_for_train[:,0]
        total_dimensions = len(y_preds_for_train.shape)
    
    last_dim = y_preds_for_train.shape[(total_dimensions - 1)] # indexing starts from zero
    if (last_dim == 1): # remove last dimension
        if (total_dimensions == 4):
            y_preds_for_train = y_preds_for_train[:,:,:,0]
        elif (total_dimensions == 3):
            y_preds_for_train = y_preds_for_train[:,:,0]
        elif (total_dimensions == 2):
            y_preds_for_train = y_preds_for_train[:,0]
    
    if ((X_test is not None) & ((y_test is not None))):
        if ((len(X_test) > 0) & ((len(y_test) >0))):
            y_preds_for_test = np.array(model.predict(X_test))
            last_dim = y_preds_for_test.shape[(total_dimensions - 1)]
            if (architecture == 'encoder_decoder'):
                y_preds_for_test = y_preds_for_test[:,0]
            if (last_dim == 1): # remove last dimension
                if (total_dimensions == 4):
                    y_preds_for_test = y_preds_for_test[:,:,:,0]
                elif (total_dimensions == 3):
                    y_preds_for_test = y_preds_for_test[:,:,0]
                elif (total_dimensions == 2):
                    y_preds_for_test = y_preds_for_test[:,0]
        
        else:
            X_test, y_test, y_preds_for_test = None, None, None

    else:
        y_preds_for_test = None

    if ((X_valid is not None) & ((y_valid is not None))):
        if ((len(X_valid) > 0) & ((len(X_valid) >0))):
            y_preds_for_validation = np.array(model.predict(X_valid))
            last_dim = y_preds_for_validation.shape[(total_dimensions - 1)]
            if (architecture == 'encoder_decoder'):
                y_preds_for_validation = y_preds_for_validation[:,0]
            if (last_dim == 1): # remove last dimension
                if (total_dimensions == 4):
                    y_preds_for_validation = y_preds_for_validation[:,:,:,0]
                elif (total_dimensions == 3):
                    y_preds_for_validation = y_preds_for_validation[:,:,0]
                elif (total_dimensions == 2):
                    y_preds_for_validation = y_preds_for_validation[:,0]
        
        else:
            X_valid, y_valid, y_preds_for_validation = None, None, None

    else:
        y_preds_for_validation = None
    
    # instantiate the model checker object:
    model_check = model_checking(model_object = model, model_type = type_of_problem, model_package = 'tensorflow', column_map_dict = column_map_dict, training_history_object = history, X = X_train, y_train = y_train, y_preds_for_train = y_preds_for_train, y_test = y_test, y_preds_for_test = y_preds_for_test, y_valid = y_valid, y_preds_for_validation = y_preds_for_validation)
            
    # Calculate model metrics:
    model_check = model_check.model_metrics()
    
    try:
        # Retrieve model metrics:
        metrics_dict = model_check.metrics_dict
    
    except:
        print("Unable to retrieve metrics.\n")

    print("Check the training loss and metrics curve below:\n")
    print("Regression models: metrics = MAE; loss = MSE.")
    print("Classification models: metrics = accuracy; loss = crossentropy (binary or sparse categorical).\n")
    
    model_check = model_check.plot_training_history (metrics_name = model_check.metrics_name, x_axis_rotation = x_axis_rotation, y_axis_rotation = y_axis_rotation, grid = grid, horizontal_axis_title = horizontal_axis_title, metrics_vertical_axis_title = metrics_vertical_axis_title, loss_vertical_axis_title = loss_vertical_axis_title, export_png = export_png, directory_to_save = directory_to_save, file_name = file_name, png_resolution_dpi = png_resolution_dpi)
    print("\n")
    
    print("Notice that:")
    print("1. If the loss did not reach a stable final baseline (a plateau), then the number of epochs should be increased. The ideal number of epochs is the minimum needed for reaching the final baseline. Increasing the number of epochs after this moment only increases the computational costs, without gain of performance.")
    print("2. A great mismatch between the curves indicates overfitting. This may be noticed as a gain of performance by the training curve (loss reduction or increase on accuracy) without correspondent improvement on the validation set performance (e.g. the validation metrics reaches a baseline very lower than the training curve).")
    print("If your data is overfitting, you can modify the sizes of training and test sets, modify the hyperparameters, or add a Dropout hidden-layer.")
    print("Adding dropout is common for image classification problems. The syntax for declaring the layer is:")
    print("tf.keras.layers.Dropout(0.5)")
    print("In this example, we added Dropout(0.5). It means that you lose 50\% of nodes. If using Dropout(0.2), you would lose 20\% of nodes.")
    print("Dropout helps avoiding overfitting because neighbor neurons can have similar weights, and thus can skew the final training.")
    print("If you set a too high dropout rate, the network will lose specialization to the effect that it would be inefficient or ineffective at learning, driving accuracy down.")
    print("\n") # line break
    
    print("\n") #line break
    print("To predict the model output y_pred for a dataframe X, declare: y_pred = model.predict(X)\n")
    print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
    print("X_train = np.reshape(np.array(X_train), (-1, 1))")
    # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362
    print("Attention: for classification with Keras/TensorFlow, this output will not be a class, but an array of probabilities correspondent to the probability that the entry belongs to each class.")
    print("The output class from the deep learning model is the class with higher probability indicated by the predict method. Again, the order of classes is the order they appear in the training dataset. For instance, when using the ImageDataGenerator, the 1st class is the name of the 1st read directory, the 2nd class is the 2nd directory, and so on.")
        
    return model, metrics_dict, history


def get_siamese_networks_model (X_train, y_train, output_dictionary, architecture = 'simple_dense', optimizer = None, X_test = None, y_test = None, X_valid = None, y_valid = None, size_of_training_batch = 200, number_of_training_epochs = 2000, verbose = 1, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, metrics_vertical_axis_title = None, loss_vertical_axis_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    import numpy as np
    import pandas as pd
    import tensorflow as tf
    
    # output_dictionary:
    # output_dictionary structure:
    # {'response_variable': {
    # 'type': 'regression', 'number_of_classes':}}
    # 'response_variable': name of the column used as response for one of the outputs. This key
    # gives access to the nested dictionary containing the following keys: 
    # 'type': type of problem. Must contain the string 'regression' or 'classification';
    # 'number_of_classes': integer. This key may not be declared for regression problems. Do not
    # include the key, set as 1, or set the number of classes used for training.
    
    # X_train = subset of predictive variables (dataframe).
    # y_train = subset of response variable (series).
    # X_test = subset of predictive variables (test dataframe).
    # y_test = subset of response variable (test series).
    # The test parameters are passed as validation data, so they are necessary here.
    
    # architecture = 'simple_dense': base_model_simple_dense from class siamese_networks;
    # architecture = 'double_dense': base_model_double_dense from class siamese_networks;
    # architecture = 'cnn': base_model_cnn_time_series from class siamese_networks;
    # architecture = 'lstm': base_model_lstm_time_series from class siamese_networks;
    # architecture = 'encoder_decoder': base_model_encoder_decoder_time_series from class siamese_networks;
    # architecture = 'cnn_lstm': hybrid base_model_cnn_lstm_time_series from class siamese_networks.
    
    # optimizer: tf.keras.optimizers.Optimizer object:
    # keep it None to use the Adam optimizer.
    # https://www.tensorflow.org/api_docs/python/tf/keras/optimizers
    # https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/Optimizer
    # use the object to set parameters such as learning rate and selection of the optimizer
    
    # size_of_training_batch (integer): amount of data used on each training cycle (epoch). 
    # If we had 20000 data and size_of_training_batch = 200, then there would be 100 
    # batches (cycles) using 200 data. Training is more efficient when dividing the data into 
    # smaller subsets (batches) of ramdonly chosen data and separately training the model
    # for each batch (in training cycles called epochs). Also, this helps preventing
    # overfitting: if we use at once all data, the model is much more prone to overfit
    # (memorizing effect), selecting non-general features highly specific from the data
    # for the description of it. Therefore, it will have lower capability of predicting
    # data for values it already did not observe.
    # This is the parameter batch_size of most of the algorithms.
    
    # number_of_training_epochs (integer): number of training cycles used. 
    # This is the 'epochs' parameter of the algorithms.
    
    # Create functions for specific reshaping
    def reshaper(architecture):
        if (architecture == 'cnn_lstm'):
            return (lambda x: np.array(x).reshape(x.shape[0], 2, 2, 1))
        elif ((architecture == 'cnn')|(architecture == 'lstm')|(architecture == 'encoder_decoder')):
            return (lambda x: np.array(x).reshape(x.shape[0], x.shape[1], 1))
        else:
            # return the array itself:
            return (lambda x: np.array(x))

    if (architecture == 'cnn_lstm'):
        # Get the hybrid cnn-lstm time series model:
        
        # Here, the sequence length or number of columns must be even: they will be grouped in pairs
        # Check if the number is even: % - remainder of the integer division
        if ((X_train.shape[1] % 2) != 0):
            # There is remainder of the division: the number of columns is not even
            print("This architecture requires the inputs to be reshape as pairs of numbers.")
            print(f"Here, there are {X_train.shape[1]} columns or sequence elements. Drop one column to use this architecture.\n")
            
            return None, None, None
    
    # Put the arrays in the correct shape for the particular architecture
    reshape_function = reshaper(architecture)
    
    try:
        X_train = reshape_function(X_train)

        if ((X_test is not None) & (y_test is not None)):   
            X_test = reshape_function(X_test)
        if ((X_valid is not None) & (y_valid is not None)):   
            X_valid = reshape_function(X_valid)
    except:
        pass
        
    # Instantiate a siamese_networks object:
    siamese_networks_obj = siamese_networks(output_dictionary = output_dictionary, X_train = X_train, y_train = y_train, X_valid = X_test, y_valid = y_test)
    
    # Compile the model:
    siamese_networks_obj = siamese_networks_obj.compile_model(architecture = architecture, optimizer = optimizer)
    
    # Fit the model:
    siamese_networks_obj = siamese_networks_obj.fit_model(epochs = number_of_training_epochs, batch_size = size_of_training_batch, verbose = verbose)
    
    # Retrieve model and the history from model and history attributes:
    model = siamese_networks_obj.model
    history = siamese_networks_obj.history
    
    
    # Get predictions for training, testing, and validation:
    y_preds_for_train = np.array(model.predict(X_train))
    
    total_dimensions = len(y_preds_for_train.shape)
    
    if (architecture == 'encoder_decoder'):
        # Since return_sequences = True, the model returns arrays containing two elements. We must pick only
        # the first position (index 0) of 2nd dimension
        # This array has dimensions like (4, 48, 2, 1) for a 4-response model output.
        # Notice that the 3rd dimension contains 2 dimensions, due to the parameter return_sequences = True.
        # We want only the first value correspondent to this dimension.
        # Also, notice that a single response model would have dimensions as (48, 2, 1), and the extra dimension
        # correspondent to return_sequences = True would be the 2nd dim.
        # Pick only the first value from third dimension:
        y_preds_for_train = y_preds_for_train[:,:,0]
        total_dimensions = len(y_preds_for_train.shape)
    
    last_dim = y_preds_for_train.shape[(total_dimensions - 1)] # indexing starts from zero
    if (last_dim == 1): # remove last dimension
        if (total_dimensions == 4):
            y_preds_for_train = y_preds_for_train[:,:,:,0]
        elif (total_dimensions == 3):
            y_preds_for_train = y_preds_for_train[:,:,0]
        elif (total_dimensions == 2):
            y_preds_for_train = y_preds_for_train[:,0]
    
    if ((X_test is not None) & ((y_test is not None))):
        if ((len(X_test) > 0) & ((len(y_test) >0))):
            y_preds_for_test = np.array(model.predict(X_test))
            last_dim = y_preds_for_test.shape[(total_dimensions - 1)]
            if (architecture == 'encoder_decoder'):
                y_preds_for_test = y_preds_for_test[:,:,0]
            if (last_dim == 1): # remove last dimension
                if (total_dimensions == 4):
                    y_preds_for_test = y_preds_for_test[:,:,:,0]
                elif (total_dimensions == 3):
                    y_preds_for_test = y_preds_for_test[:,:,0]
                elif (total_dimensions == 2):
                    y_preds_for_test = y_preds_for_test[:,0]
        
        else:
            X_test, y_test, y_preds_for_test = None, None, None

    else:
        y_preds_for_test = None

    if ((X_valid is not None) & ((y_valid is not None))):
        if ((len(X_valid) > 0) & ((len(X_valid) > 0))):
            y_preds_for_validation = np.array(model.predict(X_valid))
            last_dim = y_preds_for_validation.shape[(total_dimensions - 1)]
            if (architecture == 'encoder_decoder'):
                y_preds_for_validation = y_preds_for_validation[:,:,0]
            if (last_dim == 1): # remove last dimension
                if (total_dimensions == 4):
                    y_preds_for_validation = y_preds_for_validation[:,:,:,0]
                elif (total_dimensions == 3):
                    y_preds_for_validation = y_preds_for_validation[:,:,0]
                elif (total_dimensions == 2):
                    y_preds_for_validation = y_preds_for_validation[:,0]
        
        else:
            X_valid, y_valid, y_preds_for_validation = None, None, None

    else:
        y_preds_for_validation = None
    
    model_check = model_checking(model_object = model, model_package = 'tensorflow', column_map_dict = column_map_dict, training_history_object = history, X = X_train, y_train = y_train, y_preds_for_train = y_preds_for_train, y_test = y_test, y_preds_for_test = y_preds_for_test, y_valid = y_valid, y_preds_for_validation = y_preds_for_validation)
    
    model_check = model_check.model_metrics_multiresponses (output_dictionary = output_dictionary)
    
    try:
        # Retrieve model metrics:
        metrics_dict = model_check.metrics_dict
    except:
        print("Unable to retrieve metrics.\n")
    
    print("Check the training loss and metrics curve below:\n")
    print("Regression models: metrics = MAE; loss = MSE.")
    print("Classification models: metrics = accuracy; loss = crossentropy (binary or sparse categorical).\n")
    
    model_check = model_check.plot_history_multiresponses (x_axis_rotation = x_axis_rotation, y_axis_rotation = y_axis_rotation, grid = grid, horizontal_axis_title = horizontal_axis_title, metrics_vertical_axis_title = metrics_vertical_axis_title, loss_vertical_axis_title = loss_vertical_axis_title, export_png = export_png, directory_to_save = directory_to_save, file_name = file_name, png_resolution_dpi = png_resolution_dpi)
    
    
    print("\n")

    print("Notice that:")
    print("1. If the loss did not reach a stable final baseline (a plateau), then the number of epochs should be increased. The ideal number of epochs is the minimum needed for reaching the final baseline. Increasing the number of epochs after this moment only increases the computational costs, without gain of performance.")
    print("2. A great mismatch between the curves indicates overfitting. This may be noticed as a gain of performance by the training curve (loss reduction or increase on accuracy) without correspondent improvement on the validation set performance (e.g. the validation metrics reaches a baseline very lower than the training curve).")
    print("If your data is overfitting, you can modify the sizes of training and test sets, modify the hyperparameters, or add a Dropout hidden-layer.")
    print("Adding dropout is common for image classification problems. The syntax for declaring the layer is:")
    print("tf.keras.layers.Dropout(0.5)")
    print("In this example, we added Dropout(0.5). It means that you lose 50\% of nodes. If using Dropout(0.2), you would lose 20\% of nodes.")
    print("Dropout helps avoiding overfitting because neighbor neurons can have similar weights, and thus can skew the final training.")
    print("If you set a too high dropout rate, the network will lose specialization to the effect that it would be inefficient or ineffective at learning, driving accuracy down.")
    print("\n") # line break
    
    print("\n") #line break
    print("To predict the model output y_pred for a dataframe X, declare: y_pred = model.predict(X)\n")
    print("For a one-dimensional correlation, the one-dimension array or list with format X_train = [x1, x2, ...] must be converted into a dataframe subset, X_train = [[x1, x2, ...]] before the prediction. To do so, create a list with X_train as its element: X_train = [X_train], or use the numpy.reshape(-1,1):")
    print("X_train = np.reshape(np.array(X_train), (-1, 1))")
    # numpy reshape: https://numpy.org/doc/1.21/reference/generated/numpy.reshape.html?msclkid=5de33f8bc02c11ec803224a6bd588362
    print("Attention: for classification with Keras/TensorFlow, this output will not be a class, but an array of probabilities correspondent to the probability that the entry belongs to each class.")
    print("The output class from the deep learning model is the class with higher probability indicated by the predict method. Again, the order of classes is the order they appear in the training dataset. For instance, when using the ImageDataGenerator, the 1st class is the name of the 1st read directory, the 2nd class is the 2nd directory, and so on.")

    
    return model, metrics_dict, history


def make_model_predictions (model_object, X, dataframe_for_concatenating_predictions = None, column_with_predictions_suffix = None, function_used_for_fitting_dl_model = 'get_deep_learning_tf_model', architecture = None, list_of_responses = []):
    
    import numpy as np
    import pandas as pd
    import tensorflow as tf
    
    # The function will automatically detect if it is dealing with lists, NumPy arrays
    # or Pandas dataframes. If X is a list or a single-dimension array, predict_for
    # will be set as 'single_entry'. If X is a multi-dimension NumPy array (as the
    # outputs for preparing data - even single_entry - for deep learning models), or if
    # it is a Pandas dataframe, the function will set predict_for = 'subset'
    
    # X = subset of predictive variables (dataframe, NumPy array, or list).
    # If PREDICT_FOR = 'single_entry', X should be a list of parameters values.
    # e.g. X = [1.2, 3, 4] (dot is the decimal case separator, comma separate values). 
    # Notice that the list should contain only the numeric values, in the same order of the
    # correspondent columns.
    # If PREDICT_FOR = 'subset' (prediction for multiple entries), X should be a dataframe 
    # (subset) or a multi-dimensional NumPy array of the parameters values, as usual.
    
    # model_object: object containing the model that will be analyzed. e.g.
    # model_object = elastic_net_linear_reg_model
    
    # dataframe_for_concatenating_predictions: if you want to concatenate the predictions
    # to a dataframe, pass it here:
    # e.g. dataframe_for_concatenating_predictions = df
    # If the dataframe must be the same one passed as X, repeat the dataframe object here:
    # X = dataset, dataframe_for_concatenating_predictions = dataset.
    # Alternatively, if dataframe_for_concatenating_predictions = None, 
    # the prediction will be returned as a series or NumPy array, depending on the input format.
    # Notice that the concatenated predictions will be added as a new column.
    
    # column_with_predictions_suffix = None. If the predictions are added as a new column
    # of the dataframe dataframe_for_concatenating_predictions, you can declare this
    # parameter as string with a suffix for identifying the model. If no suffix is added, the new
    # column will be named 'y_pred'.
    # e.g. column_with_predictions_suffix = '_keras' will create a column named "y_pred_keras". This
    # parameter is useful when working with multiple models. Always start the suffix with underscore
    # "_" so that no blank spaces are added; the suffix will not be merged to the column; and there
    # will be no confusion with the dot (.) notation for methods, JSON attributes, etc.
    
    # function_used_for_fitting_dl_model: the function you used for obtaining the deep learning model.
    # Example: 'get_deep_learning_tf_model' or 'get_siamese_networks_model'
    
    # architecture: some models require inputs in a proper format. Declare here if you are using
    # one of these architectures. Example: architecture = 'cnn_lstm' from class tf_models require
    # a special reshape before getting predictions. You can keep None or put the name of the
    # architecture, if no special reshape is needed.
    
    # list_of_responses = []. This parameter is obbligatory for multi-response models, such as the ones obtained from
    # function 'get_siamese_networks_model'. It must contain a list with the same order of the output responses.
    # Example: suppose your siamese model outputs 4 responses: 'temperature', 'pressure', 'flow_rate', and 'ph', in
    # this order. The list of responses must be declared as: 
    # list_of_responses = ['temperature', 'pressure', 'flow_rate', 'ph']
    # tuples and numpy arrays are also acceptable: list_of_responses = ('temperature', 'pressure', 'flow_rate', 'ph')
    # Attention: the number of responses must be exactly the number of elements in list_of_responses, or an error will
    # be raised.
    
    
    # Check the type of input: if we are predicting the output for a subset (NumPy array reshaped
    # for deep learning models or Pandas dataframe); or predicting for a single entry (single-
    # dimension NumPy array or Python list).
    
    # 1. Check if a list was input. Lists do not have the attribute shape, present in dataframes
    # and NumPy arrays. Accessing the attribute shape from a list will raise the Exception error
    # named AttributeError
    # Try to access the attribute shape. If the error AttributeError is raised, it is a list, so
    # set predict_for = 'single_entry':
    
    
    # Create functions for specific reshaping
    def reshaper(architecture):
        # Use the str function in case user input None or a number as architecture
        if (str(architecture) == 'cnn_lstm'):
            return (lambda x: np.array(x).reshape(x.shape[0], 2, 2, 1))
        elif ((str(architecture) == 'cnn')|(str(architecture) == 'lstm')|(str(architecture) == 'encoder_decoder')):
            return (lambda x: np.array(x).reshape(x.shape[0], x.shape[1], 1))
        else: # includes architecture is None
            # return the array itself:
            return (lambda x: np.array(x))
    
    
    # Put the arrays in the correct shape for the particular architecture
    reshape_function = reshaper(architecture)
    try:
        X = reshape_function(X)
    except:
        pass
    
    # start a response dictionary:
    response_dict = {}

    # Run even if it come from list or tuple:
    if (len(X.shape) == 1):
        # If X.shape has len == 1, it is a tuple like (4,)
        # Convert the numpy array to the correct shape. It runs even if the list or tuple was
        # converted.
        X = X.reshape(1, -1)
        # generates an array like array([[1, 2, 3, 4]])
        # The reshape (-1, 1) generates an array like ([1], [2], ...) with format for the y-vector
        # used for training.
    
    # Total of entries in the dataset:
    # Get the total of values for the first response, by isolating the index 0 of 2nd dimension
    total_data = len(X)
    
    if (len(list_of_responses) == 0):
        total_of_responses = 1
    else:
        total_of_responses = len(list_of_responses)
        
    print(f"Predicting {total_of_responses} responses for a total of {total_data} entries.\n")
    
    # prediction for a subset
    y_pred = np.array(model_object.predict(X))
    print("Attention: for classification with Keras/TensorFlow and other deep learning frameworks, this output will not be a class, but an array of probabilities correspondent to the probability that the entry belongs to each class. In this case, it is better to use the function calculate_class_probability below, setting model_type == \'deep_learning\'. This function will result into dataframes containing the classes as columns and the probabilities in the respective row.\n")
    print("The output class from the deep learning model is the class with higher probability indicated by the predict method. Again, the order of classes is the order they appear in the training dataset. For instance, when using the ImageDataGenerator, the 1st class is the name of the 1st read directory, the 2nd class is the 2nd directory, and so on.\n")
    
    total_dimensions = len(y_pred.shape)
    last_dim = y_pred.shape[(total_dimensions - 1)] # indexing starts from zero
    
    # If y_pred came from a RNN with the parameter return_sequences = True and/or
    # return_states = True, then the hidden and/or cell states from the LSTMs
    # were returned. So, the returned array has at least one extra dimensions (two
    # if both parameters are True). On the other hand, we want only the first dimension,
    # correspondent to the actual output.
        
    # Remember that, due to the reshapes for preparing data for deep learning models,
    # y_pred must have at least 2 dimensions: (N, 1), where N is the number of rows of
    # the original dataset. But y_pred returned from a model with return_sequences = True
    # or return_states = True will be of dimension (N, N, 1). If both parameters are True,
    # the dimension is (N, N, N, 1), since there are extra arrays for both the hidden and
    # cell states.
        
    # The conclusion is that there is a third dimension only for models where return_sequences
    # = True or return_states = True
    
    if (function_used_for_fitting_dl_model == 'get_siamese_networks_model'):
        
        y_pred_array = y_pred # save in another variable for re-using later
        
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
        
        if (architecture == 'encoder_decoder'):
            # Since return_sequences = True, the model returns arrays containing two elements. We must pick only
            # the first position (index 0) of 2nd dimension
            # This array has dimensions like (4, 48, 2, 1) for a 4-response model output.
            # Notice that the 3rd dimension contains 2 dimensions, due to the parameter return_sequences = True.
            # We want only the first value correspondent to this dimension.
            # Also, notice that a single response model would have dimensions as (48, 2, 1), and the extra dimension
            # correspondent to return_sequences = True would be the 2nd dim.
            # Pick only the first value from third dimension:
            y_pred_array = y_pred_array[:,:,0]
        

        # Now, loop through each response:
        for index, response in enumerate(list_of_responses):
            
            if (dim == 1):
                y_pred = y_pred_array[:, index]
            
            elif (dim == 0):
                y_pred = y_pred_array[index]
            
            # add it to the dictionary as the key response:
            response_dict[('y_pred_' + response)] = y_pred

    else: # general case
        
        if (function_used_for_fitting_dl_model == 'get_deep_learning_tf_model'):
            
            if (architecture == 'encoder_decoder'):
                # Since return_sequences = True, the model returns arrays containing two elements. We must pick only
                # the first position (index 0) of 2nd dimension
                y_pred = y_pred[:,0]
                total_dimensions = len(y_pred.shape)
                last_dim = y_pred.shape[(total_dimensions - 1)]
            
            if (last_dim == 1): # remove last dimension
                if (total_dimensions == 4):
                    y_pred = y_pred[:,:,:,0]
                elif (total_dimensions == 3):
                    y_pred = y_pred[:,:,0]
                elif (total_dimensions == 2):
                    y_pred = y_pred[:,0]
        
        # check if there is a suffix:
        if not (column_with_predictions_suffix is None):
            # There is a suffix declared
            # Since there is a suffix, concatenate it to 'y_pred':
            response_dict[( "y_pred_" + column_with_predictions_suffix)] = y_pred
            
        else:
            # Create the column name as the standard.
            # The name of the new column is simply 'y_pred'
            response_dict["y_pred"] = y_pred
    
    # Check if there is a dataframe to concatenate the predictions
    if not (dataframe_for_concatenating_predictions is None):
            
        # there is a dataframe for concatenating the predictions    
        # concatenate the predicted values with dataframe_for_concatenating_predictions.
        # Add the predicted values as a column:
            
        # Set a local copy of the dataframe to manipulate:
        X_copy = dataframe_for_concatenating_predictions.copy(deep = True)
            
        # Add the predictions as the new column named col_name:
        # If y is a tensor, convert to NumPy array before adding. The numpy.array function
        # has no effect in numpy arrays, but is equivalent to the .numpy method for tensors
        
        for col_name, y_pred in response_dict.items():
            X_copy[col_name] = y_pred
            
        print(f"The prediction was added as the new columns {list(response_dict.keys())} of the dataframe, and this dataframe was returned. Check its 10 first rows:\n")
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(X_copy.head(10))
                    
        except: # regular mode
            print(X_copy.head(10))
            
        return X_copy
        
    else:
        
        # Convert the response_dict into a pandas DataFrame:
        predictions_df = pd.DataFrame(data = response_dict)
        print("Returning only the predicted values. Check the 10 first values of predictions dataframe:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(predictions_df.head(10))
                    
        except: # regular mode
            print(predictions_df.head(10))
            
        return predictions_df


def calculate_class_probability (model_object, X, list_of_classes, type_of_model = 'other', dataframe_for_concatenating_predictions = None, architecture = None):

    import numpy as np
    import pandas as pd
    import tensorflow as tf
    
    # predict_for = 'subset' or predict_for = 'single_entry'
    # The function will automatically detect if it is dealing with lists, NumPy arrays
    # or Pandas dataframes. If X is a list or a single-dimension array, predict_for
    # will be set as 'single_entry'. If X is a multi-dimension NumPy array (as the
    # outputs for preparing data - even single_entry - for deep learning models), or if
    # it is a Pandas dataframe, the function will set predict_for = 'subset'
    
    # X = subset of predictive variables (dataframe, NumPy array, or list).
    # If PREDICT_FOR = 'single_entry', X should be a list of parameters values.
    # e.g. X = [1.2, 3, 4] (dot is the decimal case separator, comma separate values). 
    # Notice that the list should contain only the numeric values, in the same order of the
    # correspondent columns.
    # If PREDICT_FOR = 'subset' (prediction for multiple entries), X should be a dataframe 
    # (subset) or a multi-dimensional NumPy array of the parameters values, as usual.
    
    # model_object: object containing the model that will be analyzed. e.g.
    # model_object = elastic_net_linear_reg_model
    
    # list_of_classes is the list of classes effectively used for training
    # the model. Set this parameter as the object returned from function
    # retrieve_classes_used_to_train
    
    # type_of_model = 'other' or type_of_model = 'deep_learning'
    
    # Notice that the output will be an array of probabilities, where each
    # element corresponds to a possible class, in the order classes appear.
    
    # dataframe_for_concatenating_predictions: if you want to concatenate the predictions
    # to a dataframe, pass it here:
    # e.g. dataframe_for_concatenating_predictions = df
    # If the dataframe must be the same one passed as X, repeat the dataframe object here:
    # X = dataset, dataframe_for_concatenating_predictions = dataset.
    # Alternatively, if dataframe_for_concatenating_predictions = None, 
    # the prediction will be returned as a series or NumPy array, depending on the input format.
    # Notice that the concatenated predictions will be added as a new column.
    
    # architecture: some models require inputs in a proper format. Declare here if you are using
    # one of these architectures. Example: architecture = 'cnn_lstm' from class tf_models require
    # a special reshape before getting predictions. You can keep None or put the name of the
    # architecture, if no special reshape is needed.
    
    
    # All of the new columns (appended or not) will have the prefix "prob_class_" followed
    # by the correspondent class name to identify them.
    
    
    # 1. Check if a list was input. Lists do not have the attribute shape, present in dataframes
    # and NumPy arrays. Accessing the attribute shape from a list will raise the Exception error
    # named AttributeError
    # Try to access the attribute shape. If the error AttributeError is raised, it is a list, so
    # set predict_for = 'single_entry':
    
    predict_for = 'subset'
    # map if we are dealing with a subset or single entry
    
    if ((type(X) == list) | (type(X) == tuple)):
        # Single entry as list or tuple
        # Convert it to NumPy array:
        X = np.array(X)
    
    # Run even if it come from list or tuple:
    if ((type(X) == np.ndarray) & (len(X.shape) == 1)):
        # If X.shape has len == 1, it is a tuple like (4,)
        # Convert the numpy array to the correct shape. It runs even if the list or tuple was
        # converted.
        X = X.reshape(1, -1)
        # generates an array like array([[1, 2, 3, 4]])
        # The reshape (-1, 1) generates an array like ([1], [2], ...) with format for the y-vector
        # used for training.
        
        # Update the predict_for variable:
        predict_for = 'single_entry'      
    
    # Finally, convert to Tensor:
    X = tf.constant(X)
    
    if (architecture == 'cnn_lstm'):
        # Get the hybrid cnn-lstm time series model from class tf_models:
        X = (lambda x: tf.constant(((x.numpy()).reshape(x.numpy().shape[0], 2, 2, 1))))(X)
    
        
    # Check if it is a keras or other deep learning framework; or if it is a sklearn or xgb model:
    boolean_check = (type_of_model == 'deep_learning')
    
    if (boolean_check): # run if it is True
        print("The predictions (outputs) from deep learning models are themselves the probabilities associated to each possible class.")
        print("\n") #line break
        print("The output will be an array of float values: each float represents the probability of one class, in the order the classes appear. For a binary classifier, the first element will correspond to class 0; and the second element will be the probability of class 1.")
    
    
    if (predict_for == 'single_entry'):
        
        print("Calculating probabilities for a single entry X.\n")
    
        if (boolean_check): 
            # Use the predict method itself for deep learning models.
            # These models do not have the predict_proba method.
            # Their output is itself the probability for each class.
            y_pred_probabilities = model_object.predict(X)
        
        else:
            # use the predict_proba method from sklearn and xgboost:
            y_pred_probabilities = model_object.predict_proba(X.numpy())
        
        print("Probabilities calculated using the entry parameters.") 
        print(f"Probabilities calculated for each one of the classes {list_of_classes} (in the order of classes) = {y_pred_probabilities}\n")
        
        # create a dictionary with the possible classes and the correspondent probabilities:
        # Use the list attribute to guarantee that the probabilities are
        # retrieved as a list:
        probability_dict = {'class': list_of_classes,
                            'probability': list(y_pred_probabilities)}
            
        # Convert it to a Pandas dataframe:
        probabilities_df = pd.DataFrame(data = probability_dict)
            
        print("Returning a dataframe containing the classes and the probabilities calculated for the entry to belong to each class. Check it below:")
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(probabilities_df)
                
        except: # regular mode
            print(probabilities_df)
            
        return probabilities_df
    
    
    else:
        
        # prediction for a subset
        
        if (boolean_check): 
            # Use the predict method itself for deep learning models.
            # These models do not have the predict_proba method.
            # Their output is itself the probability for each class.
            y_pred_probabilities = model_object.predict(X)
            
            # If y_pred_probabilities came from a RNN with the parameter return_sequences = True 
            # and/or return_states = True, then the hidden and/or cell states from the LSTMs
            # were returned. So, the returned array has at least one extra dimensions (two
            # if both parameters are True). On the other hand, we want only the first dimension,
            # correspondent to the actual output.

            # Remember that, due to the reshapes for preparing data for deep learning models,
            # y_pred_probabilities must have at least 2 dimensions: (N, 1), where N is the number 
            # of rows of the original dataset. But y_pred_probabilities returned from a model 
            # with return_sequences = True or return_states = True will be of dimension (N, N, 1). 
            # If both parameters are True, the dimension is (N, N, N, 1), since there are extra 
            # arrays for both the hidden and cell states.

            # The conclusion is that there is a third dimension only for models where 
            # return_sequences = True or return_states = True

            # Check if y_pred_probabilities is a numpy array, instead of a Pandas dataframe:

            if (len(y_pred_probabilities.shape) > 2):
                
                # The shape is a tuple containing 3 or more dimensions
                # If we could access the third_dimension, than return_states and
                # or return_sequences = True

                # We want only the values stored as the 1st dimension
                # y_pred_probabilities is an array where each element is an array with 
                # two elements. To get only the first elements:
                # (slice the arrays: get all values only for dimension 0, the 1st dim):
                y_pred_probabilities = y_pred_probabilities[:,0]
                # if we used y_pred_probabilities[:,1] we would get the second element, 
                # which is the hidden state h (input of the next LSTM unit).
                # It happens because of the parameter return_sequences = True. 
                # If return_states = True, there would be a third element, corresponding 
                # to the cell state c.
                # Notice that we want only the 1st dimension (0), no matter the case.
        
        else:
            # use the predict_proba method from sklearn and xgboost:
            y_pred_probabilities = model_object.predict_proba(X.numpy())
        
        # y_pred_probabilities is a column containing arrays of probabilities
        # Let's create a dataframe separating each element of the array into
        # a separate column
        
        # Get the size of each array. It is the total of elements from
        # list_of_classes (total of possible classes):
        total_of_classes = len(list_of_classes)
        
        # Starts a dictionary. This dictionary will have the class as the
        # key and a list of the probabilities that the element belong to that
        # class as the value (in the dataframe, the class will be column,
        # with its calculated probability in each row):
        probability_dict = {}
        
        # Loop through each possible class:
        for class_name in list_of_classes:
            
            # Let's concatenate the prefix "prob_class_" to this strings.
            # This string will be used as column name, so it will be clear 
            # in the output dataframe that the column is referrent to the 
            # probability calculated for the class. Since the elements may 
            # have been saved as numbers use the str attribute to guarantee 
            # that the element was read as a string, and concatenate the
            # prefix to its left:
            class_name = "prob_class_" + str(class_name)
            # Get the index in the list:
            class_index = list_of_class.index(class_name)
            
            # Start a list of probabilities:
            prob_list = []
            
            # Now loop through each row j from the dataframe
            # to retrieve the array in the column y_pred_probabilities:
            
            for i in range(len(y_pred_probabilities)):
                # goes from j = 0 (first row of the dataframe) to
                # j = y_pred_probabilities - 1, index of the last row
                # Get the array of probabilities for that row:
                # If y is a tensor, convert to NumPy array before adding. The numpy.array function
                # has no effect in numpy arrays, but is equivalent to the .numpy method for tensors
                prob_array = np.array(y_pred_probabilities[i])
                
                # Append the (class_index)-th element of that array in prob_list
                # The (class_index)-th position of the array is the probability
                # of the class being analyzed in the i-th iteration of
                # the main loop
                prob_list.append(prob_array[(class_index)])
            
            # Now that the probabilities for the class correspondent to
            # each row were retrieved as the list prob_list, update the
            # dictionary. Use the class name saved as class_name as the
            # key, and put the prob_list as the correspondent value:
            probability_dict[class_name] = prob_list
        
        # Now that we finished the loop, the probability dictionary contains
        # each one of the classes as its keys, and the list of probabilities
        # for each row as the correspondent values. 
        # Also, the keys are identified with the prefix 'prob_class' to
        # indicate that they are referrent to the probability of belonging to
        # one class. Let's convert this dictionary to a Pandas dataframe:
        
        probabilities_df = pd.DataFrame(data = probability_dict)
        
        # Check if there is a dataframe to concatenate the predictions
        if not (dataframe_for_concatenating_predictions is None):
            
            # there is a dataframe for concatenating the predictions.
            
            # Set a local copy of the dataframe to manipulate:
            X_copy = X.copy(deep = True)
            
            # Append the columns from probabilities_df with Pandas concat
            # method, setting axis = 1 (axis = 0  appends rows)
            # Use the pandas 'inner' join, which removes entries without
            # correspondence. It is the same strategy used for concatenating
            # the dataframe obtained from One-Hot Encoding transformation in the
            # ETL Workflow (3_Dataset_Transformation)
            X_copy = pd.concat([X_copy, probabilities_df], axis = 1, join = "inner")
    
            print(f"The dataframe X was concatenated to the probabilities calculated for each class and returned. Check its first 10 entries:\n")
            try:
                # only works in Jupyter Notebook:
                from IPython.display import display
                display(X_copy.head(10))
                    
            except: # regular mode
                print(X_copy.head(10))
            
            return X_copy
        
        else:
            
            print("Returning only the dataframe with the probabilities calculated for each class. Check its first 10 entries:\n")
            try:
                # only works in Jupyter Notebook:
                from IPython.display import display
                display(probabilities_df.head(10))
                    
            except: # regular mode
                print(probabilities_df.head(10))
            
            return probabilities_df

