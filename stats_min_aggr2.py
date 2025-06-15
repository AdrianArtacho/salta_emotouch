import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

# Load the JSON file
with open('METADATA/metadata-dates.json') as f:
    data = json.load(f)

# Duration map (Exp. 3 excluded)
project_duration_map = {
    'Pleyades-public': 178,
    'castadiva-public': 208,
    'conducting-public': 40,
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

# Plot with secondary y-axis
fig, ax1 = plt.subplots(figsize=(6, 6))

# Primary axis: taps per minute
sns.boxplot(y='taps_per_minute', data=df, color='lightblue', ax=ax1)
ax1.set_ylabel('Taps per Minute')
ax1.set_xlabel('All Experiments Combined')
ax1.set_title('Taps per Minute with Equivalent Seconds per Tap')

# Secondary axis: seconds per tap
def tpm_to_seconds(x):
    return 60 / x if x != 0 else 0

def seconds_to_tpm(x):
    return 60 / x if x != 0 else 0

ax2 = ax1.twinx()
y_ticks = ax1.get_yticks()
ax2.set_yticks(y_ticks)
ax2.set_yticklabels([f'{tpm_to_seconds(y):.0f} sec' if y > 0 else '' for y in y_ticks])
ax2.set_ylabel('Seconds per Tap')

plt.tight_layout()
plt.savefig("stats/stats_tpm_and_seconds2.png", dpi=300, bbox_inches='tight')
plt.show()
