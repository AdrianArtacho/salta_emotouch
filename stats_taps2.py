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
    # 'conducting-public': 'Exp. 3',
    'huggy-public': 'Exp. 3',
    'duo-public': 'Exp. 4',
    'piano-public': 'Exp. 5',
    'speech-public': 'Exp. 6'
}

# Desired experiment order
experiment_order = ['Exp. 1', 'Exp. 2', 'Exp. 3', 'Exp. 4', 'Exp. 5', 'Exp. 6'
                    # , 'Exp. 7'
                    ]

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

# Plot
plt.figure(figsize=(12, 6))
ax = sns.boxplot(data=df, x='experiment', y='taps', palette='Set3')
ax.yaxis.set_major_locator(MaxNLocator(integer=True))

plt.title('Distribution of Taps per Experiment')
plt.xlabel('Experiment')
plt.ylabel('Number of Taps (based on Valid Annotation)')
plt.tight_layout()
plt.savefig("stats/stats_taps2.png", dpi=300, bbox_inches='tight')
plt.show()
