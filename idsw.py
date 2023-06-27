# FUNCTIONS FROM INDUSTRIAL DATA SCIENCE WORKFLOW (IDSW) PACKAGE
# Extract, transform, and load (ETL) data

# Marco Cesar Prado Soares, Data Scientist Specialist @ Bayer Crop Science LATAM
# marcosoares.feq@gmail.com
# marco.soares@bayer.com

# Import all functions from etl and modelling with no alias
from pims import *
from etl import *
from modelling import *

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
    # list_of_file_names_with_extensions = ['doc.pdf', 'model.pkl']
    
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


def load_pandas_dataframe (file_directory_path, file_name_with_extension, load_txt_file_with_json_format = False, how_missing_values_are_registered = None, has_header = True, decimal_separator = '.', txt_csv_col_sep = "comma", load_all_sheets_at_once = False, sheet_to_load = None, json_record_path = None, json_field_separator = "_", json_metadata_prefix_list = None):
    
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
    ## JSON, txt, or CSV (comma separated values) files. Tables in webpages or html files can also be read.
    
    # file_directory_path - (string, in quotes): input the path of the directory (e.g. folder path) 
    # where the file is stored. e.g. file_directory_path = "/" or file_directory_path = "/folder"
    
    # FILE_NAME_WITH_EXTENSION - (string, in quotes): input the name of the file with the 
    # extension. e.g. FILE_NAME_WITH_EXTENSION = "file.xlsx", or, 
    # FILE_NAME_WITH_EXTENSION = "file.csv", "file.txt", or "file.json"
    # Again, the extensions may be: xls, xlsx, xlsm, xlsb, odf, ods, odt, json, txt or csv. Also,
    # html files and webpages may be also read.
    
    # You may input the path for an HTML file containing a table to be read; or 
    # a string containing the address for a webpage containing the table. The address must start
    # with www or htpp. If a website is input, the full address can be input as FILE_DIRECTORY_PATH
    # or as FILE_NAME_WITH_EXTENSION.
    
    
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
    
    
    ## Parameters for loading Excel files:
    
    # load_all_sheets_at_once = False - This parameter has effect only when for Excel files.
    # If load_all_sheets_at_once = True, the function will return a list of dictionaries, each
    # dictionary containing 2 key-value pairs: the first key will be 'sheet', and its
    # value will be the name (or number) of the table (sheet). The second key will be 'df',
    # and its value will be the pandas dataframe object obtained from that sheet.
    # This argument has preference over sheet_to_load. If it is True, all sheets will be loaded.
    
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
    
    if (file_directory_path is None):
        file_directory_path = ''
    if (file_name_with_extension is None):
        file_name_with_extension = ''
    
    # Create the complete file path:
    file_path = os.path.join(file_directory_path, file_name_with_extension)
    
    # Extract the file extension
    file_extension = os.path.splitext(file_path)[1][1:]
    # os.path.splitext(file_path) is a tuple of strings: the first is the complete file
    # root with no extension; the second is the extension starting with a point: '.txt'
    # When we set os.path.splitext(file_path)[1], we are selecting the second element of
    # the tuple. By selecting os.path.splitext(file_path)[1][1:], we are taking this string
    # from the second character (index 1), eliminating the dot: 'txt'
    
    if(file_extension not in ['xls', 'xlsx', 'xlsm', 'xlsb', 'odf',
                              'ods', 'odt', 'json', 'txt', 'csv', 'html']):
        
        # Check if it is a webpage by evaluating the 3 to 5 initial characters:
        # Notice that 'https' contains 'http'
        if ((file_path[:3] == 'www') | (file_path[:4] == '/www') | (file_path[:4] == 'http')| (file_path[:5] == '/http')):
            file_extension = 'html'

            # If the address starts with a slash (1st character), remove it:
            if (file_path[0] == '/'):
                # Pick all characters from index 1:
                file_path = file_path[1:]
    
        
    # Check if the decimal separator is None. If it is, set it as '.' (period):
    if (decimal_separator is None):
        decimal_separator = '.'
    
    if ((file_extension == 'txt') | (file_extension == 'csv')): 
        # The operator & is equivalent to 'And' (intersection).
        # The operator | is equivalent to 'Or' (union).
        # pandas.read_csv method must be used.
        if (load_txt_file_with_json_format == True):
            
            print("Reading a txt file containing JSON parsed data. A reading error will be raised if you did not set the JSON parameters.\n")
            
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
    
            
    elif (file_extension == 'html'):    
        
        if (has_header == True):
            
            dataset = pd.read_html(file_path, na_values = how_missing_values_are_registered, parse_dates = True, decimal = decimal_separator)
            
        else:
            
            dataset = pd.read_html(file_path, header = None, na_values = how_missing_values_are_registered, parse_dates = True, decimal = decimal_separator)
        
        
    else:
        # If it is not neither a csv nor a txt file, let's assume it is one of different
        # possible Excel files.
        print("Excel file inferred. If an error message is shown, check if a valid file extension was used: \'xlsx\', \'xls\', etc.\n")
        # For Excel type files, Pandas automatically detects the decimal separator and requires only the parameter parse_dates.
        # Firstly, the argument infer_datetime_format was present on read_excel function, but was removed.
        # From version 1.4 (beta, in 10 May 2022), it will be possible to pass the parameter 'decimal' to
        # read_excel function for detecting decimal cases in strings. For numeric variables, it is not needed, though
        
        if (load_all_sheets_at_once == True):
            
            # Corresponds to setting sheet_name = None
            
            if (has_header == True):
                
                xlsx_doc = pd.read_excel(file_path, sheet_name = None, na_values = how_missing_values_are_registered, verbose = True, parse_dates = True)
                # verbose = True for showing number of NA values placed in non-numeric columns.
                #  parse_dates = True: try parsing the index; infer_datetime_format = True : If True and parse_dates is enabled, pandas will attempt to infer the format of the datetime strings in 
                # the columns, and if it can be inferred, switch to a faster method of parsing them. In some cases this can increase the 
                # parsing speed by 5-10x.
                
            else:
                #No header
                xlsx_doc = pd.read_excel(file_path, sheet_name = None, header = None, na_values = how_missing_values_are_registered, verbose = True, parse_dates = True)
            
            # xlsx_doc is a dictionary containing the sheet names as keys, and dataframes as items.
            # Let's convert it to the desired format.
            # Dictionary dict, dict.keys() is the array of keys; dict.values() is an array of the values;
            # and dict.items() is an array of tuples with format ('key', value)
            
            # Create a list of returned datasets:
            list_of_datasets = []
            
            # Let's iterate through the array of tuples. The first element returned is the key, and the
            # second is the value
            for sheet_name, dataframe in (xlsx_doc.items()):
                # sheet_name = key; dataframe = value
                # Define the dictionary with the standard format:
                df_dict = {'sheet': sheet_name,
                            'df': dataframe}
                
                # Add the dictionary to the list:
                list_of_datasets.append(df_dict)
            
            print("\n")
            print(f"A total of {len(list_of_datasets)} dataframes were retrieved from the Excel file.\n")
            print(f"The dataframes correspond to the following Excel sheets: {list(xlsx_doc.keys())}\n")
            print("Returning a list of dictionaries. Each dictionary contains the key \'sheet\', with the original sheet name; and the key \'df\', with the Pandas dataframe object obtained.\n")
            print(f"Check the 10 first rows of the dataframe obtained from the first sheet, named {list_of_datasets[0]['sheet']}:\n")
            
            try:
                # only works in Jupyter Notebook:
                from IPython.display import display
                display((list_of_datasets[0]['df']).head(10))
            
            except: # regular mode
                print((list_of_datasets[0]['df']).head(10))
            
            return list_of_datasets
            
        elif (sheet_to_load is not None):        
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
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(dataset.head(10))
            
    except: # regular mode
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
    
    print(f"JSON object converted to a flat dataframe object. Check the 10 first rows of this dataframe:\n")
    
    try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(dataset.head(10))
            
    except: # regular mode
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


def load_anomaly_detector (saved_file):

    import pickle
    with open(saved_file, 'rb') as opened_file:
            
        attributes = pickle.load(opened_file)
    
    # Instantiate the anomaly_detector object:
    anomaly_detection_model = anomaly_detector()
    # With vars function, it is possible to access the attributes from an object as the keys of a dictionary.
    # Fill each attribute of the anomaly_detection_model:
    for attribute, value in attributes.items():
        vars(anomaly_detection_model)[attribute] = value
    
    return anomaly_detection_model


def import_export_model_list_dict (action = 'import', objects_manipulated = 'model_only', model_file_name = None, dictionary_or_list_file_name = None, directory_path = '', model_type = 'keras', dict_or_list_to_export = None, model_to_export = None, use_colab_memory = False):
    
    import os
    import pickle
    # import dill
    import tarfile
    from zipfile import ZipFile
    # https://docs.python.org/3/library/tarfile.html#tar-examples
    # https://docs.python.org/3/library/zipfile.html#zipfile-objects
    # pickle and dill save the file in binary (bits) serialized mode. So, we must use
    # open 'rb' or 'wb' when calling the context manager. The 'b' stands for 'binary',
    # informing the context manager (with statement) that a bit-file will be processed
    
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
    # model_type = 'keras' for deep learning keras/ tensorflow models with extension .h5
    # model_type = 'tensorflow_general' for generic deep learning tensorflow models containing 
    # custom layers, losses and architectures. Such models are compressed as tar.gz, tar, or zip.
    # model_type = 'sklearn' for models from scikit-learn (non-deep learning)
    # model_type = 'xgb_regressor' for XGBoost regression models (non-deep learning)
    # model_type = 'xgb_classifier' for XGBoost classification models (non-deep learning)
    # model_type = 'arima' for ARIMA model (Statsmodels)
    # model_type = 'prophet' for Facebook Prophet model
    # model_type = 'anomaly_detector' for the Anomaly Detection model
    
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
        from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler, MinMaxScaler
        
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
                import tensorflow as tf
                model_extension = 'h5'
            
            elif (model_type == 'sklearn'):
                from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, LogisticRegression
                from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
                from sklearn.neural_network import MLPRegressor, MLPClassifier
                model_extension = 'pkl'
                #it could be 'dill', though
            
            elif (model_type == 'anomaly_detector'):
                model_extension = 'pkl'
            
            elif (model_type == 'xgb_regressor'):
                from xgboost import XGBRegressor
                model_extension = 'json'
                #it could be 'ubj', though
            
            elif (model_type == 'xgb_classifier'):
                from xgboost import XGBClassifier
                model_extension = 'json'
                #it could be 'ubj', though
            
            elif (model_type == 'arima'):       
                from statsmodels.tsa.arima.model import ARIMA, ARIMAResults
                model_extension = 'pkl'
            
            elif (model_type == 'prophet'):
                from prophet.serialize import model_to_json, model_from_json
                # https://facebook.github.io/prophet/docs/additional_topics.html
                model_extension = 'json'
            
            # Finally, check if it is not the only one which can have several extensions:
            elif (model_type != 'tensorflow_general'):
                print("Enter a valid model_type: keras, tensorflow_general, sklearn, xgb_regressor, xgb_classifier, arima, or prophet.")
                return "error2"
            
        # If there is an extension, add it:
        if (model_type != 'tensorflow_general'):
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
            
                    imported_dict = pickle.load(opened_file)
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
            
                    imported_dict = pickle.load(opened_file)
                
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
            
            elif (model_type == 'tensorflow_general'):
                import tensorflow as tf
                
                print("Warning, save the model in a directory called 'saved_model' (before compressing.)\n")
                # Create a temporary folder in case it does not exist:
                # https://www.geeksforgeeks.org/python-os-makedirs-method/
                # Set exist_ok = True
                os.makedirs("tmp/", exist_ok = True)
                
                if (use_colab_memory == True):
                    
                    key = model_file_name
                     
                    try:
                        model = tf.keras.models.load_model("saved_model")
                        print(f"TensorFlow model successfully imported to environment.")
                    

                    except:
                            
                        try:
                            model = tf.keras.models.load_model("tmp/saved_model")
                            print(f"TensorFlow model: {model_file_name} successfully imported to environment.")

                        except:

                            try:
                                model = tf.keras.models.load_model(model_file_name)
                                print(f"TensorFlow model: {model_file_name} successfully imported to environment.")

                            except:

                                # It is compressed
                                try:
                                    # try tar.gz extension
                                    model_extension = ".tar.gz"
                                    key = key + model_extension
                                    model_path = colab_files_dict[key]

                                    # Open the context manager
                                    with tarfile.open (model_path, 'r:gz') as compressed_model:
                                        #extract all to the tmp directory:
                                        compressed_model.extractall("tmp/")

                                except:

                                    try:
                                        model_extension = ".tar"
                                        key = key + model_extension
                                        model_path = colab_files_dict[key]

                                        # Open the context manager
                                        with tarfile.open (model_path, 'r:') as compressed_model:
                                            #extract all to the tmp directory:
                                            compressed_model.extractall("tmp/")

                                        # if you were not using the context manager, it would be necessary to apply
                                        # close method: tar = tarfile.open(fname, "r:gz"); tar.extractall(); tar.close()
                                    except:
                                        
                                        # try .zip extension
                                        try:
                                            model_extension = ".zip"
                                            key = key + model_extension
                                            model_path = colab_files_dict[key]

                                            # Open the context manager
                                            with ZipFile (model_path, 'r') as compressed_model:
                                                #extract all to the tmp directory:
                                                compressed_model.extractall("tmp/")

                                        except:
                                            print("Failed to load the model. Compress it as zip, tar or tar.gz file.\n")


                                # Compress the directory using tar
                                # https://www.gnu.org/software/tar/manual/tar.html
                                #    ! tar --extract --file=model_path --verbose --verbose tmp/

                                try:
                                    model = tf.keras.models.load_model("tmp/saved_model")
                                    print(f"TensorFlow model: {model_path} successfully imported to Colab environment.")

                                except:
                                    print("Failed to load the model. Save it in a directory named 'saved_model' before compressing.\n")

                else:
                    #standard method
                    # Try simply accessing the directory:
                    
                    try:
                        model = tf.keras.models.load_model("saved_model")
                        print(f"TensorFlow model: successfully imported to environment.")
                    
                    except:

                        try:
                            model = tf.keras.models.load_model("tmp/saved_model")
                            print(f"TensorFlow model: {model_file_name} successfully imported to environment.")

                        except:

                            try:
                                model = tf.keras.models.load_model(model_file_name)
                                print(f"TensorFlow model: {model_file_nameh} successfully imported to environment.")

                            except:

                                # It is compressed
                                try:
                                    model_extension = ".tar"
                                    
                                    # Open the context manager
                                    with tarfile.open ((model_file_name + model_extension), 'r:') as compressed_model:
                                        #extract all to the tmp directory:
                                        compressed_model.extractall("tmp/")
                                        
                                    # if you were not using the context manager, it would be necessary to apply
                                    # close method: tar = tarfile.open(fname, "r:gz"); tar.extractall(); tar.close()
                                
                                except:
                                    
                                    try:
                                        # try tar.gz extension
                                        model_extension = ".tar.gz"
                                    
                                        # Open the context manager
                                        with tarfile.open ((model_file_name + model_extension), 'r:gz') as compressed_model:
                                            #extract all to the tmp directory:
                                            compressed_model.extractall("tmp/")

                                    except:
                                        # try .zip extension
                                        try:
                                            model_extension = ".zip"

                                            # Open the context manager
                                            with ZipFile ((model_file_name + model_extension), 'r') as compressed_model:
                                                #extract all to the tmp directory:
                                                compressed_model.extractall("tmp/")

                                        except:
                                            print("Failed to load the model. Compress it as zip, tar or tar.gz file.\n")


                            try:
                                model = tf.keras.models.load_model("tmp/saved_model")
                                print(f"TensorFlow model: {model_file_name} successfully imported to environment.")

                            except:
                                print("Failed to load the model. Save it in a directory named 'saved_model' before compressing.\n")
  
            elif (model_type == 'sklearn'):
                
                if (use_colab_memory == True):
                    key = model_file_name + "." + model_extension
                    
                    with open(colab_files_dict[key], 'rb') as opened_file:
            
                        model = pickle.load(opened_file)
                    
                    print(f"Scikit-learn model: {key} successfully imported to Colab environment.")
            
                else:
                    #standard method
                    with open(model_path, 'rb') as opened_file:
            
                        model = pickle.load(opened_file)
                
                    print(f"Scikit-learn model successfully imported from {model_path}.")
                    # For loading a pickle model:
                    ## model = pkl.load(open(model_path, 'rb'))
                    # 'rb' stands for read binary (read mode). For writing mode, 'wb', 'write binary'

            elif (model_type == 'anomaly_detector'):

                if (use_colab_memory == True):
                    key = model_file_name + "." + model_extension
                    model = load_anomaly_detector (saved_file = colab_files_dict[key])
                    
                    print(f"Anomaly detection model: {key} successfully imported to Colab environment.")
            
                else:
                    #standard method
                    model = load_anomaly_detector (saved_file = model_path)
                
                    print(f"Anomaly detection model successfully imported from {model_path}.")

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
            
            elif (model_type == 'prophet'):
                
                if (use_colab_memory == True):
                    key = model_file_name + "." + model_extension
                    
                    with open(colab_files_dict[key], 'r') as opened_file:
                        model = model_from_json(opened_file.read())  # Load model

                    print(f"Prophet model: {key} successfully imported to Colab environment.")
            
                else:
                    #standard method
                    with open(model_path, 'r') as fin:
                        model = model_from_json(fin.read())  # Load model

                    print(f"Prophet model successfully imported from {model_path}.")
            

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
            
                    pickle.dump(dict_or_list_to_export, opened_file)
                
                # this functionality requires the previous declaration:
                ## from google.colab import files
                files.download(key)
                
                print(f"Dictionary or list {key} successfully downloaded from Colab environment.")
            
            else:
                #standard method 
                with open(dict_path, 'wb') as opened_file:
            
                    pickle.dump(dict_or_list_to_export, opened_file)
                
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
            
            elif (model_type == 'tensorflow_general'):

                import tensorflow as tf
                
                # Save your model in the SavedModel format
                # Save as a directory named 'saved_model'
                model_to_export.save('saved_model')
                model_path = 'saved_model'
            
                try:
                    model_path = model_path + ".tar.gz"
                    
                    # Open the context manager
                    with tarfile.open (model_path, 'w:gz') as compressed_model:
                        #Add the folder:
                        compressed_model.add('saved_model/')    
                        # if you were not using the context manager, it would be necessary to apply
                        # close method: tar = tarfile.open(fname, "r:gz"); tar.extractall(); tar.close()
                
                except:
                    # try compressing as tar:
                    try:
                        model_path = model_path + ".tar"
                        # Open the context manager
                        with tarfile.open (model_path, 'w:') as compressed_model:
                            #Add the folder:
                            compressed_model.add('saved_model/') 
                    
                    except:
                        # compress as zip:
                        model_path = model_path + ".zip"
                        with ZipFile (model_path, 'w') as compressed_model:
                            compressed_model.write('saved_model/')
                
                if (use_colab_memory == True):
                    
                    key = model_path
                    files.download(key)
                    print(f"TensorFlow model: {key} successfully downloaded from Colab environment.")
            
                else:
                    #standard method
                    print(f"TensorFlow model successfully exported as {model_path}.")

            elif (model_type == 'sklearn'):
                
                if (use_colab_memory == True):
                    ## Download the model
                    key = model_file_name + "." + model_extension
                    
                    with open(key, 'wb') as opened_file:

                        pickle.dump(model_to_export, opened_file)
                    
                    #to save the file, the mode must be set as 'wb' (write binary)
                    files.download(key)
                    print(f"Scikit-learn model: {key} successfully downloaded from Colab environment.")
            
                else:
                    #standard method
                    with open(model_path, 'wb') as opened_file:

                        pickle.dump(model_to_export, opened_file)
                    
                    print(f"Scikit-learn model successfully exported as {model_path}.")
                    # For exporting a pickle model:
                    ## pkl.dump(model_to_export, open(model_path, 'wb'))
            
            elif (model_type == 'anomaly_detector'):
                
                if (use_colab_memory == True):
                    ## Download the model
                    key = model_file_name + "." + model_extension
                    model_to_export.save(path_to_save = key)
                    
                    #to save the file, the mode must be set as 'wb' (write binary)
                    files.download(key)
                    print(f"Anomaly detection model: {key} successfully downloaded from Colab environment.")
            
                else:
                    #standard method
                    model_to_export.save(path_to_save = model_path)
                    
                    print(f"Anomaly detection model successfully exported as {model_path}.")
            
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
        
            elif (model_type == 'prophet'):
                    
                    if (use_colab_memory == True):
                        ## Download the model
                        key = model_file_name + "." + model_extension
                        with open(key, 'w') as opened_file:
                            opened_file.write(model_to_json(model_to_export))  # Save model
                        
                        files.download(key)
                        print(f"Prophet model: {key} successfully downloaded from Colab environment.")
                
                    else:
                        #standard method
                        with open(model_path, 'w') as opened_file:
                            opened_file.write(model_to_json(model_to_export))  # Save model

                        print(f"Prophet model successfully exported as {model_path}.")
        
        print("Export of files completed.")
    
    else:
        print("Enter a valid action, import or export.")


def generateSensitivityAnalysis_datasets (df, simulated_variables, total_bins):
    
    import numpy as np
    import pandas as pd
    from scipy import stats
    
    # df: dataset containing historical data, from which the analysis will be generated.
    
    # SIMULATED_VARIABLES: name (string) or list of names of the variables that will be tested.
    # In the generated dataset, the variable SIMULATED_VARIABLEs will be ranged from its
    # minimum to its maximum value in the original dataset. In turns, the
    # other variables will be kept constant, and with value set as the
    # respective mean value (mean values calculated on the original dataset).
    # e.g. SIMULATED_VARIABLES = "feature1" or SIMULATED_VARIABLES = ['col1', 'col2', 'col3']

    # It allows us to perform situations where the effects of each
    # feature are isolated from the variation of the other variables.

    # Notice that it may be impossible in real scenarios: different constraints
    # and even the need for keeping the operation ongoing may require the
    # parameters to be defined in given levels. Also, it is possible that
    # the variables in the original dataset are all modified simultaneously
    # and with different rules. Finally, all the variables have their own
    # sources of variability interacting in the real data, making it
    # difficult or impossible to observe the correlations present.

    # Applying the generated dataframes to the obtained models allows us to
    # understand how each variable influences the responses (isolately) and
    # how to optimize them.

    
    # TOTAL_BINS: amount of divisions of the tested range, i.e, into how much
    # bins we will split the variables, from their minimum to their maximum
    # values in the original dataset. 
    # The range (max - min) of the variable will be divided into this number 
    # of bins. 
    # So, TOTAL_BINS will be the number of rows of the generated dataset 
    # (in fact, since the division may not result into an integer, the number
    # of rows may be total_bins +- 1).

    # For instance: if a variable Y ranges from 0 to 10, and TOTAL_BINS = 11,
    # we will create a dataset with the following values of Y: 
    # Y = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    # Each generated value will be stored as a different row (an entry)
    # of the generated dataset.
    
    # Start a local copy of the dataframe
    history_dataset = df.copy(deep = True)
    
    # Check if the names are already in a list. If not, add them to a list (brackets):
    if (type(simulated_variables) != list):
        simulated_variables = [simulated_variables]
    
    # Start a dictionary of dataframes:
    simulation_dfs_dict = {}
    
    for variable in simulated_variables:
        
        # Get a list of columns without variable:
        other_columns = list(history_dataset.columns)
        # Get the index from variable in the list other_columns and pop it:
        var_index = other_columns.index(variable)
        other_columns.pop(var_index)
        # If we make var = other_columns.pop(var_index), var would also store the variable name.
        
        # start a tested var list
        var_list = []

        # minimum value assumed by the variable:
        min_var_val = float(history_dataset[variable].min())
        
        # add this minimum value as the first element of the var list:
        var_list.append(min_var_val)

        # maximum value assumed by the variable:
        max_var_val = float(history_dataset[variable].max())
        # We apply the float command to convert the descriptive statistics obtained in describe method
        # into real (float) values to avoid obtaining them as arrays.

        # tested range: range for the sensitivity analysis: max - min value:
        tested_range = (max_var_val - min_var_val)

        # bin size: width/distance between successive bins - distance between tested points.
        bin_size = (tested_range)/(total_bins)
        
        tested_var = (min_var_val) + (bin_size)
        # Variable value that will be generated for testing

        while (tested_var < max_var_val):

            #If it gets bigger or equal to the max_var_val, we will simply make it equals to the maximum
            #possible value, so that we will not test values outside the range of possibilities.

            var_list.append(tested_var)
            #Go to next bin and restart the loop:
            tested_var = tested_var + (bin_size)

        #Now we are at the maximum possible value. Add it to the tested_var list:
        var_list.append(max_var_val)
        #Now we created the list with all the tested values. Let's check its dimension (total rows
        #of the final dataframe).

        # Let's create a dataframe from this list:
        simulation_dict = {variable: var_list}
        #the key of the dictionary (name of the future column) is the original name of the variable.

        sensitivityAnalysis_df = pd.DataFrame(data = simulation_dict)
    
        # Let's generate the new columns. They will have a constant value, equals to the average value
        # of the variable in the original dataset. The list cols_names will register the correct names
        # so we will be able to create a new column at each interaction: at each interaction, we will
        # append a new name to this list and update the columns names to be equals to the list. Then, the
        # generic name used for starting the column will be again able to be used.
        
        # Start a dictionary of statistics values (mean for numerics, mode for categoricals):
        stats_dict = {}
        # List the possible numeric data types for a Pandas dataframe column:
        numeric_dtypes = [np.int16, np.int32, np.int64, np.float16, np.float32, np.float64]
        
        # Let's get the mean or most common values for the other columns:
        for column in other_columns:
            
            # Store the column name as key, and the statistic as value:
            column_data_type = history_dataset[column].dtype
            
            if (column_data_type not in numeric_dtypes):
                # column is categorical (string):
                mode_array = stats.mode(history_dataset[column])
                            
                # The function stats.mode(X) returns an array as: 
                # ModeResult(mode=array(['a'], dtype='<U1'), count=array([2]))
                # If we select the first element from this array, stats.mode(X)[0], 
                # the function will return an array as array(['a'], dtype='<U1'). 
                # We want the first element from this array stats.mode(X)[0][0], 
                # which will return a string like 'a':
                try:
                    stats_dict[column] = mode_array[0][0]

                except IndexError:
                    # This error is generated when trying to access an array storing no values.
                    # (i.e., with missing values). Since there is no dimension, it is not possible
                    # to access the [0][0] position. In this case, simply append the np.nan 
                    # the (missing value):
                    stats_dict[column] = np.nan
            
            else:
                stats_dict[column] = history_dataset[column].mean()
        
        # Now, loop through each key-value (items) pair:
        for key, value in stats_dict.items():
            
            # Add the key as the column name, and the value as constant value of the column:
            sensitivityAnalysis_df[key] = value
        
        # Finally, add it to the output dictionary using the index in the input list as key:
        simulation_dfs_dict[simulated_variables.index(variable)] = {'variable_to_test': variable,
                                                            'sensitivity_analysis_df': sensitivityAnalysis_df}
        
        print (f"Dataset for sensitivity analysis of the variable \'{variable}\' returned.")
        print (f"In the returned dataset, \'{variable}\' ranges from its minimum = {min_var_val}; to its maximum = {max_var_val} values observed on the original dataset.") 
        print (f"This range was split into {total_bins} bins.")
        print ("Check the 5 first rows of the returned dataset:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(sensitivityAnalysis_df.head())

        except: # regular mode
            print (sensitivityAnalysis_df.head())
            # When no integer is input as parameter of the head method, the defaul
            # 5 rows is applied: .head() == .head(5)

    # Return the new dictionary:
    # The dataframes are stored in the key 'sensitivity_analysis_df'. The keys to access the nested
    # dictionaries are integers starting from zero, representing the position (order) of the generated
    # dataframe. For example, simulation_dfs_dict[0]['sensitivity_analysis_df'] access the 1st dataframe,
    # simulation_dfs_dict[1]['sensitivity_analysis_df'] access the 2nd dataframe, and so on.
    # Simply modify this object on the left of equality:
    return simulation_dfs_dict

