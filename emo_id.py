""" This script extracts the session_id
    from the .csv file
"""
import pandas as pd

def main(input_filepath,
         col_name = 'session_id',
         verbose=False):
    
    if verbose:
        print("session id", input_filepath) 

    df = pd.read_csv(input_filepath, 
                     sep=';', 
                     usecols= [col_name])

    if verbose:
        print(df.head())

    first_instance = df[col_name][0]

    if verbose:
        print("first_line:", first_instance)

    return first_instance



if __name__ == "__main__":
    main()
