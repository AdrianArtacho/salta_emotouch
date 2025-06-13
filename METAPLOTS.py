""" This script creates a DataFrame from a JSON file 
    with only the entries that have 'project_name' 
    as "Pleyades-public" and 'valid_stats' that is not "none" or "?"
"""

import json
import pandas as pd
import os
import matplotlib.pyplot as plt
import gui.gui_enterstring_t as gui_enterstring


def main(project_name,
         verbose=False):
    # Load the JSON file
    with open('METADATA/metadata.json', 'r') as file:
        data = json.load(file)

    # Filter the data
    filtered_data = []
    for key, value in data.items():
        if value['project_name'] == project_name and value['valid_stats'] not in ['none', '?']:
            filtered_data.append(value)

    # Convert the filtered data into a DataFrame
    df = pd.DataFrame(filtered_data)

    #--------
    print(df.head())
    print(df.columns)
    # Show only selected columns
    cols = ['session_id', 'project_name', 'subject_gender', 'subject_age', 'subject_music', 'subject_dance']
    print(df[cols])
    # exit()

    #------- demographic data
    import meta_demo
    meta_demo.main(df, project_name)

    #------- Convert 'subject_music' and 'subject_dance' to integers
    df['subject_music'] = df['subject_music'].astype(int)
    df['subject_dance'] = df['subject_dance'].astype(int)

    # Calculate the sum of 'subject_music' and 'subject_dance'
    df['music_dance_sum'] = df['subject_music'] + df['subject_dance']

    # Sort the DataFrame by the new column in descending order
    df_sorted = df.sort_values(by='music_dance_sum', ascending=False)

    # Reset the index if necessary
    df_sorted.reset_index(drop=True, inplace=True)

    # Print the sorted DataFrame
    print(df_sorted)
   
    #------- Get total length
    cached_df = pd.read_csv('METADATA/'+'cached_info.csv')
    filtered_df = cached_df[cached_df['TEST'] == project_name]
    video_length_value = (filtered_df['VIDEOLENGTH_ms'].values) / 1000.
    label = (filtered_df['label'].values)[0]
    if verbose:
        print(video_length_value, "seconds")
        print("label:", label)

    #-------
    import meta_tuple
    meta_tuple.main(df_sorted, project_name, label, video_length_value[0])
    
    import meta_range
    meta_range.main(df_sorted, project_name, 'alltests', video_length_value[0])

    import meta_violin
    meta_violin.main(df_sorted, project_name, 'alltests', video_length_value[0])

    import meta_box
    meta_box.main(df_sorted, project_name, 'alltests', video_length_value[0])



    
    exit()

    

if __name__ == "__main__":
    proj_string = gui_enterstring.main("Enter the string that identifies this specific set of experiments.", "String", 
                                  "Experiment name", default_text='Pleyades-public')
    # print(proj_string)
    main(proj_string,
         verbose=True)
    