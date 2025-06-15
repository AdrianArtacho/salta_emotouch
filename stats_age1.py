import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator

# Load JSON data
with open('METADATA/metadata-dates.json') as f:
    data = json.load(f)

# Extract only 'Pleyades-public' sessions with age and gender
records = []
for session in data.values():
    if session.get('project_name') == 'Pleyades-public':
        age = session.get('subject_age')
        gender = session.get('subject_gender')
        if age and gender:
            records.append({
                'age_range': age,
                'gender': gender
            })

df = pd.DataFrame(records)

# Order age ranges
def age_key(age_str):
    return int(age_str.split('-')[0])

ordered_ages = sorted(df['age_range'].unique(), key=age_key)
df['age_range'] = pd.Categorical(df['age_range'], categories=ordered_ages, ordered=True)

# Plot
plt.figure(figsize=(10, 6))
ax = sns.countplot(data=df, x='age_range', hue='gender', palette='Set2')

# Force y-axis to show only integer ticks
ax.yaxis.set_major_locator(MaxNLocator(integer=True))

plt.title('Participant Gender Distribution by Age Range')
plt.xlabel('Age Range')
plt.ylabel('Number of Participants')
plt.legend(title='Gender')
plt.tight_layout()
plt.savefig("stats/stats_age.png", dpi=300, bbox_inches='tight')
plt.show()
