import gui_abstractions.gui_choosefile as gui_choosefile

filepath = gui_choosefile.main(['Select movie to find out length from', '',(".mov", ".mp4")])
print(filepath)

import pyt_abstractions.media.get_length as get_length

length = get_length.main(filepath)

print(length, "seconds")