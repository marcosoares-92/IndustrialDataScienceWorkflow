"""FUNCTIONS FROM INDUSTRIAL DATA SCIENCE WORKFLOW (IDSW) PACKAGE
Extract, transform, and load (ETL) data

Marco Cesar Prado Soares, Data Scientist Specialist @ Bayer Crop Science LATAM
marcosoares.feq@gmail.com
marco.soares@bayer.com

Aggregate dataframes and Manipulate Timestamps.
Characterize the dataset.
Transform the dataset.
Analyze the time series.
Seggregate the dataset and check for differences.
Process diagnosis: statistical process control charts and capability analysis."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from idsw.datafetch.core import InvalidInputsError
from .transform import (OrdinalEncoding_df, reverse_OrdinalEncoding)


class SPCChartAssistant:
    """
    Class for calling a visual assistant for helping the selection of the appropriate 
    Statistical Process Control (SPC) chart.

    def __init__(self, assistant_startup = True, keep_assistant_on = True)
    """ 

    # Initialize instance attributes.
    # define the Class constructor, i.e., how are its objects:
    def __init__ (self, assistant_startup = True, keep_assistant_on = True):
                
        import os
        
        # If the user passes the argument, use them. Otherwise, use the standard values.
        # Set the class objects' attributes.
        # Suppose the object is named assistant. We can access the attribute as:
        # assistant.assistant_startup, for instance.
        # So, we can save the variables as objects' attributes.
        self.assistant_startup = assistant_startup
        self.keep_assistant_on = keep_assistant_on
        # Base Github directory containing the assistant images to be downloaded:
        self.base_git_dir = "https://github.com/marcosoares-92/img_examples_guides/raw/main"
        # Create a new folder to store the images in local environment, 
        # if the folder do not exists:
        self.new_dir = "tmp"
        
        os.makedirs(self.new_dir, exist_ok = True)
        # exist_ok = True creates the directory only if it does not exist.
        
        self.last_img_number = 18 # number of the last image on the assistant
        self.numbers_to_end_assistant = (3, 4, 7, 9, 10, 13, 15, 16, 19, 20, 21, 22)
        # tuple: cannot be modified
        # 3: 'g', 4: 't', 7: 'i_mr', 9: 'std_error', 10: '3s', 13: 'x_bar_s'
        # 15: 'std_error' (grouped), 16: '3s' (grouped), 19: 'p', 20: 'np',
        # 21: 'c', 22: 'u'
        self.screen_number = 0 # start as zero
        self.file_to_fetch = ''
        self.img_url = ''
        self.img_local_path = ''
        # to check the class attributes, use the __dict__ method. Examples:
        ## object.__dict__ will show all attributes from object
                
    # Define the class methods.
    # All methods must take an object from the class (self) as one of the parameters
    

    def download_assistant_imgs (self):
                
        import os
        import shutil # component of the standard library to move or copy files.
        from html2image import Html2Image
                
        # Start the html object
        html_img = Html2Image()
                
        for screen_number in range(0, (self.last_img_number + 1)):
                
            # ranges from 0 to (last_img_number + 1) - 1 = last_img_number
            # convert the screen number to string to create the file name:
            
            # Update the attributes:
            self.file_to_fetch = "cc_s" + str(screen_number) + ".png"
            self.img_url = os.path.join(self.base_git_dir, self.file_to_fetch)
            
            # Download the image:
            # pypi.org/project/html2image/
            img = html_img.screenshot(url = self.img_url, save_as = self.file_to_fetch, size = (500, 500))
            # If size is omitted, the image is downloaded in the low-resolution default.
            # save_as must be a file name, a path is not accepted.
            # Make the output from the method equals to a variable eliminates its verbosity
                    
            # Create the new path for the image (local environment):
            self.img_local_path = os.path.join(self.new_dir, self.file_to_fetch)
            # Move the image files to the new paths:
            # use shutil.move(source, destination) method to move the files:
            # pynative.com/python-move-files
            # docs.python.org/3/library/shutil.html
            shutil.move(self.file_to_fetch, self.img_local_path)
            # Notice that file_to_fetch attribute still stores a file name like 'cc_s0.png'
        
        # Now, all images for the assistant were downloaded and stored in the temporary
        # folder. So, let's start the two boolean variables to initiate it and run it:
        self.assistant_startup = True 
        # attribute to start the assistant in the first screen
        self.keep_assistant_on = True
        # attribute to maintain the assistant working
        
        return self


    def delete_assistant_imgs (self):
                
        import os
        # Now, that the user closed the assistant, we can remove the downloaded files 
        # (delete them) from the notebook's workspace.
                
        # The os.remove function deletes a file or directory specified.
        for screen_number in range(0, (self.last_img_number + 1)):
                    
            self.file_to_fetch = "cc_s" + str(screen_number) + ".png"
            self.img_local_path = os.path.join(self.new_dir, self.file_to_fetch)
            os.remove(self.img_local_path)
                
        # Now that the files were removed, check if the tmp folder is empty:
        size = os.path.getsize(self.new_dir)
        # os.path.getsize returns the total size in Bytes from a folder or a file.
                
        # Get the list of sub-folders, files or subdirectories (the content) from the folder:
        list_of_contents = os.listdir(self.new_dir)
        # doc.python.org/3/library/os.html
        # It returns a list of strings representing the paths of each file or directory 
        # in the analyzed folder.
                
        # If the size is 0 and the length of the list_of_contents is also zero (i.e., there is no
        # previous sub-directory created), then remove the directory:
        if ((size == 0) & (len(list_of_contents) == 0)):
            
            os.rmdir(self.new_dir)


    def print_screen_legend (self):
        
        if (self.screen_number == 0):
            
            print("The control chart is a line graph showing a measure (y-axis) over time (x-axis).")
            
            print("In contrast to the run chart, the central line of the control chart represents the (weighted) mean, rather than the median.")
            print("Additionally, two lines representing the upper and lower control limits are shown.\n")
            print("The control limits represent the boundaries of the so-called common cause variation, which is inherent to the process.")
            print("Walther A. Shewhart, who invented the control chart, described two types of variation: chance-cause variation and assignable-cause variation.")
            print("These were later renamed to common-cause and special-cause variation.\n")
            
            print("Common-cause variation:")
            print("Is present in any process.")
            print("It is caused by phenomena that are always present within the system.")
            print("It makes the process predictable (within limits).")
            print("Common-cause variation is also called random variation or noise.\n")
                    
            print("Special-cause variation:")
            print("Is present in some processes.")
            print("It is caused by phenomena that are not normally present in the system.")
            print("It makes the process unpredictable.")
            print("Special-cause variation is also called non-random variation or signal.\n")
                    
            print("It is important to notice that neither common, nor special-cause variation is in itself 'good' or 'bad'.")
            print("A stable process may function at an unsatisfactory level; and an unstable process may be moving in the right direction.")
            print("On the other hand, the end goal of improvement is always to achieve a stable process functioning at a satisfactory level.\n")
                    
            print("Control chart limits:")
            print("The control limits, also called sigma limits, are usually placed at ±3 standard deviations from the central line.")
            print("So, the standard deviation is estimated as the common variation of the process of interest.")
            print("This variation depends on the theoretical distribution of data.")
            print("It is a beginner's mistake to simply calculate the standard deviation of all the data points.")
            print("This procedure would include both the common and special-cause variation in the calculus.")
            print("Since the calculations of control limits depend on the type of data (distribution), many types of control charts have been developed for specific purposes.")
        
        elif (self.screen_number == 1):
                    
            print("CHARTS FOR RARE EVENTS\n")
            print("ATTENTION: Due not previously group data in this case. Since events are rare, they are likely to be eliminated during aggregation.\n")
                    
            print("G-chart for units produced between (rare) defectives or defects;")
            print("or total events between successive rare occurrences:\n")
            print("When defects or defectives are rare and the subgroups are small, C, U, and P-charts become useless.")
            print("That is because most subgroups will have no defects.")
                    
            print("Example: if 8% of discharged patients have a hospitals-acquired pressure ulcer, and the average weekly number of discharges in a small department is 10, we would, on average, expect to have less than one pressure ulcer per week.")
            print("Instead, we could plot the number of discharges between each discharge of a patient with one or more pressure ulcers.\n")
            print("The number of units between defectives is modelled by the geometric distribution.")
            print("So, the G-control chart plots counting of occurrence by number; time unit; or timestamp.\n")
                    
            print("In the example of discharged patients: the indicator is the number of discharges between each of these rare cases.")
            print("Note that the first patient with pressure ulcer is missing from the chart.")
            print("It is due to the fact that we do not know how many discharges there had been before the first patient with detected pressure ulcer.\n")
            print("The central line of the G-chart is the theoretical median of the distribution")
            print("median = mean × 0.693")
                    
            print("Since the geometric distribution is highly skewed, the median is a better representation of the process center.")
            print("Also, notice that the G-chart rarely has a lower control limit.\n")
                    
            print("T-chart for time between successive rare events:\n")
            print("Like the G-chart, the T-chart is a rare event chart.")
            print("Instead of displaying the number of cases between events (defectives), this chart represents the time between successive rare events.\n")
            print("Since time is a continuous variable, the T-chart belongs with the other charts for measure numeric data.")
            print("Then, T-chart plots the timedelta (e.g. number of days between occurrences) by the measurement, time unit, or timestamp.")
                
        elif (self.screen_number == 2):
            
            print("A quality characteristic that is measured on a numerical scale is called a variable.")
            print("Examples: length or width, temperature, and volume.\n")
            
            print("The Shewhart control charts are widely used to monitor the mean and variability of variables.")
            print("On the other hand, many quality characteristics can be expressed in terms of a numerical measurement.")
                    
            print("For example: the diameter of a bearing could be measured with a micrometer and expressed in millimeters.\n")
            print("A single measurable quality characteristic, such as a dimension, weight, or volume, is a variable.")
            print("Control charts for variables are used extensively, and are one of the primary tools used in the analyze and control steps of DMAIC.")
            
            print("Many quality characteristics cannot be conveniently represented numerically, though.")
            print("In such cases, we usually classify each item inspected as either conforming or nonconforming to the specifications on that quality characteristic.")
            print("The terminology defective or non-defective is often used to identify these two classifications of product.")
            print("More recently, this terminology conforming and nonconforming has become popular.")        
            print("Quality characteristics of this type are called attributes.\n")
            
            print("Control Charts for Nonconformities (defects):")
            print("A nonconforming item is a unit of product that does not satisfy one or more of the specifications of that product.")
            print("Each specific point at which a specification is not satisfied results in a defect or nonconformity.")
            print("Consequently, a nonconforming item will contain at least one nonconformity.")
            print("However, depending on their nature and severity, it is quite possible for a unit to contain several nonconformities and not be classified as nonconforming.")
                    
            print("Example: suppose we are manufacturing personal computers. Each unit could have one or more very minor flaws in the cabinet finish,")
            print("but since these flaws do not seriously affect the unit's functional operation, it could be classified as conforming.")
            print("However, if there are too many of these flaws, the personal computer should be classified as nonconforming,")
            print("because the flaws would be very noticeable to the customer and might affect the sale of the unit.\n")
                    
            print("There are many practical situations in which we prefer to work directly with the number of defects or nonconformities,")
            print("rather than the fraction nonconforming.")
            print("These include:")
            print("1. Number of defective welds in 100 m of oil pipeline.")
            print("2. Number of broken rivets in an aircraft wing.")
            print("3. Number of functional defects in an electronic logic device.")
            print("4. Number of errors on a document, etc.\n")
                    
            print("It is possible to develop control charts for either the total number of nonconformities in a unit,")
            print("or for the average number of nonconformities per unit.\n")
            print("These control charts usually assume that the occurrence of nonconformities in samples of constant size is well modeled by the Poisson distribution.\n")
                    
            print("Essentially, this requires that the number of opportunities or potential locations for nonconformities be infinitely large;")
            print("and that the probability of occurrence of a nonconformity at any location be small and constant.")
            print("Furthermore, the inspection unit must be the same for each sample.")
            print("That is, each inspection unit must always represent an identical area of opportunity for the occurrence of nonconformities.")
                    
            print("In addition, we can count nonconformities of several different types on one unit, as long as the above conditions are satisfied for each class of nonconformity.\n")
            print("In most practical situations, these conditions will not be perfectly satisfied.")
            print("The number of opportunities for the occurrence of nonconformities may be finite,")
            print("or the probability of occurrence of nonconformities may not be constant.\n")
                    
            print("As long as these departures from the assumptions are not severe,")
            print("the Poisson model will usually work reasonably well.")
            print("There are cases, however, in which the Poisson model is completely inappropriate.")
            print("So, always check carefully the distributions.")
                    
            print("If you are not sure, use the estimates based on more general assumptions, i.e.,")
            print("The estimative of the natural variation as 3 times the standard deviation;")
            print("or as 3 times the standard error.\n")
                    
            print("Individual samples x Grouped data")
            print("Often, we collect a batch of samples corresponding to the same conditions, and use aggregation measurements such as mean, sum, or standard deviation to represent them.")
            print("In this case, we are grouping our data, and not working with individual measurements.")
            print("In turns, we can collect individual samples: there are no repetitions, only individual measurements corresponding to different conditions.\n")
            print("Usually, time series data is collected individually: each measurement corresponds to an instant, so it is not possible to collect multiple samples corresponding to the same conditions for further grouping.")
            print("Example: instant assessment of pH, temperature, pressure, etc.\n")
            print("Naturally, we can define a time window like a day, and group values on that window.")
            print("The dynamic of the phenomena should not create significant differences between samples collected for a same window, though.")
        
        elif (self.screen_number == 5):
            
            print("CHARTS FOR NUMERICAL VARIABLES\n")
            print("When dealing with a quality characteristic that is a variable, it is usually necessary to monitor both the mean value of the quality characteristic and its variability.")
            print("The control of the process average or mean quality level is usually done with the control chart for means, or the X-bar control chart.")
            print("The process variability can be monitored with either a control chart for the standard deviation, called the s control chart, or with a control chart for the range, called an R control chart.\n")
            
            print("I and MR charts for individual measurements:")
            print("ATTENTION: The I-MR chart can only be used for data that follows the normal distribution.")
            print("That is because the calculus of the control limits are based on the strong hypothesis of normality.")
            print("If you have individual samples that do not follow the normal curve (like skewed data, or data with high kurtosis);")
            print("or data with an unknown distribution, select number 8 for using less restrictive hypotheses for the estimative of the natural variation.\n")
                    
            print("Example: in healthcare, most quality data are count data.")
            print("However, from time to time, there are measurement data present.")
            print("These data are often in the form of physiological parameters or waiting times.")
            print("e.g. a chart of birth weights from 24 babies.")
            print("If the birth weights follow the normal, you can use the individuals chart.\n")
                    
            print("Actually, there are many situations in which the sample size used for process monitoring is n = 1; that is, the sample consists of an individual unit.")
            print("Some other examples of these situations are as follows:")
            print("1. Automated inspection and measurement technology is used, and every unit manufactured is analyzed.")
            print("So, there is no basis for rational subgrouping.")
            print("2. Data comes available relatively slowly, and it is inconvenient to allow sample sizes of n > 1 to accumulate before analysis.") 
            print("The long interval between observations will cause problems with rational subgrouping.")
            print("This occurs frequently in both manufacturing and non-manufacturing situations.")
            print("3. Repeat measurements on the process differ only because of laboratory or analysis error, as in many chemical processes.")
            print("4. Multiple measurements are taken on the same unit of product, such as measuring oxide thickness at several different locations on a wafer in semiconductor manufacturing.")
            print("5. In process plants, such as papermaking, measurements on some parameter (such as coating thickness across the roll) will differ very little and produce a standard deviation that is much too small if the objective is to control coating thickness along the roll.")
                    
            print("In such situations, the control chart for individual units is useful.")
            print("In many applications of the individuals control chart, we use the moving range two successive observations as the basis of estimating the process variability.\n")
            print("I-charts are often accompanied by moving range (MR) charts, which show the absolute difference between neighboring data points.")
            print("The purpose of the MR chart is to identify sudden changes in the (estimated) within-subgroup variation.")
            print("If any data point in the MR is above the upper control limit, one should interpret the I-chart very cautiously.\n")
        
        elif(self.screen_number == 6):
                    
            print("One important difference: numeric variables are representative of continuous data, usually in the form of real numbers (float values).")
            print("It means that its possible values cannot be counted: there is an infinite number of possible real values.")
            
            print("Categoric variables, in turn, are discrete.")        
            print("It means they can be counted, since there is a finite number of possibilities.")
            print("Such variables are usually present as strings (texts), or as ordinal (integer) numbers.")
                    
            print("If there are only two categories, we have a binary classification.")
            print("Each category can be reduced to a binary system: or the category is present, or it is not.")
            print("This is the idea for the One-Hot Encoding.")
            print("Usually, values in a binary classification are 1 or 0, so that a probability can be easily associated through the sigmoid function.\n")
                    
            print("Some examples of quality characteristics that are based on the analysis of attributes:")
            print("1. Proportion of warped automobile engine connecting rods in a day's production.")
            print("2. Number of nonfunctional semiconductor chips on a wafer.")
            print("3. Number of errors or mistakes made in completing a loan application.")
            print("4. Number of medical errors made in a hospital.\n")
        
        elif((self.screen_number == 8) | (self.screen_number == 14)):
            
            print("If you have a distribution that is not normal, like distributions with high skewness or high kurtosis,")
            print("use less restrictive methodologies to estimate the natural variation.\n")
                    
            print("You may estimate the natural variation as 3 times the standard error; or as 3 times the standard deviation.")
            print("The interval will be symmetric around the mean value.\n")
            print("Recommended: standard error, which normalizes by the total of values.")
                
        elif(self.screen_number == 11):
            
            print("CHARTS FOR NUMERICAL VARIABLES\n")
            print("When dealing with a quality characteristic that is a variable, it is usually necessary to monitor both the mean value of the quality characteristic and its variability.")
            print("The control of the process average or mean quality level is usually done with the control chart for means, or the X-bar control chart.")
            print("The process variability can be monitored with either a control chart for the standard deviation, called the s control chart, or with a control chart for the range, called an R control chart.\n")
                    
            print("X-bar and S charts for average measurements:")
            print("If there is more than one measurement of a numeric variable in each subgroup,")
            print("the Xbar and S charts will display the average and the within-subgroup standard deviation, respectively.")
            print("e.g. a chart of average birth weights per month, for babies born over last year.")
        
        elif(self.screen_number == 12):
            
            print("CHARTS FOR CATEGORICAL VARIABLES\n")
            print("There are 4 widely used attributes control charts: P, nP, U, and C.\n")
                    
            print("To illustrate them, consider a dataset containing the weekly number of patients that acquired pressure ulcers at a hospital.")
            print("The hospital has 300 patients, with an average length of stay of four days.") 
            print("Each of the dataframe's 24 rows contains information for one week on: the number of discharges,")
            print("patient days; pressure ulcers; and number of discharged patients with one or more pressure ulcers.")
            print("On average, 8% of discharged patients have 1.5 hospital acquired pressure ulcers.\n")
                    
            print("Some of the charts for categorical variables are based on the definition of the fraction nonconforming.")
            print("The fraction nonconforming is defined as the ratio between:")
            print("the number of nonconforming items in a population; by the total number of items in that population.")
            print("The items may have several quality characteristics that are examined simultaneously by the inspector.")
            print("If the item does not conform to the standards of one or more of these characteristics, it is classified as nonconforming.\n")
                    
            print("ATTENTION: Although it is customary to work with fraction nonconforming,")
            print("we could also analyze the fraction conforming just as easily, resulting in a control chart of process yield.")
            print("Many manufacturing organizations operate a yield-management system at each stage of their manufacturing process,")
            print("with the first-pass yield tracked on a control chart.\n")
            
            print("Traditionally, the term 'defect' has been used to name whatever it is being analyzed through counting with control charts.\n")
            print("There is a subtle, but important, distinction between:")
            print("counting defects, e.g. number of pressure ulcers;")
            print("and counting defectives, e.g. number of patients with one or more pressure ulcers.\n")
                    
            print("Defects are expected to reflect the Poisson distribution,")
            print("while defectives reflect the binomial distribution.\n")
        
        elif(self.screen_number == 17):
                    
            print("P-charts for proportion of defective units:")
            print("The first of these relates to the fraction of nonconforming or defective product produced by a manufacturing process, and is called the control chart for fraction nonconforming, or P-chart.")
            
            print("The P chart is probably the most common control chart in healthcare.")
            print("It is used to plot the proportion (or percent) of defective units.")
            print("e.g. the proportion of patients with one or more pressure ulcers.")
                    
            print("As mentioned, defectives are modelled by the binomial distribution.")
            print("In theory, the P chart is less sensitive to special cause variation than the U chart.")
            print("That is because it discards information by dichotomizing inspection units (patients) in defectives and non-defectives ignoring the fact that a unit may have more than one defect (pressure ulcers).")
            print("On the other hand, the P chart often communicates better.")
                    
            print("For most people, not to mention the press, the percent of harmed patients is easier to grasp than the rate of pressure ulcers expressed in counts per 1000 patient days.\n")
            print("The sample fraction nonconforming is defined as the ratio of the number of nonconforming units in the sample D to the sample size n:")
            print("p = D/n")
            print("From the binomial distribution, the mean should be estimated as p, and the variance s² as p(1-p)/n.")
                    
            print("nP-Charts for number nonconforming:")
            print("It is also possible to base a control chart on the number nonconforming,")
            print("rather than on the fraction nonconforming.")
            print("This is often called as number nonconforming (nP) control chart.\n")
            
        elif(self.screen_number == 18):
            
            print("C-charts for count of defects:")
            print("In some situations, it is more convenient to deal with the number of defects or nonconformities observed,")
            print("rather than the fraction nonconforming.\n")
            
            print("So, another type of control chart, called the control chart for nonconformities, or the C chart,")
            print("is designed to deal with this case.\n")
                    
            print("In the hospital example:")
            print("The correct control chart for the number of pressure ulcers is the C-chart,")
            print("which is based on the Poisson distribution.\n")
                    
            print("As mentioned, DEFECTIVES are modelled by the BINOMIAL distribution, whereas DEFECTS are modelled by POISSON distribution.\n")
            
            print("U-charts for rate of defects:")
            print("The control chart for nonconformities per unit, or the U-chart, is useful in situations")
            print("where the average number of nonconformities per unit is a more convenient basis for process control.\n")
                
            print("The U-chart is different from the C-chart in that it accounts for variation in the area of opportunity.")
            print("Examples:")
            print("1. Number of patients over time.")
            print("2. Number of patients between units one wishes to compare.")
            print("3. Number of patient days over time.")
            print("4. Number of patient days between units one wishes to compare.\n")
                 
            print("If there are many more patients in the hospital in the winter than in the summer,")
            print("the C-chart may falsely detect special cause variation in the raw number of pressure ulcers.\n")
            
            print("The U-chart plots the rate of defects.")
            print("A rate differs from a proportion in that the numerator and the denominator need not be of the same kind,")
            print("and that the numerator may exceed the denominator.\n")
                
            print("For example: the rate of pressure ulcers may be expressed as the number of pressure ulcers per 1000 patient days.\n")
            print("The larger the numerator, the narrower the control limits.\n")
            print("So, the main difference between U and C-charts is that U is based on the average number of nonconformities per inspection unit.\n")
            
            print("If we find x total nonconformities in a sample of n inspection units,")
            print("then the average number of nonconformities per inspection unit will be:")
            print("u = x/n")
            print("\n")


    def open_chart_assistant_screen (self):
                
        import os
        from html2image import Html2Image
        from tensorflow.keras.preprocessing.image import img_to_array, load_img
        # img_to_array: convert the image into its numpy array representation
                
        if (self.assistant_startup): #run if it is True:
            
            self.screen_number = 0 # first screen
        
        if (self.screen_number not in self.numbers_to_end_assistant):
            
            self.print_screen_legend()
            # Use its own method
            
            # Update attributes:
            self.file_to_fetch = "cc_s" + str(self.screen_number) + ".png"
            # Obtain the path of the image (local environment):
            self.img_local_path = os.path.join(self.new_dir, self.file_to_fetch)
                    
            # Load the image and save it on variables:
            assistant_screen = load_img(self.img_local_path)
                    
            # show image with plt.imshow function:
            fig = plt.figure(figsize = (12, 8))
            plt.imshow(assistant_screen)
            # If the image is black and white, you can color it with a cmap as fig.set_cmap('hot')
            
            #set axis off:
            plt.axis('off')
            plt.show()
            print("\n")
            
            # Run again the assistant for next screen (keep assistant on):
            self.keep_assistant_on = True
            # In the next round, the assistant should not be restarted:
            self.assistant_startup = False
            
            screen_number = input("Enter the number you wish here (in the right), according to the shown in the image above: ")
            #convert the screen number to string:
            screen_number = str(screen_number)        
            # Strip spaces and format characters (trim):
            screen_number = screen_number.strip()        
            # We do not call the str attribute for string variables (only for iterables)
            # Convert to integer
            screen_number = int(screen_number)
            # Update the attribute:
            self.screen_number = screen_number
        
        else:
            
            # user selected a value that ends the assistant:
            self.keep_assistant_on = False
            self.assistant_startup = False
        
        # Return the booleans to the main function:
        return self


    def chart_selection (self):
                
        # Only if the screen is in the tuple numbers_to_end_assistant:
        if (self.screen_number in self.numbers_to_end_assistant):
                    
            # Variables are created only when requested:
            rare_events_tuple = (3, 4) # g, t
            continuous_dist_not_defined_tuple = (9, 10) # std_error, 3std
            grouped_dist_not_defined_tuple = (15, 16) # std_error, 3std
            grouped_tuple = (13, 19, 20, 21, 22) # x, p, np, c, u
            charts_map_dict = {3:'g', 4:'t', 7:'i_mr', 9:'std_error', 10:'3s_as_natural_variation',
                                13:'xbar_s', 15:'std_error', 16:'3s_as_natural_variation',
                                19:'p', 20:'np', 21:'c', 22:'u'}
                    
            chart_to_use = charts_map_dict[self.screen_number]
                    
            # Variable with subgroups, which will be updated if needed:
            column_with_labels_or_subgroups = None
                    
            # Variable for skewed distribution, which will be updated if needed:
            consider_skewed_dist_when_estimating_with_std = False
                    
            column_with_variable_to_be_analyzed = str(input("Enter here (in the right) the name or number of the column (its header) that will be analyzed with the control chart.\nDo not type it in quotes.\nKeep the exact same format of the dataset, with spaces, characters, upper and lower cases, etc (or an error will be raised): "))
            # Try to convert it to integer, if it is a number:
            try:
                # Clean the string:
                column_with_variable_to_be_analyzed = column_with_variable_to_be_analyzed.strip()
                column_with_variable_to_be_analyzed = int(column_with_variable_to_be_analyzed)
                    
            except: # simply pass
                pass
                    
            print("\n")
            
            yes_no = str(input("Do your data have a column containing timestamps or time indication (event order)?\nType yes or no, here (in the right).\nDo not type it in quotes: "))
            yes_no = yes_no.strip()        
            # convert to full lower case, independently of the user:
            yes_no = yes_no.lower()
                    
            if (yes_no == 'yes'):
                    
                print("\n")
                timestamp_tag_column = str(input("Enter here (in the right) the name or number of the column containing timestamps or time indication (event order).\nDo not type it in quotes.\nKeep the exact same format of the dataset, with spaces, characters, upper and lower cases, etc (or an error will be raised): "))
                
                # Try to convert it to integer, if it is a number:
                try:
                    timestamp_tag_column = timestamp_tag_column.strip()
                    timestamp_tag_column = int(timestamp_tag_column)
                        
                except: # simply pass
                    pass
                    
            else:
                timestamp_tag_column = None
                    
            yes_no = str(input("Do your data have a column containing event frame indication; indication for separating time windows for comparison analysis;\nstages; events to be analyzed separately; or any other indication for slicing the time axis for comparison of different means, variations, etc?\nType yes or no, here (in the right).\nDo not type it in quotes: "))
            yes_no = yes_no.strip()
            yes_no = yes_no.lower()
                    
            if (yes_no == 'yes'):
                        
                print("\n")
                column_with_event_frame_indication = str(input("Enter here (in the right) the name or number of the column containing the event frame indication.\nDo not type it in quotes.\nKeep the exact same format of the dataset, with spaces, characters, upper and lower cases, etc (or an error will be raised): "))
                        
                # Try to convert it to integer, if it is a number:
                try:
                    column_with_event_frame_indication = column_with_event_frame_indication.strip()
                    column_with_event_frame_indication = int(column_with_event_frame_indication)
                        
                except: # simply pass
                    pass
            
            else:
                column_with_event_frame_indication = None
                    
            if (self.screen_number in rare_events_tuple):
                        
                print("\n")
                print(f"How are the rare events represented in the column {column_with_variable_to_be_analyzed}?")
                print(f"Before obtaining the chart, you must have modified the {column_with_variable_to_be_analyzed} to labe these data.")
                print("The function cannot work with boolean filters. So, if a value corresponds to a rare event occurrence, modify its value to properly labelling it.")
                print("You can set a special string or a special numeric value for indicating that a particular row corresponds to a rare event.")
                print("That is because rare events occurrences must be compared against all other 'regular' events.")
                print(f"For instance, {column_with_variable_to_be_analyzed} may show a value like 'rare_event', or 'ulcer' (in our example) if it is a rare occurrence.")
                print("Also, you could input a value extremely high, like 1000000000, or extremely low, like -10000000 for marking the rare events in the column.")
                print("The chart will be obtained after finding these rare events marks on the column.\n")
                        
                rare_event_indication = str(input(f"How are the rare events represented in the column {column_with_variable_to_be_analyzed}?\nEnter here (in the right) the text or number representing a rare event.\nDo not type it in quotes.\nKeep the exact same format of the dataset, with spaces, characters, upper and lower cases, etc (or the rare events will not be localized in the dataset): "))
                        
                # Try to convert it to float, if it is a number:
                try:
                    column_with_event_frame_indication = column_with_event_frame_indication.strip()
                    column_with_event_frame_indication = float(column_with_event_frame_indication)
                
                except: # simply pass
                    pass
                        
                rare_event_timedelta_unit = str(input(f"What is the usual order of magnitude for the intervals (timedeltas) between rare events?\nEnter here (in the right).\nYou may type: year, month, day, hour, minute, or second.\nDo not type it in quotes: "))
                rare_event_timedelta_unit = rare_event_timedelta_unit.strip()
                rare_event_timedelta_unit = rare_event_timedelta_unit.lower()
                
                while (rare_event_timedelta_unit not in ['year', 'month', 'day', 'hour', 'minute', 'second']):
                    
                    rare_event_timedelta_unit = str(input("Please, enter a valid timedelta unit: year, month, day, hour, minute, or second.\nDo not type it in quotes: "))
                    rare_event_timedelta_unit = rare_event_timedelta_unit.strip()
                    rare_event_timedelta_unit = rare_event_timedelta_unit.lower()
                    
            else:
                
                rare_event_timedelta_unit = None
                rare_event_indication = None
                        
                if ((self.screen_number in grouped_dist_not_defined_tuple) | (self.screen_number in grouped_tuple)):
                            
                    print("\n")
                    column_with_labels_or_subgroups = str(input("Enter here (in the right) the name or number of the column containing the subgroups or samples for aggregating the measurements in terms of mean, standard deviation, etc.\nIt may be a column with indications like 'A', 'B', or 'C'; 'subgroup1',..., 'sample1',..., or an integer like 1, 2, 3,...\nThis column will allow grouping of rows in terms of the correspondent samples.\nDo not type it in quotes.\nKeep the exact same format of the dataset, with spaces, characters, upper and lower cases, etc (or an error will be raised): "))
                            
                    # Try to convert it to integer, if it is a number:
                    try:
                        column_with_labels_or_subgroups = column_with_labels_or_subgroups.strip()
                        column_with_labels_or_subgroups = int(column_with_labels_or_subgroups)
                    
                    except: # simply pass
                        pass
                
                if ((self.screen_number in grouped_dist_not_defined_tuple) | (self.screen_number in continuous_dist_not_defined_tuple)):
                            
                    print("\n")
                    print("Is data skewed or with high kurtosis? If it is, the median will be used as the central line estimative.")
                    print("median = mean × 0.693\n")
                            
                    yes_no = str(input("Do you want to assume a skewed (or with considerable kurtosis) distribution?\nType yes or no, here (in the right).\nDo not type it in quotes: "))
                    yes_no = yes_no.strip()
                    yes_no = yes_no.lower()
                            
                    if (yes_no == 'yes'):
                        
                        # update the boolean variable
                        consider_skewed_dist_when_estimating_with_std = True
                
                
            print("Finished mapping the variables for obtaining the control chart plots.")
            print("If an error is raised; or if the chart is not complete, check if the columns' names inputs are strictly correct.\n")
            
            return chart_to_use, column_with_labels_or_subgroups, consider_skewed_dist_when_estimating_with_std, column_with_variable_to_be_analyzed, timestamp_tag_column, column_with_event_frame_indication, rare_event_timedelta_unit, rare_event_indication


class SPCPlot:
    """
    Class for obtaining Statistical Process Control (SPC) Charts for different cases, as well
    as identifying outliers and point out of specification ranges.

    def __init__ (self, dictionary, column_with_variable_to_be_analyzed, timestamp_tag_column, chart_to_use, column_with_labels_or_subgroups = None, consider_skewed_dist_when_estimating_with_std = False, rare_event_indication = None, rare_event_timedelta_unit = 'day'):  
    """

    # Initialize instance attributes.
    # define the Class constructor, i.e., how are its objects:
    def __init__ (self, dictionary, column_with_variable_to_be_analyzed, timestamp_tag_column, chart_to_use, column_with_labels_or_subgroups = None, consider_skewed_dist_when_estimating_with_std = False, rare_event_indication = None, rare_event_timedelta_unit = 'day'):
                
        # If the user passes the argument, use them. Otherwise, use the standard values.
        # Set the class objects' attributes.
        # Suppose the object is named plot. We can access the attribute as:
        # plot.dictionary, for instance.
        # So, we can save the variables as objects' attributes.
        self.dictionary = dictionary
        self.df = self.dictionary['df']
        # Start the attribute number of labels with value 2 (correspondent to moving range)
        self.number_of_labels = 2
        # List the possible numeric data types for a Pandas dataframe column:
        self.numeric_dtypes = [np.int16, np.int32, np.int64, np.float16, np.float32, np.float64]
        # Start a dictionary of constants
        self.dict_of_constants = {}
        self.column_with_variable_to_be_analyzed = column_with_variable_to_be_analyzed
        # Indicate which is the timestamp column:
        self.timestamp_tag_column = timestamp_tag_column
        # Set the chart 
        self.chart_to_use = chart_to_use
        
        # Other arguments of the constructor (attributes):
        # These ones have default values to use if omitted when creating the object
        self.column_with_labels_or_subgroups = column_with_labels_or_subgroups
        self.consider_skewed_dist_when_estimating_with_std = consider_skewed_dist_when_estimating_with_std
        self.rare_event_indication = rare_event_indication 
        self.rare_event_timedelta_unit = rare_event_timedelta_unit
        # to check the class attributes, use the __dict__ method. Examples:
        ## object.__dict__ will show all attributes from object
                
    # Define the class methods.
    # All methods must take an object from the class (self) as one of the parameters
   
    # Define a dictionary of constants.
    # Each key in the dictionary corresponds to a number of samples in a subgroup.
    # number_of_labels - This variable represents the total of labels or subgroups n. 
    # If there are multiple labels, this variable will be updated later.
    

    def get_constants (self):
        
        if (self.number_of_labels < 2):
            
            self.number_of_labels = 2
            
        if (self.number_of_labels <= 25):
            
            dict_of_constants = {
                
                2: {'A':2.121, 'A2':1.880, 'A3':2.659, 'c4':0.7979, '1/c4':1.2533, 'B3':0, 'B4':3.267, 'B5':0, 'B6':2.606, 'd2':1.128, '1/d2':0.8865, 'd3':0.853, 'D1':0, 'D2':3.686, 'D3':0, 'D4':3.267},
                3: {'A':1.732, 'A2':1.023, 'A3':1.954, 'c4':0.8862, '1/c4':1.1284, 'B3':0, 'B4':2.568, 'B5':0, 'B6':2.276, 'd2':1.693, '1/d2':0.5907, 'd3':0.888, 'D1':0, 'D2':4.358, 'D3':0, 'D4':2.574},
                4: {'A':1.500, 'A2':0.729, 'A3':1.628, 'c4':0.9213, '1/c4':1.0854, 'B3':0, 'B4':2.266, 'B5':0, 'B6':2.088, 'd2':2.059, '1/d2':0.4857, 'd3':0.880, 'D1':0, 'D2':4.698, 'D3':0, 'D4':2.282},
                5: {'A':1.342, 'A2':0.577, 'A3':1.427, 'c4':0.9400, '1/c4':1.0638, 'B3':0, 'B4':2.089, 'B5':0, 'B6':1.964, 'd2':2.326, '1/d2':0.4299, 'd3':0.864, 'D1':0, 'D2':4.918, 'D3':0, 'D4':2.114},
                6: {'A':1.225, 'A2':0.483, 'A3':1.287, 'c4':0.9515, '1/c4':1.0510, 'B3':0.030, 'B4':1.970, 'B5':0.029, 'B6':1.874, 'd2':2.534, '1/d2':0.3946, 'd3':0.848, 'D1':0, 'D2':5.078, 'D3':0, 'D4':2.004},
                7: {'A':1.134, 'A2':0.419, 'A3':1.182, 'c4':0.9594, '1/c4':1.0423, 'B3':0.118, 'B4':1.882, 'B5':0.113, 'B6':1.806, 'd2':2.704, '1/d2':0.3698, 'd3':0.833, 'D1':0.204, 'D2':5.204, 'D3':0.076, 'D4':1.924},
                8: {'A':1.061, 'A2':0.373, 'A3':1.099, 'c4':0.9650, '1/c4':1.0363, 'B3':0.185, 'B4':1.815, 'B5':0.179, 'B6':1.751, 'd2':2.847, '1/d2':0.3512, 'd3':0.820, 'D1':0.388, 'D2':5.306, 'D3':0.136, 'D4':1.864},
                9: {'A':1.000, 'A2':0.337, 'A3':1.032, 'c4':0.9693, '1/c4':1.0317, 'B3':0.239, 'B4':1.761, 'B5':0.232, 'B6':1.707, 'd2':2.970, '1/d2':0.3367, 'd3':0.808, 'D1':0.547, 'D2':5.393, 'D3':0.184, 'D4':1.816},
                10: {'A':0.949, 'A2':0.308, 'A3':0.975, 'c4':0.9727, '1/c4':1.0281, 'B3':0.284, 'B4':1.716, 'B5':0.276, 'B6':1.669, 'd2':3.078, '1/d2':0.3249, 'd3':0.797, 'D1':0.687, 'D2':5.469, 'D3':0.223, 'D4':1.777},
                11: {'A':0.905, 'A2':0.285, 'A3':0.927, 'c4':0.9754, '1/c4':1.0252, 'B3':0.321, 'B4':1.679, 'B5':0.313, 'B6':1.637, 'd2':3.173, '1/d2':0.3152, 'd3':0.787, 'D1':0.811, 'D2':5.535, 'D3':0.256, 'D4':1.744},
                12: {'A':0.866, 'A2':0.266, 'A3':0.886, 'c4':0.9776, '1/c4':1.0229, 'B3':0.354, 'B4':1.646, 'B5':0.346, 'B6':1.610, 'd2':3.258, '1/d2':0.3069, 'd3':0.778, 'D1':0.922, 'D2':5.594, 'D3':0.283, 'D4':1.717},
                13: {'A':0.832, 'A2':0.249, 'A3':0.850, 'c4':0.9794, '1/c4':1.0210, 'B3':0.382, 'B4':1.618, 'B5':0.374, 'B6':1.585, 'd2':3.336, '1/d2':0.2998, 'd3':0.770, 'D1':1.025, 'D2':5.647, 'D3':0.307, 'D4':1.693},
                14: {'A':0.802, 'A2':0.235, 'A3':0.817, 'c4':0.9810, '1/c4':1.0194, 'B3':0.406, 'B4':1.594, 'B5':0.399, 'B6':1.563, 'd2':3.407, '1/d2':0.2935, 'd3':0.763, 'D1':1.118, 'D2':5.696, 'D3':0.328, 'D4':1.672},
                15: {'A':0.775, 'A2':0.223, 'A3':0.789, 'c4':0.9823, '1/c4':1.0180, 'B3':0.428, 'B4':1.572, 'B5':0.421, 'B6':1.544, 'd2':3.472, '1/d2':0.2880, 'd3':0.756, 'D1':1.203, 'D2':5.741, 'D3':0.347, 'D4':1.653},
                16: {'A':0.750, 'A2':0.212, 'A3':0.763, 'c4':0.9835, '1/c4':1.0168, 'B3':0.448, 'B4':1.552, 'B5':0.440, 'B6':1.526, 'd2':3.532, '1/d2':0.2831, 'd3':0.750, 'D1':1.282, 'D2':5.782, 'D3':0.363, 'D4':1.637},
                17: {'A':0.728, 'A2':0.203, 'A3':0.739, 'c4':0.9845, '1/c4':1.0157, 'B3':0.466, 'B4':1.534, 'B5':0.458, 'B6':1.511, 'd2':3.588, '1/d2':0.2787, 'd3':0.744, 'D1':1.356, 'D2':5.820, 'D3':0.378, 'D4':1.622},
                18: {'A':0.707, 'A2':0.194, 'A3':0.718, 'c4':0.9854, '1/c4':1.0148, 'B3':0.482, 'B4':1.518, 'B5':0.475, 'B6':1.496, 'd2':3.640, '1/d2':0.2747, 'd3':0.739, 'D1':1.424, 'D2':5.856, 'D3':0.391, 'D4':1.608},
                19: {'A':0.688, 'A2':0.187, 'A3':0.698, 'c4':0.9862, '1/c4':1.0140, 'B3':0.497, 'B4':1.503, 'B5':0.490, 'B6':1.483, 'd2':3.689, '1/d2':0.2711, 'd3':0.734, 'D1':1.487, 'D2':5.891, 'D3':0.403, 'D4':1.597},
                20: {'A':0.671, 'A2':0.180, 'A3':0.680, 'c4':0.9869, '1/c4':1.0133, 'B3':0.510, 'B4':1.490, 'B5':0.504, 'B6':1.470, 'd2':3.735, '1/d2':0.2677, 'd3':0.729, 'D1':1.549, 'D2':5.921, 'D3':0.415, 'D4':1.585},
                21: {'A':0.655, 'A2':0.173, 'A3':0.663, 'c4':0.9876, '1/c4':1.0126, 'B3':0.523, 'B4':1.477, 'B5':0.516, 'B6':1.459, 'd2':3.778, '1/d2':0.2647, 'd3':0.724, 'D1':1.605, 'D2':5.951, 'D3':0.425, 'D4':1.575},
                22: {'A':0.640, 'A2':0.167, 'A3':0.647, 'c4':0.9882, '1/c4':1.0119, 'B3':0.534, 'B4':1.466, 'B5':0.528, 'B6':1.448, 'd2':3.819, '1/d2':0.2618, 'd3':0.720, 'D1':1.659, 'D2':5.979, 'D3':0.434, 'D4':1.566},
                23: {'A':0.626, 'A2':0.162, 'A3':0.633, 'c4':0.9887, '1/c4':1.0114, 'B3':0.545, 'B4':1.455, 'B5':0.539, 'B6':1.438, 'd2':3.858, '1/d2':0.2592, 'd3':0.716, 'D1':1.710, 'D2':6.006, 'D3':0.443, 'D4':1.557},
                24: {'A':0.612, 'A2':0.157, 'A3':0.619, 'c4':0.9892, '1/c4':1.0109, 'B3':0.555, 'B4':1.445, 'B5':0.549, 'B6':1.429, 'd2':3.895, '1/d2':0.2567, 'd3':0.712, 'D1':1.759, 'D2':6.031, 'D3':0.451, 'D4':1.548},
                25: {'A':0.600, 'A2':0.153, 'A3':0.606, 'c4':0.9896, '1/c4':1.0105, 'B3':0.565, 'B4':1.435, 'B5':0.559, 'B6':1.420, 'd2':3.931, '1/d2':0.2544, 'd3':0.708, 'D1':1.806, 'D2':6.056, 'D3':0.459, 'D4':1.541},
            }
            
            # Access the key:
            dict_of_constants = dict_of_constants[self.number_of_labels]
            
        else: #>= 26
            
            dict_of_constants = {'A':(3/(self.number_of_labels**(0.5))), 'A2':0.153, 
                                 'A3':3/((4*(self.number_of_labels-1)/(4*self.number_of_labels-3))*(self.number_of_labels**(0.5))), 
                                 'c4':(4*(self.number_of_labels-1)/(4*self.number_of_labels-3)), 
                                 '1/c4':1/((4*(self.number_of_labels-1)/(4*self.number_of_labels-3))), 
                                 'B3':(1-3/(((4*(self.number_of_labels-1)/(4*self.number_of_labels-3)))*((2*(self.number_of_labels-1))**(0.5)))), 
                                 'B4':(1+3/(((4*(self.number_of_labels-1)/(4*self.number_of_labels-3)))*((2*(self.number_of_labels-1))**(0.5)))),
                                 'B5':(((4*(self.number_of_labels-1)/(4*self.number_of_labels-3)))-3/((2*(self.number_of_labels-1))**(0.5))), 
                                 'B6':(((4*(self.number_of_labels-1)/(4*self.number_of_labels-3)))+3/((2*(self.number_of_labels-1))**(0.5))), 
                                 'd2':3.931, '1/d2':0.2544, 'd3':0.708, 'D1':1.806, 'D2':6.056, 'D3':0.459, 'D4':1.541}
        
        # Update the attribute
        self.dict_of_constants = dict_of_constants
        
        return self
    

    def chart_i_mr (self):
        
        # access the dataframe:
        
        dictionary = self.dictionary
        df = self.df
        column_with_variable_to_be_analyzed = self.column_with_variable_to_be_analyzed
        
        # CONTROL LIMIT EQUATIONS:
        # X-bar = (sum of measurements)/(number of measurements)
        # R = Absolute value of [(largest in subgroup) - (lowest in subgroup)]
        # Individual chart: subgroup = 1
        # R = Absolute value of [(data) - (next data)]
        # R-bar = (sum of ranges R)/(number of R values calculated)
        # Lower control limit (LCL) = X-bar - (2.66)R-bar
        # Upper control limit (UCL) = X-bar + (2.66)R-bar
        
        # loop through each row from df, starting from the second (row 1):    
        # calculate mR as the difference (Xmax - Xmin) of the difference between
        # df[column_with_variable_to_be_analyzed] on row i and the row
        # i-1. Since we do not know, in principle, which one is the maximum, we can use
        # the max and min functions from Python:
        # https://www.w3schools.com/python/ref_func_max.asp
        # https://www.w3schools.com/python/ref_func_min.asp
        # Also, the moving range here must be calculated as an absolute value
        # https://www.w3schools.com/python/ref_func_abs.asp
        
        moving_range = [abs(max((df[column_with_variable_to_be_analyzed][i]), (df[column_with_variable_to_be_analyzed][(i-1)])) - min((df[column_with_variable_to_be_analyzed][i]), (df[column_with_variable_to_be_analyzed][(i-1)]))) for i in range (1, len(df))]
        x_bar_list = [(df[column_with_variable_to_be_analyzed][i] + df[column_with_variable_to_be_analyzed][(i-1)])/2 for i in range (1, len(df))]
        
        # These lists were created from index 1. We must add a initial element to
        # make their sizes equal to the original dataset length
        # Start the list to store the moving ranges, containing only the number 0
        # for the moving range (by simple concatenation):
        moving_range = [0] + moving_range
        
        # Start the list that stores the mean values of the 2-elements subgroups
        # with the first element itself (index 0):
        x_bar_list = [df[column_with_variable_to_be_analyzed][0]] + x_bar_list
        
        # Save the moving ranges as a new column from df (it may be interesting to check it):
        df['moving_range'] = moving_range
        
        # Save x_bar_list as the column to be analyzed:
        df[column_with_variable_to_be_analyzed] = x_bar_list
        
        # Get the mean values from x_bar:
        x_bar_bar = df[column_with_variable_to_be_analyzed].mean()
        
        # Calculate the mean value of the column moving_range, and save it as r_bar.
        r_bar = df['moving_range'].mean()
        
        # Get the control chart constant A2 from the dictionary, considering n = 2 the
        # number of elements of each subgroup:
        # Apply the get_constants method to update the dict_of_constants attribute:
        self = self.get_constants()
        
        control_chart_constant = self.dict_of_constants['1/d2']
        control_chart_constant = control_chart_constant * 3
        
        # calculate the upper control limit as x_bar + (3/d2)r_bar:
        upper_cl = x_bar_bar + (control_chart_constant) * (r_bar)
        
        # add a column 'upper_cl' on the dataframe with this value:
        df['upper_cl'] = upper_cl
        
        # calculate the lower control limit as x_bar - (3/d2)r_bar:
        lower_cl = x_bar_bar - (control_chart_constant) * (r_bar)
        
        # add a column 'lower_cl' on the dataframe with this value:
        df['lower_cl'] = lower_cl
        
        # Add a column with the mean value of the considered interval:
        df['center'] = x_bar_bar
        
        # Update the dataframe in the dictionary and return it:
        dictionary['df'] = df
        
        # Update the attributes:
        self.dictionary = dictionary
        self.df = df
        
        return self


    def chart_3s (self):
        
        dictionary = self.dictionary
        df = self.df
        column_with_variable_to_be_analyzed = self.column_with_variable_to_be_analyzed
        
        if(self.consider_skewed_dist_when_estimating_with_std):
            
            # Skewed data. Use the median:
            center = df[column_with_variable_to_be_analyzed].median()
            
        else:
            
            center = dictionary['center']
            
        # calculate the upper control limit as the mean + 3s
        upper_cl = center + 3 * (dictionary['std'])
        
        # add a column 'upper_cl' on the dataframe with this value:
        df['upper_cl'] = upper_cl
        
        # calculate the lower control limit as the mean - 3s:
        lower_cl = center - 3 * (dictionary['std'])
        
        # add a column 'lower_cl' on the dataframe with this value:
        df['lower_cl'] = lower_cl
        
        # Add a column with the mean value of the considered interval:
        df['center'] = center
        
        # Update the dataframe in the dictionary:
        dictionary['df'] = df
        
        # Update the attributes:
        self.dictionary = dictionary
        self.df = df
        
        return self


    def chart_std_error (self):
        
        dictionary = self.dictionary
        df = self.df
        column_with_variable_to_be_analyzed = self.column_with_variable_to_be_analyzed
        
        n_samples = df[column_with_variable_to_be_analyzed].count()
        
        s = dictionary['std']
        std_error = s/(n_samples**(0.5))
        
        if(self.consider_skewed_dist_when_estimating_with_std):
            
            # Skewed data. Use the median:
            center = df[column_with_variable_to_be_analyzed].median()
            
        else:
            
            center = dictionary['center']
            
        # calculate the upper control limit as the mean + 3 std_error
        upper_cl = center + 3 * (std_error)
        
        # add a column 'upper_cl' on the dataframe with this value:
        df['upper_cl'] = upper_cl
        
        # calculate the lower control limit as the mean - 3 std_error:
        lower_cl = center - 3 * (std_error)
        
        # add a column 'lower_cl' on the dataframe with this value:
        df['lower_cl'] = lower_cl
        
        # Add a column with the mean value of the considered interval:
        df['center'] = center
        
        # Update the dataframe in the dictionary:
        dictionary['df'] = df
        
        # Update the attributes:
        self.dictionary = dictionary
        self.df = df
        
        return self
        

    # CONTROL CHARTS FOR SUBGROUPS 
    
    def create_grouped_df (self):
        
        from scipy import stats
        
        dictionary = self.dictionary
        df = self.df
        column_with_variable_to_be_analyzed = self.column_with_variable_to_be_analyzed
        column_with_labels_or_subgroups = self.column_with_labels_or_subgroups
        numeric_dtypes = self.numeric_dtypes
           
        # We need to group each dataframe in terms of the subgroups stored in the variable
        # column_with_labels_or_subgroups.
        # The catehgorical or datetime columns must be aggregated in terms of mode.
        # The numeric variables must be aggregated both in terms of mean and in terms of count
        # (subgroup size)
        
        # 1. Start a list for categorical columns and other for numeric columns:
        categorical_cols = []
        numeric_cols = []
        
        # Variables to map if there are categorical or numeric variables:
        is_categorical = 0
        is_numeric = 0
        
        # 2. Loop through each column from the list of columns of the dataframe:
        for column in list(df.columns):
            
            # check the type of column:
            column_data_type = df[column].dtype
            
            if (column_data_type not in numeric_dtypes):
                
                # If the Pandas series was defined as an object, it means it is categorical
                # (string, date, etc). Also, this if captures the variables converted to datetime64
                # Append the column to the list of categorical columns:
                categorical_cols.append(column)
                
            else:
                # append the column to the list of numeric columns:
                numeric_cols.append(column)
                
        # 3. Check if column_with_labels_or_subgroups is in both lists. 
        # If it is missing, append it. We need that this column in all subsets for grouping.
        if (column_with_labels_or_subgroups not in categorical_cols):
            
            categorical_cols.append(column_with_labels_or_subgroups)
        
        if (column_with_labels_or_subgroups not in numeric_cols):
            
            numeric_cols.append(column_with_labels_or_subgroups)
        
        if (len(categorical_cols) > 1):    
            # There is at least one column plus column_with_labels_or_subgroups:
            is_categorical = 1
            
        if (len(numeric_cols) > 1):
            # There is at least one column plus column_with_labels_or_subgroups:
            is_numeric = 1
            
        # 4. Create copies of df, subsetting by type of column
        # 5. Group the dataframes by column_with_labels_or_subgroups, 
        # according to the aggregate function:
        if (is_categorical == 1):
            
            df_agg_mode = df.copy(deep = True)
            df_agg_mode = df_agg_mode[categorical_cols]
            # stats.mode now only works for numerically encoded variables (the previous ordinal
            # encoding is required)
            DATASET = df_agg_mode
            SUBSET_OF_FEATURES_TO_BE_ENCODED = categorical_cols
            df_agg_mode, ordinal_encoding_list = OrdinalEncoding_df (df = DATASET, subset_of_features_to_be_encoded = SUBSET_OF_FEATURES_TO_BE_ENCODED)
            # The encoded columns received the alias "_OrdinalEnc". Thus, we may drop the columns with the names in categorical_list,
            # avoiding that scipy try to aggregate them and raise an error:
            # Remove the columns that do not have numeric variables before grouping
            df_agg_mode = df_agg_mode.drop(columns = categorical_cols)

            if column_with_labels_or_subgroups in categorical_cols:
                column_with_labels_or_subgroups = column_with_labels_or_subgroups + "_OrdinalEnc"

            df_agg_mode = df_agg_mode.groupby(by = column_with_labels_or_subgroups, as_index = False, sort = True).agg(stats.mode)
            
            # 6. df_agg_mode processing:
            # Loop through each column from this dataframe:
            for col_mode in list(df_agg_mode.columns):
                
                # take the mode for all columns, except the column_with_labels_or_subgroups,
                # used for grouping the dataframe. This column already has the correct value
                if (col_mode != column_with_labels_or_subgroups):
            
                    # start a list of modes:
                    list_of_modes = []

                    # Now, loop through each row from the dataset:
                    for i in range(0, len(df_agg_mode)):
                        # i = 0 to i = len(df_agg_mode) - 1

                        mode_array = np.array(df_agg_mode[col_mode])[i]    

                        try:
                            # try accessing the mode
                            # mode array is like:
                            # ModeResult(mode=calculated_mode, count=counting_of_occurrences))
                            # To retrieve only the mode, we must access the element [0] from this array
                            # or attribute mode:
                            mode = mode_array.mode
                        except:
                            try:
                                mode = mode_array[0]
                            except:
                                try:
                                    if ((mode_array != np.nan) & (mode_array is not None)):
                                        mode = mode_array
                                    else:
                                        mode = np.nan
                                except:
                                    mode = np.nan
                        
                        # Append it to the list of modes:
                        list_of_modes.append(mode)

                    # Finally, make the column the list of modes itself:
                    df_agg_mode[col_mode] = list_of_modes
                
            # Now, reverse the encoding:
            DATASET = df_agg_mode
            ENCODING_LIST = ordinal_encoding_list
            # Now, reverse encoding and keep only the original column names:
            df_agg_mode = reverse_OrdinalEncoding (df = DATASET, encoding_list = ENCODING_LIST)
            df_agg_mode = df_agg_mode[categorical_cols]
                  
        if (is_numeric == 1):
            
            df_agg_mean = df.copy(deep = True)
            df_agg_sum = df.copy(deep = True)
            df_agg_std = df.copy(deep = True)
            df_agg_count = df.copy(deep = True)
            
            df_agg_mean = df_agg_mean[numeric_cols]
            df_agg_sum = df_agg_sum[numeric_cols]
            df_agg_std = df_agg_std[numeric_cols]
            df_agg_count = df_agg_count[numeric_cols]
            
            df_agg_mean = df_agg_mean.groupby(by = column_with_labels_or_subgroups, as_index = False, sort = True).mean()
            df_agg_sum = df_agg_sum.groupby(by = column_with_labels_or_subgroups, as_index = False, sort = True).sum()
            df_agg_std = df_agg_std.groupby(by = column_with_labels_or_subgroups, as_index = False, sort = True).std()
            df_agg_count = df_agg_count.groupby(by = column_with_labels_or_subgroups, as_index = False, sort = True).count()
            # argument as_index = False: prevents the grouper variable to be set as index of the new dataframe.
            # (default: as_index = True).
            
            # 7. df_agg_count processing:
            # Here, all original columns contain only the counting of elements in each
            # label. So, let's select only the columns 'key_for_merging' and column_with_variable_to_be_analyzed:
            df_agg_count = df_agg_count[[column_with_variable_to_be_analyzed]]
            
            # Rename the columns:
            df_agg_count.columns = ['count_of_elements_by_label']
            
            # Analogously, let's keep only the colums column_with_variable_to_be_analyzed and
            # 'key_for_merging' from the dataframes df_agg_sum and df_agg_std, and rename them:
            df_agg_sum = df_agg_sum[[column_with_variable_to_be_analyzed]]
            df_agg_std = df_agg_std[[column_with_variable_to_be_analyzed]]
            
            df_agg_sum.columns = ['sum_of_values_by_label']
            df_agg_std.columns = ['std_of_values_by_label']
            
        if ((is_categorical + is_numeric) == 2):
            # Both subsets are present and the column column_with_labels_or_subgroups
            # is duplicated.
            
            # Remove this column from df_agg_mean:
            df_agg_mean = df_agg_mean.drop(columns = column_with_labels_or_subgroups)
            
            # Concatenate all dataframes:
            df = pd.concat([df_agg_mode, df_agg_mean, df_agg_sum, df_agg_std, df_agg_count], axis = 1, join = "inner")
            
        elif (is_numeric == 1):
            
            # Only the numeric dataframes are present. So, concatenate them:
            df = pd.concat([df_agg_mean, df_agg_sum, df_agg_std, df_agg_count], axis = 1, join = "inner")
            
        elif (is_categorical == 1):
            
            # There is only the categorical dataframe:
            df = df_agg_mode
            
        df = df.reset_index(drop = True)
        
        # Notice that now we have a different mean value: we have a mean value
        # of the means calculated for each subgroup. So, we must update the
        # dictionary information:    
        dictionary['center'] = df[column_with_variable_to_be_analyzed].mean()
        dictionary['sum'] = df[column_with_variable_to_be_analyzed].sum()
        dictionary['std'] = df[column_with_variable_to_be_analyzed].std()
        dictionary['var'] = df[column_with_variable_to_be_analyzed].var()
        dictionary['count'] = len(df) # Total entries from the new dataframe
        dictionary['df'] = df
        
        # Update the attributes:
        self.dictionary = dictionary
        self.df = df
        # Notice that the number of labels is now the total of entries of the dataframe
        # grouped by labels
        self.number_of_labels = dictionary['count']
        
        return self


    def chart_x_bar_s (self):
        
        dictionary = self.dictionary
        df = self.df
        column_with_variable_to_be_analyzed = self.column_with_variable_to_be_analyzed
        number_of_labels = self.number_of_labels
        
        # CONTROL LIMIT EQUATIONS:
        # X-bar = mean =  (sum of measurements)/(subgroup size)
        # s = standard deviation in each subgroup
        # s-bar = mean (s) = (sum of all s values)/(number of subgroups)
        # x-bar-bar = mean (x-bar) = (sum of all x-bar)/(number of subgroups)
        # Lower control limit (LCL) = X-bar-bar - (A3)(s-bar)
        # Upper control limit (UCL) = X-bar-bar + (A3)(s-bar) 
        
        s = df['std_of_values_by_label']
        
        s_bar = (s.sum())/(number_of_labels)
        x_bar_bar = dictionary['center']
        
        # Retrieve A3
        self = self.get_constants()
        control_chart_constant = self.dict_of_constants['A3']
        
        # calculate the upper control limit as X-bar-bar + (A3)(s-bar):
        upper_cl = x_bar_bar + (control_chart_constant) * (s_bar)
        
        # add a column 'upper_cl' on the dataframe with this value:
        df['upper_cl'] = upper_cl
        
        # calculate the lower control limit as X-bar-bar - (A3)(s-bar):
        lower_cl = x_bar_bar - (control_chart_constant) * (s_bar)
        
        # add a column 'lower_cl' on the dataframe with this value:
        df['lower_cl'] = lower_cl
        
        # Add a column with the mean value of the considered interval:
        df['center'] = x_bar_bar
        
        # Update the dataframe in the dictionary:
        dictionary['df'] = df
        
        # Update the attributes:
        self.dictionary = dictionary
        self.df = df
        
        return self
    

    def chart_p (self):
        
        dictionary = self.dictionary
        df = self.df
        column_with_variable_to_be_analyzed = self.column_with_variable_to_be_analyzed
        number_of_labels = self.number_of_labels
        
        print("\n")
        print("Attention: before obtaining this chart, substitute the values of the analyzed binary variable by 0 or 1 (integers), or an error will be raised.")
        print("This function do not perform the automatic ordinal or One-Hot Encoding of the variables.\n")
        
        # CONTROL LIMIT EQUATIONS:
        # p-chart: control chart for proportion of defectives.
        # p = mean =  (sum of measurements)/(subgroup size)
        # pbar = (sum of subgroup defective counts)/(sum of subgroups sizes)
        # n = subgroup size
        # Lower control limit (LCL) = pbar - 3.sqrt((pbar)*(1-pbar)/n)
        # Upper control limit (UCL) = pbar + 3.sqrt((pbar)*(1-pbar)/n)
        
        count_per_label = df['count_of_elements_by_label']
        p_bar = (df['sum_of_values_by_label'].sum())/(df['count_of_elements_by_label'].sum())
        
        # calculate the upper control limit as pbar + 3.sqrt((pbar)*(1-pbar)/n):
        upper_cl = p_bar + 3 * (((p_bar)*(1 - p_bar)/(count_per_label))**(0.5))
        
        # add a column 'upper_cl' on the dataframe with this value:
        df['upper_cl'] = upper_cl
        
        # calculate the lower control limit as pbar - 3.sqrt((pbar)*(1-pbar)/n):
        lower_cl = p_bar - 3 * (((p_bar)*(1 - p_bar)/(count_per_label))**(0.5))
        
        # add a column 'lower_cl' on the dataframe with this value:
        df['lower_cl'] = lower_cl
        
        # Add a column with the mean value of the considered interval:
        df['center'] = p_bar
        
        # Update the dataframe in the dictionary:
        dictionary['df'] = df
        
        # Update the attributes:
        self.dictionary = dictionary
        self.df = df
        
        return self


    def chart_np (self):
        
        dictionary = self.dictionary
        df = self.df
        column_with_variable_to_be_analyzed = self.column_with_variable_to_be_analyzed
        number_of_labels = self.number_of_labels
        
        print("\n")
        print("Attention: before obtaining this chart, substitute the values of the analyzed binary variable by 0 or 1 (integers), or an error will be raised.")
        print("This function do not perform the automatic ordinal or One-Hot Encoding of the variables.\n")
        
        # CONTROL LIMIT EQUATIONS:
        # np-chart: control chart for count of defectives.
        # p = mean =  (sum of measurements)/(subgroup size)
        # np = sum = subgroup defective count
        # npbar = (sum of subgroup defective counts)/(number of subgroups)
        # n = subgroup size
        # pbar = npbar/n
        # Center line: npbar
        # Lower control limit (LCL) = np - 3.sqrt((np)*(1-p))
        # Upper control limit (UCL) = np + 3.sqrt((np)*(1-p))
        # available function: **(0.5) - 0.5 power
        
        # p = mean
        p = df[column_with_variable_to_be_analyzed]
        
        # Here, the column that we want to evaluate is not the mean, but the sum.
        # Since the graphics will be plotted using the column column_with_variable_to_be_analyzed
        # Let's make this column equals to the column of sums:
        
        df[column_with_variable_to_be_analyzed] = df['sum_of_values_by_label']
        np_series = df[column_with_variable_to_be_analyzed]
        
        npbar = (df['sum_of_values_by_label'].sum())/(number_of_labels) # center
        
        # calculate the upper control limit as np + 3.sqrt((np)*(1-p)):
        upper_cl = np_series + 3 * (((np_series)*(1 - p))**(0.5))
        
        # add a column 'upper_cl' on the dataframe with this value:
        df['upper_cl'] = upper_cl
        
        # calculate the lower control limit as np - 3.sqrt((np)*(1-p)):
        lower_cl = np_series - 3 * (((np_series)*(1 - p))**(0.5))
        
        # add a column 'lower_cl' on the dataframe with this value:
        df['lower_cl'] = lower_cl
        
        # Add a column with the mean value of the considered interval:
        df['center'] = npbar
        
        # Update the dataframe in the dictionary:
        dictionary['df'] = df
        
        # Update the attributes:
        self.dictionary = dictionary
        self.df = df
        
        return self


    def chart_c (self):
        
        dictionary = self.dictionary
        df = self.df
        column_with_variable_to_be_analyzed = self.column_with_variable_to_be_analyzed
        number_of_labels = self.number_of_labels
        
        # CONTROL LIMIT EQUATIONS:
        # c-chart: control chart for counts of occurrences per unit.
        # c = sum = sum of subgroup occurrences
        # cbar = (sum of subgroup occurrences)/(number of subgroups)
        # n = subgroup size
        # Lower control limit (LCL) = cbar - 3.sqrt(cbar)
        # Upper control limit (UCL) = cbar + 3.sqrt(cbar)
        
        # Here, the column that we want to evaluate is not the mean, but the sum.
        # Since the graphics will be plotted using the column column_with_variable_to_be_analyzed
        # Let's make this column equals to the column of sums:
        
        df[column_with_variable_to_be_analyzed] = df['sum_of_values_by_label']
        
        c_bar = (df['sum_of_values_by_label'].sum())/(number_of_labels)
        
        # calculate the upper control limit as cbar + 3.sqrt(cbar):
        upper_cl = c_bar + 3 * ((c_bar)**(0.5))
        
        # add a column 'upper_cl' on the dataframe with this value:
        df['upper_cl'] = upper_cl
        
        # calculate the lower control limit as cbar - 3.sqrt(cbar):
        lower_cl = c_bar - 3 * ((c_bar)**(0.5))
        
        # add a column 'lower_cl' on the dataframe with this value:
        df['lower_cl'] = lower_cl
        
        # Add a column with the mean value of the considered interval:
        df['center'] = c_bar
        
        # Update the dataframe in the dictionary:
        dictionary['df'] = df
        
        # Update the attributes:
        self.dictionary = dictionary
        self.df = df
        
        return self


    def chart_u (self):
        
        dictionary = self.dictionary
        df = self.df
        column_with_variable_to_be_analyzed = self.column_with_variable_to_be_analyzed
        number_of_labels = self.number_of_labels
        
        # CONTROL LIMIT EQUATIONS:
        # u-chart: control chart for average occurrence per unit.
        # u = mean =  (subgroup count of occurrences)/(subgroup size, in units)
        # ubar = mean value of u
        # n = subgroup size
        # Lower control limit (LCL) = ubar - 3.sqrt(ubar/n)
        # Upper control limit (UCL) = ubar + 3.sqrt(ubar/n)
        
        count_per_label = df['count_of_elements_by_label']
        
        u_bar = dictionary['center']
        
        # calculate the upper control limit as ubar + 3.sqrt(ubar/n):
        upper_cl = u_bar + 3 * ((u_bar/count_per_label)**(0.5))
        
        # add a column 'upper_cl' on the dataframe with this value:
        df['upper_cl'] = upper_cl
        
        # calculate the lower control limit as ubar - 3.sqrt(ubar/n):
        lower_cl = u_bar - 3 * ((u_bar/count_per_label)**(0.5))
        
        # add a column 'lower_cl' on the dataframe with this value:
        df['lower_cl'] = lower_cl
        
        # Add a column with the mean value of the considered interval:
        df['center'] = u_bar
        
        # Update the dataframe in the dictionary:
        dictionary['df'] = df
        
        # Update the attributes:
        self.dictionary = dictionary
        self.df = df
        
        return self


    def rare_events_chart (self):
        
        dictionary = self.dictionary
        df = self.df
        column_with_variable_to_be_analyzed = self.column_with_variable_to_be_analyzed
        rare_event_indication = self.rare_event_indication
        rare_event_timedelta_unit = self.rare_event_timedelta_unit
        timestamp_tag_column = self.timestamp_tag_column
        numeric_dtypes = self.numeric_dtypes
        chart_to_use = self.chart_to_use
        
        # Filter df to the rare events:
        rare_events_df = df.copy(deep = True)
        rare_events_df = rare_events_df[rare_events_df[column_with_variable_to_be_analyzed] == rare_event_indication]
        
        # rare_events_df stores only the entries for rare events.
        # Let's get a list of the indices of these entries (we did not reset the index):
        rare_events_indices = list(rare_events_df.index)
        
        # Start lists for storing the count of events between the rares and the time between
        # the rare events. Start both lists from np.nan, since we do not have information of
        # any rare event before the first one registered (np.nan is float).
        count_between_rares = [np.nan]
        timedelta_between_rares = [np.nan]
        
        # Check if the times are datetimes or not:
        column_data_type = df[timestamp_tag_column].dtype
        
        if (column_data_type not in numeric_dtypes):            
            # It is a datetime. Let's loop between successive indices:
            if (len(rare_events_indices) > 1):
                
                for i in range(0, (len(rare_events_indices)-1)):
                    # get the timedelta:
                    index_i = rare_events_indices[i]
                    index_i_plus = rare_events_indices[i + 1]  
                    
                    t_i = pd.Timestamp((df[timestamp_tag_column])[index_i], unit = 'ns')
                    t_i_plus = pd.Timestamp((df[timestamp_tag_column])[index_i_plus], unit = 'ns')
                    
                    # to slice a dataframe from row i to row j (including j): df[i:(j+1)]
                    total_events_between_rares = len(df[(index_i + 1):(index_i_plus)])
                    
                    # We sliced the dataframe from index_i + 1 not to include the rare
                    # event, so we started from the next one. Also, the last element is
                    # of index index_i_plus - 1, the element before the next rare.
                    count_between_rares.append(total_events_between_rares)
                    
                    # Calculate the timedelta:
                    # Convert to an integer representing the total of nanoseconds:
                    # The .delta attribute was replaced by .value attribute. 
                    # Both return the number of nanoseconds as an integer.
                    # https://pandas.pydata.org/docs/reference/api/pandas.Timedelta.html
                    timedelta = pd.Timedelta(t_i_plus - t_i).value
                    
                    if (rare_event_timedelta_unit == 'year'):
                        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
                        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
                        timedelta = timedelta / (10**9) #in seconds
                        #2. Convert it to minutes (1 min = 60 s):
                        timedelta = timedelta / 60.0 #in minutes
                        #3. Convert it to hours (1 h = 60 min):
                        timedelta = timedelta / 60.0 #in hours
                        #4. Convert it to days (1 day = 24 h):
                        timedelta = timedelta / 24.0 #in days
                        #5. Convert it to years. 1 year = 365 days + 6 h = 365 days + 6/24 h/(h/day)
                        # = (365 + 1/4) days = 365.25 days
                        timedelta = timedelta / (365.25) #in years
                        #The .0 after the numbers guarantees a float division.
                        
                    elif (rare_event_timedelta_unit == 'month'):
                        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
                        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
                        timedelta = timedelta / (10**9) #in seconds
                        #2. Convert it to minutes (1 min = 60 s):
                        timedelta = timedelta / 60.0 #in minutes
                        #3. Convert it to hours (1 h = 60 min):
                        timedelta = timedelta / 60.0 #in hours
                        #4. Convert it to days (1 day = 24 h):
                        timedelta = timedelta / 24.0 #in days
                        #5. Convert it to months. Consider 1 month = 30 days
                        timedelta = timedelta / (30.0) #in months
                        #The .0 after the numbers guarantees a float division.
                        
                    elif (rare_event_timedelta_unit == 'day'):
                        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
                        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
                        timedelta = timedelta / (10**9) #in seconds
                        #2. Convert it to minutes (1 min = 60 s):
                        timedelta = timedelta / 60.0 #in minutes
                        #3. Convert it to hours (1 h = 60 min):
                        timedelta = timedelta / 60.0 #in hours
                        #4. Convert it to days (1 day = 24 h):
                        timedelta = timedelta / 24.0 #in days
                        
                    elif (rare_event_timedelta_unit == 'hour'):
                        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
                        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
                        timedelta = timedelta / (10**9) #in seconds
                        #2. Convert it to minutes (1 min = 60 s):
                        timedelta = timedelta / 60.0 #in minutes
                        #3. Convert it to hours (1 h = 60 min):
                        timedelta = timedelta / 60.0 #in hours
                        
                    elif (rare_event_timedelta_unit == 'minute'):
                        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
                        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
                        timedelta = timedelta / (10**9) #in seconds
                        #2. Convert it to minutes (1 min = 60 s):
                        timedelta = timedelta / 60.0 #in minutes
                        
                    elif (rare_event_timedelta_unit == 'second'):
                        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
                        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
                        timedelta = timedelta / (10**9) #in seconds
                        
                    else:
                        timedelta = timedelta # nanoseconds.
                    
                    # Append the timedelta to the list:
                    timedelta_between_rares.append(timedelta)
            
            else:
                # There is a single rare event.
                print("There is a single rare event. Impossible to calculate timedeltas and counting between rare events.\n")
                return self
        
        else: 
            # The column is not a timestamp. Simply subtract the values to calculate the
            # timedeltas. Let's loop between successive indices:
            if (len(rare_events_indices) > 1):
                
                for i in range(0, (len(rare_events_indices)-1)):
                    
                    # get the timedelta:
                    index_i = rare_events_indices[i]
                    index_i_plus = rare_events_indices[i + 1]
                    
                    t_i = (df[timestamp_tag_column])[index_i]
                    t_i_plus = (df[timestamp_tag_column])[index_i_plus]
                    
                    timedelta = (t_i_plus - t_i)
                    
                    # to slice a dataframe from row i to row j (including j): df[i:(j+1)] 
                    total_events_between_rares= len(df[(index_i + 1):(index_i_plus)])
                    
                    count_between_rares.append(total_events_between_rares)
                    timedelta_between_rares.append(timedelta)
            else:
                # There is a single rare event.
                print("There is a single rare event. Impossible to calculate timedeltas and counting between rare events.\n")
                return self
            
        # Notice that the lists still have same number of elements of the dataframe of rares.
        
        # Now, lists have the same total elements of the rare_events_df, and can be
        # added as columns:        
        # firstly, reset the index:
        rare_events_df = rare_events_df.reset_index(drop = True)
        
        # Add the columns:
        rare_events_df['count_between_rares'] = count_between_rares
        rare_events_df['timedelta_between_rares'] = timedelta_between_rares
        
        # Now, make the rares dataframe the df itself:
        df = rare_events_df
        
        if (chart_to_use == 'g'):
            
            # Here, the column that we want to evaluate is not the mean, but the 'count_between_rares'.
            # Since the graphics will be plotted using the column column_with_variable_to_be_analyzed
            # Let's make this column equals to the column 'count_between_rares':
            df[column_with_variable_to_be_analyzed] = df['count_between_rares']
            
            g_bar = df['count_between_rares'].median()
            n_samples = len(df['count_between_rares'])
            
            try:
                p = (1/(g_bar + 1))*((n_samples - 1)/n_samples)
            
                # np.log = natural logarithm
                # https://numpy.org/doc/stable/reference/generated/numpy.log.html
                center = ((np.log(0.5))/(np.log(1 - p))) - 1

                # calculate the upper control limit as log(0.00135)/log(1-p)-1:
                upper_cl = ((np.log(0.00135))/(np.log(1 - p))) - 1

                # calculate the lower control limit as Max(0, log(1-0.00135)/log(1-p)-1):
                lower_cl = max(0, ((np.log(1 - 0.00135))/(np.log(1 - p)) - 1))
            
            except:
                # division by zero
                # Here, we are prone to it due to the obtention of the rare dataframe.
                p = np.nan
                center = np.nan
                upper_cl = np.nan
                lower_cl = np.nan
                
            # add a column 'lower_cl' on the dataframe with this value:
            df['lower_cl'] = lower_cl
            
            # add a column 'upper_cl' on the dataframe with this value:
            df['upper_cl'] = upper_cl
            
            # Add a column with the mean value of the considered interval:
            df['center'] = center
            
            # Update the dataframe in the dictionary:
            dictionary['df'] = df
            
        elif (chart_to_use == 't'):
            
            # Here, the column that we want to evaluate is not the mean, but the 'timedelta_between_rares'.
            # Since the graphics will be plotted using the column column_with_variable_to_be_analyzed
            # Let's make this column equals to the column 'timedelta_between_rares':
            df[column_with_variable_to_be_analyzed] = df['timedelta_between_rares']
            
            # Create the transformed series:
            # y = df['timedelta_between_rares']
            # y_transf = y**(1/3.6)
            y_transf = (df['timedelta_between_rares'])**(1/(3.6))
            # Now, let's create an I-MR chart for y_transf        
            moving_range = [abs(max((y_transf[i]), (y_transf[(i-1)])) - min((y_transf[i]), (y_transf[(i-1)]))) for i in range (1, len(y_transf))]
            
            # The first y_transf is np.nan. We cannot use it for calculating the averages.
            # That is because the average with np.nan is np.nan. So, let's skip the first entry,
            # by starting from index i = 2.
            y_bar = [(y_transf[i] + y_transf[(i-1)])/2 for i in range (2, len(y_transf))]
            # These lists were created from index 1. We must add a initial element to
            # make their sizes equal to the original dataset length
            
            # Start the list to store the moving ranges, containing only the number 0
            # for the moving range (by simple concatenation):
            moving_range = [0] + moving_range
            # Since we do not have the first element (which is np.nan), with index 0, let's
            # take the average corresponding to index 1, the first valid entry, as the y_transf[1]
            # itself:
            y_bar = [y_transf[1]] + y_bar
            # Notice that y_bar list did not start from index 0, but from index 1, so it has one
            # element less than moving_range list. With this strategy, we eliminated the null element
            # from the calculation of the mean.
            
            # The presence of other missing values in these lists will turn all results NaN.
            # So, let's convert the list to pandas series, and apply the mean method, which
            # automatically ignores the missing values from calculations (the function
            # np.average for np.arrays would return NaN)
            moving_range = pd.Series(moving_range)
            y_bar = pd.Series(y_bar)
            
            # Now we can get the mean values from y_bar list and moving_range:
            y_bar_bar = y_bar.mean()
            r_bar = moving_range.mean()
            # Get the control chart constant A2 from the dictionary, considering n = 2 the
            # number of elements of each subgroup:
            
            # Update the number of labels attribute for the moving range case
            self.number_of_labels = 2
            self = self.get_constants()
            
            control_chart_constant = self.dict_of_constants['1/d2']
            control_chart_constant = control_chart_constant * 3
            
            # calculate the upper control limit as y_bar_bar + (3/d2)r_bar:
            upper_cl_transf = y_bar_bar + (control_chart_constant) * (r_bar)
        
            # calculate the lower control limit as y_bar_bar - (3/d2)r_bar:
            lower_cl_transf = y_bar_bar - (control_chart_constant) * (r_bar)
          
            # Notice that these values are for the transformed variables:
            # y_transf = (df['timedelta_between_rares'])**(1/(3.6))
            
            # To reconvert to the correct time scale, we reverse this transform as:
            # (y_transf)**(3.6)
            
            # add a column 'upper_cl' on the dataframe with upper_cl_transf
            # converted to the original scale:
            df['upper_cl'] = (upper_cl_transf)**(3.6)
            
            # add a column 'lower_cl' on the dataframe with lower_cl_transf
            # converted to the original scale:
            df['lower_cl'] = (lower_cl_transf)**(3.6)
            
            # Finally, add the central line by reconverting y_bar_bar to the
            # original scale:
            df['center'] = (y_bar_bar)**(3.6)
            
            # Notice that this procedure naturally corrects the deviations caused by
            # the skewness of the distribution. Actually, log and exponential transforms
            # tend to reduce the skewness and to normalize the data.
            # Update the dataframe in the dictionary:
            dictionary['df'] = df
        
        # Update the attributes:
        self.dictionary = dictionary
        self.df = df
        
        return self


class CapabilityAnalysis:
    """
    Class for checking data normality, obtaining histograms, expected normal curve, actual probability density
    curve through Kernel density estimation (KDE) method, and checking process capability in relation to the specifications.

    def __init__ (self, df, column_with_variable_to_be_analyzed, specification_limits, total_of_bins = 10, alpha = 0.10)
    """

    # Initialize instance attributes.
    # define the Class constructor, i.e., how are its objects:
    def __init__ (self, df, column_with_variable_to_be_analyzed, specification_limits, total_of_bins = 10, alpha = 0.10):
        
        # If the user passes the argument, use them. Otherwise, use the standard values.
        # Set the class objects' attributes.
        # Suppose the object is named plot. We can access the attribute as:
        # plot.dictionary, for instance.
        # So, we can save the variables as objects' attributes.
        self.df = df
        self.column_with_variable_to_be_analyzed = column_with_variable_to_be_analyzed
        self.specification_limits = specification_limits
        self.sample_size = df[column_with_variable_to_be_analyzed].count()
        self.mu = (df[column_with_variable_to_be_analyzed]).mean() 
        self.median = (df[column_with_variable_to_be_analyzed]).median()
        self.sigma = (df[column_with_variable_to_be_analyzed]).std()
        self.lowest = (df[column_with_variable_to_be_analyzed]).min()
        self.highest = (df[column_with_variable_to_be_analyzed]).max()
        self.total_of_bins = total_of_bins
        self.alpha = alpha
        
        # Start a dictionary of constants
        self.dict_of_constants = {}
        # Get parameters to update later:
        self.histogram_dict = {}
        self.capability_dict = {}
        self.normality_dict = {}
        
        print("WARNING: this capability analysis is based on the strong hypothesis that data follows the normal (Gaussian) distribution.\n")
        
    # Define the class methods.
    # All methods must take an object from the class (self) as one of the parameters
   
    # Define a dictionary of constants.
    # Each key in the dictionary corresponds to a number of samples in a subgroup.
    # sample_size - This variable represents the total of labels or subgroups n. 
    # If there are multiple labels, this variable will be updated later.
    
    
    def check_data_normality (self):
        
        from scipy import stats
        from statsmodels.stats import diagnostic
        
        alpha = self.alpha
        df = self.df
        column_with_variable_to_be_analyzed = self.column_with_variable_to_be_analyzed
        sample_size = self.sample_size
        mu = self.mu 
        median = self.median
        sigma = self.sigma
        lowest = self.lowest
        highest = self.highest
        normality_dict = self.normality_dict # empty dictionary 
        
        print("WARNING: The statistical tests require at least 20 samples.\n")
        print("Interpretation:")
        print("p-value: probability of verifying the tested event, given that the null hypothesis H0 is correct.")
        print("H0: that data is described by the normal distribution.")
        print("Criterion: the series is not described by normal if p < alpha = %.3f." %(alpha))
        
        if (sample_size < 20):
            
            print(f"Unable to test series normality: at least 20 samples are needed, but found only {sample_size} entries for this series.\n")
            normality_dict['WARNING'] = "Series without the minimum number of elements (20) required to test the normality."
            
        else:
            # Let's test the series.
            y = df[column_with_variable_to_be_analyzed]
            
            # Scipy.stats’ normality test
            # It is based on D’Agostino and Pearson’s test that combines 
            # skew and kurtosis to produce an omnibus test of normality.
            _, scipystats_test_pval = stats.normaltest(y)
            # The underscore indicates an output to be ignored, which is s^2 + k^2, 
            # where s is the z-score returned by skewtest and k is the z-score returned by kurtosistest.
            # https://docs.scipy.org/doc/scipy-1.8.0/html-scipyorg/reference/generated/scipy.stats.normaltest.html
            
            print("\n")
            print("D\'Agostino and Pearson\'s normality test (scipy.stats normality test):")
            print(f"p-value = {scipystats_test_pval:e} = {scipystats_test_pval*100:.2f}% of probability of being normal.")
            # :e indicates the scientific notation; .2f: float with 2 decimal cases
            
            if (scipystats_test_pval < alpha):
                
                print("p = %.3f < %.3f" %(scipystats_test_pval, alpha))
                print(f"According to this test, data is not described by the normal distribution, for the {alpha*100}% confidence level defined.")
            
            else:
                
                print("p = %.3f >= %.3f" %(scipystats_test_pval, alpha))
                print(f"According to this test, data is described by the normal distribution, for the {alpha*100}% confidence level defined.")
            
            # add this test result to the dictionary:
            normality_dict['dagostino_pearson_p_val'] = scipystats_test_pval
            normality_dict['dagostino_pearson_p_in_pct'] = scipystats_test_pval*100
            
            # Scipy.stats’ Shapiro-Wilk test
            # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html
            shapiro_test = stats.shapiro(y)
            # returns ShapiroResult(statistic=0.9813305735588074, pvalue=0.16855233907699585)
             
            print("\n")
            print("Shapiro-Wilk normality test:")
            print(f"p-value = {shapiro_test[1]:e} = {(shapiro_test[1])*100:.2f}% of probability of being normal.")
            
            if (shapiro_test[1] < alpha):
                
                print("p = %.3f < %.3f" %(shapiro_test[1], alpha))
                print(f"According to this test, data is not described by the normal distribution, for the {alpha*100}% confidence level defined.")
            
            else:
                
                print("p = %.3f >= %.3f" %(shapiro_test[1], alpha))
                print(f"According to this test, data is described by the normal distribution, for the {alpha*100}% confidence level defined.")
            
            # add this test result to the dictionary:
            normality_dict['shapiro_wilk_p_val'] = shapiro_test[1]
            normality_dict['shapiro_wilk_p_in_pct'] = (shapiro_test[1])*100
            
            # Lilliefors’ normality test
            lilliefors_test = diagnostic.kstest_normal(y, dist = 'norm', pvalmethod = 'table')
            # Returns a tuple: index 0: ksstat: float
            # Kolmogorov-Smirnov test statistic with estimated mean and variance.
            # index 1: p-value:float
            # If the pvalue is lower than some threshold, e.g. 0.10, then we can reject the Null hypothesis that the sample comes from a normal distribution.
            
            print("\n")
            print("Lilliefors\'s normality test:")
            print(f"p-value = {lilliefors_test[1]:e} = {(lilliefors_test[1])*100:.2f}% of probability of being normal.")
            
            if (lilliefors_test[1] < alpha):
                
                print("p = %.3f < %.3f" %(lilliefors_test[1], alpha))
                print(f"According to this test, data is not described by the normal distribution, for the {alpha*100}% confidence level defined.")
            
            else:
                
                print("p = %.3f >= %.3f" %(lilliefors_test[1], alpha))
                print(f"According to this test, data is described by the normal distribution, for the {alpha*100}% confidence level defined.")
            
            # add this test result to the dictionary:
            normality_dict['lilliefors_p_val'] = lilliefors_test[1]
            normality_dict['lilliefors_p_in_pct'] = (lilliefors_test[1])*100

            # Anderson-Darling normality test
            ad_test = diagnostic.normal_ad(y, axis = 0)
            # Returns a tuple: index 0 - ad2: float
            # Anderson Darling test statistic.
            # index 1 - p-val: float
            # The p-value for hypothesis that the data comes from a normal distribution with unknown mean and variance.
            
            print("\n")
            print("Anderson-Darling (AD) normality test:")
            print(f"p-value = {ad_test[1]:e} = {(ad_test[1])*100:.2f}% of probability of being normal.")
            
            if (ad_test[1] < alpha):
                
                print("p = %.3f < %.3f" %(ad_test[1], alpha))
                print(f"According to this test, data is not described by the normal distribution, for the {alpha*100}% confidence level defined.")
            
            else:
                
                print("p = %.3f >= %.3f" %(ad_test[1], alpha))
                print(f"According to this test, data is described by the normal distribution, for the {alpha*100}% confidence level defined.")
            
            # add this test result to the dictionary:
            normality_dict['anderson_darling_p_val'] = ad_test[1]
            normality_dict['anderson_darling_p_in_pct'] = (ad_test[1])*100
            
            # Update the attribute:
            self.normality_dict = normality_dict
            
            return self
    

    def get_constants (self):
        
        if (self.sample_size < 2):
            
            self.sample_size = 2
            
        if (self.sample_size <= 25):
            
            dict_of_constants = {
                
                2: {'A':2.121, 'A2':1.880, 'A3':2.659, 'c4':0.7979, '1/c4':1.2533, 'B3':0, 'B4':3.267, 'B5':0, 'B6':2.606, 'd2':1.128, '1/d2':0.8865, 'd3':0.853, 'D1':0, 'D2':3.686, 'D3':0, 'D4':3.267},
                3: {'A':1.732, 'A2':1.023, 'A3':1.954, 'c4':0.8862, '1/c4':1.1284, 'B3':0, 'B4':2.568, 'B5':0, 'B6':2.276, 'd2':1.693, '1/d2':0.5907, 'd3':0.888, 'D1':0, 'D2':4.358, 'D3':0, 'D4':2.574},
                4: {'A':1.500, 'A2':0.729, 'A3':1.628, 'c4':0.9213, '1/c4':1.0854, 'B3':0, 'B4':2.266, 'B5':0, 'B6':2.088, 'd2':2.059, '1/d2':0.4857, 'd3':0.880, 'D1':0, 'D2':4.698, 'D3':0, 'D4':2.282},
                5: {'A':1.342, 'A2':0.577, 'A3':1.427, 'c4':0.9400, '1/c4':1.0638, 'B3':0, 'B4':2.089, 'B5':0, 'B6':1.964, 'd2':2.326, '1/d2':0.4299, 'd3':0.864, 'D1':0, 'D2':4.918, 'D3':0, 'D4':2.114},
                6: {'A':1.225, 'A2':0.483, 'A3':1.287, 'c4':0.9515, '1/c4':1.0510, 'B3':0.030, 'B4':1.970, 'B5':0.029, 'B6':1.874, 'd2':2.534, '1/d2':0.3946, 'd3':0.848, 'D1':0, 'D2':5.078, 'D3':0, 'D4':2.004},
                7: {'A':1.134, 'A2':0.419, 'A3':1.182, 'c4':0.9594, '1/c4':1.0423, 'B3':0.118, 'B4':1.882, 'B5':0.113, 'B6':1.806, 'd2':2.704, '1/d2':0.3698, 'd3':0.833, 'D1':0.204, 'D2':5.204, 'D3':0.076, 'D4':1.924},
                8: {'A':1.061, 'A2':0.373, 'A3':1.099, 'c4':0.9650, '1/c4':1.0363, 'B3':0.185, 'B4':1.815, 'B5':0.179, 'B6':1.751, 'd2':2.847, '1/d2':0.3512, 'd3':0.820, 'D1':0.388, 'D2':5.306, 'D3':0.136, 'D4':1.864},
                9: {'A':1.000, 'A2':0.337, 'A3':1.032, 'c4':0.9693, '1/c4':1.0317, 'B3':0.239, 'B4':1.761, 'B5':0.232, 'B6':1.707, 'd2':2.970, '1/d2':0.3367, 'd3':0.808, 'D1':0.547, 'D2':5.393, 'D3':0.184, 'D4':1.816},
                10: {'A':0.949, 'A2':0.308, 'A3':0.975, 'c4':0.9727, '1/c4':1.0281, 'B3':0.284, 'B4':1.716, 'B5':0.276, 'B6':1.669, 'd2':3.078, '1/d2':0.3249, 'd3':0.797, 'D1':0.687, 'D2':5.469, 'D3':0.223, 'D4':1.777},
                11: {'A':0.905, 'A2':0.285, 'A3':0.927, 'c4':0.9754, '1/c4':1.0252, 'B3':0.321, 'B4':1.679, 'B5':0.313, 'B6':1.637, 'd2':3.173, '1/d2':0.3152, 'd3':0.787, 'D1':0.811, 'D2':5.535, 'D3':0.256, 'D4':1.744},
                12: {'A':0.866, 'A2':0.266, 'A3':0.886, 'c4':0.9776, '1/c4':1.0229, 'B3':0.354, 'B4':1.646, 'B5':0.346, 'B6':1.610, 'd2':3.258, '1/d2':0.3069, 'd3':0.778, 'D1':0.922, 'D2':5.594, 'D3':0.283, 'D4':1.717},
                13: {'A':0.832, 'A2':0.249, 'A3':0.850, 'c4':0.9794, '1/c4':1.0210, 'B3':0.382, 'B4':1.618, 'B5':0.374, 'B6':1.585, 'd2':3.336, '1/d2':0.2998, 'd3':0.770, 'D1':1.025, 'D2':5.647, 'D3':0.307, 'D4':1.693},
                14: {'A':0.802, 'A2':0.235, 'A3':0.817, 'c4':0.9810, '1/c4':1.0194, 'B3':0.406, 'B4':1.594, 'B5':0.399, 'B6':1.563, 'd2':3.407, '1/d2':0.2935, 'd3':0.763, 'D1':1.118, 'D2':5.696, 'D3':0.328, 'D4':1.672},
                15: {'A':0.775, 'A2':0.223, 'A3':0.789, 'c4':0.9823, '1/c4':1.0180, 'B3':0.428, 'B4':1.572, 'B5':0.421, 'B6':1.544, 'd2':3.472, '1/d2':0.2880, 'd3':0.756, 'D1':1.203, 'D2':5.741, 'D3':0.347, 'D4':1.653},
                16: {'A':0.750, 'A2':0.212, 'A3':0.763, 'c4':0.9835, '1/c4':1.0168, 'B3':0.448, 'B4':1.552, 'B5':0.440, 'B6':1.526, 'd2':3.532, '1/d2':0.2831, 'd3':0.750, 'D1':1.282, 'D2':5.782, 'D3':0.363, 'D4':1.637},
                17: {'A':0.728, 'A2':0.203, 'A3':0.739, 'c4':0.9845, '1/c4':1.0157, 'B3':0.466, 'B4':1.534, 'B5':0.458, 'B6':1.511, 'd2':3.588, '1/d2':0.2787, 'd3':0.744, 'D1':1.356, 'D2':5.820, 'D3':0.378, 'D4':1.622},
                18: {'A':0.707, 'A2':0.194, 'A3':0.718, 'c4':0.9854, '1/c4':1.0148, 'B3':0.482, 'B4':1.518, 'B5':0.475, 'B6':1.496, 'd2':3.640, '1/d2':0.2747, 'd3':0.739, 'D1':1.424, 'D2':5.856, 'D3':0.391, 'D4':1.608},
                19: {'A':0.688, 'A2':0.187, 'A3':0.698, 'c4':0.9862, '1/c4':1.0140, 'B3':0.497, 'B4':1.503, 'B5':0.490, 'B6':1.483, 'd2':3.689, '1/d2':0.2711, 'd3':0.734, 'D1':1.487, 'D2':5.891, 'D3':0.403, 'D4':1.597},
                20: {'A':0.671, 'A2':0.180, 'A3':0.680, 'c4':0.9869, '1/c4':1.0133, 'B3':0.510, 'B4':1.490, 'B5':0.504, 'B6':1.470, 'd2':3.735, '1/d2':0.2677, 'd3':0.729, 'D1':1.549, 'D2':5.921, 'D3':0.415, 'D4':1.585},
                21: {'A':0.655, 'A2':0.173, 'A3':0.663, 'c4':0.9876, '1/c4':1.0126, 'B3':0.523, 'B4':1.477, 'B5':0.516, 'B6':1.459, 'd2':3.778, '1/d2':0.2647, 'd3':0.724, 'D1':1.605, 'D2':5.951, 'D3':0.425, 'D4':1.575},
                22: {'A':0.640, 'A2':0.167, 'A3':0.647, 'c4':0.9882, '1/c4':1.0119, 'B3':0.534, 'B4':1.466, 'B5':0.528, 'B6':1.448, 'd2':3.819, '1/d2':0.2618, 'd3':0.720, 'D1':1.659, 'D2':5.979, 'D3':0.434, 'D4':1.566},
                23: {'A':0.626, 'A2':0.162, 'A3':0.633, 'c4':0.9887, '1/c4':1.0114, 'B3':0.545, 'B4':1.455, 'B5':0.539, 'B6':1.438, 'd2':3.858, '1/d2':0.2592, 'd3':0.716, 'D1':1.710, 'D2':6.006, 'D3':0.443, 'D4':1.557},
                24: {'A':0.612, 'A2':0.157, 'A3':0.619, 'c4':0.9892, '1/c4':1.0109, 'B3':0.555, 'B4':1.445, 'B5':0.549, 'B6':1.429, 'd2':3.895, '1/d2':0.2567, 'd3':0.712, 'D1':1.759, 'D2':6.031, 'D3':0.451, 'D4':1.548},
                25: {'A':0.600, 'A2':0.153, 'A3':0.606, 'c4':0.9896, '1/c4':1.0105, 'B3':0.565, 'B4':1.435, 'B5':0.559, 'B6':1.420, 'd2':3.931, '1/d2':0.2544, 'd3':0.708, 'D1':1.806, 'D2':6.056, 'D3':0.459, 'D4':1.541},
            }
            
            # Access the key:
            dict_of_constants = dict_of_constants[self.sample_size]
            
        else: #>= 26
            
            dict_of_constants = {'A':(3/(self.sample_size**(0.5))), 'A2':0.153, 
                                 'A3':3/((4*(self.sample_size-1)/(4*self.sample_size-3))*(self.sample_size**(0.5))), 
                                 'c4':(4*(self.sample_size-1)/(4*self.sample_size-3)), 
                                 '1/c4':1/((4*(self.sample_size-1)/(4*self.sample_size-3))), 
                                 'B3':(1-3/(((4*(self.sample_size-1)/(4*self.sample_size-3)))*((2*(self.sample_size-1))**(0.5)))), 
                                 'B4':(1+3/(((4*(self.sample_size-1)/(4*self.sample_size-3)))*((2*(self.sample_size-1))**(0.5)))),
                                 'B5':(((4*(self.sample_size-1)/(4*self.sample_size-3)))-3/((2*(self.sample_size-1))**(0.5))), 
                                 'B6':(((4*(self.sample_size-1)/(4*self.sample_size-3)))+3/((2*(self.sample_size-1))**(0.5))), 
                                 'd2':3.931, '1/d2':0.2544, 'd3':0.708, 'D1':1.806, 'D2':6.056, 'D3':0.459, 'D4':1.541}
        
        # Update the attribute
        self.dict_of_constants = dict_of_constants
        
        return self
    

    def get_histogram_array (self):
        
        df = self.df
        column_with_variable_to_be_analyzed = self.column_with_variable_to_be_analyzed
        y_hist = df[column_with_variable_to_be_analyzed]
        lowest = self.lowest
        highest = self.highest
        sample_size = self.sample_size
        
        # Number of bins set by the user:
        total_of_bins = self.total_of_bins
        
        # Firstly, get the ideal bin-size according to the Montgomery's method:
        # Douglas C. Montgomery (2009). Introduction to Statistical Process Control, 
        # Sixth Edition, John Wiley & Sons.
        # Sort by the column to analyze (ascending order) and reset the index:
        y_hist = y_hist.sort_values(ascending = True)
        y_hist = y_hist.reset_index(drop = True)
        #Calculo do bin size - largura do histograma:
        #1: Encontrar o menor (lowest) e o maior (highest) valor dentro da tabela de dados)
        #2: Calcular rangehist = highest - lowest
        #3: Calcular quantidade de dados (samplesize) de entrada fornecidos
        #4: Calcular a quantidade de celulas da tabela de frequencias (ncells)
        #ncells = numero inteiro mais proximo da (raiz quadrada de samplesize)
        #5: Calcular binsize = (df[column_to_analyze])rangehist/(ncells)
        #ATENCAO: Nao se esquecer de converter range, ncells, samplesize e binsize para valores absolutos (modulos)
        #isso porque a largura do histograma tem que ser um numero positivo 

        # bin-size
        range_hist = abs(highest - lowest)
        n_cells = int(np.rint((sample_size)**(0.5)))
        # We must use the int function to guarantee that the ncells will store an
        # integer number of cells (we cannot have a fraction of a sentence).
        # The int function guarantees that the variable will be stored as an integer.
        # The numpy.rint(a) function rounds elements of the array to the nearest integer.
        # https://numpy.org/doc/stable/reference/generated/numpy.rint.html
        # For values exactly halfway between rounded decimal values, 
        # NumPy rounds to the nearest even value. 
        # Thus 1.5 and 2.5 round to 2.0; -0.5 and 0.5 round to 0.0; etc.
        if (n_cells > 3):
            
            print(f"Ideal number of histogram bins calculated through Montgomery's method = {n_cells} bins.\n")
        
        # Retrieve the histogram array hist_array
        fig, ax = plt.subplots() # (0,0) not to show the plot now:
        
        # Get a 10-bins histogram:
        hist_array = plt.hist(y_hist, bins = total_of_bins)
        plt.delaxes(ax) # this will delete ax, so that it will not be plotted.
        plt.show()
        print("") # use this print not to mix with the final plot

        # hist_array is an array of arrays:
        # hist_array = (array([count_1, count_2, ..., cont_n]), array([bin_center_1,...,
        # bin_center_n])), where n = total_of_bins
        # hist_array[0] is the array of countings for each bin, whereas hist_array[1] is
        # the array of the bin center, i.e., the central value of the analyzed variable for
        # that bin.

        # It is possible that the hist_array[0] contains more elements than hist_array[1].
        # This happens when the last bins created by the division contain zero elements.
        # In this case, we have to pad the sequence of hist_array[0], completing it with zeros.

        MAX_LENGTH = max(len(hist_array[0]), len(hist_array[1])) # Get the length of the longest sequence
        SEQUENCES = [list(hist_array[0]), list(hist_array[1])] # get a list of sequences to pad.
        # Notice that we applied the list attribute to create a list of lists

        # We cannot pad with the function pad_sequences from tensorflow because it converts all values
        # to integers. Then, we have to pad the sequences by looping through the elements from SEQUENCES:

        # Start a support_list
        support_list = []

        # loop through each sequence in SEQUENCES:
        for sequence in SEQUENCES:
            # add a zero at the end of the sequence until its length reaches MAX_LENGTH
            while (len(sequence) < MAX_LENGTH):

                sequence.append(0)

            # append the sequence to support_list:
            support_list.append(sequence)

        # Tuples and arrays are immutable. It means they do not support assignment, i.e., we cannot
        # do tuple[0] = variable. Since arrays support vectorial (element-wise) operations, we can
        # modify the whole array making it equals to support_list at once by using function np.array:
        hist_array = np.array(support_list)

        # Get the bin_size as the average difference between successive elements from support_list[1]:

        diff_lists = []

        for i in range (1, len(support_list[1])):

            diff_lists.append(support_list[1][i] - support_list[1][(i-1)])

        # Now, get the mean value as the bin_size:
        bin_size = np.amax(np.array(diff_lists))

        # Let's get the frequency table, which will be saved on DATASET (to get the code
        # equivalent to the code for the function 'histogram'):

        DATASET = pd.DataFrame(data = {'bin_center': hist_array[1], 'count': hist_array[0]})

        # Get a lists of bin_center and column_to_analyze:
        list_of_bins = list(hist_array[1])
        list_of_counts = list(hist_array[0])

        # get the maximum count:
        max_count = DATASET['count'].max()
        # Get the index of the max count:
        max_count_index = list_of_counts.index(max_count)

        # Get the value bin_center correspondent to the max count (maximum probability):
        bin_of_max_proba = list_of_bins[max_count_index]
        bin_after_the_max_proba = list_of_bins[(max_count_index + 1)] # the next bin
        number_of_bins = len(DATASET) # Total of elements on the frequency table
        
        # Obtain a list of differences between bins
        bins_diffs = [(list_of_bins[i] - list_of_bins[(i-1)]) for i in range (1, len(list_of_bins))]
        # Convert it to Pandas series and use the mean method to retrieve the average bin size:
        bin_size = pd.Series(bins_diffs).mean()
        
        self.histogram_dict = {'df': DATASET, 'list_of_bins': list_of_bins, 'list_of_counts': list_of_counts,
                              'max_count': max_count, 'max_count_index': max_count_index,
                              'bin_of_max_proba': bin_of_max_proba, 'bin_after_the_max_proba': bin_after_the_max_proba,
                              'number_of_bins': number_of_bins, 'bin_size': bin_size}
        
        return self
    

    def get_desired_normal (self):
        
        # Get a normal completely (6s) in the specifications, and centered
        # within these limits
        
        mu = self.mu
        sigma = self.sigma
        histogram_dict = self.histogram_dict
        max_count = histogram_dict['max_count']
        
        specification_limits = self.specification_limits
        
        lower_spec = specification_limits['lower_spec_lim']
        upper_spec = specification_limits['upper_spec_lim']
        
        if (lower_spec is None):
            
            # There is no lower specification: everything below it is in the specifications.
            # Make it mean - 6sigma (virtually infinite).
            lower_spec = mu - 6*(sigma)
            # Update the dictionary:
            specification_limits['lower_spec_lim'] = lower_spec
        
        if (upper_spec is None):
            
            # There is no upper specification: everything above it is in the specifications.
            # Make it mean + 6sigma (virtually infinite).
            upper_spec = mu + 6*(sigma)
            # Update the dictionary:
            specification_limits['upper_spec_lim'] = upper_spec
        
        # Desired normal mu: center of the specification limits.
        desired_mu = (lower_spec + upper_spec)/2
        
        # Desired sigma: 6 times the variation within the specific limits
        desired_sigma = (upper_spec - lower_spec)/6
        
        if (desired_sigma == 0):
            print("Impossible to obtain a normal curve overlayed, because the standard deviation is zero.\n")
            print("The analyzed variable is constant throughout the whole sample space.\n")
            
            # Get a dictionary of empty lists for this case
            desired_normal = {'x': [], 'y':[]}
            
        else:
            # create lists to store the normal curve. Center the normal curve in the bin
            # of maximum bar (max probability, which will not be the mean if the curve
            # is skewed). For normal distributions, this value will be the mean and the median.

            # set the lowest value x used for obtaining the normal curve as center_of_bin_of_max_proba - 4*sigma
            # the highest x will be center_of_bin_of_max_proba - 4*sigma
            # each value will be created by incrementing (0.10)*sigma

            # The arrays created by the plt.hist method present the value of the extreme left 
            # (the beginning) of the histogram bars, not the bin center. So, let's add half of the bin size
            # to the bin_of_max_proba, so that the adjusted normal will be positioned on the center of the
            # bar of maximum probability. We can do it by taking the average between bin_of_max_proba
            # and the following bin, bin_after_the_max_proba:
            
            # Let's create a normal around the desired mean value. Firstly, create the range X - 4s to
            # X + 4s. The probabilities will be calculated for each value in this range:

            x = (desired_mu - (4 * desired_sigma))
            x_of_normal = [x]

            while (x < (desired_mu + (4 * desired_sigma))):

                x = x + (0.10)*(desired_sigma)
                x_of_normal.append(x)

            # Convert the list to a NumPy array, so that it is possible to perform element-wise
            # (vectorial) operations:
            x_of_normal = np.array(x_of_normal)

            # Create an array of the normal curve y, applying the normal curve equation:
            # normal curve = 1/(sigma* ((2*pi)**(0.5))) * exp(-((x-mu)**2)/(2*(sigma**2)))
            # where pi = 3,14...., and exp is the exponential function (base e)
            # Let's center the normal curve on desired_mu:
            y_normal = (1 / (desired_sigma* (np.sqrt(2 * (np.pi))))) * (np.exp(-0.5 * (((1 / desired_sigma) * (x_of_normal - desired_mu)) ** 2)))
            y_normal = np.array(y_normal)

            # Pick the maximum value obtained for y_normal:
            # https://numpy.org/doc/stable/reference/generated/numpy.amax.html#numpy.amax
            y_normal_max = np.amax(y_normal)

            # Let's get a correction factor, comparing the maximum of the histogram counting, max_count,
            # with y_normal_max:
            correction_factor = max_count/(y_normal_max)

            # Now, multiply each value of the array y_normal by the correction factor, to adjust the height:
            y_normal = y_normal * correction_factor
            # Now the probability density function (values originally from 0 to 1) has the same 
            # height as the histogram.
            
            desired_normal = {'x': x_of_normal, 'y': y_normal}
        
        # Nest the desired_normal dictionary into specification_limits dictionary:
        specification_limits['desired_normal'] = desired_normal
        # Update the attribute:
        self.specification_limits = specification_limits
        
        return self
    

    def get_fitted_normal (self):
        
        # Get a normal completely (6s) in the specifications, and centered
        # within these limits
        
        mu = self.mu
        sigma = self.sigma
        histogram_dict = self.histogram_dict
        max_count = histogram_dict['max_count']
        bin_of_max_proba = histogram_dict['bin_of_max_proba']
        specification_limits = self.specification_limits
        
        if (sigma == 0):
            print("Impossible to obtain a normal curve overlayed, because the standard deviation is zero.\n")
            print("The analyzed variable is constant throughout the whole sample space.\n")
            
            # Get a dictionary of empty lists for this case
            fitted_normal = {'x': [], 'y':[]}
            
        else:
            # create lists to store the normal curve. Center the normal curve in the bin
            # of maximum bar (max probability, which will not be the mean if the curve
            # is skewed). For normal distributions, this value will be the mean and the median.

            # set the lowest value x used for obtaining the normal curve as bin_of_max_proba - 4*sigma
            # the highest x will be bin_of_max_proba - 4*sigma
            # each value will be created by incrementing (0.10)*sigma

            x = (bin_of_max_proba - (4 * sigma))
            x_of_normal = [x]

            while (x < (bin_of_max_proba + (4 * sigma))):

                x = x + (0.10)*(sigma)
                x_of_normal.append(x)

            # Convert the list to a NumPy array, so that it is possible to perform element-wise
            # (vectorial) operations:
            x_of_normal = np.array(x_of_normal)

            # Create an array of the normal curve y, applying the normal curve equation:
            # normal curve = 1/(sigma* ((2*pi)**(0.5))) * exp(-((x-mu)**2)/(2*(sigma**2)))
            # where pi = 3,14...., and exp is the exponential function (base e)
            # Let's center the normal curve on bin_of_max_proba
            y_normal = (1 / (sigma* (np.sqrt(2 * (np.pi))))) * (np.exp(-0.5 * (((1 / sigma) * (x_of_normal - bin_of_max_proba)) ** 2)))
            y_normal = np.array(y_normal)

            # Pick the maximum value obtained for y_normal:
            # https://numpy.org/doc/stable/reference/generated/numpy.amax.html#numpy.amax
            y_normal_max = np.amax(y_normal)

            # Let's get a correction factor, comparing the maximum of the histogram counting, max_count,
            # with y_normal_max:
            correction_factor = max_count/(y_normal_max)

            # Now, multiply each value of the array y_normal by the correction factor, to adjust the height:
            y_normal = y_normal * correction_factor
            
            fitted_normal = {'x': x_of_normal, 'y': y_normal}
        
        # Nest the fitted_normal dictionary into specification_limits dictionary:
        specification_limits['fitted_normal'] = fitted_normal
        # Update the attribute:
        self.specification_limits = specification_limits
        
        return self
    

    def get_actual_pdf (self):
        
        # PDF: probability density function.
        # KDE: Kernel density estimation: estimation of the actual probability density
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gaussian_kde.html#scipy.stats.gaussian_kde
        
        from scipy import stats
        
        df = self.df
        column_with_variable_to_be_analyzed = self.column_with_variable_to_be_analyzed
        array_to_analyze = np.array(df[column_with_variable_to_be_analyzed])
        
        mu = self.mu
        sigma = self.sigma
        lowest = self.lowest
        highest = self.highest
        sample_size = self.sample_size
        
        histogram_dict = self.histogram_dict
        max_count = histogram_dict['max_count']
        specification_limits = self.specification_limits 
        
        # Get the KDE object
        kde = stats.gaussian_kde(array_to_analyze)
        
        # Here, kde may represent a distribution with high skewness and kurtosis. So, let's check
        # if the intervals mu - 6s and mu + 6s are represented by the array:
        inf_kde_lim = mu - 6*sigma
        sup_kde_lim = mu + 6*sigma
        
        if (inf_kde_lim > min(list(array_to_analyze))):
            # make the inferior limit the minimum value from the array:
            inf_kde_lim = min(list(array_to_analyze))
        
        if (sup_kde_lim < max(list(array_to_analyze))):
            # make the superior limit the minimum value from the array:
            sup_kde_lim = max(list(array_to_analyze))
        
        # Let's obtain a X array, consisting with all values from which we will calculate the PDF:
        new_x = inf_kde_lim
        new_x_list = [new_x]
        
        while ((new_x) < sup_kde_lim):
            # There is already the first element, so go to the next one.
            new_x = new_x + (0.10)*sigma
            new_x_list.append(new_x)
        
        # Convert the new_x_list to NumPy array, making it the array_to_analyze:
        array_to_analyze = np.array(new_x_list)
        
        # Apply the pdf method to convert the array_to_analyze into the array of probabilities:
        # i.e., calculate the probability for each one of the values in array_to_analyze:
        # PDF: Probability density function
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gaussian_kde.pdf.html#scipy.stats.gaussian_kde.pdf
        array_of_probs = kde.pdf(array_to_analyze)
        
        # Pick the maximum value obtained for array_of_probs:
        # https://numpy.org/doc/stable/reference/generated/numpy.amax.html#numpy.amax
        array_of_probs_max = np.amax(array_of_probs)

        # Let's get a correction factor, comparing the maximum of the histogram counting, max_count,
        # with array_of_probs_max:
        correction_factor = max_count/(array_of_probs_max)

        # Now, multiply each value of the array y_normal by the correction factor, to adjust the height:
        array_of_probs = array_of_probs * correction_factor
        # Now the probability density function (values originally from 0 to 1) has the same 
        # height as the histogram.
        
        # Define a dictionary
        # X of the probability density plot: values from the series being analyzed.
        # Y of the probability density plot: probabilities calculated for each X.
        actual_pdf = {'x': array_to_analyze, 'y': array_of_probs}
        
        # Nest the desired_normal dictionary into specification_limits dictionary:
        specification_limits['actual_pdf'] = actual_pdf
        # Update the attribute:
        self.specification_limits = specification_limits
        
        return self
    

    def get_capability_indicators (self):
        
        # Get a normal completely (6s) in the specifications, and centered
        # within these limits
        
        mu = self.mu
        sigma = self.sigma
        histogram_dict = self.histogram_dict
        bin_of_max_proba = histogram_dict['bin_of_max_proba']
        bin_after_the_max_proba = histogram_dict['bin_after_the_max_proba']
        max_count = histogram_dict['max_count']
        
        specification_limits = self.specification_limits
        lower_spec = specification_limits['lower_spec_lim']
        upper_spec = specification_limits['upper_spec_lim']
        desired_mu = (lower_spec + upper_spec)/2 
        # center of the specification limits: we want the mean to be in the center of the
        # specification limits
        
        range_spec = abs(upper_spec - lower_spec)
        
        # Get the constant:
        self = self.get_constants()
        dict_of_constants = self.dict_of_constants
        constant = dict_of_constants['1/c4']
        
        # Calculate corrected sigma:
        sigma_corrected = sigma*constant
        
        # Calculate the capability indicators, adding them to the
        # capability_dict
        cp = (range_spec)/(6*sigma_corrected)
        cr = 100*(6*sigma_corrected)/(range_spec)
        cm = (range_spec)/(8*sigma_corrected)
        zu = (upper_spec - mu)/(sigma_corrected)
        zl = (mu - lower_spec)/(sigma_corrected)
        
        z_min = min(zu, zl)
        cpk = (z_min)/3

        cpm_factor = 1 + ((mu - desired_mu)/sigma_corrected)**2
        cpm_factor = cpm_factor**(0.5) # square root
        cpm = (cp)/(cpm_factor)
        
        capability_dict = {'indicator': ['cp', 'cr', 'cm', 'zu', 'zl', 'z_min', 'cpk', 'cpm'], 
                            'value': [cp, cr, cm, zu, zl, z_min, cpk, cpm]}
        # Already in format for pd.DataFrame constructor
        
        # Update the attribute:
        self.capability_dict = capability_dict
        
        return self
    

    def capability_interpretation (self):
       
        print("Capable process: a process which attends its specifications.")
        print("Naturally, we want processes capable of attending the specifications.\n")
        
        print("Specification range:")
        print("Absolute value of the difference between the upper and the lower limits of specification.\n")
        
        print("6s interval:")
        print("Consider mean value = mu; standard deviation = s")
        print("For a normal distribution, 99.7% of the values range from its (mu - 3s) to (mu + 3s).")
        print("So, if the process follows the normal distribution, we can consider that virtually all of the data is in this range with 6s width.\n")
        
        print ("Cp:")
        print ("Relation between specification range and 6s.\n")
        
        print("Cr:")
        print("Usually, 6s > specification range.")
        print("So, the inverse of Cp is the fraction of 6s correspondent to the specification range.")
        print("Example: if 1/Cp = 0.2, then the specification range corresponds to 0.20 (20%) of the 6s interval.")
        print("Cr = 100 x (1/Cp) - the percent of 6s correspondent to the specification range.")
        print("Again, if 1/Cp = 0.2, then Cr = 20: the specification range corresponds to 20% of the 6s interval.\n")
        
        print("Cm:")
        print("It is a more generalized version of Cp.")
        print("Cm is the relation between specification range and 8s.")
        print("Then, even highly distant values from long-tailed curves are analyzed by this indicator.\n")
        
        print("Zu:")
        print("Represents how far is the mean of the values from the upper specification limit.")
        print("Zu = ([upper specification limit] - mu)/s")
        print("A higher Zu indicates a mean value lower than (and more distant from) the upper specification.")
        print("A negative Zu, in turns, indicates that the mean value is greater than the upper specification (i.e.: in average, specification is not attended).\n")
        
        print("Zl:")
        print("Represents how far is the mean of the values from the lower specification limit.")
        print("Zl = (mu - [lower specification limit])/s\n")
        print("A higher Zl indicates a mean value higher than  (and more distant from) the lower specification.")
        print("A negative Zl, in turns, indicates that the mean value is inferior than the lower specification (i.e.: in average, specification is not attended).\n")
        
        print("Zmin:")
        print("It is the minimum value between Zu and Zl.")
        print("So, Zmin indicates which specification is more difficult for the process to attend: the upper or the lower one.")
        print("Example: if Zmin = Zl, the mean of the process is closer to the lower specification than it is from the upper specification.")
        print("If Zmin, Zu, and Zl are equal, than the process is equally distant from the two specifications.")
        print("Again, if Zmin is negative, at least one of the specifications is not attended.\n")
        
        print("Cpk:")
        print("This is the most fundamental capability indicator.")
        print("Consider again that 99.7% of the normally distributed data are within [(mu - 3s), (mu + 3s)].")
        print("Cpk = Zmin/3")
        print("Cpk = min((([upper specification limit] - mu)/3s), ((mu - [lower specification limit])/3s))")
        print("\n")
        print("Cpk simultaneously assess the process centrality, and if the process is capable of attending its specifications.")
        print("Here, the process centrality is verified as results which are well and simetrically distributed throughout the mean of the specification limits.")
        print("Basically, a perfectly-centralized process has its mean equally distant from both specifications")
        print("i.e., the mean is in the center of the specification interval.")
        print("Cpk = + 1 is usually considered the minimum value acceptable for a process.")
        print("Many quality programs define reaching Cpk = + 1.33 as their goal.")
        print("A 6-sigma process, in turns, is defined as a process with Cpk = + 2.")
        print("\n")
        print("High values of Cpk indicate that the process is not only centralized, but that the differences")
        print("([upper specification limit] - mu) and (mu - [lower specification limit]) are greater than 3s.")
        print("Since mu +- 3s is the range for 99.7% of data, it indicates that most of the values generated fall in a range")
        print("that is only a fraction of the specification range.")
        print("So, it is easier for the process to attend the specifications.")
        print("\n")
        print("Cpk values inferior than 1 indicate that at least one of the intervals ([upper specification limit] - mu) and (mu - [lower specification limit])")
        print("is lower than 3s, i.e., the process naturally generates values beyond at least one of the specifications.")
        print("Low values of Cpk (in particular the negative ones) indicate not-centralized processes and processes not capable of attending their specifications.")
        print("So, lower (and, specially, more negative) Cpk: process' outputs more distant from the specifications.\n")
        
        print("Cpm:")
        print("This indicator is a more generalized version of the Cpk.")
        print("It basically consists on a standard normalization of the Cpk.")
        print("For that, a normalization factor is defined as:")
        print("factor = square root(1 + ((mu - target)/s)**2)")
        print("where target is the center of the specification limits, and **2 represents the second power (square)")
        print("Cpm = Cpk/(factor)")


class RegexHelp:
    """
    Class for calling an user interactive help assistant to guide the creation of correct Regular Expressions
    (Regex). Alternatively, one could ask ChatGPT to make the Regex.

    def __init__ (self, start_helper = True, helper_screen = 0)
    """

    def __init__ (self, start_helper = True, helper_screen = 0):
        
        # from DataCamp course Regular Expressions in Python
        # https://www.datacamp.com/courses/regular-expressions-in-python#!

        self.start_helper = start_helper
        self.helper_screen = helper_screen
        
        self.helper_menu_1 = """

        Regular Expressions (RegEx) Helper
                        
        Input the number in the text box and press enter to visualize help and examples for a topic:

        1. regex basic theory and most common metacharacters
        2. regex quantifiers
        3. regex anchoring and finding
        4. regex greedy and non-greedy search
        5. regex grouping and capturing
        6. regex alternating and non-capturing groups
        7. regex backreferences
        8. regex lookaround
        9. print all topics at once
        10. Finish regex helper
        
        """
        
        # regex basic theory and most common metacharacters
        self.help_text_1 = """
        REGular EXpression or regex:
        String containing a combination of normal characters and special metacharacters that
        describes patterns to find text or positions within a text.

        Example:

        r'st\d\s\w{3,10}'
        - In Python, the r at the beginning indicates a raw string. It is always advisable to use it.
        - We said that a regex contains normal characters, or literal characters we already know. 
            - The normal characters match themselves. 
            - In the case shown above, 'st' exactly matches an 's' followed by a 't'.

        - Most important metacharacters:
            - \d: digit (number);
            - \D: non-digit;
            - \s: whitespace;
            - \s+: one or more consecutive whitespaces.
            - \S: non-whitespace;
            - \w: (word) character;
            - \W: non-word character.
            - {N, M}: indicates that the character on the left appears from N to M consecutive times.
                - \w{3,10}: a word character that appears 3, 4, 5,..., or 10 consecutive times.
            - {N}: indicates that the character on the left appears exactly N consecutive times.
                - \d{4}: a digit appears 4 consecutive times.
            - {N,}: indicates that the character appears at least N times.
                - \d{4,}: a digit appears 4 or more times.
                - phone_number = "John: 1-966-847-3131 Michelle: 54-908-42-42424"
                - re.findall(r"\d{1,2}-\d{3}-\d{2,3}-\d{4,}", phone_number) - returns: ['1-966-847-3131', '54-908-42-42424']

        ATTENTION: Using metacharacters in regular expressions will allow you to match types of characters such as digits. 
        - You can encounter many forms of whitespace such as tabs, space or new line. 
        - To make sure you match all of them always specify whitespaces as \s.

        re module: Python standard library module to search regex within individual strings.

        - .findall method: search all occurrences of the regex within the string, returning a list of strings.
        - Syntax: re.findall(r"regex", string)
            - Example: re.findall(r"#movies", "Love #movies! I had fun yesterday going to the #movies")
                - Returns: ['#movies', '#movies']

        - .split method: splits the string at each occurrence of the regex, returning a list of strings.
        - Syntax: re.split(r"regex", string)
            - Example: re.split(r"!", "Nice Place to eat! I'll come back! Excellent meat!")
                - Returns: ['Nice Place to eat', " I'll come back", ' Excellent meat', '']

        - .sub method: replace one or many matches of the regex with a given string (returns a replaced string).
        - Syntax: re.sub((r"regex", new_substring, original_string))
            - Example: re.sub(r"yellow", "nice", "I have a yellow car and a yellow house in a yellow neighborhood")
            - Returns: 'I have a nice car and a nice house in a nice neighborhood'

        - .search and .match methods: they have the same syntax and are used to find a match. 
            - Both methods return an object with the match found. 
            - The difference is that .match is anchored at the beginning of the string.
        - Syntax: re.search(r"regex", string) and re.match(r"regex", string)
            - Example 1: re.search(r"\d{4}", "4506 people attend the show")
            - Returns: <_sre.SRE_Match object; span=(0, 4), match='4506'>
            - re.match(r"\d{4}", "4506 people attend the show")
            - Returns: <_sre.SRE_Match object; span=(0, 4), match='4506'>
                - In this example, we use both methods to find a digit appearing four times. 
                - Both methods return an object with the match found.
            
            - Example 2: re.search(r"\d+", "Yesterday, I saw 3 shows")
            - Returns: <_sre.SRE_Match object; span=(17, 18), match='3'>
            - re.match(r"\d+","Yesterday, I saw 3 shows")
            - Returns: None
                - In this example,, we used them to find a match for a digit. 
                - In this case, .search finds a match, but .match does not. 
                - This is because the first characters do not match the regex.

        - .group method: detailed in Section 7 (Backreferences).
            - Retrieves the groups captured.
        - Syntax: searched_string = re.search(r"regex", string)
            re.group(N) - returns N-th group captured (group 0 is the regex itself).
            
            Example: text = "Python 3.0 was released on 12-03-2008."
            information = re.search('(\d{1,2})-(\d{2})-(\d{4})', text)
            information.group(3) - returns: '2008'
        - .group can only be used with .search and .match methods.

        Examples of regex:

        1. re.findall(r"User\d", "The winners are: User9, UserN, User8")
            ['User9', 'User8']
        2. re.findall(r"User\D", "The winners are: User9, UserN, User8")
            ['UserN']
        3. re.findall(r"User\w", "The winners are: User9, UserN, User8")
            ['User9', 'UserN', 'User8']
        4. re.findall(r"\W\d", "This skirt is on sale, only $5 today!")
            ['$5']
        5. re.findall(r"Data\sScience", "I enjoy learning Data Science")
            ['Data Science']
        6. re.sub(r"ice\Scream", "ice cream", "I really like ice-cream")
            'I really like ice cream'

        7. regex that matches the user mentions that starts with @ and follows the pattern @robot3!.

        regex = r"@robot\d\W"

        8. regex that matches the number of user mentions given as, for example: User_mentions:9.

        regex = r"User_mentions:\d"

        9. regex that matches the number of likes given as, for example, likes: 5.

        regex = r"likes:\s\d"

        10. regex that matches the number of retweets given as, for example, number of retweets: 4.

        regex = r"number\sof\sretweets:\s\d"

        11. regex that matches the user mentions that starts with @ and follows the pattern @robot3!.

        regex_sentence = r"\W\dbreak\W"

        12. regex that matches the pattern #newH

        regex_words = r"\Wnew\w"

        """

        # regex quantifiers
        self.help_text_2 = """
        Quantifiers: 
        A metacharacter that tells the regex engine how many times to match a character immediately to its left.

            1. +: Once or more times.
                - text = "Date of start: 4-3. Date of registration: 10-04."
                - re.findall(r"\d+-\d+", text) - returns: ['4-3', '10-04']
                - Again, \s+ represents one or more consecutive whitespaces.
            2. *: Zero times or more.
                - my_string = "The concert was amazing! @ameli!a @joh&&n @mary90"
                - re.findall(r"@\w+\W*\w+", my_string) - returns: ['@ameli!a', '@joh&&n', '@mary90']
            3. ?: Zero times or once: ?
                - text = "The color of this image is amazing. However, the colour blue could be brighter."
                - re.findall(r"colou?r", text) - returns: ['color', 'colour']
            
        The quantifier refers to the character immediately on the left:
        - r"apple+" : + applies to 'e' and not to 'apple'.

        Examples of regex:

        1. Most of the times, links start with 'http' and do not contain any whitespace, e.g. https://www.datacamp.com. 
        - regex to find all the matches of http links appearing:
            - regex = r"http\S+"
            - \S is very useful to use when you know a pattern does not contain spaces and you have reached the end when you do find one.

        2. User mentions in Twitter start with @ and can have letters and numbers only, e.g. @johnsmith3.
        - regex to find all the matches of user mentions appearing:
            - regex = r"@\w*\d*"

        3. regex that finds all dates in a format similar to 27 minutes ago or 4 hours ago.
        - regex = r"\d{1,2}\s\w+\sago"

        4. regex that finds all dates in a format similar to 23rd june 2018.
        - regex = r"\d{1,2}\w{2}\s\w+\s\d{4}"

        5. regex that finds all dates in a format similar to 1st september 2019 17:25.
        - regex = r"\d{1,2}\w{2}\s\w+\s\d{4}\s\d{1,2}:\d{2}"

        6. Hashtags start with a # symbol and contain letters and numbers but never whitespace.
        - regex that matches the described hashtag pattern.
            - regex = r"#\w+"
            
        """

        # regex anchoring and finding
        self.help_text_3 = """
        - Anchoring and Finding Metacharacters

            1. . (dot): Match any character (except newline).
                - my_links = "Just check out this link: www.amazingpics.com. It has amazing photos!"
                - re.findall(r"www.+com", my_links) - returns: ['www.amazingpics.com']
                    - The dot . metacharacter is very useful when we want to match all repetitions of any character. 
                    - However, we need to be very careful how we use it.
            2. ^: Anchoring on start of the string.
                - my_string = "the 80s music was much better that the 90s"
                - If we do re.findall(r"the\s\d+s", my_string) - returns: ['the 80s', 'the 90s']
                - Using ^: re.findall(r"^the\s\d+s", my_string) - returns: ['the 80s']
            3. $: Anchoring at the end of the string.
                - my_string = "the 80s music hits were much better that the 90s"
                - re.findall(r"the\s\d+s$", my_string) - returns: ['the 90s']
            4. \: Escape special characters.
                - my_string = "I love the music of Mr.Go. However, the sound was too loud."
                    - re.split(r".\s", my_string) - returns: ['', 'lov', 'th', 'musi', 'o', 'Mr.Go', 'However', 'th', 'soun', 'wa', 'to', 'loud.']
                    - re.split(r"\.\s", my_string) - returns: ['I love the music of Mr.Go', 'However, the sound was too loud.']
            5. |: OR Operator
                - my_string = "Elephants are the world's largest land animal! I would love to see an elephant one day"
                - re.findall(r"Elephant|elephant", my_string) - returns: ['Elephant', 'elephant']
            6. []: set of characters representing the OR Operator.
                Example 1 - my_string = "Yesterday I spent my afternoon with my friends: MaryJohn2 Clary3"
                - re.findall(r"[a-zA-Z]+\d", my_string) - returns: ['MaryJohn2', 'Clary3']
                Example 2 - my_string = "My&name&is#John Smith. I%live$in#London."
                - re.sub(r"[#$%&]", " ", my_string) - returns: 'My name is John Smith. I live in London.'
                
                Note 1: within brackets, the characters to be found should not be separated, as in [#$%&].
                    - Whitespaces or other separators would be interpreted as characters to be found.
                Note 2: [a-z] represents all word characters from 'a' to 'z', lowercase.
                        - [A-Z] represents all word characters from 'A' to 'Z', uppercase.
                        - Since lower and uppercase are different, we must declare [a-zA-Z] or [A-Za-z] to capture all word characters.
                        - [0-9] represents all digits from 0 to 9.
                        - Something like [a-zA-Z0-9] or [a-z0-9A-Z] will search all word characters and all numbers.
            
            7. [^ ]: OR operator combined to ^ transforms the expression to negative.
                - my_links = "Bad website: www.99.com. Favorite site: www.hola.com"
                - re.findall(r"www[^0-9]+com", my_links) - returns: ['www.hola.com']

        Examples of regex:

        1. You want to find names of files that appear at the start of the string; 
            - always start with a sequence of 2 or 3 upper or lowercase vowels (a e i o u); 
            - and always finish with the txt ending.
                - Write a regex that matches the pattern of the text file names, e.g. aemyfile.txt.
                # . = match any character
                regex = r"^[aeiouAEIOU]{2,3}.+txt"

        2. When a user signs up on the company website, they must provide a valid email address.
            - The company puts some rules in place to verify that the given email address is valid:
            - The first part can contain: Upper A-Z or lowercase letters a-z; 
            - Numbers; Characters: !, #, %, &, *, $, . Must have @. Domain: Can contain any word characters;
            - But only .com ending is allowed. 
                - Write a regular expression to match valid email addresses.
                - Match the regex to the elements contained in emails, and print out the message indicating if it is a valid email or not 
            
            # Write a regex to match a valid email address
            regex = r"^[A-Za-z0-9!#%&*$.]+@\w+\.com"

            for example in emails:
                # Match the regex to the string
                if re.match(regex, example):
                    # Complete the format method to print out the result
                    print("The email {email_example} is a valid email".format(email_example=example))
                else:
                    print("The email {email_example} is invalid".format(email_example=example))
            
            # Notice that we used the .match() method. 
            # The reason is that we want to match the pattern from the beginning of the string.

        3. Rules in order to verify valid passwords: it can contain lowercase a-z and uppercase letters A-Z;
            - It can contain numbers; it can contain the symbols: *, #, $, %, !, &, .
            - It must be at least 8 characters long but not more than 20.
                - Write a regular expression to check if the passwords are valid according to the description.
                - Search the elements in the passwords list to find out if they are valid passwords.
                - Print out the message indicating if it is a valid password or not, complete .format() statement.
            
            # Write a regex to check if the password is valid
            regex = r"[a-z0-9A-Z*#$%!&.]{8,20}"

            for example in passwords:
                # Scan the strings to find a match
                if re.match(regex, example):
                    # Complete the format method to print out the result
                    print("The password {pass_example} is a valid password".format(pass_example=example))
                else:
                    print("The password {pass_example} is invalid".format(pass_example=example))

        """

        # regex greedy and non-greedy search
        self.help_text_4 = """
        There are two types of matching methods: greedy and non-greedy (also called lazy) operators. 

        Greedy operators
        - The standard quantifiers are greedy by default, meaning that they will attempt to match as many characters as possible.
            - Standard quantifiers: * , + , ? , {num, num}
            - Example: re.match(r"\d+", "12345bcada") - returns: <_sre.SRE_Match object; span=(0, 5), match='12345'>
            - We can explain this in the following way: our quantifier will start by matching the first digit found, '1'. 
            - Because it is greedy, it will keep going to find 'more' digits and stop only when no other digit can be matched, returning '12345'.
        - If the greedy quantifier has matched so many characters that can not match the rest of pattern, it will backtrack, giving up characters matched earlier one at a time and try again. 
        - Backtracking is like driving a car without a map. If you drive through a path and hit a dead end street, you need to backtrack along your road to an earlier point to take another street. 
            - Example: re.match(r".*hello", "xhelloxxxxxx") - returns: <_sre.SRE_Match object; span=(0, 6), match='xhello'>
            - We use the greedy quantifier .* to find anything, zero or more times, followed by the letters "h" "e" "l" "l" "o". 
            - We can see here that it returns the pattern 'xhello'. 
            - So our greedy quantifier will start by matching as much as possible, the entire string. 
            - Then, it tries to match the h, but there are no characters left. So it backtracks, giving up one matched character. 
            - Trying again, it still doesn't match the h, so it backtracks one more step repeatedly until it finally matches the h in the regex, and the rest of the characters.

        Non-greedy (lazy) operators
        - Because they have lazy behavior, non-greedy quantifiers will attempt to match as few characters as needed, returning the shortest match. 
        - To obtain non-greedy quantifiers, we can append a question mark at the end of the greedy quantifiers to convert them into lazy. 
            - Example: re.match(r"\d+?", "12345bcada") - returns: <_sre.SRE_Match object; span=(0, 1), match='1'>
            - Now, our non-greedy quantifier will return the pattern '1'. 
            - In this case, our quantifier will start by matching the first digit found, '1'. 
            - Because it is non-greedy, it will stop there, as we stated that we want 'one or more', and 1 is as few as needed.
        - Non-greedy quantifiers also backtrack. 
        - In this case, if they have matched so few characters that the rest of the pattern cannot match, they backtrack, expand the matched character one at a time, and try again. 
        - In the example above: this time we use the lazy quantifier .*?. Interestingly, we obtain the same match 'xhello'. 
        - But, how this match was obtained is different from the first time: the lazy quantifier first matches as little as possible, nothing, leaving the entire string unmatched. 
        - Then it tries to match the 'h', but it doesn't work. 
        - So, it backtracks, matching one more character, the 'x'. Then, it tries again, this time matching the 'h', and afterwards, the rest of the regex.

        - Even though greedy quantifiers lead to longer matches, they are sometimes the best option. 
        - Because lazy quantifiers match as few as possible, they return a shorter match than we expected.
            - Example: if you want to extract a word starting with 'a' and ending with 'e' in the string 'I like apple pie', you may think that applying the greedy regex r"a.+e" will return 'apple'. 
            - However, your match will be 'apple pie'. A way to overcome this is to make it lazy by using '?'' which will return 'apple'.
        - On the other hand, using greedy quantifiers always leads to longer matches that sometimes are not desired. 
            - Making quantifiers lazy by adding '?' to match a shorter pattern is a very important consideration to keep in mind when handling data for text mining.

        Examples of regex:

        1. You want to extract the number contained in the sentence 'I was born on April 24th'. 
            - A lazy quantifier will make the regex return 2 and 4, because they will match as few characters as needed. 
            - However, a greedy quantifier will return the entire 24 due to its need to match as much as possible.

            1.1. Use a lazy quantifier to match all numbers that appear in the variable sentiment_analysis:
            numbers_found_lazy = re.findall(r"[0-9]+?", sentiment_analysis)
            - Output: ['5', '3', '6', '1', '2']
            
            1.2. Now, use a greedy quantifier to match all numbers that appear in the variable sentiment_analysis.
            numbers_found_greedy = re.findall(r"[0-9]+", sentiment_analysis)
            - Output: ['536', '12']

        2.1. Use a greedy quantifier to match text that appears within parentheses in the variable sentiment_analysis.
            
            sentences_found_greedy = re.findall(r"\(.+\)", sentiment_analysis)
            - Output: ["(They were so cute) a few yrs ago. PC crashed, and now I forget the name of the site ('I'm crying)"]

        2.2. Now, use a lazy quantifier to match text that appears within parentheses in the variable sentiment_analysis.

            sentences_found_lazy = re.findall(r"\(.+?\)", sentiment_analysis)
            - Output: ["(They were so cute)", "('I'm crying)"]
            
        """

        # regex grouping and capturing
        self.help_text_5 = """
        Capturing groups in regular expressions
        - Let's say that we have the following text:
            
            text = "Clary has 2 friends who she spends a lot time with. Susan has 3 brothers while John has 4 sisters."
            
        - We want to extract information about a person, how many and which type of relationships they have. 
        - So, we want to extract Clary 2 friends, Susan 3 brothers and John 4 sisters.
        - If we do: re.findall(r'[A-Za-z]+\s\w+\s\d+\s\w+', text), the output will be: ['Clary has 2 friends', 'Susan has 3 brothers', 'John has 4 sisters']
            - The output is quite close, but we do not want the word 'has'.

        - We start simple, by trying to extract only the names. We can place parentheses to group those characters, capture them, and retrieve only that group:
            - re.findall(r'([A-Za-z]+)\s\w+\s\d+\s\w+', text) - returns: ['Clary', 'Susan', 'John']
        - Actually, we can place parentheses around the three groups that we want to capture. 
            - re.findall(r'([A-Za-z]+)\s\w+\s(\d+)\s(\w+)', text)
            
            - Each group will receive a number: 
                - The entire expression will always be group 0. 
                - The first group: 1; the second: 2; and the third: 3.
            
            - The result returned is: [('Clary', '2', 'friends'), ('Susan', '3', 'brothers'), ('John', '4', 'sisters')]
                - We got a list of tuples: 
                    - The first element of each tuple is the match captured corresponding to group 1. 
                    - The second, to group 2. The last, to group 3.
            
            - We can use capturing groups to match a specific subpattern in a pattern. 
            - We can use this information for retrieving the groups by numbers; or to organize data.
                - Example: pets = re.findall(r'([A-Za-z]+)\s\w+\s(\d+)\s(\w+)', "Clary has 2 dogs but John has 3 cats")
                            pets[0][0] == 'Clary'
                            - In the code, we placed the parentheses to capture the name of the owner, the number and which type of pets each one has. 
                            - We can access the information retrieved by using indexing and slicing as seen in the code. 
        
        - Capturing groups have one important feature. 
            - Remember that quantifiers apply to the character immediately to the left. 
            - So, we can place parentheses to group characters and then apply the quantifier to the entire group. 
            
            Example: re.search(r"(\d[A-Za-z])+", "My user name is 3e4r5fg")
                - returns: <_sre.SRE_Match object; span=(16, 22), match='3e4r5f'>
                - In the code, we have placed parentheses to match the group containing a number and any letter. 
                - We applied the plus quantifier to specify that we want this group repeated once or more times. 
            
        - ATTENTION: It's not the same to capture a repeated group AND to repeat a capturing group. 
            
            my_string = "My lucky numbers are 8755 and 33"
            - re.findall(r"(\d)+", my_string) - returns: ['5', '3']
            - re.findall(r"(\d+)", my_string) - returns: ['8755', '33']
            
            - In the first code, we use findall to match a capturing group containing one number. 
                - We want this capturing group to be repeated once or more times. 
                - We get 5 and 3 as an output, because these numbers are repeated consecutively once or more times. 
            - In the second code, we specify that we should capture a group containing one or more repetitions of a number. 

        - Placing a subpattern inside parenthesis will capture that content and stores it temporarily in memory. This can be later reused.

        Examples of regex:

        1. You want to extract the first part of the email. E.g. if you have the email marysmith90@gmail.com, you are only interested in marysmith90.
        - You need to match the entire expression. So you make sure to extract only names present in emails. Also, you are only interested in names containing upper (e.g. A,B, Z) or lowercase letters (e.g. a, d, z) and numbers.
        - regex to match the email capturing only the name part. The name part appears before the @.
            - regex_email = r"([a-z0-9A-Z]+)@\S+"

        2. Text follows a pattern: "Here you have your boarding pass LA4214 AER-CDB 06NOV."
        - You need to extract the information about the flight: 
            - The two letters indicate the airline (e.g LA); the 4 numbers are the flight number (e.g. 4214);
            - The three letters correspond to the departure (e.g AER); the destination (CDB); the date (06NOV) of the flight.
            - All letters are always uppercase.

        - Regular expression to match and capture all the flight information required.
        - Find all the matches corresponding to each piece of information about the flight. Assign it to flight_matches.
        - Complete the format method with the elements contained in flight_matches: 
            - In the first line print the airline and the flight number. 
            - In the second line, the departure and destination. In the third line, the date.

        # Import re
        import re

        # Write regex to capture information of the flight
        regex = r"([A-Z]{2})(\d{4})\s([A-Z]{3})-([A-Z]{3})\s(\d{2}[A-Z]{3})"

        # Find all matches of the flight information
        flight_matches = re.findall(regex, flight)
            
        #Print the matches
        print("Airline: {} Flight number: {}".format(flight_matches[0][0], flight_matches[0][1]))
        print("Departure: {} Destination: {}".format(flight_matches[0][2], flight_matches[0][3]))
        print("Date: {}".format(flight_matches[0][4]))

            - findall() returns a list of tuples. 
            - The nth element of each tuple is the element corresponding to group n. 
            - This provides us with an easy way to access and organize our data.

        """

        # regex alternating and non-capturing groups
        self.help_text_6 = """
        Alternating and non-capturing groups

        - Vertical bar or pipe operator
            - Suppose we have the following string, and we want to find all matches for pet names. 
            - We can use the pipe operator to specify that we want to match cat or dog or bird:
                - my_string = "I want to have a pet. But I don't know if I want a cat, a dog or a bird."
                - re.findall(r"cat|dog|bird", my_string) - returns: ['cat', 'dog', 'bird']
            
            - Now, we changed the string a little bit, and once more we want to find all the pet names, but only those that come after a number and a whitespace. 
            - So, if we specify this again with the pipe operator, we get the wrong output: 
                - my_string = "I want to have a pet. But I don't know if I want 2 cats, 1 dog or a bird."
                - re.findall(r"\d+\scat|dog|bird", my_string) - returns: ['2 cat', 'dog', 'bird']
            
            - That is because the pipe operator works by comparing everything that is to its left (digit whitespace cat) with everything to the right, dog.
            - In order to solve this, we can use alternation. 
                - In simpler terms, we can use parentheses again to group the optional characters:
                
                - my_string = "I want to have a pet. But I don't know if I want 2 cats, 1 dog or a bird."
                - re.findall(r"\d+\s(cat|dog|bird)", my_string) - returns: ['cat', 'dog']
                
                In the code, now the parentheses are added to group cat or dog or bird.
            
            - In the previous example, we may also want to match the number. 
            - In that case, we need to place parentheses to capture the digit group:
            
                - my_string = "I want to have a pet. But I don't know if I want 2 cats, 1 dog or a bird."
                - re.findall(r"(\d)+\s(cat|dog|bird)", my_string) - returns: [('2', 'cat'), ('1', 'dog')]
            
                - In the code, we now use two pair of parentheses and we use findall in the string, so we get a list with two tuples.
            
        - Non-capturing groups
            - Sometimes, we need to group characters using parentheses, but we are not going to reference back to this group. 
            - For these cases, there are a special type of groups called non-capturing groups. 
            - For using them, we just need to add question mark colon inside the parenthesis but before the regex.
            
            regex = r"(?:regex)"
            
            - Example: we have the following string, and we want to find all matches of numbers. 
            
                my_string = "John Smith: 34-34-34-042-980, Rebeca Smith: 10-10-10-434-425"
            
            - We see that the pattern consists of two numbers and dash repeated three times. After that, three numbers, dash, four numbers. 
            - We want to extract only the last part, without the first repeated elements. 
            - We need to group the first two elements to indicate repetitions, but we do not want to capture them. 
            - So, we use non-capturing groups to group \d repeated two times and dash. Then we indicate this group should be repeated three times. Then, we group \d repeated three times, dash, \d repeated three times:
            
                re.findall(r"(?:\d{2}-){3}(\d{3}-\d{3})", my_string) - returns: ['042-980', '434-425']
            
        - Alternation
            - We can combine non-capturing groups and alternation together. 
            - Remember that alternation implies using parentheses and the pipe operand to group optional characters. 
            - Let's suppose that we have the following string. We want to match all the numbers of the day. 
            
                my_date = "Today is 23rd May 2019. Tomorrow is 24th May 19."
            
            - We know that they are followed by 'th' or 'rd', but we only want to capture the number, and not the letters that follow it. 
            - We write our regex to capture inside parentheses \d repeated once or more times. Then, we can use a non-capturing group. 
            - Inside, we use the pipe operator to choose between 'th' or 'rd':
            
                re.findall(r"(\d+)(?:th|rd)", my_date) - returns: ['23', '24']

        - Non-capturing groups are very often used together with alternation. 
        - Sometimes, you have optional patterns and you need to group them. 
        - However, you are not interested in keeping them. It's a nice feature of regex.

        Examples of regex:

        1. Sentiment analysis project: firstly, you want to identify positive tweets about movies and concerts.
        - You plan to find all the sentences that contain the words 'love', 'like', or 'enjoy', and capture that word. 
        - You will limit the tweets by focusing on those that contain the words 'movie' or 'concert' by keeping the word in another group. 
        - You will also save the movie or concert name.
            - For example, if you have the sentence: 'I love the movie Avengers', you match and capture 'love'. 
            - You need to match and capture 'movie'. Afterwards, you match and capture anything until the dot.
            - The list sentiment_analysis contains the text of tweets.
        - Regular expression to capture the words 'love', 'like', or 'enjoy'; 
            - match and capture the words 'movie' or 'concert'; 
            - match and capture anything appearing until the '.'.

            regex_positive = r"(love|like|enjoy).+?(movie|concert)\s(.+?)\."

            - The pipe operator works by comparing everything that is to its left with everything to the right. 
            - Grouping optional patterns is the way to get the correct result.

        2. After finding positive tweets, you want to do it for negative tweets. 
        - Your plan now is to find sentences that contain the words 'hate', 'dislike' or 'disapprove'. 
        - You will again save the movie or concert name. 
        - You will get the tweet containing the words 'movie' or 'concert', but this time, you do not plan to save the word.
            - For example, if you have the sentence: 'I dislike the movie Avengers a lot.', you match and capture 'dislike'. 
            - You will match, but not capture, the word 'movie'. Afterwards, you match and capture anything until the dot.
        - Regular expression to capture the words 'hate', 'dislike' or 'disapprove'; 
            - Match, but do not capture, the words 'movie' or 'concert'; 
            - Match and capture anything appearing until the '.'.
            
            regex_negative = r"(hate|dislike|disapprove).+?(?:movie|concert)\s(.+?)\."
                
                """

        # regex backreferences
        self.help_text_7 = """
        Backreferences
        - How we can backreference capturing groups.

        Numbered groups
        - Imagine we come across this text, and we want to extract the date: 
            
            text = "Python 3.0 was released on 12-03-2008. It was a major revision of the language. Many of its major features were backported to Python 2.6.x and 2.7.x version series."
            
        - We want to extract only the numbers. So, we can place parentheses in a regex to capture these groups:
            
            regex = r"(\d{1,2})-(\d{1,2})-(\d{4})"

        - We have also seen that each of these groups receive a number. 
        - The whole expression is group 0; the first group, 1; and so on.

        - Let's use .search to match the pattern to the text. 
        - To retrieve the groups captured, we can use the method .group specifying the number of a group we want. 

        Again: .group method retrieves the groups captured.
            - Syntax: searched_string = re.search(r"regex", string)
            re.group(N) - returns N-th group captured (group 0 is the regex itself).

        Example: text = "Python 3.0 was released on 12-03-2008."

            information = re.search('(\d{1,2})-(\d{2})-(\d{4})', text)
            information.group(3) - returns: '2008'
            information.group(0) - returns: '12-03-2008' (regex itself, the entire expression).

        - .group can only be used with .search and .match methods.

        Named groups
        - We can also give names to our capturing groups. 
        - Inside the parentheses, we write '?P', and the name inside angle brackets:

            regex = r"(?P<name>regex)"

        - Let's say we have the following string, and we want to match the name of the city and zipcode in different groups. 
        - We can use capturing groups and assign them the name 'city' and 'zipcode'. 
        - We retrieve the information by using .group, and we indicate the name of the group. 
            
            text = "Austin, 78701"
            cities = re.search(r"(?P<city>[A-Za-z]+).*?(?P<zipcode>\d{5})", text)
            cities.group("city") - returns: 'Austin'
            cities.group("zipcode") - returns: '78701'

        Backreferences
        - There is another way to backreference groups. 
        - In fact, the matched group can be reused inside the same regex or outside for substitution. 
        - We can do this using backslash and the number of the group:

            regex = r'(\d{1,2})-(\d{2})-(\d{4})'
            
            - we can backreference the groups as:
                (\d{1,2}): (\1);
                (\d{2}): (\2)
                (\d{4}): (\3)

        - Example: we have the following string, and we want to find all matches of repeated words. 
        - In the code, we specify that we want to capture a sequence of word characters, then a whitespace.
        - Finally, we write \1. This will indicate that we want to match the first group captured again. 
        - In other words, it says: 'match that sequence of characters that was previously captured once more.' 
            
            sentence = "I wish you a happy happy birthday!"
            re.findall(r"(\w+)\s\1", sentence) - returns: ['happy'] 

        - We get the word 'happy' as an output: this was the repeated word in our string.

        - Now, we want to replace the repeated word with one occurrence of the same word. 
        - In the code, we use the same regex as before, but this time, we use the .sub method. 
        - In the replacement part, we can also reference back to the captured group: 
            - We write r"\1" to say: 'replace the entire expression match with the first captured group.' 
            
            re.sub(r"(\w+)\s\1", r"\1", sentence) - returns: 'I wish you a happy birthday!'
            - In the output string, we have only one occurrence of the word 'happy'.
            
        - We can also use named groups for backreferencing. 
        - To do this, we use ?P= the group name. 

            regex = r"(?P=name)"

        Example:
            sentence = "Your new code number is 23434. Please, enter 23434 to open the door."
            re.findall(r"(?P<code>\d{5}).*?(?P=code)", sentence) - returns: ['23434']

        - In the code, we want to find all matches of the same number. 
        - We use a capturing group and name it 'code'. 
        - Later, we reference back to this group, and we obtain the number as an output.

        - To reference the group back for replacement, we need to use \g and the group name inside angle brackets. 

            regex = r"(\g<name>)"

        Example:
            sentence = "This app is not working! It's repeating the last word word."
            re.sub(r"(?P<word>\w+)\s(?P=word)", r"\g<word>", sentence) - returns: 'This app is not working! It's repeating the last word.'
            
        - In the code, we want to replace repeated words by one occurrence of the same word. 
        - Inside the regex, we use the previous syntax. 
        - In the replacement field, we need to use this new syntax as seen in the code.
        - Backreferences are very helpful when you need to reuse part of the regex match inside the regex.
        - You should remember that the group zero stands for the entire expression matched. 
            - It is always helpful to keep that in mind. Sometimes you will need to use it.

        Examples of regex:

        1. Parsing PDF files: your company gave you some PDF files of signed contracts. The goal of the project is to create a database with the information you parse from them. 
        - Three of these columns should correspond to the day, month, and year when the contract was signed.
        - The dates appear as 'Signed on 05/24/2016' ('05' indicating the month, '24' the day). 
        - You decide to use capturing groups to extract this information. Also, you would like to retrieve that information so you can store it separately in different variables.
        - The variable contract contains the text of one contract.

        - Write a regex that captures the month, day, and year in which the contract was signed. 
        - Scan contract for matches.
        - Assign each captured group to the corresponding keys in the dictionary.
        - Complete the positional method to print out the captured groups. 
        - Use the values corresponding to each key in the dictionary.

            # Write regex and scan contract to capture the dates described
            regex_dates = r"Signed\son\s(\d{2})/(\d{2})/(\d{4})"
            dates = re.search(regex_dates, contract)

            # Assign to each key the corresponding match
            signature = {
                "day": dates.group(2),
                "month": dates.group(1),
                "year": dates.group(3)
            }
            # Complete the format method to print-out
            print("Our first contract is dated back to {data[year]}. Particularly, the day {data[day]} of the month {data[month]}.".format(data=signature))

        - Remember that each capturing group is assigned a number according to its position in the regex. 
        - Only if you use .search() and .match(), you can use .group() to retrieve the groups.

        2. The company is going to develop a new product which will help developers automatically check the code they are writing. 
        - You need to write a short script for checking that every HTML tag that is open has its proper closure.
        - You have an example of a string containing HTML tags: "<title>The Data Science Company</title>"
        - You learn that an opening HTML tag is always at the beginning of the string, and appears inside "<>". 
        - A closing tag also appears inside "<>", but it is preceded by "/".
        - The list html_tags, contains strings with HTML tags.

        - Regex to match closed HTML tags: find if there is a match in each string of the list html_tags. Assign the result to match_tag;
            - If a match is found, print the first group captured and saved in match_tag;
        - If no match is found, regex to match only the text inside the HTML tag. Assign it to notmatch_tag.
            - Print the first group captured by the regex and save it in notmatch_tag.
            - To capture the text inside <>, place parenthesis around the expression: r"<(text)>. To confirm that the same text appears in the closing tag, reference back to the m group captured by using '\m'.
            - To print the 'm' group captured, use .group(m).

            for string in html_tags:
                # Complete the regex and find if it matches a closed HTML tags
                match_tag =  re.match(r"<(\w+)>.*?</\1>", string)

                if match_tag:
                    # If it matches print the first group capture
                    print("Your tag {} is closed".format(match_tag.group(1))) 
                else:
                    # If it doesn't match capture only the tag 
                    notmatch_tag = re.match(r"<(\w+)>",string)
                    # Print the first group capture
                    print("Close your {} tag!".format(notmatch_tag.group(1)))

        3. Your task is to replace elongated words that appear in the tweets. 
        - We define an elongated word as a word that contains a repeating character twice or more times. 
            - e.g. "Awesoooome".
        - Replacing those words is very important since a classifier will treat them as a different term from the source words, lowering their frequency.
        - To find them, you will use capturing groups and reference them back using numbers. E.g \4.
        - If you want to find a match for 'Awesoooome', you firstly need to capture 'Awes'. 
            - Then, match 'o' and reference the same character back, and then, 'me'.
        - The list sentiment_analysis contains the text tweets.
        - Regular expression to match an elongated word as described.
        - Search the elements in sentiment_analysis list to find out if they contain elongated words. Assign the result to match_elongated.
        - Assign the captured group number zero to the variable elongated_word.
            - Print the result contained in the variable elongated_word.

            # Complete the regex to match an elongated word
            regex_elongated = r"\w*(\w)\1*me\w*"

            for tweet in sentiment_analysis:
                # Find if there is a match in each tweet 
                match_elongated = re.search(regex_elongated, tweet)

                if match_elongated:
                    # Assign the captured group zero 
                    elongated_word = match_elongated.group(0)

                    # Complete the format method to print the word
                    print("Elongated word found: {word}".format(word=elongated_word))
                else:
                    print("No elongated word found") 

                """
        
        # regex lookaround
        self.help_text_8 = """
        Lookaround
        - There are specific types of non-capturing groups that help us look around an expression.
        - Look-around will look for what is behind or ahead of a pattern. 
        - Imagine that we have the following string:
            
            text = "the white cat sat on the chair"

        - We want to see what is surrounding a specific word. 
        - For example, we position ourselves in the word 'cat'. 
        - So look-around will let us answer the following problem: 
            - At my current position, look ahead and search if 'sat' is there. 
            - Or, look behind and search if 'white' is there.
            
        - In other words, looking around allows us to confirm that a sub-pattern is ahead or behind the main pattern.
        - "At my current position in the matching process, look ahead or behind and examine whether some pattern matches or not match before continuing."
        - In the previous example, we are looking for the word 'cat'. 
        - The look ahead expression can be either positive or negative. For positive we use ?=. For negative, ?!.
            - positive: (?=sat)
            - negative: (?!run)

        - Look-ahead
        - This non-capturing group checks whether the first part of the expression is followed or not by the lookahead expression. 
        - As a consequence, it will return the first part of the expression. 
            - Let's imagine that we have a string containing file names and the status of that file. 
            - We want to extract only those files that are followed by the word 'transferred'. 
            - So we start building the regex by indicating any word character followed by .txt.
            - We now indicate we want the first part to be followed by the word transferred. 
            - We do so by writing ?= and then whitespace transferred all inside the parenthesis:
            
            my_text ="tweets.txt transferred, mypass.txt transferred, keywords.txt error"
            re.findall(r"\w+\.txt(?=\stransferred)", my_text) - returns: ['tweets.txt', 'mypass.txt']

        - Negative look-ahead
            - Now, let's use negative lookahead in the same example.
            - In this case, we will say that we want those matches that are NOT followed by the expression 'transferred'. 
            - We use, instead, ?! inside parenthesis:

            my_text = "tweets.txt transferred, mypass.txt transferred, keywords.txt error"
            re.findall(r"\w+\.txt(?!\stransferred)", my_text) - returns: ['keywords.txt']

        - Look-behind
        - The non-capturing group look-behind gets all matches that are preceded or not by a specific pattern.
        - As a consequence, it will return the matches after the look expression.
        - Look behind expression can also be either positive or negative. 
            - For positive, we use ?<=. For negative, ?<!.
            - So, we add an intermediate '<' (angle bracket) sign. In the previous example, we can look before the word 'cat': 
                - positive: (?<=white)
                - negative: (?<!brown)
            
        - Positive look-behind
            - Let's look at the following string, in which we want to find all matches of the names that are preceded by the word 'member'. 
            - We construct our regex with positive look-behind. 
            - At the end of the regex, we indicate that we want a sequence of word characters whitespace another sequence of word characters:
            
            my_text = "Member: Angus Young, Member: Chris Slade, Past: Malcolm Young, Past: Cliff Williams."
            re.findall(r"(?<=Member:\s)\w+\s\w+", my_text) - returns: ['Angus Young', 'Chris Slade']
            
            - Pay attention to the code: the look-behind expression goes before that expression. 
            - We indicate ?<= followed by member, colon, and whitespace. All inside parentheses. 
            - In that way we get the two names that were preceded by the word member, as shown in the output.

        - Negative look-behind
        - Now, we have other string, in which will use negative look-behind. 
        - We will find all matches of the word 'cat' or 'dog' that are not preceded by the word 'brown'. 
        - In this example, we use ?<!, followed by brown, whitespace. All inside the parenthesis. 
        - Then, we indicate our alternation group: 'cat' or 'dog'. 

            my_text = "My white cat sat at the table. However, my brown dog was lying on the couch."
            re.findall(r"(?<!brown\s)(cat|dog)", my_text) - returns: ['cat']

            - Consequently, we get 'cat' as an output, the 'cat' or 'dog' word that is not after the word 'brown'.

        In summary:
        - Positive lookahead (?=) makes sure that first part of the expression is followed by the lookahead expression. 
        - Positive lookbehind (?<=) returns all matches that are preceded by the specified pattern.
        - It is important to know that positive lookahead will return the text matched by the first part of the expression after asserting that it is followed by the lookahead expression,
            - while positive lookbehind will return all matches that follow a specific pattern.
        - Negative lookarounds work in a similar way to positive lookarounds. 
            - They are very helpful when we are looking to exclude certain patterns from our analysis.

        Examples of regex:

        1. You are interested in the words surrounding 'python'. You want to count how many times a specific words appears right before and after it.
        - The variable sentiment_analysis contains the text of one tweet.
        - Get all the words that are followed by the word 'python' in sentiment_analysis. 
        - Print out the word found.
            - In re.findall(). Use \w+ to match the words followed by the word 'python';
            - In re.findall() first argument, include \spython within parentheses to indicate that everything after the word 'python' should be matched.

            # Positive lookahead
            look_ahead = re.findall(r"\w+(?=\spython)", sentiment_analysis)

            # Print out
            print(look_ahead)
        
        1.2. Get all the words that are preceded by the word 'python' or 'Python' in sentiment_analysis. Print out the words found.
        - In re.findall() first argument, include [Pp]ython\s within parentheses to indicate that everything before the word 'python' (or 'Python') should be matched.

            # Positive lookbehind
            look_behind = re.findall(r"(?<=[pP]ython\s)\w+", sentiment_analysis)

            # Print out
            print(look_behind)

        2. You need to write a script for a cell-phone searcher. 
        - It should scan a list of phone numbers and return those that meet certain characteristics.
        - The phone numbers in the list have the structure:
            - Optional area code: 3 numbers
            - Prefix: 4 numbers
            - Line number: 6 numbers
            - Optional extension: 2 numbers
            - E.g. 654-8764-439434-01.
        - You decide to use .findall() and the non-capturing group's negative lookahead (?!) and negative lookbehind (?<!).
        - The list cellphones, contains three phone numbers:
            cellphones = ['4564-646464-01', '345-5785-544245', '6476-579052-01']

        - Get all cell phones numbers that are not preceded by the optional area code.
            - In re.findall() first argument, you use a negative lookbehind ?<! within parentheses () indicating the optional area code.

            for phone in cellphones:
                # Get all phone numbers not preceded by area code
                number = re.findall(r"(?<!\d{3}-)\d{4}-\d{6}-\d{2}", phone)
                print(number)
        
        2.1. Get all the cell phones numbers that are not followed by the optional extension.
            - In re.findall() first argument, you use a negative lookahead ?! within parentheses () indicating the optional extension.

            for phone in cellphones:
                # Get all phone numbers not followed by optional extension
                number = re.findall(r"\d{3}-\d{4}-\d{6}(?!-\d{2})", phone)
                print(number)
            
                """
        
        
    def show_screen (self):
            
        helper_screen = self.helper_screen
        helper_menu_1 = self.helper_menu_1
            
        if (helper_screen == 0):
                
            # Start screen
            print(self.helper_menu_1)
            print("\n")
            # For the input, strip all whitespaces and, and so convert it to integer:
            helper_screen = int(str(input("Next screen:")).strip())
                
            # the object.__dict__ method returns all attributes from an object as a dictionary.
            # Analogously, the vars function applied to an object vars(object) returns the same
            # dictionary. We can access an attribute from the object by passing the key of this
            # dictionary:
            # vars(object)['key']
                
            while (helper_screen != 10):
                    
                if (helper_screen not in range(0, 11)):
                    # range (0, 11): integers from 0 to 10
                        
                    helper_screen = int(str(input("Input a valid number, from 0 to 10:")).strip())
                    
                else:
                        
                    if (helper_screen == 9):
                        # print all at once:
                        for screen_number in range (1, 9):
                            # integers from 1 to 8
                            key = "help_text_" + str(screen_number)
                            # apply the vars function to get the dictionary of attributes, and call the
                            # attribute by passing its name as key from the dictionary:
                            screen_text = vars(self)[key]
                            # Notice that we cannot directly call the attribute as a string. We would have to
                            # create an if else for each of the 8 attributes.
                            print(screen_text)
                            
                        # Now, make helper_screen = 10 for finishing this step:
                        helper_screen = 10
                        
                    else:
                        key = "help_text_" + str(helper_screen)
                        screen_text = vars(self)[key]
                        print(screen_text)
                        helper_screen = int(str(input("Next screen:")).strip())
            
        print("Finishing regex assistant.\n")
            
        return self
        