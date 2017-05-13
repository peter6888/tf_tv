import time
import WindowsCommand
import logging
import sys

def take(imagefolder="", seconds=0.03, waitTillFinish=True):
    take_capture_command = 'C:\\CCVerificationEngine\\CCATEngine\\Tools\\ffmpeg\\ffmpeg.exe -f decklink -i "Intensity Pro@15" -pix_fmt rgba -f image2 -t {} "{}\\{}_%04d.jpg"'.format(
        seconds, imagefolder, time.strftime('%d_%m_%Y_%H_%M_%S'))
    print(take_capture_command)
    cmd = WindowsCommand.Command(take_capture_command)
    cmd.run(timeout=10, waitTillFinish=waitTillFinish)
    return take_capture_command

def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler('log.txt', mode='w')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger

