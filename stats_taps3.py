import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator

# Load the JSON file
with open('METADATA/metadata-dates.json') as f:
    data = json.load(f)

# Mapping from project name to experiment label
project_label_map = {
    'Pleyades-public': 'Exp. 1',
    'castadiva-public': 'Exp. 2',
    'huggy-public': 'Exp. 3',
    'duo-public': 'Exp. 4',
    'piano-public': 'Exp. 5',
    'speech-public': 'Exp. 6'
}

experiment_order = ['Exp. 1', 'Exp. 2', 'Exp. 3', 'Exp. 4', 'Exp. 5', 'Exp. 6']

# Extract relevant data
records = []
for session in data.values():
    project = session.get('project_name')
    annotation = session.get('valid_annotation')
    taps_a = int(session.get('taps_A', 0))
    taps_b = int(session.get('taps_B', 0))

    if project in project_label_map:
        label = project_label_map[project]
        taps = taps_a if annotation == 'A' else taps_b
        records.append({
            'experiment': label,
            'taps': taps
        })

df = pd.DataFrame(records)
df['experiment'] = pd.Categorical(df['experiment'], categories=experiment_order, ordered=True)

# Remove outliers using IQR method per experiment group
def remove_outliers(group):
    Q1 = group['taps'].quantile(0.25)
    Q3 = group['taps'].quantile(0.75)
    IQR = Q3 - Q1
    return group[(group['taps'] >= Q1 - 1.5 * IQR) & (group['taps'] <= Q3 + 1.5 * IQR)]

df_filtered = df.groupby('experiment', group_keys=False).apply(remove_outliers)

# Plot
plt.figure(figsize=(12, 6))
ax = sns.boxplot(data=df_filtered, x='experiment', y='taps', palette='Set3')
ax.yaxis.set_major_locator(MaxNLocator(integer=True))

plt.title('Distribution of Taps per Experiment (Outliers Removed)')
plt.xlabel('Experiment')
plt.ylabel('Number of Taps (Filtered)')
plt.tight_layout()
plt.savefig("stats/stats_taps_filtered.png", dpi=300, bbox_inches='tight')
plt.show()
