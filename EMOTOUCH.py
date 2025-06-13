import pandas as pd
import matplotlib.pyplot as pyplot
import time
# import gui.gui_choosefile as gui_choosefile
import gui.gui_browse_t as gui_browse
import gui.gui_menu_t as gui_menu
import os
import emo_metadata
import emo_substring
import emo_plot
import emo_cached
import emo_stats


def main(input_filepath='',
         input_path='INPUT/',
         output_path='OUTPUT/',
         metadata_path='METADATA/',
         metadata_filename='metadata',
         add_time_labels = False, 
         verbose=False):

    # If no input_filepath argument is passed, the script will ask the user
    if input_filepath == '':
        filepath_chosen = gui_browse.main(['title',       # params_title
                                        input_path,        # params_initbrowser
                                        '.csv'])        # params_extensions
        input_filepath = filepath_chosen
    else:
        input_filepath = input_filepath

    if verbose:
        print('input_filepath:', input_filepath)

    # Extract project_name from input_filepath
    # Remove directory path if present
    filename = os.path.basename(input_filepath)
    # Remove 'emoTouch_' prefix and split at the next underscore
    if filename.startswith('emoTouch_'):
        project_name = filename[len('emoTouch_'):].split('_')[0]
    else:
        project_name = filename.split('_')[0]

    if verbose:
        print('project_name:', project_name)

    df = pd.read_csv(input_filepath, sep=';',     usecols=[
        'x', 'y', 'type', 'created_at_relative', 'object', 'session_id']
        )
    
    # exit()

    if verbose:
        print("Rows, columns", df.shape)
        print(df.head())
        print("number of columns:", len(df.columns))

    # exit()

    # Group by session_id
    for session_id, session_df in df.groupby('session_id'):
        if verbose:
            print(f"\nProcessing session_id: {session_id}")

       # Extract subject_gender
        gender_rows = session_df[
            (session_df['object'] == 'category-gender') &
            (session_df['x'].notnull()) &
            (session_df['x'] != '')
        ]
        subject_gender = gender_rows.iloc[0]['x'] if not gender_rows.empty else 'unknown'

        # Extract subject_age from the last matching row
        age_rows = session_df[
            (session_df['object'] == 'RANGE-ages') &
            (session_df['x'].notnull()) &
            (session_df['x'] != '')
        ]
        subject_age = age_rows.iloc[-1]['x'] if not age_rows.empty else 'unknown'
        
        # Extract subject_music
        music_rows = session_df[
            (session_df['object'] == 'LIKERT-music') &
            (session_df['x'].notnull()) &
            (session_df['x'] != '')
        ]
        subject_music = music_rows.iloc[-1]['x'] if not music_rows.empty else 'unknown'

        # Extract subject_dance
        dance_rows = session_df[
            (session_df['object'] == 'LIKERT-dance') &
            (session_df['x'].notnull()) &
            (session_df['x'] != '')
        ]
        subject_dance = dance_rows.iloc[-1]['x'] if not dance_rows.empty else 'unknown'

        # exit()

        # print(f"Session {session_id}: gender={subject_gender}:, age={subject_age}:, music={subject_music}:, dance={subject_dance}")
        print("session_id:",session_id,
              ":",subject_gender, 
              ":",subject_age, 
              "music:",subject_music, 
              "dance:",subject_dance)

        # print(f"Session {session_id}; subject_gender = {subject_gender}; subject_age = {subject_age}")
        # exit()


        # Create 'dataframe_first' by filtering rows based on specified conditions
        dataframe_first = session_df[(session_df['object'] == 'TAP-button-part6') & (session_df['type'] == 'BUTTONTAP')]
        dataframe_first = dataframe_first[['created_at_relative', 'x']]

        dataframe_second = session_df[(session_df['object'] == 'TAP-button-part8') & (session_df['type'] == 'BUTTONTAP')]
        dataframe_second = dataframe_second[['created_at_relative', 'x']]

        name_substring = emo_substring.main(input_filepath) + f"_session{session_id}"
        if verbose:
            print("name_substring:", name_substring)

        # exit()

        # Add a row for the start (0,0)
        new_row = pd.DataFrame({'created_at_relative': [0], 'x': [0]})
        dataframe_first = pd.concat([new_row, dataframe_first], ignore_index=True)
        dataframe_second = pd.concat([new_row, dataframe_second], ignore_index=True)

        # exit()

        # Establish the length of the video from cache_info.csv
        length_ms = emo_cached.main(test_value=name_substring, verbose=verbose)
        print("The total length of the test is", length_ms, "ms.")

        # Add a last row to each of the dataframes
        dataframe_first.loc[len(dataframe_first)] = [length_ms, '0']
        dataframe_second.loc[len(dataframe_second)] = [length_ms, '0']

        # exit()

        # Save CSVs
        csvname_first = name_substring + 'A.csv'
        dataframe_first.to_csv(output_path + csvname_first, index=False)
        csvname_second = name_substring + 'B.csv'
        dataframe_second.to_csv(output_path + csvname_second, index=False)

        if verbose:
            print("dataframe_first:")
            print(dataframe_first)
            print("\ndataframe_second:")
            print(dataframe_second)

        # exit()

        taps_A = emo_plot.main(dataframe_first,
                               output_path=output_path,
                               name_substring=name_substring + 'A',
                               verbose=verbose)
        # exit()
        taps_B = emo_plot.main(dataframe_second,
                               output_path=output_path,
                               name_substring=name_substring + 'B',
                               verbose=verbose,
                               window_position=(650, 50))
        if verbose:
            print("taps_A:", taps_A, "taps_B:", taps_B)

        # exit()

        options_AB = ('A', 'B', 'none', '?')
        valid_annotation = gui_menu.main(options_AB, "Choose option:", "window_title")
        if verbose:
            print(taps_A)

        valid_plotfile = options_AB[3]          # '?'
        valid_stats = options_AB[3]

        export_entry = False

        if valid_annotation == options_AB[0]:   # 'A'
            valid_plotfile = csvname_first
            valid_stats = emo_stats.main(valid_plotfile, output_path=output_path, verbose=verbose)
            export_entry = True
        elif valid_annotation == options_AB[1]: # 'B'
            valid_plotfile = csvname_second
            valid_stats = emo_stats.main(valid_plotfile, output_path=output_path, verbose=verbose)
            export_entry = True
        elif valid_annotation == options_AB[2]: # 'none'
            valid_plotfile = 'none'
            valid_stats = 'none'
            export_entry = False

        if verbose:
            print("Valid annotation:", valid_annotation, 
                  ", valid plotfile:", valid_plotfile)

        # exit()

        print(session_id, subject_gender, subject_age, subject_music, subject_dance)

        if export_entry==True:
            # Call the main function from emo_metadata.py
            emo_metadata.main(
                input_filepath,
                taps_A=taps_A,
                taps_B=taps_B,
                json_path=metadata_path,
                json_filename=metadata_filename,
                valid_annotation=valid_annotation,
                valid_plotfile=valid_plotfile,
                valid_stats=valid_stats,
                session_id=session_id,
                project_name=project_name, #<-- project_name extracted from input_filepath
                subject_gender=subject_gender,
                subject_age=subject_age,
                subject_music=subject_music,
                subject_dance=subject_dance,
                verbose=verbose
            )
    #----------------------    

 
if __name__ == "__main__":
    main(
        # input_filepath = 'INPUT/emoTouch_Pleyades-public_8211_raw_timeline_data_v1.7.1.csv',
         verbose=False)