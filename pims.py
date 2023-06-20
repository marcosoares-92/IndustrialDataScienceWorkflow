# FUNCTIONS FROM INDUSTRIAL DATA SCIENCE WORKFLOW (IDSW) PACKAGE
# Extract data from Plant Information Management (PIMS) systems
# AspenTech IP21
# Connect to SQLite Database

# Marco Cesar Prado Soares, Data Scientist Specialist @ Bayer Crop Science LATAM
# marcosoares.feq@gmail.com
# marco.soares@bayer.com


class ip21_extractor:
    
    # Initialize instance attributes.
    # define the Class constructor, i.e., how are its objects:

    def __init__ (self, tag_to_extract = None, actual_tag_name = None, ip21_server = None, data_source = 'localhost', start_timestamp = None, stop_timestamp = None, ip21time_array = [], previous_df_for_concatenation = None, username = None, password = None):
        
        import numpy as np
        import pandas as pd
        
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
        
        import numpy as np
        import pandas as pd
        
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
        start_timedelta = start_timedelta.delta
        # 1ms = 10^-3 s, 1ns = 10^-9 s, so 1 ns = 1ms/(10^6)
        # Divide by 10^6 to obtain the total of miliseconds:
        start_timedelta = start_timedelta/(10**6)
        # Sum with the reference value in IP21 scale to obtain the converted timestamp:
        start_ip21_scale = reference_ip21 + start_timedelta
        # Guarantee that the number is an integer:
        # np.rint rounds to the nearest integer, whereas int to convert to integer:
        start_ip21_scale = int(np.rint(start_ip21_scale))
        
        # Convert the stop timestamp:
        stop_timedelta = stop_timestamp - reference
        # apply the delta method to convert to nanoseconds:
        stop_timedelta = stop_timedelta.delta
        # Divide by 10^6 to obtain the total of miliseconds:
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
        
        import numpy as np
        import pandas as pd
        
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
            timedelta_obj = pd.Timedelta(ip21time_timedelta, unit = 'milliseconds')
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
    
        import numpy as np
        import pandas as pd
        from datetime import datetime, timedelta

        # start_time: dictionary containing start timestamp information.
        # stop_time: dictionary containing stop timestamp information.

        # Alternatively: start_time = 'today', 'now', start_time = 'yesterday', start_time = -10 for 10
        # days before, start_time = -X for - X days before. Units for offsets will be always in days, unless
        # you modify the parameters start_timedelta_unit and stop_timedelta_unit.
        # For the timedelta unit, set 'day' or 'd' for subtracting values in days,'hour' or 'h',
        # 'minute' or 'm' for minutes, 'second' or 's' for seconds, 'milisecond' or 'ms' for miliseconds.
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

                delta_t = pd.Timedelta(1, unit = 'd')
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

                elif ((start_timedelta_unit == 'milisecond') | (start_timedelta_unit == 'ms')):

                    UNIT = 'ms'

                delta_t = pd.Timedelta(start_time, unit = UNIT)
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

                delta_t = pd.Timedelta(1, unit = 'd')
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

                elif ((stop_timedelta_unit == 'milisecond') | (stop_timedelta_unit == 'ms')):

                    UNIT = 'ms'

                delta_t = pd.Timedelta(stop_time, unit = UNIT)
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
        
        import numpy as np
        import pandas as pd
        
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
        import numpy as np
        import pandas as pd
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
        
        if (("er" in dataset.columns) | ("ec" in dataset.columns) | ("es" in dataset.columns)):
            
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
            # Update the start timestamp to be the last_element plus 1 unit (1 milisecond):
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
        
        import numpy as np
        import pandas as pd
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


def get_data_from_ip21 (ip21_server, list_of_tags_to_extract = [{'tag': None, 'actual_name': None}], username = None, password = None, data_source = 'localhost', start_time = {'year': 2015, 'month': 1, 'day':1, 'hour': 0, 'minute': 0, 'second': 0}, stop_time = {'year': 2022, 'month': 4, 'day': 1, 'hour': 0, 'minute': 0, 'second': 0}, start_timedelta_unit = 'day', stop_timedelta_unit = 'day', ip21time_array = [], previous_df_for_concatenation = None):
        
    # ip21_server is a string informing the server name for the IP21 REST API.
    # If you check ASPEN ONE or ASPEN IP21 REST API URL, it will have a format like:
    # http://ip21_server_name/ProcessData/AtProcessDataREST.dll/
    # or like:
    # http://ip21_server_name.company_website/processexplorer/aspenONE.html
    # In this case, declare:
    # ip21_server = 'ip21_server_name' or as 'ip21_server_name/'
    
    # list_of_tags_to_extract = [{'tag': None, 'actual_name': None}] is a list of dictionaries.
    # The dictionaries should have always the same keys: 'tag', containing the tag name as registered
    # in the system, and 'actual_name', with a desired name for the variable. You can add as much
    # tags as you want, but adding several tags may lead to a blockage by the server. The key 'actual_name'
    # may be empty, but dictionaries where the 'tag' value is None will be ignored.
    # Examples: list_of_tags_to_extract = [{'tag': 'TEMP', 'actual_name': 'temperature'}]
    # list_of_tags_to_extract = [{'tag': 'TEMP2.1.2', 'actual_name': 'temperature'},
    # {'tag': 'PUMP.1.2', 'actual_name': 'pump_pressure'}, {'tag': 'PHTANK', 'actual_name': 'ph'}]
    # list_of_tags_to_extract = [{'tag': 'TEMP', 'actual_name': None}]
    
    # username = None, password = None: declare your username and password as strings (in quotes)
    # or keep username = None, password = None to generate input boxes. The key typed on the boxes
    # will be masked, so other users cannot see it.
    
    # data_source = 'localhost': string informing the particular data source to fetch on IP21.
    # Keep data_source = 'localhost' to query all available data sources.
    
    # start_time: dictionary containing start timestamp information.
    # Example: start_time = {'year': 2015, 'month': 1, 'day':1, 'hour': 0, 'minute': 0, 'second': 0}
    # stop_time: dictionary containing stop timestamp information.
    # Example: stop_time = {'year': 2022, 'month': 4, 'day': 1, 'hour': 0, 'minute': 0, 'second': 0}

    # Alternatively: start_time = 'today', 'now', start_time = 'yesterday', start_time = -10 for 10
    # days before, start_time = -X for - X days before. Units for offsets will be always in days, unless
    # you modify the parameters start_timedelta_unit and stop_timedelta_unit.
    # For the timedelta unit, set 'day' or 'd' for subtracting values in days,'hour' or 'h',
    # 'minute' or 'm' for minutes, 'second' or 's' for seconds, 'milisecond' or 'ms' for miliseconds.
    # Put the "-" signal, or the time will be interpreted as a future day from today.
    # Analogously for stop_time.
    # Both dictionaries must contain only float values (for 'year', 'day' and 'month'
    # are integers, naturally).

    ## WARNING: The keys must be always be the same, only change the numeric values.
    ## The keys must be: 'year', 'month', 'day', 'hour', 'minute', and 'second'
    
    # start_timedelta_unit = 'day'
    # If start_time was declared as a numeric value (integer or float), specify the timescale units
    # in this parameter. The possible values are: 'day' or 'd'; 'hour' or 'h'; 'minute' or 'm';
    # 'second' or 's', 'milisecond' or 'ms'.
    # stop_timedelta_unit = 'day' - analogous to start_timedelta_unit. Set this parameter when
    # declaring stop_time as a numeric value.
    
    # ip21time_array = [] - keep this parameter as an empty list or set ip21time_array = None.
    # If you want to use the method to independently convert an array, you could pass this array
    # to the constructor to convert it.
    
    # previous_df_for_concatenation = None: keep it None or, if you want to append the fetched data
    # to a pre-existing database, declare the object containing the pandas dataframe where it will
    # be appended. Example: previous_df_for_concatenation = dataset.
    
    
    from getpass import getpass
    
    if (username is None):
        
        username = input("Enter your username: ")
        
    if (password is None):
        
        password = getpass("Enter your password: ")
    
    # Remove trailing whitespaces:
    username = str(username).strip()
    password = str(password).strip()
    
    if (data_source is None):
        data_source = 'localhost'
    
    if (start_time is None):
        start_time = 'yesterday'
    
    if (stop_time is None):
        stop_time = 'today'
    
    # Start a support list:
    support_list = []
    
    for tag_dict in list_of_tags_to_extract:
        # If there is a tag name, append to support_list:
        if (tag_dict['tag'] is not None):
            support_list.append(tag_dict)
    
    # Now, make support_list the list_of_tags_to_extract itself>
    list_of_tags_to_extract = support_list
    # Only non-empty dictionaries remained
    
    api_call_number = 1
    # Start a list for storing the valid dataframes returned:
    returned_dfs_list = []
    
    # Loop through the list of tags:
    for tag_dict in list_of_tags_to_extract:
        
        tag_to_extract = tag_dict['tag']
        actual_tag_name = tag_dict['actual_name']
        
        # Instantiate an object from class ip21_extractor:
        extractor = ip21_extractor(tag_to_extract = tag_to_extract, actual_tag_name = actual_tag_name, ip21_server = ip21_server, data_source = data_source, start_timestamp = start_time, stop_timestamp = stop_time, ip21time_array = ip21time_array, previous_df_for_concatenation = previous_df_for_concatenation, username = username, password = password)
        # Define the extracted time window:
        extractor = extractor.set_extracted_time_window(start_timedelta_unit = start_timedelta_unit, stop_timedelta_unit = stop_timedelta_unit)
        
        while (extractor.need_next_call == True):
            
            try:
                print(f"API call {api_call_number}: fetching IP21 timestamps from {extractor.start_ip21_scale} to {extractor.stop_ip21_scale}.\n")
                # Get Rest API URL:
                extractor = extractor.get_rest_api_url()
                # Fetch the Database:
                extractor = extractor.fetch_database(request_type = 'get')
                # Retrieve Pandas dataframe:
                extractor = extractor.retrieve_pd_dataframe()
                
                # Go to the next call number:
            
            except:
                print(f"Failed API call {api_call_number} with IP21 timestamps from {extractor.start_ip21_scale} to {extractor.stop_ip21_scale}.")
                print("Returning the last valid dataframe extracted.\n")
                # Force the modification of the attribute with vars function:
                vars(extractor)['need_next_call'] = False
        
            # Get the dataset:
            extracted_df = extractor.dataset

            # Get a dictionary with the returned information:
            returned_data = tag_dict
            returned_data['dataset'] = extracted_df
            
            if (actual_tag_name is not None):
                print(f"Check the the dataframe returned from tag {tag_to_extract} ('{actual_tag_name}') on API call {api_call_number}:\n")
            
            else:
                print(f"Check the the dataframe returned from tag {tag_to_extract} on API call {api_call_number}:\n")
            
            try:
                # only works in Jupyter Notebook:
                from IPython.display import display
                display(extracted_df)

            except: # regular mode
                print(extracted_df)
            
            api_call_number = api_call_number + 1
        
        # Save the last version of the dataset and go to next tag to query.
        # For that, append the dictionary to returned_dfs_list:
        returned_dfs_list.append(returned_data)
    
    # At this level, all tags were saved (finished 'for' loop)
    
    # Return all queried tags. If a single query was queried, there is only one dictionary in the list.
    return returned_dfs_list


def manipulate_sqlite_db (file_path, table_name, action = 'fetch_table', pre_created_engine = None, df = None):

    # file_path: full path of the SQLite file. It may start with './' or '/', but with no more than 2 slashes.
    # It is a string: input in quotes. Example: file_path = '/my_db.db'
    # table_name: string with the name of the table that will be fetched or updated.
    # Example: table_name = 'main_table'

    # action = 'fetch_table' to access a table named table_name from the database.
    # action = 'update_table' to update a table named table_name from the database.

    # pre_created_engine = None - If None, a new engine will be created. If an engine was already created, pass it as argument:
    # pre_created_engine = engine

    # df = None - if a table is going to be updated, input here the new Pandas dataframe (object) correspondent to the table.
    # Example: df = dataset.

    # Make imports and create the engine for the database
    import pandas as pd
    # Configure the SQLite engine
    from sqlalchemy import create_engine
    
    # SQLAlchemy engines documentation
    # https://docs.sqlalchemy.org/en/20/core/engines.html
    # SQLite connects to file-based databases, using the Python built-in module sqlite3 by default.
    # As SQLite connects to local files, the URL format is slightly different. 
    # The “file” portion of the URL is the filename of the database. For a relative file path, this requires 
    # three slashes:
    # sqlite://<nohostname>/<path>
    # where <path> is relative:
    if (pre_created_engine is None):

        try:
                    
            if (file_path[:2] == './'):
                # Add a slash, since sqlite engine requires 3 slashes
                file_path = '/' + file_path[1:]
                
            if (file_path[0] != '/'):
                # Add a slash, since sqlite engine requires 3 slashes
                file_path = '/' + file_path
                        
            file_path = "sqlite://" + file_path
            # file_path = "sqlite:///my_db.db"
                    
            engine = create_engine(file_path)
            #And for an absolute file path, the three slashes are followed by the absolute path:
                
            """
            # Unix/Mac - 4 initial slashes in total
            engine = create_engine("sqlite:////absolute/path/to/foo.db")
                
            # Windows
            engine = create_engine("sqlite:///C:\\path\\to\\foo.db")
                
            # Windows alternative using raw string
            engine = create_engine(r"sqlite:///C:\path\to\foo.db")
            To use a SQLite :memory: database, specify an empty URL:
                
            engine = create_engine("sqlite://")
            More notes on connecting to SQLite at SQLite.
            """
        
        except:
            print("Error trying to create SQLite Engine Database. Check if no more than one slash was added to file path.\n")
            return "error", "error"
    
    else:
        engine = pre_created_engine
            

    if (action == 'fetch_table'):

        try:
            # Access the table from the database
            df = pd.read_sql(table_name, engine)

            print(f"Successfully retrieved table {table_name} from the database.")
            print("Check the 10 first rows of the dataframe:\n")
            
            try:
                # only works in Jupyter Notebook:
                from IPython.display import display
                display(df.head(10))
                    
            except: # regular mode
                print(df.head(10))
           
            return df, engine
        
        except:
            print("Error trying to fetch SQLite Engine Database. If an pre-created engine was provided, check if it is correct and working.\n")
            return "error", "error"
        

    elif (action == 'update_table'):

        try:
            # Set index = False not to add extra indices in the database:
            df.to_sql(table_name, con = engine, if_exists = 'replace', index = False)
            
            print(f"Successfully updated table {table_name} on the SQLite database.")
            print("Check the 10 first rows from this table:\n")
                
            try:
                # only works in Jupyter Notebook:
                from IPython.display import display
                display(df.head(10))
                        
            except: # regular mode
                print(df.head(10))

            return df, engine
        
        except:
            print("Error trying to update SQLite Engine Database. If an pre-created engine was provided, check if it is correct and working.\n")
            return "error", "error"

        