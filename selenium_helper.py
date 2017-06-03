import unittest
import time
import WindowsCommand
import json

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class selenium_helper(unittest.TestCase):
    _debugPort = 9999
    driver = None
    def init(self):
        self.get_stb_config()
        self.launchOperaDriver()
        print("----selenium_helper init----")
        self.driver = self.get_driver(self.stbip)
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])

    def deinit(self):
        if self.driver:
            self.driver.quit()

    def sendkey(self, keyname):
        keymap = {"GUIDE":Keys.NUMPAD6, "CHANNELUP": Keys.PAGE_UP, "CHANNELDOWN": Keys.PAGE_DOWN, "BACK": Keys.BACK_SPACE,
                  "UP":Keys.ARROW_UP, "DOWN":Keys.ARROW_DOWN, "LEFT":Keys.ARROW_LEFT, "RIGHT":Keys.ARROW_RIGHT,
                  "OK":Keys.ENTER, "INFO":Keys.HOME, "RECORD":Keys.NUMPAD9, "PAUSEPLAY":Keys.DIVIDE, "STOP":Keys.END,
                  "OPTIONS":Keys.NUMPAD5, "MENU":Keys.NUMPAD7, "SEARCH":Keys.NUMPAD1, "LAST":Keys.NUMPAD2, "APPS":Keys.NUMPAD3, "ONDEMAND":Keys.NUMPAD4,
                  "POWER":Keys.F7, "MUTE":Keys.F8, "REWIND":Keys.NUMPAD0, "FF":Keys.MULTIPLY, "REPLAY":Keys.DECIMAL, "SKIP":Keys.EQUALS,
                  "VOLUMEUP":Keys.ADD, "VOLUMEDOWN":Keys.SUBTRACT}
        if(keyname.upper()=="EXIT"):
            print("Exit to full screen")
            exitScript = "var windowEx = window;         windowEx.mstv.playback.ViewModel.backToLiveTV();"
            self.driver.execute_script(exitScript)
        else:
            print("sending key:{}".format(keyname))
            ActionChains(self.driver).send_keys(keymap[keyname.upper()]).perform()

    def get_driver(self,stbip):
        c = {'chromeOptions': {'debuggerAddress': '{}:{}'.format(stbip, self._debugPort)}}
        self.driver = webdriver.Remote("http://localhost:9515", c)
        return self.driver

    def get_stb_config(self):
        """
        http://stackoverflow.com/questions/19078170/python-how-would-you-save-a-simple-settings-config-file
        :return: nothing
        """
        with open('stbconfig.json', 'r') as f:
            c = json.load(f)
        self.stbip = c['ip']
        print('read config stb ip {}'.format(self.stbip))
        self.clientid = c['clientid']
        print('read config stb ID {}'.format(self.clientid))
        self.server = c['mrserver']
        print('read config Mediaroom Server {}'.format(self.server))
        self.buildbranch = c['buildbranch']
        print('read build branch {}'.format(self.buildbranch))
        self.version = c['version'].strip('\r\n')
        self.driver = None

    def take_hdmi_capture(self, imagefolder="", seconds=0.03):
        """
        Use command line ffmpeg to take screen capture through the HDMI capture card
        The command line example in debugging machine is C:\CCVerificationEngine\CCATEngine\Tools\ffmpeg\ffmpeg.exe -f decklink -i "Intensity Pro@15" -pix_fmt rgba -f image2 -t 0.03 "d:\\%d.png"
        :param feature: str - the feature name and subfolder name
        :return: 
        """
        take_capture_command = 'C:\\CCVerificationEngine\\CCATEngine\\Tools\\ffmpeg\\ffmpeg.exe -f decklink -i "Intensity Pro@15" -pix_fmt rgba -f image2 -t {} "{}\\{}_%04d.jpg"'.format(seconds, imagefolder, time.strftime('%d_%m_%Y_%H_%M_%S'))
        print(take_capture_command)
        cmd = WindowsCommand.Command(take_capture_command)
        cmd.run(timeout=10)
        return take_capture_command


    def take_screenshot(self, filename=None, insubfolder=""):
        """
        Use command line camera tool to capture TV screen
        Currently using https://batchloaf.wordpress.com/commandcam/
        :param filename: str
        """
        import os
        if not filename:
            filename = 'ScreenShot{}.jpg'.format(time.strftime('_%d_%m_%Y_%H_%M_%S'))
        #take_capture_command = 'WebCamImageSave.exe /capture /filename {} /ImageQuality 100'.format(filename)
        subfolder_name = '{}_{}'.format(time.strftime('%d_%m_%Y'), self.version)
        path = os.path.join(os.getcwd(), subfolder_name if not insubfolder else insubfolder)
        if not os.path.exists(path):
            os.mkdir(path)
        take_capture_command = 'CommandCam.exe /quiet /filename {}'.format(os.path.join(path, filename))
        print(take_capture_command)
        cmd = WindowsCommand.Command(take_capture_command)
        cmd.run(timeout=10)

    def take_screenshot_until_resolution(self, driver, expectedRes, filename, counter = 60):
        infopanel = None
        while not infopanel:
            try:
                infopanel = driver.find_element_by_class_name("html5-video-info-panel-content")
                print('Got info panel.')
            except exceptions.NoSuchElementException:
                counter -= 1
                print('Waiting info panel shows.')
                time.sleep(7)

        while counter:
            resolution = infopanel.find_elements_by_xpath('.//span')[2].get_attribute('innerHTML')
            if resolution==expectedRes:
                break
            print('current resolution:{}, expecting:{}'.format(resolution, expectedRes))
            time.sleep(7)
            counter -= 1
        self.take_screenshot(filename)

    def launchOperaDriver(self):
        cmd = WindowsCommand.Command("operadriver.exe")
        print(cmd.isRuning())
        if(not cmd.isRuning()):
            cmd.start()

    def execute_10minutes_command(self, command):
        print(command)
        cmd = WindowsCommand.Command(command)
        ret = cmd.run(timeout=10)
        time.sleep(60*10)
        return ret
