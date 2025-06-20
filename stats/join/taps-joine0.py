import json
import glob

# List your JSON files (adjust the pattern as needed)
json_files = glob.glob('*.json')

merged_data = {}

for file in json_files:
    with open(file, 'r') as f:
        data = json.load(f)
        merged_data.update(data)  # If keys overlap, later files overwrite earlier ones

# Save the merged result
with open('merged.json', 'w') as f:
    json.dump(merged_data, f, indent=2)