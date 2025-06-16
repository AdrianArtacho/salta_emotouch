import pandas as pd
import glob
import os
import json

# Set the directory where your files are located
directory = 'OUTPUT/'

# Find all files that start with the desired prefix and end with .csv
file_pattern = os.path.join(directory, 'emoTouch_castadiva-public*.csv')
file_list = glob.glob(file_pattern)

# Prepare the dictionary to hold all DataFrames
all_data = {}

for file_path in file_list:
    # Use the filename (without extension) as the key
    key = os.path.splitext(os.path.basename(file_path))[0]
    df = pd.read_csv(file_path)
    # Convert DataFrame to a list of dicts (records)
    all_data[key] = df.to_dict(orient='records')

# Save all data to a JSON file
output_json = os.path.join(directory, 'castadiva-taps.json')
with open(output_json, 'w') as f:
    json.dump(all_data, f, indent=2)

print(f"Saved {len(all_data)} DataFrames to {output_json}")