# -------------------------------------------------------------  
# Average Absolute Pearson Correlation for A/B pairs in  
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
with open("stats/"+proj_name+"-AB.json", "r") as f:  
    data_dict = json.load(f)  

# 2) Find A/B pairs --------------------------------------------
pairs = []
for key in data_dict:
    if key.endswith('A'):
        base = key[:-1]
        key_B = base + 'B'
        if key_B in data_dict:
            pairs.append((key, key_B))

if not pairs:
    print("No A/B pairs found.")
    exit()

# 3) Compute correlations for each pair ------------------------
correlations = []
for key_A, key_B in pairs:
    sA = pd.Series(data_dict[key_A])
    sB = pd.Series(data_dict[key_B])
    # Align by index (handles unequal lengths)
    df_pair = pd.concat([sA, sB], axis=1)
    df_pair.columns = ['A', 'B']
    corr = df_pair.corr().iloc[0, 1]  # Pearson correlation between A and B
    correlations.append(corr)

# 4) Average absolute correlation ------------------------------
mean_abs_corr = np.mean(np.abs(correlations))

# 5) Report ----------------------------------------------------
print("Average absolute Pearson correlation for A/B pairs in "+proj_name+" =", mean_abs_corr)
print("Number of pairs:", len(pairs))