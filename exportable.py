import tkinter as tk
from tkinter import filedialog
import io
import sys

class Exportable:
    
    
    def __init__(self, gui):
        self.gui = gui  # Reference to the GUIMaker instance


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
        # Capture output
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
