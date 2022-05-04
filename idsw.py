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
                    # verbose = True for showing number of NA values placed in non-numeric columns.
                    #  parse_dates = True: try parsing the index; infer_datetime_format = True : If True and parse_dates is enabled, pandas will attempt to infer the format of the datetime strings in 
                    # the columns, and if it can be inferred, switch to a faster method of parsing them. In some cases this can increase the 
                    # parsing speed by 5-10x.
                    
                else:
                    
                    try:
                        
                        # Try using the character specified as the argument txt_csv_col_sep:
                        dataset = pd.read_csv(file_path, sep = txt_csv_col_sep, na_values = how_missing_values_are_registered, verbose = True, parse_dates = True, infer_datetime_format = True, decimal = decimal_separator)
                        # verbose = True for showing number of NA values placed in non-numeric columns.
                        #  parse_dates = True: try parsing the index; infer_datetime_format = True : If True and parse_dates is enabled, pandas will attempt to infer the format of the datetime strings in 
                        # the columns, and if it can be inferred, switch to a faster method of parsing them. In some cases this can increase the 
                        # parsing speed by 5-10x.
                    
                    except:
                        # An error was raised, the separator is not valid
                        print(f"Enter a valid column separator for the {file_extension} file, like: \'comma\' or \'whitespace\'.")


            else:
                # has_header == False

                if ((txt_csv_col_sep == "comma") | (txt_csv_col_sep == ",")):

                    dataset = pd.read_csv(file_path, header = None, na_values = how_missing_values_are_registered, verbose = True, parse_dates = True, infer_datetime_format = True, decimal = decimal_separator)
                    # verbose = True for showing number of NA values placed in non-numeric columns.
                    #  parse_dates = True: try parsing the index; infer_datetime_format = True : If True and parse_dates is enabled, pandas will attempt to infer the format of the datetime strings in 
                    # the columns, and if it can be inferred, switch to a faster method of parsing them. In some cases this can increase the 
                    # parsing speed by 5-10x.
                    
                elif ((txt_csv_col_sep == "whitespace") | (txt_csv_col_sep == " ")):

                    dataset = pd.read_csv(file_path, delim_whitespace = True, header = None, na_values = how_missing_values_are_registered, verbose = True, parse_dates = True, infer_datetime_format = True, decimal = decimal_separator)
                    # verbose = True for showing number of NA values placed in non-numeric columns.
                    #  parse_dates = True: try parsing the index; infer_datetime_format = True : If True and parse_dates is enabled, pandas will attempt to infer the format of the datetime strings in 
                    # the columns, and if it can be inferred, switch to a faster method of parsing them. In some cases this can increase the 
                    # parsing speed by 5-10x.
                    
                else:
                    
                    try:
                        
                        # Try using the character specified as the argument txt_csv_col_sep:
                        dataset = pd.read_csv(file_path, sep = txt_csv_col_sep, header = None, na_values = how_missing_values_are_registered, verbose = True, parse_dates = True, infer_datetime_format = True, decimal = decimal_separator)
                        # verbose = True for showing number of NA values placed in non-numeric columns.
                        #  parse_dates = True: try parsing the index; infer_datetime_format = True : If True and parse_dates is enabled, pandas will attempt to infer the format of the datetime strings in 
                        # the columns, and if it can be inferred, switch to a faster method of parsing them. In some cases this can increase the 
                        # parsing speed by 5-10x.
                    
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
            
        if (sheet_to_load is not None):        
        #Case where the user specifies which sheet of the Excel file should be loaded.
            
            if (has_header == True):
                
                dataset = pd.read_excel(file_path, sheet_name = sheet_to_load, na_values = how_missing_values_are_registered, verbose = True, parse_dates = True, infer_datetime_format = True, decimal = decimal_separator)
                # verbose = True for showing number of NA values placed in non-numeric columns.
                #  parse_dates = True: try parsing the index; infer_datetime_format = True : If True and parse_dates is enabled, pandas will attempt to infer the format of the datetime strings in 
                # the columns, and if it can be inferred, switch to a faster method of parsing them. In some cases this can increase the 
                # parsing speed by 5-10x.
                
            else:
                #No header
                dataset = pd.read_excel(file_path, sheet_name = sheet_to_load, header = None, na_values = how_missing_values_are_registered, verbose = True, parse_dates = True, infer_datetime_format = True, decimal = decimal_separator)
                # verbose = True for showing number of NA values placed in non-numeric columns.
                #  parse_dates = True: try parsing the index; infer_datetime_format = True : If True and parse_dates is enabled, pandas will attempt to infer the format of the datetime strings in 
                # the columns, and if it can be inferred, switch to a faster method of parsing them. In some cases this can increase the 
                # parsing speed by 5-10x.
        else:
            #No sheet specified
            if (has_header == True):
                
                dataset = pd.read_excel(file_path, na_values = how_missing_values_are_registered, verbose = True, parse_dates = True, infer_datetime_format = True, decimal = decimal_separator)
                # verbose = True for showing number of NA values placed in non-numeric columns.
                #  parse_dates = True: try parsing the index; infer_datetime_format = True : If True and parse_dates is enabled, pandas will attempt to infer the format of the datetime strings in 
                # the columns, and if it can be inferred, switch to a faster method of parsing them. In some cases this can increase the 
                # parsing speed by 5-10x.
                
            else:
                #No header
                dataset = pd.read_excel(file_path, header = None, na_values = how_missing_values_are_registered, verbose = True, parse_dates = True, infer_datetime_format = True, decimal = decimal_separator)
                # verbose = True for showing number of NA values placed in non-numeric columns.
                #  parse_dates = True: try parsing the index; infer_datetime_format = True : If True and parse_dates is enabled, pandas will attempt to infer the format of the datetime strings in 
                # the columns, and if it can be inferred, switch to a faster method of parsing them. In some cases this can increase the 
                # parsing speed by 5-10x.
                
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


def MERGE_ON_TIMESTAMP (df_left, df_right, left_key, right_key, how_to_join = "inner", merge_method = 'ordered', merged_suffixes = ('_left', '_right'), asof_direction = 'nearest', ordered_filling = 'ffill'):
    
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
    
    if (merge_method == 'ordered'):
    
        if (ordered_filling == 'ffill'):
            
            merged_df = pd.merge_ordered(df_left, df_right, left_on = left_key, right_on = right_key, how = how_to_join, suffixes = merged_suffixes, fill_method='ffill')
        
        else:
            
            merged_df = pd.merge_ordered(df_left, df_right, left_on = left_key, right_on = right_key, how = how_to_join, suffixes = merged_suffixes)
    
    elif (merge_method == 'asof'):
        
        merged_df = pd.merge_asof(df_left, df_right, left_on = left_key, right_on = right_key, suffixes = merged_suffixes, direction = asof_direction)
    
    else:
        
        print("You did not enter a valid merge method for this function, \'ordered\' or \'asof\'.")
        print("Then, applying the conventional Pandas .merge method, followed by .sort_values method.")
        
        #Pandas sort_values method: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html
        
        merged_df = df_left.merge(df_right, left_on = left_key, right_on = right_key, how = how_to_join, suffixes = merged_suffixes)
        merged_df = merged_df.sort_values(by = merged_df.columns[0], ascending = True)
        #sort by the first column, with index 0.
    
    # Now, reset index positions:
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
    
    # check if the keys are the same:
    boolean_check = (left_key == right_key)
    # if boolean_check is True, we will merge using the on parameter, instead of left_on and right_on:
    
    if (boolean_check): # runs if it is True:
        
        merged_df = df_left.merge(df_right, on = left_key, how = how_to_join, suffixes = merged_suffixes)
    
    else:
        # use left_on and right_on
        merged_df = df_left.merge(df_right, left_on = left_key, right_on = right_key, how = how_to_join, suffixes = merged_suffixes)
    
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
    
    # Check axis:
    if (what_to_append == 'rows'):
        
        AXIS = 0
    
    elif (what_to_append == 'columns'):
        
        AXIS = 1
    
    else:
        print("No valid string was input to what_to_append, so appending rows (vertical append, equivalent to SQL UNION).")
        AXIS = 0
    
    if (union_join_type == 'inner'):
        
        print("Warning: concatenating dataframes using the \'inner\' join method, that removes missing values.")
        concat_df = pd.concat(list_of_dataframes, axis = AXIS, ignore_index = ignore_index_on_union, sort = sort_values_on_union, join = union_join_type)
    
    else:
        
        #In case None or an invalid value is provided, use the default 'outer', by simply
        # not declaring the 'join':
        concat_df = pd.concat(list_of_dataframes, axis = AXIS, ignore_index = ignore_index_on_union, sort = sort_values_on_union)
    
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
    
    #Create a local copy of the dataframe to manipulate:
    DATASET = df
    
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
    
    #Create a local copy of the dataframe to manipulate:
    DATASET = df
    
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
    
    # Create a local copy of the dataset to manipulate:
    DATASET = df
    
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
    print("WARNING: this function requires a time column and at least one numeric column to run. If your dataframe does not contain numeric column, create one by simply making it equals to zero. For instance, for a dataframe df, declare and run df[\'numeric_col\'] = 0 to start a numeric variable named \'numeric_col\'.\n")
    
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
        
    #aggregate_function: Pandas aggregation method: 'mean', 'median', 'std', 'sum', 'min'
    # 'max', etc. The default is 'mean'. Then, if no aggregate is provided, 
    # the mean will be calculated.
    
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
    
    # Set a copy of the dataframe to manipulate:
    df_copy = df
    
    
    #1. Start a list to store the Pandas timestamps:
    timestamp_list = []
    
    #2. Loop through each element of the timestamp column, and apply the function
    # to guarantee that all elements are Pandas timestamps
    
    for timestamp in df_copy[timestamp_tag_column]:
        #Access each element 'timestamp' of the series df[timestamp_tag_column]
        timestamp_list.append(pd.Timestamp(timestamp, unit = 'ns'))
    
    #3. Create a column in the dataframe that will be used as key for the Grouper class
    # The grouper requires a column in the dataframe - it cannot use a list for that.
    # Simply copy the list as the new column:
    df_copy['timestamp_obj'] = timestamp_list
    
    # Now we have a list correspondent to timestamp_tag_column, but only with
    # Pandas timestamp objects
    
    # In this function, we do not convert the Timestamp to a datetime64 object.
    # That is because the Grouper class specifically requires a Pandas Timestamp
    # object to group the dataframes.
    
    # Let's group the dataframe and save the grouped one as grouped_df
    
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
    
    
    #### LET'S AGGREGATE THE CATEGORICAL VARIABLES
    ### Pandas does not allow us to directly aggregate the categorical features in terms of mode,
    ### their most common value. So, we use an indirect approach:
    # 1. We use the aggregated timestamps obtained for the numeric columns as template:
    # For instance, if we aggregated by day, the aggregated timestamps will show different days.
    # Since this is an aggregated timestamp, the original dataframe contains several entries for that
    # day.
    # 2. We loop through each row of the aggregated dataframe to obtain the aggregated timestamps and
    # the correct number of rows.
    # 3. Then, we loop through each row of the original dataframe and check if that row belongs to the
    # aggregated timestamp being considered. Again, for the aggregation by days example: we look for
    # each one of the original rows that would be aggregated in a same day. Then, we save the
    # values of that categorical variable in that time interval as a list (in other words, the
    # values that belong to a same day are saved in a list).
    # 3.1. Basically, to verify if a value belongs to the aggregated interval, we must check the 
    # attributes of the Pandas Timestamps. If we are aggregating by 'seconds', so we are looking for
    # timestamps on the original dataframe that have the same year, month, day, hour, minute and second
    # as the aggregated times. If we are aggregating by days, the year, month and day must match. If we
    # are aggregating by year, only the years must match, and so on.
    # 4. After we obtained the list of values, we simply calculate the mode with scipy.stats.mode
    # function. We save all modes in a list of modes, with one mode for each aggregated dataframe row.
    # 5. Finally, we create a new column in the new dataframe for the categorical variable. This column
    # will be the list of modes.
    
    
    ## Check if there is a list of categorical features. If there is, run the next block of code:
    
    if not (list_of_categorical_columns is None):
        # There are categorical columns to aggregate too:

        # Firstly, let's obtain Timestamps objects from the aggregated column 'Timestamp_grouped'

        # Start a list:
        agg_timestamps = []

        for timestamp in grouped_df['Timestamp_grouped']:
            #Access each element 'timestamp' of the series grouped_df['Timestamp_grouped']
            agg_timestamps.append(pd.Timestamp(timestamp, unit = 'ns'))


        ### Aggregation loops:
        # - a main for loop for selecting the categorical column;
        # - a nested for loop for going through the rows of the aggregated dataframe containing
        # only numerical columns and the aggregated timestamps;
        # - a while loop nested into the nested for loop for going through the rows of the original
        # dataframe.

        # Loop through each column in the list list_of_categorical_columns:
        for cat_var in list_of_categorical_columns:

            # Each element of the list list_of_categorical_columns is referred as 'cat_var'

            # Let's fill grouped_df with the modes of the categorical features. The modes
            # for 'cat_var' will be stored as the list cat_var_modes:
            cat_var_modes = []

            # Now, loop through each row from the dataframe grouped_df. For each row, we must
            # store a mode (mode of the categorical variable for that aggregated time) in the
            # list cat_var_modes. After obtaining all the modes, the column cat_var of the
            # grouped_df will be the list cat_var_modes

            k = 0
            # Row from the dataframe df_copy, starting from 0 (1st row)
            # The counting of k will restart only when the column changes, avoiding
            # testing the first rows several times

            # Start a list to store the values of the categorical variable obtained during the
            # grouped time interval:
            vals_list = []
            # The mode of the values stored in vals_list will be the grouped value for the aggregated
            # time interval, added to cat_var_modes list

            # Loop from row i = 0 to row len(grouped_df)-1, index of the last row of the dataset
            # grouped_df:
            for i in range (0, len(grouped_df)):

                boolean_filter = True
                # Condition for starting the loop

                while (boolean_filter): # while it is True, run it:

                    # Add the element on row k from the series df_copy[cat_var]
                    # to the list vals_list:
                    vals_list.append((df_copy[cat_var][k]))
                    # Go to the next row from df_copy:
                    k = k + 1

                    # Update boolean_filter according to the frequency unit defined:

                    if (grouping_frequency_unit == 'second'):
                        # we must check the equality for all values: year, month, day, hour,
                        # minute, and second

                        # Compare the element on row k from the list timestamp_list (timestamp_list[k]),
                        # which contains the Pandas timestamp referrent to df_copy, with the element 
                        # on row i from the list agg_timestamps (agg_timestamps[i]), with the aggregated
                        # pandas Timestamp object.
                        # We need the Pandas dataframes to access the attributes year, month, day, etc.
                        boolean_filter = (((timestamp_list[k]).year) == ((agg_timestamps[i]).year))
                        boolean_filter = boolean_filter & (((timestamp_list[k]).month) == ((agg_timestamps[i]).month))
                        boolean_filter = boolean_filter & (((timestamp_list[k]).day) == ((agg_timestamps[i]).day))
                        boolean_filter = boolean_filter & (((timestamp_list[k]).hour) == ((agg_timestamps[i]).hour))
                        boolean_filter = boolean_filter & (((timestamp_list[k]).minute) == ((agg_timestamps[i]).minute))
                        boolean_filter = boolean_filter & (((timestamp_list[k]).second) == ((agg_timestamps[i]).second))

                    elif (grouping_frequency_unit == 'minute'):
                        # we must check the equality for all values: year, month, day, hour, and
                        # minute
                        boolean_filter = (((timestamp_list[k]).year) == ((agg_timestamps[i]).year))
                        boolean_filter = boolean_filter & (((timestamp_list[k]).month) == ((agg_timestamps[i]).month))
                        boolean_filter = boolean_filter & (((timestamp_list[k]).day) == ((agg_timestamps[i]).day))
                        boolean_filter = boolean_filter & (((timestamp_list[k]).hour) == ((agg_timestamps[i]).hour))
                        boolean_filter = boolean_filter & (((timestamp_list[k]).minute) == ((agg_timestamps[i]).minute))

                    elif (grouping_frequency_unit == 'hour'):
                        # we must check the equality for all values: year, month, day, and hour
                        boolean_filter = (((timestamp_list[k]).year) == ((agg_timestamps[i]).year))
                        boolean_filter = boolean_filter & (((timestamp_list[k]).month) == ((agg_timestamps[i]).month))
                        boolean_filter = boolean_filter & (((timestamp_list[k]).day) == ((agg_timestamps[i]).day))
                        boolean_filter = boolean_filter & (((timestamp_list[k]).hour) == ((agg_timestamps[i]).hour))

                    elif (grouping_frequency_unit == 'day'):
                        # we must check the equality for all values: year, month, and day
                        boolean_filter = (((timestamp_list[k]).year) == ((agg_timestamps[i]).year))
                        boolean_filter = boolean_filter & (((timestamp_list[k]).month) == ((agg_timestamps[i]).month))
                        boolean_filter = boolean_filter & (((timestamp_list[k]).day) == ((agg_timestamps[i]).day))

                    elif (grouping_frequency_unit == 'week'):
                        # we must check the equality for all values: year, month, and week
                        boolean_filter = (((timestamp_list[k]).year) == ((agg_timestamps[i]).year))
                        boolean_filter = boolean_filter & (((timestamp_list[k]).month) == ((agg_timestamps[i]).month))
                        boolean_filter = boolean_filter & (((timestamp_list[k]).week) == ((agg_timestamps[i]).week))

                    elif (grouping_frequency_unit == 'month'):
                        # we must check the equality for all values: year, and month
                        boolean_filter = (((timestamp_list[k]).year) == ((agg_timestamps[i]).year))
                        boolean_filter = boolean_filter & (((timestamp_list[k]).month) == ((agg_timestamps[i]).month))

                    else: # grouping_frequency_unit = 'year'
                        # we must check the equality for only the year
                        boolean_filter = (((timestamp_list[k]).year) == ((agg_timestamps[i]).year))

                    # The filter is updated so it comes back to the start of the loop. If the filter is True,
                    # The while loop continues. If not, the while loop is finished and we go to the end
                    # of the for loop for the row i.

                # Now we left the while loop and returned to the nested for loop (from i = 0 to the last row).
                # So, for each row i from grouped_df, we have a list
                # of categorical values vals_list. These are the values seem for the variable
                # cat_var during the whole interval that is being aggregated. We have to retrieve the
                # mode, the most common value during the aggregated interval:
                mode_for_row_i = stats.mode(np.array(vals_list))[0][0]

                # It is possible to set the following argument to stats.mode:
                # nan_policy = 'omit': do not count the missing values to calculate the mode (not the default)
                # If we omit the missing values, they will be substituted by zeros.
                
                # The numpy.array function guarantees the reading with the correct format
                # Consider: a = np.array(['a', 'a', 'b'])
                # The stats.mode function stats.mode(a) returns an array as: 
                # ModeResult(mode=array(['a'], dtype='<U1'), count=array([2]))
                # If we select the first element from this array, stats.mode(a)[0], the function will 
                # return an array as array(['a'], dtype='<U1'). 
                # We want the first element from this array stats.mode(a)[0][0], 
                # which will return a string like 'a'

                # Append the value mode_for_row_i to the list cat_var_modes:
                cat_var_modes.append(mode_for_row_i)

            # Now, we left the nested for loop (from the first to the last row) and are at the end of the
            # main for loop (which tests each 'cat_var' variable in the list of categorical features).
            # Before going to the next categorical variable, create a column cat_var in the dataframe
            # grouped_df as the list cat_var_modes:
            grouped_df[cat_var] = cat_var_modes

            # Now that we grouped the categorical variable 'cat_var' in terms of mode, we can go to the
            # nest categorical feature.

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
    
    
    # Create a local copy of the dataframe to manipulate:
    DATASET = df
    
    # Check if the list of column names is None. If it is, make it equals to the list of extracted
    # information:
    if (list_of_new_column_names is None):
        
        list_of_new_column_names = list_of_info_to_extract
    
    # START: CONVERT ALL TIMESTAMPS/DATETIMES/STRINGS TO pandas.Timestamp OBJECTS.
    # This will prevent any compatibility problems.
    
    # The pd.Timestamp function can handle a single timestamp per call. Then, we must
    # loop trough the series, and apply the function to each element.
    
    #1. Start a list to store the Pandas timestamps:
    timestamp_list = []
    
    #2. Loop through each element of the timestamp column, and apply the function
    # to guarantee that all elements are Pandas timestamps
    
    for timestamp in DATASET[timestamp_tag_column]:
        #Access each element 'timestamp' of the series df[timestamp_tag_column]
        timestamp_list.append(pd.Timestamp(timestamp, unit = 'ns'))
    
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
    
    #1. Start a list to store the Pandas timestamps:
    timestamp_list = []
    
    #2. Loop through each element of the timestamp column, and apply the function
    # to guarantee that all elements are Pandas timestamps
    
    for timestamp in df[timestamp_tag_column]:
        #Access each element 'timestamp' of the series df[timestamp_tag_column1]
        timestamp_list.append(pd.Timestamp(timestamp, unit = 'ns'))
    
    
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
    df[timestamp_tag_column2] = following_timestamp
    
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
    timedelta_obj = df[timestamp_tag_column2] - df[timestamp_tag_column]
    
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
    
    df[new_timedelta_column_name] = TimedeltaList
      
    # Pandas .head(Y) method results in a dataframe containing the first Y rows of the 
    # original dataframe. The default .head() is Y = 5. Print first 10 rows of the 
    # new dataframe:
    print("Time delays successfully calculated. Check dataset\'s 10 first rows:\n")
    print(df.head(10))
    
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
        return df, avg_delay
    
    #Finally, return the dataframe with the new column:
    
    else: 
        # Return only the dataframe
        return df


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
    
    #1. Start a list to store the Pandas timestamps:
    timestamp_list = []
    
    #2. Loop through each element of the timestamp column, and apply the function
    # to guarantee that all elements are Pandas timestamps
    
    for timestamp in df[timestamp_tag_column1]:
        #Access each element 'timestamp' of the series df[timestamp_tag_column1]
        timestamp_list.append(pd.Timestamp(timestamp, unit = 'ns'))
    
    #3. Create a column in the dataframe that will store the timestamps.
    # Simply copy the list as the column:
    df[timestamp_tag_column1] = timestamp_list
    
    #Repeate these steps for the other column (timestamp_tag_column2):
    # Restart the list, loop through all the column, and apply the pd.Timestamp function
    # to each element, individually:
    timestamp_list = []
    
    for timestamp in df[timestamp_tag_column2]:
        #Access each element 'timestamp' of the series df[timestamp_tag_column2]
        timestamp_list.append(pd.Timestamp(timestamp, unit = 'ns'))
    
    df[timestamp_tag_column2] = timestamp_list
    
    # Pandas Timestamps can be subtracted to result into a Pandas Timedelta.
    # We will apply the delta method from Pandas Timedeltas.
    
    #4. Create a timedelta object as the difference between the timestamps:
    
    # NOTICE: Even though a list could not be submitted to direct operations like
    # sum, subtraction and multiplication, the series and NumPy arrays can. When we
    # copied the list as a new column on the dataframes, we converted the lists to series
    # called df[timestamp_tag_column1] and df[timestamp_tag_column2]. These two series now
    # can be submitted to direct operations.
    
    timedelta_obj = df[timestamp_tag_column1] - df[timestamp_tag_column2]
    
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
    
    df[timedelta_column_name] = TimedeltaList
      
    # Pandas .head(Y) method results in a dataframe containing the first Y rows of the 
    # original dataframe. The default .head() is Y = 5. Print first 10 rows of the 
    # new dataframe:
    print("Timedeltas successfully calculated. Check dataset\'s 10 first rows:\n")
    print(df.head(10))
    
    #Finally, return the dataframe with the new column:
    
    return df


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
    
    #1. Start a list to store the Pandas timestamps:
    timestamp_list = []
    
    #2. Loop through each element of the timestamp column, and apply the function
    # to guarantee that all elements are Pandas timestamps
    
    for timestamp in df[timestamp_tag_column]:
        #Access each element 'timestamp' of the series df[timestamp_tag_column1]
        timestamp_list.append(pd.Timestamp(timestamp, unit = 'ns'))
    
    #3. Create a column in the dataframe that will store the timestamps.
    # Simply copy the list as the column:
    df[timestamp_tag_column] = timestamp_list
    
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
    new_timestamps = df[timestamp_tag_column] + timedelta
     
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
    
    df[new_timestamp_col] = new_timestamps
      
    # Pandas .head(Y) method results in a dataframe containing the first Y rows of the 
    # original dataframe. The default .head() is Y = 5. Print first 10 rows of the 
    # new dataframe:
    print("Timedeltas successfully added. Check dataset\'s 10 first rows:\n")
    print(df.head(10))
    
    #Finally, return the dataframe with the new column:
    
    return df


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
    
    
    # Store the total number of rows as num_rows:
    num_rows = len(df)
    
    
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
        return df
    
    elif ((first_row_index == 0) & (last_row_index == (num_rows - 1))):
        
        #return the dataframe without performing any operation
        print("Sliced dataframe is the original dataframe itself.")
        return df
         
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
    
    sliced_df = df[i:j]
    
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