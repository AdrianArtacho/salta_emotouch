import json
import os
import matplotlib.pyplot as plt

def main(df, project_name, label_string, video_length_value):
    # Lists to store the first and second values of the tuples
    first_values = []
    second_values = []

    # Iterate through the DataFrame
    for index, row in df.iterrows():
        # Construct the file path
        json_file_path = os.path.join('OUTPUT', row['valid_stats'])
        
        # Open and load the JSON file
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            # Extract the values from the "ici" key
            average_length_tuple = data['ici']['Average Length']
            first_values.append(average_length_tuple[0])
            second_values.append(average_length_tuple[1])

    # Create a plot
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plotting the first set of values (lengths in seconds)
    ax1.bar(df['session_id'].astype(str), first_values, color='blue', alpha=0.6, label='Length (seconds)')
    ax1.set_xlabel('User Session ID (sorted by subjective competence)')
    ax1.set_ylabel('Interval Length (seconds)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Create a twin axis for the second set of values (percentages)
    ax2 = ax1.twinx()
    ax2.plot(df['session_id'].astype(str), second_values, color='green', marker='o', label='Percentage')
    ax2.set_ylabel('Percentage (%) of total length', color='green')
    ax2.tick_params(axis='y', labelcolor='green')

    # Adding legendsdf_sorted
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.title(project_name+' ('+str(video_length_value)+' sec.): Comparison of Lengths and Percentages per User')

    # Save the plot with a specific filename in the 'METADATA/' folder
    plt.savefig('METADATA/emo-'+label_string+'-allusers.png')

    plt.show()

if __name__ == "__main__":
    main()