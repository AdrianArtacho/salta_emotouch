import pandas as pd
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns

def main(df, project_name, label_string, video_length_value):
    # Lists to store all values for each project
    all_values = []
    value_types = []  # To distinguish between first and second values
    projects = []

    # Iterate through the DataFrame
    for index, row in df.iterrows():
        # Construct the file path
        json_file_path = os.path.join('OUTPUT', row['valid_stats'])
        
        # Open and load the JSON file
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            # Extract the values from the "ici" key
            average_length_tuple = data['ici']['Average Length']

            # Append values and project name to the lists
            all_values.append(average_length_tuple[0])
            value_types.append('First Value')
            projects.append(row['project_name'])

            all_values.append(average_length_tuple[1])
            value_types.append('Second Value')
            projects.append(row['project_name'])

    # Create a DataFrame for plotting
    plot_df = pd.DataFrame({
        'Project': projects,
        'Value': all_values,
        'Value Type': value_types
    })

    # Create a violin plot
    plt.figure(figsize=(12, 6))
    sns.violinplot(x='Project', y='Value', hue='Value Type', data=plot_df, inner='quartile', split=True)

    plt.title(project_name+' ('+str(video_length_value)+' sec.): Aggregated Comparison of First and Second Values')
    plt.ylabel('Values')
    plt.xlabel('Project Name')

    # Save the plot with a specific filename in the 'METADATA/' folder
    plt.savefig('METADATA/'+project_name+'-'+label_string+'-aggregated_violin.png')

    plt.show()

# Assuming 'df' is your DataFrame loaded from somewhere
# Call the main function with appropriate arguments
# main(df, "Your Project Name", "label_string", video_length_value)
