import pandas as pd
import matplotlib.pyplot as pyplot
import time
# from pathlib import Path
import gui_abstractions.gui_choosefile as gui_choosefile
import os
# import emo_id
# import emo_project
# import emo_dates
# import emo_lastvalue
# import json
import emo_metadata
import emo_substring
import emo_plot


def main(input_filepath='',
         input_path='INPUT/',
         output_path='OUTPUT/',
         metadata_path='METADATA/',
         metadata_filename='metadata',
         add_time_labels = False, 
         verbose=False):

    # If no input_filepath argument is passed, the script will ask the user
    if input_filepath == '':
        filepath_chosen = gui_choosefile.main(['title',       # params_title
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

    # Save 'dataframe_first' and 'dataframe_second' as CSV files in the 'OUTPUT/' folder
    dataframe_first.to_csv(output_path+name_substring+'A.csv', index=False)
    dataframe_second.to_csv(output_path+name_substring+'B.csv', index=False)

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
    #---------------------
    emo_metadata.main(input_filepath,
                      taps_A = taps_A,
                      taps_B = taps_B,
                      json_path=metadata_path,
                      json_filename=metadata_filename,
                      verbose=verbose)
    #----------------------    
    
    exit()

    # print("saved as", output_filepath)
    # print("Rows, columns", sf.shape)



    frame_value = 1
    frames = sf['ms']
    values = sf['value']
    # print(values)
    print("len(frames)",len(frames))
    framerate_rounded = round(len(frames)/ 208)
    print("framerate_rounded",framerate_rounded)

    # Plot_Frames = False
    pyplot.plot(sf)
        
    annot_height = 1.0
    delta_height = annot_height*2/len(frames)
    # print(delta_height)
    if add_time_labels:
        for i in frames:
            # print (i)
            annot_value = i/framerate_rounded
            annot_rounded = round(annot_value, 0)
            # seconds = 52910
            annot_string = time.strftime("%M:%S", time.gmtime(annot_rounded))
            pyplot.annotate(str(annot_string), xy = (i-50,annot_height ))
            annot_height = annot_height-delta_height

    pyplot.axis([0, len(frames), -1.1, 1.1])
    string_ylabel = 'Value range between '+str(frame_value)+' and '+str(frame_value*(-1))
    pyplot.ylabel(string_ylabel)
    string_xlabel = 'frames'
    pyplot.xlabel(string_xlabel)
    pyplot.title('Estimated segments: '+str('?'), fontdict=None, loc='center', pad=None)
    pyplot.yticks([])

    # stem_name = 'Unbennant'
    # print(stem_name)
    pyplot.savefig(output_path+tail_nospaces+'_segments.png')

    print("done!")
 
if __name__ == "__main__":
    main(
        # input_filepath = 'INPUT/emoTouch_Pleyades-public_8211_raw_timeline_data_v1.7.1.csv',
         verbose=True)