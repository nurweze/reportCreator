import os
import logging
import sys


# Check if the script is being called from the GUI
IS_GUI = len(sys.argv) > 1 and sys.argv[1] == "gui"  

# Add the parent directory to sys.path to access processes and importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from exportable import ReportGenerator


IS_GUI = len(sys.argv) > 1 and sys.argv[1] == "gui"  

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def main():
    logger.info("Starting report generation...")
    report_gen = ReportGenerator()
    report_gen.generate_report()

if __name__ == "__main__":
    main()


