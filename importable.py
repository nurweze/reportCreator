

'''
Contains the classes FileReader, Serialization and Deserialization. 

FileReader reads in the file depending on its original datastructure so that the datastructure
is not lost under serialization. 

Serialization class serializes the files according to the serialization of choice, as a byte file 
with Python's pickle or as a readable JSON format.

Implemented?|  Filetype   |  Original datastructure |                     Serialized structure 
            |             |                         |        Pickle                      |  JSON
----------------------------------------------------------------------------------------------------------
    YES     |     CSV     | Tables (Rows/Column)    | List of Dictionaries or pandas DF  | Str
----------------------------------------------------------------------------------------------------------
    YES     |    Excel    | Tables (Rows/Column)    | List of Dictionaries or pandas DF  | Dictionary
----------------------------------------------------------------------------------------------------------
    YES     |    JSON     | Dict. or list of Dict.  |       -                            | Kept as original
-----------------------------------------------------------------------------------------------------------
  NOT YET   |    XML      | Tables (Rows/Column)    | List of Dictionaries or pandas DF  | 
-----------------------------------------------------------------------------------------------------------
  NOT YET   |   R/RData   | Various (Vectors, Lists,| List of Dictionaries or pandas DF  |
            |                     DataFrames)       |                                    | 
-----------------------------------------------------------------------------------------------------------
  NOT YET   |     SQL     |   SQL code              |                                    | 
-----------------------------------------------------------------------------------------------------------
 HTTP/HTTPS handling already possible but I need to check the security risks for that. 
 or maybe create a whitelist of acceptable sites. 
 
'''


import os
import pandas as pd
import pickle
import xml.etree.ElementTree as ET
import pyreadr
import time
import json

import tkinter as tk
from tkinter import filedialog


class FileReader:
    
    
    def read_file(self, file_path: str):
        """Reads a file based on its extension and returns the data in an appropriate format."""
        data = None  # Initialization 
        
        # Getting the file extension
        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.lower()

        # Check the file extension and use the appropriate reading method
        try:
            if file_extension == '.csv':
                with open(file_path, 'r') as file:
                    data = file.read()
                print("The file is a .CSV File.")
                
            elif file_extension == '.json':
                with open(file_path, 'r') as file:
                    data = json.load(file)  # Directly load JSON into a dictionary
                print("The file is a .JSON File.")
                         
            elif file_extension in ['.xls', '.xlsx']:
                data = pd.read_excel(file_path)  # Reads it in using pandas anyhow because Excel having limited row numbers
                print("The file is an Excel File (.xls/.xlsx).")
                
            elif file_extension == '.xml':
                tree = ET.parse(file_path)
                root = tree.getroot()
                data = ET.tostring(root, encoding='unicode')
                print("XML File Content as String.")
                            
            elif file_extension in ['.r', '.rdata']:
                result = pyreadr.read_r(file_path)
                data = result  # result is a dictionary-like object with dataframes
                print("R File Content in Dictionary Format.")
                
            else:
                print(f"Error: Unsupported file type: {file_extension}.")
                
        except Exception as e:
            print(f"Error reading file: {e}")

        return data


class Serialization:
    
    
    def serialize(self, data, workspace, format, filename=None, original_filename=None):
        """
        Serialize data to the specified format and save it to the workspace.
        """
        # Check if the workspace path exists
        if not os.path.exists(workspace):
            raise FileNotFoundError("Workspace path does not exist.")

        # Validate the format before proceeding
        if format not in ["Pickle", "JSON"]:
            raise ValueError(f"Unsupported serialization format '{format}'. Please choose 'Pickle' or 'JSON'.")

        if original_filename and format == "JSON":
            _, file_extension = os.path.splitext(original_filename)
            if file_extension.lower() == ".json":
                raise ValueError("Cannot serialize a .json file as .json again.")

        # Generate a filename using the original filename as the base, if provided
        if not filename and original_filename:
            extension = "pkl" if format == "Pickle" else "json"
            base_name = os.path.splitext(os.path.basename(original_filename))[0]
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"{base_name}_{timestamp}.{extension}"
        elif not filename:
            raise ValueError("Filename must be provided if original_filename is not given.")

        file_path = os.path.join(workspace, filename)

        try:
            # Serialize based on the selected format
            if format == "Pickle":
                with open(file_path, 'wb') as pickled_file:
                    pickle.dump(data, pickled_file)
                return f"Data successfully saved as Pickle to: {file_path}"

            elif format == "JSON":
                with open(file_path, 'w') as json_file:
                    json.dump(data, json_file, indent=4)
                return f"Data successfully saved as JSON to: {file_path}"

        except Exception as e:
            raise RuntimeError(f"Error serializing data: {e}")
        

class Deserialization:

    
    def __init__(self, os_module=os):
        self.os = os_module  # Store a reference to the os module
        
    
    def deserialize_data(self, file_path):
        """
        Deserialize data from a given file based on its extension.
        """
        # Check if the file exists
        if not self.os.path.isfile(file_path):  # Use self.os instead of os
            return f"Error: The file does not exist: {file_path}"

        # Get the file extension and convert it to lowercase
        _, file_extension = self.os.path.splitext(file_path)  # Use self.os instead of os
        file_extension = file_extension.lower()

        try:
            # Handle Pickle (.pkl) files
            if file_extension == '.pkl':
                with open(file_path, 'rb') as file:
                    data = pickle.load(file)
                    return data  # Return the deserialized data

            # Handle JSON (.json) files
            elif file_extension == '.json':
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    return data  # Return the deserialized data

            # If the file type is not supported
            else:
                return f"Error: Unsupported file type: {file_extension}. Please provide a .pkl or .json file."

        except Exception as e:
            return f"Error during deserialization: {e}"
        

    def deserialize_file(self, output_console_1, output_console_2):
        """Deserialize the selected file and log output to the specified consoles."""
        file_path = self.get_deserialization_file_path()
        if not file_path:
            output_console_1.insert("end", "Error: No file path provided for deserialization.\n")
            return

        # Call the existing deserialize_data method
        deserialized_data = self.deserialize_data(file_path)

        if isinstance(deserialized_data, str):  # Check if it's an error message
            output_console_1.insert("end", deserialized_data)
        else:
            output_console_2.insert("end", "Deserialized data:\n")
            output_console_2.insert("end", f"{deserialized_data[:100]}")  # Log only the first 100 characters
         
         
    def get_deserialization_file_path(self):
        """Open a file dialog to select a file for deserialization."""
        file_path = tk.filedialog.askopenfilename(
            title="Select a file for deserialization",
            filetypes=[("Pickle files", "*.pkl"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        return file_path
    