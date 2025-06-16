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
        # Keep first and last row, and all rows where 'x' != 0 (except first/last)
        filtered = pd.concat([
            df.iloc[[0]],
            df.iloc[1:-1][df.iloc[1:-1]['x'] != 0],
            df.iloc[[-1]]
        ], ignore_index=True)
    else:
        # If only two or fewer rows, keep all
        filtered = df
    all_data[key] = filtered.to_dict(orient='records')

output_json = os.path.join(output_directory, 'castadiva-taps.json')
with open(output_json, 'w') as f:
    json.dump(all_data, f, indent=2)

print(f"Saved {len(all_data)} filtered DataFrames to {output_json}")