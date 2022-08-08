# FUNCTIONS FROM INDUSTRIAL DATA SCIENCE WORKFLOW (IDSW) PACKAGE
# Modelling and Machine Learning

# Marco Cesar Prado Soares, Data Scientist Specialist @ Bayer Crop Science LATAM
# marcosoares.feq@gmail.com
# marco.soares@bayer.com
from dataclasses import dataclass


class model_checking:
            
    # Initialize instance attributes.
    # define the Class constructor, i.e., how are its objects:
    def __init__(self, model_object, model_type = 'regression', column_map_dict = None, training_history_dict = None, X = None, y_train = None, y_preds_for_train = None, y_test = None, y_preds_for_test = None, y_valid = None, y_preds_for_validation = None):

        import numpy as np
        import tensorflow as tf

        # Add the model:        
        self.model = model_object
        # model_type = 'regression' or 'classification'
        self.model_type = model_type

        # Add the columns names:
        self.column_map_dict = column_map_dict
        # Add the training history to the class:
        self.history = training_history_dict

        # Add the y series for computing general metrics:
        # Guarantee that they are tensorflow tensors
        self.y_train = tf.constant(y_train)
        self.y_preds_for_train = tf.constant(y_preds_for_train)
        self.y_test = tf.constant(y_test)
        self.y_preds_for_test = tf.constant(y_preds_for_test)
        self.y_valid = tf.constant(y_valid)
        self.y_preds_for_validation = tf.constant(y_preds_for_validation)

        # X can be X_train, X_test, or X_valid. 
        # We only want to obtain the total number of predictors. X.shape is like:
        # TensorShape([253, 11]). Second index [1] is the number of predictors:
        if (X is not None):
            # make sure it is a tensor:
            X = tf.constant(X)
            total_predictors = X.shape[1]
            # Convert to a TensorFlow integer object before storing:
            self.total_predictors = tf.int32(total_predictors)

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
        from sklearn.metrics import classification_report, confusion_matrix
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

        if (model_type == 'classification'):
            # Print meaning of classification metrics
            print("Metrics definitions:")
            print("True Positive (TP): the model correctly predicts a positive class output, i.e., it correctly predicts that the classified element belongs to that class (in binary classification, like in logistic regression, the model predicts the output 1 and the real output is also 1).")
            print("True Negative (TN): the model correctly predicts a negative class output, i.e., it correctly predicts that the classified element do not belong to that class (in binary classification, the model predicts the output 0 and the real output is also 0).")
            print("False Positive (FP, type 1 error): the model incorrectly predicts a positive class for a negative class-element, i.e., it predicts that the element belongs to that class, but it actually does not (in binary classification, the model predicts an output 1, but the correct output is 0).")
            print("False Negative (FN, type 2 error): the model incorrectly predicts a negative class for a positive class-element, i.e., it predicts that the element does not belong to that class, but it actually does (in binary classification, the model predicts an output 0, but the correct output is 1).")
            print("Naturally, the total number (TOTAL) of classifications is the sum of total correct predictions with total incorrect predictions, i.e., TOTAL = TP + TN + FP + FN")
            print("\n") # line break
            print("Accuracy: relation between the total number of correct classifications and the total number of classifications performed, i.e., Accuracy = (TP + TN)/(TOTAL)")
            print("Precision: it is referrent to the attempt of answering the question: \'What is the proportion of positive identifications that were actually correct?\'.")
            print("In other words, Precision is the relation between the number of true positives and the total of positively-labelled classifications (true and false positives), i.e., Precision = (TP)/(TP + FP)")
            print("Recall: it is referrent to the attempt of answering the question: \'What is the proportion of elements from positive class that were correctly classified?\'.")
            print("In other words, Recall is the relation between the number of true positives and the total of elements from the positive class (true positives and false negatives), i.e., Recall = (TP)/(TP + FN)")
            print("F1: is the ROC-AUC score. In a generic classification problem, this metric is representative of the capability of the model in distinguishing classes.")     
            print("F1 =2/((1/Precision)+(1/Recall)) = (2*(Precision)*(Recall))/(Precision + Recall)")
            print("\n") # line break
            # Check:
            # https://towardsdatascience.com/how-to-evaluate-your-machine-learning-models-with-python-code-5f8d2d8d945b
                  
            print("Confusion Matrix Interpretation:")
            print("The confusion matrix is a table commonly used for describing the performance of a classification model (a classifier). It visually compares the model outputs with the correct data labels.")
            print("The matrix is divided into several sectors. For a binary classifier, it is divided into 4 quadrants.")
            print("Each sector represents a given classification: in the vertical (Y) axis, the real observed labels are shown; whereas the predicted classes (model's outputs) are represented in the horizontal (X) axis.")
            print("Then, for each possible class, the following situations may happen: 1. The model predicted that the element belong to a given class, but it does not (incorrect prediction); or 2. The model predicted that the element belong to a given class, and it does (correct prediction).")
            print("If the output predicted y_pred (X-coordinate in the confusion matrix = y_pred) is the real label, then the Y-coordinate in the confusion matrix is also y_pred. For an element to have X and Y coordinates equal, it must be positioned on the principal diagonal of the matrix.")
            print("\n") #line break to highlight the next sentence
            print("So, we conclude that all the correct predictions of the model are positioned on the main or principal diagonal of the confusion matrix.")
            print("\n") # line break
            print("We also may conclude that an increase on model general accuracy is observed as an increase on the values shown in the main diagonal of the confusion matrix.")
            print("Notice that this interpretation takes in account a matrix organized starting from the bottom to the top of Y axis (i.e., lower classes on the origin), and from the left to the right of the X-axis, with lower classes closer to the origin. If the order was the opposite, then the secondary diagonal that would contain the correct predictions.")
            print("If we have N possible classifications, than we have N values on axis X, and N values in axis Y. So, we have N x N = N2 (N squared) sectors (values) in the confusion matrix.\n")
            print("Confusion matrix for a binary classifier:")
            print("For a binary classifier, we have to possible outputs: 0 (the origin of the matrix) and 1. In the vertical axis, 1 is the topper value; in the horizontal axis, 1 is the value on the extreme right (the positions more distant from the origin).")
            print("Since N = 2, we have 2 x 2 = 4 quadrants (sectors or values).Starting from the origin, clockwise, we have 4 situations:")
            print("Situation 1: X = 0 and Y = 0 - the model correctly predicted a negative output (it is a true negative prediction, TN).")
            print("Situation 2: X = 0 and Y = 1 - the model predicted a negative output for a positive class element (it is a false negative, FN).")
            print("Situation 3: X = 1 and Y = 1 - the model correctly predicted a positive class (TP).")
            print("Situation 4: X = 1 and Y = 0 - the model predicted a positive output for a negative class element (FP)\n")
            print("Each position of the confusion matrix represents the total of elements in each of the possible situations. Then, the sum of all values must be equal to the total of elements classified, and the relation between the sum of the main diagonal and the total of elements must be the accuracy.")
            print("So, use the confusion matrix to analyze the performance of the model in classifying each class, separately, and to observe the false negatives and false positives. Also, the confusion matrix will reveal if the classes are balanced, or ir a given class has much more elements than the other, what could impart the capability on differentiating the classes.")
            print("For some models, the proportion of false positives may be very different from the proportion of false negatives. It is not a problem, though, and depend on the application of the classifier.")
            print("It is an important situation that would be masked by the general metrics that take in account all the predictions, without seggregating them through the classes.")
            print("A classical example: suppose the classifier is used for predicting cancer. In this case, the model must have a proportion of false negatives much inferior than the proportion of false positives. That is because the risk associated to a false negative output is much higher.")
            print("A person who is incorrectly classified as having cancer will perform several more detailed exams to confirm the diagnosis, so the false positive may get detected without a great problem (in fact, the patient will probably feel good about it and keep taking care of the health). But a person incorrectly classified as not having cancer (when he has cancer) may feel comfortable, not taking care of his health and not making other exams (because he trusts the algorithm). Then, it may be too late when he founds out that was a false negative.")
            print("\n") # line break

            # AUC = Area under the curve
            print("AUC (Area under the curve) of the ROC (Receiver operating characteristic; default) or PR (Precision Recall) curves are quality measures of binary classifiers.\n")
                  

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
                    # Print with 6 decimals:
                    print(f"Mean squared error (MSE) = {mse:.6f}")
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
                    print(f"Root mean squared error (RMSE) = {rmse:.6f}")
                    # Add to calculated metrics:
                    calculated_metrics['rmse'] = rmse

                    # https://www.tensorflow.org/api_docs/python/tf/keras/metrics/mean_absolute_error?authuser=1
                    mae = tf.keras.metrics.mean_absolute_error(y_true, y_pred)
                    print(f"Mean absolute error (MAE) = {mae:.6f}")
                    # Add to calculated metrics:
                    calculated_metrics['mae'] = mae

                    # https://www.tensorflow.org/api_docs/python/tf/keras/metrics/mean_absolute_percentage_error?authuser=1
                    mape = tf.keras.metrics.mean_absolute_percentage_error(y_true, y_pred)
                    print(f"Mean absolute percentage error (MAPE) = {mape:.6f}")
                    # Add to calculated metrics:
                    calculated_metrics['mape'] = mape

                    # R2 and R2-adj are available only as tfa object:
                    # https://www.tensorflow.org/addons/api_docs/python/tfa/metrics/RSquare
                    # Create the object:
                    r2 = tfa.metrics.r_square.RSquare()
                    # Update its state:
                    r2 = r2.update_state(y_true, y_pred)
                    # Use the numpy method to retrieve only the value:
                    r2 = r2.numpy()
                    print(f"Coefficient of linear correlation R² = {r2:.6f}")
                    # Add to calculated metrics:
                    calculated_metrics['r_squared'] = r2

                    # Try to calculate the adjusted R² by accessing the number of predictors:
                    # This number may not be present.
                    try:
                        total_predictors = self.total_predictors
                        # Create the object:
                        r2_adj = tfa.metrics.r_square.RSquare(num_regressors = total_predictors)
                        # Update its state:
                        r2_adj = r2_adj.update_state(y_true, y_pred)
                        # Use the numpy method to retrieve only the value:
                        r2_adj = r2_adj.numpy()
                        print(f"Adjusted coefficient of correlation R²-adj = {r2_adj:.6f}")
                        # Add to calculated metrics:
                        calculated_metrics['r_squared_adj'] = r2_adj

                    except:
                        pass
                    
                    print("\n")
                    # Now, add the metrics to the metrics_dict:
                    metrics_dict[key] = calculated_metrics

                else:
                    
                    print(f"Metrics for {key}:\n")
                    # https://www.tensorflow.org/api_docs/python/tf/keras/metrics/AUC
                    # Create the object:
                    auc = tf.keras.metrics.AUC()
                    # Update its state:
                    auc = auc.update_state(y_true, y_pred)
                    # Use the numpy method to retrieve only the value:
                    auc = auc.result().numpy()
                    print(f"AUC = {auc:.4f}")
                    # Add to calculated metrics:
                    calculated_metrics['auc'] = auc

                    # https://www.tensorflow.org/api_docs/python/tf/keras/metrics/Accuracy
                    # Create the object:
                    acc = tf.keras.metrics.Accuracy()
                    # Update its state:
                    acc = acc.update_state(y_true, y_pred)
                    # Use the numpy method to retrieve only the value:
                    acc = acc.result().numpy()
                    print(f"Accuracy = {acc:.4f}")
                    # Add to calculated metrics:
                    calculated_metrics['accuracy'] = acc

                    # https://www.tensorflow.org/api_docs/python/tf/keras/metrics/Precision
                    # Create the object:
                    precision = tf.keras.metrics.Precision()
                    # Update its state:
                    precision = precision.update_state(y_true, y_pred)
                    # Use the numpy method to retrieve only the value:
                    precision = precision.result().numpy()
                    print(f"Precision = {precision:.4f}")
                    # Add to calculated metrics:
                    calculated_metrics['precision'] = precision

                    # https://www.tensorflow.org/api_docs/python/tf/keras/metrics/Recall
                    # Create the object:
                    recall = tf.keras.metrics.Recall()
                    # Update its state:
                    recall = recall.update_state(y_true, y_pred)
                    # Use the numpy method to retrieve only the value:
                    recall = recall.result().numpy()
                    print(f"Recall = {recall:.4f}")
                    # Add to calculated metrics:
                    calculated_metrics['recall'] = recall

                    # Get the classification report:
                    print("Classification Report:\n")
                    # Convert tensors to NumPy arrays
                    report = classification_report (y_true.numpy(), y_pred.numpy())

                    try:
                        # only works in Jupyter Notebook:
                        from IPython.display import display
                        display(report)
                    
                    except: # regular mode
                        print(report)
                    
                    # Add to calculated metrics:
                    calculated_metrics['classification_report'] = report

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

        if (model_class == 'linear'):

            if (column_map_dict is not None):
                # Retrieve the values (columns' names):
                columns_list = list(column_map_dict['features'].values())
                columns_list.append('intercept')
            
            # Get the list of coefficients. Apply the list method to convert the
            # array from .coef_ to a list:
            reg_coefficients = list(model.coef_)
            
            if (column_map_dict is None):
                # Retrieve the values (columns' names):
                columns_list = [i for i in range(0, len(reg_coefficients))]
                columns_list.append('intercept')

            # Append the intercept coefficient to this list:
            reg_coefficients.append(model.intercept_)
            
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


        elif (model_class == 'tree'):

            # Set the list of the predictors:
            # Use the list attribute to guarantee that it is a list:
            
            if (column_map_dict is not None):
                # Retrieve the values (columns' names):
                columns_list = list(column_map_dict['features'].values())
            
            # Get the list of feature importances. Apply the list method to convert the
            # array from .feature_importances_ to a list:
            feature_importances = list(model.feature_importances_)
            
            if (column_map_dict is None):
                # Retrieve the values (columns' names):
                columns_list = [i for i in range(0, len(feature_importances))]
            
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

          
        print("Feature importance ranking:\n")
            
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(feature_importance_df)
                    
        except: # regular mode
            print(feature_importance_df)
        
        # Save the feature importance ranking as a class variable (attribute):
        self.feature_importance_df = feature_importance_df

        features = feature_importance_df['predictive_features']
        
        if (model_class == 'linear'):
            importances = feature_importance_df['regression_coefficients']
            data_label = "linear_model_coefficients"
        
        elif (model_class == 'tree'):
            importances = feature_importance_df['feature_importances']
            data_label = "tree_model_feature_importance_ranking"

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
        train_metrics = history.history[metrics_name]
        val_metrics = history.history[val_metrics_name]
        
        train_loss = history.history['loss']
        val_loss = history.history['val_loss']

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
        ax1.plot(list_of_epochs, val_metrics, linestyle = "-", marker = '', color = 'crimson', alpha = OPACITY, label = "validation_metrics")
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
        ax2.plot(list_of_epochs, val_loss, linestyle = "-", marker = '', color = 'fuchsia', alpha = OPACITY, label = "validation_loss")
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

