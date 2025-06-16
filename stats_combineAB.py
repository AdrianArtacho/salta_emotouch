import pandas as pd
import glob
import os
import json
import gui.gui_enterstring_t as gui_enterstring

proj_name = gui_enterstring.main(
    'Enter name defining the files', 'string', 'Project name',
    default_text='castadiva-public',
    verbose=False
)

print(proj_name)

input_directory = 'OUTPUT/'
output_directory = 'stats/'

file_pattern = os.path.join(input_directory, 'emoTouch_' + proj_name + '*.csv')
file_list = glob.glob(file_pattern)

# Load metadata keys
with open('METADATA/metadata.json', 'r') as f:
    metadata = json.load(f)
metadata_keys = list(metadata.keys())

all_data = {}

for file_path in file_list:
    key = os.path.splitext(os.path.basename(file_path))[0]
    session_part = key[-5:-1]  # e.g. '7351A' -> '7351'
    if any(meta_key[-4:] == session_part for meta_key in metadata_keys):
        df = pd.read_csv(file_path)
        if len(df) > 2:
            filtered = pd.concat([
                df.iloc[[0]],
                df.iloc[1:-1][df.iloc[1:-1]['x'] != 0],
                df.iloc[[-1]]
            ], ignore_index=False)
        else:
            filtered = df
        # Store the 'created_at_relative' values as a list
        all_data[key] = filtered['created_at_relative'].tolist()

output_json = os.path.join(output_directory, proj_name + '-AB.json')
os.makedirs(output_directory, exist_ok=True)
with open(output_json, 'w') as f:
    json.dump(all_data, f, indent=2)

print(f"Saved {len(all_data)} lists of 'created_at_relative' values to {output_json}")