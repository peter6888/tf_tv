from os import listdir
from os.path import isfile, join
import WindowsCommand

def take_hdmi_capture(in_file="", out_file=""):
    """
    Use command line ffmpeg to take screen capture through the HDMI capture card
    The command line example in debugging machine is C:\CCVerificationEngine\CCATEngine\Tools\ffmpeg\ffmpeg.exe -f decklink -i "Intensity Pro@15" -pix_fmt rgba -f image2 -t 0.03 "d:\\%d.png"
    :param feature: str - the feature name and subfolder name
    :return: 
    """
    take_capture_command = 'C:\\CCVerificationEngine\\CCATEngine\\Tools\\ffmpeg\\ffmpeg.exe -i {} {}'.format(
        in_file, out_file)
    print(take_capture_command)
    cmd = WindowsCommand.Command(take_capture_command)
    cmd.run(timeout=10)
    return take_capture_command

in_folder = '\\mrfiles2.mr.ericsson.se\\userfiles\\eliiper\\ML\\OnNowGuide'
for f in listdir(in_folder):
    if isfile(join(in_folder, f)):
        #print(f)
        outfilename = join(in_folder, 'jpg', '{}.jpg'.format(f.split('.')[0]))
        infile = join(in_folder, f)
        take_hdmi_capture(infile, outfilename)

