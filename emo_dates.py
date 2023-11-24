""" This script extracts the dates (and times)
    at which the session started and finalised.
"""
import pandas as pd

def main(input_filepath,
         col_name = 'created_at',
         verbose=False):

    df = pd.read_csv(input_filepath, sep=';', usecols= [col_name])

    if verbose:
        print(df.head())

    # Get the value of the first row
    first_row_value = df.iloc[0]['created_at']
    
    # Get the value of the last row
    last_row_value = df.iloc[-1]['created_at']

    if verbose:
        print("Value of the first row:", first_row_value)
        print("Value of the last row:", last_row_value)

    return (first_row_value, last_row_value)


if __name__ == "__main__":
    main()
