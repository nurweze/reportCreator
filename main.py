'''
# Lionel Nurweze, start: 20240924, last change: 2024-10-09
# lionel.nurweze -at- gmail -dot- com

# Project motivation and goal reachable at colab.google.com.
# Some code (especially the GUImaker.py) not runnable on Colab 
# so attempted to run on Jupyter Notes with GUI(tkinter) with some successes,
# Will try to implement a runnable Notebook without own GUI. 

# Refactored using chatGPT OpenAI. (2023). 
# ChatGPT (GPT4o - Sep 2024 version) [Large language model]. https://chat.openai.com/chat.
'''

import logging
from tkinter import filedialog, Text, messagebox
from GUImaker import GUIMaker

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    """Main function to run the GUI and process files."""
    # Initialize and run the GUI
    try:
        app = GUIMaker()
        app.start()
    except Exception as e:
        logging.error(f"An error occurred while starting the application: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")
        
if __name__ == "__main__":
    main()
