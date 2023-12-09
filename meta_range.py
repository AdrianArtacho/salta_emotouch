import pandas as pd
import json
import os
import matplotlib.pyplot as plt

def main(df, project_name, label_string, video_length_value):
    # Dictionary to store aggregated values for each project
    aggregated_first_values = {}
    aggregated_second_values = {}

    # Iterate through the DataFrame
    for index, row in df.iterrows():
        # Construct the file path
        json_file_path = os.path.join('OUTPUT', row['valid_stats'])
        
        # Open and load the JSON file
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            # Extract the values from the "ici" key
            average_length_tuple = data['ici']['Average Length']
            project = row['project_name']

            # Initialize lists in dictionary if project not yet encountered
            if project not in aggregated_first_values:
                aggregated_first_values[project] = []
                aggregated_second_values[project] = []

            # Append values to the respective lists
            aggregated_first_values[project].append(average_length_tuple[0])
            aggregated_second_values[project].append(average_length_tuple[1])

    # Convert aggregated values to DataFrame for easier plotting
    aggregated_df = pd.DataFrame({
        'Project': list(aggregated_first_values.keys()),
        'First Value Average': [sum(values)/len(values) for values in aggregated_first_values.values()],
        'Second Value Average': [sum(values)/len(values) for values in aggregated_second_values.values()]
    })

    # Create a plot
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plotting aggregated first values
    ax1.bar(aggregated_df['Project'], aggregated_df['First Value Average'], color='blue', alpha=0.6, label='First Value Average')
    ax1.set_xlabel('Project Name')
    ax1.set_ylabel('First Value Average (seconds)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Create a twin axis for aggregated second values
    ax2 = ax1.twinx()
    ax2.plot(aggregated_df['Project'], aggregated_df['Second Value Average'], color='green', marker='o', label='Second Value Average')
    ax2.set_ylabel('Second Value Average (percentage)', color='green')
    ax2.tick_params(axis='y', labelcolor='green')

    # Adding legends
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.title(project_name+' ('+str(video_length_value)+' sec.): Aggregated Comparison of First and Second Values')

    # Save the plot with a specific filename in the 'METADATA/' folder
    plt.savefig('METADATA/emo-'+label_string+'-aggregated.png')

    plt.show()

# Assuming 'df' is your DataFrame loaded from somewhere
# Call the main function with appropriate arguments
# main(df, "Your Project Name", "label_string", video_length_value)

if __name__ == "__main__":
    main()
