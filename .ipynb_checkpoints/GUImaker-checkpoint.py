import os
import logging
import tkinter as tk
from tkinter import filedialog
from importable import Serialization, Deserialization
from processes import FileProcessor
from exportable import Exportable

# Global dictionary to store confirmed paths
confirmed_paths = {"datasources": [], "workspace": None}


class GUIMaker:
    
    
    def __init__(self):
        self.datasource_entry = None
        self.window = tk.Tk()
        self.window.geometry("800x800")
        self.window.title("ReportCreatorGUI")
        self.window.configure(bg="light grey")  # Set window background color

        # Default save format
        self.save_format = tk.StringVar(value="Pickle")
        
        # Create an instance of Exportable
        self.exportable = Exportable(self)

        # Create widgets including the console output
        self.create_widgets()


    def create_widgets(self):
        
        # Widgets for Data Source
        
        datasource_label = tk.Label(self.window, text="Path data source", bg="light grey")
        datasource_label.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        self.datasource_entry = tk.Entry(self.window, width=35, font=('Arial', 16), fg='green', bg='beige')
        self.datasource_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        confirm_datasource_button = tk.Button(self.window, text="Confirm data source",
                                               command=lambda: self.confirm(self.datasource_entry, "datasources"))
        confirm_datasource_button.grid(row=1, column=1, pady=5, sticky="ew")

        delete_button = tk.Button(self.window, text="Delete data paths and workspace",
                                  command=self.delete_entries)
        delete_button.grid(row=3, column=1, pady=5, sticky="ew")

        # Widgets for Workspace
        
        workspace_label = tk.Label(self.window, text="Path to working space", bg="light grey")
        workspace_label.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.workspace_entry = tk.Entry(self.window, width=35, font=('Arial', 16), bg="beige")
        self.workspace_entry.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        confirm_workspace_button = tk.Button(self.window, text="Confirm path to your working space",
                                              command=lambda: self.confirm(self.workspace_entry, "workspace"))
        confirm_workspace_button.grid(row=4, column=1, pady=5, sticky="ew")

        # Save Button
        
        save_data_to_workspace_button = tk.Button(self.window, width=35, text="Save data to Workspace",
                                                   command=self.save_data_to_workspace)
        save_data_to_workspace_button.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

        # Configure the layout for radio buttons
        
        radio_button_frame = tk.Frame(self.window, bg="light grey")
        radio_button_frame.grid(row=5, column=1, padx=10, pady=5, sticky="ew")
     
        # Use the frame to hold the radio buttons, this will prevent them from overlapping
        pickle_radio = tk.Radiobutton(radio_button_frame, text="Pickle", variable=self.save_format, value="Pickle", bg="light grey")
        pickle_radio.pack(side="left", padx=5, pady=5, fill="x", expand=True)

        json_radio = tk.Radiobutton(radio_button_frame, text="JSON", variable=self.save_format, value="JSON", bg="light grey")
        json_radio.pack(side="left", padx=5, pady=5, fill="x", expand=True)

        other_radio = tk.Radiobutton(radio_button_frame, text="Other", variable=self.save_format, value="Other", bg="light grey")
        other_radio.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        
        # Console Output Text Widget
        self.console_output_1 = tk.Text(self.window, height=10, width=80, bg="black", fg="white", font=("Arial", 12))
        self.console_output_1.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Second console Text Widget with scrollbar
        console_frame = tk.Frame(self.window)  # Create a frame for the second console and its scrollbar
        console_frame.grid(row=10, column=0, columnspan=1, padx=8, pady=10, sticky="ew")

        self.console_output_2 = tk.Text(console_frame, height=15, width=50, bg="black", fg="white", font=("Arial", 12))
        self.console_output_2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar for the second console output
        scrollbar = tk.Scrollbar(console_frame, command=self.console_output_2.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
        self.console_output_2['yscrollcommand'] = scrollbar.set  # Link scrollbar with text widget

        clear_console_button = tk.Button(self.window, text="Clear Consoles", command=self.clear_console)
        clear_console_button.grid(row=9, column=1, pady=5, sticky="ew")
 
        # Create a frame for the buttons beside the second console
        button_frame = tk.Frame(self.window, bg="light grey")  # Frame to hold the buttons
        button_frame.grid(row=10, column=1, padx=10, pady=10, sticky="ew")

        # Deserialization Button
        deserialize_button = tk.Button(button_frame, text="Deserialize", command=self.deserialize_file)
        deserialize_button.pack(pady=5, fill=tk.X)

        # Report Creator Button
        report_creator_button = tk.Button(button_frame, text="Create Report", command=self.exportable.create_report)
        report_creator_button.pack(pady=5, fill=tk.X)       
        
        # Configure grid weights for the frame and other widgets
                
        for i in range(30):
            self.window.grid_rowconfigure(i, weight=1)  # Adjust the number based on your rows
        for i in range(3):
            self.window.grid_columnconfigure(i, weight=1)  # Adjust the number based on your columns


    def confirm(self, entry, label):
        """Confirm and store the path entered in the corresponding entry widget."""
        path = entry.get()
        if path:
            try:
                if label == "datasources":
                    if os.path.isfile(path):
                        confirmed_paths["datasources"].append(path)
                        self.log_to_console(f"Added data source path: {path}")
                    else:
                        self.log_to_console(f"Error: Data source does not exist: {path}")
                else:
                    if os.path.isdir(path):
                        confirmed_paths[label] = path
                        self.log_to_console(f"Saved {label} as {path}.")
                    else:
                        self.log_to_console(f"Error: Workspace does not exist: {path}.")
            except Exception as e:
                self.log_to_console(f"Error checking path: {e}")

        else:
            self.log_to_console("Error: You need to submit your path first and check if it's correct.")


    def delete_entries(self):
        """Clear all entries and reset the confirmed paths dictionary."""
        self.datasource_entry.delete(0, tk.END)
        self.workspace_entry.delete(0, tk.END)
        confirmed_paths["datasources"] = []
        confirmed_paths["workspace"] = None
        self.log_to_console("All entries have been deleted. Please resubmit both new data paths and a new workspace.")


    def save_data_to_workspace(self):
        """Save data to the workspace if paths are confirmed and valid."""
        if not confirmed_paths["datasources"] or not confirmed_paths["workspace"]:
            self.log_to_console("Error: You need to confirm both data source paths and workspace path before saving.")
            return

        selected_format = self.save_format.get()
        self.log_to_console(f"Confirmed paths are: {confirmed_paths}")
        self.log_to_console(f"Selected format for saving: {selected_format}")

        # Call FileProcessor to read the data and serialize it
        file_processor = FileProcessor(confirmed_paths, selected_format)

        try:
            result_message = file_processor.process_files()  # Process files to read and serialize
            if result_message:  # Check if result_message is not None
                self.log_to_console(result_message)  # Log the result message
            else:
                self.log_to_console("No result message returned from processing.")
        except Exception as e:
            self.log_to_console(f"Error during file processing: {e}")


    def log_to_console(self, message):
        """Log messages to the console output widget."""
        self.console_output_1.insert(tk.END, message + "\n")
        self.console_output_1.see(tk.END)  # Scroll to the end of the console output
        print(message)


    def clear_console(self):
        """Clear all the text in the console output."""
        self.console_output_1.delete(1.0, tk.END)
        self.console_output_2.delete(1.0, tk.END) 


    def deserialize_file(self):
        """Deserialize the selected file and print output to console 2."""
        file_path = self.get_deserialization_file_path()
        if not file_path:
            self.log_to_console_2("Error: No file path provided for deserialization.")
            return

        deserializer = Deserialization()
    
        # Call the deserialize_data function from processes.py
        deserialized_data = deserializer.deserialize_data(file_path)  
        
        # Log deserialization event
        self.exportable.log_deserialization(file_path)  # Log the deserialized file path

        # Optionally log the deserialized data if it's a list or similar
        if isinstance(deserialized_data, str):  # Check if it's an error message
            self.log_to_console_2(deserialized_data)
        else:
            self.log_to_console_2("Deserialized data:")
            self.log_to_console_2(f"{deserialized_data[:100]}")  # Log only the first 1000 characters


    def get_deserialization_file_path(self):
        """Open a file dialog to select a file for deserialization."""
        file_path = tk.filedialog.askopenfilename(
            title="Select a file for deserialization",
            filetypes=[("Pickle files", "*.pkl"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        return file_path

    def log_to_console_2(self, message):
        """Log messages to the second console output widget."""
        self.console_output_2.insert(tk.END, message + "\n")
        self.console_output_2.see(tk.END)


    def start(self):
        """Start the GUI event loop."""
        self.window.mainloop()

