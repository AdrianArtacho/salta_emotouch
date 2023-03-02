import pandas as pd

input_file = "input/emoTouch_Unbenannt_timeline_data_v1.6.1.csv"

df = pd.read_csv(input_file, sep='\t', usecols= ['x','y', 'type','created_at_relative', 'object'])

print("Rows, columns", df.shape)
# print(df)
print(len(df.columns))

# print(df.iloc[0])
print(df.iloc[:5])
# print(df.head(1))

sf = pd.DataFrame(columns = ['ms', 'value']) ## segment function
# print(df)

tmp = []        # initialize list

for index, row in df.iterrows():
    if row['type'] == 'BUTTONTOGGLE':
        if row['created_at_relative'] >= 0:
            tmp.append({'ms' : row['created_at_relative'], 'value' : int(row['x'])})

sf = pd.concat([sf, pd.DataFrame(tmp)], axis=0, ignore_index=True)      # concatenate after loop

output_path = 'output/Unbenannt.csv'

sf.to_csv(output_path, index=False)

print("saved as", output_path)
print("Rows, columns", sf.shape)
