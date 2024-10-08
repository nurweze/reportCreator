import os
import logging
import io
import re
import sys
import tkinter as tk
from tkinter import filedialog
from importable import Serialization, Deserialization

class Exportable:
    
    
    def __init__(self, gui):
        self.gui = gui  # Reference to the GUIMaker instance
        self.log_file_path = os.path.join("ReportTemplates", "serialization_log.txt")


    def create_report(self):
        """Open a Python file for editing and running."""
        file_path = self.get_python_file_path()
        if not file_path:
            self.gui.log_to_console("Error: No file path provided for the report.")
            return

        with open(file_path, 'r') as file:
            report_code = file.read()

        # Open a new window for editing the Python script
        editor_window = tk.Toplevel(self.gui.window)
        editor_window.title("Edit Report")
        editor_text = tk.Text(editor_window, height=20, width=80)
        editor_text.insert(tk.END, report_code)
        editor_text.pack()

        run_button = tk.Button(editor_window, text="Run Report", command=lambda: self.run_report(editor_text.get("1.0", tk.END)))
        run_button.pack()


    def get_python_file_path(self):
        """Open a file dialog to select a Python file."""
        file_path = filedialog.askopenfilename(
            title="Select a Python file",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        return file_path


    def run_report(self, report_code):
        """Execute the report code and log messages to console 1 and output to console 2."""
        output_buffer = io.StringIO()
        sys.stdout = output_buffer  # Redirect stdout to capture print statements
        
        try:
            exec(report_code)  # Run the report code
            output = output_buffer.getvalue()
            if output:
                self.gui.log_to_console_2(output)  # Log output to console 2
            else:
                self.gui.log_to_console_2("No output produced.")
                
        except Exception as e:
            self.gui.log_to_console(f"Error executing report: {e}")  # Log error to console 1
        finally:
            sys.stdout = sys.__stdout__  # Reset stdout


#===============================================================================
#     def read_serialization_log(self):
#         """Read the serialization log and return the list of serialized and deserialized file paths."""
#         if not os.path.isfile(self.log_file_path):
#             logging.error("Serialization log does not exist.")
#             return []
# 
#         with open(self.log_file_path, 'r') as log_file:
#             lines = log_file.readlines()
# 
#         # Extract file paths from log for both serialized and deserialized entries
#         file_paths = []
#         for line in lines:
#             if "Serialized:" in line or "Deserialized:" in line:
#                 file_path = re.search(r'-> (.+)', line)
#                 if file_path:
#                     file_paths.append(file_path.group(1).strip())
# 
#         return file_paths
#===============================================================================

    def read_serialization_log(self):
        """Read the serialization log and return the list of serialized or deserialized file paths."""
        log_file_path = os.path.join("ReportTemplates", "serialization_log.txt")
    
        if not os.path.isfile(log_file_path):
            logging.error("Serialization log does not exist.")
            return []

        # Print the log file path and its contents for debugging
        print(f"Reading log file at: {log_file_path}")
    
        with open(log_file_path, 'r') as log_file:
             lines = log_file.readlines()

        print("Log file contents:")
        for line in lines:
            print(line)  # Print each line to check the format and content

        # Extract file paths from log
        file_paths = []
        for line in lines:
            # Check for both "Serialized:" and "Deserialized:"
            if "Serialized:" in line.lower() or "Deserialized:" in line.lower():
                file_path = line.split(":")[1].strip()
                file_paths.append(file_path)

        return file_paths


    def log_deserialization(self, file_path):
        """Log the deserialized file path to the serialization log."""
        with open(self.log_file_path, 'a') as log_file:
            log_file.write(f"Deserialized: {file_path}\n")


    def process_serialization_log(self):
        """Read the serialization log and deserialize the specified files."""
        file_paths = self.read_serialization_log()
        
        deserializer = Deserialization()
        
        for file_path in file_paths:
            if os.path.isfile(file_path):
                self.gui.log_to_console(f"Deserializing: {file_path}")
                deserialized_data = deserializer.deserialize_data(file_path)
                self.log_deserialization(file_path)  # Log the deserialized file path
                self.gui.log_to_console_2(f"Deserialized data from {file_path}: {deserialized_data}")
            else:
                self.gui.log_to_console(f"Error: File does not exist for deserialization: {file_path}")
