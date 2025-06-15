import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator

# Load the JSON file
with open('METADATA/metadata-dates.json') as f:
    data = json.load(f)

# Extract project_name, valid_annotation, and taps
records = []
for session in data.values():
    project = session.get('project_name')
    annotation = session.get('valid_annotation')
    taps_a = int(session.get('taps_A', 0))
    taps_b = int(session.get('taps_B', 0))

    # Choose taps based on annotation
    taps = taps_a if annotation == 'A' else taps_b

    if project:
        records.append({
            'project_name': project,
            'taps': taps
        })

df = pd.DataFrame(records)

# Plot
plt.figure(figsize=(12, 6))
ax = sns.boxplot(data=df, x='project_name', y='taps', palette='Set3')

# Ensure integer y-axis ticks
ax.yaxis.set_major_locator(MaxNLocator(integer=True))

plt.title('Distribution of Taps per Experiment')
plt.xlabel('Experiment (Project Name)')
plt.ylabel('Number of Taps (based on Valid Annotation)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
