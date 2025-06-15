import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator

# Load the JSON file
with open('METADATA/metadata-dates.json') as f:
    data = json.load(f)

# Map project names to experiment labels
project_label_map = {
    'Pleyades-public': 'Exp. 1',
    'castadiva-public': 'Exp. 2',
    # 'conducting-public': 'Exp. 3',
    'huggy-public': 'Exp. 3',
    'duo-public': 'Exp. 4',
    'piano-public': 'Exp. 5',
    'speech-public': 'Exp. 6'
}

# Map durations in seconds per experiment
experiment_durations = {
    'Exp. 1': 178,
    'Exp. 2': 208,
    'Exp. 3': 40,
    'Exp. 4': 58,
    'Exp. 5': 136,
    'Exp. 6': 194,
    # 'Exp. 7': 78
}

# Ordered list of experiments
experiment_order = list(experiment_durations.keys())

# Extract and transform data
records = []
for session in data.values():
    project = session.get('project_name')
    annotation = session.get('valid_annotation')
    taps_a = int(session.get('taps_A', 0))
    taps_b = int(session.get('taps_B', 0))

    if project in project_label_map:
        exp_label = project_label_map[project]
        taps = taps_a if annotation == 'A' else taps_b
        if taps > 0:
            seconds_per_tap = experiment_durations[exp_label] / taps
            records.append({
                'experiment': exp_label,
                'seconds_per_tap': seconds_per_tap
            })

# Create DataFrame
df = pd.DataFrame(records)
df['experiment'] = pd.Categorical(df['experiment'], categories=experiment_order, ordered=True)

# Plot
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='experiment', y='seconds_per_tap', palette='Set3')

plt.title('Seconds per Tap Across Experiments')
plt.xlabel('Experiment')
plt.ylabel('Seconds per Tap')
plt.tight_layout()
plt.savefig("stats/stats_seconds_per_tap.png", dpi=300, bbox_inches='tight')
plt.show()
