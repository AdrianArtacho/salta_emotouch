import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the JSON file
with open('METADATA/metadata-dates.json') as f:
    data = json.load(f)

# Extract relevant fields from 'Pleyades-public' sessions
records = []
for session in data.values():
    if session.get('project_name') == 'Pleyades-public':
        records.append({
            'gender': session.get('subject_gender'),
            'age_range': session.get('subject_age'),
            'music_competence': int(session.get('subject_music', 0)),
            'dance_competence': int(session.get('subject_dance', 0))
        })

df = pd.DataFrame(records)

# Determine unique age ranges and sort them numerically
def age_key(age_str):
    try:
        return int(age_str.split('-')[0])
    except:
        return 999  # place malformed ages at end

ordered_ages = sorted(df['age_range'].dropna().unique(), key=age_key)
df['age_range'] = pd.Categorical(df['age_range'], categories=ordered_ages, ordered=True)

# Set up plotting style
sns.set(style="whitegrid")

# Plot 1: Music Competence by Age Range
plt.figure(figsize=(10, 6))
sns.boxplot(x='age_range', y='music_competence', hue='gender', data=df, palette='Set2')
plt.title('Subjective Music Competence (1–7 Likert) by Age and Gender')
plt.ylabel('Music Competence')
plt.xlabel('Age Range')
plt.legend(title='Gender')
plt.tight_layout()
plt.show()

# Plot 2: Dance Competence by Age Range
plt.figure(figsize=(10, 6))
sns.boxplot(x='age_range', y='dance_competence', hue='gender', data=df, palette='Set3')
plt.title('Subjective Dance Competence (1–7 Likert) by Age and Gender')
plt.ylabel('Dance Competence')
plt.xlabel('Age Range')
plt.legend(title='Gender')
plt.tight_layout()
plt.show()

# Optional: joint distribution
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x='music_competence', y='dance_competence', hue='gender', style='age_range', palette='tab10')
plt.title('Music vs Dance Competence')
plt.xlabel('Music Competence')
plt.ylabel('Dance Competence')
plt.legend(title='Gender / Age')
plt.tight_layout()
plt.show()
