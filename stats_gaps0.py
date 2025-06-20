import numpy as np
import pandas as pd

# # Paste your data here
# data = {
#     "emoTouch_castadiva-public_raw_session7517B": [...],
#     ...
# }

import json

# Specify the path to your JSON file
json_path = "stats/castadiva-public-taps.json"

# Load the data from the file
with open(json_path, "r") as f:
    data = json.load(f)

# Now 'data' is your dictionary, just like before

# Calculate all time gaps
all_gaps = []
for timestamps in data.values():
    gaps = np.diff(timestamps)
    all_gaps.extend(gaps)

# Convert to pandas Series
gaps_series = pd.Series(all_gaps)

# Summary statistics
summary = {
    'Count': len(gaps_series),
    'Mean': gaps_series.mean(),
    'Median': gaps_series.median(),
    'Min': gaps_series.min(),
    'Max': gaps_series.max(),
    'Standard Deviation': gaps_series.std(),
    'Q1': gaps_series.quantile(0.25),
    'Q3': gaps_series.quantile(0.75),
    'IQR': gaps_series.quantile(0.75) - gaps_series.quantile(0.25),
}
print(pd.DataFrame.from_dict(summary, orient='index', columns=['Value']))
