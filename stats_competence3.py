import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the JSON data
with open('METADATA/metadata-dates.json') as f:
    data = json.load(f)

# Filter for Pleyades-public sessions and extract needed fields
records = []
for session in data.values():
    if session.get('project_name') == 'Pleyades-public':
        age = session.get('subject_age')
        music = int(session.get('subject_music', 0))
        dance = int(session.get('subject_dance', 0))
        if age:
            records.append({
                'age_range': age,
                'music_competence': music,
                'dance_competence': dance
            })

df = pd.DataFrame(records)

# Sort age ranges numerically
def age_key(age_str):
    return int(age_str.split('-')[0])

ordered_ages = sorted(df['age_range'].unique(), key=age_key)
df['age_range'] = pd.Categorical(df['age_range'], categories=ordered_ages, ordered=True)

# Melt dataframe for easier plotting
melted_df = df.melt(id_vars='age_range',
                    value_vars=['music_competence', 'dance_competence'],
                    var_name='Competence Type',
                    value_name='Score')

# Define custom palette
palette = {
    'music_competence': '#2ca02c',  # green
    'dance_competence': '#ff7f0e'   # orange
}

# Plot
plt.figure(figsize=(12, 6))
box = sns.boxplot(
    x='age_range',
    y='Score',
    hue='Competence Type',
    data=melted_df,
    palette=palette
)

# Fix legend: set labels in the same order as hue levels
handles, labels = box.get_legend_handles_labels()
label_map = {
    'music_competence': 'Music',
    'dance_competence': 'Dance'
}
box.legend(
    handles=[handles[labels.index('music_competence')], handles[labels.index('dance_competence')]],
    labels=['Music', 'Dance'],
    title='Competence Type'
)

plt.title('Music and Dance Competence by Age Range (All Genders)')
plt.xlabel('Age Range')
plt.ylabel('Competence (1–7 Likert Scale)')
plt.tight_layout()
plt.savefig('STATS/competence_by_age_range.png', dpi=300)
plt.show()
