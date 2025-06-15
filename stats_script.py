import json
import pandas as pd

# Load your JSON file
with open("METADATA/metadata-dates.json") as f:
    data = json.load(f)

# Extract data
records = []
for key, entry in data.items():
    session_id = entry.get("session_id", key.split("-")[-1])
    date = entry["project_dates"][0].split()[0]
    project_name = entry.get("project_name", key.split("_")[0])
    gender = entry.get("subject_gender")
    age_range = entry.get("subject_age")
    music = int(entry.get("subject_music", 0))
    dance = int(entry.get("subject_dance", 0))
    annotation = entry.get("valid_annotation")
    taps = int(entry.get("taps_A", 0)) if annotation == "A" else int(entry.get("taps_B", 0))
    
    records.append({
        "session_id": session_id,
        "project_name": project_name,
        "annotation": annotation,
        "date": date,
        "gender": gender,
        "age_range": age_range,
        "music_competence": music,
        "dance_competence": dance,
        "taps": taps
    })

# Create DataFrame
df = pd.DataFrame(records)
print(df.head())  # or 
df.to_csv("OUTPUT/stats.csv", index=False)
