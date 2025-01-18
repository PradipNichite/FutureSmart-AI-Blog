import os 
from datetime import *
import logging

today_date = datetime.now().strftime('%Y-%m-%d')
log_base_directory = 'logs'
log_subdirectory = os.path.join(log_base_directory, today_date)
os.makedirs(log_subdirectory, exist_ok=True)

# Define the path to the log file inside the day-wise subdirectory
log_file_path = os.path.join(log_subdirectory, 'app.log')

logging.basicConfig(
    level=logging.INFO,  # Set the default logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log message format
    handlers=[
        logging.FileHandler(log_file_path),  # Output logs to the log file
        logging.StreamHandler()  # Output logs to the console (optional)
    ]
)

logger= logging.getLogger('api_logger')