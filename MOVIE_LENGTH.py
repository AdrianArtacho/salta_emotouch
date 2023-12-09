import subprocess
import gui_abstractions.gui_browse as gui_browse

# def main(filepath):
#     # filepath = gui_browse.main(params_extensions='.csv')
#     print(filepath)

def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)

    print(float(result.stdout))
    return float(result.stdout)

if __name__ == "__main__":
    get_length('/Users/artacho/Downloads/Pleyades_ensayo.mov')