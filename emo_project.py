""" This script extracts the project name
    from the file name
"""

def main(input_filepath,
         verbose=False):
    
    if verbose:
        print("input_filepath", input_filepath) 

    # Split the string by underscores and get the third element (index 2)
    # This assumes that the string always has at least two underscores
    result = input_filepath.split('_')[1]

    if verbose:
        print("result:", result)
    
    return result


if __name__ == "__main__":
    main()
