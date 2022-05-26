# FUNCTIONS FROM INDUSTRIAL DATA SCIENCE WORKFLOW (IDSW) PACKAGE
def mount_storage_system (source = 'aws', path_to_store_imported_s3_bucket = '', s3_bucket_name = None, s3_obj_prefix = None):
    
    # source = 'google' for mounting the google drive;
    # source = 'aws' for mounting an AWS S3 bucket.
    
    # THE FOLLOWING PARAMETERS HAVE EFFECT ONLY WHEN source == 'aws'
    
    # path_to_store_imported_s3_bucket: path of the Python environment to which the
    # S3 bucket contents will be imported. If it is None, or if 
    # path_to_store_imported_s3_bucket = '/', bucket will be imported to the root path. 
    # Alternatively, input the path as a string (in quotes). e.g. 
    # path_to_store_imported_s3_bucket = 'copied_s3_bucket'
    
    # s3_bucket_name = None.
    ## This parameter is obbligatory to access an AWS S3 bucket. Substitute it for a string
    # with the bucket's name. e.g. s3_bucket_name = "aws-bucket-1" access a bucket named as
    # "aws-bucket-1"
    
    # s3_obj_prefix = None. Keep it None or as an empty string (s3_obj_key_prefix = '')
    # to import the whole bucket content, instead of a single object from it.
    # Alternatively, set it as a string containing the subfolder from the bucket to import:
    # Suppose that your bucket (admin-created) has four objects with the following object 
    # keys: Development/Projects1.xls; Finance/statement1.pdf; Private/taxdocument.pdf; and
    # s3-dg.pdf. The s3-dg.pdf key does not have a prefix, so its object appears directly 
    # at the root level of the bucket. If you open the Development/ folder, you see 
    # the Projects.xlsx object in it.
    # Check Amazon documentation:
    # https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html
    
    # In summary, if the path of the file is: 'bucket/my_path/.../file.csv'
    # where 'bucket' is the bucket's name, key_prefix = 'my_path/.../', without the
    # 'file.csv' (file name with extension) last part.
    
    # So, declare the prefix as S3_OBJECT_FOLDER_PREFIX to import only files from
    # a given folder (directory) of the bucket.
    # DO NOT PUT A SLASH before (to the right of) the prefix;
    # DO NOT ADD THE BUCKET'S NAME TO THE right of the prefix:
    # S3_OBJECT_FOLDER_PREFIX = "bucket_directory1/.../bucket_directoryN/"

    # Alternatively, provide the full path of a given file if you want to import only it:
    # S3_OBJECT_FOLDER_PREFIX = "bucket_directory1/.../bucket_directoryN/my_file.ext"
    # where my_file is the file's name, and ext is its extension.


    # Attention: after running this function for fetching AWS Simple Storage System (S3), 
    # your 'AWS Access key ID' and your 'Secret access key' will be requested.
    # The 'Secret access key' will be hidden through dots, so it cannot be visualized or copied by
    # other users. On the other hand, the same is not true for 'Access key ID', the bucket's name 
    # and the prefix. All of these are sensitive information from the organization.
    # Therefore, after importing the information, always remember of cleaning the output of this cell
    # and of removing such information from the strings.
    # Remember that these data may contain privilege for accessing the information, so it should not
    # be used for non-authorized people.

    # Also, remember of deleting the imported files from the workspace after finishing the analysis.
    # The costs for storing the files in S3 is quite inferior than those for storing directly in the
    # workspace. Also, files stored in S3 may be accessed for other users than those with access to
    # the notebook's workspace.
    
    
    if (source == 'google'):
        
        from google.colab import drive
        # Google Colab library must be imported only in case it is
        # going to be used, for avoiding AWS compatibility issues.
        
        print("Associate the Python environment to your Google Drive account, and authorize the access in the opened window.")
        
        drive.mount('/content/drive')
        
        print("Now your Python environment is connected to your Google Drive: the root directory of your environment is now the root of your Google Drive.")
        print("In Google Colab, navigate to the folder icon (\'Files\') of the left navigation menu to find a specific folder or file in your Google Drive.")
        print("Click on the folder or file name and select the elipsis (...) icon on the right of the name to reveal the option \'Copy path\', which will give you the path to use as input for loading objects and files on your Python environment.")
        print("Caution: save your files into different directories of the Google Drive. If files are all saved in a same folder or directory, like the root path, they may not be accessible from your Python environment.")
        print("If you still cannot see the file after moving it to a different folder, reload the environment.")
    
    elif (source == 'aws'):
        
        import os
        import boto3
        # boto3 is AWS S3 Python SDK
        # sagemaker and boto3 libraries must be imported only in case 
        # they are going to be used, for avoiding 
        # Google Colab compatibility issues.
        from getpass import getpass

        # Check if path_to_store_imported_s3_bucket is None. If it is, make it the root directory:
        if ((path_to_store_imported_s3_bucket is None)|(str(path_to_store_imported_s3_bucket) == "/")):
            
            # For the S3 buckets, the path should not start with slash. Assign the empty
            # string instead:
            path_to_store_imported_s3_bucket = ""
            print("Bucket\'s content will be copied to the notebook\'s root directory.")
        
        elif (str(path_to_store_imported_s3_bucket) == ""):
            # Guarantee that the path is the empty string.
            # Avoid accessing the else condition, what would raise an error
            # since the empty string has no character of index 0
            path_to_store_imported_s3_bucket = str(path_to_store_imported_s3_bucket)
            print("Bucket\'s content will be copied to the notebook\'s root directory.")
        
        else:
            # Use the str attribute to guarantee that the path was read as a string:
            path_to_store_imported_s3_bucket = str(path_to_store_imported_s3_bucket)
            
            if(path_to_store_imported_s3_bucket[0] == "/"):
                # the first character is the slash. Let's remove it

                # In AWS, neither the prefix nor the path to which the file will be imported
                # (file from S3 to workspace) or from which the file will be exported to S3
                # (the path in the notebook's workspace) may start with slash, or the operation
                # will not be concluded. Then, we have to remove this character if it is present.

                # The slash is character 0. Then, we want all characters from character 1 (the
                # second) to character len(str(path_to_store_imported_s3_bucket)) - 1, the index
                # of the last character. So, we can slice the string from position 1 to position
                # the slicing syntax is: string[1:] - all string characters from character 1
                # string[:10] - all string characters from character 10-1 = 9 (including 9); or
                # string[1:10] - characters from 1 to 9
                # So, slice the whole string, starting from character 1:
                path_to_store_imported_s3_bucket = path_to_store_imported_s3_bucket[1:]
                # attention: even though strings may be seem as list of characters, that can be
                # sliced, we cannot neither simply assign a character to a given position nor delete
                # a character from a position.

        # Ask the user to provide the credentials:
        ACCESS_KEY = input("Enter your AWS Access Key ID here (in the right). It is the value stored in the field \'Access key ID\' from your AWS user credentials CSV file.")
        print("\n") # line break
        SECRET_KEY = getpass("Enter your password (Secret key) here (in the right). It is the value stored in the field \'Secret access key\' from your AWS user credentials CSV file.")
        
        # The use of 'getpass' instead of 'input' hide the password behind dots.
        # So, the password is not visible by other users and cannot be copied.
        
        print("\n")
        print("WARNING: The bucket\'s name, the prefix, the AWS access key ID, and the AWS Secret access key are all sensitive information, which may grant access to protected information from the organization.\n")
        print("After copying data from S3 to your workspace, remember of removing these information from the notebook, specially if it is going to be shared. Also, remember of removing the files from the workspace.\n")
        print("The cost for storing files in Simple Storage Service is quite inferior than the one for storing directly in SageMaker workspace. Also, files stored in S3 may be accessed for other users than those with access the notebook\'s workspace.\n")

        # Check if the user actually provided the mandatory inputs, instead
        # of putting None or empty string:
        if ((ACCESS_KEY is None) | (ACCESS_KEY == '')):
            print("AWS Access Key ID is missing. It is the value stored in the field \'Access key ID\' from your AWS user credentials CSV file.")
            return "error"
        elif ((SECRET_KEY is None) | (SECRET_KEY == '')):
            print("AWS Secret Access Key is missing. It is the value stored in the field \'Secret access key\' from your AWS user credentials CSV file.")
            return "error"
        elif ((s3_bucket_name is None) | (s3_bucket_name == '')):
            print ("Please, enter a valid S3 Bucket\'s name. Do not add sub-directories or folders (prefixes), only the name of the bucket itself.")
            return "error"
        
        else:
            # Use the str attribute to guarantee that all AWS parameters were properly read as strings, and not as
            # other variables (like integers or floats):
            ACCESS_KEY = str(ACCESS_KEY)
            SECRET_KEY = str(SECRET_KEY)
            s3_bucket_name = str(s3_bucket_name)
        
        if(s3_bucket_name[0] == "/"):
                # the first character is the slash. Let's remove it

                # In AWS, neither the prefix nor the path to which the file will be imported
                # (file from S3 to workspace) or from which the file will be exported to S3
                # (the path in the notebook's workspace) may start with slash, or the operation
                # will not be concluded. Then, we have to remove this character if it is present.

                # So, slice the whole string, starting from character 1 (as did for 
                # path_to_store_imported_s3_bucket):
                s3_bucket_name = s3_bucket_name[1:]

        # Remove any possible trailing (white and tab spaces) spaces
        # That may be present in the string. Use the Python string
        # rstrip method, which is the equivalent to the Trim function:
        # When no arguments are provided, the whitespaces and tabulations
        # are the removed characters
        # https://www.w3schools.com/python/ref_string_rstrip.asp?msclkid=ee2d05c3c56811ecb1d2189d9f803f65
        s3_bucket_name = s3_bucket_name.rstrip()
        ACCESS_KEY = ACCESS_KEY.rstrip()
        SECRET_KEY = SECRET_KEY.rstrip()
        # Since the user manually inputs the parameters ACCESS and SECRET_KEY,
        # it is easy to input whitespaces without noticing that.

        # Now process the non-obbligatory parameter.
        # Check if a prefix was passed as input parameter. If so, we must select only the names that start with
        # The prefix.
        # Example: in the bucket 'my_bucket' we have a directory 'dir1'.
        # In the main (root) directory, we have a file 'file1.json' like: '/file1.json'
        # If we pass the prefix 'dir1', we want only the files that start as '/dir1/'
        # such as: 'dir1/file2.json', excluding the file in the main (root) directory and excluding the files in other
        # directories. Also, we want to eliminate the file names with no extensions, like 'dir1/' or 'dir1/dir2',
        # since these object names represent folders or directories, not files.	

        if (s3_obj_prefix is None):
            print ("No prefix, specific object, or subdirectory provided.") 
            print (f"Then, retrieving all content from the bucket \'{s3_bucket_name}\'.\n")
        elif ((s3_obj_prefix == "/") | (s3_obj_prefix == '')):
            # The root directory in the bucket must not be specified starting with the slash
            # If the root "/" or the empty string '' is provided, make
            # it equivalent to None (no directory)
            s3_obj_prefix = None
            print ("No prefix, specific object, or subdirectory provided.") 
            print (f"Then, retrieving all content from the bucket \'{s3_bucket_name}\'.\n")
    
        else:
            # Since there is a prefix, use the str attribute to guarantee that the path was read as a string:
            s3_obj_prefix = str(s3_obj_prefix)
            
            if(s3_obj_prefix[0] == "/"):
                # the first character is the slash. Let's remove it

                # In AWS, neither the prefix nor the path to which the file will be imported
                # (file from S3 to workspace) or from which the file will be exported to S3
                # (the path in the notebook's workspace) may start with slash, or the operation
                # will not be concluded. Then, we have to remove this character if it is present.

                # So, slice the whole string, starting from character 1 (as did for 
                # path_to_store_imported_s3_bucket):
                s3_obj_prefix = s3_obj_prefix[1:]

            # Remove any possible trailing (white and tab spaces) spaces
            # That may be present in the string. Use the Python string
            # rstrip method, which is the equivalent to the Trim function:
            s3_obj_prefix = s3_obj_prefix.rstrip()
            
            # Store the total characters in the prefix string after removing the initial slash
            # and trailing spaces:
            prefix_len = len(s3_obj_prefix)
            
            print("AWS Access Credentials, and bucket\'s prefix, object or subdirectory provided.\n")	

            
        print ("Starting connection with the S3 bucket.\n")
        
        try:
            # Start S3 client as the object 's3_client'
            s3_client = boto3.resource('s3', aws_access_key_id = ACCESS_KEY, aws_secret_access_key = SECRET_KEY)
        
            print(f"Credentials accepted by AWS. S3 client successfully started.\n")
            # An object 'data_table.xlsx' in the main (root) directory of the s3_bucket is stored in Python environment as:
            # s3.ObjectSummary(bucket_name='bucket_name', key='data_table.xlsx')
            # The name of each object is stored as the attribute 'key' of the object.
        
        except:
            
            print("Failed to connect to AWS Simple Storage Service (S3). Review if your credentials are correct.")
            print("The variable \'access_key\' must be set as the value (string) stored as \'Access key ID\' in your user security credentials CSV file.")
            print("The variable \'secret_key\' must be set as the value (string) stored as \'Secret access key\' in your user security credentials CSV file.")
        
        try:
            # Connect to the bucket specified as 'bucket_name'.
            # The bucket is started as the object 's3_bucket':
            s3_bucket = s3_client.Bucket(s3_bucket_name)
            print(f"Connection with bucket \'{s3_bucket_name}\' stablished.\n")
            
        except:
            
            print("Failed to connect with the bucket, which usually happens when declaring a wrong bucket\'s name.") 
            print("Check the spelling of your bucket_name string and remember that it must be all in lower-case.\n")
                

        # Then, let's obtain a list of all objects in the bucket (list bucket_objects):
        
        bucket_objects_list = []

        # Loop through all objects of the bucket:
        for stored_obj in s3_bucket.objects.all():
            
            # Loop through all elements 'stored_obj' from s3_bucket.objects.all()
            # Which stores the ObjectSummary for all objects in the bucket s3_bucket:
            # Let's store only the key attribute and use the str function
            # to guarantee that all values were stored as strings.
            bucket_objects_list.append(str(stored_obj.key))
        
        # Now start a support list to store only the elements from
        # bucket_objects_list that are not folders or directories
        # (objects with extensions).
        # If a prefix was provided, only files with that prefix should
        # be added:
        support_list = []
        
        for stored_obj in bucket_objects_list:
            
            # Loop through all elements 'stored_obj' from the list
            # bucket_objects_list

            # Check the file extension.
            file_extension = os.path.splitext(stored_obj)[1][1:]
            
            # The os.path.splitext method splits the string into its FIRST dot (".") to
            # separate the file extension from the full path. Example:
            # "C:/dir1/dir2/data_table.csv" is split into:
            # "C:/dir1/dir2/data_table" (root part) and '.csv' (extension part)
            # https://www.geeksforgeeks.org/python-os-path-splitext-method/?msclkid=2d56198fc5d311ec820530cfa4c6d574

            # os.path.splitext(stored_obj) is a tuple of strings: the first is the complete file
            # root with no extension; the second is the extension starting with a point: '.txt'
            # When we set os.path.splitext(stored_obj)[1], we are selecting the second element of
            # the tuple. By selecting os.path.splitext(stored_obj)[1][1:], we are taking this string
            # from the second character (index 1), eliminating the dot: 'txt'


            # Check if the file extension is not an empty string '' (i.e., that it is different from != the empty
            # string:
            if (file_extension != ''):
                    
                    # The extension is different from the empty string, so it is not neither a folder nor a directory
                    # The object is actually a file and may be copied if it satisfies the prefix condition. If there
                    # is no prefix to check, we may simply copy the object to the list.

                    # If there is a prefix, the first characters of the stored_obj must be the prefix:
                    if not (s3_obj_prefix is None):
                        
                        # Check the characters from the position 0 (1st character) to the position
                        # prefix_len - 1. Since a prefix was declared, we want only the objects that this first portion
                        # corresponds to the prefix. string[i:j] slices the string from index i to index j-1
                        # Then, the 1st portion of the string to check is: string[0:(prefix_len)]

                        # Slice the string stored_obj from position 0 (1st character) to position prefix_len - 1,
                        # The position that the prefix should end.
                        obj_name_first_part = (stored_obj)[0:(prefix_len)]
                        
                        # If this first part is the prefix, then append the object to 
                        # support list:
                        if (obj_name_first_part == (s3_obj_prefix)):

                                support_list.append(stored_obj)

                    else:
                        # There is no prefix, so we can simply append the object to the list:
                        support_list.append(stored_obj)

            
        # Make the objects list the support list itself:
        bucket_objects_list = support_list
            
        # Now, bucket_objects_list contains the names of all objects from the bucket that must be copied.

        print("Finished mapping objects to fetch. Now, all these objects from S3 bucket will be copied to the notebook\'s workspace, in the specified directory.\n")
        print(f"A total of {len(bucket_objects_list)} files were found in the specified bucket\'s prefix (\'{s3_obj_prefix}\').")
        print(f"The first file found is \'{bucket_objects_list[0]}\'; whereas the last file found is \'{bucket_objects_list[len(bucket_objects_list) - 1]}\'.")
            
        # Now, let's try copying the files:
            
        try:
            
            # Loop through all objects in the list bucket_objects and copy them to the workspace:
            for copied_object in bucket_objects_list:

                # Select the object in the bucket previously started as 's3_bucket':
                selected_object = s3_bucket.Object(copied_object)
            
                # Now, copy this object to the workspace:
                # Set the new file_path. Notice that by now, copied_object may be a string like:
                # 'dir1/.../dirN/file_name.ext', where dirN is the n-th directory and ext is the file extension.
                # We want only the file_name to joing with the path to store the imported bucket. So, we can use the
                # str.split method specifying the separator sep = '/' to break the string into a list of substrings.
                # The last element from this list will be 'file_name.ext'
                # https://www.w3schools.com/python/ref_string_split.asp?msclkid=135399b6c63111ecada75d7d91add056

                # 1. Break the copied_object full path into the list object_path_list, using the .split method:
                object_path_list = copied_object.split(sep = "/")

                # 2. Get the last element from this list. Since it has length len(object_path_list) and indexing starts from
                # zero, the index of the last element is (len(object_path_list) - 1):
                fetched_object = object_path_list[(len(object_path_list) - 1)]

                # 3. Finally, join the string fetched_object with the new path (path on the notebook's workspace) to finish
                # The new object's file_path:

                file_path = os.path.join(path_to_store_imported_s3_bucket, fetched_object)

                # Download the selected object to the workspace in the specified file_path
                # The parameter Filename must be input with the path of the copied file, including its name and
                # extension. Example Filename = "/my_table.xlsx" copies a xlsx file named 'my_table' to the notebook's main (root)
                # directory
                selected_object.download_file(Filename = file_path)

                print(f"The file \'{fetched_object}\' was successfully copied to notebook\'s workspace.\n")

                
            print("Finished copying the files from the bucket to the notebook\'s workspace. It may take a couple of minutes untill they be shown in SageMaker environment.\n") 
            print("Do not forget to delete these copies after finishing the analysis. They will remain stored in the bucket.\n")


        except:

            # Run this code for any other exception that may happen (no exception error
            # specified, so any exception runs the following code).
            # Check: https://pythonbasics.org/try-except/?msclkid=4f6b4540c5d011ecb1fe8a4566f632a6
            # for seeing how to handle successive exceptions

            print("Attention! The function raised an exception error, which is probably due to the AWS Simple Storage Service (S3) permissions.")
            print("Before running again this function, check this quick guide for configuring the permission roles in AWS.\n")
            print("It is necessary to create an user with full access permissions to interact with S3 from SageMaker. To configure the User, go to the upper ribbon of AWS, click on Services, and select IAM – Identity and Access Management.")
            print("1. In IAM\'s lateral panel, search for \'Users\' in the group of Access Management.")
            print("2. Click on the \'Add users\' button.")
            print("3. Set an user name in the text box \'User name\'.")
            print("Attention: users and S3 buckets cannot be written in upper case. Also, selecting a name already used by an Amazon user or bucket will raise an error message.\n")
            print("4. In the field \'Select type of Access to AWS\'-\'Select type of AWS credentials\' select the option \'Access key - Programmatic access\'. After that, click on the button \'Next: Permissions\'.")
            print("5. In the field \'Set Permissions\', keep the \'Add user to a group\' button marked.")
            print("6. In the field \'Add user to a group\', click on \'Create group\' (alternatively, you can be added to a group already configured or copy the permissions of another user.")
            print("7. In the text box \'Group\'s name\', set a name for the new group of permissions.")
            print("8. In the search bar below (\'Filter politics\'), search for a politics that fill your needs, and check the option button on the left of this politic. The politics \'AmazonS3FullAccess\' grants full access to the S3 content.")
            print("9. Finally, click on \'Create a group\'.")
            print("10. After the group is created, it will appear with a check box marked, over the previous groups. Keep it marked and click on the button \'Next: Tags\'.")
            print("11. Create and note down the Access key ID and Secret access key. You can also download a comma separated values (CSV) file containing the credentials for future use.")
            print("ATTENTION: These parameters are required for accessing the bucket\'s content from any application, including AWS SageMaker.")
            print("12. Click on \'Next: Review\' and review the user credentials information and permissions.")
            print("13. Click on \'Create user\' and click on the download button to download the CSV file containing the user credentials information.")
            print("The headers of the CSV file (the stored fields) is: \'User name, Password, Access key ID, Secret access key, Console login link\'.")
            print("You need both the values indicated as \'Access key ID\' and as \'Secret access key\' to fetch the S3 bucket.")
            print("\n") # line break
            print("After acquiring the necessary user privileges, use the boto3 library to fetch the bucket from the Python code. boto3 is AWS S3 Python SDK.")
            print("For fetching a specific bucket\'s file use the following code:\n")
            print("1. Set a variable \'access_key\' as the value (string) stored as \'Access key ID\' in your user security credentials CSV file.")
            print("2. Set a variable \'secret_key\' as the value (string) stored as \'Secret access key\' in your user security credentials CSV file.")
            print("3. Set a variable \'bucket_name\' as a string containing only the name of the bucket. Do not add subdirectories, folders (prefixes), or file names.")
            print("Example: if your bucket is named \'my_bucket\' and its main directory contains folders like \'folder1\', \'folder2\', etc, do not declare bucket_name = \'my_bucket/folder1\', even if you only want files from folder1.")
            print("ALWAYS declare only the bucket\'s name: bucket_name = \'my_bucket\'.")
            print("4. Set a variable \'file_path\' containing the path from the bucket\'s subdirectories to the file you want to fetch. Include the file name and its extension.")
            print("If the file is stored in the bucket\'s root (main) directory: file_path = \"my_file.ext\".")
            print("If the path of the file in the bucket is: \'dir1/…/dirN/my_file.ext\', where dirN is the N-th subdirectory, and dir1 is a folder or directory of the main (root) bucket\'s directory: file_path = \"dir1/…/dirN/my_file.ext\".")
            print("Also, we say that \'dir1/…/dirN/\' is the file\'s prefix. Notice that the name of the bucket is never declared here as the path for fetching its content from the Python code.")
            print("5. Set a variable named \'new_path\' to store the path of the file copied to the notebook’s workspace. This path must contain the file name and its extension.")
            print("Example: if you want to copy \'my_file.ext\' to the root directory of the notebook’s workspace, set: new_path = \"/my_file.ext\".")
            print("6. Finally, declare the following code, which refers to the defined variables:\n")

            # Let's use triple quotes to declare a formated string
            example_code = """
                import boto3
                # Start S3 client as the object 's3_client'
                s3_client = boto3.resource('s3', aws_access_key_id = access_key, aws_secret_access_key = secret_key)
                # Connect to the bucket specified as 'bucket_name'.
                # The bucket is started as the object 's3_bucket':
                s3_bucket = s3_client.Bucket(bucket_name)
                # Select the object in the bucket previously started as 's3_bucket':
                selected_object = s3_bucket.Object(file_path)
                # Download the selected object to the workspace in the specified file_path
                # The parameter Filename must be input with the path of the copied file, including its name and
                # extension. Example Filename = "/my_table.xlsx" copies a xlsx file named 'my_table' to the notebook's main (root)
                # directory
                selected_object.download_file(Filename = new_path)
                """

            print(example_code)

            print("An object \'my_file.ext\' in the main (root) directory of the s3_bucket is stored in Python environment as:")
            print("""s3.ObjectSummary(bucket_name='bucket_name', key='my_file.ext'""") 
            # triple quotes to keep the internal quotes without using too much backslashes "\" (the ignore next character)
            print("Then, the name of each object is stored as the attribute \'key\' of the object. To view all objects, we can loop through their \'key\' attributes:\n")
            example_code = """
                # Loop through all objects of the bucket:
                for stored_obj in s3_bucket.objects.all():		
                    # Loop through all elements 'stored_obj' from s3_bucket.objects.all()
                    # Which stores the ObjectSummary for all objects in the bucket s3_bucket:
                    # Print the object’s names:
                    print(stored_obj.key)
                    """

            print(example_code)

                
    else:
        
        print("Select a valid source: \'google\' for mounting Google Drive; or \'aws\' for accessing AWS S3 Bucket.")


def upload_to_or_download_file_from_colab (action = 'download', file_to_download_from_colab = None):
    
    # action = 'download' to download the file to the local machine
    # action = 'upload' to upload a file from local machine to
    # Google Colab's instant memory
    
    # file_to_download_from_colab = None. This parameter is obbligatory when
    # action = 'download'. 
    # Declare as file_to_download_from_colab the file that you want to download, with
    # the correspondent extension.
    # It should not be declared in quotes.
    # e.g. to download a dictionary named dict, object_to_download_from_colab = 'dict.pkl'
    # To download a dataframe named df, declare object_to_download_from_colab = 'df.csv'
    # To export a model named keras_model, declare object_to_download_from_colab = 'keras_model.h5'
 
    from google.colab import files
    # google.colab library must be imported only in case 
    # it is going to be used, for avoiding 
    # AWS compatibility issues.
        
    if (action == 'upload'):
            
        print("Click on the button for file selection and select the files from your machine that will be uploaded in the Colab environment.")
        print("Warning: the files will be removed from Colab memory after the Kernel dies or after the notebook is closed.")
        # this functionality requires the previous declaration:
        ## from google.colab import files
            
        colab_files_dict = files.upload()
            
        # The files are stored into a dictionary called colab_files_dict where the keys
        # are the names of the files and the values are the files themselves.
        ## e.g. if you upload a single file named "dictionary.pkl", the dictionary will be
        ## colab_files_dict = {'dictionary.pkl': file}, where file is actually a big string
        ## representing the contents of the file. The length of this value is the size of the
        ## uploaded file, in bytes.
        ## To access the file is like accessing a value from a dictionary: 
        ## d = {'key1': 'val1'}, d['key1'] == 'val1'
        ## we simply declare the key inside brackets and quotes, the same way we would do for
        ## accessing the column of a dataframe.
        ## In this example, colab_files_dict['dictionary.pkl'] access the content of the 
        ## .pkl file, and len(colab_files_dict['dictionary.pkl']) is the size of the .pkl
        ## file in bytes.
        ## To check the dictionary keys, apply the method .keys() to the dictionary (with empty
        ## parentheses): colab_files_dict.keys()
            
        for key in colab_files_dict.keys():
            #loop through each element of the list of keys of the dictionary
            # (list colab_files_dict.keys()). Each element is named 'key'
            print(f"User uploaded file {key} with length {len(colab_files_dict[key])} bytes.")
            # The key is the name of the file, and the length of the value
            ## correspondent to the key is the file's size in bytes.
            ## Notice that the content of the uploaded object must be passed 
            ## as argument for a proper function to be interpreted. 
            ## For instance, the content of a xlsx file should be passed as
            ## argument for Pandas .read_excel function; the pkl file must be passed as
            ## argument for pickle.
            ## e.g., if you uploaded 'table.xlsx' and stored it into colab_files_dict you should
            ## declare df = pd.read_excel(colab_files_dict['table.xlsx']) to obtain a dataframe
            ## df from the uploaded table. Notice that is the value, not the key, that is the
            ## argument.
                
            print("The uploaded files are stored into a dictionary object named as colab_files_dict.")
            print("Each key from this dictionary is the name of an uploaded file. The value correspondent to that key is the file itself.")
            print("The structure of a general Python dictionary is dict = {\'key1\': value1}. To access value1, declare file = dict[\'key1\'], as if you were accessing a column from a dataframe.")
            print("Then, if you uploaded a file named \'table.xlsx\', you can access this file as:")
            print("uploaded_file = colab_files_dict[\'table.xlsx\']")
            print("Notice, though, that the object uploaded_file is the whole file content, not a Python object already converted. To convert to a Python object, pass this element as argument for a proper function or method.")
            print("In this example, to convert the object uploaded_file to a dataframe, Pandas pd.read_excel function could be used. In the following line, a df dataframe object is obtained from the uploaded file:")
            print("df = pd.read_excel(uploaded_file)")
            print("Also, the uploaded file itself will be available in the Colaboratory Notebook\'s workspace.")
            
            return colab_files_dict
        
    elif (action == 'download'):
            
        if (file_to_download_from_colab is None):
                
            #No object was declared
            print("Please, inform a file to download from the notebook\'s workspace. It should be declared in quotes and with the extension: e.g. \'table.csv\'.")
            
        else:
                
            print("The file will be downloaded to your computer.")

            files.download(file_to_download_from_colab)

            print(f"File {file_to_download_from_colab} successfully downloaded from Colab environment.")

    else:
            
            print("Please, select a valid action, \'download\' or \'upload\'.")


def export_files_to_s3 (list_of_file_names_with_extensions, directory_of_notebook_workspace_storing_files_to_export = None, s3_bucket_name = None, s3_obj_prefix = None):
    
    import os
    import boto3
    # boto3 is AWS S3 Python SDK
    # sagemaker and boto3 libraries must be imported only in case 
    # they are going to be used, for avoiding 
    # Google Colab compatibility issues.
    from getpass import getpass
    
    # list_of_file_names_with_extensions: list containing all the files to export to S3.
    # Declare it as a list even if only a single file will be exported.
    # It must be a list of strings containing the file names followed by the extensions.
    # Example, to a export a single file my_file.ext, where my_file is the name and ext is the
    # extension:
    # list_of_file_names_with_extensions = ['my_file.ext']
    # To export 3 files, file1.ext1, file2.ext2, and file3.ext3:
    # list_of_file_names_with_extensions = ['file1.ext1', 'file2.ext2', 'file3.ext3']
    # Other examples:
    # list_of_file_names_with_extensions = ['Screen_Shot.png', 'dataset.csv']
    # list_of_file_names_with_extensions = ["dictionary.pkl", "model.h5"]
    # list_of_file_names_with_extensions = ['doc.pdf', 'model.dill']
    
    # directory_of_notebook_workspace_storing_files_to_export: directory from notebook's workspace
    # from which the files will be exported to S3. Keep it None, or
    # directory_of_notebook_workspace_storing_files_to_export = "/"; or
    # directory_of_notebook_workspace_storing_files_to_export = '' (empty string) to export from
    # the root (main) directory.
    # Alternatively, set as a string containing only the directories and folders, not the file names.
    # Examples: directory_of_notebook_workspace_storing_files_to_export = 'folder1';
    # directory_of_notebook_workspace_storing_files_to_export = 'folder1/folder2/'
    
    # For this function, all exported files must be located in the same directory.
    
    
    # s3_bucket_name = None.
    ## This parameter is obbligatory to access an AWS S3 bucket. Substitute it for a string
    # with the bucket's name. e.g. s3_bucket_name = "aws-bucket-1" access a bucket named as
    # "aws-bucket-1"
    
    # s3_obj_prefix = None. Keep it None or as an empty string (s3_obj_key_prefix = '')
    # to import the whole bucket content, instead of a single object from it.
    # Alternatively, set it as a string containing the subfolder from the bucket to import:
    # Suppose that your bucket (admin-created) has four objects with the following object 
    # keys: Development/Projects1.xls; Finance/statement1.pdf; Private/taxdocument.pdf; and
    # s3-dg.pdf. The s3-dg.pdf key does not have a prefix, so its object appears directly 
    # at the root level of the bucket. If you open the Development/ folder, you see 
    # the Projects.xlsx object in it.
    # Check Amazon documentation:
    # https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-keys.html
    
    # In summary, if the path of the file is: 'bucket/my_path/.../file.csv'
    # where 'bucket' is the bucket's name, key_prefix = 'my_path/.../', without the
    # 'file.csv' (file name with extension) last part.
    
    # So, declare the prefix as S3_OBJECT_FOLDER_PREFIX to import only files from
    # a given folder (directory) of the bucket.
    # DO NOT PUT A SLASH before (to the right of) the prefix;
    # DO NOT ADD THE BUCKET'S NAME TO THE right of the prefix:
    # S3_OBJECT_FOLDER_PREFIX = "bucket_directory1/.../bucket_directoryN/"

    # Alternatively, provide the full path of a given file if you want to import only it:
    # S3_OBJECT_FOLDER_PREFIX = "bucket_directory1/.../bucket_directoryN/my_file.ext"
    # where my_file is the file's name, and ext is its extension.


    # Attention: after running this function for connecting with AWS Simple Storage System (S3), 
    # your 'AWS Access key ID' and your 'Secret access key' will be requested.
    # The 'Secret access key' will be hidden through dots, so it cannot be visualized or copied by
    # other users. On the other hand, the same is not true for 'Access key ID', the bucket's name 
    # and the prefix. All of these are sensitive information from the organization.
    # Therefore, after importing the information, always remember of cleaning the output of this cell
    # and of removing such information from the strings.
    # Remember that these data may contain privilege for accessing the information, so it should not
    # be used for non-authorized people.

    # Also, remember of deleting the exported from the workspace after finishing the analysis.
    # The costs for storing the files in S3 is quite inferior than those for storing directly in the
    # workspace. Also, files stored in S3 may be accessed for other users than those with access to
    # the notebook's workspace.
    
    
    # Check if directory_of_notebook_workspace_storing_files_to_export is None. 
    # If it is, make it the root directory:
    if ((directory_of_notebook_workspace_storing_files_to_export is None)|(str(directory_of_notebook_workspace_storing_files_to_export) == "/")):
            
            # For the S3 buckets, the path should not start with slash. Assign the empty
            # string instead:
            directory_of_notebook_workspace_storing_files_to_export = ""
            print("The files will be exported from the notebook\'s root directory to S3.")
    
    elif (str(directory_of_notebook_workspace_storing_files_to_export) == ""):
        
            # Guarantee that the path is the empty string.
            # Avoid accessing the else condition, what would raise an error
            # since the empty string has no character of index 0
            directory_of_notebook_workspace_storing_files_to_export = str(directory_of_notebook_workspace_storing_files_to_export)
            print("The files will be exported from the notebook\'s root directory to S3.")
          
    else:
        # Use the str attribute to guarantee that the path was read as a string:
        directory_of_notebook_workspace_storing_files_to_export = str(directory_of_notebook_workspace_storing_files_to_export)
            
        if(directory_of_notebook_workspace_storing_files_to_export[0] == "/"):
            # the first character is the slash. Let's remove it

            # In AWS, neither the prefix nor the path to which the file will be imported
            # (file from S3 to workspace) or from which the file will be exported to S3
            # (the path in the notebook's workspace) may start with slash, or the operation
            # will not be concluded. Then, we have to remove this character if it is present.

            # The slash is character 0. Then, we want all characters from character 1 (the
            # second) to character len(str(path_to_store_imported_s3_bucket)) - 1, the index
            # of the last character. So, we can slice the string from position 1 to position
            # the slicing syntax is: string[1:] - all string characters from character 1
            # string[:10] - all string characters from character 10-1 = 9 (including 9); or
            # string[1:10] - characters from 1 to 9
            # So, slice the whole string, starting from character 1:
            directory_of_notebook_workspace_storing_files_to_export = directory_of_notebook_workspace_storing_files_to_export[1:]
            # attention: even though strings may be seem as list of characters, that can be
            # sliced, we cannot neither simply assign a character to a given position nor delete
            # a character from a position.

    # Ask the user to provide the credentials:
    ACCESS_KEY = input("Enter your AWS Access Key ID here (in the right). It is the value stored in the field \'Access key ID\' from your AWS user credentials CSV file.")
    print("\n") # line break
    SECRET_KEY = getpass("Enter your password (Secret key) here (in the right). It is the value stored in the field \'Secret access key\' from your AWS user credentials CSV file.")
        
    # The use of 'getpass' instead of 'input' hide the password behind dots.
    # So, the password is not visible by other users and cannot be copied.
        
    print("\n")
    print("WARNING: The bucket\'s name, the prefix, the AWS access key ID, and the AWS Secret access key are all sensitive information, which may grant access to protected information from the organization.\n")
    print("After finish exporting data to S3, remember of removing these information from the notebook, specially if it is going to be shared. Also, remember of removing the files from the workspace.\n")
    print("The cost for storing files in Simple Storage Service is quite inferior than the one for storing directly in SageMaker workspace. Also, files stored in S3 may be accessed for other users than those with access the notebook\'s workspace.\n")

    # Check if the user actually provided the mandatory inputs, instead
    # of putting None or empty string:
    if ((ACCESS_KEY is None) | (ACCESS_KEY == '')):
        print("AWS Access Key ID is missing. It is the value stored in the field \'Access key ID\' from your AWS user credentials CSV file.")
        return "error"
    elif ((SECRET_KEY is None) | (SECRET_KEY == '')):
        print("AWS Secret Access Key is missing. It is the value stored in the field \'Secret access key\' from your AWS user credentials CSV file.")
        return "error"
    elif ((s3_bucket_name is None) | (s3_bucket_name == '')):
        print ("Please, enter a valid S3 Bucket\'s name. Do not add sub-directories or folders (prefixes), only the name of the bucket itself.")
        return "error"
    
    else:
        # Use the str attribute to guarantee that all AWS parameters were properly read as strings, and not as
        # other variables (like integers or floats):
        ACCESS_KEY = str(ACCESS_KEY)
        SECRET_KEY = str(SECRET_KEY)
        s3_bucket_name = str(s3_bucket_name)

    if(s3_bucket_name[0] == "/"):
        # the first character is the slash. Let's remove it

        # In AWS, neither the prefix nor the path to which the file will be imported
        # (file from S3 to workspace) or from which the file will be exported to S3
        # (the path in the notebook's workspace) may start with slash, or the operation
        # will not be concluded. Then, we have to remove this character if it is present.

        # So, slice the whole string, starting from character 1 (as did for 
        # path_to_store_imported_s3_bucket):
        s3_bucket_name = s3_bucket_name[1:]

    # Remove any possible trailing (white and tab spaces) spaces
    # That may be present in the string. Use the Python string
    # rstrip method, which is the equivalent to the Trim function:
    # When no arguments are provided, the whitespaces and tabulations
    # are the removed characters
    # https://www.w3schools.com/python/ref_string_rstrip.asp?msclkid=ee2d05c3c56811ecb1d2189d9f803f65
    s3_bucket_name = s3_bucket_name.rstrip()
    ACCESS_KEY = ACCESS_KEY.rstrip()
    SECRET_KEY = SECRET_KEY.rstrip()
    # Since the user manually inputs the parameters ACCESS and SECRET_KEY,
    # it is easy to input whitespaces without noticing that.

    # Now process the non-obbligatory parameter.
    # Check if a prefix was passed as input parameter. If so, we must select only the names that start with
    # The prefix.
    # Example: in the bucket 'my_bucket' we have a directory 'dir1'.
    # In the main (root) directory, we have a file 'file1.json' like: '/file1.json'
    # If we pass the prefix 'dir1', we want only the files that start as '/dir1/'
    # such as: 'dir1/file2.json', excluding the file in the main (root) directory and excluding the files in other
    # directories. Also, we want to eliminate the file names with no extensions, like 'dir1/' or 'dir1/dir2',
    # since these object names represent folders or directories, not files.	

    if (s3_obj_prefix is None):
        print ("No prefix, specific object, or subdirectory provided.") 
        print (f"Then, exporting to \'{s3_bucket_name}\' root (main) directory.\n")
        # s3_path: path that the file should have in S3:
        s3_path = "" # empty string for the root directory
    elif ((s3_obj_prefix == "/") | (s3_obj_prefix == '')):
        # The root directory in the bucket must not be specified starting with the slash
        # If the root "/" or the empty string '' is provided, make
        # it equivalent to None (no directory)
        print ("No prefix, specific object, or subdirectory provided.") 
        print (f"Then, exporting to \'{s3_bucket_name}\' root (main) directory.\n")
        # s3_path: path that the file should have in S3:
        s3_path = "" # empty string for the root directory
    
    else:
        # Since there is a prefix, use the str attribute to guarantee that the path was read as a string:
        s3_obj_prefix = str(s3_obj_prefix)
            
        if(s3_obj_prefix[0] == "/"):
            # the first character is the slash. Let's remove it

            # In AWS, neither the prefix nor the path to which the file will be imported
            # (file from S3 to workspace) or from which the file will be exported to S3
            # (the path in the notebook's workspace) may start with slash, or the operation
            # will not be concluded. Then, we have to remove this character if it is present.

            # So, slice the whole string, starting from character 1 (as did for 
            # path_to_store_imported_s3_bucket):
            s3_obj_prefix = s3_obj_prefix[1:]

        # Remove any possible trailing (white and tab spaces) spaces
        # That may be present in the string. Use the Python string
        # rstrip method, which is the equivalent to the Trim function:
        s3_obj_prefix = s3_obj_prefix.rstrip()
            
        # s3_path: path that the file should have in S3:
        # Make the path the prefix itself, since there is a prefix:
        s3_path = s3_obj_prefix
            
        print("AWS Access Credentials, and bucket\'s prefix, object or subdirectory provided.\n")	

            
        print ("Starting connection with the S3 bucket.\n")
        
        try:
            # Start S3 client as the object 's3_client'
            s3_client = boto3.resource('s3', aws_access_key_id = ACCESS_KEY, aws_secret_access_key = SECRET_KEY)
        
            print(f"Credentials accepted by AWS. S3 client successfully started.\n")
            # An object 'data_table.xlsx' in the main (root) directory of the s3_bucket is stored in Python environment as:
            # s3.ObjectSummary(bucket_name='bucket_name', key='data_table.xlsx')
            # The name of each object is stored as the attribute 'key' of the object.
        
        except:
            
            print("Failed to connect to AWS Simple Storage Service (S3). Review if your credentials are correct.")
            print("The variable \'access_key\' must be set as the value (string) stored as \'Access key ID\' in your user security credentials CSV file.")
            print("The variable \'secret_key\' must be set as the value (string) stored as \'Secret access key\' in your user security credentials CSV file.")
        
        
        try:
            # Connect to the bucket specified as 'bucket_name'.
            # The bucket is started as the object 's3_bucket':
            s3_bucket = s3_client.Bucket(s3_bucket_name)
            print(f"Connection with bucket \'{s3_bucket_name}\' stablished.\n")
            
        except:
            
            print("Failed to connect with the bucket, which usually happens when declaring a wrong bucket\'s name.") 
            print("Check the spelling of your bucket_name string and remember that it must be all in lower-case.\n")
                
        # Now, let's obtain the lists of all file paths in the notebook's workspace and
        # of the paths that the files should have in S3, after being exported.
        
        try:
            
            # start the lists:
            workspace_full_paths = []
            s3_full_paths = []
            
            # Get the total of files in list_of_file_names_with_extensions:
            total_of_files = len(list_of_file_names_with_extensions)
            
            # And Loop through all elements, named 'my_file' from the list
            for my_file in list_of_file_names_with_extensions:
                
                # Get the full path in the notebook's workspace:
                workspace_file_full_path = os.path.join(directory_of_notebook_workspace_storing_files_to_export, my_file)
                # Get the full path that the file will have in S3:
                s3_file_full_path = os.path.join(s3_path, my_file)
                
                # Append these paths to the correspondent lists:
                workspace_full_paths.append(workspace_file_full_path)
                s3_full_paths.append(s3_file_full_path)
                
            # Now, both lists have the same number of elements. For an element (file) i,
            # workspace_full_paths has the full file path in notebook's workspace, and
            # s3_full_paths has the path that the new file should have in S3 bucket.
        
        except:
            
            print("The function returned an error when trying to access the list of files. Declare it as a list of strings, even if there is a single element in the list.")
            print("Example: list_of_file_names_with_extensions = [\'my_file.ext\']\n")
            return "error"
        
        
        # Now, loop through all elements i from the lists.
        # The first elements of the lists have index 0; the last elements have index
        # total_of_files - 1, since there are 'total_of_files' elements:
        
        # Then, export the correspondent element to S3:
        
        try:
            
            for i in range(total_of_files):
                # goes from i = 0 to i = total_of_files - 1

                # get the element from list workspace_file_full_path 
                # (original path of file i, from which it will be exported):
                PATH_IN_WORKSPACE = workspace_full_paths[i]

                # get the correspondent element of list s3_full_paths
                # (path that the file i should have in S3, after being exported):
                S3_FILE_PATH = s3_full_paths[i]

                # Start the new object in the bucket previously started as 's3_bucket'.
                # Start it with the specified prefix, in S3_FILE_PATH:
                new_s3_object = s3_bucket.Object(S3_FILE_PATH)
                
                # Finally, upload the file in PATH_IN_WORKSPACE.
                # Make new_s3_object the exported file:
            
                # Upload the selected object from the workspace path PATH_IN_WORKSPACE
                # to the S3 path specified as S3_FILE_PATH.
                # The parameter Filename must be input with the path of the copied file, including its name and
                # extension. Example Filename = "/my_table.xlsx" exports a xlsx file named 'my_table' to the notebook's main (root)
                # directory
                new_s3_object.upload_file(Filename = PATH_IN_WORKSPACE)

                print(f"The file \'{list_of_file_names_with_extensions[i]}\' was successfully exported from notebook\'s workspace to AWS Simple Storage Service (S3).\n")

                
            print("Finished exporting the files from the the notebook\'s workspace to S3 bucket. It may take a couple of minutes untill they be shown in S3 environment.\n") 
            print("Do not forget to delete these copies after finishing the analysis. They will remain stored in the bucket.\n")


        except:

            # Run this code for any other exception that may happen (no exception error
            # specified, so any exception runs the following code).
            # Check: https://pythonbasics.org/try-except/?msclkid=4f6b4540c5d011ecb1fe8a4566f632a6
            # for seeing how to handle successive exceptions

            print("Attention! The function raised an exception error, which is probably due to the AWS Simple Storage Service (S3) permissions.")
            print("Before running again this function, check this quick guide for configuring the permission roles in AWS.\n")
            print("It is necessary to create an user with full access permissions to interact with S3 from SageMaker. To configure the User, go to the upper ribbon of AWS, click on Services, and select IAM – Identity and Access Management.")
            print("1. In IAM\'s lateral panel, search for \'Users\' in the group of Access Management.")
            print("2. Click on the \'Add users\' button.")
            print("3. Set an user name in the text box \'User name\'.")
            print("Attention: users and S3 buckets cannot be written in upper case. Also, selecting a name already used by an Amazon user or bucket will raise an error message.\n")
            print("4. In the field \'Select type of Access to AWS\'-\'Select type of AWS credentials\' select the option \'Access key - Programmatic access\'. After that, click on the button \'Next: Permissions\'.")
            print("5. In the field \'Set Permissions\', keep the \'Add user to a group\' button marked.")
            print("6. In the field \'Add user to a group\', click on \'Create group\' (alternatively, you can be added to a group already configured or copy the permissions of another user.")
            print("7. In the text box \'Group\'s name\', set a name for the new group of permissions.")
            print("8. In the search bar below (\'Filter politics\'), search for a politics that fill your needs, and check the option button on the left of this politic. The politics \'AmazonS3FullAccess\' grants full access to the S3 content.")
            print("9. Finally, click on \'Create a group\'.")
            print("10. After the group is created, it will appear with a check box marked, over the previous groups. Keep it marked and click on the button \'Next: Tags\'.")
            print("11. Create and note down the Access key ID and Secret access key. You can also download a comma separated values (CSV) file containing the credentials for future use.")
            print("ATTENTION: These parameters are required for accessing the bucket\'s content from any application, including AWS SageMaker.")
            print("12. Click on \'Next: Review\' and review the user credentials information and permissions.")
            print("13. Click on \'Create user\' and click on the download button to download the CSV file containing the user credentials information.")
            print("The headers of the CSV file (the stored fields) is: \'User name, Password, Access key ID, Secret access key, Console login link\'.")
            print("You need both the values indicated as \'Access key ID\' and as \'Secret access key\' to fetch the S3 bucket.")
            print("\n") # line break
            print("After acquiring the necessary user privileges, use the boto3 library to export the file from the notebook’s workspace to the bucket (i.e., to upload a file to the bucket).")
            print("For exporting the file as a new bucket\'s file use the following code:\n")
            print("1. Set a variable \'access_key\' as the value (string) stored as \'Access key ID\' in your user security credentials CSV file.")
            print("2. Set a variable \'secret_key\' as the value (string) stored as \'Secret access key\' in your user security credentials CSV file.")
            print("3. Set a variable \'bucket_name\' as a string containing only the name of the bucket. Do not add subdirectories, folders (prefixes), or file names.")
            print("Example: if your bucket is named \'my_bucket\' and its main directory contains folders like \'folder1\', \'folder2\', etc, do not declare bucket_name = \'my_bucket/folder1\', even if you only want files from folder1.")
            print("ALWAYS declare only the bucket\'s name: bucket_name = \'my_bucket\'.")
            print("4. Set a variable \'file_path_in_workspace\' containing the path of the file in notebook’s workspace. The file will be exported from “file_path_in_workspace” to the S3 bucket.")
            print("If the file is stored in the notebook\'s root (main) directory: file_path = \"my_file.ext\".")
            print("If the path of the file in the notebook workspace is: \'dir1/…/dirN/my_file.ext\', where dirN is the N-th subdirectory, and dir1 is a folder or directory of the main (root) bucket\'s directory: file_path = \"dir1/…/dirN/my_file.ext\".")
            print("5. Set a variable named \'file_path_in_s3\' containing the path from the bucket’s subdirectories to the file you want to fetch. Include the file name and its extension.")
            print("6. Finally, declare the following code, which refers to the defined variables:\n")

            # Let's use triple quotes to declare a formated string
            example_code = """
                import boto3
                # Start S3 client as the object 's3_client'
                s3_client = boto3.resource('s3', aws_access_key_id = access_key, aws_secret_access_key = secret_key)
                # Connect to the bucket specified as 'bucket_name'.
                # The bucket is started as the object 's3_bucket':
                s3_bucket = s3_client.Bucket(bucket_name)
                # Start the new object in the bucket previously started as 's3_bucket'.
                # Start it with the specified prefix, in file_path_in_s3:
                new_s3_object = s3_bucket.Object(file_path_in_s3)
                # Finally, upload the file in file_path_in_workspace.
                # Make new_s3_object the exported file:
                # Upload the selected object from the workspace path file_path_in_workspace
                # to the S3 path specified as file_path_in_s3.
                # The parameter Filename must be input with the path of the copied file, including its name and
                # extension. Example Filename = "/my_table.xlsx" exports a xlsx file named 'my_table' to 
                # the notebook's main (root) directory.
                new_s3_object.upload_file(Filename = file_path_in_workspace)
                """

            print(example_code)

            print("An object \'my_file.ext\' in the main (root) directory of the s3_bucket is stored in Python environment as:")
            print("""s3.ObjectSummary(bucket_name='bucket_name', key='my_file.ext'""") 
            # triple quotes to keep the internal quotes without using too much backslashes "\" (the ignore next character)
            print("Then, the name of each object is stored as the attribute \'key\' of the object. To view all objects, we can loop through their \'key\' attributes:\n")
            example_code = """
                # Loop through all objects of the bucket:
                for stored_obj in s3_bucket.objects.all():		
                    # Loop through all elements 'stored_obj' from s3_bucket.objects.all()
                    # Which stores the ObjectSummary for all objects in the bucket s3_bucket:
                    # Print the object’s names:
                    print(stored_obj.key)
                    """

            print(example_code)


def load_pandas_dataframe (file_directory_path, file_name_with_extension, load_txt_file_with_json_format = False, how_missing_values_are_registered = None, has_header = True, decimal_separator = '.', txt_csv_col_sep = "comma", sheet_to_load = None, json_record_path = None, json_field_separator = "_", json_metadata_prefix_list = None):
    
    # Pandas documentation:
    # pd.read_csv: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
    # pd.read_excel: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html
    # pd.json_normalize: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.json_normalize.html
    # Python JSON documentation:
    # https://docs.python.org/3/library/json.html
    
    import os
    import json
    import numpy as np
    import pandas as pd
    from pandas import json_normalize
    
    ## WARNING: Use this function to load dataframes stored on Excel (xls, xlsx, xlsm, xlsb, odf, ods and odt), 
    ## JSON, txt, or CSV (comma separated values) files.
    
    # file_directory_path - (string, in quotes): input the path of the directory (e.g. folder path) 
    # where the file is stored. e.g. file_directory_path = "/" or file_directory_path = "/folder"
    
    # FILE_NAME_WITH_EXTENSION - (string, in quotes): input the name of the file with the 
    # extension. e.g. FILE_NAME_WITH_EXTENSION = "file.xlsx", or, 
    # FILE_NAME_WITH_EXTENSION = "file.csv", "file.txt", or "file.json"
    # Again, the extensions may be: xls, xlsx, xlsm, xlsb, odf, ods, odt, json, txt or csv.
    
    # load_txt_file_with_json_format = False. Set load_txt_file_with_json_format = True 
    # if you want to read a file with txt extension containing a text formatted as JSON 
    # (but not saved as JSON).
    # WARNING: if load_txt_file_with_json_format = True, all the JSON file parameters of the 
    # function (below) must be set. If not, an error message will be raised.
    
    # HOW_MISSING_VALUES_ARE_REGISTERED = None: keep it None if missing values are registered as None,
    # empty or np.nan. Pandas automatically converts None to NumPy np.nan objects (floats).
    # This parameter manipulates the argument na_values (default: None) from Pandas functions.
    # By default the following values are interpreted as NaN: ‘’, ‘#N/A’, ‘#N/A N/A’, ‘#NA’, ‘-1.#IND’, 
    #‘-1.#QNAN’, ‘-NaN’, ‘-nan’, ‘1.#IND’, ‘1.#QNAN’, ‘<NA>’, ‘N/A’, ‘NA’, ‘NULL’, ‘NaN’, 
    # ‘n/a’, ‘nan’, ‘null’.

    # If a different denomination is used, indicate it as a string. e.g.
    # HOW_MISSING_VALUES_ARE_REGISTERED = '.' will convert all strings '.' to missing values;
    # HOW_MISSING_VALUES_ARE_REGISTERED = 0 will convert zeros to missing values.

    # If dict passed, specific per-column NA values. For example, if zero is the missing value
    # only in column 'numeric_col', you can specify the following dictionary:
    # how_missing_values_are_registered = {'numeric-col': 0}
    
    
    # has_header = True if the the imported table has headers (row with columns names).
    # Alternatively, has_header = False if the dataframe does not have header.
    
    # DECIMAL_SEPARATOR = '.' - String. Keep it '.' or None to use the period ('.') as
    # the decimal separator. Alternatively, specify here the separator.
    # e.g. DECIMAL_SEPARATOR = ',' will set the comma as the separator.
    # It manipulates the argument 'decimal' from Pandas functions.
    
    # txt_csv_col_sep = "comma" - This parameter has effect only when the file is a 'txt'
    # or 'csv'. It informs how the different columns are separated.
    # Alternatively, txt_csv_col_sep = "comma", or txt_csv_col_sep = "," 
    # for columns separated by comma;
    # txt_csv_col_sep = "whitespace", or txt_csv_col_sep = " " 
    # for columns separated by simple spaces.
    # You can also set a specific separator as string. For example:
    # txt_csv_col_sep = '\s+'; or txt_csv_col_sep = '\t' (in this last example, the tabulation
    # is used as separator for the columns - '\t' represents the tab character).
    
    # sheet_to_load - This parameter has effect only when for Excel files.
    # keep sheet_to_load = None not to specify a sheet of the file, so that the first sheet
    # will be loaded.
    # sheet_to_load may be an integer or an string (inside quotes). sheet_to_load = 0
    # loads the first sheet (sheet with index 0); sheet_to_load = 1 loads the second sheet
    # of the file (index 1); sheet_to_load = "Sheet1" loads a sheet named as "Sheet1".
    # Declare a number to load the sheet with that index, starting from 0; or declare a
    # name to load the sheet with that name.
    
    ## Parameters for loading JSON files:
    
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
    
    # json_metadata_prefix_list: list of strings (in quotes). Manipulates the parameter 
    # 'meta' from json_normalize method. Fields to use as metadata for each record in resulting 
    # table. Declare here the non-nested fields, i.e., the fields in the principal JSON. They
    # will be repeated in the rows of the dataframe to give the metadata (context) of the rows.
    
    # e.g. Suppose a JSON with the following structure: {'name': 'Mary', 'last': 'Shelley',
    # 'books': [{'title': 'Frankestein', 'year': 1818}, {'title': 'Mathilda ', 'year': 1819},{'title': 'The Last Man', 'year': 1826}]},
    # Here, there are nested JSONs in the field 'books'. The fields that are not nested
    # are 'name' and 'last'.
    # Then, json_record_path = 'books'
    # json_metadata_prefix_list = ['name', 'last']
    
    
    # Create the complete file path:
    file_path = os.path.join(file_directory_path, file_name_with_extension)
    # Extract the file extension
    file_extension = os.path.splitext(file_path)[1][1:]
    # os.path.splitext(file_path) is a tuple of strings: the first is the complete file
    # root with no extension; the second is the extension starting with a point: '.txt'
    # When we set os.path.splitext(file_path)[1], we are selecting the second element of
    # the tuple. By selecting os.path.splitext(file_path)[1][1:], we are taking this string
    # from the second character (index 1), eliminating the dot: 'txt'
    
    # Check if the decimal separator is None. If it is, set it as '.' (period):
    if (decimal_separator is None):
        decimal_separator = '.'
    
    if ((file_extension == 'txt') | (file_extension == 'csv')): 
        # The operator & is equivalent to 'And' (intersection).
        # The operator | is equivalent to 'Or' (union).
        # pandas.read_csv method must be used.
        if (load_txt_file_with_json_format == True):
            
            print("Reading a txt file containing JSON parsed data. A reading error will be raised if you did not set the JSON parameters.")
            
            with open(file_path, 'r') as opened_file:
                # 'r' stands for read mode; 'w' stands for write mode
                # read the whole file as a string named 'file_full_text'
                file_full_text = opened_file.read()
                # if we used the readlines() method, we would be reading the
                # file by line, not the whole text at once.
                # https://stackoverflow.com/questions/8369219/how-to-read-a-text-file-into-a-string-variable-and-strip-newlines?msclkid=a772c37bbfe811ec9a314e3629df4e1e
                # https://www.tutorialkart.com/python/python-read-file-as-string/#:~:text=example.py%20%E2%80%93%20Python%20Program.%20%23open%20text%20file%20in,and%20prints%20it%20to%20the%20standard%20output.%20Output.?msclkid=a7723a1abfe811ecb68bba01a2b85bd8
                
            #Now, file_full_text is a string containing the full content of the txt file.
            json_file = json.loads(file_full_text)
            # json.load() : This method is used to parse JSON from URL or file.
            # json.loads(): This method is used to parse string with JSON content.
            # e.g. .json.loads() must be used to read a string with JSON and convert it to a flat file
            # like a dataframe.
            # check: https://www.pythonpip.com/python-tutorials/how-to-load-json-file-using-python/#:~:text=The%20json.load%20%28%29%20is%20used%20to%20read%20the,and%20alter%20data%20in%20our%20application%20or%20system.
            dataset = json_normalize(json_file, record_path = json_record_path, sep = json_field_separator, meta = json_metadata_prefix_list)
        
        else:
            # Not a JSON txt
        
            if (has_header == True):

                if ((txt_csv_col_sep == "comma") | (txt_csv_col_sep == ",")):

                    dataset = pd.read_csv(file_path, na_values = how_missing_values_are_registered, verbose = True, parse_dates = True, infer_datetime_format = True, decimal = decimal_separator)
                    # verbose = True for showing number of NA values placed in non-numeric columns.
                    #  parse_dates = True: try parsing the index; infer_datetime_format = True : If True and parse_dates is enabled, pandas will attempt to infer the format of the datetime strings in 
                    # the columns, and if it can be inferred, switch to a faster method of parsing them. In some cases this can increase the 
                    # parsing speed by 5-10x.

                elif ((txt_csv_col_sep == "whitespace") | (txt_csv_col_sep == " ")):

                    dataset = pd.read_csv(file_path, delim_whitespace = True, na_values = how_missing_values_are_registered, verbose = True, parse_dates = True, infer_datetime_format = True, decimal = decimal_separator)
                    
                    
                else:
                    
                    try:
                        
                        # Try using the character specified as the argument txt_csv_col_sep:
                        dataset = pd.read_csv(file_path, sep = txt_csv_col_sep, na_values = how_missing_values_are_registered, verbose = True, parse_dates = True, infer_datetime_format = True, decimal = decimal_separator)
                    
                    except:
                        # An error was raised, the separator is not valid
                        print(f"Enter a valid column separator for the {file_extension} file, like: \'comma\' or \'whitespace\'.")


            else:
                # has_header == False

                if ((txt_csv_col_sep == "comma") | (txt_csv_col_sep == ",")):

                    dataset = pd.read_csv(file_path, header = None, na_values = how_missing_values_are_registered, verbose = True, parse_dates = True, infer_datetime_format = True, decimal = decimal_separator)

                    
                elif ((txt_csv_col_sep == "whitespace") | (txt_csv_col_sep == " ")):

                    dataset = pd.read_csv(file_path, delim_whitespace = True, header = None, na_values = how_missing_values_are_registered, verbose = True, parse_dates = True, infer_datetime_format = True, decimal = decimal_separator)
                    
                    
                else:
                    
                    try:
                        
                        # Try using the character specified as the argument txt_csv_col_sep:
                        dataset = pd.read_csv(file_path, sep = txt_csv_col_sep, header = None, na_values = how_missing_values_are_registered, verbose = True, parse_dates = True, infer_datetime_format = True, decimal = decimal_separator)
                    
                    except:
                        # An error was raised, the separator is not valid
                        print(f"Enter a valid column separator for the {file_extension} file, like: \'comma\' or \'whitespace\'.")

    elif (file_extension == 'json'):
        
        with open(file_path, 'r') as opened_file:
            
            json_file = json.load(opened_file)
            # The structure json_file = json.load(open(file_path)) relies on the GC to close the file. That's not a 
            # good idea: If someone doesn't use CPython the garbage collector might not be using refcounting (which 
            # collects unreferenced objects immediately) but e.g. collect garbage only after some time.
            # Since file handles are closed when the associated object is garbage collected or closed 
            # explicitly (.close() or .__exit__() from a context manager) the file will remain open until 
            # the GC kicks in.
            # Using 'with' ensures the file is closed as soon as the block is left - even if an exception 
            # happens inside that block, so it should always be preferred for any real application.
            # source: https://stackoverflow.com/questions/39447362/equivalent-ways-to-json-load-a-file-in-python
            
        # json.load() : This method is used to parse JSON from URL or file.
        # json.loads(): This method is used to parse string with JSON content.
        # Then, json.load for a .json file
        # and json.loads for text file containing json
        # check: https://www.pythonpip.com/python-tutorials/how-to-load-json-file-using-python/#:~:text=The%20json.load%20%28%29%20is%20used%20to%20read%20the,and%20alter%20data%20in%20our%20application%20or%20system.   
        dataset = json_normalize(json_file, record_path = json_record_path, sep = json_field_separator, meta = json_metadata_prefix_list)
    
    else:
        # If it is not neither a csv nor a txt file, let's assume it is one of different
        # possible Excel files.
        print("Excel file inferred. If an error message is shown, check if a valid file extension was used: \'xlsx\', \'xls\', etc.")
        # For Excel type files, Pandas automatically detects the decimal separator and requires only the parameter parse_dates.
        # Firstly, the argument infer_datetime_format was present on read_excel function, but was removed.
        # From version 1.4 (beta, in 10 May 2022), it will be possible to pass the parameter 'decimal' to
        # read_excel function for detecting decimal cases in strings. For numeric variables, it is not needed, though
        
        if (sheet_to_load is not None):        
        #Case where the user specifies which sheet of the Excel file should be loaded.
            
            if (has_header == True):
                
                dataset = pd.read_excel(file_path, sheet_name = sheet_to_load, na_values = how_missing_values_are_registered, verbose = True, parse_dates = True)
                # verbose = True for showing number of NA values placed in non-numeric columns.
                #  parse_dates = True: try parsing the index; infer_datetime_format = True : If True and parse_dates is enabled, pandas will attempt to infer the format of the datetime strings in 
                # the columns, and if it can be inferred, switch to a faster method of parsing them. In some cases this can increase the 
                # parsing speed by 5-10x.
                
            else:
                #No header
                dataset = pd.read_excel(file_path, sheet_name = sheet_to_load, header = None, na_values = how_missing_values_are_registered, verbose = True, parse_dates = True)
                
        else:
            #No sheet specified
            if (has_header == True):
                
                dataset = pd.read_excel(file_path, na_values = how_missing_values_are_registered, verbose = True, parse_dates = True)
                
            else:
                #No header
                dataset = pd.read_excel(file_path, header = None, na_values = how_missing_values_are_registered, verbose = True, parse_dates = True)
                
    print(f"Dataset extracted from {file_path}. Check the 10 first rows of this dataframe:\n")
    print(dataset.head(10))
    
    return dataset


def json_obj_to_pandas_dataframe (json_obj_to_convert, json_obj_type = 'list', json_record_path = None, json_field_separator = "_", json_metadata_prefix_list = None):
    
    import json
    import pandas as pd
    from pandas import json_normalize
    
    # JSON object in terms of Python structure: list of dictionaries, where each value of a
    # dictionary may be a dictionary or a list of dictionaries (nested structures).
    # example of highly nested structure saved as a list 'json_formatted_list'. Note that the same
    # structure could be declared and stored into a string variable. For instance, if you have a txt
    # file containing JSON, you could read the txt and save its content as a string.
    # json_formatted_list = [{'field1': val1, 'field2': {'dict_val': dict_val}, 'field3': [{
    # 'nest1': nest_val1}, {'nest2': nestval2}]}, {'field1': val1, 'field2': {'dict_val': dict_val}, 
    # 'field3': [{'nest1': nest_val1}, {'nest2': nestval2}]}]    

    # json_obj_type = 'list', in case the object was saved as a list of dictionaries (JSON format)
    # json_obj_type = 'string', in case it was saved as a string (text) containing JSON.

    # json_obj_to_convert: object containing JSON, or string with JSON content to parse.
    # Objects may be: string with JSON formatted text;
    # list with nested dictionaries (JSON formatted);
    # dictionaries, possibly with nested dictionaries (JSON formatted).
    
    # https://docs.python.org/3/library/json.html
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
    
    # json_metadata_prefix_list: list of strings (in quotes). Manipulates the parameter 
    # 'meta' from json_normalize method. Fields to use as metadata for each record in resulting 
    # table. Declare here the non-nested fields, i.e., the fields in the principal JSON. They
    # will be repeated in the rows of the dataframe to give the metadata (context) of the rows.
    
    # e.g. Suppose a JSON with the following structure: {'name': 'Mary', 'last': 'Shelley',
    # 'books': [{'title': 'Frankestein', 'year': 1818}, {'title': 'Mathilda ', 'year': 1819},{'title': 'The Last Man', 'year': 1826}]},
    # Here, there are nested JSONs in the field 'books'. The fields that are not nested
    # are 'name' and 'last'.
    # Then, json_record_path = 'books'
    # json_metadata_prefix_list = ['name', 'last']

    
    if (json_obj_type == 'string'):
        # Use the json.loads method to convert the string to json
        json_file = json.loads(json_obj_to_convert)
        # json.load() : This method is used to parse JSON from URL or file.
        # json.loads(): This method is used to parse string with JSON content.
        # e.g. .json.loads() must be used to read a string with JSON and convert it to a flat file
        # like a dataframe.
        # check: https://www.pythonpip.com/python-tutorials/how-to-load-json-file-using-python/#:~:text=The%20json.load%20%28%29%20is%20used%20to%20read%20the,and%20alter%20data%20in%20our%20application%20or%20system.
    
    elif (json_obj_type == 'list'):
        
        # make the json_file the object itself:
        json_file = json_obj_to_convert
    
    else:
        print ("Enter a valid JSON object type: \'list\', in case the JSON object is a list of dictionaries in JSON format; or \'string\', if the JSON is stored as a text (string variable).")
        return "error"
    
    dataset = json_normalize(json_file, record_path = json_record_path, sep = json_field_separator, meta = json_metadata_prefix_list)
    
    print(f"JSON object {json_obj_to_convert} converted to a flat dataframe object. Check the 10 first rows of this dataframe:\n")
    print(dataset.head(10))
    
    return dataset


def export_pd_dataframe_as_csv (dataframe_obj_to_be_exported, new_file_name_without_extension, file_directory_path = None):
    
    import os
    import pandas as pd
    
    ## WARNING: all files exported from this function are .csv (comma separated values)
    
    # dataframe_obj_to_be_exported: dataframe object that is going to be exported from the
    # function. Since it is an object (not a string), it should not be declared in quotes.
    # example: dataframe_obj_to_be_exported = dataset will export the dataset object.
    # ATTENTION: The dataframe object must be a Pandas dataframe.
    
    # FILE_DIRECTORY_PATH - (string, in quotes): input the path of the directory 
    # (e.g. folder path) where the file is stored. e.g. FILE_DIRECTORY_PATH = "/" 
    # or FILE_DIRECTORY_PATH = "/folder"
    # If you want to export the file to AWS S3, this parameter will have no effect.
    # In this case, you can set FILE_DIRECTORY_PATH = None

    # new_file_name_without_extension - (string, in quotes): input the name of the 
    # file without the extension. e.g. new_file_name_without_extension = "my_file" 
    # will export a file 'my_file.csv' to notebook's workspace.
    
    # Create the complete file path:
    file_path = os.path.join(file_directory_path, new_file_name_without_extension)
    # Concatenate the extension ".csv":
    file_path = file_path + ".csv"

    dataframe_obj_to_be_exported.to_csv(file_path, index = False)

    print(f"Dataframe {new_file_name_without_extension} exported as CSV file to notebook\'s workspace as \'{file_path}\'.")
    print("Warning: if there was a file in this file path, it was replaced by the exported dataframe.")


def MERGE_ON_TIMESTAMP (df_left, df_right, left_key, right_key, how_to_join = "inner", merge_method = 'asof', merged_suffixes = ('_left', '_right'), asof_direction = 'nearest', ordered_filling = 'ffill'):
    
    #WARNING: Only two dataframes can be merged on each call of the function.
    
    import numpy as np
    import pandas as pd
    
    # df_left: dataframe to be joined as the left one.
    
    # df_right: dataframe to be joined as the right one
    
    # left_key: (String) name of column of the left dataframe to be used as key for joining.
    
    # right_key: (String) name of column of the right dataframe to be used as key for joining.
    
    # how_to_join: joining method: "inner", "outer", "left", "right". The default is "inner".
    
    # merge_method: which pandas merging method will be applied:
    # merge_method = 'ordered' for using the .merge_ordered method.
    # merge_method = "asof" for using the .merge_asof method.
    # WARNING: .merge_asof uses fuzzy matching, so the how_to_join parameter is not applicable.
    
    # merged_suffixes = ('_left', '_right') - tuple of the suffixes to be added to columns
    # with equal names. Simply modify the strings inside quotes to modify the standard
    # values. If no tuple is provided, the standard denomination will be used.
    
    # asof_direction: this parameter will only be used if the .merge_asof method is
    # selected. The default is 'nearest' to merge the closest timestamps in both 
    # directions. The other options are: 'backward' or 'forward'.
    
    # ordered_filling: this parameter will only be used on the merge_ordered method.
    # The default is None. Input ordered_filling = 'ffill' to fill missings with the
    # previous value.
    
    # Create dataframe local copies to manipulate, avoiding that Pandas operates on
    # the original objects; or that Pandas tries to set values on slices or copies,
    # resulting in unpredictable results.
    # Use the copy method to effectively create a second object with the same properties
    # of the input parameters, but completely independent from it.
    DF_LEFT = df_left.copy(deep = True)
    DF_RIGHT = df_right.copy(deep = True)
    
    # Firstly, let's guarantee that the keys were actually read as timestamps of the same type.
    # We will do that by converting all values to Pandas timestamps.
    
    # 1. Start lists to store the Pandas timestamps:
    timestamp_list_left = []
    timestamp_list_right = []
    
    # 2. Loop through each element of the timestamp columns left_key and right_key, 
    # and apply the function to guarantee that all elements are Pandas timestamps
    
    # left dataframe:
    for timestamp in DF_LEFT[left_key]:
        #Access each element 'timestamp' of the series df[timestamp_tag_column]
        timestamp_list_left.append(pd.Timestamp(timestamp, unit = 'ns'))
    
    # right dataframe:
    for timestamp in DF_RIGHT[right_key]:
        #Access each element 'timestamp' of the series df[timestamp_tag_column]
        timestamp_list_right.append(pd.Timestamp(timestamp, unit = 'ns'))
    
    # 3. Set the key columns as the lists of objects converted to Pandas dataframes:
    DF_LEFT[left_key] = timestamp_list_left
    DF_RIGHT[right_key] = timestamp_list_right
    
    # Now, even if the dates were read as different types of variables (like string for one
    # and datetime for the other), we converted them to a same type (Pandas timestamp), avoiding
    # compatibility issues.
    
    # For performing merge 'asof', the timestamps must be previously sorted in ascending order.
    # Pandas sort_values method: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html
    # Let's sort the dataframes in ascending order of timestamps before merging:
    
    DF_LEFT = DF_LEFT.sort_values(by = left_key, ascending = True)
    DF_RIGHT = DF_RIGHT.sort_values(by = right_key, ascending = True)
    
    # Reset indices:
    DF_LEFT = DF_LEFT.reset_index(drop = True)
    DF_RIGHT = DF_RIGHT.reset_index(drop = True)
        
    
    if (merge_method == 'ordered'):
    
        if (ordered_filling == 'ffill'):
            
            merged_df = pd.merge_ordered(DF_LEFT, DF_RIGHT, left_on = left_key, right_on = right_key, how = how_to_join, suffixes = merged_suffixes, fill_method='ffill')
        
        else:
            
            merged_df = pd.merge_ordered(DF_LEFT, DF_RIGHT, left_on = left_key, right_on = right_key, how = how_to_join, suffixes = merged_suffixes)
    
    elif (merge_method == 'asof'):
        
        merged_df = pd.merge_asof(DF_LEFT, DF_RIGHT, left_on = left_key, right_on = right_key, suffixes = merged_suffixes, direction = asof_direction)
    
    else:
        
        print("You did not enter a valid merge method for this function, \'ordered\' or \'asof\'.")
        print("Then, applying the conventional Pandas .merge method, followed by .sort_values method.")
        
        #Pandas sort_values method: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html
        
        merged_df = DF_LEFT.merge(DF_RIGHT, left_on = left_key, right_on = right_key, how = how_to_join, suffixes = merged_suffixes)
        merged_df = merged_df.sort_values(by = merged_df.columns[0], ascending = True)
        #sort by the first column, with index 0.
    
    # Now, reset index positions of the merged dataframe:
    merged_df = merged_df.reset_index(drop = True)
    
    # Pandas .head(Y) method results in a dataframe containing the first Y rows of the 
    # original dataframe. The default .head() is Y = 5. Print first 10 rows of the 
    # new dataframe:
    print("Dataframe successfully merged. Check its 10 first rows:\n")
    print(merged_df.head(10))
    
    return merged_df


def MERGE_AND_SORT_DATAFRAMES (df_left, df_right, left_key, right_key, how_to_join = "inner", merged_suffixes = ('_left', '_right'), sort_merged_df = False, column_to_sort = None, ascending_sorting = True):
    
    #WARNING: Only two dataframes can be merged on each call of the function.
    
    import numpy as np
    import pandas as pd
    
    # df_left: dataframe to be joined as the left one.
    
    # df_right: dataframe to be joined as the right one
    
    # left_key: (String) name of column of the left dataframe to be used as key for joining.
    
    # right_key: (String) name of column of the right dataframe to be used as key for joining.
    
    # how_to_join: joining method: "inner", "outer", "left", "right". The default is "inner".
    
    # merge_method: which pandas merging method will be applied:
    # merge_method = 'ordered' for using the .merge_ordered method.
    # merge_method = "asof" for using the .merge_asof method.
    # WARNING: .merge_asof uses fuzzy matching, so the how_to_join parameter is not applicable.
    
    # merged_suffixes = ('_left', '_right') - tuple of the suffixes to be added to columns
    # with equal names. Simply modify the strings inside quotes to modify the standard
    # values. If no tuple is provided, the standard denomination will be used.
    
    # sort_merged_df = False not to sort the merged dataframe. If you want to sort it,
    # set as True. If sort_merged_df = True and column_to_sort = None, the dataframe will
    # be sorted by its first column.
    
    # column_to_sort = None. Keep it None if the dataframe should not be sorted.
    # Alternatively, pass a string with a column name to sort, such as:
    # column_to_sort = 'col1'; or a list of columns to use for sorting: column_to_sort = 
    # ['col1', 'col2']
    
    # ascending_sorting = True. If you want to sort the column(s) passed on column_to_sort in
    # ascending order, set as True. Set as False if you want to sort in descending order. If
    # you want to sort each column passed as list column_to_sort in a specific order, pass a 
    # list of booleans like ascending_sorting = [False, True] - the first column of the list
    # will be sorted in descending order, whereas the 2nd will be in ascending. Notice that
    # the correspondence is element-wise: the boolean in list ascending_sorting will correspond 
    # to the sorting order of the column with the same position in list column_to_sort.
    # If None, the dataframe will be sorted in ascending order.
    
    # Create dataframe local copies to manipulate, avoiding that Pandas operates on
    # the original objects; or that Pandas tries to set values on slices or copies,
    # resulting in unpredictable results.
    # Use the copy method to effectively create a second object with the same properties
    # of the input parameters, but completely independent from it.
    DF_LEFT = df_left.copy(deep = True)
    DF_RIGHT = df_right.copy(deep = True)
    
    # check if the keys are the same:
    boolean_check = (left_key == right_key)
    # if boolean_check is True, we will merge using the on parameter, instead of left_on and right_on:
    
    if (boolean_check): # runs if it is True:
        
        merged_df = DF_LEFT.merge(DF_RIGHT, on = left_key, how = how_to_join, suffixes = merged_suffixes)
    
    else:
        # use left_on and right_on
        merged_df = DF_LEFT.merge(DF_RIGHT, left_on = left_key, right_on = right_key, how = how_to_join, suffixes = merged_suffixes)
    
    # Check if the dataframe should be sorted:
    if (sort_merged_df == True):
        
        # check if column_to_sort = None. If it is, set it as the first column (index 0):
        if (column_to_sort is None):
            
            column_to_sort = merged_df.columns[0]
            print(f"Sorting merged dataframe by its first column = {column_to_sort}")
        
        # check if ascending_sorting is None. If it is, set it as True:
        if (ascending_sorting is None):
            
            ascending_sorting = True
            print("Sorting merged dataframe in ascending order.")
        
        # Now, sort the dataframe according to the parameters:
        merged_df = merged_df.sort_values(by = column_to_sort, ascending = ascending_sorting)
        #sort by the first column, with index 0.
    
        # Now, reset index positions:
        merged_df = merged_df.reset_index(drop = True)
        print("Merged dataframe successfully sorted.")
    
    # Pandas .head(Y) method results in a dataframe containing the first Y rows of the 
    # original dataframe. The default .head() is Y = 5. Print first 10 rows of the 
    # new dataframe:
    print("Dataframe successfully merged. Check its 10 first rows:\n")
    print(merged_df.head(10))
    
    return merged_df


def UNION_DATAFRAMES (list_of_dataframes, what_to_append = 'rows', ignore_index_on_union = True, sort_values_on_union = True, union_join_type = None):
    
    import pandas as pd
    #JOIN can be 'inner' to perform an inner join, eliminating the missing values
    #The default (None) is 'outer': the dataframes will be stacked on the columns with
    #same names but, in case there is no correspondence, the row will present a missing
    #value for the columns which are not present in one of the dataframes.
    #When using the 'inner' method, only the common columns will remain
    
    #list_of_dataframes must be a list containing the dataframe objects
    # example: list_of_dataframes = [df1, df2, df3, df4]
    #Notice that the dataframes are objects, not strings. Therefore, they should not
    # be declared inside quotes.
    # There is no limit of dataframes. In this example, we will concatenate 4 dataframes.
    # If list_of_dataframes = [df1, df2, df3] we would concatenate 3, and if
    # list_of_dataframes = [df1, df2, df3, df4, df5] we would concatenate 5 dataframes.
    
    # what_to_append = 'rows' for appending the rows from one dataframe
    # into the other; what_to_append = 'columns' for appending the columns
    # from one dataframe into the other (horizontal or lateral append).
    
    # When what_to_append = 'rows', Pandas .concat method is defined as
    # axis = 0, i.e., the operation occurs in the row level, so the rows
    # of the second dataframe are added to the bottom of the first one.
    # It is the SQL union, and creates a dataframe with more rows, and
    # total of columns equals to the total of columns of the first dataframe
    # plus the columns of the second one that were not in the first dataframe.
    # When what_to_append = 'columns', Pandas .concat method is defined as
    # axis = 1, i.e., the operation occurs in the column level: the two
    # dataframes are laterally merged using the index as the key, 
    # preserving all columns from both dataframes. Therefore, the number of
    # rows will be the total of rows of the dataframe with more entries,
    # and the total of columns will be the sum of the total of columns of
    # the first dataframe with the total of columns of the second dataframe.
    
    #The other parameters are the same from Pandas .concat method.
    # ignore_index_on_union = ignore_index;
    # sort_values_on_union = sort
    # union_join_type = join
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.concat.html
    
    #Check Datacamp course Joining Data with pandas, Chap.3, 
    # Advanced Merging and Concatenating
    
    # Create dataframe local copies to manipulate, avoiding that Pandas operates on
    # the original objects; or that Pandas tries to set values on slices or copies,
    # resulting in unpredictable results.
    # Use the copy method to effectively create a second object with the same properties
    # of the input parameters, but completely independent from it.
    
    # Start a list of copied dataframes:
    LIST_OF_DATAFRAMES = []
    
    # Loop through each element from list_of_dataframes:
    for dataframe in list_of_dataframes:
        
        # create a copy of the object:
        copied_df = dataframe.copy(deep = True)
        # Append this element to the LIST_OF_DATAFRAMES:
        LIST_OF_DATAFRAMES.append(copied_df)
    
    # Check axis:
    if (what_to_append == 'rows'):
        
        AXIS = 0
    
    elif (what_to_append == 'columns'):
        
        AXIS = 1
        
        # In this case, we must save a list of columns of each one of the dataframes, containing
        # the different column names observed. That is because the concat method eliminates the
        # original column names when AXIS = 1
        # We can start the LIST_OF_COLUMNS as the columns from the first object on the
        # LIST_OF_DATAFRAMES, eliminating one iteration cycle. Since the columns method generates
        # an array, we use the list attribute to convert the array to a regular list:
        
        i = 0
        analyzed_df = LIST_OF_DATAFRAMES[i]
        LIST_OF_COLUMNS = list(analyzed_df.columns)
        
        # Now, loop through each other element on LIST_OF_DATAFRAMES. Since index 0 was already
        # considered, start from index 1:
        for i in range (1, len(LIST_OF_DATAFRAMES)):
            
            analyzed_df = LIST_OF_DATAFRAMES[i]
            
            # Now, loop through each column, named 'col', from the list of columns of analyzed_df:
            for col in list(analyzed_df.columns):
                
                # If 'col' is not in LIST_OF_COLUMNS, append it to the list with its current name.
                # The order of the columns on the concatenated dataframe will be the same (the order
                # they appear):
                if not (col in LIST_OF_COLUMNS):
                    LIST_OF_COLUMNS.append(col)
                
                else:
                    # There is already a column with this name. So, append col with a suffix:
                    LIST_OF_COLUMNS.append(col + "_df_" + str(i))
                    
        # Now, we have a list of all column names, that we will use for retrieving the headers after
        # concatenation.
    
    else:
        print("No valid string was input to what_to_append, so appending rows (vertical append, equivalent to SQL UNION).")
        AXIS = 0
    
    if (union_join_type == 'inner'):
        
        print("Warning: concatenating dataframes using the \'inner\' join method, that removes missing values.")
        concat_df = pd.concat(LIST_OF_DATAFRAMES, axis = AXIS, ignore_index = ignore_index_on_union, sort = sort_values_on_union, join = union_join_type)
    
    else:
        
        #In case None or an invalid value is provided, use the default 'outer', by simply
        # not declaring the 'join':
        concat_df = pd.concat(LIST_OF_DATAFRAMES, axis = AXIS, ignore_index = ignore_index_on_union, sort = sort_values_on_union)
    
    if (AXIS == 1):
        # If we concatentated columns, we lost the columns' names (headers). So, use the list
        # LIST_OF_COLUMNS as the new headers for this case:
        concat_df.columns = LIST_OF_COLUMNS
    
    # Pandas .head(Y) method results in a dataframe containing the first Y rows of the 
    # original dataframe. The default .head() is Y = 5. Print first 10 rows of the 
    # new dataframe:
    print("Dataframes successfully concatenated. Check the 10 first rows of new dataframe:\n")
    print(concat_df.head(10))
    
    #Now return the concatenated dataframe:
    
    return concat_df


def df_gen_charac (df):
    
    import pandas as pd
    
    print("Dataframe 10 first rows:")
    print(df.head(10))
    
    #Line break before next information:
    print("\n")
    df_shape  = df.shape
    print(f"Dataframe shape (rows, columns) = {df_shape}.")
    
    #Line break before next information:
    print("\n")
    df_columns_list = df.columns
    print(f"Dataframe columns list = {df_columns_list}.")
    
    #Line break before next information:
    print("\n")
    df_dtypes = df.dtypes
    print("Dataframe variables types:")
    print(df_dtypes)
    
    #Line break before next information:
    print("\n")
    df_general_statistics = df.describe()
    print("Dataframe general statistics (numerical variables):")
    print(df_general_statistics)
    
    #Line break before next information:
    print("\n")
    df_missing_values = df.isna().sum()
    print("Total of missing values for each feature:")
    print(df_missing_values)
    
    return df_shape, df_columns_list, df_dtypes, df_general_statistics, df_missing_values


def drop_columns_or_rows (df, what_to_drop = 'columns', cols_list = None, row_index_list = None, reset_index_after_drop = True):
    
    import pandas as pd
    
    # check https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop.html?highlight=drop
    
    # what_to_drop = 'columns' for removing the columns specified by their names (headers)
    # in cols_list (a list of strings).
    # what_to_drop = 'rows' for removing the rows specified by their indices in
    # row_index_list (a list of integers). Remember that the indexing starts from zero, i.e.,
    # the first row is row number zero.
    
    # cols_list = list of strings containing the names (headers) of the columns to be removed
    # For instance: cols_list = ['col1', 'col2', 'col3'] will 
    # remove columns 'col1', 'col2', and 'col3' from the dataframe.
    # If a single column will be dropped, you can declare it as a string (outside a list)
    # e.g. cols_list = 'col1'; or cols_list = ['col1']
    
    # row_index_list = a list of integers containing the indices of the rows that will be dropped.
    # e.g. row_index_list = [0, 1, 2] will drop the rows with indices 0 (1st row), 1 (2nd row), and
    # 2 (third row). Again, if a single row will be dropped, you can declare it as an integer (outside
    # a list).
    # e.g. row_index_list = 20 or row_index_list = [20] to drop the row with index 20 (21st row).
    
    # reset_index_after_drop = True. keep it True to restarting the indexing numeration after dropping.
    # Alternatively, set reset_index_after_drop = False to keep the original numeration (the removed indices
    # will be missing).
    
    # Create dataframe local copy to manipulate, avoiding that Pandas operates on
    # the original object; or that Pandas tries to set values on slices or copies,
    # resulting in unpredictable results.
    # Use the copy method to effectively create a second object with the same properties
    # of the input parameters, but completely independent from it.
    DATASET = df.copy(deep = True)
    
    if (what_to_drop == 'columns'):
        
        if (cols_list is None):
            #check if a list was not input:
            print("Input a list of columns cols_list to be dropped.")
            return "error"
        
        else:
            #Drop the columns in cols_list:
            DATASET = DATASET.drop(columns = cols_list)
            print(f"The columns in {cols_list} headers list were successfully removed.\n")
    
    elif (what_to_drop == 'rows'):
        
        if (row_index_list is None):
            #check if a list was not input:
            print("Input a list of rows indices row_index_list to be dropped.")
            return "error"
        
        else:
            #Drop the rows in row_index_list:
            DATASET = DATASET.drop(row_index_list)
            print(f"The rows in {row_index_list} indices list were successfully removed.\n")
    
    else:
        print("Input a valid string as what_to_drop, rows or columns.")
        return "error"
    
    if (reset_index_after_drop == True):
        
        #restart the indexing
        DATASET = DATASET.reset_index(drop = True)
        print("The indices of the dataset were successfully restarted.\n")
    
    print("Check the 10 first rows from the returned dataset:\n")
    print(DATASET.head(10))
    
    return DATASET


def remove_duplicate_rows (df, list_of_columns_to_analyze = None, which_row_to_keep = 'first', reset_index_after_drop = True):
    
    import pandas as pd
    # check https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop_duplicates.html
    
    # if list_of_columns_to_analyze = None, the whole dataset will be analyzed, i.e., rows
    # will be removed only if they have same values for all columns from the dataset.
    # Alternatively, pass a list of columns names (strings), if you want to remove rows with
    # same values for that combination of columns. Pass it as a list, even if there is a single column
    # being declared.
    # e.g. list_of_columns_to_analyze = ['column1'] will check only 'column1'. Entries with same value
    # on 'column1' will be considered duplicates and will be removed.
    # list_of_columns_to_analyze = ['col1', 'col2',  'col3'] will analyze the combination of 3 columns:
    # 'col1', 'col2', and 'col3'. Only rows with same value for these 3 columns will be considered
    # duplicates and will be removed.
    
    # which_row_to_keep = 'first' will keep the first detected row and remove all other duplicates. If
    # None or an invalid string is input, this method will be selected.
    # which_row_to_keep = 'last' will keep only the last detected duplicate row, and remove all the others.
    
    # reset_index_after_drop = True. keep it True to restarting the indexing numeration after dropping.
    # Alternatively, set reset_index_after_drop = False to keep the original numeration (the removed indices
    # will be missing).
    
    # Create dataframe local copy to manipulate, avoiding that Pandas operates on
    # the original object; or that Pandas tries to set values on slices or copies,
    # resulting in unpredictable results.
    # Use the copy method to effectively create a second object with the same properties
    # of the input parameters, but completely independent from it.
    DATASET = df.copy(deep = True)
    
    if (which_row_to_keep == 'last'):
        
        #keep only the last duplicate.
        if (list_of_columns_to_analyze is None):
            # use the whole dataset
            DATASET = DATASET.drop_duplicates(keep = 'last')
            print(f"The rows with duplicate entries were successfully removed.")
            print("Only the last one of the duplicate entries was kept in the dataset.\n")
        
        else:
            #use the subset of columns
            if (list_of_columns_to_analyze is None):
                #check if a list was not input:
                print("Input a list of columns list_of_columns_to_analyze to be analyzed.")
                return "error"
        
            else:
                #Drop the columns in cols_list:
                DATASET = DATASET.drop_duplicates(subset = list_of_columns_to_analyze, keep = 'last')
                print(f"The rows with duplicate values for the columns in {list_of_columns_to_analyze} headers list were successfully removed.")
                print("Only the last one of the duplicate entries was kept in the dataset.\n")
    
    else:
        
        #keep only the first duplicate.
        if (list_of_columns_to_analyze is None):
            # use the whole dataset
            DATASET = DATASET.drop_duplicates()
            print(f"The rows with duplicate entries were successfully removed.")
            print("Only the first one of the duplicate entries was kept in the dataset.\n")
        
        else:
            #use the subset of columns
            if (list_of_columns_to_analyze is None):
                #check if a list was not input:
                print("Input a list of columns list_of_columns_to_analyze to be analyzed.")
                return "error"
        
            else:
                #Drop the columns in cols_list:
                DATASET = DATASET.drop_duplicates(subset = list_of_columns_to_analyze)
                print(f"The rows with duplicate values for the columns in {list_of_columns_to_analyze} headers list were successfully removed.")
                print("Only the first one of the duplicate entries was kept in the dataset.\n")
    
    if (reset_index_after_drop == True):
        
        #restart the indexing
        DATASET = DATASET.reset_index(drop = True)
        print("The indices of the dataset were successfully restarted.\n")
    
    print("Check the 10 first rows from the returned dataset:\n")
    print(DATASET.head(10))
    
    return DATASET


def remove_completely_blank_rows_and_columns (df, list_of_columns_to_ignore = None):
    
    import numpy as np
    import pandas as pd
    
    # list_of_columns_to_ignore: if you do not want to check a specific column, pass its name
    # (header) as an element from this list. It should be declared as a list even if it contains
    # a single value.
    # e.g. list_of_columns_to_ignore = ['column1'] will not analyze missing values in column named
    # 'column1'; list_of_columns_to_ignore = ['col1', 'col2'] will ignore columns 'col1' and 'col2'
    
    # Create dataframe local copy to manipulate, avoiding that Pandas operates on
    # the original object; or that Pandas tries to set values on slices or copies,
    # resulting in unpredictable results.
    # Use the copy method to effectively create a second object with the same properties
    # of the input parameters, but completely independent from it.
    DATASET = df.copy(deep = True)
    
    # Get dataframe length:
    df_length = len(DATASET)
    
    # Get list of columns from the dataframe:
    df_columns = DATASET.columns
    
    # Check if there is a list of columns to ignore:
    if not (list_of_columns_to_ignore is None):
        
        # Get a list containing only columns to check:
        cols_to_check = []
        
        # Append all elements from df_columns that are not in the list
        # to ignore:
        for column in df_columns:
            # loop through all elements named 'column' and check if it satisfies both conditions
            if (column not in list_of_columns_to_ignore):
                cols_to_check.append(column)
    
    else:
        # There is no column to ignore, so we must check all columns:
        cols_to_check = df_columns
    
    # Start a list of columns to eliminate; and a list of rows to eliminate:
    cols_to_del = []
    rows_to_del = []
    
    # Firstly, let's check for completely blank columns. If a column from cols_to_check is blank,
    # append it to the list cols_to_del:
    
    for column in cols_to_check:
        
        total_of_na = DATASET[column].isna().sum()
        # Total of missing values in the dataset for that column
        
        if (total_of_na == df_length):
            # all rows contain missing values:
            cols_to_del.append(column)
    
    # check if there is a column to delete. In this case, the length of the list
    # cols_to_del is higher than zero:
    if (len(cols_to_del) > 0):
        
        DATASET = DATASET.drop(columns = cols_to_del)
        print(f"The columns {cols_to_del} were completely blank and were removed.\n")
        
        # Update the cols_to_check list
        support_list = []
        
        for column in cols_to_check:
            # loop through all elements named 'column' and check if it satisfies both conditions
            if (column not in cols_to_del):
                support_list.append(column)
        
        # Make cols_to_check the support_list itself:
        cols_to_check = support_list
    
    
    # Let's look for rows to eliminate. Firstly, we need a list of the indices of columns that
    # will be analyzed:
    cols_indices = []
    
    for j in range(len(DATASET.columns)):
        # j goes from 0 to len(DATASET.columns) - 1, index of the last column
        if (DATASET.columns[j] in cols_to_check):
            
            cols_indices.append(j)
    
    # Now, cols_indices contains only the indices of columns to be analyzed, so we can use the
    # .iloc method to analyze a value:
    
    # Now, loop through all rows from the dataset:
    
    for i in range (len(DATASET)):
        # i goes from 0 to len(DATASET) - 1, index of the last row
        
        boolean_check = True
        
        # Check all columns correspondent to row i:
        for j in cols_indices:
            
            # Loops through all values in the list of columns
            checked_val = DATASET.iloc[i,j]
            # Depending on the type of variable, the following error may be raised:
            # func 'isnan' not supported for the input types, and the inputs could not be safely coerced 
            # to any supported types according to the casting rule ''safe''
            # To avoid it, we can set the variable as a string using the str attribute and check if
            # the value is not neither 'nan' nor 'NaN'. That is because pandas will automatically convert
            # identified null values to np.nan
            
            if ((checked_val is not None) & (str(checked_val) != 'NaN') & (str(checked_val) != 'nan')):
                # If one of these conditions is true, the value is None, 'NaN' or 'nan'
                # so this condition does not run.
                # It runs if at least one value is not a missing value
                boolean_check = False
            
        # boolean_check = True if all columns contain missing values for that row;
        # If at least one value is present, then boolean_check = False
        
        if (boolean_check): # only runs if it is True
            # append the row to the list of rows to delete:
            
                rows_to_del.append(i)
    
    # Now, rows_to_del contains the indices of all rows that should be deleted
    
    # If the list is not empty, its lenght is higher than zero. If it is, delete the rows:
    if (len(rows_to_del) > 0):
        
        DATASET = DATASET.drop(rows_to_del)
        DATASET = DATASET.reset_index(drop = True)
        print(f"The rows {rows_to_del} were completely blank and were removed. The indices of the dataframe were restarted after that.\n")
    
    if ((len(rows_to_del) > 0) | (len(cols_to_del) > 0)):
        
        # There were modifications in the dataframe.
        print("Check the first 10 rows of the new returned dataframe:\n")
        print(DATASET.head(10))
    
    else:
        print("No blank columns or rows were found. Returning the original dataframe.\n")
    
    
    return DATASET


def characterize_categorical_variables (df, categorical_variables_list):
    
    import numpy as np
    import pandas as pd
    
    # df: dataframe that will be analyzed
    
    # categorical_variables_list: list of strings containing the categorical variables that
    # will be characterized. Declare as a list even if it contains a single variable.
    # e.g. categorical_variables_list = ['cat_var'] will analyze a single variable (column)
    # named 'cat_var'; categorical_variables_list = ['var1', 'var2', 'var3'] will analyze
    # 3 columns, named 'var1', 'var2', and 'var3'
       
            # Encoding syntax:
            # dataset.loc[dataset["CatVar"] == 'Value1', "EncodedColumn"] = 1
            # dataset.loc[boolean_filter, EncodedColumn"] = value,
            # boolean_filter = (dataset["CatVar"] == 'Value1') will be True when the 
            # equality is verified. The .loc method filters the dataframe, accesses the
            # column declared after the comma and inputs the value defined (e.g. value = 1)
    
    # Start a list to store the results:
    summary_list = []
    # It will be a list of dictionaries.
    
    # Loop through all variables on the list:
    for categorical_var in categorical_variables_list:
        
        # Get unique vals and respective counts.

        # Start dictionary that will be appended as a new element from the list:
        # The main dictionary will be an element of the list
        unique_dict = {'categorical_variable': categorical_var}
        
        # Start a list of unique values:
        unique_vals = []

        # Now, check the unique values of the categorical variable:
        unique_vals_array = df[categorical_var].unique()
        # unique_vals_array is a NumPy array containing the different values from the categorical variable.

        # Total rows:
        total_rows = len(df)

        # Check the total of missing values
        # Set a boolean_filter for checking if the row contains a missing value
        boolean_filter = df[categorical_var].isna()

        # Calculate the total of elements when applying the filter:
        total_na = len(df[boolean_filter])

        # Create a dictionary for the missing values:
        na_dict = {
                    'value': np.nan, 
                    'counts_of_occurences': total_na,
                    'percent_of_occurences': ((total_na/total_rows)*100)
                    }
        
        
        # Nest this dictionary as an element from the list unique_vals.
        unique_vals.append(na_dict)
        # notice that the dictionary was nested into a list, which will be itself
        # nested as an element of the dictionary unique_dict
        
        # Now loop through each possible element on unique_vals_array
        for unique_val in unique_vals_array:

            # loop through each possible value of the array. The values are called 'unique_val'
            # Check if the value is not none:
            
            # Depending on the type of variable, the following error may be raised:
            # func 'isnan' not supported for the input types, and the inputs could not be safely coerced 
            # to any supported types according to the casting rule ''safe''
            # To avoid it, we can set the variable as a string using the str attribute and check if
            # the value is not neither 'nan' nor 'NaN'. That is because pandas will automatically convert
            # identified null values to np.nan
            
            # So, since The unique method creates the strings 'nan' or 'NaN' for the missing values,
            # if we read unique_val as string using the str attribute, we can filter out the
            # values 'nan' or 'NaN', which may be present together with the None and the float
            # np.nan:
            if ((str(unique_val) != 'nan') & (str(unique_val) != 'NaN') & (unique_val is not None)):
                # If one of these conditions is true, the value is None, 'NaN' or 'nan'
                # so this condition does not run.
                # It runs if at least one value is not a missing value
                # (only when the value is neither None nor np.nan)

                # create a filter to select only the entries where the column == unique_val:
                boolean_filter = (df[categorical_var] == unique_val)
                # Calculate the total of elements when applying the filter:
                total_elements = len(df[boolean_filter])

                # Create a dictionary for these values:
                # Use the same keys as before:
                cat_var_dict = {
                    
                                'value': unique_val, 
                                'counts_of_occurences': total_elements,
                                'percent_of_occurences': ((total_elements/total_rows)*100)
                    
                                }
                
                # Nest this dictionary as an element from the list unique_vals.
                unique_vals.append(cat_var_dict)
                # notice that the dictionary was nested into a list, which will be itself
                # nested as an element of the dictionary unique_dict
        
        # Nest the unique_vals list as an element of the dictionary unique_dict:
        # Use the update method, setting 'unique_values' as the key:
        unique_dict.update({'unique_values': unique_vals})
        # Notice that unique_vals is a list where each element is a dictionary with information
        # from a given unique value of the variable 'categorical_var' being analyzed.
        
        # Finally, append 'unique_dict' as an element of the list summary_list:
        summary_list.append(unique_dict)
        
    
    # We created a highly nested JSON structure with the following format:
    
    # summary_list = [
    #          {
    #            'categorical_variable': categorical_var1,
    #            'unique_values': [
    #                             {
    #                                'value': np.nan, 
    #                               'counts_of_occurences': total_na,
    #                               'percent_of_occurences': ((total_na/total_rows)*100)
    #                      },  {
    #
    #                           'value': unique_val_1, 
    #                           'counts_of_occurences': total_elements_1,
    #                           'percent_of_occurences': ((total_elements_1/total_rows)*100)
    #               
    #                     }, ... , {
    #                           'value': unique_val_N, 
    #                           'counts_of_occurences': total_elements_N,
    #                           'percent_of_occurences': ((total_elements_N/total_rows)*100)
    #               
    #                     }
    #                    ]
    #                 }, ... {
    #                        'categorical_variable': categorical_var_M,
    #                        'unique_values': [...]
    #                       }
    # ]

    
    # Now, call the json_obj_to_dataframe function to flat the list of dictionaries
    
    JSON_OBJ_TO_CONVERT = summary_list
    JSON_OBJ_TYPE = 'list'
    JSON_RECORD_PATH = 'unique_values'
    JSON_FIELD_SEPARATOR = "_"
    JSON_METADATA_PREFIX_LIST = ['categorical_variable']
    # JSON_METADATA_PREFIX_LIST: list of strings (in quotes). Manipulates the parameter 
    # 'meta' from json_normalize method. Fields to use as metadata for each record in resulting 
    # table. Declare here the non-nested fields, i.e., the fields in the principal JSON. They
    # will be repeated in the rows of the dataframe to give the metadata (context) of the rows.

    cat_vars_summary = json_obj_to_pandas_dataframe (json_obj_to_convert = JSON_OBJ_TO_CONVERT, json_obj_type = JSON_OBJ_TYPE, json_record_path = JSON_RECORD_PATH, json_field_separator = JSON_FIELD_SEPARATOR, json_metadata_prefix_list = JSON_METADATA_PREFIX_LIST)
    
    print("\n") # line break
    print("Finished analyzing the categorical variables. Check the summary dataframe:\n")
    print(cat_vars_summary)
    
    return cat_vars_summary


def GROUP_VARIABLES_BY_TIMESTAMP (df, list_of_categorical_columns, timestamp_tag_column, grouping_frequency_unit = 'day', number_of_periods_to_group = 1, aggregate_function = 'mean', start_time = None, offset_time = None):
    
    import numpy as np
    import pandas as pd
    from scipy import stats
    # numpy has no function mode, but scipy's stats module has.
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mode.html?msclkid=ccd9aaf2cb1b11ecb57c6f4b3e03a341
    
    
    ### WARNING: At least one numeric variable must be present for this function to run. If there are
    # no numeric variables, start one by declaring and running df['numeric_col'] = 0. This will create
    # a numeric column named 'numeric_col' where all values are zero.
    
    # list_of_categorical_columns: list of strings containing the categorical variables.
    # Declare as a list even if there is a single categorical variable:
    # e.g. list_of_categorical_columns = ['var1'] if there is only a variable 'var1' which is
    # categorical
    # list_of_categorical_columns = ['var1', 'var2', 'var3'] if 'var1', 'var2', and 'var3' are
    # categorical.
    # Set list_of_categorical_columns = None if there are no categorical columns to aggregate.
    
    print("WARNING: If you do not specify the categorical variables as the list \'list_of_categorical_columns\', they will be all lost in the final dataframe.\n")
    print("This function will process all numeric variables automatically, but the categorical (object) ones will be removed if they are not specified.\n")
    print("The categorical variables will be grouped in terms of mode, i.e., as the most common value observed during the aggregated time period. This is the maximum of the statistical distribution of that variable.\n")
     
    # df - dataframe/table containing the data to be grouped
    
    # timestamp_tag_colum: name (header) of the column containing the
    
    # timestamps for grouping the data.
    
    # grouping_frequency_unit: the frequency of aggregation. The possible values are:
    
    grp_frq_unit_dict = {'year': "Y", 'month': "M", 'week': "W", 
                            'day': "D", 'hour': "H", 'minute': "min", 'second': 'S'}
    
    #Simply provide the key: 'year', 'month', 'week',..., 'second', and this dictionary
    #will convert to the Pandas coding.
    #The default is 'day', so this will be inferred frequency if no value is provided.
    
    #To access the value of a dictionary d = {key1: item1, ...}:
    #d['key1'] = item1. - simply declare the key as a string (under quotes) inside brackets
    #just as if you were accessing a column from the dataframe.
    #Since grouping_frequency_unit is variable storing a string, it should not come under
    #quotes:
    
    #Convert the input to Pandas encoding:
    frq_unit = grp_frq_unit_dict[grouping_frequency_unit]
    
    #https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html
    #To group by business day, check the example:
    #https://stackoverflow.com/questions/13019719/get-business-days-between-start-and-end-date-using-pandas
    
    #number_of_periods_to_group: the bin size. The default is 1, so we will group by '1day'
    #if number_of_periods_to_group = 2 we would be grouping by every 2 days.
    #If the unit was minute and number_of_periods_to_group = 30, we would be grouping into
    #30-min bins.
    
    if (number_of_periods_to_group <= 0):
        
        print("Invalid number of periods to group. Changing to 1 period.")
        number_of_periods_to_group = 1
    
    if (number_of_periods_to_group == 1):
        
        #Do not put the number 1 prior to the frequency unit
        FREQ =  frq_unit
    
    else:
        #perform the string concatenation. Convert the number into a string:
        number_of_periods_to_group = str(number_of_periods_to_group)
        #Concatenate the strings:
        FREQ = number_of_periods_to_group + frq_unit
        #Expected output be like '2D' for a 2-days grouping
        
    # aggregate_function: Pandas aggregation method: 'mean', 'median', 'std', 'sum', 'min'
    # 'max', 'count', etc. The default is 'mean'. Then, if no aggregate is provided, 
    # the mean will be calculated.
    
    agg_dict = {
        
        'mean': 'mean',
        'sum': 'sum',
        'median': 'median',
        'std': 'std',
        'count': 'count',
        'min': 'min',
        'max': 'max',
        'mode': stats.mode,
        'geometric_mean': stats.gmean,
        'harmonic_mean': stats.hmean,
        'kurtosis': stats.kurtosis,
        'skew': stats.skew,
        'geometric_std': stats.gstd,
        'interquartile_range': stats.iqr,
        'mean_standard_error': stats.sem,
        'entropy': stats.entropy
        
    }
    # scipy.stats Summary statistics:
    # https://docs.scipy.org/doc/scipy/reference/stats.html
    
    # Convert the input into the correct aggregation function. Access the value on key
    # aggregate_function in dictionary agg_dict:
    
    if (aggregate_function in agg_dict.keys()):
        
        aggregate_function = agg_dict[aggregate_function]
    
    else:
        print(f"Select a valid aggregate function: {agg_dict.keys()}")
        return "error"
    
    # Now, aggregate_function actually stores the value that must be passed to the agg method.
    
    
    #You can pass a list of multiple aggregations, like: 
    #aggregate_function = [mean, max, sum]
    #You can also pass custom functions, like: pct30 (30-percentile), or np.mean
    #aggregate_function = pct30
    #aggregate_function = np.mean (numpy.mean)
    
    #ADJUST OF GROUPING BASED ON A FIXED TIMESTAMP
    #This parameters are set to None as default.
    #You can specify the origin (start_time) or the offset (offset_time), which are
    #equivalent. The parameter should be declared as a timestamp.
    #For instance: start_time = '2000-10-01 23:30:00'
    
    #WARNING: DECLARE ONLY ONE OF THESE PARAMETERS. DO NOT DECLARE AN OFFSET IF AN 
    #ORIGIN WAS SPECIFIED, AND VICE-VERSA.
    
    #Create a Pandas timestamp object from the timestamp_tag_column. It guarantees that
    #the timestamp manipulation methods can be correctly applied.
    #Let's create using nanoseconds resolution, so that the timestamps present the
    #maximum possible resolution:
    
    # START: CONVERT ALL TIMESTAMPS/DATETIMES/STRINGS TO pandas.Timestamp OBJECTS.
    # This will prevent any compatibility problems.
    
    #The pd.Timestamp function can handle a single timestamp per call. Then, we must
    # loop trough the series, and apply the function to each element.
    
    # Create dataframe local copy to manipulate, avoiding that Pandas operates on
    # the original object; or that Pandas tries to set values on slices or copies,
    # resulting in unpredictable results.
    # Use the copy method to effectively create a second object with the same properties
    # of the input parameters, but completely independent from it.
    df_copy = df.copy(deep = True)
    
    
    # 1. Start a list to store the Pandas timestamps:
    timestamp_list = []
    
    # 2. Loop through each element of the timestamp column, and apply the function
    # to guarantee that all elements are Pandas timestamps
    
    for timestamp in df_copy[timestamp_tag_column]:
        #Access each element 'timestamp' of the series df[timestamp_tag_column]
        timestamp_list.append(pd.Timestamp(timestamp, unit = 'ns'))
    
    # 3. Create a column in the dataframe that will be used as key for the Grouper class
    # The grouper requires a column in the dataframe - it cannot use a list for that.
    # Simply copy the list as the new column:
    df_copy['timestamp_obj'] = timestamp_list
    
    # Now we have a list correspondent to timestamp_tag_column, but only with
    # Pandas timestamp objects
    
    # 4. Sort the dataframe in ascending order of timestamps:
    df_copy = df_copy.sort_values(by = 'timestamp_obj', ascending = True)
    
    # Reset indices before aggregation:
    df_copy = df_copy.reset_index(drop = True)
    
    # In this function, we do not convert the Timestamp to a datetime64 object.
    # That is because the Grouper class specifically requires a Pandas Timestamp
    # object to group the dataframes.
    
    if ((list_of_categorical_columns is not None) & (len(list_of_categorical_columns) > 0)):
        
        # Let's prepare another copy of the dataframe before it gets manipulated:
        
        # 1. Subset the dataframe to contain only the timestamps and the categorical columns.
        # For this, create a list with 'timestamp_obj' and append each element from the list
        # of categorical columns to this list. Save it as subset_list:
        
        subset_list = ['timestamp_obj'] 
        
        for cat_var in list_of_categorical_columns:
            subset_list.append(cat_var)
    
        # 2. Subset df_copy and save it as grouped_df_categorical:
        grouped_df_categorical = df_copy[subset_list]
        
    
    # Let's try to group the dataframe and save it as grouped_df
    try:
        
        if (start_time is not None):

            grouped_df = df_copy.groupby(pd.Grouper(key = 'timestamp_obj' , freq = FREQ, origin = start_time)).agg(aggregate_function)

        elif (offset_time is not None):

            grouped_df = df_copy.groupby(pd.Grouper(key = 'timestamp_obj' , freq = FREQ, offset = offset_time)).agg(aggregate_function)

        else:

            #Standard situation, when both start_time and offset_time are None
            grouped_df = df_copy.groupby(pd.Grouper(key = 'timestamp_obj' , freq = FREQ)).agg(aggregate_function)

        print (f"Numerical variables of the dataframe grouped by every {number_of_periods_to_group} {frq_unit}.")
    
    
        #The parameter 'key' of the Grouper class must be the name (string) of a column
        # of the dataframe
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Grouper.html

        #The objects 'timestamp_obj' are now the index from grouped_df dataframe
        #Let's store them as a column and restart the index:
        #1. Copy the index to a new column:
        grouped_df['Timestamp_grouped'] = grouped_df.index

        #2. Reset the index:
        grouped_df = grouped_df.reset_index(drop = True)

        #3. 'pandas.Timestamp_grouped' is now the last column. Let's create a list of the
        # reordered columns, starting from 'pandas.Timestamp_grouped'

        reordered_cols_list = ['Timestamp_grouped']

        for i in range((len(grouped_df.columns)-1)):

            #This loop goes from i = 0 to i = (len(grouped_df.columnns)-2)
            # grouped_df.columnns is a list containing the columns names. Since indexing goes
            # from 0, the last element is the index i = (len(grouped_df.columnns)-1).
            # But this last element is 'pandas.Timestamp_grouped', which we used as the
            # first element of the list reordered_cols_list. Then, we must loop from the
            # first element of grouped_df.columnns to the element immediately before 'pandas.Timestamp_grouped'.
            # Then, the last element to be read is (len(grouped_df.columnns)-2)
            # range (i, j) goes from i to j-1. If only one value is specified, i = 0 and j =
            # declared value. If you print all i values in range(10), numbers from 0 to 9
            # will be shown.

            reordered_cols_list.append(grouped_df.columns[i])

        #4. Reorder the dataframe passing the list reordered_cols_list as the column filters
        # / columns selection list.Notice that df[['col1', 'col2']] = df[list], where list =
        # ['col1', 'col2']. To select or reorder columns, we pass the list of columns under
        # brackets as parameter.

        grouped_df = grouped_df[reordered_cols_list]

        # Now, grouped_df contains the grouped numerical features. We must now process the categorical
        # variables.
        # Notice that we have the lists:
        # list_of_categorical_columns: categorical columns on the dataset df_copy
        # timestamp_list: list of timestamp objects correspondent to the dataset df_copy
        # grouped_df: dataframe with the aggregated timestamps, which may have been saved as strings,
        # since they were converted to index.
    
    except:
        # an exception error is returned when trying to use a numeric aggregate such as 'mean'
        # in a dataframe containing only categorical variables.
        print("No numeric variables detected to group.\n")
    
    
    #### LET'S AGGREGATE THE CATEGORICAL VARIABLES
    
    ## Check if there is a list of categorical features. If there is, run the next block of code:
    
    if ((list_of_categorical_columns is not None) & (len(list_of_categorical_columns) > 0)):
        # There are categorical columns to aggregate too - the list is not empty
        # Consider: a = np.array(['a', 'a', 'b'])
        # The stats.mode function stats.mode(a) returns an array as: 
        # ModeResult(mode=array(['a'], dtype='<U1'), count=array([2]))
        # If we select the first element from this array, stats.mode(a)[0], the function will 
        # return an array as array(['a'], dtype='<U1'). 
        # We want the first element from this array stats.mode(a)[0][0], 
        # which will return a string like 'a'
        
        # We can pass stats.mode as the aggregate function in agg: agg(stats.mode)
        
        # The original timestamps, already converted to Pandas timestamp objects, are stored in:
        # timestamp_list. So, we can again use this list to aggregation. It was saved as the
        # column 'timestamp_obj' from the dataframe df_copy
        
        # This will generate series where each element will be an array like:
        # series = ([mode_for_that_row], [X]), where X is the counting for that row. For example, if we
        # aggregate by week, and there is a 'categorical_value' by day, X will be 7.
        
        # to access a row from the series, for instance, row 0: series[0]. 
        # This element will be an array like:
        # ModeResult(mode=array([mode_for_that_row], dtype='<U19'), count=array([X])).
        # To access the first element of this array, we put another index: series[0][0].
        # This element will be like:
        # array([mode_for_that_row], dtype='<U19')
        # The mode is the first element from this array. To access it, we add another index:
        # series[0][0][0]. The result will be: mode_for_that_row
        
        ## Aggregate the dataframe in terms of mode:
        
        if (start_time is not None):

            grouped_df_categorical = grouped_df_categorical.groupby(pd.Grouper(key = 'timestamp_obj' , freq = FREQ, origin = start_time)).agg(stats.mode)

        elif (offset_time is not None):

            grouped_df_categorical = grouped_df_categorical.groupby(pd.Grouper(key = 'timestamp_obj' , freq = FREQ, offset = offset_time)).agg(stats.mode)

        else:

            #Standard situation, when both start_time and offset_time are None
            grouped_df_categorical = grouped_df_categorical.groupby(pd.Grouper(key = 'timestamp_obj' , freq = FREQ)).agg(stats.mode)

        #The objects 'timestamp_obj' are now the index from grouped_df_categorical dataframe
        #Let's store them as a column and restart the index:
        #1. Copy the index to a new column:
        grouped_df_categorical['Timestamp_grouped'] = grouped_df_categorical.index

        #2. Reset the index:
        grouped_df_categorical = grouped_df_categorical.reset_index(drop = True)
        
        # Now, each column from this dataframe is a series where each element is 
        # an array like ([mode_for_that_row], [X]). We want only the [0][0] element from the series,
        # which is the mode.
        
        # Loop through each categorical variable:
        for cat_var in list_of_categorical_columns:
            
            # save as a series:
            cat_var_series = grouped_df_categorical[cat_var]
            # Start a list to store only the modes:
            list_of_modes = []
            
            # Now, loop through each row of cat_var_series. Take the element [0][0]
            # and append it to the list_of_modes:
            
            for i in range(0, len(cat_var_series)):
                
                # Goes from i = 0 to i = len(cat_var_series) - 1, index of the last element
                # Append the element [0][0] from row [i]
                
                try:
                    list_of_modes.append(cat_var_series[i][0][0])
                
                except IndexError:
                    # This error is generated when trying to access an array storing no values.
                    # (i.e., with missing values). Since there is no dimension, it is not possible
                    # to access the [0][0] position. In this case, simply append the np.nan (missing value):
                    list_of_modes.append(np.nan)
            
            # Now we finished the nested for loop, list_of_modes contain only the modes
        
            # Make the column cat_var the list_of_modes itself:
            grouped_df_categorical[cat_var] = list_of_modes
        
        
        # Finally, we must merge grouped_df_categorical to grouped_df
        
        try:
            # Run it if there is a dataframe of aggregated numeric variables to merge with the dataframe
            # of aggregated categorical variables.
            SUFFIXES = (('_' + aggregate_function), '_mode') # Case there are duplicated rows
            grouped_df = pd.merge_ordered(grouped_df, grouped_df_categorical, on = 'Timestamp_grouped', how = 'inner', suffixes = SUFFIXES, fill_method = 'ffill')
        
        except:
            # There is no grouped_df to merge, because there were no numeric variables
            grouped_df = grouped_df_categorical
        
        print(f"Finished grouping the categorical features {list_of_categorical_columns} in terms of mode.")
        print(f"The mode is the most common value observed (maximum of the statistical distribution) for the categorical variable when we group data in terms of {number_of_periods_to_group} {frq_unit}.\n")
        
        
    # The next final block runs even if there is no categorical variable:
    
    # Pandas .head(Y) method results in a dataframe containing the first Y rows of the 
    # original dataframe. The default .head() is Y = 5. Print first 10 rows of the 
    # new dataframe:
    print("Dataframe successfully grouped. Check its 10 first rows (without the categorical/object variables):\n")
    print(grouped_df.head(10))
    
    #Now return the grouped dataframe with the timestamp as the first column:
    
    return grouped_df


def GROUP_DATAFRAME_BY_VARIABLE (df, variable_to_group_by, return_summary_dataframe = False, subset_of_columns_to_aggregate = None, aggregate_function = 'mean', add_suffix_to_aggregated_col = True, suffix = None):

    import numpy as np
    import pandas as pd
    from scipy import stats
    
    print("WARNING: Do not use this function to group the dataframe in terms of a timestamp. For this purpose, use function GROUP_VARIABLES_BY_TIMESTAMP.\n")
    
    # df: dataframe being analyzed
    
    # variable_to_group_by: string (inside quotes) containing the name 
    # of the column in terms of which the dataframe will be grouped by. e.g. 
    # variable_to_group_by = "column1" will group the dataframe in terms of 'column1'.
    # WARNING: do not use this function to group a dataframe in terms of a timestamp. To group by
    # a timestamp, use function GROUP_VARIABLES_BY_TIMESTAMP instead.
    
    # return_summary_dataframe = False. Set return_summary_dataframe = True if you want the function
    # to return a dataframe containing summary statistics (obtained with the describe method).
    
    # subset_of_columns_to_aggregate: list of strings (inside quotes) containing the names 
    # of the columns that will be aggregated. Use this argument if you want to aggregate only a subset,
    # not the whole dataframe. Declare as a list even if there is a single column to group by.
    # e.g. subset_of_columns_to_aggregate = ["response_feature"] will return the column 
    # 'response_feature' grouped. subset_of_columns_to_aggregate = ["col1", 'col2'] will return columns
    # 'col1' and 'col2' grouped.
    # If you want to aggregate the whole subset, keep subset_of_columns_to_aggregate = None.
    
    # aggregate_function = 'mean': String defining the aggregation 
    # method that will be applied. Possible values:
    # 'median', 'mean', 'mode', 'sum', 'min', 'max', 'variance', 'count',
    # 'standard_deviation', 'cum_sum', 'cum_prod', 'cum_max', 'cum_min',
    # '10_percent_quantile', '20_percent_quantile',
    # '25_percent_quantile', '30_percent_quantile', '40_percent_quantile',
    # '50_percent_quantile', '60_percent_quantile', '70_percent_quantile',
    # '75_percent_quantile', '80_percent_quantile', '90_percent_quantile',
    # '95_percent_quantile', 'kurtosis', 'skew', 'interquartile_range',
    # 'mean_standard_error', 'entropy'
    # To use another aggregate function, you can use the .agg method, passing 
    # the aggregate as argument, such as in:
    # .agg(scipy.stats.mode), 
    # where the argument is a Scipy aggregate function.
    # If None or an invalid function is input, 'mean' will be used.
    
    # add_suffix_to_aggregated_col = True will add a suffix to the
    # aggregated columns. e.g. 'responseVar_mean'. If add_suffix_to_aggregated_col 
    # = False, the aggregated column will have the original column name.
    
    # suffix = None. Keep it None if no suffix should be added, or if
    # the name of the aggregate function should be used as suffix, after
    # "_". Alternatively, set it as a string. As recommendation, put the
    # "_" sign in the beginning of this string to separate the suffix from
    # the original column name. e.g. if the response variable is 'Y' and
    # suffix = '_agg', the new aggregated column will be named as 'Y_agg'
    

    # Create a local copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    
    if (subset_of_columns_to_aggregate is not None):
        
        if (variable_to_group_by not in subset_of_columns_to_aggregate):
            
            list_with_variable_to_group_by = [variable_to_group_by]
            
            # a = ['a', 'b'], b = ['c', 'd']
            # a + b = ['a', 'b', 'c', 'd'], b + a = ['c', 'd', 'a', 'b']
            # sum of list: append of one list into the other
            subset_of_columns_to_aggregate = list_with_variable_to_group_by + subset_of_columns_to_aggregate
            # now, the first element from the list subset_of_columns_to_aggregate is the aggregation
            # column. Then, we avoid that the user eliminates this column, resulting in error
            # when trying to aggregate in terms of variable_to_group_by.
        
        # There is a subset of columns.
        # Select only the columns specified as subset_of_columns_to_aggregate:
        DATASET = DATASET[subset_of_columns_to_aggregate]
    
    
    # Before calling the method, we must guarantee that the variables may be
    # used for that aggregate. Some aggregations are permitted only for numeric variables, so calling
    # the method before selecting the variables may raise warnings or errors.
    
    
    list_of_aggregates = ['median', 'mean', 'mode', 'sum', 'min', 'max', 'variance',
                          'standard_deviation', 'count', 'cum_sum', 'cum_prod', 'cum_max', 'cum_min',
                          '10_percent_quantile', '20_percent_quantile', '25_percent_quantile', 
                          '30_percent_quantile', '40_percent_quantile', '50_percent_quantile', 
                          '60_percent_quantile', '70_percent_quantile', '75_percent_quantile', 
                          '80_percent_quantile', '90_percent_quantile', '95_percent_quantile',  
                          'kurtosis', 'skew', 'interquartile_range', 'mean_standard_error', 'entropy']
    
    list_of_numeric_aggregates = ['median', 'mean', 'sum', 'min', 'max', 'variance',
                          'standard_deviation', 'cum_sum', 'cum_prod', 'cum_max', 'cum_min',
                          '10_percent_quantile', '20_percent_quantile', '25_percent_quantile', 
                          '30_percent_quantile', '40_percent_quantile', '50_percent_quantile', 
                          '60_percent_quantile', '70_percent_quantile', '75_percent_quantile', 
                          '80_percent_quantile', '90_percent_quantile', '95_percent_quantile',  
                          'kurtosis', 'skew', 'interquartile_range', 'mean_standard_error']
    
    # Check if an invalid or no aggregation function was selected:
    if ((aggregate_function not in (list_of_aggregates)) | (aggregate_function is None)):
        
        aggregate_function = 'mean'
        print("Invalid or no aggregation function input, so using the default \'mean\'.\n")
    
    # Get dataframe's columns list. Use the list attribute to convert the array to list:
    df_cols = list(DATASET.columns)
    
    # Check if a numeric aggregate was selected:
    if (aggregate_function in list_of_numeric_aggregates):
        
        print("Numeric aggregate selected. So, subsetting dataframe containing only numeric variables.\n")
        
        # 1. start a list for the numeric columns:
        numeric_cols = []
                
        # 2. Loop through each column on df_cols. If it is numeric, put it in the correspondent 
        # list:
        for column in df_cols:
            # test each element in the list or array df_cols
            column_data_type = DATASET[column].dtype
                    
            if ((column_data_type != 'O') & (column_data_type != 'object')):
                        
                # If the Pandas series was defined as an object, it means it is categorical
                # (string, date, etc).
                # Since the column is not an object, append it to the numeric columns list:
                numeric_cols.append(column)
        
        # Now that we have a list of numeric columns, let's subset the dataframe:
        
        if (variable_to_group_by not in numeric_cols):
            
            list_with_variable_to_group_by = [variable_to_group_by]
            numeric_cols = list_with_variable_to_group_by + numeric_cols
            # now, the first element from the list numeric_cols is the aggregation
            # column. Then, we avoid that the algorithm eliminates this column, if it is
            # categorical. If so, the code would raise an error, since it would not be possible
            # to aggregate in terms of variable_to_group_by
        
        # 3. Subset the dataframe
        DATASET = DATASET[numeric_cols]
        
        if (return_summary_dataframe == True):
            # Create another copy of the dataframe to obtain the summary dataframe:
            # Copy DATASET: If a subset was passed, DATASET was already filtered
            summary_agg_df = DATASET.copy(deep = True)
            summary_agg_df = summary_agg_df.groupby(by = variable_to_group_by, as_index = False, sort = True).describe()
            # The summary should not be used to drop invalid columns. Since it process only
            # numeric variables, we apply it to the proper subset
            
    else:
        # It is a categorical variable
        
        print("Categorical aggregate selected. So, subsetting dataframe containing only categorical variables.\n")
        
        # 1. start a list for the numeric columns:
        categorical_cols = []
                
        # 2. Loop through each column on df_cols. If it is categorical, put it in the correspondent 
        # list:
        for column in df_cols:
            # test each element in the list or array df_cols
            column_data_type = DATASET[column].dtype
                    
            if ((column_data_type == 'O') | (column_data_type == 'object')):
     
                # Since the column is an object, append it to the categorical columns list:
                categorical_cols.append(column)
        
        # Now that we have a list of categorical columns, let's subset the dataframe:
        
        if (variable_to_group_by not in categorical_cols):
            
            list_with_variable_to_group_by = [variable_to_group_by]
            categorical_cols = list_with_variable_to_group_by + categorical_cols
            # now, the first element from the list categorical_cols is the aggregation
            # column. Then, we avoid that the algorithm eliminates this column, if it is
            # numeric. If so, the code would raise an error, since it would not be possible
            # to aggregate in terms of variable_to_group_by
        
        # 3. Subset the dataframe
        DATASET = DATASET[categorical_cols]
    
    # Before grouping, let's remove the missing values, avoiding the raising of TypeError.
    # Pandas deprecated the automatic dropna with aggregation:
    DATASET = DATASET.dropna(axis = 0)
    
    # Groupby according to the selection.
    # Here, there is a great gain of performance in not using a dictionary of methods:
    # If using a dictionary of methods, Pandas would calculate the results for each one of the methods.
    
    # Pandas groupby method documentation:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.groupby.html?msclkid=7b3531a6cff211ec9086f4edaddb94ba
    # argument as_index = False: prevents the grouper variable to be set as index of the new dataframe.
    # (default: as_index = True);
    # dropna = False: do not removes the missing values (default: dropna = True, used here to avoid
    # compatibility and version issues)
    
    if (aggregate_function == 'median'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).agg('median')

    elif (aggregate_function == 'mean'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).mean()
    
    elif (aggregate_function == 'mode'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).agg(stats.mode)
    
    elif (aggregate_function == 'sum'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).sum()
    
    elif (aggregate_function == 'count'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).count()
    
    elif (aggregate_function == 'min'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).min()
    
    elif (aggregate_function == 'max'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).max()
    
    elif (aggregate_function == 'variance'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).var()

    elif (aggregate_function == 'standard_deviation'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).std()
    
    elif (aggregate_function == 'cum_sum'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).cumsum()

    elif (aggregate_function == 'cum_prod'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).cumprod()
    
    elif (aggregate_function == 'cum_max'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).cummax()
    
    elif (aggregate_function == 'cum_min'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).cummin()
    
    elif (aggregate_function == '10_percent_quantile'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).quantile(0.10)
    
    elif (aggregate_function == '20_percent_quantile'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).quantile(0.20)
    
    elif (aggregate_function == '25_percent_quantile'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).quantile(0.25)
    
    elif (aggregate_function == '30_percent_quantile'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).quantile(0.30)
    
    elif (aggregate_function == '40_percent_quantile'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).quantile(0.40)
    
    elif (aggregate_function == '50_percent_quantile'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).quantile(0.50)

    elif (aggregate_function == '60_percent_quantile'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).quantile(0.60)
    
    elif (aggregate_function == '70_percent_quantile'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).quantile(0.30)

    elif (aggregate_function == '75_percent_quantile'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).quantile(0.75)

    elif (aggregate_function == '80_percent_quantile'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).quantile(0.80)
    
    elif (aggregate_function == '90_percent_quantile'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).quantile(0.90)
    
    elif (aggregate_function == '95_percent_quantile'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).quantile(0.95)

    elif (aggregate_function == 'kurtosis'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).agg(stats.kurtosis)
    
    elif (aggregate_function == 'skew'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).agg(stats.skew)

    elif (aggregate_function == 'interquartile_range'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).agg(stats.iqr)
    
    elif (aggregate_function == 'mean_standard_error'):
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).agg(stats.sem)
    
    else: # entropy
        
        DATASET = DATASET.groupby(by = variable_to_group_by, as_index = False, sort = True).agg(stats.entropy)
    
    
    # Now, update the list of columns:
    df_cols = list(DATASET.columns)
    
    if (add_suffix_to_aggregated_col == True):
        
        # Let's add a suffix. Check if suffix is None. If it is,
        # set "_" + aggregate_function as suffix:
        if (suffix is None):
            suffix = "_" + aggregate_function
    
    
    if (aggregate_function == 'mode'):
        
        # The columns will be saved as a series of Tuples. Each row contains a tuple like:
        # ([calculated_mode], [counting_of_occurrences]). We want only the calculated mode.
        # On the other hand, if we do column[0], we will get the columns first row. So, we have to
        # go through each column, retrieving only the mode:
        
        list_of_new_columns = []
        
        for column in (df_cols):
            
            # Loop through each column from the dataset
            if (column == variable_to_group_by):
                # special case for the column used for grouping.
                # Simply append this column to a list, without performing any operation
                list_of_col = [variable_to_group_by]
            
            else:
                
                if (add_suffix_to_aggregated_col == True):
                        
                        new_column_name = column + suffix
                
                else:
                    new_column_name = column + "_mode"
                    # name for differencing, allowing us to start the variable
                
                # start categorical variable as empty string:
                DATASET[new_column_name] = ''
                
                # Retrieve the index j of new_column_name in the list of columns
                # (use the list attribute to convert the array to list):
                j = (list(DATASET.columns)).index(new_column_name)
                
                # Save the new column on the list of new columns:
                list_of_new_columns.append(new_column_name)
                
                # Now, loop through each row from the dataset:
                for i in range(0, len(DATASET)):
                    # i = 0 to i = len(DATASET) - 1
                    
                    mode_array = DATASET[column][i]
                    # mode array is like:
                    # ModeResult(mode=array([calculated_mode]), count=array([counting_of_occurrences]))
                    # To retrieve only the mode, we must access the element [0][0] from this array:
                    mode = mode_array[0][0]
                    
                    # Now, save the mode in the column j (column new_column_name) for the row i:
                    DATASET.iloc[i, j] = mode
                
        # Now, repeat it for each other variable.
        
        # Concatenate the list list_of_col with list_of_new_columns
        # a = ['a', 'b'] , b = ['c', 'd'], a + b = ['a', 'b', 'c', 'd']
        # b + a = ['c', 'd', 'a', 'b']
        list_of_new_columns = list_of_col + list_of_new_columns
        
        # Subset the dataframe to keep only the columns in list_of_new_columns:
        DATASET = DATASET[list_of_new_columns]
        
        if (add_suffix_to_aggregated_col == False):
            
            # No suffix should be added, i.e., the columns should keep the original names.
            # The names were saved in the list original_columns
            DATASET.columns = df_cols
    
    else:
        
        # default case: one of other aggregate functions was selected
        # Guarantee that the columns from the aggregated dataset have the correct names

        # Check if add_suffix_to_aggregated_col is True. If it is, we must add a suffix
        if (add_suffix_to_aggregated_col == True):

            # Now, concatenate the elements from df_cols to the suffix:
            # Start a support list:
            support_list = []

            # loop through each column:
            for column in df_cols:

                if (column == variable_to_group_by):
                    # simply append the column, without adding a suffix.
                    # That is because we will not calculate a statistic for this column, since
                    # it is used to aggregate the others:
                    support_list.append(column)

                else:
                    # Concatenate the column to the suffix and append it to support_list:
                    support_list.append(column + suffix)

            # Now, make the support_list the list of columns itself:
            df_cols = support_list

            # Now, rename the columns of the aggregated dataset as the list
            # df_cols:
            DATASET.columns = df_cols
    
    
    # Now, reset index positions:
    DATASET = DATASET.reset_index(drop = True)
    
    print("Dataframe successfully grouped. Check its 10 first rows:\n")
    print(DATASET.head(10))
    
    if (return_summary_dataframe == True):
        
        print("\n")
        print("Check the summary statistics dataframe, that is also being returned:\n")
        print(summary_agg_df)
        
        return DATASET, summary_agg_df
    
    else:
        # return only the aggregated dataframe:
        return DATASET


def EXTRACT_TIMESTAMP_INFO (df, timestamp_tag_column, list_of_info_to_extract, list_of_new_column_names = None):
    
    import numpy as np
    import pandas as pd
    
    # df: dataframe containing the timestamp.
    
    # timestamp_tag_column: declare as a string under quotes. This is the column from 
    # which we will extract the timestamp.
    
    # list_of_info_to_extract: list of information to extract from the timestamp. Each information
    # will be extracted as a separate column. The allowed values are:
    # 'year', 'month', 'week', 'day', 'hour', 'minute', or 'second'. Declare as a list even if only
    # one information is going to be extracted. For instance:
    # list_of_info_to_extract = ['second'] extracts only the second.
    # list_of_info_to_extract = ['year', 'month', 'week', 'day'] extracts year, month, week and day. 
    
    # list_of_new_column_names: list of names (strings) of the new created columns. 
    # If no value is provided, it will be equals to extracted_info. For instance: if
    # list_of_info_to_extract = ['year', 'month', 'week', 'day'] and list_of_new_column_names = None,
    # the new columns will be named as 'year', 'month', 'week', and 'day'.
    # WARNING: This list must contain the same number of elements of list_of_info_to_extract and both
    # must be in the same order. Considering the same example of list, if list_of_new_column_names =
    # ['col1', 'col2', 'col3', 'col4'], 'col1' will be referrent to 'year', 'col2' to 'month', 'col3'
    # to 'week', and 'col4' to 'day'
    
    
    # Create dataframe local copy to manipulate, avoiding that Pandas operates on
    # the original object; or that Pandas tries to set values on slices or copies,
    # resulting in unpredictable results.
    # Use the copy method to effectively create a second object with the same properties
    # of the input parameters, but completely independent from it.
    DATASET = df.copy(deep = True)
    
    # Check if the list of column names is None. If it is, make it equals to the list of extracted
    # information:
    if (list_of_new_column_names is None):
        
        list_of_new_column_names = list_of_info_to_extract
    
    # START: CONVERT ALL TIMESTAMPS/DATETIMES/STRINGS TO pandas.Timestamp OBJECTS.
    # This will prevent any compatibility problems.
    
    # The pd.Timestamp function can handle a single timestamp per call. Then, we must
    # loop trough the series, and apply the function to each element.
    
    # 1. Start a list to store the Pandas timestamps:
    timestamp_list = []
    
    # 2. Loop through each element of the timestamp column, and apply the function
    # to guarantee that all elements are Pandas timestamps
    
    for timestamp in DATASET[timestamp_tag_column]:
        #Access each element 'timestamp' of the series df[timestamp_tag_column]
        timestamp_list.append(pd.Timestamp(timestamp, unit = 'ns'))
    
    # 3. Save the list as the column timestamp_tag_column itself:
    DATASET[timestamp_tag_column] = timestamp_list
    
    # 4. Sort the dataframe in ascending order of timestamps:
    DATASET = DATASET.sort_values(by = timestamp_tag_column, ascending = True)
    # Reset indices:
    DATASET = DATASET.reset_index(drop = True)
    
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html
    
    #Use the extracted_info as key to access the correct command in the dictionary.
    #To access an item from a dictionary d = {'key1': item1, ...}, declare d['key1'],
    #as if you would do to access a column from a dataframe.
    
    #By doing so, you will select the extraction command from the dictionary:
    # Loop through each element of the dataset, access the timestamp, 
    # extract the information and store it in the correspondent position of the 
    # new_column. Again. The methods can only be applied to a single Timestamp object,
    # not to the series. That is why we must loop through each of them:
    
    
    # Now, loop through each one of the items from the list 'list_of_info_to_extract'.
    # For each element, we will extract the information indicated by that item.
    
    for k in range(0, len(list_of_info_to_extract)):
        
        # loops from k = 0, index of the first element from the list list_of_info_to_extract
        # to k = len(list_of_info_to_extract) - 1, index of the last element of the list
        
        # Access the k-th element of the list list_of_info_to_extract:
        extracted_info = list_of_info_to_extract[k]
        # The element will be referred as 'extracted_info'
        
        # Access the k-th element of the list list_of_new_column_names, which is the
        # name that the new column should have:
        new_column_name = list_of_new_column_names[k]
        # The element will be referred as 'new_column_name'
        
        #start a list to store the values of the new column
        new_column_vals = []

        for i in range(len(DATASET)):
            # i goes from zero to the index of the last element of the dataframe DATASET
            # This element has index len(DATASET) - 1
            # Append the values to the list according to the selected extracted_info

            if (extracted_info == 'year'):

                new_column_vals.append((timestamp_list[i]).year)

            elif (extracted_info == "month"):

                new_column_vals.append((timestamp_list[i]).month)

            elif (extracted_info == "week"):

                new_column_vals.append((timestamp_list[i]).week)

            elif (extracted_info == "day"):

                new_column_vals.append((timestamp_list[i]).day)

            elif (extracted_info == "hour"):

                new_column_vals.append((timestamp_list[i]).hour)

            elif (extracted_info == "minute"):

                new_column_vals.append((timestamp_list[i]).minute)

            elif (extracted_info == "second"):

                new_column_vals.append((timestamp_list[i]).second)

            else:

                print("Invalid extracted information. Please select: year, month, week, day, hour, minute, or second.")

        # Copy the list 'new_column_vals' to a new column of the dataframe, named 'new_column_name':

        DATASET[new_column_name] = new_column_vals
     
    # Pandas .head(Y) method results in a dataframe containing the first Y rows of the 
    # original dataframe. The default .head() is Y = 5. Print first 10 rows of the 
    # new dataframe:
    print("Timestamp information successfully extracted. Check dataset\'s 10 first rows:\n")
    print(DATASET.head(10))
    
    #Now that the information were retrieved from all Timestamps, return the new
    #dataframe:
    
    return DATASET


def CALCULATE_DELAY (df, timestamp_tag_column, new_timedelta_column_name  = None, returned_timedelta_unit = None, return_avg_delay = True):
    
    import numpy as np
    import pandas as pd
    
    #THIS FUNCTION CALCULATES THE DIFFERENCE (timedelta - delay) BETWEEN TWO SUCCESSIVE
    # Timestamps from a same column
    
    #df: dataframe containing the two timestamp columns.
    #timestamp_tag_column: string containing the name of the column with the timestamps
    
    #new_timedelta_column_name: name of the new column. If no value is provided, the default
    #name [timestamp_tag_column1]-[timestamp_tag_column2] will be given:
    
    # return_avg_delay = True will print and return the value of the average delay.
    # return_avg_delay = False will omit this information
    
    if (new_timedelta_column_name is None):
        
        #apply the default name:
        new_timedelta_column_name = "time_delay"
    
    #Pandas Timedelta class: applicable to timedelta objects
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timedelta.html
    #The delta method from the Timedelta class converts returns the timedelta in
    #nanoseconds, guaranteeing the internal compatibility:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timedelta.delta.html#pandas.Timedelta.delta
    
    #returned_timedelta_unit: unit of the new column. If no value is provided, the unit will be
    # considered as nanoseconds. 
    # POSSIBLE VALUES FOR THE TIMEDELTA UNIT:
    #'year', 'month', 'day', 'hour', 'minute', 'second'.
    
    # START: CONVERT ALL TIMESTAMPS/DATETIMES/STRINGS TO pandas.Timestamp OBJECTS.
    # This will prevent any compatibility problems.
    
    #The pd.Timestamp function can handle a single timestamp per call. Then, we must
    # loop trough the series, and apply the function to each element.
    
    # Create dataframe local copy to manipulate, avoiding that Pandas operates on
    # the original object; or that Pandas tries to set values on slices or copies,
    # resulting in unpredictable results.
    # Use the copy method to effectively create a second object with the same properties
    # of the input parameters, but completely independent from it.
    DATASET = df.copy(deep = True)
    
    # 1. Start a list to store the Pandas timestamps:
    timestamp_list = []
    
    # 2. Loop through each element of the timestamp column, and apply the function
    # to guarantee that all elements are Pandas timestamps
    
    for timestamp in DATASET[timestamp_tag_column]:
        #Access each element 'timestamp' of the series df[timestamp_tag_column1]
        timestamp_list.append(pd.Timestamp(timestamp, unit = 'ns'))
    
    # 3. Save the list as the column timestamp_tag_column itself:
    DATASET[timestamp_tag_column] = timestamp_list
    
    # 4. Sort the dataframe in ascending order of timestamps:
    DATASET = DATASET.sort_values(by = timestamp_tag_column, ascending = True)
    # Reset indices:
    DATASET = DATASET.reset_index(drop = True)
    
    # Now, let's create a list of the following timestamps
    following_timestamp = []
    # Let's skip the index 0, correspondent to the first timestamp:
    
    for i in range (1, len(timestamp_list)):
        
        # this loop goes from i = 1 to i = len(timestamp_list) - 1, the last index
        # of the list. If we simply declared range (len(timestamp_list)), the loop
        # will start from 0, the default
        
        #append the element from timestamp_list to following_timestamp:
        following_timestamp.append(timestamp_list[i])
    
    # Notice that this list has one element less than the original list, because we started
    # copying from index 1, not 0. Therefore, let's repeat the last element of timestamp_list:
    following_timestamp.append(timestamp_list[i])
    # Notice that, once we did not restarted the variable i, it keeps its last value obtained
    # during the loop, correspondent to the index of the last element.
    # Now, let's store it into a column (series) of the dataframe:
    timestamp_tag_column2 = timestamp_tag_column + "_delayed"
    DATASET[timestamp_tag_column2] = following_timestamp
    
    # Pandas Timestamps can be subtracted to result into a Pandas Timedelta.
    # We will apply the delta method from Pandas Timedeltas.
    
    # 4. Create a timedelta object as the difference between the timestamps:
    
    # NOTICE: Even though a list could not be submitted to direct operations like
    # sum, subtraction and multiplication, the series and NumPy arrays can. When we
    # copied the list as a new column on the dataframes, we converted the lists to series
    # called df[timestamp_tag_column1] and df[timestamp_tag_column2]. These two series now
    # can be submitted to direct operations.
    
    # Delay = next measurement (tag_column2, timestamp higher) - current measurement
    # (tag_column2, timestamp lower). Since we repeated the last timestamp twice,
    # in the last row it will be subtracted from itself, resulting in zero.
    # This is the expected, since we do not have a delay yet
    timedelta_obj = DATASET[timestamp_tag_column2] - DATASET[timestamp_tag_column]
    
    #This timedelta_obj is a series of timedelta64 objects. The Pandas Timedelta function
    # can process only one element of the series in each call. Then, we must loop through
    # the series to obtain the float values in nanoseconds. Even though this loop may 
    # look unecessary, it uses the Delta method to guarantee the internal compatibility.
    # Then, no errors due to manipulation of timestamps with different resolutions, or
    # due to the presence of global variables, etc. will happen. This is the safest way
    # to manipulate timedeltas.
    
    #5. Create an empty list to store the timedeltas in nanoseconds
    TimedeltaList = []
    
    #6. Loop through each timedelta_obj and convert it to nanoseconds using the Delta
    # method. Both pd.Timedelta function and the delta method can be applied to a 
    # a single object.
    #len(timedelta_obj) is the total of timedeltas present.
    
    for i in range(len(timedelta_obj)):
        
        #This loop goes from i = 0 to i = [len(timedelta_obj) - 1], so that
        #all indices are evaluated.
        
        #append the element resultant from the delta method application on the
        # i-th element of the list timedelta_obj, i.e., timedelta_obj[i].
        TimedeltaList.append(pd.Timedelta(timedelta_obj[i]).delta)
    
    #Notice that the loop is needed because Pandas cannot handle a series/list of
    #Timedelta objects simultaneously. It can manipulate a single object
    # in each call or iteration.
    
    #Now the list contains the timedeltas in nanoseconds and guarantees internal
    #compatibility.
    # The delta method converts the Timedelta object to an integer number equals to the
    # value of the timedelta in nanoseconds. Then we are now dealing with numbers, not
    # with timestamps.
    # Even though some steps seem unecessary, they are added to avoid errors and bugs
    # hard to identify, resultant from a timestamp assigned to the wrong type of
    # object.
    
    #The list is not as the series (columns) and arrays: it cannot be directly submitted to 
    # operations like sum, division, and multiplication. For doing so, we can loop through 
    # each element, what would be the case for using the Pandas Timestamp and Timedelta 
    # functions, which can only manipulate one object per call.
    # For simpler operations like division, we can convert the list to a NumPy array and
    # submit the entire array to the operation at the same time, avoiding the use of 
    # memory consuminh iterative methods.
    
    #Convert the timedelta list to a NumPy array:
    # Notice that we could have created a column with the Timedeltalist, so that it would
    # be converted to a series. On the other hand, we still did not defined the name of the
    # new column. So, it is easier to simply convert it to a NumPy array, and then copy
    # the array as a new column.
    TimedeltaList = np.array(TimedeltaList)
    
    #Convert the array to the desired unit by dividing it by the proper factor:
    
    if (returned_timedelta_unit == 'year'):
        
        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**9) #in seconds
        
        #2. Convert it to minutes (1 min = 60 s):
        TimedeltaList = TimedeltaList / 60.0 #in minutes
        
        #3. Convert it to hours (1 h = 60 min):
        TimedeltaList = TimedeltaList / 60.0 #in hours
        
        #4. Convert it to days (1 day = 24 h):
        TimedeltaList = TimedeltaList / 24.0 #in days
        
        #5. Convert it to years. 1 year = 365 days + 6 h = 365 days + 6/24 h/(h/day)
        # = (365 + 1/4) days = 365.25 days
        
        TimedeltaList = TimedeltaList / (365.25) #in years
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in years. Considered 1 year = 365 days + 6 h.")
    
    
    elif (returned_timedelta_unit == 'month'):
        
        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**9) #in seconds
        
        #2. Convert it to minutes (1 min = 60 s):
        TimedeltaList = TimedeltaList / 60.0 #in minutes
        
        #3. Convert it to hours (1 h = 60 min):
        TimedeltaList = TimedeltaList / 60.0 #in hours
        
        #4. Convert it to days (1 day = 24 h):
        TimedeltaList = TimedeltaList / 24.0 #in days
        
        #5. Convert it to months. Consider 1 month = 30 days
        
        TimedeltaList = TimedeltaList / (30.0) #in months
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in months. Considered 1 month = 30 days.")
        
    
    elif (returned_timedelta_unit == 'day'):
        
        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**9) #in seconds
        
        #2. Convert it to minutes (1 min = 60 s):
        TimedeltaList = TimedeltaList / 60.0 #in minutes
        
        #3. Convert it to hours (1 h = 60 min):
        TimedeltaList = TimedeltaList / 60.0 #in hours
        
        #4. Convert it to days (1 day = 24 h):
        TimedeltaList = TimedeltaList / 24.0 #in days
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in days.")
        
    
    elif (returned_timedelta_unit == 'hour'):
        
        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**9) #in seconds
        
        #2. Convert it to minutes (1 min = 60 s):
        TimedeltaList = TimedeltaList / 60.0 #in minutes
        
        #3. Convert it to hours (1 h = 60 min):
        TimedeltaList = TimedeltaList / 60.0 #in hours
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in hours [h].")
    

    elif (returned_timedelta_unit == 'minute'):
        
        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**9) #in seconds
        
        #2. Convert it to minutes (1 min = 60 s):
        TimedeltaList = TimedeltaList / 60.0 #in minutes
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in minutes [min].")
        
        
    elif (returned_timedelta_unit == 'second'):
        
        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**9) #in seconds
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in seconds [s].")
        
        
    else:
        
        returned_timedelta_unit = 'ns'
        print("No unit or invalid unit provided for timedelta. Then, returned timedelta in nanoseconds (1s = 10^9 ns).")
        
        #In case None unit is provided or a non-valid value or string is provided,
        #The calculus will be in nanoseconds.
    
    #Finally, create a column in the dataframe named as new_timedelta_column_name 
    # with the elements of TimedeltaList converted to the correct unit of time:
    
    #Append the selected unit as a suffix on the new_timedelta_column_name:
    new_timedelta_column_name = new_timedelta_column_name + "_" + returned_timedelta_unit
    
    DATASET[new_timedelta_column_name] = TimedeltaList
      
    # Pandas .head(Y) method results in a dataframe containing the first Y rows of the 
    # original dataframe. The default .head() is Y = 5. Print first 10 rows of the 
    # new dataframe:
    print("Time delays successfully calculated. Check dataset\'s 10 first rows:\n")
    print(DATASET.head(10))
    
    if (return_avg_delay == True):
        
        # Let's calculate the average delay, print and return it:
        # Firstly, we must remove the last element of the TimedeltaList.
        # Remember that this element is 0 because there is no delay. It was added to allow
        # the element-wise operations between the series.
        # Let's eliminate the last element from TimedeltaList. Since this list was already
        # copied to the dataframe, there is no risk of losing information.
        
        # Index of the last element:
        last_element_index = len(TimedeltaList) - 1
        
        # Slice TimedeltaList until the element of index last_element_index - 1.
        # It will eliminate the last element before we obtain the average:
        TimedeltaList = TimedeltaList[:last_element_index]
        # slice[i:j] slices including index i to index j-1; if the first element is not included,
        # the slices goes from the 1st element; if the last element is not included, slices goes to
        # the last element.
        
        # Now we calculate the average value:
        avg_delay = np.average(TimedeltaList)
        
        print(f"Average delay = {avg_delay} {returned_timedelta_unit}")
        
        # Return the dataframe and the average value:
        return DATASET, avg_delay
    
    #Finally, return the dataframe with the new column:
    
    else: 
        # Return only the dataframe
        return DATASET


def CALCULATE_TIMEDELTA (df, timestamp_tag_column1, timestamp_tag_column2, timedelta_column_name  = None, returned_timedelta_unit = None):
    
    import numpy as np
    import pandas as pd
    
    #THIS FUNCTION PERFORMS THE OPERATION df[timestamp_tag_column1] - df[timestamp_tag_colum2]
    #The declaration order will determine the sign of the output.
    
    #df: dataframe containing the two timestamp columns.
    
    #timestamp_tag_column1: string containing the name of the column with the timestamp
    # on the left (from which the right timestamp will be subtracted).
    
    #timestamp_tag_column2: string containing the name of the column with the timestamp
    # on the right, that will be substracted from the timestamp on the left.
    
    #timedelta_column_name: name of the new column. If no value is provided, the default
    #name [timestamp_tag_column1]-[timestamp_tag_column2] will be given:
    
    if (timedelta_column_name is None):
        
        #apply the default name:
        timedelta_column_name = "[" + timestamp_tag_column1 + "]" + "-" + "[" + timestamp_tag_column2 + "]"
    
    #Pandas Timedelta class: applicable to timedelta objects
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timedelta.html
    #The delta method from the Timedelta class converts the timedelta to
    #nanoseconds, guaranteeing the internal compatibility:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timedelta.delta.html#pandas.Timedelta.delta
    
    #returned_timedelta_unit: unit of the new column. If no value is provided, the unit will be
    # considered as nanoseconds. 
    # POSSIBLE VALUES FOR THE TIMEDELTA UNIT:
    #'year', 'month', 'day', 'hour', 'minute', 'second'.
    
    # START: CONVERT ALL TIMESTAMPS/DATETIMES/STRINGS TO pandas.Timestamp OBJECTS.
    # This will prevent any compatibility problems.
    
    #The pd.Timestamp function can handle a single timestamp per call. Then, we must
    # loop trough the series, and apply the function to each element.
    
    # Create dataframe local copy to manipulate, avoiding that Pandas operates on
    # the original object; or that Pandas tries to set values on slices or copies,
    # resulting in unpredictable results.
    # Use the copy method to effectively create a second object with the same properties
    # of the input parameters, but completely independent from it.
    DATASET = df.copy(deep = True)
    
    
    # 1. Start a list to store the Pandas timestamps:
    timestamp_list = []
    
    # 2. Loop through each element of the timestamp column, and apply the function
    # to guarantee that all elements are Pandas timestamps
    
    for timestamp in DATASET[timestamp_tag_column1]:
        #Access each element 'timestamp' of the series df[timestamp_tag_column1]
        timestamp_list.append(pd.Timestamp(timestamp, unit = 'ns'))
    
    # 3. Create a column in the dataframe that will store the timestamps.
    # Simply copy the list as the column:
    DATASET[timestamp_tag_column1] = timestamp_list
    
    #Repeate these steps for the other column (timestamp_tag_column2):
    # Restart the list, loop through all the column, and apply the pd.Timestamp function
    # to each element, individually:
    timestamp_list = []
    
    for timestamp in DATASET[timestamp_tag_column2]:
        #Access each element 'timestamp' of the series df[timestamp_tag_column2]
        timestamp_list.append(pd.Timestamp(timestamp, unit = 'ns'))
    
    DATASET[timestamp_tag_column2] = timestamp_list
    
    # Pandas Timestamps can be subtracted to result into a Pandas Timedelta.
    # We will apply the delta method from Pandas Timedeltas.
    
    #4. Create a timedelta object as the difference between the timestamps:
    
    # NOTICE: Even though a list could not be submitted to direct operations like
    # sum, subtraction and multiplication, the series and NumPy arrays can. When we
    # copied the list as a new column on the dataframes, we converted the lists to series
    # called df[timestamp_tag_column1] and df[timestamp_tag_column2]. These two series now
    # can be submitted to direct operations.
    
    timedelta_obj = DATASET[timestamp_tag_column1] - DATASET[timestamp_tag_column2]
    
    #This timedelta_obj is a series of timedelta64 objects. The Pandas Timedelta function
    # can process only one element of the series in each call. Then, we must loop through
    # the series to obtain the float values in nanoseconds. Even though this loop may 
    # look unecessary, it uses the Delta method to guarantee the internal compatibility.
    # Then, no errors due to manipulation of timestamps with different resolutions, or
    # due to the presence of global variables, etc. will happen. This is the safest way
    # to manipulate timedeltas.
    
    #5. Create an empty list to store the timedeltas in nanoseconds
    TimedeltaList = []
    
    #6. Loop through each timedelta_obj and convert it to nanoseconds using the Delta
    # method. Both pd.Timedelta function and the delta method can be applied to a 
    # a single object.
    #len(timedelta_obj) is the total of timedeltas present.
    
    for i in range(len(timedelta_obj)):
        
        #This loop goes from i = 0 to i = [len(timedelta_obj) - 1], so that
        #all indices are evaluated.
        
        #append the element resultant from the delta method application on the
        # i-th element of the list timedelta_obj, i.e., timedelta_obj[i].
        TimedeltaList.append(pd.Timedelta(timedelta_obj[i]).delta)
    
    #Notice that the loop is needed because Pandas cannot handle a series/list of
    #Timedelta objects simultaneously. It can manipulate a single object
    # in each call or iteration.
    
    #Now the list contains the timedeltas in nanoseconds and guarantees internal
    #compatibility.
    # The delta method converts the Timedelta object to an integer number equals to the
    # value of the timedelta in nanoseconds. Then we are now dealing with numbers, not
    # with timestamps.
    # Even though some steps seem unecessary, they are added to avoid errors and bugs
    # hard to identify, resultant from a timestamp assigned to the wrong type of
    # object.
    
    #The list is not as the series (columns) and arrays: it cannot be directly submitted to 
    # operations like sum, division, and multiplication. For doing so, we can loop through 
    # each element, what would be the case for using the Pandas Timestamp and Timedelta 
    # functions, which can only manipulate one object per call.
    # For simpler operations like division, we can convert the list to a NumPy array and
    # submit the entire array to the operation at the same time, avoiding the use of 
    # memory consuminh iterative methods.
    
    #Convert the timedelta list to a NumPy array:
    # Notice that we could have created a column with the Timedeltalist, so that it would
    # be converted to a series. On the other hand, we still did not defined the name of the
    # new column. So, it is easier to simply convert it to a NumPy array, and then copy
    # the array as a new column.
    TimedeltaList = np.array(TimedeltaList)
    
    #Convert the array to the desired unit by dividing it by the proper factor:
    
    if (returned_timedelta_unit == 'year'):
        
        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**9) #in seconds
        
        #2. Convert it to minutes (1 min = 60 s):
        TimedeltaList = TimedeltaList / 60.0 #in minutes
        
        #3. Convert it to hours (1 h = 60 min):
        TimedeltaList = TimedeltaList / 60.0 #in hours
        
        #4. Convert it to days (1 day = 24 h):
        TimedeltaList = TimedeltaList / 24.0 #in days
        
        #5. Convert it to years. 1 year = 365 days + 6 h = 365 days + 6/24 h/(h/day)
        # = (365 + 1/4) days = 365.25 days
        
        TimedeltaList = TimedeltaList / (365.25) #in years
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in years. Considered 1 year = 365 days + 6 h.")
    
    
    elif (returned_timedelta_unit == 'month'):
        
        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**9) #in seconds
        
        #2. Convert it to minutes (1 min = 60 s):
        TimedeltaList = TimedeltaList / 60.0 #in minutes
        
        #3. Convert it to hours (1 h = 60 min):
        TimedeltaList = TimedeltaList / 60.0 #in hours
        
        #4. Convert it to days (1 day = 24 h):
        TimedeltaList = TimedeltaList / 24.0 #in days
        
        #5. Convert it to months. Consider 1 month = 30 days
        
        TimedeltaList = TimedeltaList / (30.0) #in months
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in months. Considered 1 month = 30 days.")
        
    
    elif (returned_timedelta_unit == 'day'):
        
        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**9) #in seconds
        
        #2. Convert it to minutes (1 min = 60 s):
        TimedeltaList = TimedeltaList / 60.0 #in minutes
        
        #3. Convert it to hours (1 h = 60 min):
        TimedeltaList = TimedeltaList / 60.0 #in hours
        
        #4. Convert it to days (1 day = 24 h):
        TimedeltaList = TimedeltaList / 24.0 #in days
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in days.")
        
    
    elif (returned_timedelta_unit == 'hour'):
        
        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**9) #in seconds
        
        #2. Convert it to minutes (1 min = 60 s):
        TimedeltaList = TimedeltaList / 60.0 #in minutes
        
        #3. Convert it to hours (1 h = 60 min):
        TimedeltaList = TimedeltaList / 60.0 #in hours
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in hours [h].")
    

    elif (returned_timedelta_unit == 'minute'):
        
        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**9) #in seconds
        
        #2. Convert it to minutes (1 min = 60 s):
        TimedeltaList = TimedeltaList / 60.0 #in minutes
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in minutes [min].")
        
        
    elif (returned_timedelta_unit == 'second'):
        
        #1. Convert the list to seconds (1 s = 10**9 ns, where 10**9 represents
        #the potentiation operation in Python, i.e., 10^9. e.g. 10**2 = 100):
        TimedeltaList = TimedeltaList / (10**9) #in seconds
        
        #The .0 after the numbers guarantees a float division.
        
        print("Returned timedelta in seconds [s].")
        
        
    else:
        
        returned_timedelta_unit = 'ns'
        print("No unit or invalid unit provided for timedelta. Then, returned timedelta in nanoseconds (1s = 10^9 ns).")
        
        #In case None unit is provided or a non-valid value or string is provided,
        #The calculus will be in nanoseconds.
    
    #Finally, create a column in the dataframe named as timedelta_column_name 
    # with the elements of TimedeltaList converted to the correct unit of time:
    
    #Append the selected unit as a suffix on the timedelta_column_name:
    timedelta_column_name = timedelta_column_name + "_" + returned_timedelta_unit
    
    DATASET[timedelta_column_name] = TimedeltaList
    
    # Sort the dataframe in ascending order of timestamps.
    # Importance order: timestamp1, timestamp2, timedelta
    DATASET = DATASET.sort_values(by = [timestamp_tag_column1, timestamp_tag_column2, timedelta_column_name], ascending = [True, True, True])
    # Reset indices:
    DATASET = DATASET.reset_index(drop = True)
    
    # Pandas .head(Y) method results in a dataframe containing the first Y rows of the 
    # original dataframe. The default .head() is Y = 5. Print first 10 rows of the 
    # new dataframe:
    print("Timedeltas successfully calculated. Check dataset\'s 10 first rows:\n")
    print(DATASET.head(10))
    
    #Finally, return the dataframe with the new column:
    
    return DATASET


def ADD_TIMEDELTA (df, timestamp_tag_column, timedelta, new_timestamp_col  = None, timedelta_unit = None):
    
    import numpy as np
    import pandas as pd
    
    #THIS FUNCTION PERFORMS THE OPERATION ADDING A FIXED TIMEDELTA (difference of time
    # or offset) to a timestamp.
    
    #df: dataframe containing the timestamp column.
    
    #timestamp_tag_column: string containing the name of the column with the timestamp
    # to which the timedelta will be added to.
    
    #timedelta: numeric value of the timedelta.
    # WARNING: simply input a numeric value, not a string with unit. e.g. timedelta = 2.4
    # If you want to subtract a timedelta, input a negative value. e.g. timedelta = - 2.4
    
    #new_timestamp_col: name of the new column containing the obtained timestamp. 
    # If no value is provided, the default name [timestamp_tag_column]+[timedelta] 
    # will be given (at the end of the code, after we created the timedelta object 
    # with correct units)
    
    #Pandas Timedelta class: applicable to timedelta objects
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timedelta.html
    #The delta method from the Timedelta class converts returns the timedelta in
    #nanoseconds, guaranteeing the internal compatibility:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timedelta.delta.html#pandas.Timedelta.delta
    
    #timedelta_unit: unit of the timedelta interval. If no value is provided, 
    # the unit will be considered 'ns' (default). Possible values are:
    #'day', 'hour', 'minute', 'second', 'ns'.
    
    if (timedelta_unit is None):
        
        timedelta_unit = 'ns'
    
    # Pandas do not support timedeltas in years or months, since these values may
    # be ambiguous (e.g. a month may have 30 or 31 days, so an approximation would
    # be necessary).
    
    # START: CONVERT ALL TIMESTAMPS/DATETIMES/STRINGS TO pandas.Timestamp OBJECTS.
    # This will prevent any compatibility problems.
    
    #The pd.Timestamp function can handle a single timestamp per call. Then, we must
    # loop trough the series, and apply the function to each element.
    
    # Create dataframe local copy to manipulate, avoiding that Pandas operates on
    # the original object; or that Pandas tries to set values on slices or copies,
    # resulting in unpredictable results.
    # Use the copy method to effectively create a second object with the same properties
    # of the input parameters, but completely independent from it.
    DATASET = df.copy(deep = True)
    
    #1. Start a list to store the Pandas timestamps:
    timestamp_list = []
    
    #2. Loop through each element of the timestamp column, and apply the function
    # to guarantee that all elements are Pandas timestamps
    
    for timestamp in DATASET[timestamp_tag_column]:
        #Access each element 'timestamp' of the series df[timestamp_tag_column1]
        timestamp_list.append(pd.Timestamp(timestamp, unit = 'ns'))
    
    #3. Create a column in the dataframe that will store the timestamps.
    # Simply copy the list as the column:
    DATASET[timestamp_tag_column] = timestamp_list
    
    # The Pandas Timestamp can be directly added to a Pandas Timedelta.
 
    #Dictionary for converting the timedelta_unit to Pandas encoding for the
    # Timedelta method. to access the element of a dictionary d = {"key": element},
    # simply declare d['key'], as if you were accessing the column of a dataframe. Here,
    # the key is the argument of the function, whereas the element is the correspondent
    # Pandas encoding for this method. With this dictionary we simplify the search for the
    # proper time encoding: actually, depending on the Pandas method the encoding may be
    # 'd', "D" or "day" for day, for instance. So, we avoid having to check the whole
    # documentation by creating a simpler common encoding for the functions in this notebook.
    
    unit_dict = {
        
        'day': 'd',
        'hour': 'h',
        'minute': 'min',
        'second': 's',
        'ns': 'ns'
        
    }
    
    #Create the Pandas timedelta object from the timedelta value and the selected
    # time units:
    timedelta = pd.Timedelta(timedelta, unit_dict[timedelta_unit])
    
    #A pandas Timedelta object has total compatibility with a pandas
    #Timestamp, so we can simply add the Timedelta to the Timestamp to obtain a new 
    #corrected timestamp.
    # Again, notice that the timedelta can be positive (sum of time), or negative
    # (subtraction of time).
    
    #Now, add the timedelta to the timestamp, and store it into a proper list/series:
    new_timestamps = DATASET[timestamp_tag_column] + timedelta
     
    #Finally, create a column in the dataframe named as new_timestamp_col
    #and store the new timestamps into it
    
    if (new_timestamp_col is None):
        
        #apply the default name:
        new_timestamp_col = "[" + timestamp_tag_column + "]" + "+" + "[" + str(timedelta) + "]"
        #The str function converts the timedelta object to a string, so it can be
        #concatenated in this line of code.
        #Notice that we defined the name of the new column at the end of the code so
        #that we already converted the 'timedelta' to a Timedelta object containing
        #the correct units.
    
    DATASET[new_timestamp_col] = new_timestamps
    
    # Sort the dataframe in ascending order of timestamps.
    # Importance order: timestamp, new_timestamp_col
    DATASET = DATASET.sort_values(by = [timestamp_tag_column, new_timestamp_col], ascending = [True, True])
    # Reset indices:
    DATASET = DATASET.reset_index(drop = True)
    
    # Pandas .head(Y) method results in a dataframe containing the first Y rows of the 
    # original dataframe. The default .head() is Y = 5. Print first 10 rows of the 
    # new dataframe:
    print("Timedeltas successfully added. Check dataset\'s 10 first rows:\n")
    print(DATASET.head(10))
    
    #Finally, return the dataframe with the new column:
    
    return DATASET


def SLICE_DATAFRAME (df, from_row = 'first_only', to_row = 'only', restart_index_of_the_sliced_dataframe = False):
    
    import numpy as np
    import pandas as pd
    
    # restart_index_of_the_sliced_dataframe = False to keep the 
    # same row index of the original dataframe; or 
    # restart_index_of_the_sliced_dataframe = True to reset indices 
    # (start a new index, from 0 for the first row of the 
    # returned dataframe).
    
    # from_row and to_row: integer or strings:
    
    # from_row may be any integer from 0 to the last row of the dataset
    # and the following strings: 'first' and 'first_only'
    
    # to_row may be any integer from 0 to the last row of the dataset
    # and the following strings: 'last', 'last_only', and 'only'
    
    # the combination from_row = 'first', to_row = 'last' will
    # return the original dataframe itself.
    # The same is valid for the combination from_row = 'first_only', 
    # to_row = 'last_only'; or of combinations between from_row = 0
    # (index of the first row) with 'last' or the index
    # of the last row; or combinations between 'first' and the index
    # of the last row.
    
    # These possibilities are the first checked by the code. If none
    # of these special cases are present, then:
    
    # from_row = 'first_only' selects a dataframe containing only the
    # first row, independently of the parameter passed as to_row;
    
    # to_row = 'last_only' selects a dataframe containing only the
    # last row, independently of the parameter passed as from_row;
    
    # if to_row = 'only', the sliced dataframe will be formed by only the
    # row passed as from_row (an integer representing the row index is
    # passed) - explained in the following lines
    
    # These three special cases are dominant over the following ones
    # (they are checked firstly, and force the modifying of slicing
    # limits):
    
    # Other special cases:
    
    # from_row = 'first' starts slicing on the first row (index 0) -
    # the 1st row from the dataframe will be the 1st row of the sliced
    # dataframe too.
    
    # to_row = 'last' finishes slicing in the last row - the last row
    # from the dataframe will be the last row of the sliced dataframe.
    
    # If i and j are integer numbers, they represent the indices of rows:
    
    # from_row = i starts the sliced dataframe from the row of index i
    # of the original dataframe.
    # e.g. from_row = 8 starts the slicing from row with index 8. Since
    # slicing starts from 0, this is the 9th row of the original dataframe.
    
    # to_row = j finishes the sliced dataframe on the row of index j of
    # the original dataframe. Attention: this row with index j is included,
    # and will be the last_row of the sliced dataframe.
    # e.g. if to_row = 21, the last row of the sliced dataframe will be the
    # row with index 21 of the original dataframe. Since slicing starts
    # from 0, this is the 22nd row of the original dataframe.
    
    # In summary, if from_row = 8, to_row = 21, the sliced dataframe
    # will be formed from the row of index 8 to the row of index 21 of
    # the original dataframe, including both the row of index 8 and the row
    # index 21. 
    
    # from_row is effectively the first row of the new dataframe;
    # and to_row is effectively the last row of the new dataframe.
    
    # Notice that the use of to_row < from_row will raise an error.
    
    # Create dataframe local copy to manipulate, avoiding that Pandas operates on
    # the original object; or that Pandas tries to set values on slices or copies,
    # resulting in unpredictable results.
    # Use the copy method to effectively create a second object with the same properties
    # of the input parameters, but completely independent from it.
    DATASET = df.copy(deep = True)
    
    # Store the total number of rows as num_rows:
    num_rows = len(DATASET)
    
    
    # Check if no from_row and to_row arguments were provided:
    if (from_row is None):
        print("No input for the argument \'from_row\'. Then, setting the start of the slice as the first row.\n")
        first_row_index = 0
    
    if (to_row is None):
        print("No input for the argument \'to_row\'. Then, setting the end of the slice as the last row.\n")
        last_row_index = (num_rows - 1)
    
    
    # Check type of the inputs (strings or integers):
    from_row_type = type(from_row)
    to_row_type = type(to_row)
    
    if (from_row_type == str):
        # It is a string
        
        if ((from_row == 'first') | (from_row == 'first_only')):
            # Set the first_row_index as the 0 (1st row index):
            first_row_index = 0
        
        else:
            print("Invalid string input for the argument \'from_row\'. Then, setting the start of the slice as the first row.\n")
            first_row_index = 0
    
    else:
        # Numeric input. Use the int attribute to guarantee that it 
        # was read as an integer. This value is itself the index of
        # the first row of the sliced dataframe:
        first_row_index = int(from_row)
    
    
    if (to_row_type == str):
        # It is a string
        
        if ((to_row == 'last') | (to_row == 'last_only')):
            # Set the last_row_index as the index of the last row of the dataframe:
            last_row_index = (num_rows - 1)
            # In the following code, we do last_row_index = last_row_index + 1 to
            # guarantee that the last row is actually included in the sliced df.
            
            # If to_row == 'last_only', we must correct first_row_index:
            # first_row_index was previously defined as 0 or as the value of the row
            # index provided. It must be the index of the last row, though:
            if (to_row == 'last_only'):
                first_row_index = last_row_index
                print("\'last_only\' argument provided, so starting the slicing from the last row of the dataframe.\n")
            
        elif (to_row == 'only'):
            # Use only the row declared as from_row
            last_row_index = first_row_index
            # In the following code, we do last_row_index = last_row_index + 1 to
            # guarantee that the last row is actually included in the sliced df.
        
        else:
            print("Invalid string input for the argument \'to_row\'. Then, setting the end of the slice as the last row.\n")
            last_row_index = (num_rows - 1)
    
    elif (from_row == 'first_only'):
        # In this case, last row index must be zero:
        last_row_index = 0
    
    else:
        # Numeric input. Use the int attribute to guarantee that it 
        # was read as an integer. This value is itself the index of
        # the last row of the sliced dataframe:
        last_row_index = int(to_row)
    
    
    # Check the special combination from = 1st row to last row
    # and return the original dataframe itself, without performing
    # operations:
    
    if ((from_row == 'first_only') & (to_row == 'last_only')):
        
        #return the dataframe without performing any operation
        print("Sliced dataframe is the original dataframe itself.")
        return DATASET
    
    elif ((first_row_index == 0) & (last_row_index == (num_rows - 1))):
        
        #return the dataframe without performing any operation
        print("Sliced dataframe is the original dataframe itself.")
        return DATASET
         
    # The two special combinations were checked, now we can back to
    # the main code
    
    
    # Slice a dataframe: df[i:j]
    # Slice the dataframe, getting only row i to row (j-1)
    # Indexing naturally starts from 0
    # Notice that the slicer defined as df[i:j] takes all columns from
    # the dataframe: it copies the dataframe structure (columns), but
    # selects only the specified rows.
    
    # first_row = df[0:1]
    # This is equivalent to df[:1] - if there is no start for the
    # slicer, the start from 0 is implicit
    # slice: get rows from row 0 to row (1-1) = 0
    # Therefore, we will obtain a copy of the dataframe, but containing
    # only the first row (row 0)
    
    # last_row = df[(num_rows - 1):(num_rows)] 
    # slice the dataframe from row (num_rows - 1), the index of the
    # last row, to row (num_rows) - 1 = (num_rows - 1)
    # Therefore, this slicer is a copy of the dataframe but containing
    # only its last row.
    
    # Slices are (fractions of) pandas dataframes, so elements must be
    # accessed through .iloc or .loc method
    
    
    # Set slicing limits:
    i = first_row_index # i is included
    j = last_row_index + 1
    # df[i:j] will include row i to row j - 1 = 
    # (last_row_index + 1) - 1 = last_row_index
    # Then, by summing 1 we guarantee that the row passed as
    # last_row_index will be actually included.
    # notice that when last_row_index = first_row_index
    # j will be the index of the next line.
    # e.g. the slice of only the first line must be df[0:1]
    # there must be a difference of 1 to include 1 line.
    
    # Now, slice the dataframe from line of index i to
    # line j-1, where line (j-1) is the last one included:
    
    sliced_df = DATASET[i:j]
    
    if (restart_index_of_the_sliced_dataframe == True):
        # Reset the index:
        sliced_df = sliced_df.reset_index(drop = True)
        print("Index of the returned dataframe was restarted.")
    
    print(f"Returning sliced dataframe, containing {sliced_df.shape[0]} rows and {sliced_df.shape[1]} columns.")
    # dataframe.shape is a tuple (N, M), where dataframe.shape[0] = N is
    # the number of rows; and dataframe.shape[1] = M is the number of columns
    # of the dataframe
    
    print("Check the dataframe below:\n")
    print(sliced_df)
    
    return sliced_df


def visualize_and_characterize_missing_values (df, slice_time_window_from = None, slice_time_window_to = None, aggregate_time_in_terms_of = None):

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import missingno as msno
    # misssingno package is built for visualizing missing values. 
    
    # df: dataframe to be analyzed
    
    # slice_time_window_from and slice_time_window_to (timestamps). When analyzing time series,
    # use these parameters to observe only values in a given time range.
    
    # slice_time_window_from: the inferior limit of the analyzed window. If you declare this value
    # and keep slice_time_window_to = None, then you will analyze all values that comes after
    # slice_time_window_from.
    # slice_time_window_to: the superior limit of the analyzed window. If you declare this value
    # and keep slice_time_window_from = None, then you will analyze all values until
    # slice_time_window_to.
    # If slice_time_window_from = slice_time_window_to = None, only the standard analysis with
    # the whole dataset will be performed. If both values are specified, then the specific time
    # window from 'slice_time_window_from' to 'slice_time_window_to' will be analyzed.
    # e.g. slice_time_window_from = 'May-1976', and slice_time_window_to = 'Jul-1976'
    # Notice that the timestamps must be declares in quotes, just as strings.
    
    # aggregate_time_in_terms_of = None. Keep it None if you do not want to aggregate the time
    # series. Alternatively, set aggregate_time_in_terms_of = 'Y' or aggregate_time_in_terms_of = 
    # 'year' to aggregate the timestamps in years; set aggregate_time_in_terms_of = 'M' or
    # 'month' to aggregate in terms of months; or set aggregate_time_in_terms_of = 'D' or 'day'
    # to aggregate in terms of days.
    
    print("Possible reasons for missing data:\n")
    print("One of the obvious reasons is that data is simply missing at random.")
    print("Other reasons might be that the missingness is dependent on another variable;")
    print("or it is due to missingness of the same variables or other variables.\n")
    
    print("Types of missingness:\n")
    print("Identifying the missingness type helps narrow down the methodologies that you can use for treating missing data.")
    print("We can group the missingness patterns into 3 broad categories:\n")
    
    print("Missing Completely at Random (MCAR)\n")
    print("Missingness has no relationship between any values, observed or missing.")
    print("Example: consider you have a class of students. There are a few students absent on any given day. The students are absent just randomly for their specific reasons. This is missing completely at random.\n")
    
    print("Missing at Random (MAR)\n")
    print("There is a systematic relationship between missingness and other observed data, but not the missing data.")
    print("Example: consider the attendance in a classroom of students during winter, where many students are absent due to the bad weather. Although this might be at random, the hidden cause might be that students sitting closer might have contracted a fever.\n")
    print("Missing at random means that there might exist a relationship with another variable.")
    print("In this example, the attendance is slightly correlated to the season of the year.")
    print("It\'s important to notice that, for MAR, missingness is dependent only on the observed values; and not the other missing values.\n")
    
    print("Missing not at Random (MNAR)\n")
    print("There is a relationship between missingness and its values, missing or non-missing.")
    print("Example: in our class of students, it is Sally\'s birthday. Sally and many of her friends are absent to attend her birthday party. This is not at all random as Sally and only her friends are absent.\n")
    
    # Start the agg_dict, a dictionary that correlates the input aggregate_time_in_terms_of to
    # the correspondent argument that must be passed to the matrix method:
    agg_dict = {
        
        'year': 'Y',
        'Y': 'Y',
        'month': 'M',
        'M': 'M',
        'day': 'D',
        'D':'D'
    }
    
    
    if not (aggregate_time_in_terms_of is None):
        # access the frequency in the dictionary
        frequency = agg_dict[aggregate_time_in_terms_of] 
    
    df_length = len(df)
    print(f"Total of rows of the dataframe = {df_length}\n")

    total_of_missing_values = df.isna().sum()
    print("Total of missing values for each feature:\n")
    print(total_of_missing_values)
    print("\n") # line_break
    
    percent_of_missing_values = (df.isna().mean()) * 100
    print("Percent (%) of missing values for each feature:\n")
    print(percent_of_missing_values)
    print("\n") # line_break
    
    print("Bar chart of the missing values - Nullity bar:\n")
    msno.bar(df)
    plt.show()
    print("\n")
    print("The nullity bar allows us to visualize the completeness of the dataframe.\n")
    
    print("Nullity Matrix: distribution of missing values through the dataframe:\n")
    msno.matrix(df)
    plt.show()
    print("\n")
    
    if not ((slice_time_window_from is None) | (slice_time_window_to is None)):
        
        # There is at least one of these two values for slicing:
        if not ((slice_time_window_from is None) & (slice_time_window_to is None)):
                # both are present
                
                if not (aggregate_time_in_terms_of is None):
                    print("Nullity matrix for the defined time window and for the selected aggregation frequency:\n")
                    msno.matrix(df.loc[slice_time_window_from:slice_time_window_to], freq = frequency)
                    
                else:
                    # do not aggregate:
                    print("Nullity matrix for the defined time window:\n")
                    msno.matrix(df.loc[slice_time_window_from:slice_time_window_to])
                
                plt.show()
                print("\n")
        
        elif not (slice_time_window_from is None):
            # slice only from the start. The condition where both limits were present was already
            # checked. To reach this condition, only one is not None
            # slice from 'slice_time_window_from' to the end of dataframe
            
                if not (aggregate_time_in_terms_of is None):
                    print("Nullity matrix for the defined time window and for the selected aggregation frequency:\n")
                    msno.matrix(df.loc[slice_time_window_from:], freq = frequency)
                
                else:
                    # do not aggregate:
                    print("Nullity matrix for the defined time window:\n")
                    msno.matrix(df.loc[slice_time_window_from:])
        
                plt.show()
                print("\n")
            
        else:
        # equivalent to elif not (slice_time_window_to is None):
            # slice only from the beginning to the upper limit. 
            # The condition where both limits were present was already checked. 
            # To reach this condition, only one is not None
            # slice from the beginning to 'slice_time_window_to'
            
                if not (aggregate_time_in_terms_of is None):
                    print("Nullity matrix for the defined time window and for the selected aggregation frequency:\n")
                    msno.matrix(df.loc[:slice_time_window_to], freq = frequency)
                
                else:
                    # do not aggregate:
                    print("Nullity matrix for the defined time window:\n")
                    msno.matrix(df.loc[:slice_time_window_to])
                
                plt.show()
                print("\n")
    
    else:
        # Both slice limits are not. Let's check if we have to aggregate the dataframe:
        if not (aggregate_time_in_terms_of is None):
                print("Nullity matrix for the selected aggregation frequency:\n")
                msno.matrix(df, freq = frequency)
                plt.show()
                print("\n")
    
    print("The nullity matrix allows us to visualize the location of missing values in the dataset.")
    print("The nullity matrix describes the nullity in the dataset and appears blank wherever there are missing values.")
    print("It allows us to quickly analyze the patterns in missing values.")
    print("The sparkline on the right of the matrix summarizes the general shape of data completeness and points out the row with the minimum number of null values in the dataframe.")
    print("In turns, the nullity matrix shows the total counts of columns at its bottom.")
    print("We can previously slice the dataframe for a particular interval of analysis (e.g. slice the time interval) to obtain more clarity on the amount of missingness.")
    print("Slicing will be particularly helpful when analyzing large datasets.\n")
    print("MCAR: plotting the missingness matrix plot (nullity matrix) for a MCAR variable will show values missing at random, with no correlation or clear pattern.")
    print("Correlation here implies the dependency of missing values on another variable present or absent.\n")
    print("MAR: the nullity matrix for MAR can be visualized as the presence of many missing values for a given feature. In this case, there might be a reason for the missingness that cannot be directly observed.\n")
    print("MNAR: the nullity matrix for MNAR shows a strong correlation between the missingness of two variables A and B.")
    print("This correlation is easily observable by sorting the dataframe in terms of A or B before obtaining the matrix.\n")
    
    print("Missingness Heatmap:\n")
    msno.heatmap(df)
    plt.show()
    print("\n")
    
    print("The missingness heatmap describes the correlation of missingness between columns.")
    print("The heatmap is a graph of correlation of missing values between columns.")
    print("It explains the dependencies of missingness between columns.")
    print("In simple terms, if the missingness for two columns are highly correlated, then the heatmap will show high values of coefficient of correlation R2 for them.")
    print("That is because columns where the missing values co-occur the maximum are highly related and vice-versa.\n")
    print("In the graph, the redder the color, the lower the correlation between the missing values of the columns.")
    print("In turns, the bluer the color, the higher the correlation of missingness between the two variables.\n")
    print("ATTENTION: before deciding if the missing values in one variable is correlated with other, so that they would be characterized as MAR or MNAR, check the total of missing values.")
    print("Even if the heatmap shows a certain degree of correlation, the number of missing values may be too small to substantiate that.")
    print("Missingness in very small number may be considered completely random, and missing values can be eliminated.\n")
    
    print("Missingness Dendrogram:\n")
    msno.dendrogram(df)
    plt.show()
    print("\n")
    
    print("A dendrogram is a tree diagram that groups similar objects in close branches.")
    print("So, the missingness dendrogram is a tree diagram of missingness that describes correlation of variables by grouping similarly missing columns together.")
    print("To interpret this graph, read it from a top-down perspective.")
    print("Cluster leaves which are linked together at a distance of zero fully predict one another\'s presence.")
    print("In other words, when two variables are grouped together in the dendogram, one variable might always be empty while another is filled (the presence of one explains the missingness of the other), or they might always both be filled or both empty, and so on (the missingness of one explains the missigness of the other).\n")
    
    return total_of_missing_values, percent_of_missing_values


def visualizing_and_comparing_missingness_across_numeric_vars (df, column_to_analyze, column_to_compare_with, show_interpreted_example = False, grid = True, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    import os
    # Two conditions require the os library, so we import it at the beginning of the function,
    # to avoid importing it twice.
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    
    # column_to_analyze, column_to_compare_with: strings (in quotes).
    # column_to_analyze is the column from the dataframe df that will be analyzed in terms of
    # missingness; whereas column_to_compare_with is the column to which column_to_analyze will
    # be compared.
    # e.g. column_to_analyze = 'column1' will analyze 'column1' from df.
    # column_to_compare_with = 'column2' will compare 'column1' against 'column2'
    
    # show_interpreted_example: set as True if you want to see an example of a graphic analyzed and
    # interpreted.
    
    print("Missingness across a variable:\n")
    print("In this analysis, we will graphically analyze the relationship between missing values and non-missing values.")
    print("To do so, we will start by visualizing the missingness of a variable against another variable.")
    print("The scatter plot will show missing values in one color, and non-missing values in other color.")
    print("It will allow us to visualize how missingness of a variable changes against another variable.")
    print("Analyzing the missingness of a variable against another variable helps you determine any relationships between missing and non-missing values.")
    print("This is very similar to how you found correlations of missingness between two columns.")
    print("In summary, we will plot a scatter plot to analyze if there is any correlation of missingness in one column against another column.\n")
    
    # To create the graph, we will use the matplotlib library. 
    # However, matplotlib skips all missing values while plotting. 
    # Therefore, we would need to first create a function that fills in dummy values for all the 
    # missing values in the DataFrame before plotting.
    
    # We will create a function 'fill_dummy_values' that fill in all columns in the DataFrame.
    #The operations involve shifting and scaling the column range with a scaling factor.
        
    # We use a for loop to produce dummy values for all the columns in a given DataFrame. 
    # We can also define the scaling factor so that we can resize the range of dummy values. 
    # In addition to the previous steps of scaling and shifting the dummy values, we'll also have to 
    # create a copy of the DataFrame to fill in dummy values first. Let's now use this function to 
    # create our scatterplot.
    
    # define a subfunction for filling the dummy values.
    # In your function definition, set the default value of scaling_factor to be 0.075:
    def fill_dummy_values(df, scaling_factor = 0.075):
        
        # To generate dummy values, we can use the 'rand()' function from 'numpy.random'. 
        # We first store the number of missing values in column_to_analyze to 'num_nulls'
        # and then generate an array of random dummy values of the size 'num_nulls'. 
        # The generated dummy values appear as shown beside on the graph. 
        
        # The rand function always outputs values between 0 and 1. 
        # However, you must observe that the values of both column_to_analyze and column_to_compare_with 
        # have their own ranges, that may be different. 
        # Hence we'll need to scale and shift the generated dummy values so that they nicely fit 
        # into the graph.
        
        from numpy.random import rand
        # https://numpy.org/doc/stable/reference/random/generated/numpy.random.rand.html?msclkid=7414313ace7611eca18491dd4e7e86ae
        
        df_dummy = df.copy(deep = True)
        # Get the list of columns from df_dummy.
        # Use the list attribute to convert the array df_dummy.columns to list:
        df_cols_list = list(df_dummy.columns)
        
        # Calculate the number of missing values in each column of the dummy DataFrame.
        for col_name in df_dummy:
            
            col = df_dummy[col_name]
            # Create a column informing if the element is missing (True)
            # or not (False):
            col_null = col.isnull()
            # Calculate number of missing values in this column:
            num_nulls = col_null.sum()
            
            # Return the index j of column col_name. 
            # Use the index method from lists, setting col_name as argument. It will return
            # the index of col_name from the list of columns
            # https://www.programiz.com/python-programming/methods/list/index#:~:text=The%20list%20index%20%28%29%20method%20can%20take%20a,-%20search%20the%20element%20up%20to%20this%20index?msclkid=a690b8dacfaa11ec8e84e10a50ae45ec
            j = df_cols_list.index(col_name)
            
            # Check if the column is a text or timestamp. In this case, the type
            # of column will be 'object'
            if ((col.dtype == 'O') | (col.dtype == 'object')):
                
                # Try converting it to a datetime64 object:
                
                try:
                    
                    col = (col).astype('datetime64[ns]')
                
                except:
                    
                    # It is not a timestamp, so conversion was not possible.
                    # Simply ignore it.
                    pass
                
            # Now, try to perform the scale adjustment:
            try:
                # Calculate column range
                col_range = (col.max() - col.min())

                # Scale the random values to scaling_factor times col_range
                # Calculate random values with the size of num_nulls.
                # The rand() function takes in as argument the size of the array to be generated
                # (i.e. the number num_nulls itself):
                
                try:
                    dummy_values = (rand(num_nulls) - 2) * (scaling_factor) * (col_range) + (col.min())
                
                except:
                    # It may be a timestamp, so we cannot multiply col_range and sum.
                    dummy_values = (rand(num_nulls) - 2) * (scaling_factor) + (col.min())
                
                # We can shift the dummy values from 0 and 1 to -2 and -1 by subtracting 2, as in:
                # (rand(num_nulls) - 2)
                # By doing this, we make sure that the dummy values are always below or lesser than 
                # the actual values, as can be observed from the graph.
                # So, by subtracting 2, we guarantee that the dummy values will be below the maximum 
                # possible.

                # Next, scale your dummy values by scaling_factor and multiply them by col_range:
                #  * (scaling_factor) * (col_range)
                # Finally add the bias: the minimum observed for that column col.min():
                # + (col.min())
                # When we shift the values to the minimum (col.min()), we make sure that the dummy 
                # values are just below the actual values.

                # Therefore, the procedure results in dummy values a distance apart from the 
                # actual values.

                # Loop through the array of dummy values generated:
                # Loop through each row of the dataframe:
                
                k = 0 # first element from the array of dummy values
                for i in range (0, len(df_dummy)):

                        # Check if the position is missing:
                        boolean_filter = col_null[i]
                        if (boolean_filter):

                            # Run if it is True.
                            # Fill the position in col_name with the dummy value
                            # at the position k from the array of dummy values.
                            # This array was created with a single element for each
                            # missing value:
                            df_dummy.iloc[i,j] = dummy_values[k]
                            # go to the next element
                            k = k + 1
                
            except:
                # It was not possible, because it is neither numeric nor timestamp.
                # Simply ignore it.
                pass
                
        return df_dummy
  
    # We fill the dummy values to 'df_dummy' with the function `fill_dummy_values`. 
    # The graph can be plotted with 'df_dummy.plot()' of 'x=column_to_analyze', 
    # 'y=column_to_compare_with', 'kind="scatter"' and 'alpha=0.5' for transparency. 
    
    # Call the subfunction for filling the dummy values:
    df_dummy = fill_dummy_values(df)
    
    # The object 'nullity' is the sum of the nullities of column_to_analyze and column_to_compare_with. 
    # It is a series of True and False values. 
    # True implies missing, while False implies not missing.
    
    # The nullity can be used to set the color of the data points with 'cmap="rainbow"'. 
    # Thus, we obtain the graph that we require.
    
    # Set the nullity of column_to_analyze and column_to_compare_with:
    nullity = ((df[column_to_analyze].isnull()) | (df[column_to_compare_with].isnull()))
    # For setting different colors to the missing and non-missing values, you can simply add 
    # the nullity, or the sum of null values of both respective columns that you are plotting, 
    # calculated using the .isnull() method. The nullity returns a Series of True or False 
    # (i.e., a boolean filter) where:
    # True - At least one of col1 or col2 is missing.
    # False - Neither of col1 and col2 values are missing.

    if (plot_title is None):
        plot_title = "missingness_of_" + "[" + column_to_analyze + "]" + "_vs_" + "[" + column_to_compare_with + "]"
    
    #Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
    fig = plt.figure(figsize = (12, 8))
    
    # Create a scatter plot of column_to_analyze and column_to_compare_with 
    df_dummy.plot(x = column_to_analyze, y = column_to_compare_with, 
                        kind = 'scatter', alpha = 0.5,
                        # Set color to nullity of column_to_analyze and column_to_compare_with
                        # alpha: transparency. alpha = 0.5 = 50% of transparency.
                        c = nullity,
                        # The c argument controls the color of the points in the plot.
                        cmap = 'rainbow',
                        grid = grid,
                        legend = True,
                        title = plot_title)
       
    if (export_png == True):
        # Image will be exported
        
        #check if the user defined a directory path. If not, set as the default root path:
        if (directory_to_save is None):
            #set as the default
            directory_to_save = ""
        
        #check if the user defined a file name. If not, set as the default name for this
        # function.
        if (file_name is None):
            #set as the default
            file_name = "comparison_of_missing_values"
        
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
    print("Plot Legend:") 
    print("1 = Missing value")
    print("0 = Non-missing value")
    
    if (show_interpreted_example):
        # Run if it is True. Requires TensorFlow to load. Load the extra library only
        # if necessary:
        from tensorflow.keras.preprocessing.image import img_to_array, load_img
        # img_to_array: convert the image into its numpy array representation
        
        # Download the images to the notebook's workspace:
        # Use the command !wget to download web content:
        example_na1 = !wget "https://github.com/marcosoares-92/img_examples_guides/raw/main/example_na1.PNG"
        example_na2 = !wget "https://github.com/marcosoares-92/img_examples_guides/raw/main/example_na2.PNG"
        example_na3 = !wget "https://github.com/marcosoares-92/img_examples_guides/raw/main/example_na3.PNG"
        example_na4 = !wget "https://github.com/marcosoares-92/img_examples_guides/raw/main/example_na4.PNG"
        # When saving the !wget calls as variables, we silent the verbosity of the Wget GNU.
        # Then, user do not see that a download has been made.
        # To check the help from !wget GNU, type and run a cell with: 
        # ! wget --help
        
        # Load the images and save them on variables:
        sample_image1 = load_img("example_na1.PNG")
        sample_image2 = load_img("example_na2.PNG")
        sample_image3 = load_img("example_na3.PNG")
        sample_image4 = load_img("example_na4.PNG")
        
        print("\n")
        print("Example of analysis:\n")
        
        print("Consider the following \'diabetes\' dataset, where scatterplot of \'Serum_Insulin\' and \'BMI\' illustrated below shows the non-missing values in purple and the missing values in red.\n")
        
        # Image example 1:
        # show image with plt.imshow function:
        plt.imshow(sample_image1)
        plt.show()
        print("\n")
        
        print("The red points along the y-axis are the missing values of \'Serum_Insulin\' plotted against their \'BMI\' values.\n")
        # Image example 2:
        # show image with plt.imshow function:
        plt.imshow(sample_image2)
        plt.show()
        print("\n")
        
        print("Likewise, the points along the x-axis are the missing values of \'BMI\' against their \'Serum_Insulin\' values.\n")
        # show image with plt.imshow function:
        plt.imshow(sample_image3)
        plt.show()
        print("\n")
        
        print("The bottom-left corner represents the missing values of both \'BMI\' and \'Serum_Insulin\'.\n")
        # Image example 4:
        # show image with plt.imshow function:
        plt.imshow(sample_image4)
        plt.show()
        print("\n")
        
        print("To interprete this graph, observe that the missing values of \'Serum_Insulin\' are spread throughout the \'BMI\' column.")
        print("Thus, we do not observe any specific correlation between the missingness of \'Serum_Insulin\' and \'BMI\'.\n")
        
        # Finally, before finishing the function, 
        # delete (remove) the files from the notebook's workspace.
        # The os.remove function deletes a file or directory specified.
        os.remove("example_na1.PNG")
        os.remove("example_na2.PNG")
        os.remove("example_na3.PNG")
        os.remove("example_na4.PNG")
        # Since we are not specifying a sub-directory (folder), files are being deleted from
        # the root, where the ! wget automatically saved them.


def handle_missing_values (df, subset_columns_list = None, drop_missing_val = True, fill_missing_val = False, eliminate_only_completely_empty_rows = False, min_number_of_non_missing_val_for_a_row_to_be_kept = None, value_to_fill = None, fill_method = "fill_with_zeros", interpolation_order = 'linear'):
    
    import numpy as np
    import pandas as pd
    from scipy import stats
    # numpy has no function mode, but scipy's stats module has.
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mode.html?msclkid=ccd9aaf2cb1b11ecb57c6f4b3e03a341
    # Pandas dropna method: remove rows containing missing values.
    # Pandas fillna method: fill missing values.
    # Pandas interpolate method: fill missing values with interpolation:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.dropna.html
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.fillna.html
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.interpolate.html#pandas.DataFrame.interpolate
    
    
    # subset_columns_list = list of columns to look for missing values. Only missing values
    # in these columns will be considered for deciding which columns to remove.
    # Declare it as a list of strings inside quotes containing the columns' names to look at,
    # even if this list contains a single element. e.g. subset_columns_list = ['column1']
    # will check only 'column1'; whereas subset_columns_list = ['col1', 'col2', 'col3'] will
    # chek the columns named as 'col1', 'col2', and 'col3'.
    # ATTENTION: Subsets are considered only for dropping missing values, not for filling.
    
    # drop_missing_val = True to eliminate the rows containing missing values.
    
    # fill_missing_val = False. Set this to True to activate the mode for filling the missing
    # values.
    
    # eliminate_only_completely_empty_rows = False - This parameter shows effect only when
    # drop_missing_val = True. If you set eliminate_only_completely_empty_rows = True, then
    # only the rows where all the columns are missing will be eliminated.
    # If you define a subset, then only the rows where all the subset columns are missing
    # will be eliminated.
    
    # min_number_of_non_missing_val_for_a_row_to_be_kept = None - 
    # This parameter shows effect only when drop_missing_val = True. 
    # If you set min_number_of_non_missing_val_for_a_row_to_be_kept equals to an integer value,
    # then only the rows where at least this integer number of non-missing values will be kept
    # after dropping the NAs.
    # e.g. if min_number_of_non_missing_val_for_a_row_to_be_kept = 2, only rows containing at
    # least two columns without missing values will be kept.
    # If you define a subset, then the criterium is applied only to the subset.
    
    # value_to_fill = None - This parameter shows effect only when
    # fill_missing_val = True. Set this parameter as a float value to fill all missing
    # values with this value. e.g. value_to_fill = 0 will fill all missing values with
    # the number 0. You can also pass a function call like 
    # value_to_fill = np.sum(dataset['col1']). In this case, the missing values will be
    # filled with the sum of the series dataset['col1']
    # Alternatively, you can also input a string to fill the missing values. e.g.
    # value_to_fill = 'text' will fill all the missing values with the string "text".
    
    # You can also input a dictionary containing the column(s) to be filled as key(s);
    # and the values to fill as the correspondent values. For instance:
    # value_to_fill = {'col1': 10} will fill only 'col1' with value 10.
    # value_to_fill = {'col1': 0, 'col2': 'text'} will fill 'col1' with zeros; and will
    # fill 'col2' with the value 'text'
    
    # fill_method = "fill_with_zeros". - This parameter shows effect only 
    # when fill_missing_val = True.
    # Alternatively: fill_method = "fill_with_zeros" - fill all the missing values with 0
    
    # fill_method = "fill_with_value_to_fill" - fill the missing values with the value
    # defined as the parameter value_to_fill
    
    # fill_method = "fill_with_avg_or_mode" - fill the missing values with the average value for 
    # each column, if the column is numeric; or fill with the mode, if the column is categorical.
    # The mode is the most commonly observed value.
    
    # fill_method = "ffill" - Forward (pad) fill: propagate last valid observation forward 
    # to next valid.
    # fill_method = 'bfill' - backfill: use next valid observation to fill gap.
    # fill_method = 'nearest' - 'ffill' or 'bfill', depending if the point is closest to the
    # next or to the previous non-missing value.
    
    # fill_method = "fill_by_interpolating" - fill by interpolating the previous and the 
    # following value. For categorical columns, it fills the
    # missing with the previous value, just as like fill_method = 'ffill'
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.interpolate.html#pandas.DataFrame.interpolate
    
    # interpolation_order: order of the polynomial used for interpolating if fill_method =
    # "fill_by_interpolating". If interpolation_order = None, interpolation_order = 'linear',
    # or interpolation_order = 1, a linear (1st-order polynomial) will be used.
    # If interpolation_order is an integer > 1, then it will represent the polynomial order.
    # e.g. interpolation_order = 2, for a 2nd-order polynomial; interpolation_order = 3 for a
    # 3rd-order, and so on.
    
    # WARNING: if the fillna method is selected (fill_missing_val == True), but no filling
    # methodology is selected, the missing values of the dataset will be filled with 0.
    # The same applies when a non-valid fill methodology is selected.
    # Pandas fillna method does not allow us to fill only a selected subset.
    
    # WARNING: if fill_method == "fill_with_value_to_fill" but value_to_fill is None, the 
    # missing values will be filled with the value 0.
    
    
    # Set a local copy of df to manipulate.
    # The methods used in this function can modify the original object itself. So,
    # here we apply the copy method setting deep = True
    cleaned_df = df.copy(deep = True)
   
    if (subset_columns_list is None):
        # all the columns are considered:
        total_columns = cleaned_df.shape[1]
    
    else:
        # Only the columns in the subset are considered.
        # Total columns is the length of the list of columns to subset:
        total_columns = len(subset_columns_list)
        
    # thresh argument of dropna method: int, optional - Require that many non-NA values.
    # This is the minimum of non-missing values that a row must have in order to be kept:
    THRESHOLD = min_number_of_non_missing_val_for_a_row_to_be_kept
    
    if ((drop_missing_val is None) & (fill_missing_val is None)):
        print("No valid input set for neither \'drop_missing_val\' nor \'fill_missing_val\'. Then, setting \'drop_missing_val\' = True and \'fill_missing_val\' = False.\n")
        drop_missing_val = True
        fill_missing_val = False
    
    elif (drop_missing_val is None):
        # The condition where both were missing was already tested. This one is tested only when the
        # the first if was not run.
        drop_missing_val = False
        fill_missing_val = True
    
    elif (fill_missing_val is None):
        drop_missing_val = True
        fill_missing_val = False
    
    elif ((drop_missing_val == True) & (fill_missing_val == True)):
        print("Both options \'drop_missing_val\' and \'fill_missing_val\' set as True. Then, selecting \'drop_missing_val\', which has preference.\n")
        fill_missing_val = False
    
    elif ((drop_missing_val == False) & (fill_missing_val == False)):
        print("Both options \'drop_missing_val\' and \'fill_missing_val\' set as False. Then, setting \'drop_missing_val\' = True.\n")
        drop_missing_val = True
    
    boolean_filter1 = (drop_missing_val == True)

    boolean_filter2 = (boolean_filter1) & (subset_columns_list is None)
    # These filters are True only if both conditions inside parentheses are True.
    # The operator & is equivalent to 'And' (intersection).
    # The operator | is equivalent to 'Or' (union).
    
    boolean_filter3 = (fill_missing_val == True) & (fill_method is None)
    # boolean_filter3 represents the situation where the fillna method was selected, but
    # no filling method was set.
    
    boolean_filter4 = (value_to_fill is None) & (fill_method == "fill_with_value_to_fill")
    # boolean_filter4 represents the situation where the fillna method will be used and the
    # user selected to fill the missing values with 'value_to_fill', but did not set a value
    # for 'value_to_fill'.
    
    if (boolean_filter1 == True):
        # drop missing values
        
        print("Dropping rows containing missing values, accordingly to the provided parameters.\n")
        
        if (boolean_filter2 == True):
            # no subset to filter
            
            if (eliminate_only_completely_empty_rows == True):
                #Eliminate only completely empty rows
                cleaned_df = cleaned_df.dropna(axis = 0, how = "all")
                # if axis = 1, dropna will eliminate each column containing missing values.
            
            elif (min_number_of_non_missing_val_for_a_row_to_be_kept is not None):
                # keep only rows containing at least the specified number of non-missing values:
                cleaned_df = cleaned_df.dropna(axis = 0, thresh = THRESHOLD)
            
            else:
                #Eliminate all rows containing missing values.
                #The only parameter is drop_missing_val
                cleaned_df = cleaned_df.dropna(axis = 0)
        
        else:
            #In this case, there is a subset for applying the Pandas dropna method.
            #Only the coluns in the subset 'subset_columns_list' will be analyzed.
                  
            if (eliminate_only_completely_empty_rows == True):
                #Eliminate only completely empty rows
                cleaned_df = cleaned_df.dropna(subset = subset_columns_list, how = "all")
            
            elif (min_number_of_non_missing_val_for_a_row_to_be_kept is not None):
                # keep only rows containing at least the specified number of non-missing values:
                cleaned_df = cleaned_df.dropna(subset = subset_columns_list, thresh = THRESHOLD)
            
            else:
                #Eliminate all rows containing missing values.
                #The only parameter is drop_missing_val
                cleaned_df = cleaned_df.dropna(subset = subset_columns_list)
        
        print("Finished dropping of missing values.\n")
    
    else:
        
        print("Filling missing values.\n")
        
        # In this case, the user set a value for the parameter fill_missing_val to fill 
        # the missing data.
        
        # Check if a filling dictionary was passed as value_to_fill:
        if (type(value_to_fill) == dict):
            
            print(f"Applying the filling dictionary. Filling columns {value_to_fill.keys()} with the values {value_to_fill.values()}, respectively.\n")
            cleaned_df = cleaned_df.fillna(value = value_to_fill)
        
        elif (boolean_filter3 == True):
            # If this condition was reached, no filling dictionary was input.
            # fillna method was selected, but no filling method was set.
            # Then, filling with zero.
            print("No filling method defined, so filling missing values with 0.\n")
            cleaned_df = cleaned_df.fillna(0)
        
        elif (boolean_filter4 == True):
            # fill_method == "fill_with_value_to_fill" but value_to_fill is None.
            # Then, filling with zero.
            print("No value input for filling, so filling missing values with 0.\n")
            cleaned_df = cleaned_df.fillna(0)
        
        else:
            # A filling methodology was selected.
            if (fill_method == "fill_with_zeros"):
                print("Filling missing values with 0.\n")
                cleaned_df = cleaned_df.fillna(0)
            
            elif (fill_method == "fill_with_value_to_fill"):
                print(f"Filling missing values with {value_to_fill}.\n")
                cleaned_df = cleaned_df.fillna(value_to_fill)
            
            elif ((fill_method == "fill_with_avg_or_mode") | (fill_method == "fill_by_interpolating")):
                
                # We must separate the dataset into numerical columns and categorical columns
                # 1. Get dataframe's columns list:
                df_cols = cleaned_df.columns
                
                # 2. start a list for the numeric and a list for the text (categorical) columns:
                numeric_cols = []
                text_cols = []
                
                # 3. Loop through each column on df_cols, to put it in the correspondent type of column:
                for column in df_cols:
                    # test each element in the list or array df_cols
                    column_data_type = cleaned_df[column].dtype
                    
                    if ((column_data_type == 'O') | (column_data_type == 'object')):
                        
                        # The Pandas series was defined as an object, meaning it is categorical
                        # (string, date, etc).
                        # Append it to the list text_cols:
                        text_cols.append(column)
                    
                    else:
                        # The Pandas series is a numeric column: int64, float64,...
                        # Append it to the numeric_cols list:
                        numeric_cols.append(column)
                
                # Now, we have two subsets (lists) of columns, one for the categoricals, other
                # for the numeric. It will avoid trying to fill categorical columns with the
                # mean values.
                
                if (fill_method == "fill_with_avg_or_mode"):
                
                    print("Filling missing values with the average values (numeric variables); or with the modes (categorical variables). The mode is the most commonly observed value of the categorical variable.\n")
                
                    # 3. Start an empty list to store all of the average values,
                    # and a list to store the modes:
                    avg_list = []
                    mode_list = []

                    # 3. Loop through each column of numeric_cols.
                    # Calculate the average value for the series df[column].
                    # Append this value to avg_list.
                    for column in numeric_cols:
                        #check all elements of numeric_cols, named 'column'
                        # Calculate the average of the series df[column]
                        # and append it to the avg_list
                        avg_list.append(cleaned_df[column].mean())    
                        # Alternatively, one could append np.average(cleaned_df[column])

                    # Now, we have a list containing the average value correspondent
                    # to each column of the dataframe, named avg_list.
                    # 4. Create a dictionary informing the columns and the values
                    # to be input in each column. Each key of the dictionary must be a column.
                    # The value for that key will be used to fill the correspondent column.

                    # Start the dictionary:
                    fill_dict = {}

                    for i in range (0, len(numeric_cols)):
                        # i = 0 to i = len(numeric_cols) - 1, index of the last value of the list.
                        # Apply the update method to include numeric_cols[i] as key and
                        # avg_list[i] as the value:
                        fill_dict.update({numeric_cols[i]: avg_list[i]})

                    # 5. Loop through each column of text_cols.
                    # Calculate the mode for the series df[column].
                    # Append this value to mode_list.
                    for column in text_cols:
                        #check all elements of numeric_cols, named 'column'
                        # Calculate the average of the series df[column]
                        # and append it to the mode_list

                        mode_array = stats.mode(cleaned_df[column])
                        # Here, if we use cleaned_df[column].agg(stats.mode), the function will
                        # firstly group each element of the series and then calculate the mode,
                        # resulting in a series of modes. Since each row has only one value,
                        # This value will be repeated. If we call stats.mode (series), instead,
                        # we aggregate the whole series in a single mode array.

                        # The function stats.mode(X) returns an array as: 
                        # ModeResult(mode=array(['a'], dtype='<U1'), count=array([2]))
                        # If we select the first element from this array, stats.mode(X)[0], 
                        # the function will return an array as array(['a'], dtype='<U1'). 
                        # We want the first element from this array stats.mode(X)[0][0], 
                        # which will return a string like 'a':
                        try:
                            mode_list.append(mode_array[0][0])

                        except IndexError:
                            # This error is generated when trying to access an array storing no values.
                            # (i.e., with missing values). Since there is no dimension, it is not possible
                            # to access the [0][0] position. In this case, simply append the np.nan 
                            # the (missing value):
                            mode_list.append(np.nan)

                    # Update the dictionary to include the text columns and the correspondent modes,
                    # keeping the same format. For that, loop through each element of the lists
                    # text_cols and mode_list:
                    for i in range (0, len(text_cols)):
                        # i = 0 to i = len(text_cols) - 1, index of the last value of the list.
                        # Apply the update method to include text_cols[i] as key and
                        # mode_list[i] as the value:
                        fill_dict.update({text_cols[i]: mode_list[i]})

                    # Now, fill_dict is in the correct format for the fillna method:
                    # 'column' as key; value to fill that column as value.
                    # In fillna documentation, we see that the argument 'value' must have a dictionary
                    # with this particular format as input:
                    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.fillna.html#pandas.DataFrame.fillna

                    # This dictionary correlates each column to its average value.

                    #6. Finally, use this dictionary to fill the missing values of each column
                    # with the average value of that column
                    cleaned_df = cleaned_df.fillna(value = fill_dict)
                    # The method will search the column name in fill_dict (key of the dictionary),
                    # and will use the correspondent value (average) to fill the missing values.

                elif (fill_method == "fill_by_interpolating"):
                    # Pandas interpolate method
                    
                    # Separate the dataframes into a dataframe for filling with interpolation (numeric
                    # variables); and a dataframe for forward filling (categorical variables).
                    
                    # Before subsetting, check if the list is not empty.
                    
                    if (len(numeric_cols) > 0):
                        # There are numeric columns to subset.
                        # Define the subset of numeric varibles.
                        numeric_subset = cleaned_df.copy(deep = True)
                        # Select only the numeric variables for this copy:
                        numeric_subset = numeric_subset[numeric_cols]
                        # Create a key series from index, which will be used as key for merging the 
                        # subsets (the correspondent rows necessarily have same index):
                        numeric_subset['interpolate_key'] = numeric_subset.index
                    
                        if (type(interpolation_order) == int):
                            # an integer number was input

                            if (interpolation_order > 1):

                                print(f"Performing interpolation of numeric variables with {interpolation_order}-degree polynomial to fill missing values.\n")
                                numeric_subset = numeric_subset.interpolate(method = 'polynomial', order = interpolation_order)

                            else:
                                # 1st order or invalid order (0 or negative) was used
                                print("Performing linear interpolation of numeric variables to fill missing values.\n")
                                numeric_subset = numeric_subset.interpolate(method = 'linear')

                        else:
                            # 'linear', None or invalid text was input:
                            print("Performing linear interpolation of numeric variables to fill missing values.\n")
                            numeric_subset = numeric_subset.interpolate(method = 'linear')
                    
                    # Now, we finished the interpolation of the numeric variables. Let's check if
                    # there are categorical variables to forward fill.
                    if (len(text_cols) > 0):
                        # There are text columns to subset.
                        # Define the subset of text varibles.
                        text_subset = cleaned_df.copy(deep = True)
                        # Select only the categorical variables:
                        text_subset = text_subset[text_cols]
                        # Create a key series from index, which will be used as key for merging the 
                        # subsets (the correspondent rows necessarily have same index):
                        text_subset['interpolate_key'] = text_subset.index
                        
                        # Now, fill missing values by forward filling:
                        print("Using forward filling to fill missing values of the categorical variables.\n")
                        text_subset = text_subset.fillna(method = "ffill")
                    
                    # Now, let's check if there are both a numeric_subset and a text_subset to merge
                    if ((len(numeric_cols) > 0) & (len(text_cols) > 0)):
                        # Two subsets were created. Merge them on column key, using 'inner' join
                        # (perfect correspondence of the indices). Save it on cleaned_df.
                        # Use the merge method: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.merge.html
                        cleaned_df = numeric_subset.merge(text_subset, on = 'interpolate_key', how = "inner")
                        
                        # Drop the column 'interpolate_key', created only for merging.
                        # Use the drop method:
                        cleaned_df = cleaned_df.drop(columns = 'interpolate_key')
                    
                    elif (len(numeric_cols) > 0):
                        # since it did not pass the test for checking if both were present, there
                        # are only numeric columns. So, make the cleaned_df the numeric_subset itself
                        # and drop the key column:
                        cleaned_df = numeric_subset
                        cleaned_df = cleaned_df.drop(columns = 'interpolate_key')
                    
                    elif (len(text_cols) > 0):
                        # since it did not pass the test for checking if both were present, there
                        # are only text columns. So, make the cleaned_df the text_subset itself
                        # and drop the key column:
                        cleaned_df = text_subset
                        cleaned_df = cleaned_df.drop(columns = 'interpolate_key')
                        
            
            elif ((fill_method == "ffill") | (fill_method == "bfill")):
                # use forward or backfill
                cleaned_df = cleaned_df.fillna(method = fill_method)
            
            elif (fill_method == "nearest"):
                # nearest: applies the 'bfill' or 'ffill', depending if the point
                # is closes to the previous or to the next non-missing value.
                # It is a Pandas dataframe interpolation method, not a fillna one.
                cleaned_df = cleaned_df.interpolate(method = 'nearest')
            
            else:
                print("No valid filling methodology was selected. Then, filling missing values with 0.")
                cleaned_df = cleaned_df.fillna(0)
        
        
    #Reset index before returning the cleaned dataframe:
    cleaned_df = cleaned_df.reset_index(drop = True)
    
    
    print(f"Number of rows of the dataframe before cleaning = {df.shape[0]} rows.")
    print(f"Number of rows of the dataframe after cleaning = {cleaned_df.shape[0]} rows.")
    print(f"Percentual variation of the number of rows = {(df.shape[0] - cleaned_df.shape[0])/(df.shape[0]) * 100} %\n")
    print("Check the 10 first rows of the cleaned dataframe:\n")
    print(cleaned_df.head(10))
    
    return cleaned_df


def adv_imputation_missing_values (df, column_to_fill, timestamp_tag_column = None, test_value_to_fill = None, show_imputation_comparison_plots = True):
    
    # Check DataCamp course Dealing with Missing Data in Python
    # https://app.datacamp.com/learn/courses/dealing-with-missing-data-in-python
    
    # This function handles only one column by call, whereas handle_missing_values can process the whole
    # dataframe at once.
    # The strategies used for handling missing values is different here. You can use the function to
    # process data that does not come from time series, but only plot the graphs for time series data.
    
    # This function is more indicated for dealing with missing values on time series data than handle_missing_values.
    # This function will search for the best imputer for a given column.
    # It can process both numerical and categorical columns.
    
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy.stats import linregress
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import OrdinalEncoder
    from fancyimpute import KNN, IterativeImputer
    
    # column_to_fill: string (in quotes) indicating the column with missing values to fill.
    # e.g. if column_to_fill = 'col1', imputations will be performed on column 'col1'.
    
    # timestamp_tag_column = None. string containing the name of the column with the timestamp. 
    # If timestamp_tag_column is None, the index will be used for testing different imputations.
    # be the time series reference. declare as a string under quotes. This is the column from 
    # which we will extract the timestamps or values with temporal information. e.g.
    # timestamp_tag_column = 'timestamp' will consider the column 'timestamp' a time column.
    
    # test_value_to_fill: the function will test the imputation of a constant. Specify this constant here
    # or the tested constant will be zero. e.g. test_value_to_fill = None will test the imputation of 0.
    # test_value_to_fill = 10 will test the imputation of value zero.
    
    # show_imputation_comparison_plots = True. Keep it True to plot the scatter plot comparison
    # between imputed and original values, as well as the Kernel density estimate (KDE) plot.
    # Alternatively, set show_imputation_comparison_plots = False to omit the plots.
    
    # The following imputation techniques will be tested, and the best one will be automatically
    # selected: mean_imputer, median_imputer, mode_imputer, constant_imputer, linear_interpolation,
    # quadratic_interpolation, cubic_interpolation, nearest_interpolation, bfill_imputation,
    # ffill_imputation, knn_imputer, mice_imputer (MICE = Multiple Imputations by Chained Equations).
    
    # MICE: Performs multiple regressions over random samples of the data; 
    # Takes the average of multiple regression values; and imputes the missing feature value for the 
    # data point.
    # KNN (K-Nearest Neighbor): Selects K nearest or similar data points using all the 
    # non-missing features. It takes the average of the selected data points to fill in the missing 
    # feature.
    # These are Machine Learning techniques to impute missing values.
    # KNN finds most similar points for imputing.
    # MICE performs multiple regression for imputing. MICE is a very robust model for imputation.
    
    
    # Set a local copy of df to manipulate.
    # The methods used in this function can modify the original object itself. So,
    # here we apply the copy method setting deep = True
    cleaned_df = df.copy(deep = True)
    
    subset_columns_list = [column_to_fill] # only the column indicated.
    total_columns = 1 # keep the homogeneity with the previous function
    
    # Get the list of columns of the dataframe:
    df_cols = list(cleaned_df.columns)
    # Get the index j of the column_to_fill:
    j = df_cols.index(column_to_fill)
    print(f"Filling missing values on column {column_to_fill}. This is the column with index {j} in the original dataframe.\n")

    # Firstly, let's process the timestamp column and save it as x. 
    # That is because datetime objects cannot be directly applied to linear regressions and
    # numeric procedure. We must firstly convert it to an integer scale capable of preserving
    # the distance relationships.
   
    # Check if there is a timestamp_tag_column. If not, make the index the timestamp:
    if (timestamp_tag_column is None):
        
        timestamp_tag_column = column_to_fill + "_index"
        
        # Create the x array
        x = np.array(cleaned_df.index)
        
    else:
        # Run only if there was a timestamp column originally.
        # sort this dataframe by timestamp_tag_column and column_to_fill:
        cleaned_df = cleaned_df.sort_values(by = [timestamp_tag_column, column_to_fill], ascending = [True, True])
        # restart index:
        cleaned_df = cleaned_df.reset_index(drop = True)
        
        # If timestamp_tag_column is an object, the user may be trying to pass a date as x. 
        # So, let's try to convert it to datetime:
        if ((cleaned_df[timestamp_tag_column].dtype == 'O') | (cleaned_df[timestamp_tag_column].dtype == 'object')):

            try:
                cleaned_df[timestamp_tag_column] = (cleaned_df[timestamp_tag_column]).astype('datetime64[ns]')
                        
            except:
                # Simply ignore it
                pass
        
        ts_array = np.array(cleaned_df[timestamp_tag_column])
        
        # Check if the elements from array x are np.datetime64 objects. Pick the first
        # element to check:
        if (type(ts_array[0]) == np.datetime64):
            # In this case, performing the linear regression directly in X will
            # return an error. We must associate a sequential number to each time.
            # to keep the distance between these integers the same as in the original sequence
            # let's define a difference of 1 ns as 1. The 1st timestamp will be zero, and the
            # addition of 1 ns will be an addition of 1 unit. So a timestamp recorded 10 ns
            # after the time zero will have value 10. At the end, we divide every element by
            # 10**9, to obtain the correspondent distance in seconds.
                
            # start a list for the associated integer timescale. Put the number zero,
            # associated to the first timestamp:
            int_timescale = [0]
                
            # loop through each element of the array x, starting from index 1:
            for i in range(1, len(ts_array)):
                    
                # calculate the timedelta between x[i] and x[i-1]:
                # The delta method from the Timedelta class converts the timedelta to
                # nanoseconds, guaranteeing the internal compatibility:
                timedelta = pd.Timedelta(ts_array[i] - ts_array[(i-1)]).delta
                    
                # Sum this timedelta (integer number of nanoseconds) to the
                # previous element from int_timescale, and append the result to the list:
                int_timescale.append((timedelta + int_timescale[(i-1)]))
                
            # Now convert the new scale (that preserves the distance between timestamps)
            # to NumPy array:
            int_timescale = np.array(int_timescale)
            
            # Divide by 10**9 to obtain the distances in seconds, reducing the order of
            # magnitude of the integer numbers (the division is allowed for arrays).
            # make it the timestamp array ts_array itself:
            ts_array = int_timescale / (10**9)
            # Now, reduce again the order of magnitude through division by (60*60)
            # It will obtain the ts_array in hour:
            ts_array = int_timescale / (60*60)
            
        # make x the ts_array itself:
        x = ts_array
    
    column_data_type = cleaned_df[column_to_fill].dtype
    
    # Pre-process the column if it is categorical
    if ((column_data_type == 'O') | (column_data_type == 'object')):
        
        # Ordinal encoding: let's associate integer sequential numbers to the categorical column
        # to apply the advanced encoding techniques. Even though the one-hot encoding could perform
        # the same task and would, in fact, better, since there may be no ordering relation, the
        # ordinal encoding is simpler and more suitable for this particular task:
        
        # Create Ordinal encoder
        ord_enc = OrdinalEncoder()
        
        # Select non-null values of the column in the dataframe:
        series_on_df = cleaned_df[column_to_fill]
        
        # Reshape series_on_df to shape (-1, 1)
        reshaped_vals = series_on_df.values.reshape(-1, 1)
        
        # Fit the ordinal encoder to the reshaped column_to_fill values:
        encoded_vals = ord_enc.fit_transform(reshaped_vals)
        
        # Finally, store the values to non-null values of the column in dataframe
        cleaned_df.iloc[:,j] = encoded_vals

        # Max and minimum of the encoded range
        max_encoded = max(encoded_vals)
        min_encoded = min(encoded_vals)


    # Start a list of imputations:
    list_of_imputations = []
    
    subset_from_cleaned_df = cleaned_df.copy(deep = True)
    subset_from_cleaned_df = subset_from_cleaned_df[subset_columns_list]

    mean_imputer = SimpleImputer(strategy = 'mean')
    list_of_imputations.append('mean_imputer')
    
    # Now, apply the fit_transform method from the imputer to fit it to the indicated column:
    mean_imputer.fit(subset_from_cleaned_df)
    # If you wanted to obtain constants for all columns, you should not specify a subset:
    # imputer.fit_transform(cleaned_df)
        
    # create a column on the dataframe as 'mean_imputer':
    cleaned_df['mean_imputer'] = mean_imputer.transform(subset_from_cleaned_df)
        
    # Create the median imputer:
    median_imputer = SimpleImputer(strategy = 'median')
    list_of_imputations.append('median_imputer')
    median_imputer.fit(subset_from_cleaned_df)
    cleaned_df['median_imputer'] = median_imputer.transform(subset_from_cleaned_df)
    
    # Create the mode imputer:
    mode_imputer = SimpleImputer(strategy = 'most_frequent')
    list_of_imputations.append('mode_imputer')
    mode_imputer.fit(subset_from_cleaned_df)
    cleaned_df['mode_imputer'] = mode_imputer.transform(subset_from_cleaned_df)
    
    # Create the constant value imputer:
    if (test_value_to_fill is None):
        test_value_to_fill = 0
    
    constant_imputer = SimpleImputer(strategy = 'constant', fill_value = test_value_to_fill)
    list_of_imputations.append('constant_imputer')
    constant_imputer.fit(subset_from_cleaned_df)
    cleaned_df['constant_imputer'] = constant_imputer.transform(subset_from_cleaned_df)
    
    # Make the linear interpolation imputation:
    linear_interpolation_df = cleaned_df[subset_columns_list].copy(deep = True)
    linear_interpolation_df = linear_interpolation_df.interpolate(method = 'linear')
    cleaned_df['linear_interpolation'] = linear_interpolation_df[column_to_fill]
    list_of_imputations.append('linear_interpolation')
        
    # Interpolate 2-nd degree polynomial:
    quadratic_interpolation_df = cleaned_df[subset_columns_list].copy(deep = True)
    quadratic_interpolation_df = quadratic_interpolation_df.interpolate(method = 'polynomial', order = 2)
    cleaned_df['quadratic_interpolation'] = quadratic_interpolation_df[column_to_fill]
    list_of_imputations.append('quadratic_interpolation')
        
    # Interpolate 3-rd degree polynomial:
    cubic_interpolation_df = cleaned_df[subset_columns_list].copy(deep = True)
    cubic_interpolation_df = cubic_interpolation_df.interpolate(method = 'polynomial', order = 3)
    cleaned_df['cubic_interpolation'] = cubic_interpolation_df[column_to_fill]
    list_of_imputations.append('cubic_interpolation')
    
    # Nearest interpolation
    # Similar to bfill and ffill, but uses the nearest
    nearest_interpolation_df = cleaned_df[subset_columns_list].copy(deep = True)
    nearest_interpolation_df = nearest_interpolation_df.interpolate(method = 'nearest')
    cleaned_df['nearest_interpolation'] = nearest_interpolation_df[column_to_fill]
    list_of_imputations.append('nearest_interpolation')
    
    # bfill and ffill:
    bfill_df = cleaned_df[subset_columns_list].copy(deep = True)
    ffill_df = cleaned_df[subset_columns_list].copy(deep = True)
    
    bfill_df = bfill_df.fillna(method = 'bfill')
    cleaned_df['bfill_imputation'] = bfill_df[column_to_fill]
    list_of_imputations.append('bfill_imputation')
    
    ffill_df = ffill_df.fillna(method = 'ffill')
    cleaned_df['ffill_imputation'] = ffill_df[column_to_fill]
    list_of_imputations.append('ffill_imputation')
    
    
    # Now, we can go to the advanced machine learning techniques:
    
    # KNN Imputer:
    # Initialize KNN
    knn_imputer = KNN()
    list_of_imputations.append('knn_imputer')
    cleaned_df['knn_imputer'] = knn_imputer.fit_transform(subset_from_cleaned_df)
    
    # Initialize IterativeImputer
    mice_imputer = IterativeImputer()
    list_of_imputations.append('mice_imputer')
    cleaned_df['mice_imputer'] = mice_imputer.fit_transform(subset_from_cleaned_df)
    
    # Now, let's create linear regressions for compare the performance of different
    # imputation strategies.
    # Firstly, start a dictionary to store
    
    imputation_performance_dict = {}

    # Now, loop through each imputation and calculate the adjusted R²:
    for imputation in list_of_imputations:
        
        y = cleaned_df[imputation]
        
        # fit the linear regression
        slope, intercept, r, p, se = linregress(x, y)
        
        # Get the adjusted R² and add it as the key imputation of the dictionary:
        imputation_performance_dict[imputation] = r**2
    
    # Select best R-squared
    best_imputation = max(imputation_performance_dict, key = imputation_performance_dict.get)
    print(f"The best imputation strategy for the column {column_to_fill} is {best_imputation}.\n")
    
    
    if (show_imputation_comparison_plots & ((column_data_type != 'O') & (column_data_type != 'object'))):
        
        # Firstly, converts the values obtained to closest integer (since we
        # encoded the categorical values as integers, we cannot reconvert
        # decimals):)): # run if it is True
    
        print("Check the Kernel density estimate (KDE) plot for the different imputations.\n")
        labels_list = ['baseline\ncomplete_case']
        y = cleaned_df[column_to_fill]
        X = cleaned_df[timestamp_tag_column] # not the converted scale

        fig = plt.figure(figsize = (12, 8))
        ax = fig.add_subplot()
        
        # Plot graphs of imputed DataFrames and the complete case
        y.plot(kind = 'kde', c = 'red', linewidth = 3)

        for imputation in list_of_imputations:
            
            labels_list.append(imputation)
            y = cleaned_df[imputation]
            y.plot(kind = 'kde')
        
        #ROTATE X AXIS IN XX DEGREES
        plt.xticks(rotation = 0)
        # XX = 0 DEGREES x_axis (Default)
        #ROTATE Y AXIS IN XX DEGREES:
        plt.yticks(rotation = 0)
        # XX = 0 DEGREES y_axis (Default)

        ax.set_title("Kernel_density_estimate_plot_for_each_imputation")
        ax.set_xlabel(column_to_fill)
        ax.set_ylabel("density")

        ax.grid(True) # show grid or not
        ax.legend(loc = 'upper left')
        # position options: 'upper right'; 'upper left'; 'lower left'; 'lower right';
        # 'right', 'center left'; 'center right'; 'lower center'; 'upper center', 'center'
        # https://www.statology.org/matplotlib-legend-position/
        plt.show()
        
        print("\n")
        print(f"Now, check the original time series compared with the values obtained through {best_imputation}:\n")
        
        fig = plt.figure(figsize = (12, 8))
        ax = fig.add_subplot()
        
        # Plot the imputed DataFrame in red dotted style
        selected_imputation = cleaned_df[best_imputation]
        ax.plot(X, selected_imputation, color = 'red', marker = 'o', linestyle = 'dotted', label = best_imputation)
        
        # Plot the original DataFrame with title
        # Put a degree of transparency (35%) to highlight the imputation.
        ax.plot(X, y, color = 'darkblue', alpha = 0.65, linestyle = '-', marker = '', label = (column_to_fill + "_original"))
        
        plt.xticks(rotation = 70)
        plt.yticks(rotation = 0)
        ax.set_title(column_to_fill + "_original_vs_imputations")
        ax.set_xlabel(timestamp_tag_column)
        ax.set_ylabel(column_to_fill)

        ax.grid(True) # show grid or not
        ax.legend(loc = 'upper left')
        # position options: 'upper right'; 'upper left'; 'lower left'; 'lower right';
        # 'right', 'center left'; 'center right'; 'lower center'; 'upper center', 'center'
        # https://www.statology.org/matplotlib-legend-position/
        plt.show()
        print("\n")
    
                
    print(f"Returning a dataframe where {best_imputation} strategy was used for filling missing values in {column_to_fill} column.\n")
     
    if (best_imputation == 'mice_imputer'):
        print("MICE = Multiple Imputations by Chained Equations")
        print("MICE: Performs multiple regressions over random samples of the data.")
        print("It takes the average of multiple regression values and imputes the missing feature value for the data point.")
        print("It is a Machine Learning technique to impute missing values.")
        print("MICE performs multiple regression for imputing and is a very robust model for imputation.\n")
    
    elif (best_imputation == 'knn_imputer'):
        print("KNN = K-Nearest Neighbor")
        print("KNN selects K nearest or similar data points using all the non-missing features.")
        print("It takes the average of the selected data points to fill in the missing feature.")
        print("It is a Machine Learning technique to impute missing values.")
        print("KNN finds most similar points for imputing.\n")
    
    # Make all rows from the column j equals to the selected imputer:
    cleaned_df.iloc[:, j] = cleaned_df[best_imputation]
    # If you wanted to make all rows from all columns equal to the imputer, you should declare:
    # cleaned_df.iloc[:, :] = imputer
    
    # Drop all the columns created for storing different imputers:
    # These columns were saved in the list list_of_imputations.
    # Notice that the selected imputations were saved in the original column.
    cleaned_df = cleaned_df.drop(columns = list_of_imputations)
    
    # Finally, let's reverse the ordinal encoding used in the beginning of the code to process object
    # columns:
    
    if ((column_data_type == 'O') | (column_data_type == 'object')):
        
        # Firstly, converts the values obtained to closest integer (since we
        # encoded the categorical values as integers, we cannot reconvert
        # decimals):
        
        cleaned_df[column_to_fill] = (np.rint(cleaned_df[column_to_fill]))
        
        # If a value is above the max_encoded, make it equals to the maximum.
        # If it is below the minimum, make it equals to the minimum:
        for k in range(0, len(cleaned_df)):

          if (cleaned_df.iloc[k,j] > max_encoded):
            cleaned_df.iloc[k,j] = max_encoded
          
          elif (cleaned_df.iloc[k,j] < min_encoded):
            cleaned_df.iloc[k,j] = min_encoded

        new_series = cleaned_df[column_to_fill]
        # We must use the int function to guarantee that the column_to_fill will store an
        # integer number (we cannot have a fraction of an encoding).
        # The int function guarantees that the variable will be stored as an integer.
        # The numpy.rint(a) function rounds elements of the array to the nearest integer.
        # https://numpy.org/doc/stable/reference/generated/numpy.rint.html
        # For values exactly halfway between rounded decimal values, 
        # NumPy rounds to the nearest even value. 
        # Thus 1.5 and 2.5 round to 2.0; -0.5 and 0.5 round to 0.0; etc.
        
        # Reshape series_not_null to shape (-1, 1)
        reshaped_vals = new_series.values.reshape(-1, 1)
        
        # Perform inverse transform of the ordinally encoded columns
        cleaned_df[column_to_fill] = ord_enc.inverse_transform(reshaped_vals)


    print("Check the 10 first rows from the original dataframe:\n")
    print(cleaned_df.head(10))
    
    return cleaned_df


def correlation_plot (df, show_masked_plot = True, responses_to_return_corr = None, set_returned_limit = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    #show_masked_plot = True - keep as True if you want to see a cleaned version of the plot
    # where a mask is applied.
    
    #responses_to_return_corr - keep as None to return the full correlation tensor.
    # If you want to display the correlations for a particular group of features, input them
    # as a list, even if this list contains a single element. Examples:
    # responses_to_return_corr = ['response1'] for a single response
    # responses_to_return_corr = ['response1', 'response2', 'response3'] for multiple
    # responses. Notice that 'response1',... should be substituted by the name ('string')
    # of a column of the dataset that represents a response variable.
    # WARNING: The returned coefficients will be ordered according to the order of the list
    # of responses. i.e., they will be firstly ordered based on 'response1'
    
    # set_returned_limit = None - This variable will only present effects in case you have
    # provided a response feature to be returned. In this case, keep set_returned_limit = None
    # to return all of the correlation coefficients; or, alternatively, 
    # provide an integer number to limit the total of coefficients returned. 
    # e.g. if set_returned_limit = 10, only the ten highest coefficients will be returned. 
    
    # set a local copy of the dataset to perform the calculations:
    DATASET = df.copy(deep = True)
    
    correlation_matrix = DATASET.corr(method = 'pearson')
    
    if (show_masked_plot == False):
        #Show standard plot
        
        plt.figure(figsize = (12, 8))
        sns.heatmap((correlation_matrix)**2, annot = True, fmt = ".2f")
        
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
                file_name = "correlation_plot"

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

        plt.show()

    #Oncee the pandas method .corr() calculates R, we raised it to the second power 
    # to obtain R². R² goes from zero to 1, where 1 represents the perfect correlation.
    
    else:
        
        # Show masked (cleaner) plot instead of the standard one
        # Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
        plt.figure(figsize = (12, 8))
        # Mask for the upper triangle
        mask = np.zeros_like((correlation_matrix)**2)

        mask[np.triu_indices_from(mask)] = True

        # Generate a custom diverging colormap
        cmap = sns.diverging_palette(220, 10, as_cmap = True)

        # Heatmap with mask and correct aspect ratio
        sns.heatmap(((correlation_matrix)**2), mask = mask, cmap = cmap, center = 0,
                    linewidths = .5)
        
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
                file_name = "correlation_plot"

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

        plt.show()

        #Again, the method dataset.corr() calculates R within the variables of dataset.
        #To calculate R², we simply raise it to the second power: (dataset.corr()**2)
    
    #Sort the values of correlation_matrix in Descending order:
    
    if (responses_to_return_corr is not None):
        
        #Select only the desired responses, by passing the list responses_to_return_corr
        # as parameter for column filtering:
        correlation_matrix = correlation_matrix[responses_to_return_corr]
        
        #Now sort the values according to the responses, by passing the list
        # responses_to_return_corr as the parameter
        correlation_matrix = correlation_matrix.sort_values(by = responses_to_return_corr, ascending = False)
        
        # If a limit of coefficients was determined, apply it:
        if (set_returned_limit is not None):
                
                correlation_matrix = correlation_matrix.head(set_returned_limit)
                #Pandas .head(X) method returns the first X rows of the dataframe.
                # Here, it returns the defined limit of coefficients, set_returned_limit.
                # The default .head() is X = 5.
        
        print(correlation_matrix)
    
    print("ATTENTION: The correlation plots show the linear correlations R², which go from 0 (none correlation) to 1 (perfect correlation). Obviously, the main diagonal always shows R² = 1, since the data is perfectly correlated to itself.\n")
    print("The returned correlation matrix, on the other hand, presents the linear coefficients of correlation R, not R². R values go from -1 (perfect negative correlation) to 1 (perfect positive correlation).\n")
    print("None of these coefficients take non-linear relations and the presence of a multiple linear correlation in account. For these cases, it is necessary to calculate R² adjusted, which takes in account the presence of multiple preditors and non-linearities.\n")
    
    print("Correlation matrix - numeric results:\n")
    print(correlation_matrix)
    
    return correlation_matrix


def bar_chart (df, categorical_var_name, response_var_name, aggregate_function = 'sum', add_suffix_to_aggregated_col = True, suffix = None, calculate_and_plot_cumulative_percent = True, orientation = 'vertical', limit_of_plotted_categories = None, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy import stats
    
    # df: dataframe being analyzed
    
    # categorical_var_name: string (inside quotes) containing the name 
    # of the column to be analyzed. e.g. 
    # categorical_var_name = "column1"
    
    # response_var_name: string (inside quotes) containing the name 
    # of the column that stores the response correspondent to the
    # categories. e.g. response_var_name = "response_feature" 
    
    # aggregate_function = 'sum': String defining the aggregation 
    # method that will be applied. Possible values:
    # 'median', 'mean', 'mode', 'sum', 'min', 'max', 'variance', 'count',
    # 'standard_deviation', '10_percent_quantile', '20_percent_quantile',
    # '25_percent_quantile', '30_percent_quantile', '40_percent_quantile',
    # '50_percent_quantile', '60_percent_quantile', '70_percent_quantile',
    # '75_percent_quantile', '80_percent_quantile', '90_percent_quantile',
    # '95_percent_quantile', 'kurtosis', 'skew', 'interquartile_range',
    # 'mean_standard_error', 'entropy'
    # To use another aggregate function, you can use the .agg method, passing 
    # the aggregate as argument, such as in:
    # .agg(scipy.stats.mode), 
    # where the argument is a Scipy aggregate function.
    # If None or an invalid function is input, 'sum' will be used.
    
    # add_suffix_to_aggregated_col = True will add a suffix to the
    # aggregated column. e.g. 'responseVar_mean'. If add_suffix_to_aggregated_col 
    # = False, the aggregated column will have the original column name.
    
    # suffix = None. Keep it None if no suffix should be added, or if
    # the name of the aggregate function should be used as suffix, after
    # "_". Alternatively, set it as a string. As recommendation, put the
    # "_" sign in the beginning of this string to separate the suffix from
    # the original column name. e.g. if the response variable is 'Y' and
    # suffix = '_agg', the new aggregated column will be named as 'Y_agg'
    
    # calculate_and_plot_cumulative_percent = True to calculate and plot
    # the line of cumulative percent, or 
    # calculate_and_plot_cumulative_percent = False to omit it.
    # This feature is only shown when aggregate_function = 'sum', 'median',
    # 'mean', or 'mode'. So, it will be automatically set as False if 
    # another aggregate is selected.
    
    # orientation = 'vertical' is the standard, and plots vertical bars
    # (perpendicular to the X axis). In this case, the categories are shown
    # in the X axis, and the correspondent responses are in Y axis.
    # Alternatively, orientation = 'horizontal' results in horizontal bars.
    # In this case, categories are in Y axis, and responses in X axis.
    # If None or invalid values are provided, orientation is set as 'vertical'.
    
    # Note: to obtain a Pareto chart, keep aggregate_function = 'sum',
    # plot_cumulative_percent = True, and orientation = 'vertical'.
    
    # limit_of_plotted_categories: integer value that represents
    # the maximum of categories that will be plot. Keep it None to plot
    # all categories. Alternatively, set an integer value. e.g.: if
    # limit_of_plotted_categories = 4, but there are more categories,
    # the dataset will be sorted in descending order and: 1) The remaining
    # categories will be sum in a new category named 'others' if the
    # aggregate function is 'sum'; 2) Or the other categories will be simply
    # omitted from the plot, for other aggregate functions. Notice that
    # it limits only the variables in the plot: all of them will be
    # returned in the dataframe.
    # Use this parameter to obtain a cleaner plot. Notice that the remaining
    # columns will be aggregated as 'others' even if there is a single column
    # beyond the limit.
    
    
    # Create a local copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    
    # Before calling the method, we must guarantee that the variables may be
    # used for that aggregate. Some aggregations are permitted only for numeric variables, so calling
    # the methods before selecting the variables may raise warnings or errors.
    
    
    list_of_aggregates = ['median', 'mean', 'mode', 'sum', 'min', 'max', 'variance', 'count',
                          'standard_deviation', '10_percent_quantile', '20_percent_quantile', 
                          '25_percent_quantile', '30_percent_quantile', '40_percent_quantile', 
                          '50_percent_quantile', '60_percent_quantile', '70_percent_quantile', 
                          '75_percent_quantile', '80_percent_quantile', '90_percent_quantile', 
                          '95_percent_quantile', 'kurtosis', 'skew', 'interquartile_range', 
                          'mean_standard_error', 'entropy']
    
    list_of_numeric_aggregates = ['median', 'mean', 'sum', 'min', 'max', 'variance',
                                  'standard_deviation', '10_percent_quantile', '20_percent_quantile', 
                                  '25_percent_quantile', '30_percent_quantile', '40_percent_quantile', 
                                  '50_percent_quantile', '60_percent_quantile', '70_percent_quantile', 
                                  '75_percent_quantile', '80_percent_quantile', '90_percent_quantile',
                                  '95_percent_quantile', 'kurtosis', 'skew', 'interquartile_range', 
                                  'mean_standard_error']
    
    # Check if an invalid or no aggregation function was selected:
    if ((aggregate_function not in (list_of_aggregates)) | (aggregate_function is None)):
        
        aggregate_function = 'sum'
        print("Invalid or no aggregation function input, so using the default \'sum\'.\n")
    
    # Check if a numeric aggregate was selected:
    if (aggregate_function in list_of_numeric_aggregates):
        
        column_data_type = DATASET[response_var_name].dtype
        
        if ((column_data_type == 'O') | (column_data_type == 'object')):
            
                # If the Pandas series was defined as an object, it means it is categorical
                # (string, date, etc).
                print("Numeric aggregate selected, but categorical variable indicated as response variable.")
                print("Setting aggregate_function = \'mode\', to make aggregate compatible with data type.\n")
                
                aggregate_function = 'mode'
    
    else: # categorical aggregate function
        
        column_data_type = DATASET[response_var_name].dtype
        
        if ((column_data_type != 'O') & (column_data_type != 'object') & (aggregate_function != 'count')):
                # count is the only aggregate for categorical that can be used for numerical variables as well.
                
                print("Categorical aggregate selected, but numeric variable indicated as response variable.")
                print("Setting aggregate_function = \'sum\', to make aggregate compatible with data type.\n")
                
                aggregate_function = 'sum'
    
    # Before grouping, let's remove the missing values, avoiding the raising of TypeError.
    # Pandas deprecated the automatic dropna with aggregation:
    DATASET = DATASET.dropna(axis = 0)
    
    # If an aggregate function different from 'sum', 'mean', 'median' or 'mode' 
    # is used with plot_cumulative_percent = True, 
    # set plot_cumulative_percent = False:
    # (check if aggregate function is not in the list of allowed values):
    if ((aggregate_function not in ['sum', 'mean', 'median', 'mode', 'count']) & (calculate_and_plot_cumulative_percent == True)):
        
        calculate_and_plot_cumulative_percent = False
        print("The cumulative percent is only calculated when aggregate_function = \'sum\', \'mean\', \'median\', \'mode\', or \'count\'. So, plot_cumulative_percent was set as False.")
    
    # Guarantee that the columns from the aggregated dataset have the correct names
    
    # Groupby according to the selection.
    # Here, there is a great gain of performance in not using a dictionary of methods:
    # If using a dictionary of methods, Pandas would calculate the results for each one of the methods.
    
    # Pandas groupby method documentation:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.groupby.html?msclkid=7b3531a6cff211ec9086f4edaddb94ba
    # argument as_index = False: prevents the grouper variable to be set as index of the new dataframe.
    # (default: as_index = True);
    # dropna = False: do not removes the missing values (default: dropna = True, used here to avoid
    # compatibility and version issues)
    
    if (aggregate_function == 'median'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].agg('median')

    elif (aggregate_function == 'mean'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].mean()
    
    elif (aggregate_function == 'mode'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].agg(stats.mode)
    
    elif (aggregate_function == 'sum'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].sum()
    
    elif (aggregate_function == 'count'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].count()

    elif (aggregate_function == 'min'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].min()
    
    elif (aggregate_function == 'max'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].max()
    
    elif (aggregate_function == 'variance'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].var()

    elif (aggregate_function == 'standard_deviation'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].std()
    
    elif (aggregate_function == '10_percent_quantile'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].quantile(0.10)
    
    elif (aggregate_function == '20_percent_quantile'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].quantile(0.20)
    
    elif (aggregate_function == '25_percent_quantile'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].quantile(0.25)
    
    elif (aggregate_function == '30_percent_quantile'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].quantile(0.30)
    
    elif (aggregate_function == '40_percent_quantile'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].quantile(0.40)
    
    elif (aggregate_function == '50_percent_quantile'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].quantile(0.50)

    elif (aggregate_function == '60_percent_quantile'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].quantile(0.60)
    
    elif (aggregate_function == '70_percent_quantile'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].quantile(0.30)

    elif (aggregate_function == '75_percent_quantile'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].quantile(0.75)

    elif (aggregate_function == '80_percent_quantile'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].quantile(0.80)
    
    elif (aggregate_function == '90_percent_quantile'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].quantile(0.90)
    
    elif (aggregate_function == '95_percent_quantile'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].quantile(0.95)

    elif (aggregate_function == 'kurtosis'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].agg(stats.kurtosis)
    
    elif (aggregate_function == 'skew'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].agg(stats.skew)

    elif (aggregate_function == 'interquartile_range'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].agg(stats.iqr)
    
    elif (aggregate_function == 'mean_standard_error'):
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].agg(stats.sem)
    
    else: # entropy
        
        DATASET = DATASET.groupby(by = categorical_var_name, as_index = False, sort = True)[response_var_name].agg(stats.entropy)

        
    if (add_suffix_to_aggregated_col == True):
        
        # Let's add a suffix. Check if suffix is None. If it is,
        # set "_" + aggregate_function as suffix:
        if (suffix is None):
            suffix = "_" + aggregate_function
    
    # List of columns of the aggregated dataset:
    original_columns = list(DATASET.columns) # convert to a list
    
    
    if (aggregate_function == 'mode'):
        
        # The columns will be saved as a series of Tuples. Each row contains a tuple like:
        # ([calculated_mode], [counting_of_occurrences]). We want only the calculated mode.
        # On the other hand, if we do column[0], we will get the columns first row. So, we have to
        # go through each column, retrieving only the mode:
        
        list_of_new_columns = []
        
        for column in (original_columns):
            
            # Loop through each column from the dataset
            if (column == categorical_var_name):
                # special case for the column used for grouping.
                # Simply append this column to a list, without performing any operation
                list_of_col = [categorical_var_name]
            
            else:
                
                if (add_suffix_to_aggregated_col == True):
                        
                        new_column_name = column + suffix
                
                else:
                    new_column_name = column + "_mode"
                    # name for differencing, allowing us to start the variable
                
                # start categorical variable as empty string:
                DATASET[new_column_name] = ''
                
                # Retrieve the index j of new_column_name in the list of columns
                # (use the list attribute to convert the array to list):
                j = (list(DATASET.columns)).index(new_column_name)
                
                # Save the new column on the list of new columns:
                list_of_new_columns.append(new_column_name)
                
                # Now, loop through each row from the dataset:
                for i in range(0, len(DATASET)):
                    # i = 0 to i = len(DATASET) - 1
                    
                    mode_array = DATASET[column][i]
                    # mode array is like:
                    # ModeResult(mode=array([calculated_mode]), count=array([counting_of_occurrences]))
                    # To retrieve only the mode, we must access the element [0][0] from this array:
                    mode = mode_array[0][0]
                    
                    # Now, save the mode in the column j (column new_column_name) for the row i:
                    DATASET.iloc[i, j] = mode
                
        # Now, repeat it for each other variable.
        
        # Concatenate the list list_of_col with list_of_new_columns
        # a = ['a', 'b'] , b = ['c', 'd'], a + b = ['a', 'b', 'c', 'd']
        # b + a = ['c', 'd', 'a', 'b']
        list_of_new_columns = list_of_col + list_of_new_columns
        
        # Subset the dataframe to keep only the columns in list_of_new_columns:
        DATASET = DATASET[list_of_new_columns]
        
        if (add_suffix_to_aggregated_col == False):
            
            # No suffix should be added, i.e., the columns should keep the original names.
            # The names were saved in the list original_columns
            DATASET.columns = original_columns
    
    
    else:
        # default case: one of other aggregate functions was selected
    
        # Guarantee that the columns from the aggregated dataset have the correct names
        # Check if add_suffix_to_aggregated_col is True. If it is, we must add a suffix

        if (add_suffix_to_aggregated_col == True):

            # Let's add a suffix. Check if suffix is None. If it is,
            # set "_" + aggregate_function as suffix:
            if (suffix is None):
                suffix = "_" + aggregate_function

            # Now, concatenate the elements from original_columns to the suffix:
            # Start a support list:
            list_of_new_columns = []

            # loop through each column:
            for column in original_columns:

                if (column == categorical_var_name):
                    # simply append the column, without adding a suffix.
                    # That is because we will not calculate a statistic for this column, since
                    # it is used to aggregate the others:
                    list_of_new_columns.append(column)

                else:
                    # Concatenate the column to the suffix and append it to support_list:
                    list_of_new_columns.append(column + suffix)

            # Now, rename the columns of the aggregated dataset as the list
            # list_of_new_columns:
            DATASET.columns = list_of_new_columns
            
    
    # the name of the response variable is now the second element from the list of column:
    response_var_name = list(DATASET.columns)[1]
    # the categorical variable name was not changed.
    
    # Let's sort the dataframe.
    
    # Order the dataframe in descending order by the response.
    # If there are equal responses, order them by category, in
    # ascending order; put the missing values in the first position
    # To pass multiple columns and multiple types of ordering, we use
    # lists. If there was a single column to order by, we would declare
    # it as a string. If only one order of ascending was used, we would
    # declare it as a simple boolean
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html
    
    DATASET = DATASET.sort_values(by = [response_var_name, categorical_var_name], ascending = [False, True], na_position = 'first')
    
    # Now, reset index positions:
    DATASET = DATASET.reset_index(drop = True)
    
    if (aggregate_function == 'count'):
        
        # Here, the column represent the counting, no matter the variable set as response.
        DATASET.columns = [categorical_var_name, 'count_of_entries']
        response_var_name = 'count_of_entries'
    
    # plot_cumulative_percent = True, create a column to store the
    # cumulative percent:
    if (calculate_and_plot_cumulative_percent): 
        # Run the following code if the boolean value is True (implicity)
        # Only calculates cumulative percent in case aggregate is 'sum' or 'mode'
        
        # Create a column series for the cumulative sum:
        cumsum_col = response_var_name + "_cumsum"
        DATASET[cumsum_col] = DATASET[response_var_name].cumsum()
        
        # total sum is the last element from this series
        # (i.e. the element with index len(DATASET) - 1)
        total_sum = DATASET[cumsum_col][(len(DATASET) - 1)]
        
        # Now, create a column for the accumulated percent
        # by dividing cumsum_col by total_sum and multiplying it by
        # 100 (%):
        cum_pct_col = response_var_name + "_cum_pct"
        DATASET[cum_pct_col] = (DATASET[cumsum_col])/(total_sum) * 100
        print(f"Successfully calculated cumulative sum and cumulative percent correspondent to the response variable {response_var_name}.")
    
    print("Successfully aggregated and ordered the dataset to plot. Check the 10 first rows of this returned dataset:\n")
    print(DATASET.head(10))
    
    # Check if the total of plotted categories is limited:
    if not (limit_of_plotted_categories is None):
        
        # Since the value is not None, we have to limit it
        # Check if the limit is lower than or equal to the length of the dataframe.
        # If it is, we simply copy the columns to the series (there is no need of
        # a memory-consuming loop or of applying the head method to a local copy
        # of the dataframe):
        df_length = len(DATASET)
            
        if (df_length <= limit_of_plotted_categories):
            # Simply copy the columns to the graphic series:
            categories = DATASET[categorical_var_name]
            responses = DATASET[response_var_name]
            # If there is a cum_pct column, copy it to a series too:
            if (calculate_and_plot_cumulative_percent):
                cum_pct = DATASET[cum_pct_col]
        
        else:
            # The limit is lower than the total of categories,
            # so we actually have to limit the size of plotted df:
        
            # If aggregate_function is not 'sum', we simply apply
            # the head method to obtain the first rows (number of
            # rows input as parameter; if no parameter is input, the
            # number of 5 rows is used):
            
            # Limit to the number limit_of_plotted_categories:
            # create another local copy of the dataframe not to
            # modify the returned dataframe object:
            plotted_df = DATASET.copy(deep = True).head(limit_of_plotted_categories)

            # Create the series of elements to plot:
            categories = list(plotted_df[categorical_var_name])
            responses = list(plotted_df[response_var_name])
            # If the cumulative percent was obtained, create the series for it:
            if (calculate_and_plot_cumulative_percent):
                cum_pct = list(plotted_df[cum_pct_col])
            
            # Start variable to store the aggregates from the others:
            other_responses = 0
            
            # Loop through each row from DATASET:
            for i in range(0, len(DATASET)):
                
                # Check if the category is not in categories:
                category = DATASET[categorical_var_name][i]
                
                if (category not in categories):
                    
                    # sum the value in the response variable to other_responses:
                    other_responses = other_responses + DATASET[response_var_name][i]
            
            # Now we finished the sum of the other responses, let's add these elements to
            # the lists:
            categories.append("others")
            responses.append(other_responses)
            # If there is a cumulative percent, append 100% to the list:
            if (calculate_and_plot_cumulative_percent):
                cum_pct.append(100)
                # The final cumulative percent must be the total, 100%
            
            else:

                # Firstly, copy the elements that will be kept to x, y and (possibly) cum_pct
                # lists.
                # Start the lists:
                categories = []
                responses = []
                if (calculate_and_plot_cumulative_percent):
                    cum_pct = [] # start this list only if its needed to save memory

                for i in range (0, limit_of_plotted_categories):
                    # i goes from 0 (first index) to limit_of_plotted_categories - 1
                    # (index of the last category to be kept):
                    # copy the elements from the DATASET to the list
                    # category is the 1st column (column 0); response is the 2nd (col 1);
                    # and cumulative percent is the 4th (col 3):
                    categories.append(DATASET.iloc[i, 0])
                    responses.append(DATASET.iloc[i, 1])
                    
                    if (calculate_and_plot_cumulative_percent):
                        cum_pct.append(DATASET.iloc[i, 3]) # only if there is something to iloc
                    
                # Now, i = limit_of_plotted_categories - 1
                # Create a variable to store the sum of other responses
                other_responses = 0
                # loop from i = limit_of_plotted_categories to i = df_length-1, index
                # of the last element. Notice that this loop may have a single call, if there
                # is only one element above the limit:
                for i in range (limit_of_plotted_categories, (df_length - 1)):
                    
                    other_responses = other_responses + (DATASET.iloc[i, 1])
                
                # Now, add the last elements to the series:
                # The last category is named 'others':
                categories.append('others')
                # The correspondent aggregated response is the value 
                # stored in other_responses:
                responses.append(other_responses)
                # The cumulative percent is 100%, since this must be the sum of all
                # elements (the previous ones plus the ones aggregated as 'others'
                # must totalize 100%).
                # On the other hand, the cumulative percent is stored only if needed:
                cum_pct.append(100)
    
    else:
        # This is the situation where there is no limit of plotted categories. So, we
        # simply copy the columns to the plotted series (it is equivalent to the 
        # situation where there is a limit, but the limit is equal or inferior to the
        # size of the dataframe):
        categories = DATASET[categorical_var_name]
        responses = DATASET[response_var_name]
        # If there is a cum_pct column, copy it to a series too:
        if (calculate_and_plot_cumulative_percent):
            cum_pct = DATASET[cum_pct_col]
    
    
    # Now the data is prepared and we only have to plot 
    # categories, responses, and cum_pct:
    
    # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
    # so that the bars do not completely block other views.
    OPACITY = 0.95
    
    # Set labels and titles for the case they are None
    if (plot_title is None):
        
        if (aggregate_function == 'count'):
            # The graph is the same count, no matter the response
            plot_title = f"Bar_chart_count_of_{categorical_var_name}"
        
        else:
            plot_title = f"Bar_chart_for_{response_var_name}_by_{categorical_var_name}"
    
    if (horizontal_axis_title is None):

        horizontal_axis_title = categorical_var_name

    if (vertical_axis_title is None):
        # Notice that response_var_name already has the suffix indicating the
        # aggregation function
        vertical_axis_title = response_var_name
    
    fig, ax1 = plt.subplots(figsize = (12, 8))
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
        ax1.set_ylabel(horizontal_axis_title)
        ax1.set_xlabel(vertical_axis_title, color = 'darkblue')
        
        # Horizontal bars used - barh method (bar horizontal):
        # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.barh.html
        # Now, the categorical variables stored in series categories must be
        # positioned as the vertical axis Y, whereas the correspondent responses
        # must be in the horizontal axis X.
        ax1.barh(categories, responses, color = 'darkblue', alpha = OPACITY, label = categorical_var_name)
        #.barh(y, x, ...)
        
        if (calculate_and_plot_cumulative_percent):
            # Let's plot the line for the cumulative percent
            # Set the grid for the bar chart as False. If it is True, there will
            # be to grids, one for the bars and other for the percents, making 
            # the image difficult to interpretate:
            ax1.grid(False)
            
            # Create the twin plot for the cumulative percent:
            # for the vertical orientation, we use the twinx. Here, we use twiny
            ax2 = ax1.twiny()
            # Here, the x axis must be the cum_pct value, and the Y
            # axis must be categories (it must be correspondent to the
            # bar chart)
            ax2.plot(cum_pct, categories, '-ro', color = 'red', label = "cumulative\npercent")
            #.plot(x, y, ...)
            ax2.tick_params('x', color = 'red')
            ax2.set_xlabel("Cumulative Percent (%)", color = 'red')
            ax2.legend()
            ax2.grid(grid) # shown if user set grid = True
            # If user wants to see the grid, it is shown only for the cumulative line.
        
        else:
            # There is no cumulative line, so the parameter grid must control 
            # the bar chart's grid
            ax1.legend()
            ax1.grid(grid)
        
    else: 
        
        ax1.set_xlabel(horizontal_axis_title)
        ax1.set_ylabel(vertical_axis_title, color = 'darkblue')
        # If None or an invalid orientation was used, set it as vertical
        # Use Matplotlib standard bar method (vertical bar):
        # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html#matplotlib.pyplot.bar
        
        # In this standard case, the categorical variables (categories) are positioned
        # as X, and the responses as Y:
        ax1.bar(categories, responses, color = 'darkblue', alpha = OPACITY, label = categorical_var_name)
        #.bar(x, y, ...)
        
        if (calculate_and_plot_cumulative_percent):
            # Let's plot the line for the cumulative percent
            # Set the grid for the bar chart as False. If it is True, there will
            # be to grids, one for the bars and other for the percents, making 
            # the image difficult to interpretate:
            ax1.grid(False)
            
            # Create the twin plot for the cumulative percent:
            ax2 = ax1.twinx()
            ax2.plot(categories, cum_pct, '-ro', color = 'red', label = "cumulative\npercent")
            #.plot(x, y, ...)
            ax2.tick_params('y', color = 'red')
            ax2.set_ylabel("Cumulative Percent (%)", color = 'red', rotation = 270)
            # rotate the twin axis so that its label is inverted in relation to the main
            # vertical axis.
            ax2.legend()
            ax2.grid(grid) # shown if user set grid = True
            # If user wants to see the grid, it is shown only for the cumulative line.
        
        else:
            # There is no cumulative line, so the parameter grid must control 
            # the bar chart's grid
            ax1.legend()
            ax1.grid(grid)
    
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
            file_name = "bar_chart"
        
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
    
    return DATASET


def calculate_cumulative_stats (df, column_to_analyze, cumulative_statistic = 'sum', new_cum_stats_col_name = None):
    
    import numpy as np
    import pandas as pd
    
    # df: the whole dataframe to be processed.
    
    # column_to_analyze: string (inside quotes), 
    # containing the name of the column that will be analyzed. 
    # e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    # cumulative_statistic: the statistic that will be calculated. The cumulative
    # statistics allowed are: 'sum' (for cumulative sum, cumsum); 'product' 
    # (for cumulative product, cumprod); 'max' (for cumulative maximum, cummax);
    # and 'min' (for cumulative minimum, cummin).
    
    # new_cum_stats_col_name = None or string (inside quotes), 
    # containing the name of the new column created for storing the cumulative statistic
    # calculated. 
    # e.g. new_cum_stats_col_name = "cum_stats" will create a column named as 'cum_stats'.
    # If its None, the new column will be named as column_to_analyze + "_" + [selected
    # cumulative function] ('cumsum', 'cumprod', 'cummax', 'cummin')
     
    
    #WARNING: Use this function to a analyze a single column from a dataframe.
    
    if ((cumulative_statistic not in ['sum', 'product', 'max', 'min']) | (cumulative_statistic is None)):
        
        print("Please, select a valid method for calculating the cumulative statistics: sum, product, max, or min.")
        return "error"
    
    else:
        
        if (new_cum_stats_col_name is None):
            # set the standard name
            # column_to_analyze + "_" + [selected cumulative function] 
            # ('cumsum', 'cumprod', 'cummax', 'cummin')
            # cumulative_statistic variable stores ['sum', 'product', 'max', 'min']
            # we must concatenate "cum" to the left of this string:
            new_cum_stats_col_name = column_to_analyze + "_" + "cum" + cumulative_statistic
        
        # create a local copy of the dataframe to manipulate:
        DATASET = df.copy(deep = True)
        # The series to be analyzed is stored as DATASET[column_to_analyze]
        
        # Now apply the correct method
        # the dictionary dict_of_methods correlates the input cumulative_statistic to the
        # correct Pandas method to be applied to the dataframe column
        dict_of_methods = {
            
            'sum': DATASET[column_to_analyze].cumsum(),
            'product': DATASET[column_to_analyze].cumprod(),
            'max': DATASET[column_to_analyze].cummax(),
            'min': DATASET[column_to_analyze].cummin()
        }
        
        # To access the value (method) correspondent to a given key (input as 
        # cumulative_statistic): dictionary['key'], just as if accessing a column from
        # a dataframe. In this case, the method is accessed as:
        # dict_of_methods[cumulative_statistic], since cumulative_statistic is itself the key
        # of the dictionary of methods.
        
        # store the resultant of the method in a new column of DATASET 
        # named as new_cum_stats_col_name
        DATASET[new_cum_stats_col_name] = dict_of_methods[cumulative_statistic]
        
        print(f"The cumulative {cumulative_statistic} statistic was successfully calculated and added as the column \'{new_cum_stats_col_name}\' of the returned dataframe.")
        print("Check the new dataframe's 10 first rows:\n")
        print(DATASET.head(10))
        
        return DATASET


def scatter_plot_lin_reg (data_in_same_column = False, df = None, column_with_predict_var_x = None, column_with_response_var_y = None, column_with_labels = None, list_of_dictionaries_with_series_to_analyze = [{'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}], x_axis_rotation = 70, y_axis_rotation = 0, show_linear_reg = True, grid = True, add_splines_lines = False, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330): 
    
    import random
    # Python Random documentation:
    # https://docs.python.org/3/library/random.html?msclkid=9d0c34b2d13111ec9cfa8ddaee9f61a1
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    from scipy import stats
    
    # matplotlib.colors documentation:
    # https://matplotlib.org/3.5.0/api/colors_api.html?msclkid=94286fa9d12f11ec94660321f39bf47f
    
    # Matplotlib list of colors:
    # https://matplotlib.org/stable/gallery/color/named_colors.html?msclkid=0bb86abbd12e11ecbeb0a2439e5b0d23
    # Matplotlib colors tutorial:
    # https://matplotlib.org/stable/tutorials/colors/colors.html
    # Matplotlib example of Python code using matplotlib.colors:
    # https://matplotlib.org/stable/_downloads/0843ee646a32fc214e9f09328c0cd008/colors.py
    # Same example as Jupyter Notebook:
    # https://matplotlib.org/stable/_downloads/2a7b13c059456984288f5b84b4b73f45/colors.ipynb
    
        
    # data_in_same_column = False: set as True if all the values to plot are in a same column.
    # If data_in_same_column = True, you must specify the dataframe containing the data as df;
    # the column containing the predict variable (X) as column_with_predict_var_x; the column 
    # containing the responses to plot (Y) as column_with_response_var_y; and the column 
    # containing the labels (subgroup) indication as column_with_labels. 
    # df is an object, so do not declare it in quotes. The other three arguments (columns' names) 
    # are strings, so declare in quotes. 
    
    # Example: suppose you have a dataframe saved as dataset, and two groups A and B to compare. 
    # All the results for both groups are in a column named 'results', wich will be plot against
    # the time, saved as 'time' (X = 'time'; Y = 'results'). If the result is for
    # an entry from group A, then a column named 'group' has the value 'A'. If it is for group B,
    # column 'group' shows the value 'B'. In this example:
    # data_in_same_column = True,
    # df = dataset,
    # column_with_predict_var_x = 'time',
    # column_with_response_var_y = 'results', 
    # column_with_labels = 'group'
    # If you want to declare a list of dictionaries, keep data_in_same_column = False and keep
    # df = None (the other arguments may be set as None, but it is not mandatory: 
    # column_with_predict_var_x = None, column_with_response_var_y = None, column_with_labels = None).
    

    # Parameter to input when DATA_IN_SAME_COLUMN = False:
    # list_of_dictionaries_with_series_to_analyze: if data is already converted to series, lists
    # or arrays, provide them as a list of dictionaries. It must be declared as a list, in brackets,
    # even if there is a single dictionary.
    # Use always the same keys: 'x' for the X-series (predict variables); 'y' for the Y-series
    # (response variables); and 'lab' for the labels. If you do not want to declare a series, simply
    # keep as None, but do not remove or rename a key (ALWAYS USE THE KEYS SHOWN AS MODEL).
    # If you want, you can remove elements (dictionaries) from the list to declare fewer elements;
    # and you can also add more elements (dictionaries) to the lists, if you need to plot more series.
    # Simply put a comma after the last element from the list and declare a new dictionary, keeping the
    # same keys: {'x': x_series, 'y': y_series, 'lab': label}, where x_series, y_series and label
    # represents the series and label of the added dictionary (you can pass 'lab': None, but if 
    # 'x' or 'y' are None, the new dictionary will be ignored).
    
    # Examples:
    # list_of_dictionaries_with_series_to_analyze = 
    # [{'x': DATASET['X'], 'y': DATASET['Y'], 'lab': 'label'}]
    # will plot a single variable. In turns:
    # list_of_dictionaries_with_series_to_analyze = 
    # [{'x': DATASET['X'], 'y': DATASET['Y1'], 'lab': 'label'}, {'x': DATASET['X'], 'y': DATASET['Y2'], 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}]
    # will plot two series, Y1 x X and Y2 x X.
    # Notice that all dictionaries where 'x' or 'y' are None are automatically ignored.
    # If None is provided to 'lab', an automatic label will be generated.
    
    if (data_in_same_column == True):
        
        print("Data to be plotted in a same column.\n")
        
        if (df is None):
            
            print("Please, input a valid dataframe as df.\n")
            list_of_dictionaries_with_series_to_analyze = []
            # The code will check the size of this list on the next block.
            # If it is zero, code is simply interrupted.
            # Instead of returning an error, we use this code structure that can be applied
            # on other graphic functions that do not return a summary (and so we should not
            # return a value like 'error' to interrupt the function).
        
        elif (column_with_predict_var_x is None):
            
            print("Please, input a valid column name as column_with_predict_var_x.\n")
            list_of_dictionaries_with_series_to_analyze = []
           
        elif (column_with_response_var_y is None):
            
            print("Please, input a valid column name as column_with_response_var_y.\n")
            list_of_dictionaries_with_series_to_analyze = []
        
        elif (column_with_labels is None):
            
            print("Please, input a valid column name as column_with_labels.\n")
            list_of_dictionaries_with_series_to_analyze = []
        
        else:
            
            # set a local copy of the dataframe:
            DATASET = df.copy(deep = True)
            
            # sort DATASET; by column_with_predict_var_x; by column column_with_labels
            # and by column_with_response_var_y, all in Ascending order
            # Since we sort by label (group), it is easier to separate the groups.
            DATASET = DATASET.sort_values(by = [column_with_predict_var_x, column_with_labels, column_with_response_var_y], ascending = [True, True, True])
            
            # Reset indices:
            DATASET = DATASET.reset_index(drop = True)
            
            # If column_with_predict_var_x is an object, the user may be trying to pass a date as x. 
            # So, let's try to convert it to datetime:
            if (((DATASET[column_with_predict_var_x]).dtype == 'O') | ((DATASET[column_with_predict_var_x]).dtype == 'object')):
                  
                try:
                    DATASET[column_with_predict_var_x] = (DATASET[column_with_predict_var_x]).astype('datetime64[ns]')
                    print("Variable X successfully converted to datetime64[ns].\n")
                    
                except:
                    # Simply ignore it
                    pass
            
            # Get a series of unique values of the labels, and save it as a list using the
            # list attribute:
            unique_labels = list(DATASET[column_with_labels].unique())
            print(f"{len(unique_labels)} different labels detected: {unique_labels}.\n")
            
            # Start a list to store the dictionaries containing the keys:
            # 'x': list of predict variables; 'y': list of responses; 'lab': the label (group)
            list_of_dictionaries_with_series_to_analyze = []
            
            # Loop through each possible label:
            for lab in unique_labels:
                # loop through each element from the list unique_labels, referred as lab
                
                # Set a filter for the dataset, to select only rows correspondent to that
                # label:
                boolean_filter = (DATASET[column_with_labels] == lab)
                
                # Create a copy of the dataset, with entries selected by that filter:
                ds_copy = (DATASET[boolean_filter]).copy(deep = True)
                # Sort again by X and Y, to guarantee the results are in order:
                ds_copy = ds_copy.sort_values(by = [column_with_predict_var_x, column_with_response_var_y], ascending = [True, True])
                # Restart the index of the copy:
                ds_copy = ds_copy.reset_index(drop = True)
                
                # Re-extract the X and Y series and convert them to NumPy arrays 
                # (these arrays will be important later in the function):
                x = np.array(ds_copy[column_with_predict_var_x])
                y = np.array(ds_copy[column_with_response_var_y])
            
                # Then, create the dictionary:
                dict_of_values = {'x': x, 'y': y, 'lab': lab}
                
                # Now, append dict_of_values to list_of_dictionaries_with_series_to_analyze:
                list_of_dictionaries_with_series_to_analyze.append(dict_of_values)
                
            # Now, we have a list of dictionaries with the same format of the input list.
            
    else:
        
        # The user input a list_of_dictionaries_with_series_to_analyze
        # Create a support list:
        support_list = []
        
        # Loop through each element on the list list_of_dictionaries_with_series_to_analyze:
        
        for i in range (0, len(list_of_dictionaries_with_series_to_analyze)):
            # from i = 0 to i = len(list_of_dictionaries_with_series_to_analyze) - 1, index of the
            # last element from the list
            
            # pick the i-th dictionary from the list:
            dictionary = list_of_dictionaries_with_series_to_analyze[i]
            
            # access 'x', 'y', and 'lab' keys from the dictionary:
            x = dictionary['x']
            y = dictionary['y']
            lab = dictionary['lab']
            # Remember that all this variables are series from a dataframe, so we can apply
            # the astype function:
            # https://www.askpython.com/python/built-in-methods/python-astype?msclkid=8f3de8afd0d411ec86a9c1a1e290f37c
            
            # check if at least x and y are not None:
            if ((x is not None) & (y is not None)):
                
                # If column_with_predict_var_x is an object, the user may be trying to pass a date as x. 
                # So, let's try to convert it to datetime:
                if ((x.dtype == 'O') | (x.dtype == 'object')):

                    try:
                        x = (x).astype('datetime64[ns]')
                        print(f"Variable X from {i}-th dictionary successfully converted to datetime64[ns].\n")

                    except:
                        # Simply ignore it
                        pass
                
                # Possibly, x and y are not ordered. Firstly, let's merge them into a temporary
                # dataframe to be able to order them together.
                # Use the 'list' attribute to guarantee that x and y were read as lists. These lists
                # are the values for a dictionary passed as argument for the constructor of the
                # temporary dataframe. When using the list attribute, we make the series independent
                # from its origin, even if it was created from a Pandas dataframe. Then, we have a
                # completely independent dataframe that may be manipulated and sorted, without worrying
                # that it may modify its origin:
                
                temp_df = pd.DataFrame(data = {'x': list(x), 'y': list(y)})
                # sort this dataframe by 'x' and 'y':
                temp_df = temp_df.sort_values(by = ['x', 'y'], ascending = [True, True])
                # restart index:
                temp_df = temp_df.reset_index(drop = True)
                
                # Re-extract the X and Y series and convert them to NumPy arrays 
                # (these arrays will be important later in the function):
                x = np.array(temp_df['x'])
                y = np.array(temp_df['y'])
                
                # check if lab is None:
                if (lab is None):
                    # input a default label.
                    # Use the str attribute to convert the integer to string, allowing it
                    # to be concatenated
                    lab = "X" + str(i) + "_x_" + "Y" + str(i)
                    
                # Then, create the dictionary:
                dict_of_values = {'x': x, 'y': y, 'lab': lab}
                
                # Now, append dict_of_values to support list:
                support_list.append(dict_of_values)
            
        # Now, support_list contains only the dictionaries with valid entries, as well
        # as labels for each collection of data. The values are independent from their origin,
        # and now they are ordered and in the same format of the data extracted directly from
        # the dataframe.
        # So, make the list_of_dictionaries_with_series_to_analyze the support_list itself:
        list_of_dictionaries_with_series_to_analyze = support_list
        print(f"{len(list_of_dictionaries_with_series_to_analyze)} valid series input.\n")

        
    # Now that both methods of input resulted in the same format of list, we can process both
    # with the same code.
    
    # Each dictionary in list_of_dictionaries_with_series_to_analyze represents a series to
    # plot. So, the total of series to plot is:
    total_of_series = len(list_of_dictionaries_with_series_to_analyze)
    
    if (total_of_series <= 0):
        
        print("No valid series to plot. Please, provide valid arguments.\n")
        return "error" 
        # we return the value because this function always returns an object.
        # In other functions, this return would be omitted.
    
    else:
        
        # Continue to plotting and calculating the fitting.
        # Notice that we sorted the all the lists after they were separated and before
        # adding them to dictionaries. Also, the timestamps were converted to datetime64 variables
        
        # Now we pre-processed the data, we can obtain a final list of dictionaries, containing
        # the linear regression information (it will be plotted only if the user asked to). Start
        # a list to store all predictions:
        list_of_dictionaries_with_series_and_predictions = []
        
        # Loop through each dictionary (element) on the list list_of_dictionaries_with_series_to_analyze:
        for dictionary in list_of_dictionaries_with_series_to_analyze:
                
            # Access keys 'x' and 'y' to retrieve the arrays.
            x = dictionary['x']
            y = dictionary['y']
            
            # Check if the elements from array x are np.datetime64 objects. Pick the first
            # element to check:
            if (type(x[0]) == np.datetime64):
                # In this case, performing the linear regression directly in X will
                # return an error. We must associate a sequential number to each time.
                # to keep the distance between these integers the same as in the original sequence
                # let's define a difference of 1 ns as 1. The 1st timestamp will be zero, and the
                # addition of 1 ns will be an addition of 1 unit. So a timestamp recorded 10 ns
                # after the time zero will have value 10. At the end, we divide every element by
                # 10**9, to obtain the correspondent distance in seconds.
                
                # start a list for the associated integer timescale. Put the number zero,
                # associated to the first timestamp:
                int_timescale = [0]
                
                # loop through each element of the array x, starting from index 1:
                for i in range(1, len(x)):
                    
                    # calculate the timedelta between x[i] and x[i-1]:
                    # The delta method from the Timedelta class converts the timedelta to
                    # nanoseconds, guaranteeing the internal compatibility:
                    timedelta = pd.Timedelta(x[i] - x[(i-1)]).delta
                    
                    # Sum this timedelta (integer number of nanoseconds) to the
                    # previous element from int_timescale, and append the result to the list:
                    int_timescale.append((timedelta + int_timescale[(i-1)]))
                
                # Now convert the new scale (that preserves the distance between timestamps)
                # to NumPy array:
                int_timescale = np.array(int_timescale)
                
                # Divide by 10**9 to obtain the distances in seconds, reducing the order of
                # magnitude of the integer numbers (the division is allowed for arrays)
                int_timescale = int_timescale / (10**9)
                
                # Finally, use this timescale to obtain the linear regression:
                lin_reg = stats.linregress(int_timescale, y = y)
            
            else:
                # Obtain the linear regression object directly from x. Since x is not a
                # datetime object, we can calculate the regression directly on it:
                lin_reg = stats.linregress(x, y = y)
                
            # Retrieve the equation as a string.
            # Access the attributes intercept and slope from the lin_reg object:
            lin_reg_equation = "y = %.2f*x + %.2f" %((lin_reg).slope, (lin_reg).intercept)
            # .2f: float with only two decimals
                
            # Retrieve R2 (coefficient of correlation) also as a string
            r2_lin_reg = "R²_lin_reg = %.4f" %(((lin_reg).rvalue) ** 2)
            # .4f: 4 decimals. ((lin_reg).rvalue) is the coefficient R. We
            # raise it to the second power by doing **2, where ** is the potentiation.
                
            # Add these two strings to the dictionary
            dictionary['lin_reg_equation'] = lin_reg_equation
            dictionary['r2_lin_reg'] = r2_lin_reg
                
            # Now, as final step, let's apply the values x to the linear regression
            # equation to obtain the predicted series used to plot the straight line.
                
            # The lists cannot perform vector operations like element-wise sum or product, 
            # but numpy arrays can. For example, [1, 2] + 1 would be interpreted as the try
            # for concatenation of two lists, resulting in error. But, np.array([1, 2]) + 1
            # is allowed, resulting in: np.array[2, 3].
            # This and the fact that Scipy and Matplotlib are built on NumPy were the reasons
            # why we converted every list to numpy arrays.
            
            # Save the predicted values as the array y_pred_lin_reg.
            # Access the attributes intercept and slope from the lin_reg object.
            # The equation is y = (slope * x) + intercept
            
            # Notice that again we cannot apply the equation directly to a timestamp.
            # So once again we will apply the integer scale to obtain the predictions
            # if we are dealing with datetime objects:
            if (type(x[0]) == np.datetime64):
                y_pred_lin_reg = ((lin_reg).intercept) + ((lin_reg).slope) * (int_timescale)
            
            else:
                # x is not a timestamp, so we can directly apply it to the regression
                # equation:
                y_pred_lin_reg = ((lin_reg).intercept) + ((lin_reg).slope) * (x)
            
            # Add this array to the dictionary with the key 'y_pred_lin_reg':
            dictionary['y_pred_lin_reg'] = y_pred_lin_reg
            
            if (type(x[0]) == np.datetime64):
            
                print("For performing the linear regression, a sequence of floats proportional to the timestamps was created. In this sequence, check on the returned object a dictionary containing the timestamps and the correspondent integers, that keeps the distance proportion between successive timestamps. The sequence was created by calculating the timedeltas as an integer number of nanoseconds, which were converted to seconds. The first timestamp was considered time = 0.")
                print("Notice that the regression equation is based on the use of this sequence of floats as X.\n")
                
                dictionary['sequence_of_floats_correspondent_to_timestamps'] = {
                                                                                'original_timestamps': x,
                                                                                'sequence_of_floats': int_timescale
                                                                                }
            
            # Finally, append this dictionary to list support_list:
            list_of_dictionaries_with_series_and_predictions.append(dictionary)
        
        print("Returning a list of dictionaries. Each one contains the arrays of valid series and labels, and the equations, R² and values predicted by the linear regressions.\n")
        
        # Now we finished the loop, list_of_dictionaries_with_series_and_predictions 
        # contains all series converted to NumPy arrays, with timestamps parsed as datetimes, 
        # and all the information regarding the linear regression, including the predicted 
        # values for plotting.
        # This list will be the object returned at the end of the function. Since it is an
        # JSON-formatted list, we can use the function json_obj_to_pandas_dataframe to convert
        # it to a Pandas dataframe.
        
        
        # Now, we can plot the figure.
        # we set alpha = 0.95 (opacity) to give a degree of transparency (5%), 
        # so that one series do not completely block the visualization of the other.
        
        # Let's retrieve the list of Matplotlib CSS colors:
        css4 = mcolors.CSS4_COLORS
        # css4 is a dictionary of colors: {'aliceblue': '#F0F8FF', 'antiquewhite': '#FAEBD7', ...}
        # Each key of this dictionary is a color name to be passed as argument color on the plot
        # function. So let's retrieve the array of keys, and use the list attribute to convert this
        # array to a list of colors:
        list_of_colors = list(css4.keys())
        
        # In 11 May 2022, this list of colors had 148 different elements
        # Since this list is in alphabetic order, let's create a random order for the colors.
        
        # Function random.sample(input_sequence, number_of_samples): 
        # this function creates a list containing a total of elements equals to the parameter 
        # "number_of_samples", which must be an integer.
        # This list is obtained by ramdomly selecting a total of "number_of_samples" elements from the
        # list "input_sequence" passed as parameter.
        
        # Function random.choices(input_sequence, k = number_of_samples):
        # similarly, randomly select k elements from the sequence input_sequence. This function is
        # newer than random.sample
        # Since we want to simply randomly sort the sequence, we can pass k = len(input_sequence)
        # to obtain the randomly sorted sequence:
        list_of_colors = random.choices(list_of_colors, k = len(list_of_colors))
        # Now, we have a random list of colors to use for plotting the charts
        
        if (add_splines_lines == True):
            LINE_STYLE = '-'

        else:
            LINE_STYLE = ''
        
        # Matplotlib linestyle:
        # https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html?msclkid=68737f24d16011eca9e9c4b41313f1ad
        
        if (plot_title is None):
            # Set graphic title
            plot_title = f"Y_x_X"

        if (horizontal_axis_title is None):
            # Set horizontal axis title
            horizontal_axis_title = "X"

        if (vertical_axis_title is None):
            # Set vertical axis title
            vertical_axis_title = "Y"
        
        # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
        # so that the bars do not completely block other views.
        OPACITY = 0.95
        
        #Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
        fig = plt.figure(figsize = (12, 8))
        ax = fig.add_subplot()

        i = 0 # Restart counting for the loop of colors
        
        # Loop through each dictionary from list_of_dictionaries_with_series_and_predictions:
        for dictionary in list_of_dictionaries_with_series_and_predictions:
            
            # Try selecting a color from list_of_colors:
            try:
                
                COLOR = list_of_colors[i]
                # Go to the next element i, so that the next plot will use a different color:
                i = i + 1
            
            except IndexError:
                
                # This error will be raised if list index is out of range, 
                # i.e. if i >= len(list_of_colors) - we used all colors from the list (at least 148).
                # So, return the index to zero to restart the colors from the beginning:
                i = 0
                COLOR = list_of_colors[i]
                i = i + 1
            
            # Access the arrays and label from the dictionary:
            X = dictionary['x']
            Y = dictionary['y']
            LABEL = dictionary['lab']
            
            # Scatter plot:
            ax.plot(X, Y, linestyle = LINE_STYLE, marker = "o", color = COLOR, alpha = OPACITY, label = LABEL)
            # Axes.plot documentation:
            # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html?msclkid=42bc92c1d13511eca8634a2c93ab89b5
            
            # x and y are positional arguments: they are specified by their position in function
            # call, not by an argument name like 'marker'.
            
            # Matplotlib markers:
            # https://matplotlib.org/stable/api/markers_api.html?msclkid=36c5eec5d16011ec9583a5777dc39d1f
            
            if (show_linear_reg == True):
                
                # Plot the linear regression using the same color.
                # Access the array of fitted Y's in the dictionary:
                Y_PRED = dictionary['y_pred_lin_reg']
                Y_PRED_LABEL = 'lin_reg_' + LABEL
                
                ax.plot(X, Y_PRED,  linestyle = '-', marker = '', color = COLOR, alpha = OPACITY, label = Y_PRED_LABEL)

        # Now we finished plotting all of the series, we can set the general configuration:
        
        #ROTATE X AXIS IN XX DEGREES
        plt.xticks(rotation = x_axis_rotation)
        # XX = 0 DEGREES x_axis (Default)
        #ROTATE Y AXIS IN XX DEGREES:
        plt.yticks(rotation = y_axis_rotation)
        # XX = 0 DEGREES y_axis (Default)
        
        ax.set_title(plot_title)
        ax.set_xlabel(horizontal_axis_title)
        ax.set_ylabel(vertical_axis_title)

        ax.grid(grid) # show grid or not
        ax.legend(loc = 'upper left')
        # position options: 'upper right'; 'upper left'; 'lower left'; 'lower right';
        # 'right', 'center left'; 'center right'; 'lower center'; 'upper center', 'center'
        # https://www.statology.org/matplotlib-legend-position/

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
                file_name = "scatter_plot_lin_reg"

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
        
        if (show_linear_reg == True):
            print("\nLinear regression summaries (equations and R²):\n")
            
            for dictionary in list_of_dictionaries_with_series_and_predictions:
                
                print(f"Linear regression summary for {dictionary['lab']}:\n")
                print(dictionary['lin_reg_equation'])
                print(dictionary['r2_lin_reg'])
                print("\n")
         
        
        return list_of_dictionaries_with_series_and_predictions


def time_series_vis (data_in_same_column = False, df = None, column_with_predict_var_x = None, column_with_response_var_y = None, column_with_labels = None, list_of_dictionaries_with_series_to_analyze = [{'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}], x_axis_rotation = 70, y_axis_rotation = 0, grid = True, add_splines_lines = True, add_scatter_dots = False, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
     
    import random
    # Python Random documentation:
    # https://docs.python.org/3/library/random.html?msclkid=9d0c34b2d13111ec9cfa8ddaee9f61a1
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    
    # matplotlib.colors documentation:
    # https://matplotlib.org/3.5.0/api/colors_api.html?msclkid=94286fa9d12f11ec94660321f39bf47f
    
    # Matplotlib list of colors:
    # https://matplotlib.org/stable/gallery/color/named_colors.html?msclkid=0bb86abbd12e11ecbeb0a2439e5b0d23
    # Matplotlib colors tutorial:
    # https://matplotlib.org/stable/tutorials/colors/colors.html
    # Matplotlib example of Python code using matplotlib.colors:
    # https://matplotlib.org/stable/_downloads/0843ee646a32fc214e9f09328c0cd008/colors.py
    # Same example as Jupyter Notebook:
    # https://matplotlib.org/stable/_downloads/2a7b13c059456984288f5b84b4b73f45/colors.ipynb
    
        
    # data_in_same_column = False: set as True if all the values to plot are in a same column.
    # If data_in_same_column = True, you must specify the dataframe containing the data as df;
    # the column containing the predict variable (X) as column_with_predict_var_x; the column 
    # containing the responses to plot (Y) as column_with_response_var_y; and the column 
    # containing the labels (subgroup) indication as column_with_labels. 
    # df is an object, so do not declare it in quotes. The other three arguments (columns' names) 
    # are strings, so declare in quotes. 
    
    # Example: suppose you have a dataframe saved as dataset, and two groups A and B to compare. 
    # All the results for both groups are in a column named 'results', wich will be plot against
    # the time, saved as 'time' (X = 'time'; Y = 'results'). If the result is for
    # an entry from group A, then a column named 'group' has the value 'A'. If it is for group B,
    # column 'group' shows the value 'B'. In this example:
    # data_in_same_column = True,
    # df = dataset,
    # column_with_predict_var_x = 'time',
    # column_with_response_var_y = 'results', 
    # column_with_labels = 'group'
    # If you want to declare a list of dictionaries, keep data_in_same_column = False and keep
    # df = None (the other arguments may be set as None, but it is not mandatory: 
    # column_with_predict_var_x = None, column_with_response_var_y = None, column_with_labels = None).
    

    # Parameter to input when DATA_IN_SAME_COLUMN = False:
    # list_of_dictionaries_with_series_to_analyze: if data is already converted to series, lists
    # or arrays, provide them as a list of dictionaries. It must be declared as a list, in brackets,
    # even if there is a single dictionary.
    # Use always the same keys: 'x' for the X-series (predict variables); 'y' for the Y-series
    # (response variables); and 'lab' for the labels. If you do not want to declare a series, simply
    # keep as None, but do not remove or rename a key (ALWAYS USE THE KEYS SHOWN AS MODEL).
    # If you want, you can remove elements (dictionaries) from the list to declare fewer elements;
    # and you can also add more elements (dictionaries) to the lists, if you need to plot more series.
    # Simply put a comma after the last element from the list and declare a new dictionary, keeping the
    # same keys: {'x': x_series, 'y': y_series, 'lab': label}, where x_series, y_series and label
    # represents the series and label of the added dictionary (you can pass 'lab': None, but if 
    # 'x' or 'y' are None, the new dictionary will be ignored).
    
    # Examples:
    # list_of_dictionaries_with_series_to_analyze = 
    # [{'x': DATASET['X'], 'y': DATASET['Y'], 'lab': 'label'}]
    # will plot a single variable. In turns:
    # list_of_dictionaries_with_series_to_analyze = 
    # [{'x': DATASET['X'], 'y': DATASET['Y1'], 'lab': 'label'}, {'x': DATASET['X'], 'y': DATASET['Y2'], 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}]
    # will plot two series, Y1 x X and Y2 x X.
    # Notice that all dictionaries where 'x' or 'y' are None are automatically ignored.
    # If None is provided to 'lab', an automatic label will be generated.
    
    if (data_in_same_column == True):
        
        print("Data to be plotted in a same column.\n")
        
        if (df is None):
            
            print("Please, input a valid dataframe as df.\n")
            list_of_dictionaries_with_series_to_analyze = []
            # The code will check the size of this list on the next block.
            # If it is zero, code is simply interrupted.
            # Instead of returning an error, we use this code structure that can be applied
            # on other graphic functions that do not return a summary (and so we should not
            # return a value like 'error' to interrupt the function).
        
        elif (column_with_predict_var_x is None):
            
            print("Please, input a valid column name as column_with_predict_var_x.\n")
            list_of_dictionaries_with_series_to_analyze = []
           
        elif (column_with_response_var_y is None):
            
            print("Please, input a valid column name as column_with_response_var_y.\n")
            list_of_dictionaries_with_series_to_analyze = []
        
        elif (column_with_labels is None):
            
            print("Please, input a valid column name as column_with_labels.\n")
            list_of_dictionaries_with_series_to_analyze = []
        
        else:
            
            # set a local copy of the dataframe:
            DATASET = df.copy(deep = True)
            
            # sort DATASET; by column_with_predict_var_x; by column column_with_labels
            # and by column_with_response_var_y, all in Ascending order
            # Since we sort by label (group), it is easier to separate the groups.
            DATASET = DATASET.sort_values(by = [column_with_predict_var_x, column_with_labels, column_with_response_var_y], ascending = [True, True, True])
            
            # Reset indices:
            DATASET = DATASET.reset_index(drop = True)
            
            # If column_with_predict_var_x is an object, the user may be trying to pass a date as x. 
            # So, let's try to convert it to datetime:
            if (((DATASET[column_with_predict_var_x]).dtype == 'O') | ((DATASET[column_with_predict_var_x]).dtype == 'object')):
                  
                try:
                    DATASET[column_with_predict_var_x] = (DATASET[column_with_predict_var_x]).astype('datetime64[ns]')
                    print("Variable X successfully converted to datetime64[ns].\n")
                    
                except:
                    # Simply ignore it
                    pass
            
            # Get a series of unique values of the labels, and save it as a list using the
            # list attribute:
            unique_labels = list(DATASET[column_with_labels].unique())
            print(f"{len(unique_labels)} different labels detected: {unique_labels}.\n")
            
            # Start a list to store the dictionaries containing the keys:
            # 'x': list of predict variables; 'y': list of responses; 'lab': the label (group)
            list_of_dictionaries_with_series_to_analyze = []
            
            # Loop through each possible label:
            for lab in unique_labels:
                # loop through each element from the list unique_labels, referred as lab
                
                # Set a filter for the dataset, to select only rows correspondent to that
                # label:
                boolean_filter = (DATASET[column_with_labels] == lab)
                
                # Create a copy of the dataset, with entries selected by that filter:
                ds_copy = (DATASET[boolean_filter]).copy(deep = True)
                # Sort again by X and Y, to guarantee the results are in order:
                ds_copy = ds_copy.sort_values(by = [column_with_predict_var_x, column_with_response_var_y], ascending = [True, True])
                # Restart the index of the copy:
                ds_copy = ds_copy.reset_index(drop = True)
                
                # Re-extract the X and Y series and convert them to NumPy arrays 
                # (these arrays will be important later in the function):
                x = np.array(ds_copy[column_with_predict_var_x])
                y = np.array(ds_copy[column_with_response_var_y])
            
                # Then, create the dictionary:
                dict_of_values = {'x': x, 'y': y, 'lab': lab}
                
                # Now, append dict_of_values to list_of_dictionaries_with_series_to_analyze:
                list_of_dictionaries_with_series_to_analyze.append(dict_of_values)
                
            # Now, we have a list of dictionaries with the same format of the input list.
            
    else:
        
        # The user input a list_of_dictionaries_with_series_to_analyze
        # Create a support list:
        support_list = []
        
        # Loop through each element on the list list_of_dictionaries_with_series_to_analyze:
        
        for i in range (0, len(list_of_dictionaries_with_series_to_analyze)):
            # from i = 0 to i = len(list_of_dictionaries_with_series_to_analyze) - 1, index of the
            # last element from the list
            
            # pick the i-th dictionary from the list:
            dictionary = list_of_dictionaries_with_series_to_analyze[i]
            
            # access 'x', 'y', and 'lab' keys from the dictionary:
            x = dictionary['x']
            y = dictionary['y']
            lab = dictionary['lab']
            # Remember that all this variables are series from a dataframe, so we can apply
            # the astype function:
            # https://www.askpython.com/python/built-in-methods/python-astype?msclkid=8f3de8afd0d411ec86a9c1a1e290f37c
            
            # check if at least x and y are not None:
            if ((x is not None) & (y is not None)):
                
                # If column_with_predict_var_x is an object, the user may be trying to pass a date as x. 
                # So, let's try to convert it to datetime:
                if ((x.dtype == 'O') | (x.dtype == 'object')):

                    try:
                        x = (x).astype('datetime64[ns]')
                        print(f"Variable X from {i}-th dictionary successfully converted to datetime64[ns].\n")

                    except:
                        # Simply ignore it
                        pass
                
                # Possibly, x and y are not ordered. Firstly, let's merge them into a temporary
                # dataframe to be able to order them together.
                # Use the 'list' attribute to guarantee that x and y were read as lists. These lists
                # are the values for a dictionary passed as argument for the constructor of the
                # temporary dataframe. When using the list attribute, we make the series independent
                # from its origin, even if it was created from a Pandas dataframe. Then, we have a
                # completely independent dataframe that may be manipulated and sorted, without worrying
                # that it may modify its origin:
                
                temp_df = pd.DataFrame(data = {'x': list(x), 'y': list(y)})
                # sort this dataframe by 'x' and 'y':
                temp_df = temp_df.sort_values(by = ['x', 'y'], ascending = [True, True])
                # restart index:
                temp_df = temp_df.reset_index(drop = True)
                
                # Re-extract the X and Y series and convert them to NumPy arrays 
                # (these arrays will be important later in the function):
                x = np.array(temp_df['x'])
                y = np.array(temp_df['y'])
                
                # check if lab is None:
                if (lab is None):
                    # input a default label.
                    # Use the str attribute to convert the integer to string, allowing it
                    # to be concatenated
                    lab = "X" + str(i) + "_x_" + "Y" + str(i)
                    
                # Then, create the dictionary:
                dict_of_values = {'x': x, 'y': y, 'lab': lab}
                
                # Now, append dict_of_values to support list:
                support_list.append(dict_of_values)
            
        # Now, support_list contains only the dictionaries with valid entries, as well
        # as labels for each collection of data. The values are independent from their origin,
        # and now they are ordered and in the same format of the data extracted directly from
        # the dataframe.
        # So, make the list_of_dictionaries_with_series_to_analyze the support_list itself:
        list_of_dictionaries_with_series_to_analyze = support_list
        print(f"{len(list_of_dictionaries_with_series_to_analyze)} valid series input.\n")

        
    # Now that both methods of input resulted in the same format of list, we can process both
    # with the same code.
    
    # Each dictionary in list_of_dictionaries_with_series_to_analyze represents a series to
    # plot. So, the total of series to plot is:
    total_of_series = len(list_of_dictionaries_with_series_to_analyze)
    
    if (total_of_series <= 0):
        
        print("No valid series to plot. Please, provide valid arguments.\n")
    
    else:
        
        # Continue to plotting and calculating the fitting.
        # Notice that we sorted the all the lists after they were separated and before
        # adding them to dictionaries. Also, the timestamps were converted to datetime64 variables
        # Now we finished the loop, list_of_dictionaries_with_series_to_analyze 
        # contains all series converted to NumPy arrays, with timestamps parsed as datetimes.
        # This list will be the object returned at the end of the function. Since it is an
        # JSON-formatted list, we can use the function json_obj_to_pandas_dataframe to convert
        # it to a Pandas dataframe.
        
        
        # Now, we can plot the figure.
        # we set alpha = 0.95 (opacity) to give a degree of transparency (5%), 
        # so that one series do not completely block the visualization of the other.
        
        # Let's retrieve the list of Matplotlib CSS colors:
        css4 = mcolors.CSS4_COLORS
        # css4 is a dictionary of colors: {'aliceblue': '#F0F8FF', 'antiquewhite': '#FAEBD7', ...}
        # Each key of this dictionary is a color name to be passed as argument color on the plot
        # function. So let's retrieve the array of keys, and use the list attribute to convert this
        # array to a list of colors:
        list_of_colors = list(css4.keys())
        
        # In 11 May 2022, this list of colors had 148 different elements
        # Since this list is in alphabetic order, let's create a random order for the colors.
        
        # Function random.sample(input_sequence, number_of_samples): 
        # this function creates a list containing a total of elements equals to the parameter 
        # "number_of_samples", which must be an integer.
        # This list is obtained by ramdomly selecting a total of "number_of_samples" elements from the
        # list "input_sequence" passed as parameter.
        
        # Function random.choices(input_sequence, k = number_of_samples):
        # similarly, randomly select k elements from the sequence input_sequence. This function is
        # newer than random.sample
        # Since we want to simply randomly sort the sequence, we can pass k = len(input_sequence)
        # to obtain the randomly sorted sequence:
        list_of_colors = random.choices(list_of_colors, k = len(list_of_colors))
        # Now, we have a random list of colors to use for plotting the charts
        
        if (add_splines_lines == True):
            LINE_STYLE = '-'

        else:
            LINE_STYLE = ''
        
        if (add_scatter_dots == True):
            MARKER = 'o'
            
        else:
            MARKER = ''
        
        # Matplotlib linestyle:
        # https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html?msclkid=68737f24d16011eca9e9c4b41313f1ad
        
        if (plot_title is None):
            # Set graphic title
            plot_title = f"Y_x_timestamp"

        if (horizontal_axis_title is None):
            # Set horizontal axis title
            horizontal_axis_title = "timestamp"

        if (vertical_axis_title is None):
            # Set vertical axis title
            vertical_axis_title = "Y"
        
        # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
        # so that the bars do not completely block other views.
        OPACITY = 0.95
        
        #Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
        fig = plt.figure(figsize = (12, 8))
        ax = fig.add_subplot()

        i = 0 # Restart counting for the loop of colors
        
        # Loop through each dictionary from list_of_dictionaries_with_series_and_predictions:
        for dictionary in list_of_dictionaries_with_series_to_analyze:
            
            # Try selecting a color from list_of_colors:
            try:
                
                COLOR = list_of_colors[i]
                # Go to the next element i, so that the next plot will use a different color:
                i = i + 1
            
            except IndexError:
                
                # This error will be raised if list index is out of range, 
                # i.e. if i >= len(list_of_colors) - we used all colors from the list (at least 148).
                # So, return the index to zero to restart the colors from the beginning:
                i = 0
                COLOR = list_of_colors[i]
                i = i + 1
            
            # Access the arrays and label from the dictionary:
            X = dictionary['x']
            Y = dictionary['y']
            LABEL = dictionary['lab']
            
            # Scatter plot:
            ax.plot(X, Y, linestyle = LINE_STYLE, marker = MARKER, color = COLOR, alpha = OPACITY, label = LABEL)
            # Axes.plot documentation:
            # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html?msclkid=42bc92c1d13511eca8634a2c93ab89b5
            
            # x and y are positional arguments: they are specified by their position in function
            # call, not by an argument name like 'marker'.
            
            # Matplotlib markers:
            # https://matplotlib.org/stable/api/markers_api.html?msclkid=36c5eec5d16011ec9583a5777dc39d1f
            
        # Now we finished plotting all of the series, we can set the general configuration:
        
        #ROTATE X AXIS IN XX DEGREES
        plt.xticks(rotation = x_axis_rotation)
        # XX = 0 DEGREES x_axis (Default)
        #ROTATE Y AXIS IN XX DEGREES:
        plt.yticks(rotation = y_axis_rotation)
        # XX = 0 DEGREES y_axis (Default)

        ax.set_title(plot_title)
        ax.set_xlabel(horizontal_axis_title)
        ax.set_ylabel(vertical_axis_title)

        ax.grid(grid) # show grid or not
        ax.legend(loc = 'upper left')
        # position options: 'upper right'; 'upper left'; 'lower left'; 'lower right';
        # 'right', 'center left'; 'center right'; 'lower center'; 'upper center', 'center'
        # https://www.statology.org/matplotlib-legend-position/

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
                file_name = "time_series_vis"

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


def histogram (df, column_to_analyze, normal_curve_overlay = True, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    
    # ideal bin interval calculated through Montgomery's method. 
    # Histogram is obtained from this calculated bin size.
    # Douglas C. Montgomery (2009). Introduction to Statistical Process Control, 
    # Sixth Edition, John Wiley & Sons.
    
    # column_to_analyze: string with the name of the column that will be analyzed.
    # column_to_analyze = 'col1' obtain a histogram from column 1.
    
    # Set a local copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    
    # Sort by the column to analyze (ascending order) and reset the index:
    DATASET = DATASET.sort_values(by = column_to_analyze, ascending = True)
    
    DATASET = DATASET.reset_index(drop = True)
    
    #Calculo do bin size - largura do histograma:
    #1: Encontrar o menor (lowest) e o maior (highest) valor dentro da tabela de dados)
    #2: Calcular rangehist = highest - lowest
    #3: Calcular quantidade de dados (samplesize) de entrada fornecidos
    #4: Calcular a quantidade de celulas da tabela de frequencias (ncells)
    #ncells = numero inteiro mais proximo da (raiz quadrada de samplesize)
    #5: Calcular binsize = (df[column_to_analyze])rangehist/(ncells)
    #ATENCAO: Nao se esquecer de converter range, ncells, samplesize e binsize para valores absolutos (modulos)
    #isso porque a largura do histograma tem que ser um numero positivo

    # General stats
    mu = (DATASET[column_to_analyze]).mean() 
    median = (DATASET[column_to_analyze]).median()
    sigma = (DATASET[column_to_analyze]).std() 

    # bin-size
    lowest = (DATASET[column_to_analyze]).min()
    highest = (DATASET[column_to_analyze]).max()
    sample_size = (DATASET[column_to_analyze]).count()
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
    
    if (n_cells <= 1):
        
        # Manually set to 5 cells:
        n_cells = 5
    
    #ncells = numero de linhas da tabela de frequencias
    bin_size = range_hist/n_cells  
    
    # 1st bin:
    
    inf_bin_lim = lowest
    sup_bin_lim = inf_bin_lim + bin_size
    bin_mean = (inf_bin_lim + sup_bin_lim)/2
    
    boolean_filter = ((DATASET[column_to_analyze] >= inf_bin_lim) & (DATASET[column_to_analyze] <= sup_bin_lim))
    # Use the filter to input the value bin_mean to the column named 'bin_center'
    # dataset.loc[dataset["CatVar"] == 'Value1', "EncodedColumn"] = 1
    DATASET.loc[boolean_filter, 'bin_center'] = bin_mean        
    
    while (highest > sup_bin_lim):
        
        # Update the limits:
        inf_bin_lim = sup_bin_lim
        sup_bin_lim = inf_bin_lim + bin_size
        bin_mean = (inf_bin_lim + sup_bin_lim)/2
        
        boolean_filter = ((DATASET[column_to_analyze] >= inf_bin_lim) & (DATASET[column_to_analyze] <= sup_bin_lim))
        
        # Use the filter to input the value bin_mean to the column named 'bin_center'
        # dataset.loc[dataset["CatVar"] == 'Value1', "EncodedColumn"] = 1
        DATASET.loc[boolean_filter, 'bin_center'] = bin_mean
    
    # Now, select only the columns column_to_analyze and 'bin_center':
    DATASET = DATASET[[column_to_analyze, 'bin_center']]
    
    # Group by bin_center in terms of counting:
    DATASET = DATASET.groupby(by = 'bin_center', as_index = False, sort = True)[column_to_analyze].count()
    
    # Rename the columns:
    DATASET.columns = ['bin_center', 'count']
    
    # Get a lists of bin_center and column_to_analyze:
    list_of_bins = list(DATASET['bin_center'])
    list_of_counts = list(DATASET['count'])
    
    # get the maximum count:
    max_count = DATASET['count'].max()
    # Get the index of the max count:
    max_count_index = list_of_counts.index(max_count)
    
    # Get the value bin_center correspondent to the max count (maximum probability):
    bin_of_max_proba = list_of_bins[max_count_index] 
    number_of_bins = len(DATASET) # Total of elements on the frequency table
    
    string_for_title = " - $\mu = %.2f$, $\sigma = %.2f$" %(mu, sigma)
    
    if not (plot_title is None):
        plot_title = plot_title + string_for_title
        #concatena a string do titulo a string com a media e desvio-padrao
        #%.2f: o numero entre %. e f indica a quantidade de casas decimais da 
        #variavel float f. No caso, arredondamos para 2 casas
        #NAO SE ESQUECA DO PONTO: ele que indicara que sera arredondado o 
        #numero de casas
    
    else:
        # Set graphic title
        plot_title = f"histogram_of_{column_to_analyze}" + string_for_title

    if (horizontal_axis_title is None):
        # Set horizontal axis title
        horizontal_axis_title = column_to_analyze

    if (vertical_axis_title is None):
        # Set vertical axis title
        vertical_axis_title = "Counting/Frequency"
        
    # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
    # so that the bars do not completely block other views.
    OPACITY = 0.95
    
    if (normal_curve_overlay == True):
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
    
    x_hist = DATASET['bin_center']
    y_hist = DATASET['count']
    
    # Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
    fig = plt.figure(figsize = (12, 8))
    ax = fig.add_subplot()
    
    #ROTATE X AXIS IN XX DEGREES
    plt.xticks(rotation = x_axis_rotation)
    # XX = 70 DEGREES x_axis (Default)
    #ROTATE Y AXIS IN XX DEGREES:
    plt.yticks(rotation = y_axis_rotation)
    # XX = 0 DEGREES y_axis (Default)
    
    #STANDARD MATPLOTLIB METHOD:
    #bins = number of bins (intervals) of the histogram. Adjust it manually
    #increasing bins will increase the histogram's resolution, but height of bars
    
    #ax.hist(y, bins=20, width = bar_width, label=xlabel, color='blue')
    #IF GRAPHIC IS NOT SHOWN: THAT IS BECAUSE THE DISTANCES BETWEEN VALUES ARE LOW, AND YOU WILL
    #HAVE TO USE THE STANDARD HISTOGRAM METHOD FROM MATPLOTLIB.
    #TO DO THAT, UNMARK LINE ABOVE: ax.hist(y, bins=20, width = bar_width, label=xlabel, color='blue')
    #AND MARK LINE BELOW AS COMMENT: ax.bar(xhist, yhist, width = bar_width, label=xlabel, color='blue')
    
    #IF YOU WANT TO CREATE GRAPHIC AS A BAR CHART BASED ON THE CALCULATED DISTRIBUTION TABLE, 
    #MARK THE LINE ABOVE AS COMMENT AND UNMARK LINE BELOW:
    ax.bar(x_hist, y_hist, alpha = OPACITY, label = f'counting_of\n{column_to_analyze}', color = 'darkblue')
    #ajuste manualmente a largura, width, para deixar as barras mais ou menos proximas
    
    if (normal_curve_overlay == True):
    
        # add normal curve
        ax.plot(x_of_normal, y_normal, color = 'red', linestyle = 'dashed', alpha = OPACITY, label = 'Adjusted\nnormal_curve')
    
    #ROTATE X AXIS IN XX DEGREES
    plt.xticks(rotation = x_axis_rotation)
    # XX = 0 DEGREES x_axis (Default)
    #ROTATE Y AXIS IN XX DEGREES:
    plt.yticks(rotation = y_axis_rotation)
    # XX = 0 DEGREES y_axis (Default)

    ax.set_title(plot_title)
    ax.set_xlabel(horizontal_axis_title)
    ax.set_ylabel(vertical_axis_title)

    ax.grid(grid) # show grid or not
    ax.legend(loc = 'upper right')
    # position options: 'upper right'; 'upper left'; 'lower left'; 'lower right';
    # 'right', 'center left'; 'center right'; 'lower center'; 'upper center', 'center'
    # https://www.statology.org/matplotlib-legend-position/

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
            file_name = "histogram"

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
      
    stats_dict = {
                  'statistics': ['mean', 'median', 'standard_deviation', f'lowest_{column_to_analyze}', 
                                f'highest_{column_to_analyze}', 'count_of_values', 'number_of_bins', 
                                 'bin_size', 'bin_of_max_proba', 'count_on_bin_of_max_proba'],
                  'value': [mu, median, sigma, lowest, highest, sample_size, number_of_bins,
                           bin_size, bin_of_max_proba, max_count]
                 }
    
    # Convert it to a Pandas dataframe setting the list 'statistics' as the index:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
    general_stats = pd.DataFrame(data = stats_dict)
    
    # Set the column 'statistics' as the index of the dataframe, using set_index method:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.set_index.html
    
    # If inplace = True, modifies the DataFrame in place (do not create a new object).
    # Then, we do not create an object equal to the expression. We simply apply the method (so,
    # None is returned from the method):
    general_stats.set_index(['statistics'], inplace = True)
    
    print("Check the general statistics from the analyzed variable:\n")
    print(general_stats)
    print("\n")
    print("Check the frequency table:\n")
    print(DATASET)

    return general_stats, DATASET


def histogram_alternative (df, column_to_analyze, total_of_bins, normal_curve_overlay = True, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    
    # column_to_analyze: string with the name of the column that will be analyzed.
    # column_to_analyze = 'col1' obtain a histogram from column 1.
    
    # Set a local copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    
    # Sort by the column to analyze (ascending order) and reset the index:
    DATASET = DATASET.sort_values(by = column_to_analyze, ascending = True)
    
    DATASET = DATASET.reset_index(drop = True)
    
    y_hist = DATASET[column_to_analyze]
    
    # General stats
    mu = (DATASET[column_to_analyze]).mean() 
    median = (DATASET[column_to_analyze]).median()
    sigma = (DATASET[column_to_analyze]).std() 

    # bin-size
    lowest = (DATASET[column_to_analyze]).min()
    highest = (DATASET[column_to_analyze]).max()
    sample_size = (DATASET[column_to_analyze]).count()
    
    # Retrieve the histogram array hist_array
    fig, ax = plt.subplots() # (0,0) not to show the plot now:
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
    
    string_for_title = " - $\mu = %.2f$, $\sigma = %.2f$" %(mu, sigma)
    
    if not (plot_title is None):
        plot_title = plot_title + string_for_title
        #concatena a string do titulo a string com a media e desvio-padrao
        #%.2f: o numero entre %. e f indica a quantidade de casas decimais da 
        #variavel float f. No caso, arredondamos para 2 casas
        #NAO SE ESQUECA DO PONTO: ele que indicara que sera arredondado o 
        #numero de casas
    
    else:
        # Set graphic title
        plot_title = f"histogram_of_{column_to_analyze}" + string_for_title

    if (horizontal_axis_title is None):
        # Set horizontal axis title
        horizontal_axis_title = column_to_analyze

    if (vertical_axis_title is None):
        # Set vertical axis title
        vertical_axis_title = "Counting/Frequency"
        
    # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
    # so that the bars do not completely block other views.
    OPACITY = 0.95
    
    if (normal_curve_overlay == True):
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
        
        center_of_bin_of_max_proba = (bin_of_max_proba + bin_after_the_max_proba)/2
        
        x = (center_of_bin_of_max_proba - (4 * sigma))
        x_of_normal = [x]
        
        while (x < (center_of_bin_of_max_proba + (4 * sigma))):
            
            x = x + (0.10)*(sigma)
            x_of_normal.append(x)
        
        # Convert the list to a NumPy array, so that it is possible to perform element-wise
        # (vectorial) operations:
        x_of_normal = np.array(x_of_normal)
        
        # Create an array of the normal curve y, applying the normal curve equation:
        # normal curve = 1/(sigma* ((2*pi)**(0.5))) * exp(-((x-mu)**2)/(2*(sigma**2)))
        # where pi = 3,14...., and exp is the exponential function (base e)
        # Let's center the normal curve on center_of_bin_of_max_proba
        y_normal = (1 / (sigma* (np.sqrt(2 * (np.pi))))) * (np.exp(-0.5 * (((1 / sigma) * (x_of_normal - center_of_bin_of_max_proba)) ** 2)))
        y_normal = np.array(y_normal)
        
        # Pick the maximum value obtained for y_normal:
        # https://numpy.org/doc/stable/reference/generated/numpy.amax.html#numpy.amax
        y_normal_max = np.amax(y_normal)
        
        # Let's get a correction factor, comparing the maximum of the histogram counting, max_count,
        # with y_normal_max:
        correction_factor = max_count/(y_normal_max)
        
        # Now, multiply each value of the array y_normal by the correction factor, to adjust the height:
        y_normal = y_normal * correction_factor
    
    # values needed for the standard matplotlib barchart:
    #x_hist = DATASET['bin_center']
    #y_hist = DATASET['count']
    
    # Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
    fig = plt.figure(figsize = (12, 8))
    ax = fig.add_subplot()
    
    #ROTATE X AXIS IN XX DEGREES
    plt.xticks(rotation = x_axis_rotation)
    # XX = 70 DEGREES x_axis (Default)
    #ROTATE Y AXIS IN XX DEGREES:
    plt.yticks(rotation = y_axis_rotation)
    # XX = 0 DEGREES y_axis (Default)
    
    #STANDARD MATPLOTLIB METHOD:
    #bins = number of bins (intervals) of the histogram. Adjust it manually
    #increasing bins will increase the histogram's resolution, but height of bars
    
    ax.hist(y_hist, bins = total_of_bins, alpha = OPACITY, label = f'counting_of\n{column_to_analyze}', color='darkblue')
    #ax.hist(y, bins=20, width = bar_width, label=xlabel, color='blue')
    #IF GRAPHIC IS NOT SHOWN: THAT IS BECAUSE THE DISTANCES BETWEEN VALUES ARE LOW, AND YOU WILL
    #HAVE TO USE THE STANDARD HISTOGRAM METHOD FROM MATPLOTLIB.
    #TO DO THAT, UNMARK LINE ABOVE: ax.hist(y, bins=20, width = bar_width, label=xlabel, color='blue')
    #AND MARK LINE BELOW AS COMMENT: ax.bar(xhist, yhist, width = bar_width, label=xlabel, color='blue')
    
    #IF YOU WANT TO CREATE GRAPHIC AS A BAR CHART BASED ON THE CALCULATED DISTRIBUTION TABLE, 
    #MARK THE LINE ABOVE AS COMMENT AND UNMARK LINE BELOW:
    #ax.bar(x_hist, y_hist, label = f'counting_of\n{column_to_analyze}', color = 'darkblue')
    #ajuste manualmente a largura, width, para deixar as barras mais ou menos proximas
    
    if (normal_curve_overlay == True):
    
        # add normal curve
        ax.plot(x_of_normal, y_normal, color = 'red', linestyle = 'dashed', alpha = OPACITY, label = 'Adjusted\nnormal_curve')
    
    #ROTATE X AXIS IN XX DEGREES
    plt.xticks(rotation = x_axis_rotation)
    # XX = 0 DEGREES x_axis (Default)
    #ROTATE Y AXIS IN XX DEGREES:
    plt.yticks(rotation = y_axis_rotation)
    # XX = 0 DEGREES y_axis (Default)

    ax.set_title(plot_title)
    ax.set_xlabel(horizontal_axis_title)
    ax.set_ylabel(vertical_axis_title)

    ax.grid(grid) # show grid or not
    ax.legend(loc = 'upper right')
    # position options: 'upper right'; 'upper left'; 'lower left'; 'lower right';
    # 'right', 'center left'; 'center right'; 'lower center'; 'upper center', 'center'
    # https://www.statology.org/matplotlib-legend-position/

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
            file_name = "histogram"

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
      
    stats_dict = {
                  'statistics': ['mean', 'median', 'standard_deviation', f'lowest_{column_to_analyze}', 
                                f'highest_{column_to_analyze}', 'count_of_values', 'number_of_bins', 
                                 'bin_size', 'bin_of_max_proba', 'count_on_bin_of_max_proba'],
                  'value': [mu, median, sigma, lowest, highest, sample_size, number_of_bins,
                           bin_size, bin_of_max_proba, max_count]
                 }
    
    # Convert it to a Pandas dataframe setting the list 'statistics' as the index:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
    general_stats = pd.DataFrame(data = stats_dict)
    
    # Set the column 'statistics' as the index of the dataframe, using set_index method:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.set_index.html
    
    # If inplace = True, modifies the DataFrame in place (do not create a new object).
    # Then, we do not create an object equal to the expression. We simply apply the method (so,
    # None is returned from the method):
    general_stats.set_index(['statistics'], inplace = True)
    
    print("Check the general statistics from the analyzed variable:\n")
    print(general_stats)
    print("\n")
    print("Check the frequency table:\n")
    print(DATASET)

    return general_stats, DATASET


def test_data_normality (df, column_to_analyze, column_with_labels_to_test_subgroups = None, alpha = 0.10, show_probability_plot = True, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from statsmodels.stats import diagnostic
    from scipy import stats
    # Check https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.probplot.html#scipy.stats.probplot
    # Check https://docs.scipy.org/doc/scipy/tutorial/stats.html
    # Check https://docs.scipy.org/doc/scipy-1.8.0/html-scipyorg/reference/generated/scipy.stats.normaltest.html
    
    # WARNING: The statistical tests require at least 20 samples
    
    # column_to_analyze: column (variable) of the dataset that will be tested. Declare as a string,
    # in quotes.
    # e.g. column_to_analyze = 'col1' will analyze a column named 'col1'.
    
    # column_with_labels_to_test_subgroups: if there is a column with labels or
    # subgroup indication, and the normality should be tested separately for each label, indicate
    # it here as a string (in quotes). e.g. column_with_labels_to_test_subgroups = 'col2' 
    # will retrieve the labels from 'col2'.
    # Keep column_with_labels_to_test_subgroups = None if a single series (the whole column)
    # will be tested.
    
    # Confidence level = 1 - ALPHA. For ALPHA = 0.10, we get a 0.90 = 90% confidence
    # Set ALPHA = 0.05 to get 0.95 = 95% confidence in the analysis.
    # Notice that, when less trust is needed, we can increase ALPHA to get less restrictive
    # results.
    
    print("WARNING: The statistical tests require at least 20 samples.\n")
    print("Interpretation:")
    print("p-value: probability that data is described by the normal distribution.")
    print("Criterion: the series is not described by normal if p < alpha = %.3f." %(alpha))
    
    # Set a local copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    
    # Start a list to store the different Pandas series to test:
    list_of_dicts = []
    
    if not (column_with_labels_to_test_subgroups is None):
        
        # 1. Get the unique values from column_with_labels_to_test_subgroups
        # and save it as the list labels_list:
        labels_list = list(DATASET[column_with_labels_to_test_subgroups].unique())
        
        # 2. Loop through each element from labels_list:
        for label in labels_list:
            
            # 3. Create a copy of the DATASET, filtering for entries where 
            # column_with_labels_to_test_subgroups == label:
            filtered_df = (DATASET[DATASET[column_with_labels_to_test_subgroups] == label]).copy(deep = True)
            # 4. Reset index of the copied dataframe:
            filtered_df = filtered_df.reset_index(drop = True)
            # 5. Create a dictionary, with an identification of the series, and the series
            # that will be tested:
            series_dict = {'series_id': (column_to_analyze + "_" + label), 
                           'series': filtered_df[column_to_analyze],
                           'total_elements_to_test': filtered_df[column_to_analyze].count()}
            
            # 6. Append this dictionary to the list of series:
            list_of_dicts.append(series_dict)
        
    else:
        # In this case, the only series is the column itself. So, let's create a dictionary with
        # same structure:
        series_dict = {'series_id': column_to_analyze, 'series': DATASET[column_to_analyze],
                       'total_elements_to_test': DATASET[column_to_analyze].count()}
        
        # Append this dictionary to the list of series:
        list_of_dicts.append(series_dict)
    
    
    # Now, loop through each element from the list of series:
    
    for series_dict in list_of_dicts:
        
        # start a support list:
        support_list = []
        
        # Check if there are at least 20 samples to test:
        series_id = series_dict['series_id']
        total_elements_to_test = series_dict['total_elements_to_test']
        
        if (total_elements_to_test < 20):
            
            print(f"Unable to test series {series_id}: at least 20 samples are needed, but found only {total_elements_to_test} entries for this series.\n")
            # Add a warning to the dictionary:
            series_dict['WARNING'] = "Series without the minimum number of elements (20) required to test the normality."
            # Append it to the support list:
            support_list.append(series_dict)
            
        else:
            # Let's test the series.
            y = series_dict['series']
            
            # Scipy.stats’ normality test
            # It is based on D’Agostino and Pearson’s test that combines 
            # skew and kurtosis to produce an omnibus test of normality.
            _, scipystats_test_pval = stats.normaltest(y)
            # The underscore indicates an output to be ignored, which is s^2 + k^2, 
            # where s is the z-score returned by skewtest and k is the z-score returned by kurtosistest.
            # https://docs.scipy.org/doc/scipy-1.8.0/html-scipyorg/reference/generated/scipy.stats.normaltest.html
            
            print("\n")
            print("D\'Agostino and Pearson\'s normality test (scipy.stats normality test):")
            print(f"p-value = {scipystats_test_pval} = {scipystats_test_pval*100}% of probability of being normal.")
            
            if (scipystats_test_pval < alpha):
                
                print("p = %.3f < %.3f" %(scipystats_test_pval, alpha))
                print(f"According to this test, data is not described by the normal distribution, for the {alpha*100}% confidence level defined.")
            
            else:
                
                print("p = %.3f >= %.3f" %(scipystats_test_pval, alpha))
                print(f"According to this test, data is described by the normal distribution, for the {alpha*100}% confidence level defined.")
            
            # add this test result to the dictionary:
            series_dict['dagostino_pearson_p_val'] = scipystats_test_pval
            series_dict['dagostino_pearson_p_in_pct'] = scipystats_test_pval*100
            
            # Scipy.stats’ Shapiro-Wilk test
            # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html
            shapiro_test = stats.shapiro(y)
            # returns ShapiroResult(statistic=0.9813305735588074, pvalue=0.16855233907699585)
             
            print("\n")
            print("Shapiro-Wilk normality test:")
            print(f"p-value = {shapiro_test[1]} = {(shapiro_test[1])*100}% of probability of being normal.")
            
            if (shapiro_test[1] < alpha):
                
                print("p = %.3f < %.3f" %(shapiro_test[1], alpha))
                print(f"According to this test, data is not described by the normal distribution, for the {alpha*100}% confidence level defined.")
            
            else:
                
                print("p = %.3f >= %.3f" %(shapiro_test[1], alpha))
                print(f"According to this test, data is described by the normal distribution, for the {alpha*100}% confidence level defined.")
            
            # add this test result to the dictionary:
            series_dict['shapiro_wilk_p_val'] = shapiro_test[1]
            series_dict['shapiro_wilk_p_in_pct'] = (shapiro_test[1])*100
            
            # Lilliefors’ normality test
            lilliefors_test = diagnostic.kstest_normal(y, dist = 'norm', pvalmethod = 'table')
            # Returns a tuple: index 0: ksstat: float
            # Kolmogorov-Smirnov test statistic with estimated mean and variance.
            # index 1: p-value:float
            # If the pvalue is lower than some threshold, e.g. 0.10, then we can reject the Null hypothesis that the sample comes from a normal distribution.
            
            print("\n")
            print("Lilliefors\'s normality test:")
            print(f"p-value = {lilliefors_test[1]} = {(lilliefors_test[1])*100}% of probability of being normal.")
            
            if (lilliefors_test[1] < alpha):
                
                print("p = %.3f < %.3f" %(lilliefors_test[1], alpha))
                print(f"According to this test, data is not described by the normal distribution, for the {alpha*100}% confidence level defined.")
            
            else:
                
                print("p = %.3f >= %.3f" %(lilliefors_test[1], alpha))
                print(f"According to this test, data is described by the normal distribution, for the {alpha*100}% confidence level defined.")
            
            # add this test result to the dictionary:
            series_dict['lilliefors_p_val'] = lilliefors_test[1]
            series_dict['lilliefors_p_in_pct'] = (lilliefors_test[1])*100
            
    
            # Anderson-Darling normality test
            ad_test = diagnostic.normal_ad(y, axis = 0)
            # Returns a tuple: index 0 - ad2: float
            # Anderson Darling test statistic.
            # index 1 - p-val: float
            # The p-value for hypothesis that the data comes from a normal distribution with unknown mean and variance.
            
            print("\n")
            print("Anderson-Darling (AD) normality test:")
            print(f"p-value = {ad_test[1]} = {(ad_test[1])*100}% of probability of being normal.")
            
            if (ad_test[1] < alpha):
                
                print("p = %.3f < %.3f" %(ad_test[1], alpha))
                print(f"According to this test, data is not described by the normal distribution, for the {alpha*100}% confidence level defined.")
            
            else:
                
                print("p = %.3f >= %.3f" %(ad_test[1], alpha))
                print(f"According to this test, data is described by the normal distribution, for the {alpha*100}% confidence level defined.")
            
            # add this test result to the dictionary:
            series_dict['anderson_darling_p_val'] = ad_test[1]
            series_dict['anderson_darling_p_in_pct'] = (ad_test[1])*100
            
            # Now, append the series dictionary to the support list:
            support_list.append(series_dict)
            
            # If the probability plot is supposed to be shown, plot it:
            
            if (show_probability_plot == True):
                
                print("\n")
                #Obtain the probability plot  
                fig, ax = plt.subplots(figsize = (12, 8))

                ax.set_title(f"probability_plot_of_{series_id}_for_normal_distribution")

                #ROTATE X AXIS IN XX DEGREES
                plt.xticks(rotation = x_axis_rotation)
                # XX = 70 DEGREES x_axis (Default)
                #ROTATE Y AXIS IN XX DEGREES:
                plt.yticks(rotation = y_axis_rotation)
                # XX = 0 DEGREES y_axis (Default)   

                plot_results = stats.probplot(y, dist = 'norm', fit = True, plot = ax)
                #This function resturns a tuple, so we must store it into res

                # Other distributions to check, see scipy Stats documentation. 
                # you could test dist=stats.loggamma, where stats was imported from scipy
                # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.probplot.html#scipy.stats.probplot

                ax.grid(grid)

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
                        file_name = "probability_plot_normal"

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
            
        
    # Now we left the for loop, make the list of dicts support list itself:
    list_of_dicts = support_list
    
    print("\n")
    print("Finished normality tests. Returning a list of dictionaries, where each dictionary contains the series analyzed and the p-values obtained.")
    print("Now, check general statistics of the data distribution:\n")
    
    # Now, let's obtain general statistics for all of the series, even those without the normality
    # test results.
    
    # start a support list:
    support_list = []
    
    for series_dict in list_of_dicts:
        
        # Calculate data skewness and kurtosis
    
        # Skewness
        data_skew = stats.skew(y)
        # skewness = 0 : normally distributed.
        # skewness > 0 : more weight in the left tail of the distribution.
        # skewness < 0 : more weight in the right tail of the distribution.
        # https://www.geeksforgeeks.org/scipy-stats-skew-python/

        # Kurtosis
        data_kurtosis = stats.kurtosis(y, fisher = True)
        # scipy.stats.kurtosis(array, axis=0, fisher=True, bias=True) function 
        # calculates the kurtosis (Fisher or Pearson) of a data set. It is the the fourth 
        # central moment divided by the square of the variance. 
        # It is a measure of the “tailedness” i.e. descriptor of shape of probability 
        # distribution of a real-valued random variable. 
        # In simple terms, one can say it is a measure of how heavy tail is compared 
        # to a normal distribution.
        # fisher parameter: fisher : Bool; Fisher’s definition is used (normal 0.0) if True; 
        # else Pearson’s definition is used (normal 3.0) if set to False.
        # https://www.geeksforgeeks.org/scipy-stats-kurtosis-function-python/
        print("A normal distribution should present no skewness (distribution distortion); and no kurtosis (long-tail).\n")
        print("For the data analyzed:\n")
        print(f"skewness = {data_skew}")
        print(f"kurtosis = {data_kurtosis}\n")

        if (data_skew < 0):

            print(f"Skewness = {data_skew} < 0: more weight in the left tail of the distribution.")

        elif (data_skew > 0):

            print(f"Skewness = {data_skew} > 0: more weight in the right tail of the distribution.")

        else:

            print(f"Skewness = {data_skew} = 0: no distortion of the distribution.")
                

        if (data_kurtosis == 0):

            print("Data kurtosis = 0. No long-tail effects detected.\n")

        else:

            print(f"The kurtosis different from zero indicates long-tail effects on the distribution.\n")

        #Calculate the mode of the distribution:
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mode.html
        data_mode = stats.mode(y, axis = None)[0][0]
        # returns an array of arrays. The first array is called mode=array and contains the mode.
        # Axis: Default is 0. If None, compute over the whole array.
        # we set axis = None to compute the general mode.

        #Create general statistics dictionary:
        general_statistics_dict = {

            "series_mean": y.mean(),
            "series_variance": y.var(),
            "series_standard_deviation": y.std(),
            "series_skewness": data_skew,
            "series_kurtosis": data_kurtosis,
            "series_mode": data_mode

        }
        
        # Add this dictionary to the series dictionary:
        series_dict['general_statistics'] = general_statistics_dict
        
        # Append the dictionary to support list:
        support_list.append(series_dict)
    
    # Now, make the list of dictionaries support_list itself:
    list_of_dicts = support_list

    return list_of_dicts


def test_stat_distribution (df, column_to_analyze, column_with_labels_to_test_subgroups = None, statistical_distribution_to_test = 'lognormal'):
    
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from statsmodels.stats import diagnostic
    from scipy import stats
    # Check https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.probplot.html#scipy.stats.probplot
    # Check https://docs.scipy.org/doc/scipy/tutorial/stats.html
    # Check https://docs.scipy.org/doc/scipy-1.8.0/html-scipyorg/reference/generated/scipy.stats.normaltest.html
    
    # column_to_analyze: column (variable) of the dataset that will be tested. Declare as a string,
    # in quotes.
    # e.g. column_to_analyze = 'col1' will analyze a column named 'col1'.
    
    # column_with_labels_to_test_subgroups: if there is a column with labels or
    # subgroup indication, and the normality should be tested separately for each label, indicate
    # it here as a string (in quotes). e.g. column_with_labels_to_test_subgroups = 'col2' 
    # will retrieve the labels from 'col2'.
    # Keep column_with_labels_to_test_subgroups = None if a single series (the whole column)
    # will be tested.
    
    # Attention: if you want to test a normal distribution, use the function 
    # test_data_normality. Function test_data_normality tests normality through 4 methods 
    # and compare them: D’Agostino and Pearson’s; Shapiro-Wilk; Lilliefors; 
    # and Anderson-Darling tests.
    # The calculus of the p-value from the Anderson-Darling statistic is available only 
    # for some distributions. The function specific for the normality calculates these 
    # probabilities of following the normal.
    # Here, the function is destined to test a variety of distributions, and so only the 
    # Anderson-Darling test is performed.
        
    # statistical_distribution: string (inside quotes) containing the tested statistical 
    # distribution.
    # Notice: if data Y follow a 'lognormal', log(Y) follow a normal
    # Poisson is a special case from 'gamma' distribution.
    ## There are 91 accepted statistical distributions:
    # 'alpha', 'anglit', 'arcsine', 'beta', 'beta_prime', 'bradford', 'burr', 'burr12', 
    # 'cauchy', 'chi', 'chi-squared', 'cosine', 'double_gamma', 
    # 'double_weibull', 'erlang', 'exponential', 'exponentiated_weibull', 'exponential_power',
    # 'fatigue_life_birnbaum-saunders', 'fisk_log_logistic', 'folded_cauchy', 'folded_normal',
    # 'F', 'gamma', 'generalized_logistic', 'generalized_pareto', 'generalized_exponential', 
    # 'generalized_extreme_value', 'generalized_gamma', 'generalized_half-logistic', 
    # 'generalized_inverse_gaussian', 'generalized_normal', 
    # 'gilbrat', 'gompertz_truncated_gumbel', 'gumbel', 'gumbel_left-skewed', 'half-cauchy', 
    # 'half-normal', 'half-logistic', 'hyperbolic_secant', 'gauss_hypergeometric', 
    # 'inverted_gamma', 'inverse_normal', 'inverted_weibull', 'johnson_SB', 'johnson_SU', 
    # 'KSone', 'KStwobign', 'laplace', 'left-skewed_levy', 
    # 'levy', 'logistic', 'log_laplace', 'log_gamma', 'lognormal', 'log-uniform', 'maxwell', 
    # 'mielke_Beta-Kappa', 'nakagami', 'noncentral_chi-squared', 'noncentral_F', 
    # 'noncentral_t', 'normal', 'normal_inverse_gaussian', 'pareto', 'lomax', 
    # 'power_lognormal', 'power_normal', 'power-function', 'R', 'rayleigh', 'rice', 
    # 'reciprocal_inverse_gaussian', 'semicircular', 'student-t', 
    # 'triangular', 'truncated_exponential', 'truncated_normal', 'tukey-lambda',
    # 'uniform', 'von_mises', 'wald', 'weibull_maximum_extreme_value', 
    # 'weibull_minimum_extreme_value', 'wrapped_cauchy'
    
    print("WARNING: The statistical tests require at least 20 samples.\n")
    print("Attention: if you want to test a normal distribution, use the function test_data_normality.")
    print("Function test_data_normality tests normality through 4 methods and compare them: D’Agostino and Pearson’s; Shapiro-Wilk; Lilliefors; and Anderson-Darling tests.")
    print("The calculus of the p-value from the Anderson-Darling statistic is available only for some distributions.")
    print("The function which specifically tests the normality calculates these probabilities that data follows the normal.")
    print("Here, the function is destined to test a variety of distributions, and so only the Anderson-Darling test is performed.\n")
    
    print("If a compilation error is shown below, please update your Scipy version. Declare and run the following code into a separate cell:")
    print("! pip install scipy --upgrade\n")
    
    # Lets define the statistic distributions:
    # This are the callable Scipy objects which can be tested through Anderson-Darling test:
    # They are listed and explained in: 
    # https://docs.scipy.org/doc/scipy/tutorial/stats/continuous.html
    
    # This dictionary correlates the input name of the distribution to the correct scipy.stats
    # callable object
    # There are 91 possible statistical distributions:
    
    callable_statistical_distributions_dict = {
        
        'alpha': stats.alpha, 'anglit': stats.anglit, 'arcsine': stats.arcsine,
        'beta': stats.beta, 'beta_prime': stats.betaprime, 'bradford': stats.bradford,
        'burr': stats.burr, 'burr12': stats.burr12, 'cauchy': stats.cauchy,
        'chi': stats.chi, 'chi-squared': stats.chi2,
        'cosine': stats.cosine, 'double_gamma': stats.dgamma, 'double_weibull': stats.dweibull,
        'erlang': stats.erlang, 'exponential': stats.expon, 'exponentiated_weibull': stats.exponweib,
        'exponential_power': stats.exponpow, 'fatigue_life_birnbaum-saunders': stats.fatiguelife,
        'fisk_log_logistic': stats.fisk, 'folded_cauchy': stats.foldcauchy,
        'folded_normal': stats.foldnorm, 'F': stats.f, 'gamma': stats.gamma,
        'generalized_logistic': stats.genlogistic, 'generalized_pareto': stats.genpareto,
        'generalized_exponential': stats.genexpon, 'generalized_extreme_value': stats.genextreme,
        'generalized_gamma': stats.gengamma, 'generalized_half-logistic': stats.genhalflogistic,
        'generalized_inverse_gaussian': stats.geninvgauss,
        'generalized_normal': stats.gennorm, 'gilbrat': stats.gilbrat,
        'gompertz_truncated_gumbel': stats.gompertz, 'gumbel': stats.gumbel_r,
        'gumbel_left-skewed': stats.gumbel_l, 'half-cauchy': stats.halfcauchy, 'half-normal': stats.halfnorm,
        'half-logistic': stats.halflogistic, 'hyperbolic_secant': stats.hypsecant,
        'gauss_hypergeometric': stats.gausshyper, 'inverted_gamma': stats.invgamma,
        'inverse_normal': stats.invgauss, 'inverted_weibull': stats.invweibull,
        'johnson_SB': stats.johnsonsb, 'johnson_SU': stats.johnsonsu, 'KSone': stats.ksone,
        'KStwobign': stats.kstwobign, 'laplace': stats.laplace,
        'left-skewed_levy': stats.levy_l,
        'levy': stats.levy, 'logistic': stats.logistic, 'log_laplace': stats.loglaplace,
        'log_gamma': stats.loggamma, 'lognormal': stats.lognorm, 'log-uniform': stats.loguniform,
        'maxwell': stats.maxwell, 'mielke_Beta-Kappa': stats.mielke, 'nakagami': stats.nakagami,
        'noncentral_chi-squared': stats.ncx2, 'noncentral_F': stats.ncf, 'noncentral_t': stats.nct,
        'normal': stats.norm, 'normal_inverse_gaussian': stats.norminvgauss, 'pareto': stats.pareto,
        'lomax': stats.lomax, 'power_lognormal': stats.powerlognorm, 'power_normal': stats.powernorm,
        'power-function': stats.powerlaw, 'R': stats.rdist, 'rayleigh': stats.rayleigh,
        'rice': stats.rayleigh, 'reciprocal_inverse_gaussian': stats.recipinvgauss,
        'semicircular': stats.semicircular,
        'student-t': stats.t, 'triangular': stats.triang,
        'truncated_exponential': stats.truncexpon, 'truncated_normal': stats.truncnorm,
        'tukey-lambda': stats.tukeylambda, 'uniform': stats.uniform, 'von_mises': stats.vonmises,
        'wald': stats.wald, 'weibull_maximum_extreme_value': stats.weibull_max,
        'weibull_minimum_extreme_value': stats.weibull_min, 'wrapped_cauchy': stats.wrapcauchy
                
    }
    
    # Get a list of keys from this dictionary, to compare with the selected string:
    list_of_dictionary_keys = callable_statistical_distributions_dict.keys()
    
    #check if an invalid string was provided using the in method:
    # The string must be in the list of dictionary keys
    boolean_filter = statistical_distribution_to_test in list_of_dictionary_keys
    # if it is the list, boolean_filter == True. If it is not, boolean_filter == False
    
    if (boolean_filter == False):
        
        print(f"Please, select a valid statistical distribution to test: {list_of_dictionary_keys}")
        return "error"
    
    # Set a local copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    
    # Start a list to store the different Pandas series to test:
    list_of_dicts = []
    
    if not (column_with_labels_to_test_subgroups is None):
        
        # 1. Get the unique values from column_with_labels_to_test_subgroups
        # and save it as the list labels_list:
        labels_list = list(DATASET[column_with_labels_to_test_subgroups].unique())
        
        # 2. Loop through each element from labels_list:
        for label in labels_list:
            
            # 3. Create a copy of the DATASET, filtering for entries where 
            # column_with_labels_to_test_subgroups == label:
            filtered_df = (DATASET[DATASET[column_with_labels_to_test_subgroups] == label]).copy(deep = True)
            # 4. Reset index of the copied dataframe:
            filtered_df = filtered_df.reset_index(drop = True)
            # 5. Create a dictionary, with an identification of the series, and the series
            # that will be tested:
            series_dict = {'series_id': (column_to_analyze + "_" + label), 
                           'series': filtered_df[column_to_analyze],
                           'total_elements_to_test': filtered_df[column_to_analyze].count()}
            
            # 6. Append this dictionary to the list of series:
            list_of_dicts.append(series_dict)
        
    else:
        # In this case, the only series is the column itself. So, let's create a dictionary with
        # same structure:
        series_dict = {'series_id': column_to_analyze, 'series': DATASET[column_to_analyze],
                       'total_elements_to_test': DATASET[column_to_analyze].count()}
        
        # Append this dictionary to the list of series:
        list_of_dicts.append(series_dict)
    
    
    # Now, loop through each element from the list of series:
    
    for series_dict in list_of_dicts:
        
        # start a support list:
        support_list = []
        
        # Check if there are at least 20 samples to test:
        series_id = series_dict['series_id']
        total_elements_to_test = series_dict['total_elements_to_test']
        
        if (total_elements_to_test < 20):
            
            print(f"Unable to test series {series_id}: at least 20 samples are needed, but found only {total_elements_to_test} entries for this series.\n")
            # Add a warning to the dictionary:
            series_dict['WARNING'] = "Series without the minimum number of elements (20) required to test the normality."
            # Append it to the support list:
            support_list.append(series_dict)
            
        else:
            # Let's test the series.
            y = series_dict['series']
            
            # Calculate data skewness and kurtosis
            # Skewness
            data_skew = stats.skew(y)
            # skewness = 0 : normally distributed.
            # skewness > 0 : more weight in the left tail of the distribution.
            # skewness < 0 : more weight in the right tail of the distribution.
            # https://www.geeksforgeeks.org/scipy-stats-skew-python/

            # Kurtosis
            data_kurtosis = stats.kurtosis(y, fisher = True)
            # scipy.stats.kurtosis(array, axis=0, fisher=True, bias=True) function 
            # calculates the kurtosis (Fisher or Pearson) of a data set. It is the the fourth 
            # central moment divided by the square of the variance. 
            # It is a measure of the “tailedness” i.e. descriptor of shape of probability 
            # distribution of a real-valued random variable. 
            # In simple terms, one can say it is a measure of how heavy tail is compared 
            # to a normal distribution.
            # fisher parameter: fisher : Bool; Fisher’s definition is used (normal 0.0) if True; 
            # else Pearson’s definition is used (normal 3.0) if set to False.
            # https://www.geeksforgeeks.org/scipy-stats-kurtosis-function-python/
            print("A normal distribution should present no skewness (distribution distortion); and no kurtosis (long-tail).\n")
            print("For the data analyzed:\n")
            print(f"skewness = {data_skew}")
            print(f"kurtosis = {data_kurtosis}\n")

            if (data_skew < 0):

                print(f"Skewness = {data_skew} < 0: more weight in the left tail of the distribution.")

            elif (data_skew > 0):

                print(f"Skewness = {data_skew} > 0: more weight in the right tail of the distribution.")

            else:

                print(f"Skewness = {data_skew} = 0: no distortion of the distribution.")
                

            if (data_kurtosis == 0):

                print("Data kurtosis = 0. No long-tail effects detected.\n")

            else:

                print(f"The kurtosis different from zero indicates long-tail effects on the distribution.\n")

            #Calculate the mode of the distribution:
            # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mode.html
            data_mode = stats.mode(y, axis = None)[0][0]
            # returns an array of arrays. The first array is called mode=array and contains the mode.
            # Axis: Default is 0. If None, compute over the whole array.
            # we set axis = None to compute the general mode.
            
            # Access the object correspondent to the distribution provided. To do so,
            # simply access dict['key1'], where 'key1' is a key from a dictionary dict ={"key1": 'val1'}
            # Access just as accessing a column from a dataframe.

            anderson_darling_statistic = diagnostic.anderson_statistic(y, dist = (callable_statistical_distributions_dict[statistical_distribution_to_test]), fit = True)
            
            print(f"Anderson-Darling statistic for the distribution {statistical_distribution_to_test} = {anderson_darling_statistic}\n")
            print("The Anderson–Darling test assesses whether a sample comes from a specified distribution.")
            print("It makes use of the fact that, when given a hypothesized underlying distribution and assuming the data does arise from this distribution, the cumulative distribution function (CDF) of the data can be assumed to follow a uniform distribution.")
            print("Then, data can be tested for uniformity using an appropriate distance test (Shapiro 1980).\n")
            # source: https://en.wikipedia.org/wiki/Anderson%E2%80%93Darling_test

            # Fit the distribution and get its parameters
            # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_continuous.fit.html

            distribution_parameters = callable_statistical_distributions_dict[statistical_distribution_to_test].fit(y)
            
            # With method="MLE" (default), the fit is computed by minimizing the negative 
            # log-likelihood function. A large, finite penalty (rather than infinite negative 
            # log-likelihood) is applied for observations beyond the support of the distribution. 
            # With method="MM", the fit is computed by minimizing the L2 norm of the relative errors 
            # between the first k raw (about zero) data moments and the corresponding distribution 
            # moments, where k is the number of non-fixed parameters. 

            # distribution_parameters: Estimates for any shape parameters (if applicable), 
            # followed by those for location and scale.
            print(f"Distribution shape parameters calculated for {statistical_distribution_to_test} = {distribution_parameters}\n")
            
            print("ATTENTION:\n")
            print("The critical values for the Anderson-Darling test are dependent on the specific distribution that is being tested.")
            print("Tabulated values and formulas have been published (Stephens, 1974, 1976, 1977, 1979) for a few specific distributions: normal, lognormal, exponential, Weibull, logistic, extreme value type 1.")
            print("The test consists on an one-sided test of the hypothesis that the distribution is of a specific form.")
            print("The hypothesis is rejected if the test statistic, A, is greater than the critical value for that particular distribution.")
            print("Note that, for a given distribution, the Anderson-Darling statistic may be multiplied by a constant which usually depends on the sample size, n).")
            print("These constants are given in the various papers by Stephens, and may be simply referred as the \'adjusted Anderson-Darling statistic\'.")
            print("This adjusted statistic is what should be compared against the critical values.")
            print("Also, be aware that different constants (and therefore critical values) have been published.")
            print("Therefore, you just need to be aware of what constant was used for a given set of critical values (the needed constant is typically given with the correspondent critical values).")
            print("To learn more about the Anderson-Darling statistics and the check the full references of Stephens, go to the webpage from the National Institute of Standards and Technology (NIST):\n")
            print("https://itl.nist.gov/div898/handbook/eda/section3/eda3e.htm")
            print("\n")
            
            #Create general statistics dictionary:
            general_statistics_dict = {

                "series_mean": y.mean(),
                "series_variance": y.var(),
                "series_standard_deviation": y.std(),
                "series_skewness": data_skew,
                "series_kurtosis": data_kurtosis,
                "series_mode": data_mode,
                "AndersonDarling_statistic_A": anderson_darling_statistic,
                "distribution_parameters": distribution_parameters

            }

            # Add this dictionary to the series dictionary:
            series_dict['general_statistics'] = general_statistics_dict
 
            # Now, append the series dictionary to the support list:
            support_list.append(series_dict)
        
    # Now we left the for loop, make the list of dicts support list itself:
    list_of_dicts = support_list
    
    print("General statistics successfully returned in the list \'list_of_dicts\'.\n")
    print(list_of_dicts)
    print("\n")
    
    print("Note: the obtention of the probability plot specific for each distribution requires shape parameters.")
    print("Check Scipy documentation for additional information:")
    print("https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.probplot.html")
    
    return list_of_dicts


def col_filter_rename (df, cols_list, mode = 'filter'):
    
    import pandas as pd
    
    # mode = 'filter' for filtering only the list of columns passed as cols_list;
    # mode = 'rename' for renaming the columns with the names passed as cols_list.
    
    # cols_list = list of strings containing the names (headers) of the columns to select
    # (filter); or to be set as the new columns' names, according to the selected mode.
    # For instance: cols_list = ['col1', 'col2', 'col3'] will 
    # select columns 'col1', 'col2', and 'col3' (or rename the columns with these names). 
    # Declare the names inside quotes.
    
    # Set a local copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    
    print(f"Original columns in the dataframe:\n{DATASET.columns}")
    
    if (mode == 'filter'):
        
        #filter the dataframe so that it will contain only the cols_list.
        DATASET = DATASET[cols_list]
        print("Dataframe filtered according to the list provided.")
        print("Check the new dataframe:\n")
        print(DATASET)
        
    elif (mode == 'rename'):
        
        # Check if the number of columns of the dataset is equal to the number of elements
        # of the new list. It will avoid raising an exception error.
        boolean_filter = (len(cols_list) == len(DATASET.columns))
        
        if (boolean_filter == False):
            #Impossible to rename, number of elements are different.
            print("The number of columns of the dataframe is different from the number of elements of the list. Please, provide a list with number of elements equals to the number of columns.")
        
        else:
            #Same number of elements, so that we can update the columns' names.
            DATASET.columns = cols_list
            print("Dataframe columns renamed according to the list provided.")
            print("Warning: the substitution is element-wise: the first element of the list is now the name of the first column, and so on, ..., so that the last element is the name of the last column.")
            print("Check the new dataframe:\n")
            print(DATASET)
        
    else:
        print("Enter a valid mode: \'filter\' or \'rename\'.")
    
    return DATASET


def log_transform (df, subset = None, create_new_columns = True, new_columns_suffix = "_log"):
    
    import numpy as np
    import pandas as pd
    
    #### WARNING: This function will eliminate rows where the selected variables present 
    #### values lower or equal to zero (condition for the logarithm to be applied).
    
    # subset = None
    # Set subset = None to transform the whole dataset. Alternatively, pass a list with 
    # columns names for the transformation to be applied. For instance:
    # subset = ['col1', 'col2', 'col3'] will apply the transformation to the columns named
    # as 'col1', 'col2', and 'col3'. Declare the names inside quotes.
    # Declaring the full list of columns is equivalent to setting subset = None.
    
    # create_new_columns = True
    # Alternatively, set create_new_columns = True to store the transformed data into new
    # columns. Or set create_new_columns = False to overwrite the existing columns
    
    #new_columns_suffix = "_log"
    # This value has effect only if create_new_column = True.
    # The new column name will be set as column + new_columns_suffix. Then, if the original
    # column was "column1" and the suffix is "_log", the new column will be named as
    # "collumn1_log".
    # Alternatively, input inside quotes a string with the desired suffix. Recommendation:
    # start the suffix with "_" to separate it from the original name.
    
    
    # Start a local copy of the dataframe:
    DATASET = df.copy(deep = True)
    
    # Check if a subset was defined. If so, make columns_list = subset 
    if not (subset is None):
        
        columns_list = subset
    
    else:
        #There is no declared subset. Then, make columns_list equals to the list of
        # numeric columns of the dataframe.
        columns_list = list(DATASET.columns)
        
    # Let's check if there are categorical columns in columns_list. Only numerical
    # columns should remain
    # Start a support list:
    support_list = []
    
    # Loop through each column in columns_list:
    for column in columns_list:
        
        # Check the Pandas series (column) data type:
        column_type = DATASET[column].dtype
            
        # If it is not categorical (object), append it to the support list:
        if ((column_type != 'O') | (column_type != 'object')):
                
            support_list.append(column)
    
    # Finally, make the columns_list support_list itself:
    columns_list = support_list
    
    #Loop through each column to apply the transform:
    for column in columns_list:
        #access each element in the list column_list. The element is named 'column'.
        
        #boolean filter to check if the entry is higher than zero, condition for the log
        # to be applied
        boolean_filter = (DATASET[column] > 0)
        #This filter is equals True only for the rows where the column is higher than zero.
        
        #Apply the boolean filter to the dataframe, removing the entries where the column
        # cannot be log transformed.
        # The boolean_filter selects only the rows for which the filter values are True.
        DATASET = DATASET[boolean_filter]
        
        #Check if a new column will be created, or if the original column should be
        # substituted.
        if (create_new_columns == True):
            # Create a new column.
            
            # The new column name will be set as column + new_columns_suffix
            new_column_name = column + new_columns_suffix
        
        else:
            # Overwrite the existing column. Simply set new_column_name as the value 'column'
            new_column_name = column
        
        # Calculate the column value as the log transform of the original series (column)
        DATASET[new_column_name] = np.log(DATASET[column])
    
    # Reset the index:
    DATASET.reset_index(drop = True)
    
    print("The columns were successfully log-transformed. Check the 10 first rows of the new dataset:\n")
    print(DATASET.head(10))
    
    return DATASET

    # One curve derived from the normal is the log-normal.
    # If the values Y follow a log-normal distribution, their log follow a normal.
    # A log normal curve resembles a normal, but with skewness (distortion); 
    # and kurtosis (long-tail).

    # Applying the log is a methodology for normalizing the variables: 
    # the sample space gets shrinkled after the transformation, making the data more 
    # adequate for being processed by Machine Learning algorithms. Preferentially apply 
    # the transformation to the whole dataset, so that all variables will be of same order 
    # of magnitude.
    # Obviously, it is not necessary for variables ranging from -100 to 100 in numerical 
    # value, where most outputs from the log transformation are.


def reverse_log_transform (df, subset = None, create_new_columns = True, new_columns_suffix = "_originalScale"):
    
    import numpy as np
    import pandas as pd
    
    #### WARNING: This function will eliminate rows where the selected variables present 
    #### values lower or equal to zero (condition for the logarithm to be applied).
    
    # subset = None
    # Set subset = None to transform the whole dataset. Alternatively, pass a list with 
    # columns names for the transformation to be applied. For instance:
    # subset = ['col1', 'col2', 'col3'] will apply the transformation to the columns named
    # as 'col1', 'col2', and 'col3'. Declare the names inside quotes.
    # Declaring the full list of columns is equivalent to setting subset = None.
    
    # create_new_columns = True
    # Alternatively, set create_new_columns = True to store the transformed data into new
    # columns. Or set create_new_columns = False to overwrite the existing columns
    
    #new_columns_suffix = "_log"
    # This value has effect only if create_new_column = True.
    # The new column name will be set as column + new_columns_suffix. Then, if the original
    # column was "column1" and the suffix is "_originalScale", the new column will be named 
    # as "collumn1_originalScale".
    # Alternatively, input inside quotes a string with the desired suffix. Recommendation:
    # start the suffix with "_" to separate it from the original name.
    
    
    # Start a local copy of the dataframe:
    DATASET = df.copy(deep = True)
    
    # Check if a subset was defined. If so, make columns_list = subset 
    if not (subset is None):
        
        columns_list = subset
    
    else:
        #There is no declared subset. Then, make columns_list equals to the list of
        # numeric columns of the dataframe.
        columns_list = list(DATASET.columns)
        
    # Let's check if there are categorical columns in columns_list. Only numerical
    # columns should remain
    # Start a support list:
    support_list = []
    
    # Loop through each column in columns_list:
    for column in columns_list:
        
        # Check the Pandas series (column) data type:
        column_type = DATASET[column].dtype
            
        # If it is not categorical (object), append it to the support list:
        if ((column_type != 'O') | (column_type != 'object')):
                
            support_list.append(column)
    
    # Finally, make the columns_list support_list itself:
    columns_list = support_list
    
    #Loop through each column to apply the transform:
    for column in columns_list:
        #access each element in the list column_list. The element is named 'column'.
        
        # The exponential transformation can be applied to zero and negative values,
        # so we remove the boolean filter.
        
        #Check if a new column will be created, or if the original column should be
        # substituted.
        if (create_new_columns == True):
            # Create a new column.
            
            # The new column name will be set as column + new_columns_suffix
            new_column_name = column + new_columns_suffix
        
        else:
            # Overwrite the existing column. Simply set new_column_name as the value 'column'
            new_column_name = column
        
        # Calculate the column value as the log transform of the original series (column)
        DATASET[new_column_name] = np.exp(DATASET[column])
    
    print("The log_transform was successfully reversed through the exponential transformation. Check the 10 first rows of the new dataset:\n")
    print(DATASET.head(10))
    
    return DATASET


