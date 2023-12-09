""" Plot the results
"""

import matplotlib.pyplot as plt
import time


def main(df,
         output_path= 'OUTPUT/',
         name_substring = 'test',
        #  output_path_and_name = 'OUTPUT/test',
        #  add_time_labels = False,
         frames_column = 'created_at_relative',
         values_column = 'x',
         pause_secs = 2,
         verbose=False):

    
    # Create a figure and axis for the plot
    fig, ax = plt.subplots()

    # Plot the data with time in seconds on the x-axis
    ax.step(df[frames_column] / 1000, df[values_column], where='post', marker='o', linestyle='-')

    # Set the custom title
    ax.set_title(name_substring)

    # Count the number of lines where 'x' is one
    count_x_one = df[df[values_column] == '1'].shape[0]

    # Display the count as text in the plot
    # ax.text(0.5, 0.3, f'Count of x=1: {count_x_one}', transform=ax.transAxes, fontsize=12, color='red')

    # Set labels for the x and y axes
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('TAP')

    # Invert the y-axis
    # ax.invert_yaxis()

    # Get the position of the x-axis label
    x_label_position = ax.xaxis.get_label().get_position()

    # Display the count as text to the right of the x-axis label
    ax.text(x_label_position[0] + 0.25, x_label_position[1] - 0.11, f'Taps: {count_x_one} times',
        transform=ax.transAxes, fontsize=11, color='black')


    # Save the plot as a PNG file in the 'OUTPUT' folder
    plt.savefig(output_path+name_substring+'.png')

    # Show the plot (optional)
    # if verbose:
    # plt.show()
    

    # Display the plot for 5 seconds
    plt.show(block=False)
    plt.pause(pause_secs)
    
    return count_x_one
    
    
    
    
    
    # exit()      
    # frame_value = 1
    # frames = sf[frames_column]
    # values = sf[values_column]
    # if verbose:
    #     print(values)

    # framerate_rounded = round(len(frames)/ 1000) ##ms

    # if verbose:
    #     print("len(frames)",len(frames))
    #     print("framerate_rounded",framerate_rounded)


    # exit()
    # # Plot_Frames = False
    # plt.plot(sf)
        
    # annot_height = 1.0
    # delta_height = annot_height*2/len(frames)
    # # print(delta_height)
    # if add_time_labels:
    #     for i in frames:
    #         # print (i)
    #         annot_value = i/framerate_rounded
    #         annot_rounded = round(annot_value, 0)
    #         # seconds = 52910
    #         annot_string = time.strftime("%M:%S", time.gmtime(annot_rounded))
    #         plt.annotate(str(annot_string), xy = (i-50,annot_height ))
    #         annot_height = annot_height-delta_height

    # plt.axis([0, len(frames), -1.1, 1.1])
    # string_ylabel = 'Value range between '+str(frame_value)+' and '+str(frame_value*(-1))
    # plt.ylabel(string_ylabel)
    # string_xlabel = 'frames'
    # plt.xlabel(string_xlabel)
    # plt.title('Estimated segments: '+str('?'), fontdict=None, loc='center', pad=None)
    # plt.yticks([])

    # # stem_name = 'Unbennant'
    # # print(stem_name)

    # plt.savefig(output_path+name_substring+'_segments.png')
    # print("Plot saved as", output_path+name_substring+'_segments.png')

    # print("done!")

if __name__ == "__main__":
    main()