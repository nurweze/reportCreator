import os
import logging
import sys

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  

from exportable import Exportable
from importable import Deserialization  


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='report.log', filemode='a')

def main():
    # Initialize the Exportable class
    exportable = Exportable(gui=None)  # Pass GUI instance if required

    # Read the serialization log and get the file paths
    file_paths = exportable.read_serialization_log()

    # Check if any file paths were found
    if not file_paths:
        logging.info("No serialized or deserialized files found in the log.")
        print("No serialized or deserialized files found in the log.")
        return

    # Create an instance of Deserialization
    deserializer = Deserialization()

    # Iterate over each file path to deserialize
    for file_path in file_paths:
        if os.path.isfile(file_path):
            logging.info(f"Deserializing: {file_path}")
            print(f"Deserializing: {file_path}")

            # Deserialize the data
            deserialized_data = deserializer.deserialize_data(file_path)
            logging.info(f"Deserialized data from {file_path}: {deserialized_data}")
            print(f"Deserialized data from {file_path}: {deserialized_data}")
        else:
            logging.error(f"Error: File does not exist: {file_path}")
            print(f"Error: File does not exist: {file_path}")

if __name__ == "__main__":
    main()
