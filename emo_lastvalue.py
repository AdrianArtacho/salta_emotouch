""" This script extracts the last value in a given column ('x')
    corresponding to a tag string in another column.
"""
import pandas as pd

def main(input_filepath,
         tag_column = 'object',
         tag_string = 'RANGE-ages',
         val_column = 'x',
         verbose=False):

    # df = pd.read_csv(input_filepath, sep='\t', usecols= [tag_column, 'type', 'x', 'y'])
    df = pd.read_csv(input_filepath, sep=';')

    if verbose:
        print(df.head())
        # exit()    

    # Filter rows where 'object' column is equal to 'category-gender'
    filtered_df = df[df[tag_column] == tag_string]

    if verbose:
        print("filtered_df:", filtered_df)

    # exit()
    # Check if there are any rows with 'object' equal to 'category-gender'
    if not filtered_df.empty:
        # Get the 'x' value from the last row of the filtered DataFrame
        x_value_last_row = filtered_df.iloc[-1][val_column]
        return_value = x_value_last_row
        if verbose:
            print("x value of the last row with 'object' equal to 'category-gender':", x_value_last_row)
    else:
        if verbose:
            print("No rows with 'object' equal to 'category-gender' found.")
        return_value = ''

    # exit()

    return return_value



if __name__ == "__main__":
    main()
