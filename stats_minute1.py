import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator

# Load JSON data
with open('METADATA/metadata-dates.json') as f:
    data = json.load(f)

# Updated project mapping (Exp. 3 removed)
project_label_map = {
    'Pleyades-public': 'Exp. 1',
    'castadiva-public': 'Exp. 2',
    # 'conducting-public': 'Exp. 3',  ← excluded
    'huggy-public': 'Exp. 4',
    'duo-public': 'Exp. 5',
    'piano-public': 'Exp. 6',
    'speech-public': 'Exp. 7'
}

# Updated durations (Exp. 3 removed)
experiment_durations = {
    'Exp. 1': 178,
    'Exp. 2': 208,
    'Exp. 4': 58,
    'Exp. 5': 136,
    'Exp. 6': 194,
    'Exp. 7': 78
}

# Ordered list without Exp. 3
experiment_order = list(experiment_durations.keys())

# Extract and compute taps per minute
records = []
for session in data.values():
    project = session.get('project_name')
    annotation = session.get('valid_annotation')
    taps_a = int(session.get('taps_A', 0))
    taps_b = int(session.get('taps_B', 0))

    if project in project_label_map:
        label = project_label_map[project]
        duration_min = experiment_durations[label] / 60
        taps = taps_a if annotation == 'A' else taps_b
        if duration_min > 0:
            tpm = taps / duration_min
            records.append({
                'experiment': label,
                'taps_per_minute': tpm
            })

df = pd.DataFrame(records)
df['experiment'] = pd.Categorical(df['experiment'], categories=experiment_order, ordered=True)

# Plot
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='experiment', y='taps_per_minute', palette='Set3')
plt.title('Taps per Minute Across Experiments (Excluding Exp. 3)')
plt.xlabel('Experiment')
plt.ylabel('Taps per Minute')
plt.tight_layout()
plt.savefig("stats/stats_taps_per_minute_excluding_exp3.png", dpi=300, bbox_inches='tight')
plt.show()
