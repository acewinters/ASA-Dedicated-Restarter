import os
import subprocess
import psutil
import time

# Define the list of applications to monitor
applications = [
    {
        'name': 'Application1.exe',
        'batch_file': 'path/to/batch/file1.bat',
        'process_id': None
    },
    {
        'name': 'Application2.exe',
        'batch_file': 'path/to/batch/file2.bat',
        'process_id': None
    },
    # Add more applications as needed
]

# Function to check if the application is running
def is_running(process_id):
    try:
        process = psutil.Process(process_id)
        return process.is_running()
    except psutil.NoSuchProcess:
        return False

# Function to terminate the application
def terminate_application(process_id):
    try:
        process = psutil.Process(process_id)
        process.terminate()
        process.wait()
    except psutil.NoSuchProcess:
        pass

# Function to start the batch file for the application
def start_batch_file(batch_file):
    subprocess.Popen(batch_file)

# Main loop
while True:
    for application in applications:
        if application['process_id'] is None or not is_running(application['process_id']):
            # Application is not running or has crashed, start the batch file
            if application['process_id'] is not None:
                terminate_application(application['process_id'])
            start_batch_file(application['batch_file'])
            time.sleep(5)  # Wait for the application to start
            # Get the new process ID
            for process in psutil.process_iter(['pid', 'name']):
                if process.info['name'] == application['name']:
                    application['process_id'] = process.info['pid']
                    break
    time.sleep(30)  # Check the status every 30 seconds
