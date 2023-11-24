""" All metadata operations...
"""
import json
import os
import emo_id
import emo_project
import emo_dates
import emo_lastvalue
import pandas as pd

def main(input_filepath,
         taps_A = 0,
         taps_B = 0,
         save_as_csv=True,
         json_path = 'METADATA/',
         json_filename = 'metadata',
         verbose=False):

    if verbose:
        print("taps_A:", taps_A, "taps_B:", taps_B)
#----------------------
    session_id = emo_id.main(input_filepath)
    if verbose:
        print("session_id:", session_id)
    #----------------------
    project_name = emo_project.main(input_filepath)
    if verbose:
        print("project_name:", project_name)
    #----------------------
    project_dates = emo_dates.main(input_filepath)
    if verbose:
        print("project_dates:", project_dates)
    #----------------------
    subject_gender = emo_lastvalue.main(input_filepath, 
                                        tag_string = "category-gender")
    subject_age = emo_lastvalue.main(input_filepath, 
                                        tag_string = 'RANGE-ages')
    subject_music = emo_lastvalue.main(input_filepath, 
                                        tag_string = "LIKERT-music")
    subject_dance = emo_lastvalue.main(input_filepath, 
                                        tag_string = "LIKERT-dance")
    
    if verbose:
        print("subject_gender:", subject_gender)
        print("subject_age:", subject_age)
        print("subject_music:", subject_music)
        print("subject_dance:", subject_dance)
    
    #-----------------


    # Define the data for the new record with session_id as the key
    new_record_key = project_name + "_" + str(session_id)
    new_record_data = {
        new_record_key: {
            'session_id': str(session_id),
            'project_name': project_name,
            'project_dates': project_dates,
            'subject_gender': subject_gender,
            'subject_age': subject_age,
            'subject_music': str(subject_music),
            'subject_dance': str(subject_dance),
            'taps_A': str(taps_A),
            'taps_A_ms': [],
            'taps_B': str(taps_B),
            'taps_B_ms': []
        }
    }

    # Specify the path to the JSON file

    json_filepath = json_path+json_filename+'.json'  # Specify the correct path to your JSON file

    # Check if the JSON file exists
    if os.path.exists(json_filepath):
        # Read the existing JSON file into a Python list
        with open(json_filepath, 'r') as json_file:
            existing_data = json.load(json_file)
    else:
        # If the file doesn't exist, create an empty list
        existing_data = []

    # if verbose:
        # print("existing_data:", existing_data)

    # Initialize a flag to track whether the key was found
    key_found = False

    # Iterate through the existing data to check for a record with the same key
    for i, record in enumerate(existing_data):
        if new_record_key in record:
            # Update the existing record with the new data
            existing_data[i][new_record_key] = new_record_data[new_record_key]
            key_found = True
            break

    # If the key was not found, add a new record
    if not key_found:
        existing_data.append(new_record_data)

    # Write the updated data back to the JSON file
    with open(json_filepath, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)

    # exit()
    #------------------
    csv_filepath = json_path+json_filename+'.csv'
    if save_as_csv:
        # Convert the list of dictionaries to a Pandas DataFrame
        df = pd.DataFrame(existing_data)

        # Save the DataFrame as a CSV file
        df.to_csv(csv_filepath, index=False)

        # Optional: Display the DataFrame
        # if verbose:
        #     print(df)
   

if __name__ == "__main__":
    main()