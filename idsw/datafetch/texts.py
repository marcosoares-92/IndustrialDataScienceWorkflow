"""FUNCTIONS FROM INDUSTRIAL DATA SCIENCE WORKFLOW (IDSW) PACKAGE
Pipelines for reading text files like PDFs, CSVs, HTML and DOCX

Marco Cesar Prado Soares, Data Scientist Specialist @ Bayer Crop Science LATAM
marcosoares.feq@gmail.com
marco.soares@bayer.com"""

import numpy as np
import pandas as pd

from idsw import (InvalidInputsError, ControlVars)


def text_extraction (file_paths, doc_separator = '\n\n-----\n\n',
                        output_text_path = None, output_meta_path = None,
                        previous_text_database_path = None, previous_metadata_database_path = None,
                        previous_filenames_database_path = None):

    import os
    from langchain_community.document_loaders import PyPDFLoader, CSVLoader, UnstructuredHTMLLoader, Docx2txtLoader, TextLoader
    
    """
    Extracts the full text and metadata from a file or list of files. Extensions may be pdf, csv, html, txt.
    
    Parameters:
    ----------
    file_paths : list of str
        A list of file paths to be processed. Each element must be the full path to a file.

    doc_separator : str
        The string that will be used to separate different texts when all documents are saved in a same string or txt.

    output_text_path : str or None, optional (default = None)
        If provided, saves the extracted full text from the files to a text file at this path.
        If None, output_text_path will be set to 'extracted_text.txt'

    output_meta_path : str or None, optional (default = None)
        If provided, saves the metadata of the processed files to a text file at this path.
        If None, output_meta_path will be set to 'metadata.txt'
    
    previous_text_database_path : str or None, optional (default = None)
        If provided, the text database from this path will be read, and new data will be appended to it

    previous_metadata_database_path : str or None, optional (default = None)
        If provided, the metadata database from this path will be read, and new data will be appended to it

    previous_filenames_database_path : str or None, optional (default = None)
        If provided, the file names database from this path will be read, and new data will be appended to it
    
    WARNING: The new database will not automatically overwrite the previous ones. It will be saved to the provided path or to the default path.

    Returns:
    
        texts: list where each element is one of the documents read
        metadata: list correspondent to 'texts', where each element is the correspondent metadata
        file_names: list correspondent to 'texts', where each element is the correspondent file name read

    """    

    if (type(file_paths) == str):
        # Convert to list:
        file_paths = [file_paths]
    
    print(f"Processing {len((file_paths))} files.\n")
    
    if output_text_path is None:
        output_text_path = 'extracted_text.txt'
    
    if output_meta_path is None:
        output_meta_path = 'metadata.txt'


    error_msg = """Run the command for downloading the required package:
        ! pip install """

    # Initialize the list to store metadata for reporting and a structured result to return
    # Create empty lists for storing files information
    metadata = []
    texts = []
    file_names = []

    
    for file_path in file_paths:
        
        # Ensure the object has a valid extension
        if (os.path.splitext(file_path)[1][1:] != ''):
            
            extension = os.path.splitext(file_path)[1].lower()
            extension = extension.strip('.')
            file_name = os.path.basename(file_path)
            file_names.append(file_name)
            
            # Load the file based on its extension
            if extension == "pdf":
                try:
                    loader = PyPDFLoader(file_path)
                except ModuleNotFoundError:
                    raise ModuleNotFoundError(error_msg + "pypdf")

            elif extension == "csv":
                loader = CSVLoader (file_path = file_path)

            elif extension == "html":
                try:
                    loader = UnstructuredHTMLLoader(file_path)
                except ModuleNotFoundError:
                    raise ModuleNotFoundError(error_msg + "unstructured")

            elif extension == "txt":
                loader = TextLoader (file_path)

            elif ((extension == "docx") | (extension == "doc")):
                try:
                    loader = Docx2txtLoader (file_path)
                except ModuleNotFoundError:
                    raise ModuleNotFoundError(error_msg + "docx2txt")

            else:
                print(f"Found file with extension that is not supported: {extension}")
                continue # Skip to the next file

            # Try to read the document:
            try:

                data = loader.load()

                # Try to extract metadata. If no metadata is available, add this info:
                try:
                      # Extract metadata and append it to the metadata list
                      meta = data[0].metadata

                except:
                      meta = 'file with no metadata'
                    
                metadata.append(meta)

                # Extract all the pages:
                pages = [page.page_content for page in data]
                # Concatenate the full text and append it to the texts list, separating each page with a line break
                text = '\n'.join(pages)
                texts.append(text)

            except:
                  pass
            
    print(f"Total of {len(texts)} documents read.")
    print(f"First document metadata: {metadata[0]}")
    print(f"First document 50 initial characters: {texts[0][:50]}")
    print(f"Last document metadata: {metadata[-1]}")
    print(f"Last document 50 initial characters:: {texts[-1][:50]}")
    
    if (len(texts) != len(metadata)):
        print(f"Attention! Found metadata for only {len(metadata)} documents.")
        
    print("\n")
        
    # doc_separator = '\n\n-----\n\n'
        
    if previous_text_database_path is not None:
        # Read it as a string and append the new texts to it:
        with open (previous_text_database_path, 'r') as f:
            previous_db = f.read()
            
        # Separate documents into a list
        previous_db_texts = previous_db.split(doc_separator)
        # Combine the lists:
        texts = previous_db_texts + texts
            
    # Concatenate all documents in a single text
    all_texts = doc_separator.join(texts)

        
    if previous_metadata_database_path is not None:
        # Read it as a string and append the new texts to it:
        with open (previous_metadata_database_path, 'r') as f:
            previous_metadata_db = f.read()
            
        # Separate documents into a list
        previous_metadata_db_texts = previous_metadata_db.split(doc_separator)
        # Combine the lists:
        metadata = previous_metadata_db_texts + metadata
        
    # Concatenate all metadata in a single text
    metadata_text = doc_separator.join([str(meta) for meta in metadata])
        
        
    if previous_filenames_database_path is not None:
        # Read it as a string and append the new texts to it:
        with open (previous_filenames_database_path, 'r') as f:
            filenames_db = f.read()
            
        # Separate documents into a list
        filenames_db_texts = filenames_db.split(doc_separator)
        # Combine the lists:
        file_names = filenames_db_texts + file_names
   
    # Concatenate all file names:
    files = doc_separator.join(file_names)

    # Save outputs
        
    with open(output_meta_path, 'w') as f:
        f.write(metadata_text)

    with open(output_text_path, 'w') as f:
        f.write(all_texts)
        
    with open('file_names.txt', 'w') as f:
        f.write(files)
    
    
    return texts, metadata, file_names


def read_txt_database (file_path, split_strings = True, doc_separator = '\n\n-----\n\n'):
    
    """
    Read a text database saved as a single txt file. The different files in the database may be returned as different
    elements from a list
    
    Parameters:
    ----------
    file_path : str
        file path to be processed
    
    split_strings: bool
        If True: each string will be a different element from the returned list.
        If False: a list with a single string containing the whole text will be returned.

    doc_separator : str
        The string that will be used to separate different texts when all documents are saved in a same string or txt.

    Returns:
    
        texts: list of strings containing the read texts. If split_strings = False, the list will contain a single element

    """    
    
    # Read the database:
    with open (file_path, 'r') as f:
        db = f.read()
    
    if split_strings:
        # Separate documents into a list
        # doc_separator = '\n\n-----\n\n'
        texts = db.split(doc_separator)
    
    else:
        texts = [db]

    return texts


def create_txt_db (file_path, strings_to_save, doc_separator = '\n\n-----\n\n'):
    
    """
    Create a txt database from the provided strings. 
    If a list of strings is provided, the output txt will combine all of them and separate them with doc_separator.
    
    Parameters:
    ----------
    file_path : str
        file paths to be processed
    
    strings_to_save: str or list of strs
        List of strings to be combined into a single text or string to be saved in the txt file.

    doc_separator : str
        The string that will be used to separate different texts when all documents are saved in a same string or txt.

    Returns:
    
        None (only the file is exported)

    """
    
    if type(strings_to_save) == list:
        # Concatenate all documents:
        # doc_separator = '\n\n-----\n\n'
        files = doc_separator.join(strings_to_save)
    
    else:
        files = strings_to_save

    # Save outputs
    with open(file_path, 'w') as f:
        f.write(files)


def convert_str_to_dicts (text_to_convert):
    """
    If the text being converted is already structured as a dictionary, use this function to automatically return Python dicts, instead of strings.
    This is particularly useful for processing metadata text databases.
    
    Parameter:
    ----------
    text_to_convert : str or list of strs
        texts to be converted to dictionaries

    Returns:
        returned_dicts: list of dictionaries retrieved from the string.
        The Python dictionar with the exact same structure as the input string.

    Raises:
        ValueError: If the input string is not a valid Python dictionary literal.
    """

    # Subfunction created with Gemini's support:
    import ast

    def convert_string_to_dict(input_string: str) -> dict:
        """
        Converts a string representation of a Python dictionary literal
        into an actual Python dictionary.

        Args:
            input_string: The string containing the dictionary literal.

        Returns:
            A Python dictionary with the exact same structure as the input string.

        Raises:
            ValueError: If the input string is not a valid Python dictionary literal.
        """
        try:
            # Use ast.literal_eval to safely parse the string as a Python literal
            # This is safer than eval() as it only evaluates literals and not arbitrary code.
            result_dict = ast.literal_eval(input_string)
            if isinstance(result_dict, dict):
                return result_dict
            else:
                raise ValueError("The provided string does not represent a dictionary.")
        except (ValueError, SyntaxError) as e:
            raise ValueError(f"Failed to parse string as dictionary: {e}")
    
    if type(text_to_convert) == str:
        returned_dicts = [convert_string_to_dict(text_to_convert)]
    
    else:
        returned_dicts = [convert_string_to_dict(text) for text in text_to_convert]
        
        
    return returned_dicts

