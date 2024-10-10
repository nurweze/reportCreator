import os
import logging
from importable import FileReader, Serialization, Deserialization

# Configure logging for console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FileProcessor:

    def __init__(self, confirmed_paths: dict, selected_format: str = "Pickle"):
        self.datasources = confirmed_paths.get("datasources", [])
        self.workspace = confirmed_paths.get("workspace")
        self.selected_format = selected_format
        self.file_reader = FileReader()
        self.serializer = Serialization()
        self.log_file_path = os.path.join("ReportTemplates", "serialization_log.txt")
        self.confirmed_paths = confirmed_paths  
        self.deserialization = Deserialization()

    def process_files(self) -> str:
        """Process each data source and serialize the content."""
        if not self.datasources or not self.workspace:
            logging.error("No paths were provided for data sources or workspace.")
            return "No paths were provided for data sources or workspace."

        result_messages = []

        with open(self.log_file_path, 'a') as log_file:
            for data_source in self.datasources:
                if not os.path.isfile(data_source):
                    error_message = f"Data source does not exist: {data_source}"
                    logging.error(error_message)
                    result_messages.append(error_message)
                    continue

                logging.info(f"Reading data from: {data_source}")
                data = self.file_reader.read_file(data_source)

                if data is not None:
                    saved_file_path = self.serialize_data(data, data_source)
                    if saved_file_path:
                        result_messages.append(f"Serialized: {saved_file_path}")
                else:
                    error_message = f"Failed to read data from: {data_source}"
                    logging.error(error_message)
                    result_messages.append(error_message)

        return "\n".join(result_messages)

    def serialize_data(self, data, data_source: str) -> str:
        """Serialize the data and log the saved file path."""
        try:
            saved_file_path = self.serializer.serialize(
                data=data,
                workspace=self.workspace,
                format=self.selected_format,
                original_filename=data_source
            )
            with open(self.log_file_path, 'a') as log_file:
                log_file.write(f"Serialized: {saved_file_path}\n")
            logging.info(f"Serialized: {saved_file_path}")
            return saved_file_path
        except Exception as e:
            error_message = f"Error serializing data from {data_source}: {e}"
            logging.error(error_message)
            return ""

    def read_serialization_log(self, log_file_path: str) -> list:
        """Read the serialization log file and extract file paths."""
        logging.info(f"Reading log file at: {log_file_path}")
        file_paths = []

        if not os.path.isfile(log_file_path):
            logging.error(f"Log file does not exist: {log_file_path}")
            return file_paths

        with open(log_file_path, 'r') as log_file:
            log_contents = log_file.readlines()

        for line in log_contents:
            if line.startswith("Serialized:"):
                file_path = line.split("Serialized: ")[-1].strip()
                file_paths.append(file_path)
                logging.info(f"Extracted file path: '{file_path}'")

        return file_paths    

    def process_serialization_log(self):
        """Process the serialization log and perform actions based on the file paths."""
        log_file_path = os.path.join(self.confirmed_paths["workspace"], "serialization_log.txt")
    
        # Ensure the log file exists before trying to open it
        if not os.path.isfile(log_file_path):
            with open(log_file_path, 'w') as log_file:  # Create the log file
                log_file.write("Log file created.\n")
    
        # Read file paths from the serialization log
        file_paths = self.read_serialization_log(log_file_path)
    
        processed_paths = set()  # Keep track of processed paths
    
        # Process each file path
        for file_path in file_paths:
            if file_path in processed_paths:  # Skip if already processed
                logging.warning(f"Skipping already processed file: {file_path}")
                continue
            
            if os.path.isfile(file_path):
                logging.info(f"Deserializing: {file_path}")
                deserialized_data = self.deserialization.deserialize_data(file_path)
                if isinstance(deserialized_data, str):  # Check for error message
                    logging.error(deserialized_data)
                else:
                    log_message = f"Deserialized: {file_path}"
                    logging.info(log_message)
                    processed_paths.add(file_path)  # Mark as processed
                    with open(log_file_path, 'a') as log_file:
                        log_file.write(f"{log_message}\n")
            else:
                logging.error(f"Error: File does not exist for deserialization: {file_path}")


    def deserialize_file(self, file_path: str, log_file_path: str):
        """Deserialize the given file and log the outcome."""
        if os.path.isfile(file_path):
            logging.info(f"Deserializing: {file_path}")
            deserialized_data = self.deserialization.deserialize_data(file_path)
            if isinstance(deserialized_data, str):
                logging.error(deserialized_data)
            else:
                log_message = f"Deserialized: {file_path}"
                logging.info(log_message)
                with open(log_file_path, 'a') as log_file:
                    log_file.write(f"{log_message}\n")
        else:
            logging.error(f"Error: File does not exist for deserialization: {file_path}")
