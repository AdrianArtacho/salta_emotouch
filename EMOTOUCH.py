import pandas as pd
import matplotlib.pyplot as pyplot
import time
# import gui.gui_choosefile as gui_choosefile
import gui.gui_browse_t as gui_browse
import gui.gui_menu_t as gui_menu
# import os
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

    # exit()
    # #---------------------
    # emo_metadata.main(input_filepath, 
    #                   json_path=metadata_path,
    #                   json_filename=metadata_filename,
    #                   verbose=False)
    # #----------------------
    
    df = pd.read_csv(input_filepath, sep=';', usecols= ['x','y', 'type','created_at_relative', 'object'])
    
    if verbose:
        print("Rows, columns", df.shape)
        # exit()
        print(df.head())
        print("number of columns:", len(df.columns))
        # exit()

    # Create 'dataframe_first' by filtering rows based on specified conditions
    dataframe_first = df[(df['object'] == 'TAP-button-part6') & (df['type'] == 'BUTTONTAP')]

    # Select only the desired columns 'created_at_relative' and 'x'
    dataframe_first = dataframe_first[['created_at_relative', 'x']]

    # Create 'dataframe_second' with similar conditions
    dataframe_second = df[(df['object'] == 'TAP-button-part8') & (df['type'] == 'BUTTONTAP')]
    dataframe_second = dataframe_second[['created_at_relative', 'x']]

    name_substring = emo_substring.main(input_filepath)
    if verbose:
        print("name_substring:", name_substring)
    # exit()

    #-----------------
    #### Add a row for the start (0,0)

    # Create a new DataFrame for the row to be added
    new_row = pd.DataFrame({'created_at_relative': [0], 'x': [0]})

    # Concatenate the new row with the original DataFrame
    dataframe_first = pd.concat([new_row, dataframe_first], ignore_index=True)
    dataframe_second = pd.concat([new_row, dataframe_second], ignore_index=True)

    #------------------
    # Establish the length of the video from cache_info.csv
    length_ms = emo_cached.main(
        test_value=name_substring
        )
    print("The total length of the test is", length_ms, "ms.")

    # Add a last row to each of the dataframes
    # Method 1: Using loc
    dataframe_first.loc[len(dataframe_first)] = [length_ms, '0']
    dataframe_second.loc[len(dataframe_second)] = [length_ms, '0']
    # exit()
    #-------------------


    #-------------------

    # Save 'dataframe_first' and 'dataframe_second' as CSV files in the 'OUTPUT/' folder
    csvname_first = name_substring+'A.csv'
    dataframe_first.to_csv(output_path+csvname_first, index=False)

    csvname_second = name_substring+'B.csv'
    dataframe_second.to_csv(output_path+csvname_second, index=False)

    # exit()
    # Optional: Display the resulting DataFrames
    if verbose:
        print("dataframe_first:")
        print(dataframe_first)
        print("\ndataframe_second:")
        print(dataframe_second)

    # exit()
    # name_substring
    taps_A = emo_plot.main(dataframe_first,
                           output_path=output_path,
                           name_substring = name_substring+'A',
                           verbose=verbose)
    taps_B = emo_plot.main(dataframe_second,
                           output_path=output_path,
                           name_substring=name_substring+'B',
                           verbose=verbose)
    if verbose:
        print("taps_A:", taps_A, "taps_B:", taps_B)

    # exit()
    #---------------------
    options_AB = ('A', 'B', 'none', '?')

    # Ask the user to manually choose an annotation (or none)
    valid_annotation = gui_menu.main(options_AB, 
                             "info_text", 
                             "window_title")
    #---------------------
    print(taps_A)

    #------------------
    valid_plotfile = options_AB[3]          # '?'
    valid_stats = options_AB[3]

    if valid_annotation == options_AB[0]:   # 'A'
        valid_plotfile = csvname_first
        valid_stats = emo_stats.main(valid_plotfile, output_path=output_path)

    elif valid_annotation == options_AB[1]: # 'B'
        valid_plotfile = csvname_second
        valid_stats = emo_stats.main(valid_plotfile, output_path=output_path)

    elif valid_annotation == options_AB[2]: # 'none'
        valid_plotfile = 'none'
        valid_stats = 'none'

    print("Valid annotation:", valid_annotation, ", valid plotfile:", valid_plotfile)
    # exit()
    #---------------------
    emo_metadata.main(input_filepath,
                      taps_A = taps_A,
                      taps_B = taps_B,
                      json_path=metadata_path,
                      json_filename=metadata_filename,
                      valid_annotation=valid_annotation,
                      valid_plotfile=valid_plotfile,
                      valid_stats=valid_stats,
                      verbose=verbose)
    #----------------------    

 
if __name__ == "__main__":
    main(
        # input_filepath = 'INPUT/emoTouch_Pleyades-public_8211_raw_timeline_data_v1.7.1.csv',
         verbose=True)