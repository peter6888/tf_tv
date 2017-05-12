import time
import WindowsCommand

def take(imagefolder="", seconds=0.03):
    take_capture_command = 'C:\\CCVerificationEngine\\CCATEngine\\Tools\\ffmpeg\\ffmpeg.exe -f decklink -i "Intensity Pro@15" -pix_fmt rgba -f image2 -t {} "{}\\{}_%04d.jpg"'.format(
        seconds, imagefolder, time.strftime('%d_%m_%Y_%H_%M_%S'))
    print(take_capture_command)
    cmd = WindowsCommand.Command(take_capture_command)
    cmd.run(timeout=10)
    return take_capture_command