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


def APPLY_ROW_FILTERS_LIST (df, list_of_row_filters):
    
    import numpy as np
    import pandas as pd
    
    print("Warning: this function filter the rows and results into a smaller dataset, since it removes the non-selected entries.")
    print("If you want to pass a filter to simply label the selected rows, use the function LABEL_DATAFRAME_SUBSETS, which do not eliminate entries from the dataframe.")
    
    # This function applies filters to the dataframe and remove the non-selected entries.
    
    # df: dataframe to be analyzed.
    
    ## define the filters and only them define the filters list
    # EXAMPLES OF BOOLEAN FILTERS TO COMPOSE THE LIST
    # boolean_filter1 = ((None) & (None)) 
    # (condition1 AND (&) condition2)
    # boolean_filter2 = ((None) | (None)) 
    # condition1 OR (|) condition2
    
    # boolean filters result into boolean values True or False.

    ## Examples of filters:
    ## filter1 = (condition 1) & (condition 2)
    ## filter1 = (df['column1'] > = 0) & (df['column2']) < 0)
    ## filter2 = (condition)
    ## filter2 = (df['column3'] <= 2.5)
    ## filter3 = (df['column4'] > 10.7)
    ## filter3 = (condition 1) | (condition 2)
    ## filter3 = (df['column5'] != 'string1') | (df['column5'] == 'string2')

    ## comparative operators: > (higher); >= (higher or equal); < (lower); 
    ## <= (lower or equal); == (equal); != (different)

    ## concatenation operators: & (and): the filter is True only if the 
    ## two conditions concatenated through & are True
    ## | (or): the filter is True if at least one of the two conditions concatenated
    ## through | are True.
    ## ~ (not): inverts the boolean, i.e., True becomes False, and False becomes True. 

    ## separate conditions with parentheses. Use parentheses to define a order
    ## of definition of the conditions:
    ## filter = ((condition1) & (condition2)) | (condition3)
    ## Here, firstly ((condition1) & (condition2)) = subfilter is evaluated. 
    ## Then, the resultant (subfilter) | (condition3) is evaluated.

    ## Pandas .isin method: you can also use this method to filter rows belonging to
    ## a given subset (the row that is in the subset is selected). The syntax is:
    ## is_black_or_brown = dogs["color"].isin(["Black", "Brown"])
    ## or: filter = (dataframe_column_series).isin([value1, value2, ...])
    # The negative of this condition may be acessed with ~ operator:
    ##  filter = ~(dataframe_column_series).isin([value1, value2, ...])
    ## Also, you may use isna() method as filter for missing values:
    ## filter = (dataframe_column_series).isna()
    ## or, for not missing: ~(dataframe_column_series).isna()
    
    # list_of_row_filters: list of boolean filters to be applied to the dataframe
    # e.g. list_of_row_filters = [filter1]
    # applies a single filter saved as filter 1. Notice: even if there is a single
    # boolean filter, it must be declared inside brackets, as a single-element list.
    # That is because the function will loop through the list of filters.
    # list_of_row_filters = [filter1, filter2, filter3, filter4]
    # will apply, in sequence, 4 filters: filter1, filter2, filter3, and filter4.
    # Notice that the filters must be declared in the order you want to apply them.
    
    
    # Set a local copy of the dataframe:
    DATASET = df.copy(deep = True)
    
    # Get the original index and convert it to a list
    original_index = list(DATASET.index)
    
    # Loop through the filters list, applying the filters sequentially:
    # Each element of the list is identified as 'boolean_filter'
    
    if (len(list_of_row_filters) > 0):
        
        # Start a list of indices that were removed. That is because we must
        # remove these elements from the boolean filter series before filtering, avoiding
        # the index mismatch.
        removed_indices = []
        
        # Now, loop through other rows in the list_of_row_filters:
        for boolean_series in list_of_row_filters:
            
            if (len(removed_indices) > 0):
                # Drop rows in list removed_indices. Set inplace = True to remove by simply applying
                # the method:
                # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop.html
                boolean_series.drop(labels = removed_indices, axis = 0, inplace = True)
            
            # Apply the filter:
            DATASET = DATASET[boolean_series]
            
            # Finally, let's update the list of removed indices:
            for index in original_index:
                if ((index not in list(DATASET.index)) & (index not in removed_indices)):
                    removed_indices.append(index)
    
    
    # Reset index:
    DATASET = DATASET.reset_index(drop = True)
    
    print("Successfully filtered the dataframe. Check the 10 first rows of the filtered and returned dataframe:\n")
    print(DATASET.head(10))
    
    return DATASET


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


def RECORD_LINKAGE (df_left, df_right, columns_to_block_as_basis_for_comparison = {'left_df_column': None, 'right_df_column': None}, columns_where_exact_matches_are_required = [{'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}], columns_where_similar_strings_should_be_found = [{'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}, {'left_df_column': None, 'right_df_column': None}], threshold_for_percent_of_similarity = 80.0):
    
    #WARNING: Only two dataframes can be merged on each call of the function.
    
    import numpy as np
    import pandas as pd
    import recordlinkage
    
    # Record linkage is the act of linking data from different sources regarding the same entity.
    # Generally, we clean two or more DataFrames, generate pairs of potentially matching records, 
    # score these pairs according to string similarity and other similarity metrics, and link them.
    # Example: we may want to merge data from different clients using the address as key, but there may
    # be differences on the format used for registering the addresses.
    
    # df_left: dataframe to be joined as the left one.
    
    # df_right: dataframe to be joined as the right one
    
    # columns_to_block_as_basis_for_comparison = {'left_df_column': None, 'right_df_column': None}
    # Dictionary of strings, in quotes. Do not change the keys. If a pair of columns should be
    # blocked for being used as basis for merging declare here: in 'left_df_column', input the name
    # of the column of the left dataframe. In right_df_column, input the name of the column on the right
    # dataframe.
    # We first want to generate pairs between both DataFrames. Ideally, we want to generate all
    # possible pairs between our DataFrames.
    # But, if we had big DataFrames, it is possible that we ende up having to generate millions, 
    # if not billions of pairs. It would not prove scalable and could seriously hamper development time.
    
    # This is where we apply what we call blocking, which creates pairs based on a matching column, 
    # reducing the number of possible pairs.
    
    # threshold_for_percent_of_similarity = 80.0 - 0.0% means no similarity and 100% means equal strings.
    # The threshold_for_percent_of_similarity is the minimum similarity calculated from the
    # Levenshtein (minimum edit) distance algorithm. This distance represents the minimum number of
    # insertion, substitution or deletion of characters operations that are needed for making two
    # strings equal.
    
    # columns_where_exact_matches_are_required = [{'left_df_column': None, 'right_df_column': None}]
    # columns_where_similar_strings_should_be_found = [{'left_df_column': None, 'right_df_column': None}]
    
    # Both of these arguments have the same structure. The single difference is that
    # columns_where_exact_matches_are_required is referent to a group of columns (or a single column)
    # where we require perfect correspondence between the dataframes, i.e., where no differences are
    # tolerated. Example: the month and day numbers must be precisely the same.
    # columns_where_similar_strings_should_be_found, in turns, is referent to the columns where there
    # is no rigid standard in the dataset, so similar values should be merged as long as the similarity
    # is equal or higher than threshold_for_percent_of_similarity.
    
    # Let's check the structure for these arguments, using columns_where_similar_strings_should_be_found
    # as example. All instructions are valid for columns_where_exact_matches_are_required.
    
    # columns_where_similar_strings_should_be_found =
    # [{'left_df_column': None, 'right_df_column': None}]
    # This is a list of dictionaries, where each dictionary contains two key-value pairs:
    # the first one contains the column name on the left dataframe; and the second one contains the 
    # correspondent column on the right dataframe.
    # The function will loop through all dictionaries in
    # this list, access the values of the key 'left_df_column' to retrieve a column to analyze in the left 
    # dataframe; and access access the key 'righ_df_column' to obtain the correspondent column in the right
    # dataframe. Then, it will look for potential matches.
    # For columns_where_exact_matches_are_required, only columns with perfect correspondence will be
    # retrieved. For columns_where_similar_strings_should_be_found, when the algorithm finds a correspondence
    # that satisfies the threshold criterium, it will assign it as a match. 
    # For instance, suppose you have a word written in too many ways, in a column named 'continent' that
    # should be used as key: "EU" , "eur" , "Europ" , "Europa" , "Erope" , "Evropa" ...
    # Since they have sufficient similarity, they will be assigned as matching.
    
    # The objects columns_where_similar_strings_should_be_found and
    # columns_where_exact_matches_are_required must be declared as lists, 
    # in brackets, even if there is a single dictionary.
    # Use always the same keys: 'left_df_column' and 'right_df_column'.
    # Notice that this function performs fuzzy matching, so it MAY SEARCH substrings and strings
    # written with different cases (upper or lower) when this portions or modifications make the
    # strings sufficiently similar to each other.
    
    # If you want, you can remove elements (dictionaries) from the list to declare fewer elements;
    # and you can also add more elements (dictionaries) to the lists, if you need to replace more
    # values.
    # Simply put a comma after the last element from the list and declare a new dictionary, keeping the
    # same keys: {'left_df_column': df_left_column, 'right_df_column': df_right_column}, 
    # where df_left_column and df_right_column represent the strings for searching and replacement 
    # (If the key contains None, the new dictionary will be ignored).
    
    
    print("Record linkage attempts to join data sources that have similarly fuzzy duplicate values.")
    print("The object is to end up with a final DataFrame with no duplicates by using string similarity.\n")
    
    # Create dataframe local copies to manipulate, avoiding that Pandas operates on
    # the original objects; or that Pandas tries to set values on slices or copies,
    # resulting in unpredictable results.
    # Use the copy method to effectively create a second object with the same properties
    # of the input parameters, but completely independent from it.
    DF_LEFT = df_left.copy(deep = True)
    DF_RIGHT = df_right.copy(deep = True)
    
    # If an invalid value was set for threshold_for_percent_of_similarity, correct it to 80% standard:
                
    if(threshold_for_percent_of_similarity is None):
        threshold_for_percent_of_similarity = 80.0
                
    if((threshold_for_percent_of_similarity == np.nan) | (threshold_for_percent_of_similarity < 0)):
        threshold_for_percent_of_similarity = 80.0
    
    # Convert the threshold for fraction (as required by recordlinkage) and save it as THRESHOLD:
    THRESHOLD = threshold_for_percent_of_similarity/100
    
    # Before finding the pairs, let's check if the column names on the lists of dictionaries are
    # the same. If they are not, let's rename the right dataframe columns so that they are equal to
    # the left one.
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html
    
    # Start a list of valid columns for exact matches:
    valid_columns_exact_matches = []
    
    for dictionary in columns_where_exact_matches_are_required:
        
        # Access elements on keys 'left_df_column' and 'right_df_column':
        left_df_column = dictionary['left_df_column']
        right_df_column = dictionary['right_df_column']
        
        # Check if no key is None:
        if ((left_df_column is not None) & (right_df_column is not None)):
            
            # If right_df_column is different from left_df_column, rename them to
            # make them equal:
            if (left_df_column != right_df_column):
                
                DF_RIGHT.rename(columns = {right_df_column: left_df_column}, inplace = True)
            
            # Add the column to the validated list:
            valid_columns_exact_matches.append(left_df_column)
    
    # Repeat the procedure for the other list:
    # Start a list of valid columns for similar strings:
    valid_columns_similar_str = []
    for dictionary in columns_where_similar_strings_should_be_found:
        
        # Access elements on keys 'left_df_column' and 'right_df_column':
        left_df_column = dictionary['left_df_column']
        right_df_column = dictionary['right_df_column']
        
        # Check if no key is None:
        if ((left_df_column is not None) & (right_df_column is not None)):
            
            # If right_df_column is different from left_df_column, rename them to
            # make them equal:
            if (left_df_column != right_df_column):
                
                DF_RIGHT.rename(columns = {right_df_column: left_df_column}, inplace = True)         
            
            # Add the column to the validated list:
            valid_columns_similar_str.append(left_df_column)
   
    # Now, we can create the objects for linkage:
    
    # Create an indexer object and find possible pairs:
    indexer = recordlinkage.Index()
    
    left_block = columns_to_block_as_basis_for_comparison['left_df_column']
    
    # Check if left_block is in one of the validated columns list. If it is, right_block
    # may have been renamed, and has the same label left_block:
    if ((left_block in valid_columns_exact_matches) | (left_block in valid_columns_similar_str)):
        
        right_block = left_block
    
    else:
        # right_block was not evaluated yet
        right_block = columns_to_block_as_basis_for_comparison['right_df_column']
    
    if ((left_block is not None) & (right_block is not None)):
        # If they are different, make them equal:
        if (left_block != right_block):
                
            DF_RIGHT.rename(columns = {right_block: left_block}, inplace = True)
        
        # block pairing in this column:
        indexer.block(left_block)
    
    elif (left_block is not None):
        # Try accessing this column on right dataframe:
        try:
            column_block = DF_RIGHT[left_block]
            # If no exception was raised, the column is actually present:
            indexer.block(left_block)
        except:
            pass
    
    elif (right_block is not None):
       # Try accessing this column on left dataframe:
        try:
            column_block = DF_LEFT[right_block]
            # If no exception was raised, the column is actually present:
            indexer.block(right_block)
        except:
            pass
    
    # Now that the columns were renaimed, we can generate the pairs from the object indexer:
    # Generate pairs
    pairs = indexer.index(DF_LEFT, DF_RIGHT)
    # The resulting object, is a pandas multi index object containing pairs of row indices from both 
    # DataFrames, i.e., it is an array containing possible pairs of indices that makes it much easier 
    # to subset DataFrames on.
    
    # Comparing the DataFrames
    # Since we've already generated our pairs, it's time to find potential matches. 
    # We first start by creating a comparison object using the recordlinkage dot compare function. 
    # This is similar to the indexing object we created while generating pairs, but this one is 
    # responsible for assigning different comparison procedures for pairs. 
    # Let's say there are columns for which we want exact matches between the pairs. To do that, 
    # we use the exact method. It takes in the column name in question for each DataFrame, 
    # and a label argument which lets us set the column name in the resulting DataFrame. 
    # Now in order to compute string similarities between pairs of rows for columns that have 
    # fuzzy values, we use the dot string method, which also takes in the column names in question, 
    # the similarity cutoff point in the threshold argument, which takes in a value between 0 and 1.
    # Finally to compute the matches, we use the compute function, which takes in the possible pairs, 
    # and the two DataFrames in question. Note that you need to always have the same order of DataFrames
    # when inserting them as arguments when generating pairs, comparing between columns, 
    # and computing comparisons.
    
    # Create a comparison object
    comp_cl = recordlinkage.Compare()
    
    # Create a counter for assessing the total number of valid columns being analyzed:
    column_counter = len(valid_columns_exact_matches) + len(valid_columns_similar_str)
    
    # Find exact matches for the columns in the list columns_where_exact_matches_are_required.
    # Loop through all elements from the list:
    
    for valid_column in valid_columns_exact_matches:
            
        # set column as the label for merged column:
        LABEL = valid_column
            
        # Find the exact matches:
        comp_cl.exact(valid_column, valid_column, label = LABEL)
 
    # Now, let's repeat the procedure for the columns where we will look for similar strings
    # for fuzzy matching. These columns were indicated in columns_where_similar_strings_should_be_found.
    # So, loop through all elements from this list:
    for valid_column in valid_columns_similar_str:
        
        # set column as the label for merged column:
        LABEL = valid_column
            
        # Find similar matches:
        comp_cl.string(valid_column, valid_column, label = LABEL, threshold = THRESHOLD) 

    # Now, compute the comparison of the pairs by using the .compute() method of comp_cl,
    # i.e, get potential matches:
    potential_matches = comp_cl.compute(pairs, DF_LEFT, DF_RIGHT)
    # potential_matches is a multi index DataFrame, where the first index is the row index from 
    # the first DataFrame (left), and the second index is a list of all row indices in the right dataframe. 
    # The columns are the columns being compared, with values being 1 for a match, and 0 for not a match.
    
    # The columns of our potential matches are the columns we chose to link both DataFrames on, 
    # where the value is 1 for a match, and 0 otherwise.
    # The first step in linking DataFrames, is to isolate the potentially matching pairs to the ones 
    # we're pretty sure of. We can do it by subsetting the rows where the row sum is above a certain 
    # number of columns: column_counter - 1 (i.e., where the match occurs for all columns, or do not
    # happen for a single column).
    # Isolate potential matches with row sum >=column_counter - 1
    matches = potential_matches[potential_matches.sum(axis = 1) >= (column_counter - 1)]
    
    # matches is row indices between DF_LEFT and DF_RIGHT that are most likely duplicates. 
    # Our next step is to extract the one of the index columns, and subsetting its associated 
    # DataFrame to filter for duplicates.
    
    # Get values of second column index of matches (i.e., indices for DF_RIGHT only).
    # We can access a DataFrame's index using the index attribute. Since this is a multi index 
    # DataFrame, it returns a multi index object containing pairs of row indices from DF_LEFT and 
    # DF_RIGHT respectively. We want to extract all DF_RIGHT indices, so we chain it with the 
    # get_level_values method, which takes in which column index we want to extract its values. 
    # We can either input the index column's name, or its order, which is in this case 1.
    matching_indices = matches.index.get_level_values(1)

    # Subset DF_RIGHT on non-duplicate values (i.e., removing the duplicates 
    # selected as matching_indices).
    # To find the duplicates in DF_RIGHTDF_RIGHT, we can simply subset on all indices of DF_RIGHT, 
    # with the ones found through record linkage. 
    # You can choose to examine them further for similarity with their duplicates in DF_LEFT, 
    # but if you're sure of your analysis, you can go ahead and find the non duplicates with 
    # the exact same line of code, except by adding a tilde at the beginning of your subset. 
    non_dup = DF_RIGHT[~DF_RIGHT.index.isin(matching_indices)]
    # ~ is the not (invert) operator: 
    # https://stackoverflow.com/questions/21415661/logical-operators-for-boolean-indexing-in-pandas
    
    # Append non_dup to DF_LEFT.
    # Now that you have your non duplicates, all you need is a simple append 
    # using the DataFrame append method of DF_LEFT, and you have your linked Data.
    merged_df = pd.concat([DF_LEFT, DF_RIGHT], axis = 0)
    
    # Now, reset index positions:
    merged_df = merged_df.reset_index(drop = True)
    
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


def df_general_characterization (df):
    
    import pandas as pd

    # Set a local copy of the dataframe:
    DATASET = df.copy(deep = True)

    # Show dataframe's header
    print("Dataframe\'s 10 first rows:\n")
    print(DATASET.head(10))

    # Show dataframe's tail:
    # Line break before next information:
    print("\n")
    print("Dataframe\'s 10 last rows:\n")
    print(DATASET.tail(10))
    
    # Show dataframe's shape:
    # Line break before next information:
    print("\n")
    df_shape  = DATASET.shape
    print("Dataframe\'s shape = (number of rows, number of columns) =\n")
    print(df_shape)
    
    # Show dataframe's columns:
    # Line break before next information:
    print("\n")
    df_columns_array = DATASET.columns
    print("Dataframe\'s columns =\n")
    print(df_columns_array)
    
    # Show dataframe's columns types:
    # Line break before next information:
    print("\n")
    df_dtypes = DATASET.dtypes
    # Now, the df_dtypes seroes has the original columns set as index, but this index has no name.
    # Let's rename it using the .rename method from Pandas Index object:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Index.rename.html#pandas.Index.rename
    # To access the Index object, we call the index attribute from Pandas dataframe.
    # By setting inplace = True, we modify the object inplace, by simply calling the method:
    df_dtypes.index.rename(name = 'dataframe_column', inplace = True)
    # Let's also modify the series label or name:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.rename.html
    df_dtypes.rename('dtype_series', inplace = True)
    print("Dataframe\'s variables types:\n")
    print(df_dtypes)
    
    # Show dataframe's general statistics for numerical variables:
    # Line break before next information:
    print("\n")
    df_general_statistics = DATASET.describe()
    print("Dataframe\'s general (summary) statistics for numeric variables:\n")
    print(df_general_statistics)
    
    # Show total of missing values for each variable:
    # Line break before next information:
    print("\n")
    total_of_missing_values_series = DATASET.isna().sum()
    # This is a series which uses the original column names as index
    proportion_of_missing_values_series = DATASET.isna().mean()
    percent_of_missing_values_series = proportion_of_missing_values_series * 100
    missingness_dict = {'count_of_missing_values': total_of_missing_values_series,
                       'proportion_of_missing_values': proportion_of_missing_values_series,
                       'percent_of_missing_values': percent_of_missing_values_series}
    
    df_missing_values = pd.DataFrame(data = missingness_dict)
    # Now, the dataframe has the original columns set as index, but this index has no name.
    # Let's rename it using the .rename method from Pandas Index object:
    df_missing_values.index.rename(name = 'dataframe_column', inplace = True)
    
    # Create a one row dataframe with the missingness for the whole dataframe:
    # Pass the scalars as single-element lists or arrays:
    one_row_data = {'dataframe_column': ['missingness_accross_rows'],
                    'count_of_missing_values': [len(DATASET) - len(DATASET.copy(deep = True).dropna(how = 'any'))],
                    'proportion_of_missing_values': [(len(DATASET) - len(DATASET.copy(deep = True).dropna(how = 'any')))/(len(DATASET))],
                    'percent_of_missing_values': [(len(DATASET) - len(DATASET.copy(deep = True).dropna(how = 'any')))/(len(DATASET))*100]
                    }
    one_row_df = pd.DataFrame(data = one_row_data)
    one_row_df.set_index('dataframe_column', inplace = True)
    
    # Append this one_row_df to df_missing_values:
    df_missing_values = pd.concat([df_missing_values, one_row_df])
    
    print("Missing values on each feature; and missingness considering all rows from the dataframe:")
    print("(note: \'missingness_accross_rows\' was calculated by: checking which rows have at least one missing value (NA); and then comparing total rows with NAs with total rows in the dataframe).\n")

    print(df_missing_values)
    
    return df_shape, df_columns_array, df_dtypes, df_general_statistics, df_missing_values


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

    if (list_of_categorical_columns is None):
        # Set it as an empty list (length = 0):
        list_of_categorical_columns = []
    
    elif (list_of_categorical_columns == np.nan):
        list_of_categorical_columns = []
    
    
    if (len(list_of_categorical_columns) > 0):
        
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
    
    if (len(list_of_categorical_columns) > 0):
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
    
    # set a local copy of the dataframe:
    DATASET = df.copy(deep = True)
    
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
    
    df_length = len(DATASET)
    print(f"Count of rows from the dataframe =\n")
    print(df_length)
    print("\n")

    # Show total of missing values for each variable:
    total_of_missing_values_series = DATASET.isna().sum()
    # This is a series which uses the original column names as index
    proportion_of_missing_values_series = DATASET.isna().mean()
    percent_of_missing_values_series = proportion_of_missing_values_series * 100
    missingness_dict = {'count_of_missing_values': total_of_missing_values_series,
                       'proportion_of_missing_values': proportion_of_missing_values_series,
                       'percent_of_missing_values': percent_of_missing_values_series}
    
    df_missing_values = pd.DataFrame(data = missingness_dict)
    # Now, the dataframe has the original columns set as index, but this index has no name.
    # Let's rename it using the .rename method from Pandas Index object:
    df_missing_values.index.rename(name = 'dataframe_column', inplace = True)
    
    # Create a one row dataframe with the missingness for the whole dataframe:
    # Pass the scalars as single-element lists or arrays:
    one_row_data = {'dataframe_column': ['missingness_accross_rows'],
                    'count_of_missing_values': [len(DATASET) - len(DATASET.copy(deep = True).dropna(how = 'any'))],
                    'proportion_of_missing_values': [(len(DATASET) - len(DATASET.copy(deep = True).dropna(how = 'any')))/(len(DATASET))],
                    'percent_of_missing_values': [(len(DATASET) - len(DATASET.copy(deep = True).dropna(how = 'any')))/(len(DATASET))*100]
                    }
    one_row_df = pd.DataFrame(data = one_row_data)
    one_row_df.set_index('dataframe_column', inplace = True)
    
    # Append this one_row_df to df_missing_values:
    df_missing_values = pd.concat([df_missing_values, one_row_df])
    
    print("Missing values on each feature; and missingness considering all rows from the dataframe:")
    print("(note: \'missingness_accross_rows\' was calculated by: checking which rows have at least one missing value (NA); and then comparing total rows with NAs with total rows in the dataframe).\n")

    print(df_missing_values)
    print("\n") # line_break
    
    print("Bar chart of the missing values - Nullity bar:\n")
    msno.bar(DATASET)
    plt.show()
    print("\n")
    print("The nullity bar allows us to visualize the completeness of the dataframe.\n")
    
    print("Nullity Matrix: distribution of missing values through the dataframe:\n")
    msno.matrix(DATASET)
    plt.show()
    print("\n")
    
    if not ((slice_time_window_from is None) | (slice_time_window_to is None)):
        
        # There is at least one of these two values for slicing:
        if not ((slice_time_window_from is None) & (slice_time_window_to is None)):
                # both are present
                
                if not (aggregate_time_in_terms_of is None):
                    print("Nullity matrix for the defined time window and for the selected aggregation frequency:\n")
                    msno.matrix(DATASET.loc[slice_time_window_from:slice_time_window_to], freq = frequency)
                    
                else:
                    # do not aggregate:
                    print("Nullity matrix for the defined time window:\n")
                    msno.matrix(DATASET.loc[slice_time_window_from:slice_time_window_to])
                
                plt.show()
                print("\n")
        
        elif not (slice_time_window_from is None):
            # slice only from the start. The condition where both limits were present was already
            # checked. To reach this condition, only one is not None
            # slice from 'slice_time_window_from' to the end of dataframe
            
                if not (aggregate_time_in_terms_of is None):
                    print("Nullity matrix for the defined time window and for the selected aggregation frequency:\n")
                    msno.matrix(DATASET.loc[slice_time_window_from:], freq = frequency)
                
                else:
                    # do not aggregate:
                    print("Nullity matrix for the defined time window:\n")
                    msno.matrix(DATASET.loc[slice_time_window_from:])
        
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
                    msno.matrix(DATASET.loc[:slice_time_window_to], freq = frequency)
                
                else:
                    # do not aggregate:
                    print("Nullity matrix for the defined time window:\n")
                    msno.matrix(DATASET.loc[:slice_time_window_to])
                
                plt.show()
                print("\n")
    
    else:
        # Both slice limits are not. Let's check if we have to aggregate the dataframe:
        if not (aggregate_time_in_terms_of is None):
                print("Nullity matrix for the selected aggregation frequency:\n")
                msno.matrix(DATASET, freq = frequency)
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
    msno.heatmap(DATASET)
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
    msno.dendrogram(DATASET)
    plt.show()
    print("\n")
    
    print("A dendrogram is a tree diagram that groups similar objects in close branches.")
    print("So, the missingness dendrogram is a tree diagram of missingness that describes correlation of variables by grouping similarly missing columns together.")
    print("To interpret this graph, read it from a top-down perspective.")
    print("Cluster leaves which are linked together at a distance of zero fully predict one another\'s presence.")
    print("In other words, when two variables are grouped together in the dendogram, one variable might always be empty while another is filled (the presence of one explains the missingness of the other), or they might always both be filled or both empty, and so on (the missingness of one explains the missigness of the other).\n")
    
    return df_missing_values


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
            ax2.plot(cum_pct, categories, '-ro', label = "cumulative\npercent")
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
            ax2.plot(cum_pct, categories, '-ro', label = "cumulative\npercent")
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
        
        else:
            
            # set a local copy of the dataframe:
            DATASET = df.copy(deep = True)
            
            if (column_with_labels is None):
            
                print("Using the whole series (column) for correlation.\n")
                column_with_labels = 'whole_series_' + column_with_response_var_y
                DATASET[column_with_labels] = column_with_labels
            
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
            
            x_is_datetime = False
            # boolean that will map if x is a datetime or not. Only change to True when it is.
            
            # Access keys 'x' and 'y' to retrieve the arrays.
            x = dictionary['x']
            y = dictionary['y']
            
            # Check if the elements from array x are np.datetime64 objects. Pick the first
            # element to check:
            
            if (type(x[0]) == np.datetime64):
                
                x_is_datetime = True
                
            if (x_is_datetime):
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
            if (x_is_datetime):
                y_pred_lin_reg = ((lin_reg).intercept) + ((lin_reg).slope) * (int_timescale)
            
            else:
                # x is not a timestamp, so we can directly apply it to the regression
                # equation:
                y_pred_lin_reg = ((lin_reg).intercept) + ((lin_reg).slope) * (x)
            
            # Add this array to the dictionary with the key 'y_pred_lin_reg':
            dictionary['y_pred_lin_reg'] = y_pred_lin_reg
            
            if (x_is_datetime):
            
                print("For performing the linear regression, a sequence of floats proportional to the timestamps was created. In this sequence, check on the returned object a dictionary containing the timestamps and the correspondent integers, that keeps the distance proportion between successive timestamps. The sequence was created by calculating the timedeltas as an integer number of nanoseconds, which were converted to seconds. The first timestamp was considered time = 0.")
                print("Notice that the regression equation is based on the use of this sequence of floats as X.\n")
                
                dictionary['warning'] = "x is a numeric scale that was obtained from datetimes, preserving the distance relationships. It was obtained for allowing the polynomial fitting."
                dictionary['numeric_to_datetime_correlation'] = {
                    
                    'x = 0': x[0],
                    f'x = {max(int_timescale)}': x[(len(x) - 1)]
                    
                }
                
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
                Y_PRED_LABEL = 'lin_reg_' + str(LABEL) # for the case where label is numeric
                
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


def polynomial_fit (data_in_same_column = False, df = None, column_with_predict_var_x = None, column_with_response_var_y = None, column_with_labels = None, list_of_dictionaries_with_series_to_analyze = [{'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}], polynomial_degree = 6, calculate_roots = False, calculate_derivative = False, calculate_integral = False, x_axis_rotation = 70, y_axis_rotation = 0, show_polynomial_reg = True, grid = True, add_splines_lines = False, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    import random
    # Python Random documentation:
    # https://docs.python.org/3/library/random.html?msclkid=9d0c34b2d13111ec9cfa8ddaee9f61a1
    import numpy as np
    from numpy.polynomial.polynomial import Polynomial
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    
    # Check numpy.polynomial class API documentation for other polynomials 
    # (chebyshev, legendre, hermite, etc):
    # https://numpy.org/doc/stable/reference/routines.polynomials.package.html#module-numpy.polynomial
    
    # df: the whole dataframe to be processed.
    
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
    
    # polynomial_degree = integer value representing the degree of the fitted polynomial.
    
    # calculate_derivative = False. Alternatively, set as True to calculate the derivative of the
    #  fitted polynomial and add it as a column of the dataframe.
    
    # calculate_integral = False. Alternatively, set as True to calculate the integral of the
    #  fitted polynomial and add it as a column of the dataframe.
    
    # calculate_roots = False.  Alternatively, set as True to calculate the roots of the
    #  fitted polynomial and return them as a NumPy array.
    
    if (data_in_same_column == True):
        
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
        
        else:
            
            # set a local copy of the dataframe:
            DATASET = df.copy(deep = True)
            
            if (column_with_labels is None):
            
                print("Using the whole series (column) for correlation.\n")
                column_with_labels = 'whole_series_' + column_with_response_var_y
                DATASET[column_with_labels] = column_with_labels
            
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
                        x_is_datetime = True
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
        
        print("No valid series to fit. Please, provide valid arguments.\n")
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
            
            x_is_datetime = False
            # boolean that will map if x is a datetime or not. Only change to True when it is.
            
            # Access keys 'x' and 'y' to retrieve the arrays.
            x = dictionary['x']
            y = dictionary['y']
            lab = dictionary['lab']
            
            # Check if the elements from array x are np.datetime64 objects. Pick the first
            # element to check:
            
            if (type(x[0]) == np.datetime64):
                
                x_is_datetime = True
            
            if (x_is_datetime):
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
                
                # Finally, use this timescale to obtain the polynomial fit;
                # Use the method .fit, passing X, Y, and degree as coefficients
                # to fit the polynomial to data:
                # Perform the least squares fit to data:
                #create an instance (object) named 'pol' from the class Polynomial:
                fitted_pol = Polynomial.fit(int_timescale, y, deg = polynomial_degree, full = False)
                
            
            else:
                # Obtain the polynomial fitting object directly from x. Since x is not a
                # datetime object, we can calculate the regression directly on it:
                fitted_pol = Polynomial.fit(x, y, deg = polynomial_degree, full = False)
   
            # when full = True, the [resid, rank, sv, rcond] list is returned
            # check: https://numpy.org/doc/stable/reference/generated/numpy.polynomial.polynomial.Polynomial.fit.html#numpy.polynomial.polynomial.Polynomial.fit

            # This method returned a series named 'fitted_pol', with the values of Y predicted by the
            # polynomial fitting. Now add it to the dictionary as fitted_polynomial_series:
            dictionary['fitted_polynomial'] = fitted_pol
            print(f"{polynomial_degree} degree polynomial successfully fitted to data using the least squares method. The fitting Y ({lab}) values were added to the dataframe as the column \'fitted_polynomial\'.")    
            
            # Get the polynomial coefficients array:
            if (x_is_datetime):
                coeff_array = Polynomial.fit(int_timescale, y, deg = polynomial_degree, full = False).coef
            
            else:
                coeff_array = Polynomial.fit(x, y, deg = polynomial_degree, full = False).coef
            
            # Create a coefficient dictionary:
            coeff_dict = {}
            # Loop through each element from the array, and append it to the dictionary:
            full_polynomial_format = "a0"
            
            for i in range(1, len(coeff_array)):
                
                    full_polynomial_format = full_polynomial_format + " + a" + str(i) + "*x" + str(i)
            
            coeff_dict['full_polynomial_format'] = full_polynomial_format
            
            for i in range(0, len(coeff_array)):
                
                # Create a key for the element i:
                dict_key = "a" + str(i)
                # Store the correspondent element on the array:
                coeff_dict[dict_key] = coeff_array[i]
            
            if (x_is_datetime):
                
                coeff_dict['warning'] = "x is a numeric scale that was obtained from datetimes, preserving the distance relationships. It was obtained for allowing the polynomial fitting."
                coeff_dict['numeric_to_datetime_correlation'] = {
                    
                    'x = 0': x[0],
                    f'x = {max(int_timescale)}': x[(len(x) - 1)]
                    
                }
                
                coeff_dict['sequence_of_floats_correspondent_to_timestamps'] = {
                                                                                'original_timestamps': x,
                                                                                'sequence_of_floats': int_timescale
                                                                                }
            
            print("Polynomial summary:\n")
            print(f"Polynomial format = {full_polynomial_format}\n")
            print("Polynomial coefficients:")
            
            for i in range(0, len(coeff_array)):
                print(f"{str('a') + str(i)} = {coeff_array[i]}")
            
            print(f"Fitted polynomial = {dictionary['fitted_polynomial']}")
            print("\n")
            
            if (x_is_datetime):
                print(coeff_dict['warning'])
                print(coeff_dict['numeric_to_datetime_correlation'])
                print("\n")
            
            # Add it to the main dictionary:
            dictionary['fitted_polynomial_coefficients'] = coeff_dict
            
            # Now, calculate the fitted series. Start a Pandas series as a copy from y:
            fitted_series = y.copy()
            # Make it zero:
            fitted_series = 0
            
            # Now loop through the polynomial coefficients: ai*(x**i):
            for i in range(0, len(coeff_array)):
                
                if (x_is_datetime):
                    
                    fitted_series = (coeff_array[i])*(int_timescale**(i))
                
                else:
                    fitted_series = (coeff_array[i])*(x**(i))
            
            # Add the series to the dictionary:
            dictionary['fitted_polynomial_series'] = fitted_series
            
            
            if (calculate_derivative == True):
        
                # Calculate the derivative of the polynomial:
                if (x_is_datetime):
                    pol_deriv = Polynomial.fit(int_timescale, y, deg = polynomial_degree, full = False).deriv(m = 1)
                
                else:
                    pol_deriv = Polynomial.fit(x, y, deg = polynomial_degree, full = False).deriv(m = 1)
                # m (integer): order of the derivative. If m = 2, the second order is returned.
                # This method returns a series. Check:
                # https://numpy.org/doc/stable/reference/generated/numpy.polynomial.polynomial.Polynomial.deriv.html#numpy.polynomial.polynomial.Polynomial.deriv

                #Add pol_deriv series as a new key from the dictionary:
                dictionary['fitted_polynomial_derivative'] = pol_deriv
                print("1st Order derivative of the polynomial successfully calculated and added to the dictionary as the key \'fitted_polynomial_derivative\'.\n")

            if (calculate_integral == True):

                # Calculate the integral of the polynomial:
                if (x_is_datetime):
                    pol_integral = Polynomial.fit(int_timescale, y, deg = polynomial_degree, full = False).integ(m = 1)
                
                else:
                    pol_integral = Polynomial.fit(x, y, deg = polynomial_degree, full = False).integ(m = 1)
                # m (integer): The number of integrations to perform.
                # This method returns a series. Check:
                # https://numpy.org/doc/stable/reference/generated/numpy.polynomial.polynomial.Polynomial.integ.html#numpy.polynomial.polynomial.Polynomial.integ

                #Add pol_deriv series as a new key from the dictionary:
                dictionary['fitted_polynomial_integral'] = pol_integral
                print("Integral of the polynomial successfully calculated and added to the dictionary as the key \'fitted_polynomial_integral\'.\n")

            if (calculate_roots == True):

                # Calculate the roots of the polynomial:
                if (x_is_datetime):
                    roots_array = Polynomial.fit(int_timescale, y, deg = polynomial_degree, full = False).roots()
                
                else:
                    roots_array = Polynomial.fit(x, y, deg = polynomial_degree, full = False).roots()
                # This method returns an array with the polynomial roots. Check:
                # https://numpy.org/doc/stable/reference/generated/numpy.polynomial.polynomial.Polynomial.roots.html#numpy.polynomial.polynomial.Polynomial.roots

                #Add it as the key polynomial_roots:
                dictionary['polynomial_roots'] = roots_array
                print(f"Roots of the polynomial: {roots_array}.\n")
                print("Roots added to the dictionary as the key \'polynomial_roots\'.\n")

            # Finally, append this dictionary to list support_list:
            list_of_dictionaries_with_series_and_predictions.append(dictionary)
        
        print("Returning a list of dictionaries. Each one contains the arrays of valid series and labels, as well as the regression statistics obtained.\n")
        
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
            
            if (show_polynomial_reg == True):
                
                # Plot the linear regression using the same color.
                # Access the array of fitted Y's in the dictionary:
                Y_PRED = dictionary['fitted_polynomial_series']
                Y_PRED_LABEL = 'fitted_pol_' + str(LABEL) # for the case where label is numeric
                
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
                file_name = "polynomial_fitting"

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
        
        else:
            
            # set a local copy of the dataframe:
            DATASET = df.copy(deep = True)
            
            if (column_with_labels is None):
            
                print("Using the whole series (column) for correlation.\n")
                column_with_labels = 'whole_series_' + column_with_response_var_y
                DATASET[column_with_labels] = column_with_labels
            
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


def select_order_or_rename_columns (df, columns_list, mode = 'select_or_order_columns'):
    
    import numpy as np
    import pandas as pd
    
    # MODE = 'select_or_order_columns' for filtering only the list of columns passed as columns_list,
    # and setting a new column order. In this mode, you can pass the columns in any order: 
    # the order of elements on the list will be the new order of columns.

    # MODE = 'rename_columns' for renaming the columns with the names passed as columns_list. In this
    # mode, the list must have same length and same order of the columns of the dataframe. That is because
    # the columns will sequentially receive the names in the list. So, a mismatching of positions
    # will result into columns with incorrect names.
    
    # columns_list = list of strings containing the names (headers) of the columns to select
    # (filter); or to be set as the new columns' names, according to the selected mode.
    # For instance: columns_list = ['col1', 'col2', 'col3'] will 
    # select columns 'col1', 'col2', and 'col3' (or rename the columns with these names). 
    # Declare the names inside quotes.
    
    # Set a local copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    
    print(f"Original columns in the dataframe:\n{DATASET.columns}")
    
    if ((columns_list is None) | (columns_list == np.nan)):
        # empty list
        columns_list = []
    
    if (len(columns_list) == 0):
        print("Please, input a valid list of columns.\n")
        return DATASET
    
    if (mode == 'select_or_order_columns'):
        
        #filter the dataframe so that it will contain only the cols_list.
        DATASET = DATASET[columns_list]
        print("Dataframe filtered according to the list provided.")
        print("Check the new dataframe:\n")
        print(DATASET)
        
    elif (mode == 'rename_columns'):
        
        # Check if the number of columns of the dataset is equal to the number of elements
        # of the new list. It will avoid raising an exception error.
        boolean_filter = (len(columns_list) == len(DATASET.columns))
        
        if (boolean_filter == False):
            #Impossible to rename, number of elements are different.
            print("The number of columns of the dataframe is different from the number of elements of the list. Please, provide a list with number of elements equals to the number of columns.\n")
            return DATASET
        
        else:
            #Same number of elements, so that we can update the columns' names.
            DATASET.columns = columns_list
            print("Dataframe columns renamed according to the list provided.")
            print("Warning: the substitution is element-wise: the first element of the list is now the name of the first column, and so on, ..., so that the last element is the name of the last column.")
            print("Check the new dataframe:\n")
            print(DATASET)
        
    else:
        print("Enter a valid mode: \'select_or_order_columns\' or \'rename_columns\'.")
        return DATASET
    
    return DATASET


def rename_or_clean_columns_labels (df, mode = 'set_new_names', substring_to_be_replaced = ' ', new_substring_for_replacement = '_', trailing_substring = None, list_of_columns_labels = [{'column_name': None, 'new_column_name': None}, {'column_name': None, 'new_column_name': None}, {'column_name': None, 'new_column_name': None}, {'column_name': None, 'new_column_name': None}, {'column_name': None, 'new_column_name': None}, {'column_name': None, 'new_column_name': None}, {'column_name': None, 'new_column_name': None}, {'column_name': None, 'new_column_name': None}]):
    
    import numpy as np
    import pandas as pd
    # Pandas .rename method:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html
    
    # mode = 'set_new_names' will change the columns according to the specifications in
    # list_of_columns_labels.
    
    # list_of_columns_labels = [{'column_name': None, 'new_column_name': None}]
    # This is a list of dictionaries, where each dictionary contains two key-value pairs:
    # the first one contains the original column name; and the second one contains the new name
    # that will substitute the original one. The function will loop through all dictionaries in
    # this list, access the values of the keys 'column_name', and it will be replaced (switched) 
    # by the correspondent value in key 'new_column_name'.
    
    # The object list_of_columns_labels must be declared as a list, 
    # in brackets, even if there is a single dictionary.
    # Use always the same keys: 'column_name' for the original label; 
    # and 'new_column_name', for the correspondent new label.
    # Notice that this function will not search substrings: it will substitute a value only when
    # there is perfect correspondence between the string in 'column_name' and one of the columns
    # labels. So, the cases (upper or lower) must be the same.
    
    # If you want, you can remove elements (dictionaries) from the list to declare fewer elements;
    # and you can also add more elements (dictionaries) to the lists, if you need to replace more
    # values.
    # Simply put a comma after the last element from the list and declare a new dictionary, keeping the
    # same keys: {'column_name': original_col, 'new_column_name': new_col}, 
    # where original_col and new_col represent the strings for searching and replacement 
    # (If one of the keys contains None, the new dictionary will be ignored).
    # Example: list_of_columns_labels = [{'column_name': 'col1', 'new_column_name': 'col'}] will
    # rename 'col1' as 'col'.
    
    
    # mode = 'capitalize_columns' will capitalize all columns names (i.e., they will be put in
    # upper case). e.g. a column named 'column' will be renamed as 'COLUMN'
    
    # mode = 'lowercase_columns' will lower the case of all columns names. e.g. a column named
    # 'COLUMN' will be renamed as 'column'.
    
    # mode = 'replace_substring' will search on the columns names (strings) for the 
    # substring_to_be_replaced (which may be a character or a string); and will replace it by 
    # new_substring_for_replacement (which again may be either a character or a string). 
    # Numbers (integers or floats) will be automatically converted into strings.
    # As an example, consider the default situation where we search for a whitespace ' ' 
    # and replace it by underscore '_': 
    # substring_to_be_replaced = ' ', new_substring_for_replacement = '_'  
    # In this case, a column named 'new column' will be renamed as 'new_column'.
    
    # mode = 'trim' will remove all trailing or leading whitespaces from column names.
    # e.g. a column named as ' col1 ' will be renamed as 'col1'; 'col2 ' will be renamed as
    # 'col2'; and ' col3' will be renamed as 'col3'.
    
    # mode = 'eliminate_trailing_characters' will eliminate a defined trailing and leading 
    # substring from the columns' names. 
    # The substring must be indicated as trailing_substring, and its default, when no value
    # is provided, is equivalent to mode = 'trim' (eliminate white spaces). 
    # e.g., if trailing_substring = '_test' and you have a column named 'col_test', it will be 
    # renamed as 'col'.
    
    
    # Set a local copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    # Guarantee that the columns were read as strings:
    DATASET.columns = (DATASET.columns).astype(str)
    # dataframe.columns is a Pandas Index object, so it has the dtype attribute as other Pandas
    # objects. So, we can use the astype method to set its type as str or 'object' (or "O").
    # Notice that there are situations with int Index, when integers are used as column names or
    # as row indices. So, this portion guarantees that we can call the str attribute to apply string
    # methods.
    
    if (mode == 'set_new_names'):
        
        # Start a mapping dictionary:
        mapping_dict = {}
        # This dictionary will be in the format required by .rename method: old column name as key,
        # and new name as value.

        # Loop through each element from list_of_columns_labels:
        for dictionary in list_of_columns_labels:

            # Access the values in keys:
            column_name = dictionary['column_name']
            new_column_name = dictionary['new_column_name']

            # Check if neither is None:
            if ((column_name is not None) & (new_column_name is not None)):
                
                # Guarantee that both were read as strings:
                column_name = str(column_name)
                new_column_name = str(new_column_name)

                # Add it to the mapping dictionary setting column_name as key, and the new name as the
                # value:
                mapping_dict[column_name] = new_column_name

        # Now, the dictionary is in the correct format for the method. Let's apply it:
        DATASET.rename(columns = mapping_dict, inplace = True)
    
    elif (mode == 'capitalize_columns'):
        
        DATASET.rename(str.upper, axis = 'columns', inplace = True)
    
    elif (mode == 'lowercase_columns'):
        
        DATASET.rename(str.lower, axis = 'columns', inplace = True)
    
    elif (mode == 'replace_substring'):
        
        if (substring_to_be_replaced is None):
            # set as the default (whitespace):
            substring_to_be_replaced = ' '
        
        if (new_substring_for_replacement is None):
            # set as the default (underscore):
            new_substring_for_replacement = '_'
        
        # Apply the str attribute to guarantee that numbers were read as strings:
        substring_to_be_replaced = str(substring_to_be_replaced)
        new_substring_for_replacement = str(new_substring_for_replacement)
        # Replace the substrings in the columns' names:
        substring_replaced_series = (pd.Series(DATASET.columns)).str.replace(substring_to_be_replaced, new_substring_for_replacement)
        # The Index object is not callable, and applying the str attribute to a np.array or to a list
        # will result in a single string concatenating all elements from the array. So, we convert
        # the columns index to a pandas series for performing a element-wise string replacement.
        
        # Now, convert the columns to the series with the replaced substrings:
        DATASET.columns = substring_replaced_series
        
    elif (mode == 'trim'):
        # Use the strip method from str attribute with no argument, correspondening to the
        # Trim function.
        DATASET.rename(str.strip, axis = 'columns', inplace = True)
    
    elif (mode == 'eliminate_trailing_characters'):
        
        if ((trailing_substring is None) | (trailing_substring == np.nan)):
            # Apply the str.strip() with no arguments:
            DATASET.rename(str.strip, axis = 'columns', inplace = True)
        
        else:
            # Apply the str attribute to guarantee that numbers were read as strings:
            trailing_substring = str(trailing_substring)

            # Apply the strip method:
            stripped_series = (pd.Series(DATASET.columns)).str.strip(trailing_substring)
            # The Index object is not callable, and applying the str attribute to a np.array or to a list
            # will result in a single string concatenating all elements from the array. So, we convert
            # the columns index to a pandas series for performing a element-wise string replacement.

            # Now, convert the columns to the series with the stripped strings:
            DATASET.columns = stripped_series
    
    else:
        print("Select a valid mode: \'set_new_names\', \'capitalize_columns\', \'lowercase_columns\', \'replace_substrings\', \'trim\', or \'eliminate_trailing_characters\'.\n")
        return "error"
    
    print("Finished renaming dataframe columns.")
    print("Check the new dataframe:\n")
    print(DATASET)
        
    return DATASET


def trim_spaces_or_characters (df, column_to_analyze, new_variable_type = None, method = 'trim', substring_to_eliminate = None, create_new_column = True, new_column_suffix = "_trim"):
    
    import numpy as np
    import pandas as pd
    
    # column_to_analyze: string (inside quotes), 
    # containing the name of the column that will be analyzed. 
    # e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    # new_variable_type = None. String (in quotes) that represents a given data type for the column
    # after transformation. Set:
    # - new_variable_type = 'int' to convert the column to integer type after the transform;
    # - new_variable_type = 'float' to convert the column to float (decimal number);
    # - new_variable_type = 'datetime' to convert it to date or timestamp;
    # - new_variable_type = 'category' to convert it to Pandas categorical variable.
    
    # method = 'trim' will eliminate trailing and leading white spaces from the strings in
    # column_to_analyze.
    # method = 'substring' will eliminate a defined trailing and leading substring from
    # column_to_analyze.
    
    # substring_to_eliminate = None. Set as a string (in quotes) if method = 'substring'.
    # e.g. suppose column_to_analyze contains time information: each string ends in " min":
    # "1 min", "2 min", "3 min", etc. If substring_to_eliminate = " min", this portion will be
    # eliminated, resulting in: "1", "2", "3", etc. If new_variable_type = None, these values will
    # continue to be strings. By setting new_variable_type = 'int' or 'float', the series will be
    # converted to a numeric type.
    
    # create_new_column = True
    # Alternatively, set create_new_column = True to store the transformed data into a new
    # column. Or set create_new_column = False to overwrite the existing column.
    
    # new_column_suffix = "_trim"
    # This value has effect only if create_new_column = True.
    # The new column name will be set as column + new_column_suffix. Then, if the original
    # column was "column1" and the suffix is "_trim", the new column will be named as
    # "column1_trim".
    # Alternatively, input inside quotes a string with the desired suffix. Recommendation:
    # start the suffix with "_" to separate it from the original name.
    
    
    # Set a local copy of dataframe to manipulate
    DATASET = df.copy(deep = True)
    # Guarantee that the column to analyze was read as string:
    DATASET[column_to_analyze] = (DATASET[column_to_analyze]).astype(str)
    new_series = DATASET[column_to_analyze].copy()
    
    if (method == 'substring'):
        
        if (substring_to_eliminate is None):
            
            method = 'trim'
            print("No valid substring input. Modifying method to \'trim\'.\n")
    
    if (method == 'substring'):
        
        print("ATTENTION: Operations of string strip (removal) or replacement are all case-sensitive. There must be correct correspondence between cases and spaces for the strings being removed or replaced.\n")
        # For manipulating strings, call the str attribute and, then, the method to be applied:
        new_series = new_series.str.strip(substring_to_eliminate)
    
    else:
        
        new_series = new_series.str.strip()
    
    # Check if a the series type should be modified:
    if (new_variable_type is not None):
        
        if (new_variable_type == 'int'):

            new_type = np.int64

        elif (new_variable_type == 'float'):
            
            new_type = np.float64
        
        elif (new_variable_type == 'datetime'):
            
            new_type = np.datetime64
        
        elif (new_variable_type == 'category'):
            
            new_type = new_variable_type
        
        # Try converting the type:
        try:
            new_series = new_series.astype(new_type)
            print(f"Successfully converted the series to the type {new_variable_type}.\n")
        
        except:
            pass

    if (create_new_column):
        
        if (new_column_suffix is None):
            new_column_suffix = "_trim"
                
        new_column_name = column_to_analyze + new_column_suffix
        DATASET[new_column_name] = new_series
            
    else:
        
        DATASET[column_to_analyze] = new_series
    
    # Now, we are in the main code.
    print("Finished removing leading and trailing spaces or characters (substrings).")
    print("Check the 10 first elements from the series:\n")
    print(new_series.head(10))
    
    return DATASET


def capitalize_or_lower_string_case (df, column_to_analyze, method = 'lowercase', create_new_column = True, new_column_suffix = "_homogenized"):
     
    import numpy as np
    import pandas as pd
    
    # column_to_analyze: string (inside quotes), 
    # containing the name of the column that will be analyzed. 
    # e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    # method = 'capitalize' will capitalize all letters from the input string 
    # (turn them to upper case).
    # method = 'lowercase' will make the opposite: turn all letters to lower case.
    # e.g. suppose column_to_analyze contains strings such as 'String One', 'STRING 2',  and
    # 'string3'. If method = 'capitalize', the output will contain the strings: 
    # 'STRING ONE', 'STRING 2', 'STRING3'. If method = 'lowercase', the outputs will be:
    # 'string one', 'string 2', 'string3'.
    
    # create_new_column = True
    # Alternatively, set create_new_columns = True to store the transformed data into a new
    # column. Or set create_new_column = False to overwrite the existing column.
    
    # new_column_suffix = "_homogenized"
    # This value has effect only if create_new_column = True.
    # The new column name will be set as column + new_column_suffix. Then, if the original
    # column was "column1" and the suffix is "_homogenized", the new column will be named as
    # "column1_homogenized".
    # Alternatively, input inside quotes a string with the desired suffix. Recommendation:
    # start the suffix with "_" to separate it from the original name.
    
    
    # Set a local copy of dataframe to manipulate
    DATASET = df.copy(deep = True)
    # Guarantee that the column to analyze was read as string:
    DATASET[column_to_analyze] = (DATASET[column_to_analyze]).astype(str)
    new_series = DATASET[column_to_analyze].copy()
    
    if (method == 'capitalize'):
        
        print("Capitalizing the string (moving all characters to upper case).\n")
        # For manipulating strings, call the str attribute and, then, the method to be applied:
        new_series = new_series.str.upper()
    
    else:
        
        print("Lowering the string case (moving all characters to lower case).\n")
        new_series = new_series.str.lower()
        
    if (create_new_column):
        
        if (new_column_suffix is None):
            new_column_suffix = "_homogenized"
                
        new_column_name = column_to_analyze + new_column_suffix
        DATASET[new_column_name] = new_series
            
    else:
        
        DATASET[column_to_analyze] = new_series
    
    # Now, we are in the main code.
    print(f"Finished homogenizing the string case of {column_to_analyze}, giving value consistency.")
    print("Check the 10 first elements from the series:\n")
    print(new_series.head(10))
    
    return DATASET


def replace_substring (df, column_to_analyze, substring_to_be_replaced = None, new_substring_for_replacement = '', create_new_column = True, new_column_suffix = "_substringReplaced"):
     
    import numpy as np
    import pandas as pd
    
    # column_to_analyze: string (inside quotes), 
    # containing the name of the column that will be analyzed. 
    # e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    # substring_to_be_replaced = None; new_substring_for_replacement = ''. 
    # Strings (in quotes): when the sequence of characters substring_to_be_replaced was
    # found in the strings from column_to_analyze, it will be substituted by the substring
    # new_substring_for_replacement. If None is provided to one of these substring arguments,
    # it will be substituted by the empty string: ''
    # e.g. suppose column_to_analyze contains the following strings, with a spelling error:
    # "my collumn 1", 'his collumn 2', 'her column 3'. We may correct this error by setting:
    # substring_to_be_replaced = 'collumn' and new_substring_for_replacement = 'column'. The
    # function will search for the wrong group of characters and, if it finds it, will substitute
    # by the correct sequence: "my column 1", 'his column 2', 'her column 3'.
    
    # create_new_column = True
    # Alternatively, set create_new_columns = True to store the transformed data into a new
    # column. Or set create_new_column = False to overwrite the existing column.
    
    # new_column_suffix = "_substringReplaced"
    # This value has effect only if create_new_column = True.
    # The new column name will be set as column + new_column_suffix. Then, if the original
    # column was "column1" and the suffix is "_substringReplaced", the new column will be named as
    # "column1_substringReplaced".
    # Alternatively, input inside quotes a string with the desired suffix. Recommendation:
    # start the suffix with "_" to separate it from the original name.
    
    
    # Set a local copy of dataframe to manipulate
    DATASET = df.copy(deep = True)
    # Guarantee that the column to analyze was read as string:
    DATASET[column_to_analyze] = (DATASET[column_to_analyze]).astype(str)
    new_series = DATASET[column_to_analyze].copy()
    
    print("ATTENTION: Operations of string strip (removal) or replacement are all case-sensitive. There must be correct correspondence between cases and spaces for the strings being removed or replaced.\n")
        
    # If one of the input substrings is None, make it the empty string:
    if (substring_to_be_replaced is None):
        substring_to_be_replaced = ''
    
    if (new_substring_for_replacement is None):
        new_substring_for_replacement = ''
    
    # Guarantee that both were read as strings (they may have been improperly read as 
    # integers or floats):
    substring_to_be_replaced = str(substring_to_be_replaced)
    new_substring_for_replacement = str(new_substring_for_replacement)
    
    # For manipulating strings, call the str attribute and, then, the method to be applied:
    new_series = new_series.str.replace(substring_to_be_replaced, new_substring_for_replacement)
        
    if (create_new_column):
        
        if (new_column_suffix is None):
            new_column_suffix = "_substringReplaced"
                
        new_column_name = column_to_analyze + new_column_suffix
        DATASET[new_column_name] = new_series
            
    else:
        
        DATASET[column_to_analyze] = new_series
    
    # Now, we are in the main code.
    print(f"Finished replacing the substring {substring_to_be_replaced} by {new_substring_for_replacement}.")
    print("Check the 10 first elements from the series:\n")
    print(new_series.head(10))
    
    return DATASET


def switch_strings (df, column_to_analyze, list_of_dictionaries_with_original_strings_and_replacements = [{'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}], create_new_column = True, new_column_suffix = "_stringReplaced"):
     
    import numpy as np
    import pandas as pd
    
    # column_to_analyze: string (inside quotes), 
    # containing the name of the column that will be analyzed. 
    # e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    # list_of_dictionaries_with_original_strings_and_replacements = 
    # [{'original_string': None, 'new_string': None}]
    # This is a list of dictionaries, where each dictionary contains two key-value pairs:
    # the first one contains the original string; and the second one contains the new string
    # that will substitute the original one. The function will loop through all dictionaries in
    # this list, access the values of the keys 'original_string', and search these values on the strings
    # in column_to_analyze. When the value is found, it will be replaced (switched) by the correspondent
    # value in key 'new_string'.
    
    # The object list_of_dictionaries_with_original_strings_and_replacements must be declared as a list, 
    # in brackets, even if there is a single dictionary.
    # Use always the same keys: 'original_string' for the original strings to search on the column 
    # column_to_analyze; and 'new_string', for the strings that will replace the original ones.
    # Notice that this function will not search substrings: it will substitute a value only when
    # there is perfect correspondence between the string in 'column_to_analyze' and 'original_string'.
    # So, the cases (upper or lower) must be the same.
    
    # If you want, you can remove elements (dictionaries) from the list to declare fewer elements;
    # and you can also add more elements (dictionaries) to the lists, if you need to replace more
    # values.
    # Simply put a comma after the last element from the list and declare a new dictionary, keeping the
    # same keys: {'original_string': original_str, 'new_string': new_str}, 
    # where original_str and new_str represent the strings for searching and replacement 
    # (If one of the keys contains None, the new dictionary will be ignored).
    
    # Example:
    # Suppose the column_to_analyze contains the values 'sunday', 'monday', 'tuesday', 'wednesday',
    # 'thursday', 'friday', 'saturday', but you want to obtain data labelled as 'weekend' or 'weekday'.
    # Set: list_of_dictionaries_with_original_strings_and_replacements = 
    # [{'original_string': 'sunday', 'new_string': 'weekend'},
    # {'original_string': 'saturday', 'new_string': 'weekend'},
    # {'original_string': 'monday', 'new_string': 'weekday'},
    # {'original_string': 'tuesday', 'new_string': 'weekday'},
    # {'original_string': 'wednesday', 'new_string': 'weekday'},
    # {'original_string': 'thursday', 'new_string': 'weekday'},
    # {'original_string': 'friday', 'new_string': 'weekday'}]
    
    # create_new_column = True
    # Alternatively, set create_new_columns = True to store the transformed data into a new
    # column. Or set create_new_column = False to overwrite the existing column.
    
    # new_column_suffix = "_stringReplaced"
    # This value has effect only if create_new_column = True.
    # The new column name will be set as column + new_columns_suffix. Then, if the original
    # column was "column1" and the suffix is "_stringReplaced", the new column will be named as
    # "column1_stringReplaced".
    # Alternatively, input inside quotes a string with the desired suffix. Recommendation:
    # start the suffix with "_" to separate it from the original name.
    
    
    # Set a local copy of dataframe to manipulate
    DATASET = df.copy(deep = True)
    # Guarantee that the column to analyze was read as string:
    DATASET[column_to_analyze] = (DATASET[column_to_analyze]).astype(str)
    new_series = DATASET[column_to_analyze].copy()
    
    print("ATTENTION: Operations of string strip (removal) or replacement are all case-sensitive. There must be correct correspondence between cases and spaces for the strings being removed or replaced.\n")
     
    # Create the mapping dictionary for the str.replace method:
    mapping_dict = {}
    # The key of the mapping dict must be an string, whereas the value must be the new string
    # that will replace it.
        
    # Loop through each element on the list list_of_dictionaries_with_original_strings_and_replacements:
    
    for i in range (0, len(list_of_dictionaries_with_original_strings_and_replacements)):
        # from i = 0 to i = len(list_of_dictionaries_with_original_strings_and_replacements) - 1, index of the
        # last element from the list
            
        # pick the i-th dictionary from the list:
        dictionary = list_of_dictionaries_with_original_strings_and_replacements[i]
            
        # access 'original_string' and 'new_string' keys from the dictionary:
        original_string = dictionary['original_string']
        new_string = dictionary['new_string']
        
        # check if they are not None:
        if ((original_string is not None) & (new_string is not None)):
            
            #Guarantee that both are read as strings:
            original_string = str(original_string)
            new_string = str(new_string)
            
            # add them to the mapping dictionary, using the original_string as key and
            # new_string as the correspondent value:
            mapping_dict[original_string] = new_string
    
    # Now, the input list was converted into a dictionary with the correct format for the method.
    # Check if there is at least one key in the dictionary:
    if (len(mapping_dict) > 0):
        # len of a dictionary returns the amount of key:value pairs stored. If nothing is stored,
        # len = 0. dictionary.keys() method (no arguments in parentheses) returns an array containing
        # the keys; whereas dictionary.values() method returns the arrays of the values.
        
        new_series = new_series.replace(mapping_dict)
        # For replacing the whole strings using a mapping dictionary, do not call the str
        # attribute
    
        if (create_new_column):
            
            if (new_column_suffix is None):
                new_column_suffix = "_substringReplaced"

            new_column_name = column_to_analyze + new_column_suffix
            DATASET[new_column_name] = new_series
            
        else:

            DATASET[column_to_analyze] = new_series

        # Now, we are in the main code.
        print(f"Finished replacing the substrings accordingly to the mapping: {mapping_dict}.")
        print("Check the 10 first elements from the series:\n")
        print(new_series.head(10))

        return DATASET
    
    else:
        print("Input at least one dictionary containing a pair of original string, in the key \'original_string\', and the correspondent new string as key \'new_string\'.")
        print("The dictionaries must be elements from the list list_of_dictionaries_with_original_strings_and_replacements.\n")
        
        return "error"


def string_replacement_ml (df, column_to_analyze, mode = 'find_and_replace', threshold_for_percent_of_similarity = 80.0, list_of_dictionaries_with_standard_strings_for_replacement = [{'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}], create_new_column = True, new_column_suffix = "_stringReplaced"):
    
    import numpy as np
    import pandas as pd
    from fuzzywuzzy import process
    
    # column_to_analyze: string (inside quotes), 
    # containing the name of the column that will be analyzed. 
    # e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    # mode = 'find_and_replace' will find similar strings; and switch them by one of the
    # standard strings if the similarity between them is higher than or equals to the threshold.
    # Alternatively: mode = 'find' will only find the similar strings by calculating the similarity.
    
    # threshold_for_percent_of_similarity = 80.0 - 0.0% means no similarity and 100% means equal strings.
    # The threshold_for_percent_of_similarity is the minimum similarity calculated from the
    # Levenshtein (minimum edit) distance algorithm. This distance represents the minimum number of
    # insertion, substitution or deletion of characters operations that are needed for making two
    # strings equal.
    
    # list_of_dictionaries_with_standard_strings_for_replacement =
    # [{'standard_string': None}]
    # This is a list of dictionaries, where each dictionary contains a single key-value pair:
    # the key must be always 'standard_string', and the value will be one of the standard strings 
    # for replacement: if a given string on the column_to_analyze presents a similarity with one 
    # of the standard string equals or higher than the threshold_for_percent_of_similarity, it will be
    # substituted by this standard string.
    # For instance, suppose you have a word written in too many ways, making it difficult to use
    # the function switch_strings: "EU" , "eur" , "Europ" , "Europa" , "Erope" , "Evropa" ...
    # You can use this function to search strings similar to "Europe" and replace them.
    
    # The function will loop through all dictionaries in
    # this list, access the values of the keys 'standard_string', and search these values on the strings
    # in column_to_analyze. When the value is found, it will be replaced (switched) if the similarity
    # is sufficiently high.
    
    # The object list_of_dictionaries_with_standard_strings_for_replacement must be declared as a list, 
    # in brackets, even if there is a single dictionary.
    # Use always the same keys: 'standard_string'.
    # Notice that this function performs fuzzy matching, so it MAY SEARCH substrings and strings
    # written with different cases (upper or lower) when this portions or modifications make the
    # strings sufficiently similar to each other.
    
    # If you want, you can remove elements (dictionaries) from the list to declare fewer elements;
    # and you can also add more elements (dictionaries) to the lists, if you need to replace more
    # values.
    # Simply put a comma after the last element from the list and declare a new dictionary, keeping the
    # same key: {'standard_string': other_std_str}, 
    # where other_std_str represents the string for searching and replacement 
    # (If the key contains None, the new dictionary will be ignored).
    
    # Example:
    # Suppose the column_to_analyze contains the values 'California', 'Cali', 'Calefornia', 
    # 'Calefornie', 'Californie', 'Calfornia', 'Calefernia', 'New York', 'New York City', 
    # but you want to obtain data labelled as the state 'California' or 'New York'.
    # Set: list_of_dictionaries_with_standard_strings_for_replacement = 
    # [{'standard_string': 'California'},
    # {'standard_string': 'New York'}]
    
    # ATTENTION: It is advisable for previously searching the similarity to find the best similarity
    # threshold; set it as high as possible, avoiding incorrect substitutions in a gray area; and then
    # perform the replacement. It will avoid the repetition of original incorrect strings in the
    # output dataset, as well as wrong replacement (replacement by one of the standard strings which
    # is not the correct one).
    
    # create_new_column = True
    # Alternatively, set create_new_columns = True to store the transformed data into a new
    # column. Or set create_new_column = False to overwrite the existing column.
    
    # new_column_suffix = "_stringReplaced"
    # This value has effect only if create_new_column = True.
    # The new column name will be set as column + new_columns_suffix. Then, if the original
    # column was "column1" and the suffix is "_stringReplaced", the new column will be named as
    # "column1_stringReplaced".
    # Alternatively, input inside quotes a string with the desired suffix. Recommendation:
    # start the suffix with "_" to separate it from the original name.
    
    
    print("Performing fuzzy replacement based on the Levenshtein (minimum edit) distance algorithm.")
    print("This distance represents the minimum number of insertion, substitution or deletion of characters operations that are needed for making two strings equal.\n")
    
    print("This means that substrings or different cases (upper or higher) may be searched and replaced, as long as the similarity threshold is reached.\n")
    
    print("ATTENTION!\n")
    print("It is advisable for previously searching the similarity to find the best similarity threshold.")
    print("Set the threshold as high as possible, and only then perform the replacement.")
    print("It will avoid the repetition of original incorrect strings in the output dataset, as well as wrong replacement (replacement by one of the standard strings which is not the correct one.\n")
    
    # Set a local copy of dataframe to manipulate
    DATASET = df.copy(deep = True)
    # Guarantee that the column to analyze was read as string:
    DATASET[column_to_analyze] = (DATASET[column_to_analyze]).astype(str)
    new_series = DATASET[column_to_analyze].copy()

    # Get the unique values present in column_to_analyze:
    unique_types = new_series.unique()
    
    # Create the summary_list:
    summary_list = []
        
    # Loop through each element on the list list_of_dictionaries_with_original_strings_and_replacements:
    
    for i in range (0, len(list_of_dictionaries_with_standard_strings_for_replacement)):
        # from i = 0 to i = len(list_of_dictionaries_with_standard_strings_for_replacement) - 1, index of the
        # last element from the list
            
        # pick the i-th dictionary from the list:
        dictionary = list_of_dictionaries_with_standard_strings_for_replacement[i]
            
        # access 'standard_string' key from the dictionary:
        standard_string = dictionary['standard_string']
        
        # check if it is not None:
        if (standard_string is not None):
            
            # Guarantee that it was read as a string:
            standard_string = str(standard_string)
            
            # Calculate the similarity between each one of the unique_types and standard_string:
            similarity_list = process.extract(standard_string, unique_types, limit = len(unique_types))
            
            # Add the similarity list to the dictionary:
            dictionary['similarity_list'] = similarity_list
            # This is a list of tuples with the format (tested_string, percent_of_similarity_with_standard_string)
            # e.g. ('asiane', 92) for checking similarity with string 'asian'
            
            if (mode == 'find_and_replace'):
                
                # If an invalid value was set for threshold_for_percent_of_similarity, correct it to 80% standard:
                
                if(threshold_for_percent_of_similarity is None):
                    threshold_for_percent_of_similarity = 80.0
                
                if((threshold_for_percent_of_similarity == np.nan) | (threshold_for_percent_of_similarity < 0)):
                    threshold_for_percent_of_similarity = 80.0
                
                list_of_replacements = []
                # Let's replace the matches in the series by the standard_string:
                # Iterate through the list of matches
                for match in similarity_list:
                    # Check whether the similarity score is greater than or equal to threshold_for_percent_of_similarity.
                    # The similarity score is the second element (index 1) from the tuples:
                    if (match[1] >= threshold_for_percent_of_similarity):
                        # If it is, select all rows where the column_to_analyze is spelled as
                        # match[0] (1st Tuple element), and set it to standard_string:
                        boolean_filter = (new_series == match[0])
                        new_series.loc[boolean_filter] = standard_string
                        print(f"Found {match[1]}% of similarity between {match[0]} and {standard_string}.")
                        print(f"Then, {match[0]} was replaced by {standard_string}.\n")
                        
                        # Add match to the list of replacements:
                        list_of_replacements.append(match)
                
                # Add the list_of_replacements to the dictionary, if its length is higher than zero:
                if (len(list_of_replacements) > 0):
                    dictionary['list_of_replacements_by_std_str'] = list_of_replacements
            
            # Add the dictionary to the summary_list:
            summary_list.append(dictionary)
      
    # Now, let's replace the original column or create a new one if mode was set as replace:
    if (mode == 'find_and_replace'):
    
        if (create_new_column):
            
            if (new_column_suffix is None):
                new_column_suffix = "_substringReplaced"

            new_column_name = column_to_analyze + new_column_suffix
            DATASET[new_column_name] = new_series
            
        else:

            DATASET[column_to_analyze] = new_series

        # Now, we are in the main code.
        print(f"Finished replacing the strings by the provided standards. Returning the new dataset and a summary list.")
        print("In summary_list, you can check the calculated similarities in keys \'similarity_list\' from the dictionaries.")
        print("The similarity list is a list of tuples, where the first element is the string compared against the value on key  \'standard_string\'; and the second element is the similarity score, the percent of similarity between the tested and the standard string.\n")
        print("Check the 10 first elements from the new series, with strings replaced:\n")
        print(new_series.head(10))
    
    else:
        
        print("Finished mapping similarities. Returning the original dataset and a summary list")
        print("Check the similarities below, in keys \'similarity_list\' from the dictionaries.")
        print("The similarity list is a list of tuples, where the first element is the string compared against the value on key  \'standard_string\'; and the second element is the similarity score, the percent of similarity between the tested and the standard string.\n")
        print(summary_list)
    
    return DATASET, summary_list


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
    
    # new_columns_suffix = "_log"
    # This value has effect only if create_new_column = True.
    # The new column name will be set as column + new_columns_suffix. Then, if the original
    # column was "column1" and the suffix is "_log", the new column will be named as
    # "column1_log".
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
    
    # new_columns_suffix = "_originalScale"
    # This value has effect only if create_new_column = True.
    # The new column name will be set as column + new_columns_suffix. Then, if the original
    # column was "column1" and the suffix is "_originalScale", the new column will be named 
    # as "column1_originalScale".
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


def box_cox_transform (df, column_to_transform, mode = 'calculate_and_apply', lambda_boxcox = None, suffix = '_BoxCoxTransf', specification_limits = {'lower_spec_lim': None, 'upper_spec_lim': None}):
    
    import numpy as np
    import pandas as pd
    from statsmodels.stats import diagnostic
    from scipy import stats
    
    # This function will process a single column column_to_transform 
    # of the dataframe df per call.
    
    # Check https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.boxcox.html
    ## Box-Cox transform is given by:
    ## y = (x**lmbda - 1) / lmbda,  for lmbda != 0
    ## log(x),                  for lmbda = 0
    
    # column_to_transform must be a string with the name of the column.
    # e.g. column_to_transform = 'column1' to transform a column named as 'column1'
    
    # mode = 'calculate_and_apply'
    # Aternatively, mode = 'calculate_and_apply' to calculate lambda and apply Box-Cox
    # transform; mode = 'apply_only' to apply the transform for a known lambda.
    # To 'apply_only', lambda_box must be provided.
    
    # lambda_boxcox must be a float value. e.g. lamda_boxcox = 1.7
    # If you calculated lambda from the function box_cox_transform and saved the
    # transformation data summary dictionary as data_sum_dict, simply set:
    # lambda_boxcox = data_sum_dict['lambda_boxcox']
    # This will access the value on the key 'lambda_boxcox' of the dictionary, which
    # contains the lambda. 
    
    # Analogously, spec_lim_dict['Inf_spec_lim_transf'] access
    # the inferior specification limit transformed; and spec_lim_dict['Sup_spec_lim_transf'] 
    # access the superior specification limit transformed.
    
    # If lambda_boxcox is None, 
    # the mode will be automatically set as 'calculate_and_apply'.
    
    # suffix: string (inside quotes).
    # How the transformed column will be identified in the returned data_transformed_df.
    # If y_label = 'Y' and suffix = '_BoxCoxTransf', the transformed column will be
    # identified as 'Y_BoxCoxTransf'.
    # Alternatively, input inside quotes a string with the desired suffix. Recommendation:
    # start the suffix with "_" to separate it from the original name
    
    # specification_limits = {'lower_spec_lim': None, 'upper_spec_lim': None}
    # If there are specification limits, input them in this dictionary. Do not modify the keys,
    # simply substitute None by the lower and/or the upper specification.
    # e.g. Suppose you have a tank that cannot have more than 10 L. So:
    # specification_limits = {'lower_spec_lim': None, 'upper_spec_lim': 10}, there is only
    # an upper specification equals to 10 (do not add units);
    # Suppose a temperature cannot be lower than 10 ºC, but there is no upper specification. So,
    # specification_limits = {'lower_spec_lim': 10, 'upper_spec_lim': None}. Finally, suppose
    # a liquid which pH must be between 6.8 and 7.2:
    # specification_limits = {'lower_spec_lim': 6.8, 'upper_spec_lim': 7.2}
    
    if not (suffix is None):
        #only if a suffix was declared
        #concatenate the column name to the suffix
        new_col = column_to_transform + suffix
    
    else:
        #concatenate the column name to the standard '_BoxCoxTransf' suffix
        new_col = column_to_transform + '_BoxCoxTransf'
    
    boolean_check = (mode != 'calculate_and_apply') & (mode != 'apply_only')
    # & is the 'and' operator. != is the 'is different from' operator.
    #Check if neither 'calculate_and_apply' nor 'apply_only' were selected
    
    if ((lambda_boxcox is None) & (mode == 'apply_only')):
        print("Invalid value set for \'lambda_boxcox'\. Setting mode to \'calculate_and_apply\'.")
        mode = 'calculate_and_apply'
    
    elif (boolean_check == True):
        print("Invalid value set for \'mode'\. Setting mode to \'calculate_and_apply\'.")
        mode = 'calculate_and_apply'
    
    
    # Start a local copy of the dataframe:
    DATASET = df.copy(deep = True)
    
    print("Box-Cox transformation must be applied only to values higher than zero.")
    print("That is because it is a logarithmic transformation.")
    print(f"So, filtering out all values from {column_to_transform} lower than or equal to zero.\n")
    DATASET = DATASET[DATASET[column_to_transform] > 0]
    DATASET = DATASET.reset_index(drop = True)
    
    y = DATASET[column_to_transform]
    
    
    if (mode == 'calculate_and_apply'):
        # Calculate lambda_boxcox
        lambda_boxcox = stats.boxcox_normmax(y, method = 'pearsonr')
        #calcula o lambda da transformacao box-cox utilizando o metodo da maxima verossimilhanca
        #por meio da maximizacao do coeficiente de correlacao de pearson da funcao
        #y = boxcox(x), onde boxcox representa a transformacao
    
    # For other cases, we will apply the lambda_boxcox set as the function parameter.

    #Calculo da variavel transformada
    y_transform = stats.boxcox(y, lmbda = lambda_boxcox, alpha = None)
    #Calculo da transformada
    
    DATASET[new_col] = y_transform
    #dataframe contendo os dados transformados
    
    print("Data successfully transformed. Check the 10 first transformed rows:\n")
    print(DATASET.head(10))
    print("\n") #line break
    
    # Start a dictionary to store the summary results of the transform and the normality
    # tests:
    data_sum_dict = {'lambda_boxcox': lambda_boxcox}
    
    # Test normality of the transformed variable:
    # Scipy.stats’ normality test
    # It is based on D’Agostino and Pearson’s test that combines 
    # skew and kurtosis to produce an omnibus test of normality.
    _, scipystats_test_pval = stats.normaltest(y_transform) 
    # add this test result to the dictionary:
    data_sum_dict['dagostino_pearson_p_val'] = scipystats_test_pval
            
    # Scipy.stats’ Shapiro-Wilk test
    shapiro_test = stats.shapiro(y_transform)
    data_sum_dict['shapiro_wilk_p_val'] = shapiro_test[1]
    
    # Lilliefors’ normality test
    lilliefors_test = diagnostic.kstest_normal(y_transform, dist = 'norm', pvalmethod = 'table')
    data_sum_dict['lilliefors_p_val'] = lilliefors_test[1]
    
    # Anderson-Darling normality test
    ad_test = diagnostic.normal_ad(y_transform, axis = 0)
    data_sum_dict['anderson_darling_p_val'] = ad_test[1]
     
    print("Box-Cox Transformation Summary:\n")
    print(data_sum_dict)
    print("\n") #line break
    
    if not ((specification_limits['lower_spec_lim'] is None) & (specification_limits['upper_spec_lim'] is None)):
        # Convert it to a list of specs:
        list_of_specs = []
        
        if not (specification_limits['lower_spec_lim'] is None):
            
            if (specification_limits['lower_spec_lim'] <= 0):
                print("Box-Cox transform can only be applied to values higher than zero. So, ignoring the lower specification.\n")
            
            else:
                list_of_specs.append(specification_limits['lower_spec_lim'])
        
        if not (specification_limits['upper_spec_lim'] is None):
            
            if (specification_limits['upper_spec_lim'] <= 0):
                print("Box-Cox transform can only be applied to values higher than zero. So, ignoring the upper specification.\n")
            
            else:
                list_of_specs.append(specification_limits['upper_spec_lim'])
        
        # Notice that the list may have 1 or 2 elements.
        
        # Convert the list of specifications into a NumPy array:
        spec_lim_array = np.array(list_of_specs)
        
        # If the array has a single element, we cannot apply stats method. So, let's transform
        # manually:
        ## y = (x**lmbda - 1) / lmbda,  for lmbda != 0
        ## log(x),                  for lmbda = 0
        if (lambda_boxcox == 0):
            
            spec_lim_array = np.log(spec_lim_array)
        
        else:
            spec_lim_array = ((spec_lim_array**lambda_boxcox) - 1)/(lambda_boxcox)
        
        # Start a dictionary to store the transformed limits:
        spec_lim_dict = {}
        
        if not (specification_limits['lower_spec_lim'] is None):
            # First element of the array is the lower specification. Add it to the
            # dictionary:
            spec_lim_dict['lower_spec_lim_transf'] = spec_lim_array[0]
            
            if not (specification_limits['upper_spec_lim'] is None):
                # Second element of the array is the upper specification. Add it to the
                # dictionary:
                spec_lim_dict['upper_spec_lim_transf'] = spec_lim_array[1]
        
        else:
            # The array contains only one element, which is the upper specification. Add
            # it to the dictionary:
            spec_lim_dict['upper_spec_lim_transf'] = spec_lim_array[0]
        
        print("New specification limits successfully obtained:\n")
        print(spec_lim_dict)
        
        # Add spec_lim_dict as a new element from data_sum_dict:
        data_sum_dict['spec_lim_dict'] = spec_lim_dict
    
    
    return DATASET, data_sum_dict


def reverse_box_cox (df, column_to_transform, lambda_boxcox, suffix = '_ReversedBoxCox'):
    
    import numpy as np
    import pandas as pd
    
    # This function will process a single column column_to_transform 
    # of the dataframe df per call.
    
    # Check https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.boxcox.html
    ## Box-Cox transform is given by:
    ## y = (x**lmbda - 1) / lmbda,  for lmbda != 0
    ## log(x),                  for lmbda = 0
    
    # column_to_transform must be a string with the name of the column.
    # e.g. column_to_transform = 'column1' to transform a column named as 'column1'
    
    # lambda_boxcox must be a float value. e.g. lamda_boxcox = 1.7
    # If you calculated lambda from the function box_cox_transform and saved the
    # transformation data summary dictionary as data_sum_dict, simply set:
    # lambda_boxcox = data_sum_dict['lambda_boxcox']
    # This will access the value on the key 'lambda_boxcox' of the dictionary, which
    # contains the lambda. 
    
    # Analogously, spec_lim_dict['Inf_spec_lim_transf'] access
    # the inferior specification limit transformed; and spec_lim_dict['Sup_spec_lim_transf'] 
    # access the superior specification limit transformed.
    
    #suffix: string (inside quotes).
    # How the transformed column will be identified in the returned data_transformed_df.
    # If y_label = 'Y' and suffix = '_ReversedBoxCox', the transformed column will be
    # identified as '_ReversedBoxCox'.
    # Alternatively, input inside quotes a string with the desired suffix. Recommendation:
    # start the suffix with "_" to separate it from the original name
    
    
    # Start a local copy of the dataframe:
    DATASET = df.copy(deep = True)

    y = DATASET[column_to_transform]
    
    if (lambda_boxcox == 0):
        #ytransf = np.log(y), according to Box-Cox definition. Then
        #y_retransform = np.exp(y)
        #In the case of this function, ytransf is passed as the argument y.
        y_transform = np.exp(y)
    
    else:
        #apply Box-Cox function:
        #y_transf = (y**lmbda - 1) / lmbda. Then,
        #y_retransf ** (lmbda) = (y_transf * lmbda) + 1
        #y_retransf = ((y_transf * lmbda) + 1) ** (1/lmbda), where ** is the potentiation
        #In the case of this function, ytransf is passed as the argument y.
        y_transform = ((y * lambda_boxcox) + 1) ** (1/lambda_boxcox)
    
    if not (suffix is None):
        #only if a suffix was declared
        #concatenate the column name to the suffix
        new_col = column_to_transform + suffix
    
    else:
        #concatenate the column name to the standard '_ReversedBoxCox' suffix
        new_col = column_to_transform + '_ReversedBoxCox'
    
    DATASET[new_col] = y_transform
    #dataframe contendo os dados transformados
    
    print("Data successfully retransformed. Check the 10 first retransformed rows:\n")
    print(DATASET.head(10))
    print("\n") #line break
 
    return DATASET


def OneHotEncode_df (df, subset_of_features_to_be_encoded):

    import pandas as pd
    from sklearn.preprocessing import OneHotEncoder
    # https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html
    
    # df: the whole dataframe to be processed.
    
    # subset_of_features_to_be_encoded: list of strings (inside quotes), 
    # containing the names of the columns with the categorical variables that will be 
    # encoded. If a single column will be encoded, declare this parameter as list with
    # only one element e.g.subset_of_features_to_be_encoded = ["column1"] 
    # will analyze the column named as 'column1'; 
    # subset_of_features_to_be_encoded = ["col1", 'col2', 'col3'] will analyze 3 columns
    # with categorical variables: 'col1', 'col2', and 'col3'.
    
    #Start an encoding list empty (it will be a JSON object):
    encoding_list = []
    
    # Start a copy of the original dataframe. This copy will be updated to create the new
    # transformed dataframe. Then, we avoid manipulating the original object.
    new_df = df.copy(deep = True)
    
    #loop through each column of the subset:
    for column in subset_of_features_to_be_encoded:
        
        # Start two empty dictionaries:
        encoding_dict = {}
        nested_dict = {}
        
        # Add the column to encoding_dict as the key 'column':
        encoding_dict['column'] = column
        
        # Loop through each element (named 'column') of the list of columns to analyze,
        # subset_of_features_to_be_encoded
        
        # We could process the whole subset at once, but it could make us lose information
        # about the generated columns
        
        # set a subset of the dataframe X containing 'column' as the only column:
        # it will be equivalent to using .reshape(-1,1) to set a 1D-series
        # or array in the shape for scikit-learn:
        # For doing so, pass a list of columns for column filtering, containing
        # the object column as its single element:
        X  = df[[column]]
        
        #Start the OneHotEncoder object:
        OneHot_enc_obj = OneHotEncoder()
        
        #Fit the object to that column:
        OneHot_enc_obj = OneHot_enc_obj.fit(X)
        # Get the transformed columns as a SciPy sparse matrix: 
        transformed_columns = OneHot_enc_obj.transform(X)
        # Convert the sparse matrix to a NumPy dense array:
        transformed_columns = transformed_columns.toarray()
        
        # Now, let's retrieve the encoding information and save it:
        # Show encoded categories and store this array. 
        # It will give the proper columns' names:
        encoded_columns = OneHot_enc_obj.categories_

        # encoded_columns is an array containing a single element.
        # This element is an array like:
        # array(['cat1', 'cat2', 'cat3', 'cat4', 'cat5', 'cat6', 'cat7', 'cat8'], dtype=object)
        # Then, this array is the element of index 0 from the list encoded_columns.
        # It is represented as encoded_columns[0]

        # Therefore, we actually want the array which is named as encoded_columns[0]
        # Each element of this array is the name of one of the encoded columns. In the
        # example above, the element 'cat2' would be accessed as encoded_columns[0][1],
        # since it is the element of index [1] (second element) from the array 
        # encoded_columns[0].
        
        new_columns = encoded_columns[0]
        # To identify the column that originated these new columns, we can join the
        # string column to each element from new_columns:
        
        # Update the nested dictionary: store the new_columns as the key 'categories':
        nested_dict['categories'] = new_columns
        # Store the encoder object as the key 'OneHot_enc_obj'
        # Add the encoder object to the dictionary:
        nested_dict['OneHot_enc_obj'] = OneHot_enc_obj
        
        # Store the nested dictionary in the encoding_dict as the key 'OneHot_encoder':
        encoding_dict['OneHot_encoder'] = nested_dict
        # Append the encoding_dict as an element from list encoding_list:
        encoding_list.append(encoding_dict)
        
        # Now we saved all encoding information, let's transform the data:
        
        # Start a support_list to store the concatenated strings:
        support_list = []
        
        for encoded_col in new_columns:
            # Use the str attribute to guarantee that the array stores only strings.
            # Add an underscore "_" to separate the strings and an identifier of the transform:
            new_column = column + "_" + str(encoded_col) + "_OneHotEnc"
            # Append it to the support_list:
            support_list.append(new_column)
            
        # Convert the support list to NumPy array, and make new_columns the support list itself:
        new_columns = np.array(support_list)
        
        # Crete a Pandas dataframe from the array transformed_columns:
        encoded_X_df = pd.DataFrame(transformed_columns)
        
        # Modify the name of the columns to make it equal to new_columns:
        encoded_X_df.columns = new_columns
        
        #Inner join the new dataset with the encoded dataset.
        # Use the index as the key, since indices are necessarily correspondent.
        # To use join on index, we apply pandas .concat method.
        # To join on a specific key, we could use pandas .merge method with the arguments
        # left_on = 'left_key', right_on = 'right_key'; or, if the keys have same name,
        # on = 'key':
        # Check Pandas merge and concat documentation:
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.merge.html
        
        new_df = pd.concat([new_df, encoded_X_df], axis = 1, join = "inner")
        # When axis = 0, the .concat operation occurs in the row level, so the rows
        # of the second dataframe are added to the bottom of the first one.
        # It is the SQL union, and creates a dataframe with more rows, and
        # total of columns equals to the total of columns of the first dataframe
        # plus the columns of the second one that were not in the first dataframe.
        # When axis = 1, the operation occurs in the column level: the two
        # dataframes are laterally merged using the index as the key, 
        # preserving all columns from both dataframes. Therefore, the number of
        # rows will be the total of rows of the dataframe with more entries,
        # and the total of columns will be the sum of the total of columns of
        # the first dataframe with the total of columns of the second dataframe.
        
        print(f"Successfully encoded column \'{column}\' and merged the encoded columns to the dataframe.")
        print("Check first 5 rows of the encoded table that was merged:\n")
        print(encoded_X_df.head())
        # The default of the head method, when no parameter is printed, is to show 5 rows; if an
        # integer number Y is passed as argument .head(Y), Pandas shows the first Y-rows.
        print("\n")
        
    print("Finished One-Hot Encoding. Returning the new transformed dataframe; and an encoding list.\n")
    print("Each element from this list is a dictionary with the original column name as key \'column\', and a nested dictionary as the key \'OneHot_encoder\'.\n")
    print("In turns, the nested dictionary shows the different categories as key \'categories\' and the encoder object as the key \'OneHot_enc_obj\'.\n")
    print("Use the encoder object to inverse the One-Hot Encoding in the correspondent function.\n")
    print(f"For each category in the columns \'{subset_of_features_to_be_encoded}\', a new column has value 1, if it is the actual category of that row; or is 0 if not.\n")
    print("Check the first 10 rows of the new dataframe:\n")
    print(new_df.head(10))

    #return the transformed dataframe and the encoding dictionary:
    return new_df, encoding_list


def reverse_OneHotEncode (df, encoding_list):

    import pandas as pd
    from sklearn.preprocessing import OneHotEncoder
    # https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html
    
    # df: the whole dataframe to be processed.
    
    # encoding_list: list in the same format of the one generated by OneHotEncode_df function:
    # it must be a list of dictionaries where each dictionary contains two keys:
    # key 'column': string with the original column name (in quotes); 
    # key 'OneHot_encoder': this key must store a nested dictionary.
    # Even though the nested dictionaries generates by the encoding function present
    # two keys:  'categories', storing an array with the different categories;
    # and 'OneHot_enc_obj', storing the encoder object, only the key 'OneHot_enc_obj' is required.
    ## On the other hand, a third key is needed in the nested dictionary:
    ## key 'encoded_columns': this key must store a list or array with the names of the columns
    # obtained from Encoding.
    
    
    # Start a copy of the original dataframe. This copy will be updated to create the new
    # transformed dataframe. Then, we avoid manipulating the original object.
    new_df = df.copy(deep = True)
    
    for encoder_dict in encoding_list:
        
        try:
            # Check if the required arguments are present:
            if ((encoder_dict['column'] is not None) & (encoder_dict['OneHot_encoder']['OneHot_enc_obj'] is not None) & (encoder_dict['OneHot_encoder']['encoded_columns'] is not None)):

                # Access the column name:
                col_name = encoder_dict['column']

                # Access the nested dictionary:
                nested_dict = encoder_dict['OneHot_encoder']
                # Access the encoder object on the dictionary
                OneHot_enc_obj = nested_dict['OneHot_enc_obj']
                # Access the list of encoded columns:
                list_of_encoded_cols = list(nested_dict['encoded_columns'])

                # Get a subset of the encoded columns
                X = new_df.copy(deep = True)
                X = X[list_of_encoded_cols]

                # Reverse the encoding:
                reversed_array = OneHot_enc_obj.inverse_transform(X)

                # Add the reversed array as the column col_name on the dataframe:
                new_df[col_name] = reversed_array
                
                print(f"Reversed the encoding for {col_name}. Check the 5 first rows of the re-transformed series:\n")
                print(new_df[[col_name]].head())
                print("\n")
            
        except:
            print("Detected dictionary with incorrect keys or format. Unable to reverse encoding. Please, correct it.\n")
    
    print("Finished reversing One-Hot Encoding. Returning the new transformed dataframe.")
    print("Check the first 10 rows of the new dataframe:\n")
    print(new_df.head(10))

    #return the transformed dataframe:
    return new_df


def OrdinalEncode_df (df, subset_of_features_to_be_encoded):

    # Ordinal encoding: let's associate integer sequential numbers to the categorical column
    # to apply the advanced encoding techniques. Even though the one-hot encoding could perform
    # the same task and would, in fact, better, since there may be no ordering relation, the
    # ordinal encoding is simpler and more suitable for this particular task:    
    
    import pandas as pd
    from sklearn.preprocessing import OrdinalEncoder
    # https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OrdinalEncoder.html#sklearn.preprocessing.OrdinalEncoder 
    
    # df: the whole dataframe to be processed.
    
    # subset_of_features_to_be_encoded: list of strings (inside quotes), 
    # containing the names of the columns with the categorical variables that will be 
    # encoded. If a single column will be encoded, declare this parameter as list with
    # only one element e.g.subset_of_features_to_be_encoded = ["column1"] 
    # will analyze the column named as 'column1'; 
    # subset_of_features_to_be_encoded = ["col1", 'col2', 'col3'] will analyze 3 columns
    # with categorical variables: 'col1', 'col2', and 'col3'.
    
    #Start an encoding list empty (it will be a JSON object):
    encoding_list = []
    
    # Start a copy of the original dataframe. This copy will be updated to create the new
    # transformed dataframe. Then, we avoid manipulating the original object.
    new_df = df.copy(deep = True)
   
    #loop through each column of the subset:
    for column in subset_of_features_to_be_encoded:
        
        # Start two empty dictionaries:
        encoding_dict = {}
        nested_dict = {}
        
        # Add the column to encoding_dict as the key 'column':
        encoding_dict['column'] = column
        
        # Loop through each element (named 'column') of the list of columns to analyze,
        # subset_of_features_to_be_encoded
        
        # We could process the whole subset at once, but it could make us lose information
        # about the generated columns
        
        # set a subset of the dataframe X containing 'column' as the only column:
        # it will be equivalent to using .reshape(-1,1) to set a 1D-series
        # or array in the shape for scikit-learn:
        # For doing so, pass a list of columns for column filtering, containing
        # the object column as its single element:
        X  = new_df[[column]]
        
        #Start the OrdinalEncoder object:
        ordinal_enc_obj = OrdinalEncoder()
        
        # Fit the ordinal encoder to the dataframe X:
        ordinal_enc_obj = ordinal_enc_obj.fit(X)
        # Get the transformed dataframe X: 
        transformed_X = ordinal_enc_obj.transform(X)
        # transformed_X is an array of arrays like: [[0.], [0.], ..., [8.]]
        # We want all the values in the first position of the internal arrays:
        transformed_X = transformed_X[:,0]
        # Get the encoded series as a NumPy array:
        encoded_series = np.array(transformed_X)
        
        # Get a name for the new encoded column:
        new_column = column + "_OrdinalEnc"
        # Add this column to the dataframe:
        new_df[new_column] = encoded_series
        
        # Now, let's retrieve the encoding information and save it:
        # Show encoded categories and store this array. 
        # It will give the proper columns' names:
        encoded_categories = ordinal_enc_obj.categories_

        # encoded_categories is an array of strings containing the information of
        # encoded categories and their values.
        
        # Update the nested dictionary: store the categories as the key 'categories':
        nested_dict['categories'] = encoded_categories
        # Store the encoder object as the key 'ordinal_enc_obj'
        # Add the encoder object to the dictionary:
        nested_dict['ordinal_enc_obj'] = ordinal_enc_obj
        
        # Store the nested dictionary in the encoding_dict as the key 'ordinal_encoder':
        encoding_dict['ordinal_encoder'] = nested_dict
        # Append the encoding_dict as an element from list encoding_list:
        encoding_list.append(encoding_dict)
        
        print(f"Successfully encoded column \'{column}\' and added the encoded column to the dataframe.")
        print("Check first 5 rows of the encoded series that was merged:\n")
        print(new_df[[new_column]].head())
        # The default of the head method, when no parameter is printed, is to show 5 rows; if an
        # integer number Y is passed as argument .head(Y), Pandas shows the first Y-rows.
        print("\n")
        
    print("Finished Ordinal Encoding. Returning the new transformed dataframe; and an encoding list.\n")
    print("Each element from this list is a dictionary with the original column name as key \'column\', and a nested dictionary as the key \'ordinal_encoder\'.\n")
    print("In turns, the nested dictionary shows the different categories as key \'categories\' and the encoder object as the key \'ordinal_enc_obj\'.\n")
    print("Use the encoder object to inverse the Ordinal Encoding in the correspondent function.\n")
    print("Check the first 10 rows of the new dataframe:\n")
    print(new_df.head(10))

    #return the transformed dataframe and the encoding dictionary:
    return new_df, encoding_list


def reverse_OrdinalEncode (df, encoding_list):

    import pandas as pd
    from sklearn.preprocessing import OrdinalEncoder
    # https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OrdinalEncoder.html#sklearn.preprocessing.OrdinalEncoder
    
    # df: the whole dataframe to be processed.
    
    # encoding_list: list in the same format of the one generated by OrdinalEncode_df function:
    # it must be a list of dictionaries where each dictionary contains two keys:
    # key 'column': string with the original column name (in quotes); 
    # key 'ordinal_encoder': this key must store a nested dictionary.
    # Even though the nested dictionaries generates by the encoding function present
    # two keys:  'categories', storing an array with the different categories;
    # and 'ordinal_enc_obj', storing the encoder object, only the key 'ordinal_enc_obj' is required.
    ## On the other hand, a third key is needed in the nested dictionary:
    ## key 'encoded_column': this key must store a string with the name of the column
    # obtained from Encoding.
    
    
    # Start a copy of the original dataframe. This copy will be updated to create the new
    # transformed dataframe. Then, we avoid manipulating the original object.
    new_df = df.copy(deep = True)
    
    for encoder_dict in encoding_list:
        
        try:
            # Check if the required arguments are present:
            if ((encoder_dict['column'] is not None) & (encoder_dict['ordinal_encoder']['ordinal_enc_obj'] is not None) & (encoder_dict['ordinal_encoder']['encoded_column'] is not None)):

                # Access the column name:
                col_name = encoder_dict['column']

                # Access the nested dictionary:
                nested_dict = encoder_dict['ordinal_encoder']
                # Access the encoder object on the dictionary
                ordinal_enc_obj = nested_dict['ordinal_enc_obj']
                # Access the encoded column and save it as a list:
                list_of_encoded_cols = [nested_dict['encoded_column']]
                # In OneHotEncoding we have an array of strings. Applying the list
                # attribute would convert the array to list. Here, in turns, we have a simple
                # string, which is also an iterable object. Applying the list attribute to a string
                # creates a list of characters of that string.
                # So, here we create a list with the string as its single element.

                # Get a subset of the encoded column
                X = new_df.copy(deep = True)
                X = X[list_of_encoded_cols]

                # Reverse the encoding:
                reversed_array = ordinal_enc_obj.inverse_transform(X)

                # Add the reversed array as the column col_name on the dataframe:
                new_df[col_name] = reversed_array
                    
                print(f"Reversed the encoding for {col_name}. Check the 5 first rows of the re-transformed series:\n")
                print(new_df[[col_name]].head())
                print("\n")
                   
        except:
            print("Detected dictionary with incorrect keys or format. Unable to reverse encoding. Please, correct it.\n")
    
    
    print("Finished reversing Ordinal Encoding. Returning the new transformed dataframe.")
    print("Check the first 10 rows of the new dataframe:\n")
    print(new_df.head(10))

    #return the transformed dataframe:
    return new_df


def feature_scaling (df, subset_of_features_to_scale, mode = 'min_max', scale_with_new_params = True, list_of_scaling_params = None, suffix = '_scaled'):
    
    import numpy as np
    import pandas as pd
    from sklearn.preprocessing import StandardScaler
    from sklearn.preprocessing import MinMaxScaler
    # Scikit-learn Preprocessing data guide:
    # https://scikit-learn.org/stable/modules/preprocessing.html#preprocessing-scaler
    # Standard scaler documentation:
    # https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html
    # Min-Max scaler documentation:
    # https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html#sklearn.preprocessing.MinMaxScaler.set_params
    
    ## Machine Learning algorithms are extremely sensitive to scale. 
    
    ## This function provides 4 methods (modes) of scaling:
    ## mode = 'standard': applies the standard scaling, 
    ##  which creates a new variable with mean = 0; and standard deviation = 1.
    ##  Each value Y is transformed as Ytransf = (Y - u)/s, where u is the mean 
    ##  of the training samples, and s is the standard deviation of the training samples.
    
    ## mode = 'min_max': applies min-max normalization, with a resultant feature 
    ## ranging from 0 to 1. each value Y is transformed as 
    ## Ytransf = (Y - Ymin)/(Ymax - Ymin), where Ymin and Ymax are the minimum and 
    ## maximum values of Y, respectively.
    
    ## mode = 'factor': divides the whole series by a numeric value provided as argument. 
    ## For a factor F, the new Y values will be Ytransf = Y/F.
    
    ## mode = 'normalize_by_maximum' is similar to mode = 'factor', but the factor will be selected
    # as the maximum value. This mode is available only for scale_with_new_params = True. If
    # scale_with_new_params = False, you should provide the value of the maximum as a division 'factor'.
    
    # df: the whole dataframe to be processed.
    
    # subset_of_features_to_be_scaled: list of strings (inside quotes), 
    # containing the names of the columns with the categorical variables that will be 
    # encoded. If a single column will be encoded, declare this parameter as list with
    # only one element e.g.subset_of_features_to_be_scaled = ["column1"] 
    # will analyze the column named as 'column1'; 
    # subset_of_features_to_be_scaled = ["col1", 'col2', 'col3'] will analyze 3 columns
    # with categorical variables: 'col1', 'col2', and 'col3'.
    
    # scale_with_new_params = True
    # Alternatively, set scale_with_new_params = True if you want to calculate a new
    # scaler for the data; or set scale_with_new_params = False if you want to apply 
    # parameters previously obtained to the data (i.e., if you want to apply the scaler
    # previously trained to another set of data; or wants to simply apply again the same
    # scaler).
    
    # list_of_scaling_params:
    # This variable has effect only when SCALE_WITH_NEW_PARAMS = False
    ## WARNING: The mode 'factor' demmands the input of the list of factors that will be 
    # used for normalizing each column. Therefore, it can be used only 
    # when scale_with_new_params = False.
    
    # list_of_scaling_params is a list of dictionaries with the same format of the list returned
    # from this function. Each dictionary must correspond to one of the features that will be scaled,
    # but the list do not have to be in the same order of the columns - it will check one of the
    # dictionary keys.
    # The first key of the dictionary must be 'column'. This key must store a string with the exact
    # name of the column that will be scaled.
    # the second key must be 'scaler'. This key must store a dictionary. The dictionary must store
    # one of two keys: 'scaler_obj' - sklearn scaler object to be used; or 'scaler_details' - the
    # numeric parameters for re-calculating the scaler without the object. The key 'scaler_details', 
    # must contain a nested dictionary. For the mode 'min_max', this dictionary should contain 
    # two keys: 'min', with the minimum value of the variable, and 'max', with the maximum value. 
    # For mode 'standard', the keys should be 'mu', with the mean value, and 'sigma', with its 
    # standard deviation. For the mode 'factor', the key should be 'factor', and should contain the 
    # factor for division (the scaling value. e.g 'factor': 2.0 will divide the column by 2.0.).
    # Again, if you want to normalize by the maximum, declare the maximum value as any other factor for
    # division.
    # The key 'scaler_details' will not create an object: the transform will be directly performed 
    # through vectorial operations.
    
    # suffix: string (inside quotes).
    # How the transformed column will be identified in the returned data_transformed_df.
    # If y_label = 'Y' and suffix = '_scaled', the transformed column will be
    # identified as '_scaled'.
    # Alternatively, input inside quotes a string with the desired suffix. Recommendation:
    # start the suffix with "_" to separate it from the original name
      
    if (suffix is None):
        #set as the default
        suffix = '_scaled'
    
    #Start a copy of the original dataframe. This copy will be updated to create the new
    # transformed dataframe. Then, we avoid manipulating the original object.
    new_df = df.copy(deep = True)
    
    #Start an scaling list empty (it will be a JSON object):
    scaling_list = []
    
    for column in subset_of_features_to_scale:
        
        # Create a dataframe X by subsetting only the analyzed column
        # it will be equivalent to using .reshape(-1,1) to set a 1D-series
        # or array in the shape for scikit-learn:
        # For doing so, pass a list of columns for column filtering, containing
        # the object column as its single element:
        X = new_df[[column]]
        
        if (scale_with_new_params == False):
            
            # Use a previously obtained scaler.
            # Loop through each element of the list:
            
            for scaling_dict in list_of_scaling_params:
                
                # check if the dictionary is from that column:
                if (scaling_dict['column'] == column):
                    
                    # We found the correct dictionary. Let's retrieve the information:
                    # retrieve the nested dictionary:
                    nested_dict = scaling_dict['scaler']
                    
                    # try accessing the scaler object:
                    try:
                        scaler = nested_dict['scaler_obj']
                        #calculate the scaled feature, and store it as new array:
                        scaled_feature = scaler.transform(X)
                        
                        # Add the parameters to the nested dictionary:
                        nested_dict['scaling_params'] = scaler.get_params(deep = True)
                        
                        if (mode == 'standard'):
                            
                            nested_dict['scaler_details'] = {
                                'mu': X[column].mean(),
                                'sigma': X[column].std()
                            }
                        
                        elif (mode == 'min_max'):
                            
                            nested_dict['scaler_details'] = {
                                'min': X[column].min(),
                                'max': X[column].max()
                            }
                    
                    except:
                        
                        try:
                            # As last alternative, let's try accessing the scaler details dict
                            scaler_details = nested_dict['scaler_details']
                                
                            if (mode == 'standard'):
                                
                                nested_dict['scaling_params'] = 'standard_scaler_manually_defined'
                                mu = scaler_details['mu']
                                sigma = scaler_details['sigma']
                                    
                                if (sigma != 0):
                                    scaled_feature = (X - mu)/sigma
                                else:
                                    scaled_feature = (X - mu)
                                
                            elif (mode == 'min_max'):
                                    
                                nested_dict['scaling_params'] = 'min_max_scaler_manually_defined'
                                minimum = scaler_details['min']
                                maximum = scaler_details['max']
                                    
                                if ((maximum - minimum) != 0):
                                    scaled_feature = (X - minimum)/(maximum - minimum)
                                else:
                                    scaled_feature = X/maximum
                                
                            elif (mode == 'factor'):
                                
                                nested_dict['scaling_params'] = 'normalization_by_factor'
                                factor = scaler_details['factor']
                                scaled_feature = X/(factor)
                                
                            else:
                                print("Select a valid mode: standard, min_max, or factor.\n")
                                return "error", "error"
                            
                        except:
                                
                            print(f"No valid scaling dictionary was input for column {column}.\n")
                            return "error", "error"
            
        elif (mode == 'normalize_by_maximum'):
            
            #Start an scaling dictionary empty:
            scaling_dict = {}

            # add the column to the scaling dictionary:
            scaling_dict['column'] = column

            # Start a nested dictionary:
            nested_dict = {}
            
            factor = X[column].max()
            scaled_feature = X/(factor)
            nested_dict['scaling_params'] = 'normalization_by_factor'
            nested_dict['scaler_details'] = {'factor': factor, 'description': 'division_by_maximum_detected_value'}
    
        else:
            # Create a new scaler:
            
            #Start an scaling dictionary empty:
            scaling_dict = {}

            # add the column to the scaling dictionary:
            scaling_dict['column'] = column
            
            # Start a nested dictionary:
            nested_dict = {}
                
            #start the scaler object:
            if (mode == 'standard'):
                
                scaler = StandardScaler()
                scaler_details = {'mu': X[column].mean(), 'sigma': X[column].std()}

            elif (mode == 'min_max'):
                
                scaler = MinMaxScaler()
                scaler_details = {'min': X[column].min(), 'max': X[column].max()}
                
            # fit the scaler to the column
            scaler = scaler.fit(X)
                    
            # calculate the scaled feature, and store it as new array:
            scaled_feature = scaler.transform(X)
            # scaler.inverse_transform(X) would reverse the scaling.
                
            # Get the scaling parameters for that column:
            scaling_params = scaler.get_params(deep = True)
                    
            # scaling_params is a dictionary containing the scaling parameters.
            # Add the scaling parameters to the nested dictionary:
            nested_dict['scaling_params'] = scaling_params
                
            # add the scaler object to the nested dictionary:
            nested_dict['scaler_obj'] = scaler
            
            # Add the scaler_details dictionary:
            nested_dict['scaler_details'] = scaler_details
            
            # Now, all steps are the same for all cases, so we can go back to the main
            # for loop:
    
        # Create the new_column name:
        new_column = column + suffix
        # Create the new_column by dividing the previous column by the scaling factor:
                    
        # Set the new column as scaled_feature
        new_df[new_column] = scaled_feature
                
        # Add the nested dictionary to the scaling_dict:
        scaling_dict['scaler'] = nested_dict
                
        # Finally, append the scaling_dict to the list scaling_list:
        scaling_list.append(scaling_dict)
                    
        print(f"Successfully scaled column {column}.")
                
    print("Successfully scaled the dataframe. Returning the transformed dataframe and the scaling dictionary.")
    print("Check 10 first rows of the new dataframe:\n")
    print(new_df.head(10))
                
    return new_df, scaling_list


def reverse_feature_scaling (df, subset_of_features_to_scale, list_of_scaling_params, mode = 'min_max', suffix = '_reverseScaling'):
    
    import pandas as pd
    from sklearn.preprocessing import StandardScaler
    from sklearn.preprocessing import MinMaxScaler
    # Scikit-learn Preprocessing data guide:
    # https://scikit-learn.org/stable/modules/preprocessing.html#preprocessing-scaler
    # Standard scaler documentation:
    # https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html
    # Min-Max scaler documentation:
    # https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html#sklearn.preprocessing.MinMaxScaler.set_params
    
    ## mode = 'standard': reverses the standard scaling, 
    ##  which creates a new variable with mean = 0; and standard deviation = 1.
    ##  Each value Y is transformed as Ytransf = (Y - u)/s, where u is the mean 
    ##  of the training samples, and s is the standard deviation of the training samples.
    
    ## mode = 'min_max': reverses min-max normalization, with a resultant feature 
    ## ranging from 0 to 1. each value Y is transformed as 
    ## Ytransf = (Y - Ymin)/(Ymax - Ymin), where Ymin and Ymax are the minimum and 
    ## maximum values of Y, respectively.
    ## mode = 'factor': reverses the division of the whole series by a numeric value 
    # provided as argument. 
    ## For a factor F, the new Y transformed values are Ytransf = Y/F.
    # Notice that if the original mode was 'normalize_by_maximum', then the maximum value used
    # must be declared as any other factor.
    
    # df: the whole dataframe to be processed.
    
    # subset_of_features_to_be_scaled: list of strings (inside quotes), 
    # containing the names of the columns with the categorical variables that will be 
    # encoded. If a single column will be encoded, declare this parameter as list with
    # only one element e.g.subset_of_features_to_be_scaled = ["column1"] 
    # will analyze the column named as 'column1'; 
    # subset_of_features_to_be_scaled = ["col1", 'col2', 'col3'] will analyze 3 columns
    # with categorical variables: 'col1', 'col2', and 'col3'.
    
    # list_of_scaling_params is a list of dictionaries with the same format of the list returned
    # from this function. Each dictionary must correspond to one of the features that will be scaled,
    # but the list do not have to be in the same order of the columns - it will check one of the
    # dictionary keys.
    # The first key of the dictionary must be 'column'. This key must store a string with the exact
    # name of the column that will be scaled.
    # the second key must be 'scaler'. This key must store a dictionary. The dictionary must store
    # one of two keys: 'scaler_obj' - sklearn scaler object to be used; or 'scaler_details' - the
    # numeric parameters for re-calculating the scaler without the object. The key 'scaler_details', 
    # must contain a nested dictionary. For the mode 'min_max', this dictionary should contain 
    # two keys: 'min', with the minimum value of the variable, and 'max', with the maximum value. 
    # For mode 'standard', the keys should be 'mu', with the mean value, and 'sigma', with its 
    # standard deviation. For the mode 'factor', the key should be 'factor', and should contain the 
    # factor for division (the scaling value. e.g 'factor': 2.0 will divide the column by 2.0.).
    # Again, if you want to normalize by the maximum, declare the maximum value as any other factor for
    # division.
    # The key 'scaler_details' will not create an object: the transform will be directly performed 
    # through vectorial operations.
    
    # suffix: string (inside quotes).
    # How the transformed column will be identified in the returned data_transformed_df.
    # If y_label = 'Y' and suffix = '_reverseScaling', the transformed column will be
    # identified as '_reverseScaling'.
    # Alternatively, input inside quotes a string with the desired suffix. Recommendation:
    # start the suffix with "_" to separate it from the original name
      
    if (suffix is None):
        #set as the default
        suffix = '_reverseScaling'
    
    #Start a copy of the original dataframe. This copy will be updated to create the new
    # transformed dataframe. Then, we avoid manipulating the original object.
    new_df = df.copy(deep = True)
    
    #Start an scaling list empty (it will be a JSON object):
    scaling_list = []
    
    # Use a previously obtained scaler:
    
    for column in subset_of_features_to_scale:
        
        # Create a dataframe X by subsetting only the analyzed column
        # it will be equivalent to using .reshape(-1,1) to set a 1D-series
        # or array in the shape for scikit-learn:
        # For doing so, pass a list of columns for column filtering, containing
        # the object column as its single element:
        X = new_df[[column]]

        # Loop through each element of the list:
            
        for scaling_dict in list_of_scaling_params:
                
            # check if the dictionary is from that column:
            if (scaling_dict['column'] == column):
                    
                # We found the correct dictionary. Let's retrieve the information:
                # retrieve the nested dictionary:
                nested_dict = scaling_dict['scaler']
                    
                # try accessing the scaler object:
                try:
                    scaler = nested_dict['scaler_obj']
                    #calculate the reversed scaled feature, and store it as new array:
                    rev_scaled_feature = scaler.inverse_transform(X)
                        
                    # Add the parameters to the nested dictionary:
                    nested_dict['scaling_params'] = scaler.get_params(deep = True)
                        
                    if (mode == 'standard'):
                            
                        nested_dict['scaler_details'] = {
                                'mu': rev_scaled_feature.mean(),
                                'sigma': rev_scaled_feature.std()
                            }
                        
                    elif (mode == 'min_max'):
                            
                        nested_dict['scaler_details'] = {
                                'min': rev_scaled_feature.min(),
                                'max': rev_scaled_feature.max()
                            }
                    
                except:
                        
                    try:
                        # As last alternative, let's try accessing the scaler details dict
                        scaler_details = nested_dict['scaler_details']
                                
                        if (mode == 'standard'):
                                
                            nested_dict['scaling_params'] = 'standard_scaler_manually_defined'
                            mu = scaler_details['mu']
                            sigma = scaler_details['sigma']
                                    
                            if (sigma != 0):
                                # scaled_feature = (X - mu)/sigma
                                rev_scaled_feature = (X * sigma) + mu
                            else:
                                # scaled_feature = (X - mu)
                                rev_scaled_feature = (X + mu)
                                
                        elif (mode == 'min_max'):
                                    
                            nested_dict['scaling_params'] = 'min_max_scaler_manually_defined'
                            minimum = scaler_details['min']
                            maximum = scaler_details['max']
                                    
                            if ((maximum - minimum) != 0):
                                # scaled_feature = (X - minimum)/(maximum - minimum)
                                rev_scaled_feature = (X * (maximum - minimum)) + minimum
                            else:
                                # scaled_feature = X/maximum
                                rev_scaled_feature = (X * maximum)
                                
                        elif (mode == 'factor'):
                                
                            nested_dict['scaling_params'] = 'normalization_by_factor'
                            factor = scaler_details['factor']
                            # scaled_feature = X/(factor)
                            rev_scaled_feature = (X * factor)
                                
                        else:
                            print("Select a valid mode: standard, min_max, or factor.\n")
                            return "error", "error"
                            
                    except:
                                
                        print(f"No valid scaling dictionary was input for column {column}.\n")
                        return "error", "error"
         
                # Create the new_column name:
                new_column = column + suffix
                # Create the new_column by dividing the previous column by the scaling factor:

                # Set the new column as rev_scaled_feature
                new_df[new_column] = rev_scaled_feature

                # Add the nested dictionary to the scaling_dict:
                scaling_dict['scaler'] = nested_dict

                # Finally, append the scaling_dict to the list scaling_list:
                scaling_list.append(scaling_dict)

                print(f"Successfully re-scaled column {column}.")
                
    print("Successfully re-scaled the dataframe.")
    print("Check 10 first rows of the new dataframe:\n")
    print(new_df.head(10))
                
    return new_df, scaling_list


def import_export_model_list_dict (action = 'import', objects_manipulated = 'model_only', model_file_name = None, dictionary_or_list_file_name = None, directory_path = '', model_type = 'keras', dict_or_list_to_export = None, model_to_export = None, use_colab_memory = False):
    
    import os
    import pickle as pkl
    import dill
    import tensorflow as tf
    from statsmodels.tsa.arima.model import ARIMA, ARIMAResults
    from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler, MinMaxScaler
    from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, LogisticRegression
    from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
    from sklearn.neural_network import MLPRegressor, MLPClassifier
    from xgboost import XGBRegressor, XGBClassifier
    
    # action = 'import' for importing a model and/or a dictionary;
    # action = 'export' for exporting a model and/or a dictionary.
    
    # objects_manipulated = 'model_only' if only a model will be manipulated.
    # objects_manipulated = 'dict_or_list_only' if only a dictionary or list will be manipulated.
    # objects_manipulated = 'model_and_dict' if both a model and a dictionary will be
    # manipulated.
    
    # model_file_name: string with the name of the file containing the model (for 'import');
    # or of the name that the exported file will have (for 'export')
    # e.g. model_file_name = 'model'
    # WARNING: Do not add the file extension.
    # Keep it in quotes. Keep model_file_name = None if no model will be manipulated.
    
    # dictionary_or_list_file_name: string with the name of the file containing the dictionary 
    # (for 'import');
    # or of the name that the exported file will have (for 'export')
    # e.g. dictionary_or_list_file_name = 'history_dict'
    # WARNING: Do not add the file extension.
    # Keep it in quotes. Keep dictionary_or_list_file_name = None if no 
    # dictionary or list will be manipulated.
    
    # DIRECTORY_PATH: path of the directory where the model will be saved,
    # or from which the model will be retrieved. If no value is provided,
    # the DIRECTORY_PATH will be the root: "/"
    # Notice that the model and the dictionary must be stored in the same path.
    # If a model and a dictionary will be exported, they will be stored in the same
    # DIRECTORY_PATH.
    
    # model_type: This parameter has effect only when a model will be manipulated.
    # model_type: 'keras' for deep learning keras/ tensorflow models with extension .h5
    # model_type = 'sklearn' for models from scikit-learn (non-deep learning)
    # model_type = 'xgb_regressor' for XGBoost regression models (non-deep learning)
    # model_type = 'xgb_classifier' for XGBoost classification models (non-deep learning)
    # model_type = 'arima' for ARIMA model (Statsmodels)
    
    # dict_or_list_to_export and model_to_export: 
    # These two parameters have effect only when ACTION == 'export'. In this case, they
    # must be declared. If ACTION == 'export', keep:
    # dict_or_list_to_export = None, 
    # model_to_export = None
    # If one of these objects will be exported, substitute None by the name of the object
    # e.g. if your model is stored in the global memory as 'keras_model' declare:
    # model_to_export = keras_model. Notice that it must be declared without quotes, since
    # it is not a string, but an object.
    # For exporting a dictionary named as 'dict':
    # dict_or_list_to_export = dict
    
    # use_colab_memory: this parameter has only effect when using Google Colab (or it will
    # raise an error). Set as use_colab_memory = True if you want to use the instant memory
    # from Google Colaboratory: you will update or download the file and it will be available
    # only during the time when the kernel is running. It will be excluded when the kernel
    # dies, for instance, when you close the notebook.
    
    # If action == 'export' and use_colab_memory == True, then the file will be downloaded
    # to your computer (running the cell will start the download).
    
    # Check the directory path
    if (directory_path is None):
        # set as the root (empty string):
        directory_path = ""
        
        
    bool_check1 = (objects_manipulated != 'model_only')
    # bool_check1 == True if a dictionary will be manipulated
    
    bool_check2 = (objects_manipulated != 'dict_or_list_only')
    # bool_check1 == True if a dictionary will be manipulated
    
    if (bool_check1 == True):
        #manipulate a dictionary
        
        if (dictionary_or_list_file_name is None):
            print("Please, enter a name for the dictionary or list.")
            return "error1"
        
        else:
            # Create the file path for the dictionary:
            dict_path = os.path.join(directory_path, dictionary_or_list_file_name)
            # Extract the file extension
            dict_extension = 'pkl'
            #concatenate:
            dict_path = dict_path + "." + dict_extension
            
    
    if (bool_check2 == True):
        #manipulate a model
        
        if (model_file_name is None):
            print("Please, enter a name for the model.")
            return "error1"
        
        else:
            # Create the file path for the dictionary:
            model_path = os.path.join(directory_path, model_file_name)
            # Extract the file extension
            
            #check model_type:
            if (model_type == 'keras'):
                model_extension = 'h5'
            
            elif (model_type == 'sklearn'):
                model_extension = 'dill'
                #it could be 'pkl', though
            
            elif (model_type == 'xgb_regressor'):
                model_extension = 'json'
                #it could be 'ubj', though
            
            elif (model_type == 'xgb_classifier'):
                model_extension = 'json'
                #it could be 'ubj', though
            
            elif (model_type == 'arima'):
                model_extension = 'pkl'
            
            else:
                print("Enter a valid model_type: keras, sklearn_xgb, or arima.")
                return "error2"
            
            #concatenate:
            model_path = model_path +  "." + model_extension
            
    # Now we have the full paths for the dictionary and for the model.
    
    if (action == 'import'):
        
        if (use_colab_memory == True):
             
            from google.colab import files
            # google.colab library must be imported only in case 
            # it is going to be used, for avoiding 
            # AWS compatibility issues.
            
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
        
        if (bool_check1 == True):
            #manipulate a dictionary
            if (use_colab_memory == True):
                key = dictionary_file_name + "." + dict_extension
                #Use the key to access the file content, and pass the file content
                # to pickle:
                with open(colab_files_dict[key], 'rb') as opened_file:
            
                    imported_dict = pkl.load(opened_file)
                    # The structure imported_dict = pkl.load(open(colab_files_dict[key], 'rb')) relies 
                    # on the GC to close the file. That's not a good idea: If someone doesn't use 
                    # CPython the garbage collector might not be using refcounting (which collects 
                    # unreferenced objects immediately) but e.g. collect garbage only after some time.
                    # Since file handles are closed when the associated object is garbage collected or 
                    # closed explicitly (.close() or .__exit__() from a context manager) the file 
                    # will remain open until the GC kicks in.
                    # Using 'with' ensures the file is closed as soon as the block is left - even if 
                    # an exception happens inside that block, so it should always be preferred for any 
                    # real application.
                    # source: https://stackoverflow.com/questions/39447362/equivalent-ways-to-json-load-a-file-in-python

                print(f"Dictionary or list {key} successfully imported to Colab environment.")
            
            else:
                #standard method
                with open(dict_path, 'rb') as opened_file:
            
                    imported_dict = pkl.load(opened_file)
                
                # 'rb' stands for read binary (read mode). For writing mode, 'wb', 'write binary'
                print(f"Dictionary or list successfully imported from {dict_path}.")
                
        if (bool_check2 == True):
            #manipulate a model
            # select the proper model
        
            if (model_type == 'keras'):
                
                if (use_colab_memory == True):
                    key = model_file_name + "." + model_extension
                    model = tf.keras.models.load_model(colab_files_dict[key])
                    print(f"Keras/TensorFlow model: {key} successfully imported to Colab environment.")
            
                else:
                    #standard method
                    # We previously declared:
                    # from keras.models import load_model
                    model = tf.keras.models.load_model(model_path)
                    print(f"Keras/TensorFlow model successfully imported from {model_path}.")

            elif (model_type == 'sklearn'):
                
                if (use_colab_memory == True):
                    key = model_file_name + "." + model_extension
                    
                    with open(colab_files_dict[key], 'rb') as opened_file:
            
                        model = dill.load(opened_file)
                    
                    print(f"Scikit-learn model: {key} successfully imported to Colab environment.")
            
                else:
                    #standard method
                    with open(model_path, 'rb') as opened_file:
            
                        model = dill.load(opened_file)
                
                    print(f"Scikit-learn model successfully imported from {model_path}.")
                    # For loading a pickle model:
                    ## model = pkl.load(open(model_path, 'rb'))
                    # 'rb' stands for read binary (read mode). For writing mode, 'wb', 'write binary'

            elif (model_type == 'xgb_regressor'):
                
                # Create an instance (object) from the class XGBRegressor:
                
                model = XGBRegressor()
                # Now we can apply the load_model method from this class:
                
                if (use_colab_memory == True):
                    key = model_file_name + "." + model_extension
                    model = model.load_model(colab_files_dict[key])
                    print(f"XGBoost regression model: {key} successfully imported to Colab environment.")
            
                else:
                    #standard method
                    model = model.load_model(model_path)
                    print(f"XGBoost regression model successfully imported from {model_path}.")
                    # model.load_model("model.json") or model.load_model("model.ubj")
                    # .load_model is a method from xgboost object
            
            elif (model_type == 'xgb_classifier'):

                # Create an instance (object) from the class XGBClassifier:

                model = XGBClassifier()
                # Now we can apply the load_model method from this class:
                
                if (use_colab_memory == True):
                    key = model_file_name + "." + model_extension
                    model = model.load_model(colab_files_dict[key])
                    print(f"XGBoost classification model: {key} successfully imported to Colab environment.")
            
                else:
                    #standard method
                    model = model.load_model(model_path)
                    print(f"XGBoost classification model successfully imported from {model_path}.")
                    # model.load_model("model.json") or model.load_model("model.ubj")
                    # .load_model is a method from xgboost object

            elif (model_type == 'arima'):
                
                if (use_colab_memory == True):
                    key = model_file_name + "." + model_extension
                    model = ARIMAResults.load(colab_files_dict[key])
                    print(f"ARIMA model: {key} successfully imported to Colab environment.")
            
                else:
                    #standard method
                    # We previously declared:
                    # from statsmodels.tsa.arima.model import ARIMAResults
                    model = ARIMAResults.load(model_path)
                    print(f"ARIMA model successfully imported from {model_path}.")
            
            if (objects_manipulated == 'model_only'):
                # only the model should be returned
                return model
            
            elif (objects_manipulated == 'dict_only'):
                # only the dictionary should be returned:
                return imported_dict
            
            else:
                # Both objects are returned:
                return model, imported_dict

    
    elif (action == 'export'):
        
        #Let's export the models or dictionary:
        if (use_colab_memory == True):
            
            from google.colab import files
            # google.colab library must be imported only in case 
            # it is going to be used, for avoiding 
            # AWS compatibility issues.
            
            print("The files will be downloaded to your computer.")
        
        if (bool_check1 == True):
            #manipulate a dictionary
            if (use_colab_memory == True):
                ## Download the dictionary
                key = dictionary_or_list_file_name + "." + dict_extension
                
                with open(key, 'wb') as opened_file:
            
                    pkl.dump(dict_or_list_to_export, opened_file)
                
                # this functionality requires the previous declaration:
                ## from google.colab import files
                files.download(key)
                
                print(f"Dictionary or list {key} successfully downloaded from Colab environment.")
            
            else:
                #standard method 
                with open(dict_path, 'wb') as opened_file:
            
                    pkl.dump(dict_or_list_to_export, opened_file)
                
                #to save the file, the mode must be set as 'wb' (write binary)
                print(f"Dictionary or list successfully exported as {dict_path}.")
                
        if (bool_check2 == True):
            #manipulate a model
            # select the proper model
        
            if (model_type == 'keras'):
                
                if (use_colab_memory == True):
                    ## Download the model
                    key = model_file_name + "." + model_extension
                    model_to_export.save(key)
                    files.download(key)
                    print(f"Keras/TensorFlow model: {key} successfully downloaded from Colab environment.")
            
                else:
                    #standard method
                    model_to_export.save(model_path)
                    print(f"Keras/TensorFlow model successfully exported as {model_path}.")

            elif (model_type == 'sklearn'):
                
                if (use_colab_memory == True):
                    ## Download the model
                    key = model_file_name + "." + model_extension
                    
                    with open(key, 'wb') as opened_file:

                        dill.dump(model_to_export, opened_file)
                    
                    #to save the file, the mode must be set as 'wb' (write binary)
                    files.download(key)
                    print(f"Scikit-learn model: {key} successfully downloaded from Colab environment.")
            
                else:
                    #standard method
                    with open(model_path, 'wb') as opened_file:

                        dill.dump(model_to_export, opened_file)
                    
                    print(f"Scikit-learn model successfully exported as {model_path}.")
                    # For exporting a pickle model:
                    ## pkl.dump(model_to_export, open(model_path, 'wb'))
            
            elif ((model_type == 'xgb_regressor')|(model_type == 'xgb_classifier')):
                # In both cases, the XGBoost object is already loaded in global
                # context memory. So there is already the object for using the
                # save_model method, available for both classes (XGBRegressor and
                # XGBClassifier).
                # We can simply check if it is one type OR the other, since the
                # method is the same:
                
                if (use_colab_memory == True):
                    ## Download the model
                    key = model_file_name + "." + model_extension
                    model_to_export.save_model(key)
                    files.download(key)
                    print(f"XGBoost model: {key} successfully downloaded from Colab environment.")
            
                else:
                    #standard method
                    model_to_export.save_model(model_path)
                    print(f"XGBoost model successfully exported as {model_path}.")
                    # For exporting a pickle model:
                    ## pkl.dump(model_to_export, open(model_path, 'wb'))
            
            elif (model_type == 'arima'):
                
                if (use_colab_memory == True):
                    ## Download the model
                    key = model_file_name + "." + model_extension
                    model_to_export.save(key)
                    files.download(key)
                    print(f"ARIMA model: {key} successfully downloaded from Colab environment.")
            
                else:
                    #standard method
                    model_to_export.save(model_path)
                    print(f"ARIMA model successfully exported as {model_path}.")
        
        print("Export of files completed.")
    
    else:
        print("Enter a valid action, import or export.")


def lag_diagnosis (df, column_to_analyze, number_of_lags = 40, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import statsmodels.api as sm
    
    # df: the whole dataframe to be processed.
    
    #column_to_analyze: string (inside quotes), 
    # containing the name of the column that will be analyzed. 
    # e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    #number_of_lags: integer value. e.g. number_of_lags = 50
    # represents how much lags will be tested, and the length of the horizontal axis.
    
    # Set a copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    
    #Define the series to be analyzed:
    y = DATASET[column_to_analyze]
    
    #Create the figure:
    fig = plt.figure(figsize = (12, 8)) 
    ax1 = fig.add_subplot(211)
    #ax1.set_xlabel("Lags")
    ax1.set_ylabel("Autocorrelation_Function_ACF")
    
    #ROTATE X AXIS IN XX DEGREES
    plt.xticks(rotation = x_axis_rotation)
    # XX = 0 DEGREES x_axis (Default)
    #ROTATE Y AXIS IN XX DEGREES:
    plt.yticks(rotation = y_axis_rotation)
    # XX = 0 DEGREES y_axis (Default)
    
    ax1.grid(grid)
    
    fig = sm.graphics.tsa.plot_acf(y.values.squeeze(), lags = number_of_lags, ax = ax1, color = 'darkblue')
    ax2 = fig.add_subplot(212)
    fig = sm.graphics.tsa.plot_pacf(y, lags = number_of_lags, ax = ax2, color = 'darkblue', method = 'ywm')
    ax2.set_xlabel("Lags")
    ax2.set_ylabel("Partial_Autocorrelation_Function_PACF")
        
    #ROTATE X AXIS IN XX DEGREES
    plt.xticks(rotation = x_axis_rotation)
    # XX = 0 DEGREES x_axis (Default)
    #ROTATE Y AXIS IN XX DEGREES:
    plt.yticks(rotation = y_axis_rotation)
    # XX = 0 DEGREES y_axis (Default)
    
    ax2.grid(grid)
        
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
            file_name = "lag_diagnosis"

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
    
    #Print background and interpretation of the graphic:
    print("\n") #line break
    print("Use this plot to define the parameters (p, q) for testing ARIMA and ARMA models.\n")
    print("p defines the order of the autoregressive part (AR) of the time series.")
    print("p = lags correspondent to the spikes of PACF plot (2nd plot) that are outside the error (blue region).\n")
    print("For instance, if there are spikes in both lag = 1 and lag = 2, then p = 2, or p = 1\n")
    print("q defines the order of the moving average part (MA) of the time series.")
    print("q = lags correspondent to the spikes of ACF plot that are outside blue region.\n")
    print("For instance, if all spikes until lag = 6 are outside the blue region, then q = 1, 2, 3, 4, 5, 6.\n")
    print("WARNING: do not test the ARIMA/ARMA model for p = 0, or q = 0.")
    print("For lag = 0, the correlation and partial correlation coefficients are always equal to 1, because the data is always perfectly correlated to itself.") 
    print("Therefore, ignore the first spikes (lag = 0) from ACF and PACF plots.")


def test_d_parameters (df, column_to_analyze, number_of_lags = 40, max_tested_d = 2, confidence_level = 0.95, x_axis_rotation = 0, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import statsmodels.api as sm
    from statsmodels.tsa.stattools import adfuller
    
    #df: the whole dataframe to be processed.
    
    #column_to_analyze: string (inside quotes), 
    # containing the name of the column that will be analyzed. 
    # e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    #max_tested_d: differential order (integer value)
    #change the integer if you want to test other cases. By default, max_tested_d = 2, meaning
    # that the values d = 0, 1, and 2 will be tested.
    # If max_tested_d = 1, d = 0 and 1 will be tested.
    # If max_tested_d = 3, d = 0, 1, 2, and 3 will be tested, and so on.
    
    #column_to_analyze: string (inside quotes), 
    # containing the name of the column that will be analyzed. 
    # e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    # CONFIDENCE_LEVEL = 0.95 = 95% confidence
    # Set CONFIDENCE_LEVEL = 0.90 to get 0.90 = 90% confidence in the analysis.
    # Notice that, when less trust is needed, we can reduce CONFIDENCE_LEVEL 
    # to get less restrictive results.
    
    #number_of_lags: integer value. e.g. number_of_lags = 50
    # represents how much lags will be tested, and the length of the horizontal axis.
    
    
    # Set a copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    
    #Define the series to be analyzed:
    time_series = DATASET[column_to_analyze]
    
    # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
    # so that the bars do not completely block other views.
    OPACITY = 0.95
    
    #Create the figure:
    # Original Series
    fig, axes = plt.subplots((max_tested_d + 1), 2, sharex = True, figsize = (12, 8)) 
    # sharex = share axis X
    # number of subplots equals to the total of orders tested (in this case, 2)
    # If max_tested_d = 2, we must have a subplot for d = 0, d = 1 and d = 2, i.e.,
    # wer need 3 subplots = max_tested_d + 1
    axes[0, 0].plot(time_series, color = 'darkblue', alpha = OPACITY); axes[0, 0].set_title('Original Series')
    sm.graphics.tsa.plot_acf(time_series, lags = number_of_lags, ax = axes[0, 1], color = 'darkblue', alpha = 0.30)
    
    #ROTATE X AXIS IN XX DEGREES
    plt.xticks(rotation = x_axis_rotation)
    # XX = 0 DEGREES x_axis (Default)
    #ROTATE Y AXIS IN XX DEGREES:
    plt.yticks(rotation = y_axis_rotation)
    # XX = 0 DEGREES y_axis (Default)
    
    axes[0, 0].grid(grid)
    
    # Create a subplot for each possible 'd'.
    # Notice that d = 0 was already tested.
    for i in range(1, (max_tested_d + 1)):
        # This loop goes from i = 1 to i = (max_tested_d + 1) - 1 = max_tested_d.
        # If max_tested_d = 2, this loop goes from i = 1 to i = 2.
        # If only one value was declared in range(X), then the loop would start from 0.
        
        # Difference the time series:
        time_series = time_series.diff()
        
        #the indexing of the list d goes from zero to len(d) - 1
        # 1st Differencing
        axes[i, 0].plot(time_series, color = 'darkblue', alpha = OPACITY); axes[i, 0].set_title('%d Order Differencing' %(i))
        sm.graphics.tsa.plot_acf(time_series.diff().dropna(), lags = number_of_lags, ax = axes[i, 1], color = 'darkblue', alpha = 0.30)
                
        #ROTATE X AXIS IN XX DEGREES
        plt.xticks(rotation = x_axis_rotation)
        # XX = 0 DEGREES x_axis (Default)
        #ROTATE Y AXIS IN XX DEGREES:
        plt.yticks(rotation = y_axis_rotation)
        # XX = 0 DEGREES y_axis (Default)

        axes[i, 0].grid(grid)
    
        print('ADF Statistic for %d Order Differencing' %(i))
        result = adfuller(time_series.dropna())
        print('ADF Statistic: %f' % result[0])
        print('p-value: %f' % result[1])
        print("Null-hypothesis: the process is non-stationary. p-value represents this probability.")

        if (result[1] < (1-confidence_level)):
            print("For a %.2f confidence level, the %d Order Difference is stationary." %(confidence_level, i))
            print("You may select d = %d\n" %(i))

        else:
            print("For a %.2f confidence level, the %d Order Difference is non-stationary.\n" %(confidence_level, i))
        
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
            file_name = "test_d_parameters"

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
    print("d = differentiation order for making the process stationary.\n")
    print("If d = N, then we have to make N successive differentiations.")
    print("A differentiation consists on substracting a signal Si from its previous signal Si-1.\n")
    print("Example: 1st-order differentiating consists on taking the differences on the original time series.")
    print("The 2nd-order, in turns, consists in differentiating the 1st-order differentiation series.")


def best_arima_model (df, column_to_analyze, p_vals, d, q_vals, timestamp_tag_column = None, confidence_level = 0.95, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    # https://www.statsmodels.org/stable/generated/statsmodels.tsa.arima.model.ARIMAResults.html#statsmodels.tsa.arima.model.ARIMAResults
    # https://www.statsmodels.org/stable/examples/notebooks/generated/tsa_arma_1.html?highlight=statsmodels%20graphics%20tsaplots%20plot_predict
    
    ## d = 0 corresponds to the ARMA model
    
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import statsmodels as sm
    from statsmodels.graphics.tsaplots import plot_predict
    #this model is present only in the most recent versions of statsmodels

    from statsmodels.tsa.arima.model import ARIMA, ARIMAResults
    
    #df: the whole dataframe to be processed.
    
    #column_to_analyze: string (inside quotes), 
    # containing the name of the column that will be analyzed. 
    # e.g. column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    # timestamp_tag_column = None - keep it as None if you do not want to inform the timestamps
    # Alternatively, declare a string (inside quotes), 
    # containing the name of the column containing the time information. 
    # e.g. timestamp_tag_column = "DATE" will take the timestamps from column 'DATE'.
    # If no column is provided, the index in the dataframe will be used.
    
    #p_vals: list of integers correspondent to the lags (spikes) in the PACF plot.
    # From function lag_diagnosis
    #q_vals: list of integers correspondent to the lags (spikes) in ACF plot
    # From function lag_diagnosis
    #d = difference for making the process stationary
    # From function test_d_parameters
    
    ## WARNING: do not test the ARIMA/ARMA model for p = 0, or q = 0.
    ## For lag = 0, the correlation and partial correlation coefficients 
    ## are always equal to 1, because the data is perfectly correlated to itself. 
    ## Therefore, ignore the first spikes (lag = 0) of ACF and PACF plots.
    
    ALPHA = 1 - confidence_level
    # CONFIDENCE_LEVEL = 0.95 = 95% confidence
    # Set CONFIDENCE_LEVEL = 0.90 to get 0.90 = 90% confidence in the analysis.
    # Notice that, when less trust is needed, we can reduce CONFIDENCE_LEVEL 
    # to get less restrictive results.
    
    # Set a copy of the dataframe to manipulate:
    DATASET = df.copy(deep = True)
    
    #x: timestamp or index series, if no timestamp is provided:
    if (timestamp_tag_column is None):
        #Use the indices of the dataframe
        x = DATASET.index
    
    else:
        #Use the timestamp properly converted to datetime (as in the graphics functions):
        x = (DATASET[timestamp_tag_column]).astype('datetime64[ns]')
        DATASET[timestamp_tag_column] = x
        # To pass the date to ARIMA model, we must specify it as the index, and also pass the
        # start and end dates
        DATASET = DATASET.set_index(timestamp_tag_column)
    
    #y: tested variable series
    y = DATASET[column_to_analyze]
    
    # date to start the plot (the second element from series x - we will ignore the first one):
    start_date = x[1]
    # last date to plot (last element from the series)
    end_date = x[(len(x) - 1)]
    print(f"ARIMA model from date (or measurement) = {start_date}; to date (or measurement) = {end_date}.\n")
    
    #calculate the first aic and bic
    #first argument = time series y
    
    returned_p = p_vals[0]
    returned_q = q_vals[0]
    returned_d = d
    #use the d-value selected in the non-stationary analysis.
    #set the integration in 
    #at this moment, the function simply returns the first elements.
    
    ARIMA_model = ARIMA(y, order = (returned_p, returned_d, returned_q))

    #order = (p, d, q) - these are the parameters of the autoregression (p = 2), 
    #integration (d = parameter selected in previous analysis), and
    #moving average (q = 1, 2, 3, 4, 5, etc)

    ARIMA_Results = ARIMA_model.fit()
    aic_val = ARIMA_Results.aic
    #AIC value for the first combination.
    bic_val = ARIMA_Results.bic
    #BIC value for the first combination, to start the loops.
    
    # Mean absolute error:
    mae = ARIMA_Results.mae
    # log likelihood calculated:
    loglikelihood = ARIMA_Results.llf
    
    returned_ARIMA_Results = ARIMA_Results
    #returned object
    
    for p in p_vals:
        #test each possible value for p (each d, p combination)
        #each p in p_vals list is used.
        for q in q_vals:
            #test each possible value for q (each p, d, q combination)
            #each q in q_vals list is used.
                
            ARIMA_model = ARIMA(y, order = (p, returned_d, q))
            ARIMA_Results = ARIMA_model.fit()
            aic_tested = ARIMA_Results.aic
            bic_tested = ARIMA_Results.bic
            mae_tested = ARIMA_Results.mae
            loglikelihood_tested = ARIMA_Results.llf
            
            if ((mae_tested < mae) & (abs(loglikelihood_tested) > abs(loglikelihood))):
                
                # Check if the absolute error was reduced and the likelihood was increased
                
                #if better parameters were found, they should be used
                #update AIC, BIC; the p, d, q returned values;
                #and the ARIMA_Results from the ARIMA:
                aic_val = aic_tested
                bic_val = bic_tested
                mae = mae_tested
                loglikelihood = loglikelihood_tested
                returned_p = p

                returned_q = q
                #return the Statsmodels object:
                returned_ARIMA_Results = ARIMA_Results
    
    #Create a dictionary containing the best parameters and the metrics AIC and BIC
    arima_summ_dict = {"p": returned_p, "d": returned_d, "q": returned_q,
                   "AIC": returned_ARIMA_Results.aic, "BIC": returned_ARIMA_Results.bic,
                    "MAE": returned_ARIMA_Results.mae, "log_likelihood": returned_ARIMA_Results.llf}
    
    #Show ARIMA results:
    print(returned_ARIMA_Results.summary())
    print("\n")
    #Break the line and show the combination
    print("Best combination found: (p, d, q) = (%d, %d, %d)\n" %(returned_p, returned_d, returned_q))
    #Break the line and print the next indication:
    print(f"Time series, values predicted by the model, and the correspondent {confidence_level * 100}% Confidence interval for the predictions:\n")
    #Break the line and print the ARIMA graphic:
    
    # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
    # so that the bars do not completely block other views.
    OPACITY = 0.95
    
    #Start the figure:
    fig, ax = plt.subplots(figsize = (12, 8))
    # Add line of the actual values:
    ax.plot(x, y, linestyle = '-', marker = '', color = 'darkblue', label = column_to_analyze)
    # Use the name of the analyzed column as the label
    fig = plot_predict(returned_ARIMA_Results, start = start_date, end = end_date,  ax = ax, alpha = ALPHA)
    ## https://www.statsmodels.org/v0.12.2/generated/statsmodels.tsa.arima_model.ARIMAResults.plot_predict.html
    # ax = ax to plot the arima on the original plot of the time series
    # start = x[1]: starts the ARIMA graphic from the second point of the series x
    # if x is the index, then it will be from the second x; if x is a time series, then
    # x[1] will be the second timestamp
    #We defined the start in x[1], instead of index = 0, because the Confidence Interval for the 
    #first point is very larger than the others (there is perfect autocorrelation for lag = 0). 
    #Therefore, it would have resulted in the need for using a very broader y-scale, what
    #would compromise the visualization.
    # We could set another index or even a timestamp to start:
    # start=pd.to_datetime('1998-01-01')
    
    ax.set_alpha(OPACITY)
    
    if not (plot_title is None):
        #graphic's title
        ax.set_title(plot_title)
    
    else:
        #set a default title:
        ax.set_title("ARIMA_model")
    
    if not (horizontal_axis_title is None):
        #X-axis title
        ax.set_xlabel(horizontal_axis_title)
    
    else:
        #set a default title:
        ax.set_xlabel("Time")
    
    if not (vertical_axis_title is None):
        #Y-axis title
        ax.set_ylabel(vertical_axis_title)
    
    else:
        #set a default title:
        ax.set_ylabel(column_to_analyze)
    
    #ROTATE X AXIS IN XX DEGREES
    plt.xticks(rotation = x_axis_rotation)
    # XX = 70 DEGREES x_axis (Default)
    #ROTATE Y AXIS IN XX DEGREES:
    plt.yticks(rotation = y_axis_rotation)
    # XX = 0 DEGREES y_axis (Default)
    
    ax.grid(grid)
    ax.legend(loc = "upper left")
    
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
            file_name = "arima_model"

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
    
    # Get dataframe with the predictions and confidence intervals
    arima_predictions = returned_ARIMA_Results.get_prediction(start = x[0], end = None, dynamic = False, full_results = True, alpha = ALPHA)
    # Here, we started in start = x[0] to obtain a correspondent full dataset, and did not set an end.
    # The start can be an integer representing the index of the data in the dataframe,
    # or a timestamp. Check:
    # https://www.statsmodels.org/devel/generated/statsmodels.tsa.arima.model.ARIMAResults.get_prediction.html#statsmodels.tsa.arima.model.ARIMAResults.get_prediction
    # Again, no matter if x is an index or a time series, x[0] starts from the first element
    # You could set another index or a oparticular timestamp to start, like:
    # start=pd.to_datetime('1998-01-01')
    # The dynamic = False argument ensures that we produce one-step ahead forecasts, 
    # meaning that forecasts at each point are generated using the full history up 
    # to that point.
    predicted_mean_vals = arima_predictions.predicted_mean
    predicted_conf_intervals = arima_predictions.conf_int(alpha = ALPHA)
    # predicted_conf_intervals has two columns: first one is the inferior confidence limit
    # second one is the superior confidence limit
    # each column from this dataframe gets a name derived from the name of the original series.
    # So, let's rename them:
    predicted_conf_intervals.columns = ['lower_cl', 'upper_cl']
    
    # let's create a copy of the dataframe to be returned with the new information:
    # This will avoid manipulating the df:
    arima_df = DATASET.copy(deep = True)
    # This DATASET already contains the timestamp column as the index, so it is adequate for
    # obtaining predictions associated to the correct time values.
    
    #create a column for the predictions:
    arima_df['arima_predictions'] = predicted_mean_vals
    
    #create a column for the inferior (lower) confidence interval.
    # Copy all the rows from the column 0 of predicted_conf_intervals
    arima_df['lower_cl'] = predicted_conf_intervals['lower_cl']
    
    #create a column for the superior (upper) confidence interval.
    # Copy all the rows from the column 1 of predicted_conf_intervals
    arima_df['upper_cl'] = predicted_conf_intervals['upper_cl']
    
    # Let's turn again the timestamps into a column, restart the indices and re-order the columns,
    # so that the last column will be the response, followed by ARIMA predictions
    
    ordered_columns_list = []
    
    if (timestamp_tag_column is not None):
        #Use the indices of the dataframe
        ordered_columns_list.append(timestamp_tag_column)
        # Create a timestamp_tag_column in the dataframe containing the values in the index:
        arima_df[timestamp_tag_column] = np.array(arima_df.index)
        # Reset the indices from the dataframe:
        arima_df = arima_df.reset_index(drop = True)
    
    # create a list of columns with fixed position:
    fixed_columns_list = [column_to_analyze, 'arima_predictions', 'lower_cl', 'upper_cl']
    
    # Now, loop through all the columns:
    for column in list(arima_df.columns):
        
        # If the column is not one from fixed_columns_list, and it is not on ordered_columns_list
        # yet, add it to ordered_columns_list (timestamp_tag_column may be on the list):
        if ((column not in fixed_columns_list) & (column not in ordered_columns_list)):
            ordered_columns_list.append(column)
    
    # Now, concatenate ordered_columns_list to fixed_columns_list. 
    # If a = ['a', 'b'] and b = ['c', 'd'], a + b = ['a', 'b', 'c', 'd'] and b + a = [ 'c', 'd', 'a', 'b']
    ordered_columns_list = ordered_columns_list + fixed_columns_list
    
    # Finally, select the columns from arima_df passing this list as argument:
    arima_df = arima_df[ordered_columns_list]
    print("\n")
    print("Check the dataframe containing the ARIMA predictions:\n")
    print(arima_df)
    
    print("\n") #line break
    print("Notice that the presence of data outside the confidence interval limits of the ARIMA forecast is a strong indicative of outliers or of untrust time series.\n")
    print("For instance: if you observe a very sharp and sudden deviation from the predictive time series, it can be an indicative of incomplete information or outliers presence.\n")
    print("A famous case is the pandemic data: due to lags or latencies on the time needed for consolidating the information in some places, the data could be incomplete in a given day, leading to a sharp decrease that did not actually occurred.")
    
    print("\n")
    print("REMEMBER: q represents the moving average (MA) part of the time series.")
    print(f"Then, it is interesting to group the time series {column_to_analyze} by each q = {returned_q} periods when modelling or analyzing it.")
    print("For that, you can use moving window or rolling functions.\n")
    
    return returned_ARIMA_Results, arima_summ_dict, arima_df


def arima_forecasting (arima_model_object, df = None, column_to_forecast = None, timestamp_tag_column = None, time_unit = None, number_of_periods_to_forecast = 7, confidence_level = 0.95, plot_predicted_time_series = True, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import statsmodels as sm
    from statsmodels.graphics.tsaplots import plot_predict
    #this model is present only in the most recent versions of statsmodels

    from statsmodels.tsa.arima.model import ARIMA, ARIMAResults
    
    # arima_model_object : object containing the ARIMA model previously obtained.
    # e.g. arima_model_object = returned_ARIMA_Results if the model was obtained as returned_ARIMA_Results
    # do not declare in quotes, since it is an object, not a string.
    
    # time_unit: Unit of the new column. If no value is provided, the unit will be considered as nanoseconds. 
    # Alternatively: keep it None, for the results in nanoseconds, or input time_unit = 
    # 'year', 'month', 'day', 'hour', 'minute', or 'second' (keep these inside quotes).
    # It will be the input for the functions CALCULATE_DELAY and ADD_TIMEDELTA.
    
    # number_of_periods_to_forecast = 7
    # integer value representing the total of periods to forecast. The periods will be in the
    # unit (dimension) of the original dataset. If 1 period = 1 day, 7 periods will represent
    # seven days.
    
    # Keep plot_predicted_time_series = True to see the graphic of the predicted values.
    # WARNING: This functionality requires that the function scatter_plot_lin_reg is properly
    # running, since this function will be called.
    # Other functions required: CALCULATE_DELAY and UNION_DATAFRAMES
    # Alternatively, set plot_predicted_time_series = True not to show the plot.
    
    # df = None, column_to_analyze = None - keep it as None if you do not want to show
    # the ARIMA predictions combined to the original data; or if you do not want to append
    # the ARIMA predictions to the original dataframe.
    # Alternatively, set:
    # df: the whole dataframe to be processed.
    
    # column_to_forecast: string (inside quotes), 
    # containing the name of the column that will be analyzed.
    # Keep it as None if the graphic of the predictions will not be shown with the
    # responses or if the combined dataset will not be returned.
    # e.g. column_to_forecast = "column1" will analyze and forecast values for 
    # the column named as 'column1'.
    
    # timestamp_tag_column: string (inside quotes), 
    # containing the name of the column containing timestamps.
    # Keep it as None if the graphic of the predictions will not be shown with the
    # responses or if the combined dataset will not be returned.
    # e.g. timestamp_tag_column = "column1" will analyze the column named as 'column1'.
    
    ## ARIMA predictions:
    ## The .forecast and .predict methods only produce point predictions:
    ## y_forecast = ARIMA_Results.forecast(7) results in a group of values (7 predictions)
    ## without the confidence intervals
    ## On the other hand, the .get_forecast and .get_prediction methods 
    ## produce full results including prediction intervals.

    ## In our example, we can do:
    ## forecast = ARIMA_Results.get_forecast(123)
    ## yhat = forecast.predicted_mean
    ## yhat_conf_int = forecast.conf_int(alpha=0.05)
    ## If your data is a Pandas Series, then yhat_conf_int will be a DataFrame with 
    ## two columns, lower <name> and upper <name>, where <name> is the name of the Pandas 
    ## Series.
    ## If your data is a numpy array (or Python list), then yhat_conf_int will be an 
    ## (n_forecasts, 2) array, where the first column is the lower part of the interval 
    ## and the second column is the upper part.
   
    numeric_data_types = [np.float16, np.float32, np.float64, np.int16, np.int32, np.int64]
    
    ALPHA = 1 - confidence_level
    # CONFIDENCE_LEVEL = 0.95 = 95% confidence
    # Set CONFIDENCE_LEVEL = 0.90 to get 0.90 = 90% confidence in the analysis.
    # Notice that, when less trust is needed, we can reduce CONFIDENCE_LEVEL 
    # to get less restrictive results.
    
    # Calculate the predictions:
    # It does not depend on the presence of a dataframe df
    # https://www.statsmodels.org/devel/generated/statsmodels.tsa.arima.model.ARIMAResults.get_forecast.html#statsmodels.tsa.arima.model.ARIMAResults.get_forecast
    
    arima_forecasts = arima_model_object.get_forecast(number_of_periods_to_forecast, dynamic = False, full_results = True, alpha = ALPHA)
    
    forecast_mean_vals = arima_forecasts.predicted_mean
    forecast_conf_intervals = arima_forecasts.conf_int(alpha = ALPHA)
    # forecast_conf_intervals has two columns: first one is the inferior confidence limit
    # second one is the superior confidence limit
    # each column from this dataframe gets a name derived from the name of the original series.
    # So, let's rename them:
    forecast_conf_intervals.columns = ['lower_cl', 'upper_cl']
    
    #create a series for the inferior confidence interval.
    lower_cl = forecast_conf_intervals['lower_cl'].copy(deep = True)
    #create a series for the superior confidence interval.
    upper_cl = forecast_conf_intervals['upper_cl'].copy(deep = True)
    
    # If there is no df, we can already obtain a X series, that will be a series of indices
    # starting from period 1 (the first forecast. Period zero corresponds to the last actual value):
    if (df is None):
        
        x_forecast = []
        
        for j in range (1, (number_of_periods_to_forecast + 1)):
            #Goes from j = 1, the first forecast period; to j = (number_of_periods_to_forecast+1)-1
            # = number_of_periods_to_forecast, which must be the last forecast.
            x_forecast.append(j)
        
        # Now, create the dictionary of forecasts:
        forecast_dict = {
            
            "x": x_forecast,
            "forecast_mean_vals": forecast_mean_vals,
            "lower_cl": lower_cl,
            "upper_cl": upper_cl,
            'source': 'forecast'
        }
        
        # Convert it to a dataframe:
        forecast_df = pd.DataFrame(data = forecast_dict)
        x_forecast_series = forecast_df['x']
        y_forecast_series = forecast_df['forecast_mean_vals']
        lcl_series = forecast_df['lower_cl']
        ucl_series = forecast_df['upper_cl']
    
    
    # If there is a dataframe df, we must combine the original data from df
    # with the new predictions:
    else:
        
        # Start a dataset copy to manipulate:
        DATASET = df.copy(deep = True)
        
        # Create a column with a label indicating that the data in DATASET (before concatenation 
        # with predictions) is from the original dataframe:
        DATASET['source'] = 'input_dataframe'
        # In turns, The source column in the dataframe from the forecasts will 
        # be labelled with the string 'forecast'
        
        # Check if a column_to_forecast was indicated in the input dataframe:
        if not (column_to_forecast is None):
            
            # If there is a response column indicated, then the forecast column of the 
            # generated predictions must be stored in a column with the exact same name, so that
            # the columns can be correctly appended
            y_forecast_label = column_to_forecast
            # Also, create a separate series for the original data, that will be used for
            # differentiating between data and forecasts on the plot:
            y_original_series = DATASET[column_to_forecast].copy(deep = True)
        
        # If no column was indicated, set a default column name for the forecasts:
        else:
            # Set the default name:
            y_forecast_label = "y_forecast"
        
        
        # Check if a timestamp_tag_column was input. If not, use the indices themselves as times.
        # Create a new standard name for the column in forecasts:
        if (timestamp_tag_column is None):
            
            # Let's set an index series as the index of the dataframe:
            DATASET['index_series'] = DATASET.index
            # Check if this series contains an object. If it has, then, user set the timestamps
            # as the indices
            index_series_type = DATASET['index_series'].dtype
            
            # If it is an object, the user may be trying to pass the date as index. 
            # So, let's try to convert it to datetime:
            if ((index_series_type not in numeric_data_types) | (index_series_type == 'O') | (index_series_type == 'object')):
                  
                try:
                    DATASET['index_series'] = (DATASET['index_series']).astype('datetime64[ns]')
                    
                    # Rename column 'index_series':
                    # https://www.statology.org/pandas-rename-columns/
                    DATASET.rename(columns = {'index_series': 'timestamp'}, inplace = True)
                    # Set 'timestamp' as the timestamp_tag_column:
                    timestamp_tag_column = 'timestamp'
                    
                except:
                    # A variable that is not neither numeric nor date was passed. Reset the index:
                    DATASET = DATASET.reset_index(drop = True)
                    # Update the index series
                    DATASET['index_series'] = DATASET.index
                    
            # Now, try to manipulate the 'index_series'. An exception will be raised in case
            # the name was changed because the index contains a timestamp
            try:
                
                # convert the 'index_series' to the default name for column X:
                x_forecast_label  = "x_forecast"
                DATASET.rename(columns = {'index_series': x_forecast_label}, inplace = True)
                x_original_series = DATASET[x_forecast_label].copy(deep = True)
            
                # Let's create the series for forecasted X. Simply add more values to x
                # until reaching the number_of_periods_to_forecast:
            
                # Get the value of the last X of the dataframe
                # index start from zero, so the last one is length - 1
                last_x = x_original_series[(len(x_original_series) - 1)]

                #Start the list
                x_forecast = []

                #Append its first value: last X plus 1 period
                x_forecast.append(last_x + 1)
            
                j = 1
                while (j < number_of_periods_to_forecast):
                    #Last cycle occurs when j == number_of_periods_to_forecast - 1
                    # Since indexing starts from zero, there will be number_of_periods_to_forecast
                    # elements in the list.
                    # Also, we already added the first period, so we are starting from the 2nd
                    # forecast period, j = 1.
                    x_forecast.append((x_forecast[(j - 1)] + 1))

                    #Go to next iteration:
                    j = j + 1
                
                # Now, x_forecast stores the next indices for the situation where no timestamp
                # was provided initially.
            
            except:
                #simply pass
                pass
        
        
        # Again, check if timestamp_tag_column is None. It may have changed, since we created a value
        # for the case where a timestamp is in the index. So, we will not use else: the else would
        # ignore the modification in the first if:
        
        if not (timestamp_tag_column is None):
            # Use the timestamp properly converted to datetime (as in the graphics functions).
            # The labels must be the same for when the dataframes are merged.
            x_forecast_label  = timestamp_tag_column
            
            # Check if it is an object or is not a numeric variable (e.g. if it is a timestamp):
            if ((DATASET[timestamp_tag_column].dtype not in numeric_data_types) | (DATASET[timestamp_tag_column].dtype == 'O') | (DATASET[timestamp_tag_column].dtype == 'object')):
                
                # Try to convert it to np.datetime64
                try:

                    DATASET[timestamp_tag_column] = (DATASET[timestamp_tag_column]).astype('datetime64[ns]')
                
                except:
                    pass
                
            # Now, timestamp is either a numeric column or a datetime column.
            # Again, create a separate series for the original data, that will be used for
            # differentiating between data and forecasts on the plot:
            x_original_series = DATASET[timestamp_tag_column].copy(deep = True)
            
            # Get the last X of the dataframe
            # index start from zero, so the last one is length - 1
            last_x = x_original_series[(len(x_original_series) - 1)]
            
            # Check the case where it is a timestamp:
            if (type(x_original_series[0]) == np.datetime64):
                
                # Let's obtain the mean value of the timedeltas between each measurement:
                TIMESTAMP_TAG_COLUMN = timestamp_tag_column
                NEW_TIMEDELTA_COLUMN_NAME = None
                RETURNED_TIMEDELTA_UNIT = time_unit
                # If it is none, the value will be returned in nanoseconds.
                # keep it None, for the results in nanoseconds
                RETURN_AVG_DELAY = True
                _, avg_delay = CALCULATE_DELAY (df = DATASET, timestamp_tag_column = TIMESTAMP_TAG_COLUMN, new_timedelta_column_name  = NEW_TIMEDELTA_COLUMN_NAME, returned_timedelta_unit = RETURNED_TIMEDELTA_UNIT, return_avg_delay = RETURN_AVG_DELAY)
                # The underscore indicates that we will not keep the returned dataframe
                # only the average time delay in nanoseconds.
                print("\n")
                print(f"Average delay on the original time series, used for obtaining times of predicted values = {avg_delay}.\n")

                # Now, avg_delay stores the mean time difference between successive measurements from the
                # original dataset.
            
                # Now, let's create the prediction timestamps, by adding the avg_delay to
                # the last X.
                # Firstly, convert last_x to a Pandas timestamp, so that we can add a pandas
                # timedelta:
                last_x = pd.Timestamp(last_x, unit = 'ns')
            
                # Now, let's create a pandas timedelta object correspondent to avg_delay
                # 1. Check units:
                if (time_unit is None):
                    time_unit = 'ns'
            
                # Notice that CALCULATE_DELAY and ADD_TIMEDELTA update the unit for us, but
                # such functions deal with a dataframe, not with a single value. So, we are
                # using a small piece from ADD_TIMEDELTA function to operate with a single
                # timestamp.

                #2. Create the pandas timedelta object:
                timedelta = pd.Timedelta(avg_delay, time_unit)
            
                #3. Let's create the values of timestamps correspondent to the forecast
                x_forecast = []
                # The number of elements of this list is number_of_periods_to_forecast
                # if number_of_periods_to_forecast, we will forecast a single period further,
                # then we need to sum timedelta once. If number_of_periods_to_forecast = 3,
                # we will sum timedelta 3 times, and so on.
            
                # Append the first element (last element + timedelta) - first value forecast
                x_forecast.append((last_x + timedelta))
            
                j = 1
                while (j < number_of_periods_to_forecast):
                    #Last cycle occurs when j == number_of_periods_to_forecast - 1
                    # Since indexing starts from zero, there will be number_of_periods_to_forecast
                    # elements in the list.
                    # Also, we already added the first period, so we are starting from the 2nd
                    # forecast period, j = 1.

                    # append the previous element + timedelta.
                    # If j = 1, (j - 1) = 0, the first element
                    x_forecast.append((x_forecast[(j - 1)] + timedelta))
                
                    #Go to next iteration:
                    j = j + 1
        
                # Now, x_forecast stores the values of timestamps correspondent to
                # the forecasts.
                # Convert x_forecast to Pandas Series, so that it will be possible to perform vectorial
                # operations:
                x_forecast = pd.Series(x_forecast)
                # Convert it to datetime64:
                x_forecast = (x_forecast).astype('datetime64[ns]')
            
            else:
                # We have a numerical variable used as time. We have to calculate the average 'delay' between
                # Successive values. For that, we can again use Pandas.diff method, which may be applied to
                # Series or DataFrames
                # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.diff.html
                # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.diff.html#pandas.Series.diff
                
                x_diff_series = x_original_series.copy(deep = True)
                x_diff_series = x_diff_series.diff(periods = 1)
                # periods - int, default 1 - Periods to shift for calculating difference, accepts negative values.
                
                # Now, get the average delay as the mean value from series x_diff_series:
                avg_delay = x_diff_series.mean()
                print("\n")
                print(f"Average delay on the original time series, used for obtaining times of predicted values = {avg_delay}.\n")
                
                # Let's create the values of times correspondent to the forecast
                x_forecast = []
                # The number of elements of this list is number_of_periods_to_forecast
                # if number_of_periods_to_forecast, we will forecast a single period further,
                # then we need to sum timedelta once. If number_of_periods_to_forecast = 3,
                # we will sum timedelta 3 times, and so on.
            
                # Append the first element (last element + avg_delay) - first value forecast
                x_forecast.append((last_x + avg_delay))
            
                j = 1
                while (j < number_of_periods_to_forecast):
                    #Last cycle occurs when j == number_of_periods_to_forecast - 1
                    # Since indexing starts from zero, there will be number_of_periods_to_forecast
                    # elements in the list.
                    # Also, we already added the first period, so we are starting from the 2nd
                    # forecast period, j = 1.

                    # append the previous element + timedelta.
                    # If j = 1, (j - 1) = 0, the first element
                    x_forecast.append((x_forecast[(j - 1)] + avg_delay))
                
                    #Go to next iteration:
                    j = j + 1
                
        # Notice that all these steps are possible only when the timestamps were
        # given, and so they should not be executed if the values are not provided.
        
        
        # Now, steps are the same for all cases where there is a dataframe (Main Else node that we are evaluating): 
        # create the dictionary of forecasts:
        forecast_dict = {

            x_forecast_label: x_forecast,
            y_forecast_label: forecast_mean_vals,
            "lower_cl": lower_cl,
            "upper_cl": upper_cl,
            'source': 'forecast'
        }

        # Convert it to a dataframe:
        forecast_df = pd.DataFrame(data = forecast_dict)
        x_forecast_series = forecast_df[x_forecast_label]
        y_forecast_series = forecast_df[y_forecast_label]
        lcl_series = forecast_df['lower_cl']
        ucl_series = forecast_df['upper_cl']

        # Now, let's concatenate the new dataframe to the old one.
        # The use of the variables 'source', x_ and y_forecast_label guarantees that the new
        # columns have the same name as the ones of the original dataframe, so that
        # the concatenation is performed correctly.

        # Now, merge the dataframes:
        LIST_OF_DATAFRAMES = [DATASET, forecast_df]
        IGNORE_INDEX_ON_UNION = True
        SORT_VALUES_ON_UNION = True
        UNION_JOIN_TYPE = None
        forecast_df = UNION_DATAFRAMES (list_of_dataframes = LIST_OF_DATAFRAMES, ignore_index_on_union = IGNORE_INDEX_ON_UNION, sort_values_on_union = SORT_VALUES_ON_UNION, union_join_type = UNION_JOIN_TYPE)
        
        # Full series, with input data and forecasts:
        x = forecast_df[x_forecast_label]
        y = forecast_df[y_forecast_label]
        
        # Now, let's re-order the dataframe, putting the x_forecast_label as the first column
        # and y_forecast_label: forecast_mean_vals, "lower_cl", "upper_cl", and 'source'
        # as the last ones.
        
        # Set a list of the last columns (fixed positions):
        fixed_columns_list = [y_forecast_label, 'lower_cl', 'upper_cl', 'source']
        
        # Start the list with only x_forecast_label:
        ordered_columns_list = [x_forecast_label]
        
        # Now, loop through all the columns:
        for column in list(forecast_df.columns):

            # If the column is not one from fixed_columns_list, and it is not on ordered_columns_list
            # yet, add it to ordered_columns_list (timestamp_tag_column may be on the list):
            if ((column not in fixed_columns_list) & (column not in ordered_columns_list)):
                ordered_columns_list.append(column)
        
        # Now, concatenate ordered_columns_list to fixed_columns_list. 
        # If a = ['a', 'b'] and b = ['c', 'd'], a + b = ['a', 'b', 'c', 'd'] and b + a = [ 'c', 'd', 'a', 'b']
        ordered_columns_list = ordered_columns_list + fixed_columns_list
        
        # Finally, pass ordered_columns_list as argument for column filtering and re-order:
        forecast_df = forecast_df[ordered_columns_list]

        
    # We are finally in the general case, after obtaining the dataframe through all possible ways:
    print(f"Finished the obtention of the forecast dataset. Check the 10 last rows of the forecast dataset:\n")
    print(forecast_df.tail(10))
    
    # Now, let's create the graphics
    if (plot_predicted_time_series == True):
        
        LINE_STYLE = '-'
        MARKER = ''
        
        if (plot_title is None):
            # Set graphic title
            plot_title = f"ARIMA_forecasts"

        if (horizontal_axis_title is None):
            # Set horizontal axis title
            if (timestamp_tag_column is None):
                horizontal_axis_title = "timestamp"
            else:
                horizontal_axis_title = timestamp_tag_column

        if (vertical_axis_title is None):
            if (column_to_forecast is None):
                vertical_axis_title = "time_series"
            else:
                vertical_axis_title = column_to_forecast
        
        # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
        # so that the bars do not completely block other views.
        OPACITY = 0.95
        
        #Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
        fig = plt.figure(figsize = (12, 8))
        ax = fig.add_subplot()
        
        if ((df is not None) & ((column_to_forecast is not None))):
            
            # Plot the original data series:
            ax.plot(x, y, linestyle = LINE_STYLE, marker = MARKER, color = 'darkblue', alpha = OPACITY, label = 'input_dataframe')
        
        # Plot the predictions (completely opaque, so that the input data series will not be
        # visible)
        ax.plot(x_forecast_series, y_forecast_series, linestyle = LINE_STYLE, marker = MARKER, color = 'red', alpha = 1.0, label = 'forecast')
        
        # Plot the confidence limits:
        ax.plot(x_forecast_series, lcl_series, linestyle = 'dashed', marker = MARKER, color = 'magenta', alpha = 0.70, label = 'lower_confidence_limit')
        ax.plot(x_forecast_series, ucl_series, linestyle = 'dashed', marker = MARKER, color = 'magenta', alpha = 0.70, label = 'upper_confidence_limit')    
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
        ax.legend()
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
                file_name = "arima_forecast"

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
    
    print("\nARIMA Forecasting completed.\n")
    
    return forecast_df


def df_rolling_window_stats (df, window_size = 2, window_statistics = 'mean', min_periods_required = None, window_center = False, window_type = None, window_on = None, row_accross = 'rows', how_to_close_window = None, drop_missing_values = True):
    
    import numpy as np
    import pandas as pd
    
    # Check Pandas rolling statistics documentation:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rolling.html
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/window.html#window-generic
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.diff.html
    
    ## df: the whole dataframe to be processed.
    
    # window_statistics = 'mean', 'std', 'sum', or 'difference'
    # 'difference' will perform the first discrete difference of element: Yn - Yn-1
    
    # window_size: integer value or offset time.
    # Manipulate parameter window of the .rolling method; or the parameter
    # periods of the .diff method.
    # window = window_size; or periods = window_size.
    # Size of the moving window. If an integer, the fixed number of observations 
    # used for each window. If an offset, the time period of each window. 
    # Each window will be a variable sized based on the observations included in the 
    # time-period. This is only valid for datetime-like indexes. 
    
    # min_periods_required = None. Alternatively, set as an integer value.
    # Manipulate parameter min_periods of .rolling method
    # min_periods = min_periods_required
    # Minimum number of observations in window required to have a value; otherwise, 
    # result is np.nan. For a window that is specified by an offset, min_periods will 
    # default to 1. For a window that is specified by an integer, min_periods will default 
    # to the size of the window.
    
    # window_center = False.
    # Manipulate parameter center of .rolling method
    # center = window_center
    # If False, set the window labels as the right edge of the window index.
    # If True, set the window labels as the center of the window index.
    
    # window_type = None
    # Manipulate parameter win_type of .rolling method
    # win_type = window_type
    # If None, all points are evenly weighted. If a string, it must be a valid 
    # scipy.signal window function:
    # https://docs.scipy.org/doc/scipy/reference/signal.windows.html#module-scipy.signal.windows
    # Certain Scipy window types require additional parameters to be passed in the 
    # aggregation function. The additional parameters must match the keywords specified 
    # in the Scipy window type method signature.
    
    # window_on = None
    # Manipulate parameter on of .rolling method
    # on = window_on
    # string; For a DataFrame, a column label or Index level on which to calculate 
    # the rolling window, rather than the DataFrame’s index. Provided integer column is 
    # ignored and excluded from result since an integer index is not used to calculate 
    # the rolling window.
    
    # row_accross = 'rows'. Alternatively, row_accross = 'columns'
    # manipulate the parameter axis of .rolling method:
    # if row_accross = 'rows', axis = 0; if row_accross = 'columns', axis = 1.
    # If axis = 0 or 'index', roll across the rows.
    # If 1 or 'columns', roll across the columns.
    
    # how_to_close_window = None
    # Manipulate parameter closed of .rolling method
    # closed = how_to_close_window
    # String: If 'right', the first point in the window is excluded from calculations.
    # If 'left', the last point in the window is excluded from calculations.
    # If 'both', the no points in the window are excluded from calculations.
    # If 'neither', the first and last points in the window are excluded from calculations.
    # Default None ('right').
    
    # drop_missing_values = True will remove all missing values created by the methods (all
    # rows containing missing values). 
    # If drop_missing_values = False, the positions containing NAs will be kept.
    
    DATASET = df.copy(deep = True)
    WINDOW = window_size
    MIN_PERIODS = min_periods_required
    CENTER = window_center
    WIN_TYPE = window_type
    ON = window_on
    
    numeric_data_types = [np.float16, np.float32, np.float64, np.int16, np.int32, np.int64]
    
    # Variable to map if the timestamp was correctly parsed. It will be set of True
    # only when it happens:
    date_parser_marker = False
    
    try:
        if (type(DATASET[ON][0]) not in numeric_data_types):
            # Try to Parse the date:
            try:
                
                DATASET[ON] = (DATASET[ON]).astype('datetime64[ns]')
                # Change the value of the marker to map that the date was correctly parsed:
                date_parser_marker = True
                print(f"Column {ON} successfully converted to numpy.datetime64[ns].\n")     
            
            except:
                pass
    except:
        pass
    
    
    if (row_accross == 'columns'):
        
        AXIS = 1
    
    else:
        # 'rows' or an invalid value was set, so set to 'rows' (Axis = 0)
        AXIS = 0
    
    CLOSED = how_to_close_window
    
    # Now all the parameters for the rolling method are set. Calculate the dataframe
    # for the selected statistic:
    
    if (window_statistics == 'mean'):
        
        rolling_window_df = DATASET.rolling(window = WINDOW, min_periods = MIN_PERIODS, center = CENTER, win_type = WIN_TYPE, on = ON, axis = AXIS, closed = CLOSED).mean()
        print(f"Calculated rolling mean for a window size of {WINDOW}. Returning the rolling \'mean\' dataframe.\n")
    
    elif (window_statistics == 'std'):
        
        rolling_window_df = DATASET.rolling(window = WINDOW, min_periods = MIN_PERIODS, center = CENTER, win_type = WIN_TYPE, on = ON, axis = AXIS, closed = CLOSED).std()
        print(f"Calculated rolling standard deviation for a window size of {WINDOW}. Returning the rolling \'std\' dataframe.\n")
    
    elif (window_statistics == 'sum'):
        
        rolling_window_df = DATASET.rolling(window = WINDOW, min_periods = MIN_PERIODS, center = CENTER, win_type = WIN_TYPE, on = ON, axis = AXIS, closed = CLOSED).sum()
        print(f"Calculated rolling sum for a window size of {WINDOW}. Returning the rolling \'sum\' dataframe.\n")
    
    elif (window_statistics == 'difference'):
        
        # Create a list of the columns that can be differentiated and of those that cannot be.
        diff_columns = []
        excluded_columns = []
        for column in list(DATASET.columns):
            
            if (type(DATASET[column][0]) in numeric_data_types):
                diff_columns.append(column)
            
            else:
                
                if ((column == ON) & (date_parser_marker == True)):
                    # This is the column we converted to date. Set it as the index.
                    # It will allow us to calculate the differences without losing this
                    # information
                    DATASET = DATASET.set_index(column)
                
                else:
                    excluded_columns.append(column)
        
        # Select only the columns in diff_columns:
        DATASET= DATASET[diff_columns]
        
        if (len(excluded_columns) > 0):
            print(f"It is not possible to calculate the differences for columns in {excluded_columns}, so they were removed.\n")
        
        rolling_window_df = DATASET.diff(periods = WINDOW, axis = AXIS)
        print(f"Calculated discrete differences ({WINDOW} periods). Returning the differentiated dataframe.\n")
    
    else:
        print("Please, select a valid rolling window function: \'mean\', \'std\', \'sum\', or \'difference\'.")
        return "error"
    
    # drop missing values generated:
    if (drop_missing_values):
        # Run of it is True. Do not reset index for mode 'difference'.
        # In this mode, the index was set as the date.
        rolling_window_df.dropna(axis = 0, how = 'any', inplace = True)
        
        if (window_statistics != 'difference'):
            rolling_window_df.reset_index(drop = True, inplace = True)
    
    print("Check the rolling dataframe:\n")
    print(rolling_window_df)
        
    return rolling_window_df


def seasonal_decomposition (df, response_column_to_analyze, column_with_timestamps = None, decomposition_mode = "additive", maximum_number_of_cycles_or_periods_to_test = 100, x_axis_rotation = 70, y_axis_rotation = 0, grid = True, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import statsmodels as sm
    from statsmodels.tsa.seasonal import DecomposeResult
    from statsmodels.tsa.seasonal import seasonal_decompose
    
    #Check seasonal_decompose and DecomposeResult documentations:
    # https://www.statsmodels.org/dev/generated/statsmodels.tsa.seasonal.seasonal_decompose.html
    # https://www.statsmodels.org/dev/generated/statsmodels.tsa.seasonal.DecomposeResult.html#statsmodels.tsa.seasonal.DecomposeResult
    # seasonal_decompose results in an object from class DecomposeResult.
    # Check the documentation of the .plot method for DecomposeResult objects:
    # https://www.statsmodels.org/dev/generated/statsmodels.tsa.seasonal.DecomposeResult.plot.html#statsmodels.tsa.seasonal.DecomposeResult.plot
    
    #number_of_periods_to_forecast = 7
    # integer value representing the total of periods to forecast. The periods will be in the
    # unit (dimension) of the original dataset. If 1 period = 1 day, 7 periods will represent
    # seven days.
    
    # df: the whole dataframe to be processed.
    
    # response_column_to_analyze: string (inside quotes), 
    # containing the name of the column that will be analyzed.
    # e.g. response_column_to_analyze = "column1" will analyze the column named as 'column1'.
    # WARNING: This must be the response variable
    
    # column_with_timestamps: string (inside quotes), 
    # containing the name of the column containing timestamps.
    # Keep it as None if you want to set the index as the time.
    # e.g. response_column_to_analyze = "column1" will analyze the column named as 'column1'.
    
    # MAXIMUM_NUMBER_OF_CYCLES_OR_PERIODS_TO_TEST = integer (minimum value is 2) representing
    # the total of cycles or periods that may be present on time series. The function will loop through
    # 2 to MAXIMUM_NUMBER_OF_CYCLES_OR_PERIODS_TO_TEST to find the number that minimizes the sum of
    # modules (absolute values) of the residues.
    # e.g. MAXIMUM_NUMBER_OF_CYCLES_OR_PERIODS_TO_TEST = 4 will test 2, 3 and 4 cycles on the time series.

    # decomposition_mode = "additive" - manipulate the parameter 'model' from seasonal_decompose.
    # model = decomposition_mode
    # Alternatively, set decomposition_mode = "multiplicative" for decomposing as a multiplicative time series.
    
    ## 'additive' model: An additive model suggests that the components are added together as: 
    ## y(t) = Level + Trend + Seasonality + Noise
    ## An additive model is linear where changes over time are consistently made by the same amount. A linear trend is 
    ## a straight line. A linear seasonality has the same frequency (width of cycles) and amplitude (height of cycles).
    
    ## 'multiplicative' model: A multiplicative model suggests that the components are multiplied together as:
    ## y(t) = Level * Trend * Seasonality * Noise
    ## A multiplicative model is nonlinear, such as quadratic or exponential. Changes increase or decrease over time.
    ## A nonlinear trend is a curved line. A non-linear seasonality has an increasing or decreasing frequency 
    ## and/or amplitude over time.
    # https://machinelearningmastery.com/decompose-time-series-data-trend-seasonality/#:~:text=The%20statsmodels%20library%20provides%20an%20implementation%20of%20the,careful%20to%20be%20critical%20when%20interpreting%20the%20result.
    
    
    # Set a local copy of the dataframe to manipulate?
    DATASET = df.copy(deep = True)
    
    #Check if there is a column with the timestamps:
    if not (column_with_timestamps is None):
        
        DATASET = DATASET.sort_values(by = column_with_timestamps)
        
        x = DATASET[column_with_timestamps].copy()
        
        # try to convert it to datetime:
        try:
            x = x.astype(np.datetime64)
        
        except:
            pass
        
        # Set it as index to include it in the seasonal decomposition model:
        DATASET = DATASET.set_index(column_with_timestamps)
    
    else:
        #the index will be used to plot the charts:
        x = DATASET.index
        
    # Extract the time series from the dataframe:
    Y = DATASET[response_column_to_analyze]
    
    # Set the parameters for modelling:
    MODEL = decomposition_mode
    MAXIMUM_NUMBER_OF_CYCLES_OR_PERIODS_TO_TEST = maximum_number_of_cycles_or_periods_to_test
    
    # Check if the arguments are valid:
    if MODEL not in ["additive", "multiplicative"]:
        # set model as 'additive'
        MODEL = "additive"
    
    print(f"Testing {MODEL} model for seasonal decomposition.\n")
    
    try:
        MAXIMUM_NUMBER_OF_CYCLES_OR_PERIODS_TO_TEST = int(MAXIMUM_NUMBER_OF_CYCLES_OR_PERIODS_TO_TEST)
        # If it is lower than 2, make it equals to 2:
        if (MAXIMUM_NUMBER_OF_CYCLES_OR_PERIODS_TO_TEST < 2):
            MAXIMUM_NUMBER_OF_CYCLES_OR_PERIODS_TO_TEST = 2
        
        print(f"Testing the presence of until {MAXIMUM_NUMBER_OF_CYCLES_OR_PERIODS_TO_TEST} periods or cycles in the time series.\n")
    
    except:
        print("Input a valid MAXIMUM_NUMBER_OF_CYCLES_OR_PERIODS_TO_TEST. It must be an integer higher or equal to 2, representing the maximum possible number of cycles or periods present in time series.\n")
        return "error"
    
    # Now, let's loop through the possible number of cycles and periods:
    # Start a dictionary to store the number of cycles and the correspondent sum of 
    # absolute values of the residues:
    residues_dict = {}
    
    for TOTAL_OF_CYCLES in range (2, (MAXIMUM_NUMBER_OF_CYCLES_OR_PERIODS_TO_TEST + 1)):
        
        # TOTAL_OF_CYCLES is an integer looping from TOTAL_OF_CYCLES = 2 to
        # TOTAL_OF_CYCLES = (MAXIMUM_NUMBER_OF_CYCLES_OR_PERIODS_TO_TEST + 1) - 1 = (MAXIMUM_NUMBER_OF_CYCLES_OR_PERIODS_TO_TEST)
        
        try:
        
            # Start an instance (object) from class DecomposeResult
            # Set this object as the resultant from seasonal_decompose
            decompose_res_obj = seasonal_decompose(Y, model = MODEL, period = TOTAL_OF_CYCLES, two_sided = True)
            # decompose_res_obj is an instance (object) from class DecomposeResult

            # Get the array of the residues. Convert it to NumPy array to guarantee the vectorial operations:
            residues_array = np.array(decompose_res_obj.resid)
            # Convert the values in the array to the absolute values:
            residues_array = abs(residues_array)
            # Get the sum of the absolute residues:
            sum_of_abs_residues = np.sum(residues_array)

            # Store it in the dictionary (value correspondent to the key TOTAL_OF_CYCLES):
            residues_dict[TOTAL_OF_CYCLES] = sum_of_abs_residues
        
        except:
            # There are no sufficient measurements to test this total of cycles
            pass
    
    # get the list of dictionary's values:
    dict_vals = list(residues_dict.values())
    # Get the minimum value on the list:
    minimum_residue = min(dict_vals)
    # Get the index of minimum_residue on the list:
    minimum_residue_index = dict_vals.index(minimum_residue)
    
    # Now, retrieve OPTIMAL_TOTAL_CYCLES. It will be the value with index minimum_residue_index
    # in the list of keys:
    list_of_keys = list(residues_dict.keys())
    OPTIMAL_TOTAL_CYCLES = list_of_keys[minimum_residue_index]
    
    print(f"Number of total cycles or periods in time series: {OPTIMAL_TOTAL_CYCLES}.\n")
    
    # Start an instance (object) from class DecomposeResult
    # Set this object as the resultant from seasonal_decompose
    decompose_res_obj = seasonal_decompose(Y, model = MODEL, period = OPTIMAL_TOTAL_CYCLES, two_sided = True)
    # decompose_res_obj is an instance (object) from class DecomposeResult
    
    # Create a dictionary with the resultants from the seasonal decompose:
    # These resultants are obtained as attributes of the decompose_res_obj
    
    number_of_observations_used = decompose_res_obj.nobs
    print(f"Seasonal decomposition concluded using {number_of_observations_used} observations.")
    
    decompose_dict = {
        
        'timestamp': x,
        "observed_data": decompose_res_obj.observed,
        "seasonal_component": decompose_res_obj.seasonal,
        "trend_component": decompose_res_obj.trend,
        "residuals": decompose_res_obj.resid
    }
    
    # Convert it into a returned dataframe:
    seasonal_decompose_df = pd.DataFrame(data = decompose_dict)
    
    print("Check the first 10 rows of the seasonal decompose dataframe obtained:\n")
    print(seasonal_decompose_df.head(10))
    print("\n") # line break
    print(f"Check the time series decomposition graphics for the {MODEL} model:\n")
    
    # Plot parameters:
    x = decompose_dict['timestamp']
    y1 = decompose_dict['observed_data']
    lab1 = "observed_data"
    y2 = decompose_dict['seasonal_component']
    lab2 = 'seasonal_component'
    y3 = decompose_dict['trend_component']
    lab3 = 'trend_component'
    y4 = decompose_dict['residuals']
    lab4 = 'residuals'
    
    plot_title = "seasonal_decomposition_for_" + response_column_to_analyze
    
    # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
    # so that the bars do not completely block other views.
    OPACITY = 0.95
    
    # Now, let's obtain the graphic:
    # Create the figure:
    fig, ax = plt.subplots(4, 1, sharex = True, figsize = (12, 8)) 
    # sharex = share axis X
    # number of subplots equals to the total of series to plot (in this case, 4)
    
    ax[0].plot(x, y1, linestyle = '-', marker = '', color = 'darkblue', alpha = OPACITY, label = lab1)
    # Set title only for this subplot:
    ax[0].set_title(plot_title)
    ax[0].grid(grid)
    ax[0].legend(loc = 'upper right')
    # position options: 'upper right'; 'upper left'; 'lower left'; 'lower right';
    # 'right', 'center left'; 'center right'; 'lower center'; 'upper center', 'center'
    # https://www.statology.org/matplotlib-legend-position/
    
    ax[1].plot(x, y2, linestyle = '-', marker = '', color = 'crimson', alpha = OPACITY, label = lab2)
    # Add the y-title only for this subplot:
    ax[1].set_ylabel(response_column_to_analyze)
    ax[1].grid(grid)
    ax[1].legend(loc = 'upper right')
    
    ax[2].plot(x, y3, linestyle = '-', marker = '', color = 'darkgreen', alpha = OPACITY, label = lab3)
    ax[2].grid(grid)
    ax[2].legend(loc = 'upper right')
    
    ax[3].plot(x, y4, linestyle = '', marker = 'o', color = 'red', alpha = OPACITY, label = lab4)
    # Add an horizontal line in y = zero:
    ax[3].axhline(0, color = 'black', linestyle = 'dashed', alpha = OPACITY)
    # Set the x label only for this subplot
    ax[3].set_xlabel('timestamp')
    ax[3].grid(grid)
    ax[3].legend(loc = 'upper right')
    
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
            file_name = "seasonal_decomposition"

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
    
    #Finally, return the full dataframe:
    print("The full dataframe obtained from the decomposition was returned as seasonal_decompose_df.")
    
    return seasonal_decompose_df

