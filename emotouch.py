import pandas as pd
import matplotlib.pyplot as pyplot
import time
# from pathlib import Path
import gui_abstractions.gui_choosefile as gui_choosefile

# VARIABLES-----------------
add_time_labels = False
input_file = "input/emoTouch_Unbenannt_timeline_data_v1.6.1.csv"
#---------------------------

file_chosen = gui_choosefile.main(['title',       # params_title
                                  'input/',        # params_initbrowser
                                  '.csv'])        # params_extensions

input_file = file_chosen
# print('input_file:', input_file)
# quit()

df = pd.read_csv(input_file, sep='\t', usecols= ['x','y', 'type','created_at_relative', 'object'])

print("Rows, columns", df.shape)
# print(df)
print(len(df.columns))

# print(df.iloc[:5])          # head

sf = pd.DataFrame(columns = ['ms', 'value']) ## segment function
# print(df)

tmp = []        # initialize list

for index, row in df.iterrows():
    if row['type'] == 'BUTTONTOGGLE':
        if row['created_at_relative'] >= 0:
            if row['x'] == 1:
                tmp.append({'ms' : row['created_at_relative'], 'value' : int(row['x'])})
            else:
                tmp.append({'ms' : row['created_at_relative'], 'value' : int(-1)})

sf = pd.concat([sf, pd.DataFrame(tmp)], axis=0, ignore_index=True)      # concatenate after loop

output_path = 'output/Unbenannt.csv'

sf.to_csv(output_path, index=False)

print("saved as", output_path)
print("Rows, columns", sf.shape)



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

stem_name = 'Unbennant'
print(stem_name)
pyplot.savefig('output/'+stem_name+'_segments.png')

print("done!")
 
