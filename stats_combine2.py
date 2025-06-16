import pandas as pd
import glob
import os
import json

input_directory = 'OUTPUT/'
output_directory = 'stats/'

file_pattern = os.path.join(input_directory, 'emoTouch_castadiva-public*.csv')
file_list = glob.glob(file_pattern)

all_data = {}

for file_path in file_list:
    key = os.path.splitext(os.path.basename(file_path))[0]
    df = pd.read_csv(file_path)
    if len(df) > 2:
        filtered = pd.concat([
            df.iloc[[0]],
            df.iloc[1:-1][df.iloc[1:-1]['x'] != 0],
            df.iloc[[-1]]
        ], ignore_index=True)
    else:
        filtered = df
    # Store only the 'x' values as a list
    all_data[key] = filtered['x'].tolist()

output_json = os.path.join(output_directory, 'castadiva-taps.json')
with open(output_json, 'w') as f:
    json.dump(all_data, f, indent=2)

print(f"Saved {len(all_data)} lists of 'x' values to {output_json}")