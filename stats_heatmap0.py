# -------------------------------------------------------------  
# Correlation analysis of time-series stored in castadiva-public-taps.json  
# -------------------------------------------------------------  
import json  
import pandas as pd  
import matplotlib.pyplot as plt  
import seaborn as sns  
import gui.gui_enterstring_t as gui_enterstring

proj_name = gui_enterstring.main(
    'Enter name defining the files', 'string', 'Project name',
    default_text='castadiva-public',
    verbose=False
)
print(proj_name)

substring = proj_name.split('-')[0]
print(substring)
# exit()

  
# 1) Load the JSON file ---------------------------------------  
with open("stats/"+proj_name+"-taps.json", "r") as f:  
    data_dict = json.load(f)          # keys = series-names, values = lists  
  
# 2) Align the series into a DataFrame -------------------------  
# Different keys have different lengths → build Series then concat  
series_list = [pd.Series(values, name=key) for key, values in data_dict.items()]  
df = pd.concat(series_list, axis=1)  
  
# Optional sanity check  
print("Head of aligned DataFrame:")  
print(df.head(), "\n")               # first few rows  
print("Shape:", df.shape, "\n")       # (rows, columns)  
  
# 3) Compute pair-wise Pearson correlations --------------------  
corr = df.corr()                     # pandas ignores NaNs pair-wise  
  
print("Correlation matrix:")  
print(corr, "\n")  
  
# 4) Visualise as a heat-map -----------------------------------  
plt.figure(figsize=(10, 8))  
sns.heatmap(  
    corr,  
    annot=True, fmt=".2f",  
    cmap="coolwarm",  
    square=True,  
    linewidths=0.5,  
    cbar_kws={"shrink": 0.8}  
)  
plt.title("Correlation Heat-map of "+substring+" Time-Series")  
plt.tight_layout()  
plt.savefig("stats/heatmap_"+substring+".png", dpi=300, bbox_inches='tight')
plt.show()  