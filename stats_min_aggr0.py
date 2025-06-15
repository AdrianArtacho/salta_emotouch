import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator

# Load the JSON file
with open('METADATA/metadata-dates.json') as f:
    data = json.load(f)

# Mapping of project → duration (Exp. 3 excluded)
project_duration_map = {
    'Pleyades-public': 178,
    'castadiva-public': 208,
    # 'conducting-public': 40,  ← excluded
    'huggy-public': 58,
    'duo-public': 136,
    'piano-public': 194,
    'speech-public': 78
}

# Extract and compute taps per minute
records = []
for session in data.values():
    project = session.get('project_name')
    annotation = session.get('valid_annotation')
    taps_a = int(session.get('taps_A', 0))
    taps_b = int(session.get('taps_B', 0))

    if project in project_duration_map:
        duration_min = project_duration_map[project] / 60
        taps = taps_a if annotation == 'A' else taps_b
        if duration_min > 0:
            tpm = taps / duration_min
            records.append({'taps_per_minute': tpm})

df = pd.DataFrame(records)

# Plot
plt.figure(figsize=(6, 6))
sns.boxplot(y='taps_per_minute', data=df, color='lightblue')
plt.title('Taps per Minute (All Experiments Combined, Excluding Exp. 3)')
plt.ylabel('Taps per Minute')
plt.xlabel('All Experiments Combined')
plt.tight_layout()
plt.show()
