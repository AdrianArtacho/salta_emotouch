# -------------------------------------------------------------  
# Average Absolute Pair-wise Pearson Correlation for  
# 'castadiva-public-taps.json'  
# -------------------------------------------------------------  
import json  
import numpy as np  
import pandas as pd  
import gui.gui_enterstring_t as gui_enterstring

proj_name = gui_enterstring.main(
    'Enter name defining the files', 'string', 'Project name',
    default_text='castadiva-public',
    verbose=False
)
print(proj_name)

# 1) Load JSON -------------------------------------------------  
with open("stats/"+proj_name+"-taps.json", "r") as f:  
    data_dict = json.load(f)  
  
# 2) Build aligned DataFrame (concat unequal length series) ----  
series_list = [pd.Series(vals, name=key) for key, vals in data_dict.items()]  
df = pd.concat(series_list, axis=1)  
  
# 3) Compute Pearson correlation matrix ------------------------  
corr = df.corr()                     # pair-wise, ignores NaNs  
  
# 4) Extract the upper triangle (unique pairs) -----------------  
n = corr.shape[0]  
upper = corr.values[np.triu_indices(n, k=1)]   # k=1 → exclude diagonal  
  
# 5) Average absolute correlations -----------------------------  
mean_abs_corr = np.mean(np.abs(upper))  
  
# 6) Report ----------------------------------------------------  
print("Average absolute pair-wise Pearson correlation for "+proj_name+"=", mean_abs_corr)