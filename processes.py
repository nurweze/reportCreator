import os
import time
import logging
import tkinter as tk


'''
File functions: 

Reads in the commands from the GUI (GUImaker.py) and processes with the serialization
by reading in the datafile and serializing (importable.py) it according to the selected format.

Prints messages during the processing to both the log and the GUI console, in order to ease debugging. 
(both error messages and success messages).

'''


from importable import FileReader, Serialization

# Configure logging for console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class FileProcessor:

    def __init__(self, confirmed_paths, selected_format="Pickle"):
        self.datasources = confirmed_paths.get("datasources", [])
        self.workspace = confirmed_paths.get("workspace")
        self.selected_format = selected_format
        self.file_reader = FileReader()
        self.serializer = Serialization()
        self.log_file_path = os.path.join("ReportTemplates", "serialization_log.txt")  # Ensure log is in the ReportTemplates directory

    def process_files(self):
        """Process each data source and serialize the content."""
        if not self.datasources or not self.workspace:
            logging.error("No paths were provided for data sources or workspace.")
            return "No paths were provided for data sources or workspace."

        result_messages = []  # List to capture all result messages

        # Create or open the log file to write serialized file paths
        with open(self.log_file_path, 'a') as log_file:  # Using context manager to ensure file is properly closed

            for data_source in self.datasources:
                if not os.path.isfile(data_source):
                    logging.error(f"Data source does not exist: {data_source}")
                    result_messages.append(f"Data source does not exist: {data_source}")
                    continue

                logging.info(f"Reading data from: {data_source}")
                data = self.file_reader.read_file(data_source)

                if data is not None:
                    try:
                        # Serialize the data and get the saved file path
                        saved_file_path = self.serializer.serialize(
                            data=data,
                            workspace=self.workspace,
                            format=self.selected_format,
                            original_filename=data_source
                        )

                        # Log only the saved file path to the serialization log
                        log_file.write(f"Serialized: {saved_file_path}\n")

                        # Log and collect a concise success message for the console
                        success_message = f"Data successfully saved as: {saved_file_path}"
                        logging.info(success_message)
                        result_messages.append(success_message)

                    except Exception as e:
                        error_message = f"Error serializing data from {data_source}: {e}"
                        logging.error(error_message)
                        result_messages.append(error_message)
                else:
                    error_message = f"Failed to read data from: {data_source}"
                    logging.error(error_message)
                    result_messages.append(error_message)

        return "\n".join(result_messages)
