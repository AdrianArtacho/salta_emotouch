""" This script that iterates over all .csv files in a folder 
    (e.g.'INPUT/') and runs the command 
    EMOTOUCH.main(input_filepath=<filepath>) 
    for each of them.
"""

import os
import emotouch
import time

# Define the directory containing the CSV files
directory = 'INPUT/'

# Iterate over all files in the directory
for filename in os.listdir(directory):
    # Check if the file is a CSV file
    if filename.endswith('.csv'):
        # Construct the full file path
        filepath = os.path.join(directory, filename)

        try:
            # Call the EMOTOUCH.main function with the file path
            EMOTOUCH.main(input_filepath=filepath)
            print(f"Processed file: {filename}")
        except Exception as e:
            print(f"Error processing file {filename}: {e}")

        # Pause for a specified number of seconds
        time.sleep(2)  # Pauses for 2 seconds, adjust the number as needed