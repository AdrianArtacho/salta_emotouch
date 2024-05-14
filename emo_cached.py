""" This script reads the 'cached' info
    stored in the 'cached_info.csv'
    and provides access to it in different ways.
"""

import pandas as pd
import gui.gui_menu as gui_menu

def main(test_value ='choose',          # Use gui_menu to let the user choose
         column_name='VIDEOLENGTH_ms',
         filepath='METADATA/',
         filename='cached_info.csv',
         verbose=False):
    
    # test_value = 'Pleyades-public'
    if verbose:
        print(filepath+filename)

    # Read the CSV file
    df = pd.read_csv(filepath+filename)

    # Now 'df' is a DataFrame containing the data from your CSV file
    if verbose:
        print(df)

    #-------------------
    if test_value == 'choose':
        test_values = df['TEST'].values     # Access all values in the 'TEST' column
        test_value = gui_menu.main(test_values, 
                                   "Which test does the file ?? correspond to?", 
                                   "Which test are we processing?")
    else:
        print("test_value", test_value)
        # Split the string at the dash and take the first part
        extracted_part = '-'.join(test_value.split('_')[1].split('-')[:2])
        print("extracted_part", extracted_part)
        test_value = extracted_part
    # exit()


    # Filter the DataFrame to find rows where TEST matches your specified value
    filtered_df = df[df['TEST'] == test_value]

    # Extract the VIDEOLENGTH_ms values
    video_length_values = filtered_df[column_name].values

    if verbose:
        print("Video length values for TEST =", test_value, "are:", video_length_values)
    
    return video_length_values[0]
    
if __name__ == "__main__":
    # test_value = 'Pleyades-public'
    main(test_value = 'Pleyades-public',
         verbose=False)