import os
import logging
import io
import re
import sys
import tkinter as tk
import pandas as pd


from tkinter import filedialog
from importable import Serialization, Deserialization
from processes import FileProcessor

''' 
Important note: that the ReportTemplates directory is hardcoded as 
the default one for all reports. 
'''

class Exportable: 


    def __init__(self, gui = None):
        self.gui = gui  # Reference to the GUIMaker instance
        self.log_file_path = os.path.join("ReportTemplates", "serialization_log.txt")
        

    def create_report(self):
        """Open a Python file for editing and running."""
        file_path = self.get_python_file_path()  # Open file dialog to get the path of the report
        if not file_path:
            self.gui.log_to_console("Error: No file path provided for the report.")
            return
    
        with open(file_path, 'r') as file:
            report_code = file.read()
    
        # Open a new window for editing the Python script
        editor_window = tk.Toplevel(self.gui.window)
        editor_window.title(f"Edit Report - {os.path.basename(file_path)}")  # Display the file name in the window title
    
        # Create a text editor widget to display the content of the Python report
        editor_text = tk.Text(editor_window, height=20, width=80)
        editor_text.insert(tk.END, report_code)  # Insert the contents of the report
        editor_text.pack()
    
        # Define a button to run the report, passing the file path to run_report
        run_button = tk.Button(
            editor_window,
            text="Run Report",
            command=lambda: self.run_report(editor_text.get("1.0", tk.END), report_file_path=file_path)
        )
        run_button.pack()



    def get_python_file_path(self):
        """Open a file dialog to select a Python file."""
        file_path = filedialog.askopenfilename(
            title="Select a Python file",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        return file_path


    def run_report(self, report_code, report_file_path=None):
        """Execute the report code with the proper file path and log messages to console 1 and output to console 2."""
        output_buffer = io.StringIO()
        error_buffer = io.StringIO()
        sys.stdout = output_buffer  # Redirect stdout to capture print statements
        sys.stderr = error_buffer   # Redirect stderr to capture errors
    
        # Ensure ReportTemplates is added to sys.path only once
        report_dir = os.path.join(os.path.dirname(__file__), "ReportTemplates")
        if report_dir not in sys.path:
            sys.path.append(report_dir)
    
        # Change directory to ReportTemplates
        os.chdir(report_dir)
    
        # Create a custom globals dictionary with __file__ set to the provided report file path
        exec_globals = {"__file__": report_file_path} if report_file_path else {}
    
        try:
            # Run the provided report code with the modified globals context
            exec(report_code, exec_globals)
    
            # Capture the standard output and error output
            output = output_buffer.getvalue()
            error_output = error_buffer.getvalue()
    
            # Log outputs accordingly
            if output:
                self.gui.log_to_console_2(output)  # Log stdout to console 2
            if error_output:
                self.gui.log_to_console(f"Errors detected:\n{error_output}")  # Log stderr to console 1
    
            # Handle cases where no output is produced
            if not output and not error_output:
                self.gui.log_to_console_2("No output produced.")
    
        except Exception as e:
            # Capture unexpected exceptions in a more readable format
            self.gui.log_to_console(f"Error executing report: {e}")
        finally:
            # Reset stdout and stderr back to their original streams
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__



    def read_serialization_log(self):
        """Read the serialization log and return the list of serialized or deserialized file paths."""
        log_file_path = os.path.join(os.path.dirname(__file__), "ReportTemplates", "serialization_log.txt")

        if not os.path.isfile(log_file_path):
            logging.error("Serialization log does not exist.")
            return []

        # Debugging: Print the log file path
        print(f"Reading log file at: {log_file_path}")

        with open(log_file_path, 'r') as log_file:
            lines = log_file.readlines()

        # Print log file contents for debugging
        print("Log file contents:")
        for line in lines:
            print(line.strip())

        # Extract file paths from log
        file_paths = []
        for line in lines:
            line = line.strip()
            if "Serialized:" in line or "Deserialized:" in line:
                parts = line.split(":")
                if len(parts) > 1:
                    file_path = parts[1].strip()
                    file_paths.append(file_path)
                    print(f"Extracted file path: '{file_path}'")

        if not file_paths:
            logging.error("No file paths found in the serialization log.")
        
        return file_paths


    def log_deserialization(self, file_path):
        """Log the deserialized file path to the serialization log."""
        with open(self.log_file_path, 'a') as log_file:
            log_file.write(f"Deserialized: {file_path}\n")



class ReportGenerator:
    
    '''
    Contains methods that collect the datapaths of processed files. 
    Is called by report0.py to produce standard report. 
    '''

    def __init__(self):
        self.logger = logging.getLogger()
        self.deserializer = Deserialization()  # Initialize once
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

    def generate_report(self):
        self.logger.info("Starting report generation...")
        self.logger.info(f"Current directory: {self.current_dir}")
    
        # Initialize Exportable to read the serialization log
        exportable_instance = Exportable()
        log_file_path = os.path.join(self.current_dir, "serialization_log.txt")
    
        try:
            # Read the serialization log to get file paths
            file_paths = exportable_instance.read_serialization_log()
    
            self.logger.info(f"File paths from log: {file_paths}")
    
            if not file_paths:
                self.logger.error("No file paths found in the serialization log.")
                return
    
            # Process each file path to deserialize and inspect contents
            for file_path in file_paths:
                data = self.deserializer.deserialize_data(file_path)  # Use the correct method
                
                if isinstance(data, str) and data.startswith("Error"):
                    self.logger.error(data)  # Log errors from deserialization
                else:
                    # Log or print summary information about the deserialized data
                    if isinstance(data, pd.DataFrame):
                        self.logger.info(f"Successfully deserialized DataFrame from {file_path}.\n: Shape:{data.shape}. Preview: {data.head()}")
                    elif isinstance(data, dict):
                        self.logger.info(f"Successfully deserialized JSON from {file_path}.:\n Keys:{list(data.keys())}")
                    else:
                        self.logger.info(f"Successfully deserialized data from {file_path}:\n{data}")  # Adjust this line if data needs special formatting
    
            self.logger.info("Report generation completed.")
            return True  # Indicate success
    
        except Exception as e:
            self.logger.error(f"An error occurred in generate_report: {e}")
            return False  # Indicate failure
