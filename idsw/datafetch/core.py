"""FUNCTIONS FROM INDUSTRIAL DATA SCIENCE WORKFLOW (IDSW) PACKAGE
Extract data from Plant Information Management (PIMS) systems
AspenTech IP21
Connect to SQLite Database

Marco Cesar Prado Soares, Data Scientist Specialist @ Bayer Crop Science LATAM
marcosoares.feq@gmail.com
marco.soares@bayer.com"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class InvalidInputsError (Exception): pass  # class for raising errors when invalid inputs are provided.


class IP21Extractor:
    """
    Class for extracting information from Aspentech IP21 database.
    def __init__ (self, tag_to_extract = None, actual_tag_name = None, ip21_server = None, 
                data_source = 'localhost', start_timestamp = None, stop_timestamp = None, ip21time_array = [], 
                previous_df_for_concatenation = None, username = None, password = None):  
    """    

    # Initialize instance attributes.
    # define the Class constructor, i.e., how are its objects:

    def __init__ (self, tag_to_extract = None, actual_tag_name = None, ip21_server = None, data_source = 'localhost', start_timestamp = None, stop_timestamp = None, ip21time_array = [], previous_df_for_concatenation = None, username = None, password = None):
        
        # If the user passes the argument, use them. Otherwise, use the standard values.
        # Set the class objects' attributes.
        # Suppose the object is named assistant. We can access the attribute as:
        # assistant.assistant_startup, for instance.
        # So, we can save the variables as objects' attributes.
        
        self.tag = tag_to_extract
        # If actual_tag_name is None, make it equal to the tag:
        if (actual_tag_name is None):
            actual_tag_name = tag_to_extract
        
        self.actual_tag_name = actual_tag_name
        
        self.start_timestamp = start_timestamp
        self.start_ip21_scale = np.nan # float, instead of None object
        self.stop_timestamp = stop_timestamp
        self.stop_ip21_scale = np.nan # float, instead of None object
        
        if (ip21time_array is None):
            ip21time_array = []
        
        self.ip21time_array = np.array(ip21time_array)
        
        # Attention: do not include http:// in the server, only the server name
        # (what appears after http://)
        self.server = ip21_server
        
        # If no specific data source is provided, use 'localhost'
        self.data_source = data_source
        
        # Create an attribute that checks if another API call is needed:
        self.need_next_call = True
        
        # Check if there is a previous dataset for concatenating with new data:
        self.dataset = previous_df_for_concatenation
        
        # Save credentials:
        self.username = username
        self.password = password
        
        # to check the class attributes, use the __dict__ method. Examples:
        ## object.__dict__ will show all attributes from object
        # You can also manipule this dictionary through vars function:
        # vars(object)['attribute'] = value
                
    # Define the class methods.
    # All methods must take an object from the class (self) as one of the parameters
    

    def convert_window_to_ip21_timescale (self):
        
        start_timestamp = self.start_timestamp 
        stop_timestamp = self.stop_timestamp
        
        # Pick the closest reference timestamp:
        if (start_timestamp >= pd.Timestamp('06-21-2022 0:00:00.001', unit = 'ns')):
            
            reference = pd.Timestamp('06-21-2022 0:00:00.001', unit = 'ns')
            # reference timestamp in IP21 scale:
            reference_ip21 = 1655780400001
        
        elif (start_timestamp >= pd.Timestamp('06-21-2022', unit = 'd')):
            
            reference = pd.Timestamp('06-21-2022', unit = 'd')
            # reference timestamp in IP21 scale:
            reference_ip21 = 1655780400000
        
        elif (start_timestamp >= pd.Timestamp('06-20-2022', unit = 'd')):
            
            reference = pd.Timestamp('06-20-2022', unit = 'd')
            # reference timestamp in IP21 scale:
            reference_ip21 = 1655694000000
        
        elif (start_timestamp >= pd.Timestamp('01-01-2018', unit = 'd')):
            
            reference = pd.Timestamp('01-01-2018', unit = 'd')
            # reference timestamp in IP21 scale:
            reference_ip21 = 1514772000000
        
        elif (start_timestamp >= pd.Timestamp('01-01-2000', unit = 'd')):
            
            reference = pd.Timestamp('01-01-2000', unit = 'd')
            # reference timestamp in IP21 scale:
            reference_ip21 = 946692000000
        
        elif (start_timestamp >= pd.Timestamp('01-01-1970', unit = 'd')):
            
            reference = pd.Timestamp('01-01-1970', unit = 'd')
            # reference timestamp in IP21 scale:
            reference_ip21 = 10800000
        
        else:
            # Use the lowest timestamp:
            reference = pd.Timestamp('01-01-1960', unit = 'd')
            # reference timestamp in IP21 scale:
            reference_ip21 = -315608400000
            
        
        # Convert the start timestamp:
        start_timedelta = start_timestamp - reference
        # apply the delta method to convert to nanoseconds:
        # The .delta attribute was replaced by .value attribute. 
        # Both return the number of nanoseconds as an integer.
        # https://pandas.pydata.org/docs/reference/api/pandas.Timedelta.html
        start_timedelta = start_timedelta.value
        # 1ms = 10^-3 s, 1ns = 10^-9 s, so 1 ns = 1ms/(10^6)
        # Divide by 10^6 to obtain the total of milliseconds:
        start_timedelta = start_timedelta/(10**6)
        # Sum with the reference value in IP21 scale to obtain the converted timestamp:
        start_ip21_scale = reference_ip21 + start_timedelta
        # Guarantee that the number is an integer:
        # np.rint rounds to the nearest integer, whereas int to convert to integer:
        start_ip21_scale = int(np.rint(start_ip21_scale))
        
        # Convert the stop timestamp:
        stop_timedelta = stop_timestamp - reference
        # apply the delta method to convert to nanoseconds:
        stop_timedelta = stop_timedelta.value
        # Divide by 10^6 to obtain the total of milliseconds:
        stop_timedelta = stop_timedelta/(10**6)
        # Sum with the reference value in IP21 scale to obtain the converted timestamp:
        stop_ip21_scale = reference_ip21 + stop_timedelta
        # Guarantee that the number is an integer:
        # np.rint rounds to the nearest integer, whereas int to convert to integer:
        stop_ip21_scale = int(np.rint(stop_ip21_scale))
        
        # Update the attributes:
        self.start_ip21_scale = start_ip21_scale
        self.stop_ip21_scale = stop_ip21_scale
        
        return self
            
        
    def convert_ip21_timescale_array_to_timestamp (self):
        
        # Convert to Pandas series:
        ip21time_window = pd.Series(self.ip21time_array)
        # Guarantee that the series is sorted ascendingly:
        #https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.sort_values.html
        ip21time_window = ip21time_window.sort_values(ascending = True)
        # Get the first ip21 time from the series:
        start_ip21_scale = ip21time_window[0]
        
        # Pick the closest reference timestamp:
        if (start_ip21_scale >= 1655780400001):
            
            reference = pd.Timestamp('06-21-2022 0:00:00.001', unit = 'ns')
            # reference timestamp in IP21 scale:
            reference_ip21 = 1655780400001
        
        elif (start_ip21_scale >= 1655780400000):
            
            reference = pd.Timestamp('06-21-2022', unit = 'd')
            # reference timestamp in IP21 scale:
            reference_ip21 = 1655780400000
        
        elif (start_ip21_scale >= 1655694000000):
            
            reference = pd.Timestamp('06-20-2022', unit = 'd')
            # reference timestamp in IP21 scale:
            reference_ip21 = 1655694000000
        
        elif (start_ip21_scale >= 1514772000000):
            
            reference = pd.Timestamp('01-01-2018', unit = 'd')
            # reference timestamp in IP21 scale:
            reference_ip21 = 1514772000000
        
        elif (start_ip21_scale >= 946692000000):
            
            reference = pd.Timestamp('01-01-2000', unit = 'd')
            # reference timestamp in IP21 scale:
            reference_ip21 = 946692000000
        
        elif (start_ip21_scale >= 10800000):
            
            reference = pd.Timestamp('01-01-1970', unit = 'd')
            # reference timestamp in IP21 scale:
            reference_ip21 = 10800000
        
        else:
            # Use the lowest timestamp:
            reference = pd.Timestamp('01-01-1960', unit = 'd')
            # reference timestamp in IP21 scale:
            reference_ip21 = -315608400000
        
        # Get the IP21 timedelta series:
        ip21time_timedeltas = ip21time_window - reference_ip21
        
        # Start a list for the new timestamps:
        new_timestamps = []
        
        # Now, loop through each element from the series ip21time_timedeltas:
        for ip21time_timedelta in ip21time_timedeltas:
            
            # Create a pandas timedelta object, in ms:
            timedelta_obj = pd.Timedelta(ip21time_timedelta, 'ms')
            # Sum this timedelta to reference to obtain the new timestamp:
            new_timestamp = reference + timedelta_obj
            # Append to the list of new_timestamps:
            new_timestamps.append(new_timestamp)
        
        # Now, convert the list to Pandas series:
        timestamp_series = pd.Series(new_timestamps)
        # Rename this series:
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.rename.html
        timestamp_series = timestamp_series.rename("timestamps")
        
        # Save it as an attribute and return the object:
        self.timestamp_series = timestamp_series
        
        return self
        
    
    def set_extracted_time_window (self, start_timedelta_unit = 'day', stop_timedelta_unit = 'day'):
    
        from datetime import datetime, timedelta

        # start_time: dictionary containing start timestamp information.
        # stop_time: dictionary containing stop timestamp information.

        # Alternatively: start_time = 'today', 'now', start_time = 'yesterday', start_time = -10 for 10
        # days before, start_time = -X for - X days before. Units for offsets will be always in days, unless
        # you modify the parameters start_timedelta_unit and stop_timedelta_unit.
        # For the timedelta unit, set 'day' or 'd' for subtracting values in days,'hour' or 'h',
        # 'minute' or 'm' for minutes, 'second' or 's' for seconds, 'millisecond' or 'ms' for milliseconds.
        # Put the "-" signal, or the time will be interpreted as a future day from today.
        # Analogously for stop_time.
        # Both dictionaries must contain only float values (for 'year', 'day' and 'month'
        # are integers, naturally).

        ## WARNING: The keys must be always be the same, only change the numeric values.
        ## The keys must be: 'year', 'month', 'day', 'hour', 'minute', and 'second'
        
        start_time = self.start_timestamp
        stop_time = self.stop_timestamp
                
        now = datetime.now()
        today = pd.Timestamp(now, unit = 'ns')

        
        if (type (start_time) == dict):

            # Retrieve information from the dictionary:  
            # START timestamp information:
            START_YEAR = start_time['year']
            START_MONTH = start_time['month']
            START_DAY = start_time['day']
            START_HOUR = start_time['hour']
            START_MINUTE = start_time['minute']
            START_SECOND = start_time['second']

            # Create datetime objects from the input information 
            # START_DATETIME: this is the first moment of the database that will be queried.
            START_DATETIME = datetime(year = START_YEAR, month = START_MONTH, day = START_DAY, hour = START_HOUR, minute = START_MINUTE, second = START_SECOND)

            # convert the datetimes to Pandas timestamps, more powerful and compatible with other 
            # Pandas functions, classes and methods. Specify unit = 'ns' (nanoseconds) to guarantee 
            # the resolution
            START_TIMESTAMP = pd.Timestamp(START_DATETIME, unit = 'ns')

        elif (type (start_time) == str):

            if ((start_time == "today") | (start_time == "now")):

                START_TIMESTAMP = today

            elif (start_time == "yesterday"):

                delta_t = pd.Timedelta(1, 'd')
                START_TIMESTAMP = today - delta_t

        elif  ((type (start_time) == float) | (type (start_time) == int)):

                if ((start_timedelta_unit == 'day') | (start_timedelta_unit == 'd')):

                    UNIT = 'd'

                elif ((start_timedelta_unit == 'hour') | (start_timedelta_unit == 'h')):

                    UNIT = 'h'

                elif ((start_timedelta_unit == 'minute') | (start_timedelta_unit == 'm')):

                    UNIT = 'm'

                elif ((start_timedelta_unit == 'second') | (start_timedelta_unit == 's')):

                    UNIT = 's'

                elif ((start_timedelta_unit == 'millisecond') | (start_timedelta_unit == 'ms')):

                    UNIT = 'ms'

                delta_t = pd.Timedelta(start_time, UNIT)
                START_TIMESTAMP = today - delta_t

        if (type (stop_time) == dict):

            # STOP timestamp information:
            STOP_YEAR = stop_time['year']
            STOP_MONTH = stop_time['month']
            STOP_DAY = stop_time['day']
            STOP_HOUR = stop_time['hour']
            STOP_MINUTE = stop_time['minute']
            STOP_SECOND = stop_time['second']

            # STOP_DATETIME: this is the last moment of the database that will be queried.
            STOP_DATETIME = datetime(year = STOP_YEAR, month = STOP_MONTH, day = STOP_DAY, hour = STOP_HOUR, minute = STOP_MINUTE, second = STOP_SECOND)
            STOP_TIMESTAMP = pd.Timestamp(STOP_DATETIME, unit = 'ns')
        
        elif (type (stop_time) == str):

            now = datetime.now()
            today = pd.Timestamp(now, unit = 'ns')

            if ((stop_time == "today") | (stop_time == "now")):

                STOP_TIMESTAMP = today

            elif (stop_time == "yesterday"):

                delta_t = pd.Timedelta(1, 'd')
                STOP_TIMESTAMP = today - delta_t

        elif  ((type (stop_time) == float) | (type (stop_time) == int)):

                if ((stop_timedelta_unit == 'day') | (stop_timedelta_unit == 'd')):

                    UNIT = 'd'

                elif ((stop_timedelta_unit == 'hour') | (stop_timedelta_unit == 'h')):

                    UNIT = 'h'

                elif ((stop_timedelta_unit == 'minute') | (stop_timedelta_unit == 'm')):

                    UNIT = 'm'

                elif ((stop_timedelta_unit == 'second') | (stop_timedelta_unit == 's')):

                    UNIT = 's'

                elif ((stop_timedelta_unit == 'millisecond') | (stop_timedelta_unit == 'ms')):

                    UNIT = 'ms'

                delta_t = pd.Timedelta(stop_time, UNIT)
                STOP_TIMESTAMP = today - delta_t

        self.start_timestamp = START_TIMESTAMP
        self.stop_timestamp = STOP_TIMESTAMP
        
        # Convert to the the IP21 scale:
        self = self.convert_window_to_ip21_timescale()
        # Check if the conversion was performed correctly:
        print(f"Extracting entries from {self.start_timestamp} to {self.stop_timestamp}.")
        print(f"Start to Stop timestamp interval in IP21 timescale = ({self.start_ip21_scale}, {self.stop_ip21_scale})\n")
        
        return self
    
    
    def get_rest_api_url (self):
        
        server = self.server
        tag = self.tag
        data_source = self.data_source
        start_ip21_scale = self.start_ip21_scale
        stop_ip21_scale = self.stop_ip21_scale
        
        # URL Encodings:
        # https://docs.osisoft.com/bundle/pi-web-api-reference/page/help/topics/url-encoding.html
        
        # Check if the last character of the server is /:
        if (server[-1] != "/"):
            # Concatenate the character:
            server = server + "/"
        
        url = "http://" + server
        # To access the API Portal:
        # processdata_portal_suffix = "processdata/samples/sample_home.html/"
        # api_portal_url = url + processdata_portal_suffix
        query_prefix = "ProcessData/AtProcessDataREST.dll/History"
        # For the full URL:
        # ? indicates a query
        url = url + query_prefix
        
        # URL-encoded URL:
        query = f"""%3CQ%20f=%22d%22%20allQuotes=%221%22%3E%3CTag%3E%3CN%3E%3C![CDATA[{tag}]]%3E%3C/N%3E%3CD%3E%3C![CDATA[{data_source}]]%3E%3C/D%3E%3CF%3E%3C![CDATA[VAL]]%3E%3C/F%3E%3CHF%3E0%3C/HF%3E%3CSt%3E{start_ip21_scale}%3C/St%3E%3CEt%3E{stop_ip21_scale}%3C/Et%3E%3CRT%3E0%3C/RT%3E%3CX%3E100000%3C/X%3E%3CO%3E1%3C/O%3E%3C/Tag%3E%3C/Q%3E"""
        
        # Not-encoded URL:
        #query = f"""<Q%20f="d"%20allQuotes="1"><Tag><N><![CDATA[{tag}]]></N><D><![CDATA[{data_source}]]></D><F><![CDATA[VAL]]></F><HF>0</HF><St>{start_ip21_scale}</St><Et>{stop_ip21_scale}</Et><RT>0</RT><X>100000</X><O>1</O></Tag></Q>"""
        
        
        # Save the url as an attribute and return it:
        self.url = url
        self.query = query
        
        return self
    
    
    def retrieve_pd_dataframe (self, json_file_path = None):
        
        import os
        import json
        from pandas import json_normalize
        
        json_response = self.json_response
        tag_name = self.actual_tag_name
        start_ip21_scale = self.start_ip21_scale
        stop_ip21_scale = self.stop_ip21_scale
        
        # Retrieve previous dataset in memory:
        previous_df = self.dataset
        
        if (json_file_path is not None):
            try:
                # Extract the file extension
                file_extension = os.path.splitext(json_file_path)[1][1:]
                # os.path.splitext(file_path) is a tuple of strings: the first is the complete file
                # root with no extension; the second is the extension starting with a point: '.txt'
                # When we set os.path.splitext(file_path)[1], we are selecting the second element of
                # the tuple. By selecting os.path.splitext(file_path)[1][1:], we are taking this string
                # from the second character (index 1), eliminating the dot: 'txt'

                if (file_extension == 'json'):

                    json_file = json.load(json_response)

                else:
                    # Open context manager:
                    with open (json_response, 'r') as file:
                        # Read all lines:
                        response = file.readlines()

                    # Use the json.loads method to convert the string to json
                    json_file = json.loads(response)
            
            except:
                pass
        
        else:
            try:
                # It is a string:
                json_file = json.loads(json_response)
            
            except:
                pass
        
        """
        JSON structure obtained from IP21:
        {"data":[{...,"samples":[{"t":TIMESTAMP in IP21 scale,"v": VALUE FOR THAT TIMESTAMP,...},...]}]}
        
        """
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.json_normalize.html#pandas.json_normalize
        # json_record_path (string): manipulate parameter 'record_path' from json_normalize method.
        # Path in each object to list of records. If not passed, data will be assumed to 
        # be an array of records. If a given field from the JSON stores a nested JSON (or a nested
        # dictionary) declare it here to decompose the content of the nested data. e.g. if the field
        # 'books' stores a nested JSON, declare, json_record_path = 'books'

        # json_field_separator = "_" (string). Manipulates the parameter 'sep' from json_normalize method.
        # Nested records will generate names separated by sep. 
        # e.g., for json_field_separator = ".", {‘foo’: {‘bar’: 0}} -> foo.bar.
        # Then, if a given field 'main_field' stores a nested JSON with fields 'field1', 'field2', ...
        # the name of the columns of the dataframe will be formed by concatenating 'main_field', the
        # separator, and the names of the nested fields: 'main_field_field1', 'main_field_field2',...

        # e.g. Suppose a JSON with the following structure: {'name': 'Mary', 'last': 'Shelley',
        # 'books': [{'title': 'Frankestein', 'year': 1818}, {'title': 'Mathilda ', 'year': 1819},{'title': 'The Last Man', 'year': 1826}]},
        # Here, there are nested JSONs in the field 'books'. The fields that are not nested
        # are 'name' and 'last'.
        # Then, json_record_path = 'books'
        # json_metadata_prefix_list = ['name', 'last']
        json_record_path = ['data', 'samples']
        json_field_separator = "_"
        dataset = json_normalize(json_file, record_path = json_record_path, sep = json_field_separator)
        
        if ((dataset is None) | ("er" in dataset.columns) | ("ec" in dataset.columns) | ("es" in dataset.columns) | (len(dataset) == 0)):
            
            print("There is no data available for the defined time window.\n")
            
            # If the attribute is not None, concatenate the dataframes:
            if (previous_df is not None):
                # Concatenate all dataframes (append rows):
                dataset = previous_df
                print("Returning the previous dataset itself.\n")
        
            self.dataset = dataset
            self.need_next_call = False
            # Interrupt the algorithm:
            return self
            
        
        if (('t' not in dataset.columns) & ('v' not in dataset.columns)):
            
            # Lower case column names:
            columns = [c.lower() for c in dataset.columns]
            # Pick only first character (until character of index 1, excluding index 1):
            columns = [c[:1] for c in columns]
            # Make this list the columns names:
            dataset.columns = columns
        
        if (('t' in dataset.columns) & ('v' in dataset.columns)):
            
            # Keep only columns 't' and 'v':
            dataset = dataset[['t', 'v']]
            # Rename these columns:
            dataset.columns = ['timestamp_ip21_scale', tag_name]
        
        else:
            # Substitute only the 1st column name and pick the other columns starting from
            # the second one (index 1)
            columns = ['timestamp_ip21_scale'] + list(dataset.columns)[1:]
        
        # Isolate the time series:
        time_series = dataset['timestamp_ip21_scale']
        # Get the last element (convert to list to access index -1).
        # In Pandas series, we can do [:-1] to get a single-element series:
        last_element = list(time_series)[-1]
        
        if (last_element < stop_ip21_scale):
            
            self.need_next_call = True
            # Update the start timestamp to be the last_element plus 1 unit (1 millisecond):
            self.start_ip21_scale = last_element + 1
        
        else:
            self.need_next_call = False
        
        # Save the timestamps as numpy array in the attribute ip21time_array:
        self.ip21time_array = np.array(dataset['timestamp_ip21_scale'])
        # Convert to timestamp using the conversion method:
        self = self.convert_ip21_timescale_array_to_timestamp()
        # Retrieve the timestamps:
        dataset['timestamp'] = self.timestamp_series
        
        # Select only these columns:
        dataset = dataset[['timestamp', tag_name]]
        
        
        # If the attribute is not None, concatenate the dataframes:
        if (previous_df is not None):
            
            # Compare the last timestamp from dataset and previous_df
            last_timestamp = list(dataset['timestamp'])[-1]
            previous_last_timestamp = list(previous_df['timestamp'])[-1]
            
            if (last_timestamp == previous_last_timestamp):
                
                # We already reached the end of the database. It actually never reaches the stop timestamp.
                print(f"The last timestamp registered in the database is: {last_timestamp}\n")
                # Pick the previous dataframe, which is already concatenated with dfs from previous calls
                dataset = previous_df
                # Now, finish the process:
                self.need_next_call = False
            
            else:
                # Concatenate all dataframes (append rows):
                dataset = pd.concat([previous_df, dataset], axis = 0, join = "inner")
                # Reset previous indices so that numeration is continuous:
                dataset = dataset.reset_index(drop = True)

        # Finally, save the concatenated dataset as dataset attribute and return the object:
        self.dataset = dataset
        
        return self
    

    def fetch_database (self, request_type = 'get'):
        
        import requests
        # IP21 uses the NTLM authentication protocol
        from requests_ntlm import HttpNtlmAuth
       
        url = self.url
        query = self.query
        username = self.username
        password = self.password
        
        # Create the NTLM Authorization object:
        AUTH = HttpNtlmAuth(username, password)
        
        # IP21 requires the 'post' protocol
        
        if (request_type == 'post'):
            
            json_response = requests.post(url, auth = AUTH, data = query)
        
        else: #get
            
            url = url + "?" + query
            json_response = requests.get(url, auth = AUTH)
        
        json_response = json_response.text
        
        self.json_response = json_response
        
        return self


class SQLServerConnection:
    """
    Class for extracting data from a SQL Server instance.
    def __init__ (self, server, 
                  database,
                  username = '', 
                  password = '',
                  system = 'windows'):
    
    : param: system = 'windows', 'macos' or 'linux'

        If the user passes the argument, use them. Otherwise, use the standard values.
        Set the class objects' attributes.
        Suppose the object is named assistant. We can access the attribute as:
        assistant.assistant_startup, for instance.
        So, we can save the variables as objects' attributes.

    INSTALL ODBC DRIVER IF USING MACOS OR LINUX (Windows already has it):
    - MacOS Installation: https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver16
    - Linux Installation: https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=alpine18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline
    """

    # Initialize instance attributes.
    # define the Class constructor, i.e., how are its objects:

    def __init__ (self, server, 
                  database,
                  username = '', 
                  password = '',
                  system = 'windows'):

        
        import pyodbc
        import pandas as pd
        # Some other example server values are
        # server = 'localhost\sqlexpress' # for a named instance
        # server = 'myserver,port' # to specify an alternate port

        if ((username is None)|(username == '')):
            # Ask the user to provide the credentials:
            username = input(f"Enter your username for accessing the SQL database {database} from server {server} here (in the right).")
            print("\n") # line break
        
        if ((password is None)|(password == '')):
            from getpass import getpass
            password = getpass(f"Enter your password (Secret key) for accessing the SQL database {database} from server {server} here (in the right).")
        
        
        if (system == 'windows'):
            cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        
        else:
            cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password + 'Encrypt=no;TrustServerCertificate=yes')
            # https://stackoverflow.com/questions/71587239/operationalerror-when-trying-to-connect-to-sql-server-database-using-pyodbc/71588236#71588236
        
        cursor = cnxn.cursor()
        
        self.cnxn = cnxn
        self.cursor = cursor
        self.query_counter = 0
        

    def get_db_schema (self, show_schema = True, export_csv = False, saving_directory_path = "db_schema.csv"):
            
        import pandas as pd
        query = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'"
            
        schema_df = pd.read_sql(query, self.cnxn)
        
        if (show_schema):
            print("Database schema:")
            print(f"There are {len(schema_df)} tables registered in the database.\n")
            try:
                from IPython.display import display
                display(schema_df)
                
            except:
                print(schema_df)
                
        self.schema_df = schema_df

        if (export_csv):
            if ((saving_directory_path is None)|(saving_directory_path == '')):
                saving_directory_path = "db_schema.csv"
            
            schema_df.to_csv(saving_directory_path)
            
        return self
        
        
    def run_sql_query (self, query, show_table = True, export_csv = False, saving_directory_path = ""):

        # show_table: keep as True to print the queried table, set False to hide it.
        # export_csv: set True to export the queried table as CSV file, or set False not to export it.
        # saving_directory_path: full path containing directories and table name, with .csv extension, used when
        # export_csv = True

        # SQL SERVER INNER JOIN:
        """
        https://www.sqlservertutorial.net/sql-server-basics/sql-server-inner-join/

        FROM table1 d
        INNER JOIN table2 t
        ON d.key1 = t.key2
        """
        
        # SQL SERVER UNION STATEMENT (vertical concatenation/append):
        """
        https://www.w3schools.com/sql/sql_union.asp

        FROM table1 d
        INNER JOIN table2 t
        ON d.key1 = t.key2
        UNION
        SELECT ValueTime as timestamp, TagName AS tag
        FROM LatestIP21TagDataNumeric
        WHERE TagName = 'TAGABC' OR TagName = 'TAGABD' OR TagName = 'TAGABE' 
        ORDER BY timestamp ASC;
        -- Notice that ORDER BY appears at the end of the query, after all joins and unions
        """

        # SQL SERVER TOP (EQUIVALENT TO LIMIT):
        """
        https://www.w3schools.com/sqL/sql_top.asp
        
        SELECT TOP 100 *
        FROM table;
        """
        
        # SQL SERVER WHERE STATEMENT (FILTER):
        """
        https://learn.microsoft.com/en-us/sql/t-sql/queries/where-transact-sql?view=sql-server-ver16

        WHERE column1 = 'val1' OR column1 = 'val2'
        """
        
        # SQL SERVER CASE STATEMENT (IF ELSE):
        """
        https://www.w3schools.com/sql/sql_case.asp

        CASE
            WHEN t.TagName = 'CODEXXX' THEN 'Variable X'
        ELSE ''
        END AS variable,
        """

        import pandas as pd

        query_counter = self.query_counter
            
        df = pd.read_sql(query, self.cnxn)

        if (show_table):   
            print("Returned table:\n")
            try:
                from IPython.display import display
                display(df)
                
            except:
                print(df)

        # Vars function allows accessing the attributes from a class as a key from a dictionary.
        # vars(object) is a dictionary where each key is one attribute from the object. A new attribute may be
        # created by setting a value for a new key;
        # Then, an attribute name may be created as a string:
        vars(self)[f"df_query{query_counter}"] = df

        if (export_csv):
            if ((saving_directory_path is None)|(saving_directory_path == '')):
                saving_directory_path = f"table{query_counter}.csv"
            
            df.to_csv(saving_directory_path)
        
        # Update counter:
        self.query_counter = query_counter + 1

        return df
        
        
    def get_full_table (self, table, show_table = True, export_csv = False, saving_directory_path = ""):
            
        import pandas as pd
        
        query_counter = self.query_counter

        query = "SELECT * FROM " + str(table)
            
        df_table = pd.read_sql(query, self.cnxn)
        
        if (show_table): 
            print("Returned table:\n")
            try:
                from IPython.display import display
                display(df_table)
                
            except:
                print(df_table)
        
        # Vars function allows accessing the attributes from a class as a key from a dictionary.
        # vars(object) is a dictionary where each key is one attribute from the object. A new attribute may be
        # created by setting a value for a new key;
        # Then, an attribute name may be created as a string:
        vars(self)[f"df_table{query_counter}"] = df_table

        if (export_csv):
            if ((saving_directory_path is None)|(saving_directory_path == '')):
                saving_directory_path = f"table{query_counter}.csv"
            
            df_table.to_csv(saving_directory_path)
         
        # Update counter:
        self.query_counter = query_counter + 1    
            
        return df_table
    
    
    def query_specific_tag_ip21sqlserver (self, tag, variable_name = None, show_table = True, export_csv = False, saving_directory_path = ""):
        """ : param: tag: string with tag as registered in IP21. e.g. tag = 'ABC00AA101-01'.
        
            : param: variable_name: string containing a more readable name for the tag, that will be also shown.
            e.g. variable_name = 'Temperature in C'
        """
        
        import pandas as pd
        # https://www.sqlservertutorial.net/sql-server-basics/sql-server-inner-join/
        # https://www.w3schools.com/sqL/sql_top.asp
        # https://learn.microsoft.com/en-us/sql/t-sql/queries/where-transact-sql?view=sql-server-ver16
        # https://www.w3schools.com/sql/sql_case.asp
        # https://www.w3schools.com/sql/sql_union.asp
        
        if (variable_name is None):
            #Repeat the tag
            variable_name = tag

        query = f"""SELECT d.ValueTime AS timestamp, t.TagName AS tag,
                    CASE
                        WHEN t.TagName = '{tag}' THEN '{variable_name}'
                        ELSE ''
                    END AS variable,
                    d.Value AS value
                    FROM IP21DataNumeric d
                    INNER JOIN IP21PublishConfig t
                    ON d.TagConfigID = t.ID
                    WHERE t.TagName = '{tag}'
                    UNION
                    SELECT ValueTime as timestamp, TagName AS tag, 
                    CASE
                        WHEN TagName = '{tag}' THEN '{variable_name}'
                        ELSE ''
                    END AS variable,
                    Value AS value
                    FROM LatestIP21TagDataNumeric
                    WHERE TagName = '{tag}'
                    ORDER BY timestamp ASC;
                """
        
        tag_df = self.run_sql_query(query = query, show_table = show_table, export_csv = export_csv, saving_directory_path = saving_directory_path)
        
            
        return tag_df


class GCPBigQueryConnection:
    """
    Class for accessing Google Cloud Platform (GCP) BigQuery data.

    : param: system = 'windows', 'macos' or 'linux'

        If the user passes the argument, use them. Otherwise, use the standard values.
        Set the class objects' attributes.
        Suppose the object is named assistant. We can access the attribute as:
        assistant.assistant_startup, for instance.
        So, we can save the variables as objects' attributes.
        
    : param: authetication_method = 'manual' for GCP standard manual authentication on browser
     
    MANUAL AUTHENTICATION INSTRUCTION
        
        - BEFORE INSTATIATING THE CLASS, FOLLOW THESE GUIDELINES!
        
        1. Copy and run the following line in a notebook cell. Do not add quotes.
        The "!" sign must be added to indicate the use of a command line software:


                            !gcloud auth application-default login
        

        2. Also, you can run the SQL query on GCP console and, when the query results appear, click on EXPLORE DATA - Explore with Python notebook.
        It will launch a Google Colab Python notebook that you may run for data exploring, manipulation and exporting.

        2.1. To export data, you expand the hamburger icon on the left side of the Google Colab, click on Files, and then select an exported CSV or other files. Finally, click on the ellipsis (3 dots) and select Download to obtain it.
        
        
    : param: authetication_method = 'vault' for Vault automatic authentication, dependent on corporate
        cibersecurity and data asset.
    : params: vault_secret_path = '', app_role = '', app_secret = '' are the parameters for vault authorization
        
        
    Install Google Cloud Software Development Kit (SDK) before running
            
    General Instructions for Installation: https://cloud.google.com/sdk/docs/install-sdk?hl=pt-br#installing_the_latest_version
    Instructions for Windows: https://cloud.google.com/sdk/docs/install-sdk?hl=pt-br#windows
    Instructions for Mac OS: https://cloud.google.com/sdk/docs/install-sdk?hl=pt-br#mac
    Instructions for Linux: https://cloud.google.com/sdk/docs/install-sdk?hl=pt-br#linux
    
    From: https://stackoverflow.com/questions/39419754/downloading-and-importing-google-cloud-python
    First, make sure you have installed gcloud on your system then run the commands like this:

    First: gcloud components update in your terminal.
    then: pip install google-cloud
    And for the import error:
    Adding "--ignore-installed" to pip command may work.
    This might be a bug in pip - see this page for more details: https://github.com/pypa/pip/issues/2751

    This pipeline may be blocked also due to security configurations, and may fail on some Virtual Private Networks (VPNs).
    - Try to run this pipeline outside of the VPN in case it fails
    """
    
    # Initialize instance attributes.
    # define the Class constructor, i.e., how are its objects:

    def __init__ (self, project = '', dataset = '', authentication_method = 'manual',
                  vault_secret_path = '', app_role = '', app_secret = ''):
        
        
        
        from google.cloud import bigquery
        import pandas as pd
        
        
        if ((project is None)|(project == '')):
            # Ask the user to provide the credentials:
            # This is the name that appears on the right-hand menu from GCP console Big Query page, 
            # (https://console.cloud.google.com/bigquery) called Explorer
            # that contains a group of datasets. E.g.: location360-datasets; bcs-csw-core, etc
            # The individual datasets are revealed after expanding the project name by clicking on the arrow.
            print("\n")
            self.project = input(f"Enter the name of the project registered on Google Cloud Platform (GCP).\n")
        
        if ((dataset is None)|(dataset == '')):
            # Ask the user to provide the credentials:
            # E.g.: core
            print("\n")
            self.dataset = input(f"Enter the name of the dataset from project {self.project} registered on GCP, containing the tables that will be queried.\n")

        self.query_counter = 0
        
        if (authentication_method == 'manual'):
            self.client = self.connect_to_gcp_project()
        
        elif (authentication_method == 'vault'):
            self.client, self.storage_client = self.connect_to_gcp_project(vault_secret_path = vault_secret_path, app_role = app_role, app_secret = app_secret)


    def connect_to_gcp_project (self):
        
        start_msg = """
        This function allows the manual autentication: if the command 

            !gcloud auth application-default login

        was run for GCP authentication, this protocol will allow the creation of the client.
        It is not designed to be used with a corporate protocol for fully automatic pipelines, such as Vault access. For that, the Cybersecurity or Data Asset team must be contacted.
            """
        
        print(start_msg)
        
        # Some other example server values are
        # server = 'localhost\sqlexpress' # for a named instance
        # server = 'myserver,port' # to specify an alternate port
        
        # subprocess module allows running shell commands. Each portion from a Bash script is declared as an element 
        # from a list of strings. Outputs are captured as a list of strings as well.        
        # Example:
        """
        with Popen(["ls"], stdout=PIPE) as proc:
        out = proc.readlines()
        print(out)
        
        output: ['some_file.txt','some_other_file.txt']
        # Notice that a Python variable of string type may be included to the list for generating dynamic execution of commands.
        """

        """
        Example 2 command: python -m pip show pandas
        from subprocess import Popen, PIPE, TimeoutExpired
        proc = Popen(["python", "-m", "pip", "show", "pandas"], stdout = PIPE, stderr = PIPE)
        try:
            output, error = proc.communicate(timeout = 15)
            print(output)
        except:
                    # General exception
            output, error = proc.communicate()
            print(f"Process with output: {output}, error: {error}.\n")

        output: b'Name: pandas\r\nVersion: 2.0.3\r\nSummary: Powerful data structures for data analysis, time series, and statistics\r\nHome-page: \r\nAuthor: \r\nAuthor-email: The Pandas Development Team <pandas-dev@python.org>\r\nLicense: BSD 3-Clause License\r\n        \r\n        Copyright (c) 2008-2011, AQR Capital Management, LLC, Lambda Foundry, Inc. and PyData Development Team\r\n        All rights reserved.\r\n        \r\n        Copyright (c) 2011-2023, Open source contributors.\r\n        \r\n        Redistribution and use in source and binary forms, with or without\r\n        modification, are permitted provided that the following conditions are met:\r\n        \r\n        * Redistributions of source code must retain the above copyright notice, this\r\n          list of conditions and the following disclaimer.\r\n        \r\n        * Redistributions in binary form must reproduce the above copyright notice,\r\n          this list of conditions and the following disclaimer in the documentation\r\n          and/or other materials provided with the distribution.\r\n        \r\n        * Neither the name of the copyright holder nor the names of its\r\n          contributors may be used to endorse or promote products derived from\r\n          this software without specific prior written permission.\r\n        \r\n        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"\r\n        AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE\r\n        IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE\r\n        DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE\r\n        FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL\r\n        DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR\r\n        SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER\r\n        CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,\r\n        OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE\r\n        OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\r\n        \r\nLocation: c:\\users\\gnklm\\appdata\\local\\anaconda3\\lib\\site-packages\r\nRequires: numpy, python-dateutil, pytz, tzdata\r\nRequired-by: cmdstanpy, datashader, holoviews, hvplot, prophet, seaborn, shap, statsmodels, xarray\r\n'
        """

        from subprocess import Popen, PIPE, TimeoutExpired

        # Start a long running process using subprocess.Popen()
        # Command to run:
        """!gcloud auth application-default login"""

        try:
            proc = Popen(["gcloud", "auth", "application-default", "login"], stdout = PIPE, stderr = PIPE)

            """
            You will use the subprocess.communicate() method to wait for the command to finish running for up to 15 seconds. 
            The process will then timeout and it will return an Exception: i.e. error detected during execution, which will be caught 
            and the process will be cleaned up by proc.kill(). 
            """

            # Use subprocess.communicate() to create a timeout 
            try:
                output, error = proc.communicate(timeout = 15)
                # Simply remove timeout argument if process is not supposed to finish after a given time.

            except TimeoutExpired:

                # Cleanup the process if it takes longer than the timeout
                proc.kill()

                # Read standard out and standard error streams and print
                output, error = proc.communicate()
                print(f"Process timed out with output: {output}, error: {error}.")

            except:
                # General exception
                proc.kill()
                output, error = proc.communicate()
                print(f"Process of Google Cloud Mount with output: {output}, error: {error}.\n")

                warning = """
                Install Google Cloud Software Development Kit (SDK) before running this function.

                General Instructions for Installation: https://cloud.google.com/sdk/docs/install-sdk?hl=pt-br#installing_the_latest_version
                Instructions for Windows: https://cloud.google.com/sdk/docs/install-sdk?hl=pt-br#windows
                Instructions for Mac OS: https://cloud.google.com/sdk/docs/install-sdk?hl=pt-br#mac
                Instructions for Linux: https://cloud.google.com/sdk/docs/install-sdk?hl=pt-br#linux
                """

                print(warning)

            """try:
                from IPython.display import display 
                # from IPython.display import display, display_html
                out = list(proc._fileobj2output.keys())
                out1, out2 = out[1], out[0]
                display(proc._fileobj2output[out1][0])
                print("\n")
                # display(proc._fileobj2output[out2][0])
                # display_html(proc._fileobj2output[out2][0])

            except:
                pass"""
        
        except:
            pass
        
        
        from google.cloud import bigquery

        client = bigquery.Client(project = self.project)

        return client


    def get_vault_secret (self, vault_secret_path: str, app_role: str, app_secret: str):
               
        import base64
        import json
        import hvac
        import os

        from google.oauth2 import service_account
        from google.cloud import bigquery, bigquery_storage
        
        """
        Get the vault secret in dictionary
        More detail about hvac: https://hvac.readthedocs.io/en/stable/overview.html
        
        """
        vault_url = 'https://vault.agro.services'
        vault_client = hvac.Client(url = vault_url)
        
        vault_client.auth.approle.login(app_role, app_secret)

        vault_path = vault_secret_path
        vault_secret = vault_client.read(vault_path)
        
        return vault_secret['data']['data']

 
    def get_vault_credentials (self, vault_secret_path: str, app_role: str, app_secret: str):
        
        import base64
        import json
        import hvac
        import os

        from google.oauth2 import service_account
        from google.cloud import bigquery, bigquery_storage
        
        """
        Bigquery project credential with service account
        Return credential of a service account using app role and app secret
        
        """
        vault_secret = self.get_vault_secret(vault_secret_path, app_role, app_secret)

        if 'data' in vault_secret and type(vault_secret['data']) == str:
            service_account_creds = json.loads(base64.b64decode(vault_secret['data']))
        else:
            # in case credentials are saved directly as json object in vault (not encoded) you can get it directly
            service_account_creds = json.loads(base64.b64decode(vault_secret))
        bq_credentials = service_account.Credentials.from_service_account_info(service_account_creds)

        return bq_credentials


    def vault_access_gcp (self, vault_secret_path = '', app_role = '', app_secret = ''):     
        
        import base64
        import json
        import hvac
        import os

        from google.oauth2 import service_account
        from google.cloud import bigquery, bigquery_storage

        
        if ((vault_secret_path is None)|(vault_secret_path == '')):
            vault_secret_path = input(f"Enter Vault Secret Path for accessing CSW.")
            print("\n") # line break
        
        if ((app_role is None)|(app_role == '')):
            app_role = input(f"Enter App Role for getting the Vault client.")
            print("\n") # line break

        if ((app_secret is None)|(app_secret == '')):
            from getpass import getpass
            vault_secret_path = getpass(f"Enter App Secret for getting the Vault client.")
            print("\n") # line break

        self.credentials = self.get_vault_credentials(vault_secret_path = vault_secret_path, app_role = app_role, app_secret = app_secret)

        client = bigquery.Client(credentials = self.credentials, project = self.project)
        storage_client = bigquery_storage.BigQueryReadClient(credentials = self.credentials)

        return client, storage_client

 
    def run_sql_query (self, query, show_table = True, export_csv = False, saving_directory_path = ""):

        # show_table: keep as True to print the queried table, set False to hide it.
        # export_csv: set True to export the queried table as CSV file, or set False not to export it.
        # saving_directory_path: full path containing directories and table name, with .csv extension, used when
        # export_csv = True

        import pandas as pd

        query_counter = self.query_counter

        client = self.client
        job = client.query(query)
        df = job.to_dataframe()

        if (show_table):   
            print("Returned table:\n")
            try:
                from IPython.display import display
                display(df)
                
            except:
                print(df)

        # Vars function allows accessing the attributes from a class as a key from a dictionary.
        # vars(object) is a dictionary where each key is one attribute from the object. A new attribute may be
        # created by setting a value for a new key;
        # Then, an attribute name may be created as a string:
        vars(self)[f"df_query{query_counter}"] = df

        if (export_csv):
            if ((saving_directory_path is None)|(saving_directory_path == '')):
                saving_directory_path = f"table{query_counter}.csv"
            
            df.to_csv(saving_directory_path)
        
        # Update counter:
        self.query_counter = query_counter + 1

        return df
        
        
    def get_full_table (self, table, show_table = True, export_csv = False, saving_directory_path = ""):
        
        # show_table: keep as True to print the queried table, set False to hide it.
        # export_csv: set True to export the queried table as CSV file, or set False not to export it.
        # saving_directory_path: full path containing directories and table name, with .csv extension, used when
        # export_csv = True
        
        import pandas as pd

        table_name = f"""`{self.project}.{self.dataset}.{str(table)}`"""
        
        query_counter = self.query_counter

        query = "SELECT * FROM " + table_name
            
        client = self.client
        job = client.query(query)
        df_table = job.to_dataframe()
        
        if (show_table): 
            print("Returned table:\n")
            try:
                from IPython.display import display
                display(df_table)
                
            except:
                print(df_table)
        
        # Vars function allows accessing the attributes from a class as a key from a dictionary.
        # vars(object) is a dictionary where each key is one attribute from the object. A new attribute may be
        # created by setting a value for a new key;
        # Then, an attribute name may be created as a string:
        vars(self)[f"df_table{query_counter}"] = df_table

        if (export_csv):
            if ((saving_directory_path is None)|(saving_directory_path == '')):
                saving_directory_path = f"table{query_counter}.csv"
            
            df_table.to_csv(saving_directory_path)
         
        # Update counter:
        self.query_counter = query_counter + 1    
            
        return df_table
    

    def write_data_on_bigquery_table (self, table, df):
        
        # df: Pandas dataframe to be written on BigQuery table
        # table: string with table name
        import pandas as pd

        client = self.client
        table_ref = client.dataset(self.dataset).table(str(table))
        table = client.get_table(table_ref)

        errors = client.insert_rows_from_dataframe(table, df)

        if errors != [[]]: 
            raise RuntimeError('Error in writing to BigQuery: {}'.format(errors))

        else:
            
            print(f"Dataframe written on Big Query {table} table from dataset {self.project}.{self.dataset}.\n")
            
            return self


    def delete_specific_values_from_column_on_table (self, table, column, values_to_delete, show_table = True, export_csv = False, saving_directory_path = ""):

        # show_table: keep as True to print the queried table, set False to hide it.
        # export_csv: set True to export the queried table as CSV file, or set False not to export it.
        # saving_directory_path: full path containing directories and table name, with .csv extension, used when
        # export_csv = True
        
        # column is the column name on a given BigQuery table (a string).
        # values_to_delete is a single value (numeric or string) or an iterable containing a set
        # of values to be deleted.

        import pandas as pd

        if (type(values_to_delete) == str):
            # put inside list:
            values_to_delete = [values_to_delete]
        
        else:
            try:
                values_to_delete = list(values_to_delete)
            
            except:
                # It is not an iterable (it is a value):
                values_to_delete = [values_to_delete]

        # pick 1st element and remove it from list
        val0 = values_to_delete.pop(0)

        if (type(val0) == str):
            
            delete_query = f"""
                                DELETE 
                                    FROM `{self.project}.{self.dataset}.{str(table)}`
                                    WHERE {column} = '{val0}' """
        
        else:
            delete_query = f"""
                                DELETE 
                                    FROM `{self.project}.{self.dataset}.{str(table)}`
                                    WHERE {column} = {val0} """

        # Now, loop through the remaining list (if there is a remaining one) to update query.
        # If list is empty, the loop does not run
        for val in values_to_delete:
            if (type(val) == str):
                delete_query = delete_query + f"""OR {column} = '{val}' """
                
            else:
                delete_query = delete_query + f"""OR {column} = {val} """

        client = self.client
        query_counter = self.query_counter

        table_ref = client.dataset(self.dataset).table(str(table))
        table = client.get_table(table_ref)

        table.streaming_buffer

        if table.streaming_buffer is None:
            job = client.query(delete_query)
            job.result()
        else:
            raise RuntimeError("Table contains data in a streaming buffer, which cannot be updated or deleted. Please perform this action when the streaming buffer is empty (may take up to 90 minutes from last data insertion).")

        df_table = job.to_dataframe()
        
        if (show_table): 
            print("Returned table with deleted data:\n")
            try:
                from IPython.display import display
                display(df_table)
                
            except:
                print(df_table)
        
        # Vars function allows accessing the attributes from a class as a key from a dictionary.
        # vars(object) is a dictionary where each key is one attribute from the object. A new attribute may be
        # created by setting a value for a new key;
        # Then, an attribute name may be created as a string:
        vars(self)[f"df_table{query_counter}"] = df_table

        if (export_csv):
            if ((saving_directory_path is None)|(saving_directory_path == '')):
                saving_directory_path = f"table{query_counter}.csv"
            
            df_table.to_csv(saving_directory_path)
         
        # Update counter:
        self.query_counter = query_counter + 1    
            
        return df_table    


    def update_specific_value_from_column_on_table (self, table, column, old_value, updated_value, show_table = True, export_csv = False, saving_directory_path = ""):

        # show_table: keep as True to print the queried table, set False to hide it.
        # export_csv: set True to export the queried table as CSV file, or set False not to export it.
        # saving_directory_path: full path containing directories and table name, with .csv extension, used when
        # export_csv = True
        
        # column is the column name on a given BigQuery table (a string).
        # old_value: value that must be replaced
        # updated_value: new value to be added.

        import pandas as pd
            
        if ((type(old_value) == str)|(type(updated_value) == str)):
                update_query = f"""
                    UPDATE `{self.project}.{self.dataset}.{str(table)}`
                        SET `{column}` = '{updated_value}'
                        WHERE `{column}` = '{old_value}'
                        """
            
        else:
                update_query = f"""
                    UPDATE `{self.project}.{self.dataset}.{str(table)}`
                        SET `{column}` = {updated_value}
                        WHERE `{column}` = {old_value}
                        """
            
        client = self.client
        query_counter = self.query_counter

        table_ref = client.dataset(self.dataset).table(str(table))
        table = client.get_table(table_ref)

        table.streaming_buffer

        if table.streaming_buffer is None:
            job = client.query(update_query)
            job.result()
        else:
            raise RuntimeError("Table contains data in a streaming buffer, which cannot be updated or deleted. Please perform this action when the streaming buffer is empty (may take up to 90 minutes from last data insertion).")

        df_table = job.to_dataframe()
        
        if (show_table): 
            print("Returned table with updated data:\n")
            try:
                from IPython.display import display
                display(df_table)
                
            except:
                print(df_table)
        
        # Vars function allows accessing the attributes from a class as a key from a dictionary.
        # vars(object) is a dictionary where each key is one attribute from the object. A new attribute may be
        # created by setting a value for a new key;
        # Then, an attribute name may be created as a string:
        vars(self)[f"df_table{query_counter}"] = df_table

        if (export_csv):
            if ((saving_directory_path is None)|(saving_directory_path == '')):
                saving_directory_path = f"table{query_counter}.csv"
            
            df_table.to_csv(saving_directory_path)
         
        # Update counter:
        self.query_counter = query_counter + 1    
            
        return df_table


    def update_entire_column_from_table (self, table, column, updated_value, show_table = True, export_csv = False, saving_directory_path = ""):

        # show_table: keep as True to print the queried table, set False to hide it.
        # export_csv: set True to export the queried table as CSV file, or set False not to export it.
        # saving_directory_path: full path containing directories and table name, with .csv extension, used when
        # export_csv = True
        
        # column is the column name on a given BigQuery table (a string).
        # updated_value: new value to be added.

        import pandas as pd
            
        if (type(updated_value) == str):
                update_query = f"""
                    UPDATE `{self.project}.{self.dataset}.{str(table)}`
                        SET `{column}` = '{updated_value}'
                        WHERE TRUE
                        """
            
        else:
                update_query = f"""
                    UPDATE `{self.project}.{self.dataset}.{str(table)}`
                        SET `{column}` = {updated_value}
                        WHERE TRUE
                        """
            
        client = self.client
        query_counter = self.query_counter

        table_ref = client.dataset(self.dataset).table(str(table))
        table = client.get_table(table_ref)

        table.streaming_buffer

        if table.streaming_buffer is None:
            job = client.query(update_query)
            job.result()
        else:
            raise RuntimeError("Table contains data in a streaming buffer, which cannot be updated or deleted. Please perform this action when the streaming buffer is empty (may take up to 90 minutes from last data insertion).")

        df_table = job.to_dataframe()
        
        if (show_table): 
            print("Returned table with updated data:\n")
            try:
                from IPython.display import display
                display(df_table)
                
            except:
                print(df_table)
        
        # Vars function allows accessing the attributes from a class as a key from a dictionary.
        # vars(object) is a dictionary where each key is one attribute from the object. A new attribute may be
        # created by setting a value for a new key;
        # Then, an attribute name may be created as a string:
        vars(self)[f"df_table{query_counter}"] = df_table

        if (export_csv):
            if ((saving_directory_path is None)|(saving_directory_path == '')):
                saving_directory_path = f"table{query_counter}.csv"
            
            df_table.to_csv(saving_directory_path)
         
        # Update counter:
        self.query_counter = query_counter + 1    
            
        return df_table    


    def update_value_when_finding_str_or_substring_on_another_column (self, table, column, updated_value, string_column, str_or_substring_to_search, show_table = True, export_csv = False, saving_directory_path = ""):

        # show_table: keep as True to print the queried table, set False to hide it.
        # export_csv: set True to export the queried table as CSV file, or set False not to export it.
        # saving_directory_path: full path containing directories and table name, with .csv extension, used when
        # export_csv = True
        
        # column is the column name on a given BigQuery table (a string).
        # updated_value: new value to be added.
        # string_column: column containing a string or substring that will be searched.
        # str_or_substring_to_search (in quotes): string or substring that will be searched on column 'string_column'. 
        # When it is find, the value on 'column' will be updated.

        import pandas as pd
            
        if (type(updated_value) == str):
                update_query = f"""
                    UPDATE `{self.project}.{self.dataset}.{str(table)}`
                        SET `{column}` = '{updated_value}'
                        WHERE CONTAINS_SUBSTR({string_column}, "{str_or_substring_to_search}")
                        """
            
        else:
                update_query = f"""
                    UPDATE `{self.project}.{self.dataset}.{str(table)}`
                        SET `{column}` = {updated_value}
                        WHERE CONTAINS_SUBSTR({string_column}, "{str_or_substring_to_search}")
                        """
            
        client = self.client
        query_counter = self.query_counter

        table_ref = client.dataset(self.dataset).table(str(table))
        table = client.get_table(table_ref)

        table.streaming_buffer

        if table.streaming_buffer is None:
            job = client.query(update_query)
            job.result()
        else:
            raise RuntimeError("Table contains data in a streaming buffer, which cannot be updated or deleted. Please perform this action when the streaming buffer is empty (may take up to 90 minutes from last data insertion).")

        df_table = job.to_dataframe()
        
        if (show_table): 
            print("Returned table with updated data:\n")
            try:
                from IPython.display import display
                display(df_table)
                
            except:
                print(df_table)
        
        # Vars function allows accessing the attributes from a class as a key from a dictionary.
        # vars(object) is a dictionary where each key is one attribute from the object. A new attribute may be
        # created by setting a value for a new key;
        # Then, an attribute name may be created as a string:
        vars(self)[f"df_table{query_counter}"] = df_table

        if (export_csv):
            if ((saving_directory_path is None)|(saving_directory_path == '')):
                saving_directory_path = f"table{query_counter}.csv"
            
            df_table.to_csv(saving_directory_path)
         
        # Update counter:
        self.query_counter = query_counter + 1    
            
        return df_table


    def update_value_when_finding_numeric_value_on_another_column (self, table, column, updated_value, comparative_column, value_to_search, show_table = True, export_csv = False, saving_directory_path = ""):

        # show_table: keep as True to print the queried table, set False to hide it.
        # export_csv: set True to export the queried table as CSV file, or set False not to export it.
        # saving_directory_path: full path containing directories and table name, with .csv extension, used when
        # export_csv = True
        
        # column is the column name on a given BigQuery table (a string).
        # updated_value: new value to be added.
        # comparative_column: column containing a numeric value that will be searched.
        # value_to_search (in quotes): numeric value that will be searched on column 'comparative_colum'. 
        # When it is find, the value on 'column' will be updated.

        import pandas as pd
            
        if (type(updated_value) == str):
                update_query = f"""
                    UPDATE `{self.project}.{self.dataset}.{str(table)}`
                        SET `{column}` = '{updated_value}'
                        WHERE `{comparative_column}` = {value_to_search}
                        """
            
        else:
                update_query = f"""
                    UPDATE `{self.project}.{self.dataset}.{str(table)}`
                        SET `{column}` = {updated_value}
                        WHERE `{comparative_column}` = {value_to_search}
                        """
            
        client = self.client
        query_counter = self.query_counter

        table_ref = client.dataset(self.dataset).table(str(table))
        table = client.get_table(table_ref)

        table.streaming_buffer

        if table.streaming_buffer is None:
            job = client.query(update_query)
            job.result()
        else:
            raise RuntimeError("Table contains data in a streaming buffer, which cannot be updated or deleted. Please perform this action when the streaming buffer is empty (may take up to 90 minutes from last data insertion).")

        df_table = job.to_dataframe()
        
        if (show_table): 
            print("Returned table with updated data:\n")
            try:
                from IPython.display import display
                display(df_table)
                
            except:
                print(df_table)
        
        # Vars function allows accessing the attributes from a class as a key from a dictionary.
        # vars(object) is a dictionary where each key is one attribute from the object. A new attribute may be
        # created by setting a value for a new key;
        # Then, an attribute name may be created as a string:
        vars(self)[f"df_table{query_counter}"] = df_table

        if (export_csv):
            if ((saving_directory_path is None)|(saving_directory_path == '')):
                saving_directory_path = f"table{query_counter}.csv"
            
            df_table.to_csv(saving_directory_path)
         
        # Update counter:
        self.query_counter = query_counter + 1    
            
        return df_table
