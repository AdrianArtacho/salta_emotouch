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

# Load metadata and build a set of valid session+annotation codes
with open('METADATA/metadata.json', 'r') as f:
    metadata = json.load(f)

valid_codes = set()
for meta_key, meta_val in metadata.items():
    session_num = meta_key[-4:]
    annotation = str(meta_val.get('valid_annotation', '')).strip()
    if annotation in ('A', 'B'):
        valid_codes.add(session_num + annotation)

all_data = {}

for file_path in file_list:
    key = os.path.splitext(os.path.basename(file_path))[0]
    session_code = key[-5:]  # e.g. '7351A'
    if session_code in valid_codes:
        df = pd.read_csv(file_path)
        if len(df) > 2:
            filtered = pd.concat([
                df.iloc[[0]],
                df.iloc[1:-1][df.iloc[1:-1]['x'] != 0],
                df.iloc[[-1]]
            ], ignore_index=False)
        else:
            filtered = df
        all_data[key] = filtered['created_at_relative'].tolist()

output_json = os.path.join(output_directory, proj_name + '-taps.json')
os.makedirs(output_directory, exist_ok=True)
with open(output_json, 'w') as f:
    json.dump(all_data, f, indent=2)

print(f"Saved {len(all_data)} lists of 'created_at_relative' values to {output_json}")