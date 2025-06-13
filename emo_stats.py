""" This script reads from a csv the annotation
    and generates different statistical data.
"""

import pandas as pd
import numpy as np
import json

def percent(length, total_length):
    percent_length = (length * 100) / total_length
    return percent_length


def stats(list_lengths,
          total_length,
          label='?',
          verbose=True):

    if not list_lengths:
        if verbose:
            print(f"No data for {label}. Returning N/A for all statistics.")
        return {
            "Average Length": ("N/A", "N/A"),
            "Median Value": ("N/A", "N/A"),
            "Standard Deviation": ("N/A", "N/A"),
            "Minimum Value": ("N/A", "N/A"),
            "Maximum Value": ("N/A", "N/A"),
            "Range": ("N/A", "N/A"),
            "Variance": ("N/A", "N/A"),
            "Percentiles": {
                "25th": "N/A",
                "50th": "N/A",
                "75th": "N/A"
            },
            "Total Sum": "N/A"
        }

    list_in_seconds = [element / 1000 for element in list_lengths]

    #-------Calculate statistics: SEG_
    average_length = np.mean(list_in_seconds)
    median_value = np.median(list_in_seconds)# / 1000.
    standard_deviation = np.std(list_in_seconds)# / 1000.
    minimum_value = np.min(list_in_seconds)# / 1000.
    maximum_value = np.max(list_in_seconds)# / 1000.
    range_value = maximum_value - minimum_value
    variance = np.var(list_in_seconds)# / 1000.
    percentiles = np.percentile(list_in_seconds, [25, 50, 75])
    total_sum = np.sum(list_in_seconds)# / 1000.

    # Print results
    if verbose:
        print("Average Length ("+label+"):", average_length, "sec.")
        print("Median Value ("+label+"):", median_value, "sec.")
        print("Standard Deviation ("+label+"):", standard_deviation, "sec.")
        print("Minimum Value ("+label+"):", minimum_value, "sec.")
        print("Maximum Value ("+label+"):", maximum_value, "sec.")
        print("Range ("+label+"):", range_value, "sec.")
        print("Variance ("+label+"):", variance, "sec.")
        print("Percentiles (25th, 50th, 75th) ("+label+"):", percentiles, "sec.")
        print("Total Sum ("+label+"):", total_sum, "sec.")

    #------- Create a dictionary with the calculated statistical values (SEG_)
    sub_dict = {
        "Average Length": (average_length, percent(average_length, total_length)),
        "Median Value": (median_value, percent(median_value, total_length)),
        "Standard Deviation": (standard_deviation, percent(standard_deviation, total_length)),
        "Minimum Value": (minimum_value, percent(minimum_value, total_length)),
        "Maximum Value": (maximum_value, percent(maximum_value, total_length)),
        "Range": (range_value, percent(range_value, total_length)),
        "Variance": (variance, percent(variance, total_length)),
        "Percentiles": {
            "25th": percentiles[0],
            "50th": percentiles[1],
            "75th": percentiles[2]
        },
        "Total Sum": total_sum
    }

    # Return dictionary
    return sub_dict


###################

def main(csvname,
         output_path='OUTPUT/',
         verbose=False):
    print("Processing", output_path+csvname)

    # Read the CSV file
    df = pd.read_csv(output_path+csvname)

    if verbose:
        print(df)
    
    #-------total_length
    # Get the last value in 'created_at_relative' column
    total_length = df['created_at_relative'].iloc[-1] / 1000.
    print("total_length:",total_length, "seconds")
    
    #-------total_taps
    total_taps = df['x'].sum()
    # print("total_taps:",total_taps)

    #-------TE per minute (not so useful, not a power of 10)
    TEpm = total_taps * 60. / total_length
    print("total_taps:",total_taps, "TEpm:", TEpm, "TEE / minute")

    #-------Remove start/end markers (first/last rows)
    # Remove the first and last rows from the DataFrame
    df_modified = df.iloc[1:-1]
    if verbose:
        print(df_modified)

    #-------EXTRACT lengths of segments/windows
    # Initialize lists
    list_segments = []
    list_windows = []

    # Iterate through DataFrame
    for i in range(1, len(df_modified)):
        current_row = df_modified.iloc[i]
        previous_row = df_modified.iloc[i - 1]

        # Check conditions for list_segments
        if current_row['x'] == 1 and previous_row['x'] == 0:
            list_segments.append(current_row['created_at_relative'] - previous_row['created_at_relative'])

        # Check conditions for list_windows
        if current_row['x'] == 0 and previous_row['x'] == 1:
            list_windows.append(current_row['created_at_relative'] - previous_row['created_at_relative'])

    # Print the results
    if verbose:
        print("list_segments:", list_segments)
        print("list_windows:", list_windows)

    #------- Create the list 'list_ici'
    list_ici = []
    for i in range(len(list_segments)):
        # Calculate the average of the current and next item in list_windows
        window_average = (list_windows[i] + list_windows[i + 1]) / 2 if i + 1 < len(list_windows) else list_windows[i]
        # Add to the corresponding item in list_segments
        list_ici.append(list_segments[i] + window_average)

    # Print the resulting list
    if verbose:
        print("list_ici:", list_ici)

    #------- Create the list 'list_dev' (deviations in length from the previous ICI)
    list_dev = []

    # Calculate differences
    for i in range(1, len(list_ici)):
        difference = abs(list_ici[i] - list_ici[i - 1])
        list_dev.append(difference)
    
    # Print the resulting list
    if verbose:
        print("list_dev:", list_dev)

    #------- Generate dictionaries
    
    seg_dict = stats(list_segments, total_length, label='segments', verbose=verbose)
    # print(seg_dict)
    win_dict = stats(list_windows, total_length, label='windows', verbose=verbose)
    # print(seg_dict)
    ici_dict = stats(list_ici, total_length, label='ici', verbose=verbose)
    # print(seg_dict)
    dev_dict = stats(list_dev, total_length, label='dev', verbose=verbose)
    # print(seg_dict)

    # exit()
    #------- Wrap the existing dictionaries
    statistics_dict = {'seg': seg_dict,
                       'win': win_dict,
                       'ici': ici_dict,
                       'dev': dev_dict}

    # Print the dictionary with indentation for better readability
    if verbose:
        print(json.dumps(statistics_dict, indent=4))

    # Remove '.csv' and add '.json' extension
    json_filename = csvname.rsplit('.', 1)[0] + '.json'

    # Save the dictionary as a JSON file
    with open(output_path+json_filename, 'w') as json_file:
        json.dump(statistics_dict, json_file, indent=4)
    
    return json_filename

if __name__ == "__main__":
    main("emoTouch_Pleyades-public_7424B.csv",
         verbose=True)