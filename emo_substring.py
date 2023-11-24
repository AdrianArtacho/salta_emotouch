""" Simply extracting the gist of the file name
"""

def main(input_filepath,
         verbose=False):
    # print(input_filepath)
    # Split the file path by '/'
    parts = input_filepath.split('/')
    # Get the last part of the split, which is the file name
    file_name = parts[-1]
    # Split the file name using underscores as separators
    name_parts = file_name.split('_')
    # Join the first three parts using underscores to get the desired portion
    result = '_'.join(name_parts[:3])
    if verbose:
        print(result)
    
    return result

if __name__ == "__main__":
    main("INPUT/emoTouch_Pleyades-public_8211_raw_timeline_data_v1.7.1.csv")