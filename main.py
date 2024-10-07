'''
# Lionel Nurweze, start: 20240925, last change: 2024-10-07
# lionel.nurweze -at- gmail -dot- com

# Project motivation and goal reachable at colab.google.com.

https://colab.research.google.com/drive/1adnpYwz4BZpKCxpzp8V3HDiCQg-Jvb24?usp=sharing

# Some code (especially the GUImaker.py) not runnable on Colab so the project has been moved to Jupyter Lab 

# Refactored using chatGPT OpenAI. (2023). 
# ChatGPT (GPT4o - Sep 2024 version) [Large language model].
# https://chat.openai.com/chat.
'''

import logging
from tkinter import filedialog, Text, messagebox

# Import custom modules
from importable import FileReader, Serialization, Deserialization
from processes import FileProcessor
from exportable import Exportable
from GUImaker import *

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """Main function to run the GUI and process files."""
    # Initialize and run the GUI
    app = GUIMaker()
    app.start()

if __name__ == "__main__":
    main()
