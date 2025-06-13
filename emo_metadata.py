""" All metadata operations, specifically
    storing away the infromation form the different tests.
"""
import json
import os
import emo_id
import emo_project
import emo_dates
import emo_lastvalue
import pandas as pd

def main(input_filepath,
         taps_A=0,
         taps_B=0,
         save_as_csv=True,
         json_path='METADATA/',
         json_filename='metadata',
         valid_annotation='?',
         valid_plotfile='?',
         valid_stats='?',
         session_id=None,
         project_name=None,
         subject_gender=None,
         subject_age=None,
         subject_music=None,
         subject_dance=None,
         verbose=False):
    
    print("mtdt|",session_id, project_name, subject_gender, subject_age, subject_music, subject_dance)

    # Only extract from file if not provided
    if session_id is None:
        session_id = emo_id.main(input_filepath)
    if project_name is None:
        project_name = emo_project.main(input_filepath)
    # if subject_gender is None:
    #     subject_gender = ... # fallback extraction

    if verbose:
        print("taps_A:", taps_A, "taps_B:", taps_B)
        print("session_id:", session_id)
        print("project_name:", project_name)
#----------------------
    project_dates = emo_dates.main(input_filepath)
    if verbose:
        print("project_dates:", project_dates)
    #----------------------
    # subject_gender = emo_lastvalue.main(input_filepath, 
    #                                     tag_string = "category-gender")
    # subject_age = emo_lastvalue.main(input_filepath, 
    #                                     tag_string = 'RANGE-ages')
    # subject_music = emo_lastvalue.main(input_filepath, 
    #                                     tag_string = "LIKERT-music")
    # subject_dance = emo_lastvalue.main(input_filepath, 
    #                                     tag_string = "LIKERT-dance")
    
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
            'taps_B_ms': [],
            'valid_annotation': valid_annotation,
            'valid_plotfile': valid_plotfile,
            'valid_stats': valid_stats
        }
    }

    # Specify the path to the JSON file
    json_filepath = json_path+json_filename+'.json'  

    # Check if the JSON file exists
    if os.path.exists(json_filepath):
        # Read the existing JSON file into a Python dict
        with open(json_filepath, 'r') as json_file:
            try:
                existing_data = json.load(json_file)
                if not isinstance(existing_data, dict):
                    existing_data = {}
            except json.JSONDecodeError:
                existing_data = {}
    else:
        # If the file doesn't exist, create an empty dict
        existing_data = {}

    # Update or add the new record
    existing_data[new_record_key] = new_record_data[new_record_key]

    # Write the updated data back to the JSON file
    with open(json_filepath, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)

    #------------------
    csv_filepath = json_path+json_filename+'.csv'
    if save_as_csv:
        # Convert the dict to a Pandas DataFrame
        df = pd.DataFrame.from_dict(existing_data, orient='index')

        # Save the DataFrame as a CSV file
        df.to_csv(csv_filepath)

        # Optional: Display the DataFrame
        # if verbose:
        #     print(df)
   

if __name__ == "__main__":
    main()