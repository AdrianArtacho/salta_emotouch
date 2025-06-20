# -----------------------------------------------------------  
# gap_analysis.py  – Analyse variability of time-stamp gaps  
# -----------------------------------------------------------  
# 1. Standard imports  
import json  
import re  
import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  
import seaborn as sns  
  
import json

# Specify the path to your JSON file
json_path = "stats/castadiva-public-taps.json"

# Load the data from the file
with open(json_path, "r") as f:
    json_data = json.load(f)
# json_data = json.loads(json_str)    # <- dict keyed by session name  
  
# json_data = json.loads(json_str)    # <- dict keyed by session name  
  
# 4. Compute gaps + stats -----------------------------------  
stats_rows = []     # collect rows for summary table  
all_gaps   = []     # collect all gaps across every series  
  
for series, ts in json_data.items():  
    # remove sentinel marker ‘111111’ if present  
    timepoints = [t for t in ts if t != 111111]  
  
    # successive differences:  
    gaps = np.diff(timepoints)  
  
    if len(gaps) == 0:  
        # skip empty / singleton series  
        continue  
  
    gaps_ser = pd.Series(gaps)  
    stats_rows.append({  
        'series': series,  
        'count':  gaps_ser.count(),  
        'mean':   gaps_ser.mean(),  
        'median': gaps_ser.median(),  
        'std':    gaps_ser.std(),  
        'min':    gaps_ser.min(),  
        'max':    gaps_ser.max(),  
        'IQR':    gaps_ser.quantile(0.75) - gaps_ser.quantile(0.25),  
        'cv':     gaps_ser.std() / gaps_ser.mean()  # coefficient of variation  
    })  
  
    all_gaps.extend(gaps.tolist())  
  
summary_df = (
    pd.DataFrame(stats_rows)
      .sort_values('cv', ascending=False)
      .reset_index(drop=True)
) 
  
# 5. Show the summary table ---------------------------------  
print('Per-session gap statistics:')  
print(summary_df.to_string(index=False, float_format='{:,.1f}'.format))  
  
# 6. Overall distribution numbers ---------------------------  
overall = pd.Series(all_gaps)  
print('\nOverall median gap  (ms):', overall.median())  
print('Overall IQR gap     (ms):', overall.quantile(0.75) - overall.quantile(0.25))  
  
# 7. Box-plot of gaps per series ----------------------------  
records = [{'series': s, 'gap_ms': g}  
           for s, ts in json_data.items()  
           for g in np.diff([t for t in ts if t != 111111])]  
  
long_df = pd.DataFrame(records)  
  
plt.figure(figsize=(11, 4))  
sns.boxplot(x='series', y='gap_ms', data=long_df, palette='Set3')  
plt.xticks(rotation=90)  
plt.title('Gap length distribution per series (ms)')  
plt.ylabel('Gap length (ms)')  
plt.xlabel('')  
plt.tight_layout()  
plt.show()  