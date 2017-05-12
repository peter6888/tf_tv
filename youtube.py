import unittest
import time
import WindowsCommand
import json

from selenium import webdriver
from selenium.common import exceptions

import hdmi_capture

class test_youtube(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        return super().__init__(methodName)

    @classmethod
    def setUpClass(cls):
        cls.get_stb_config(cls)
        test_youtube.launchOperaDriver(cls)
        print("----setUpClass----")

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()
        print("----tearDownClass-----")

    def test_launch_yt_and_hdmi_capture(self):
        self.driver = self.verify_launched_try_get_driver(self.stbip)
        hdmi_capture.take("D:\\YouTube", 10) # time.sleep(10)

     # <editor-fold desc="common private functions">
    def playback_video_vid(self, vid):
        """
        :param vid: the YouTube Video ID, such as '9bZkp7q19f0' for PSY - GANGNAM STYLE
        :return: None
        """
        self.driver = self.verify_launched_try_get_driver(self.stbip)
        self.driver.get(
            "https://www.youtube.com/tv/?env_isVideoInfoVisible=1&forced_experiments=9450477&fps=1&env_forceFullAnimation=1#/watch/video/control?v={}".format(vid))
        return self.driver

    def verify_launched_try_get_driver(self, stbip, debugsh=False):
        if not hasattr(self,'driver') or not self.driver:
            enable_debugging_port = 'upload_chmod.xml' if not debugsh else 'upload_chmod_debugsh.xml'
            c1 = WindowsCommand.Command(self.get_companion_automation_command(stbip, enable_debugging_port))
            c1.run(timeout=10)
        return self.launch_youtube_get_driver_common(stbip)

    def launch_youtube_get_driver(self, stbip, launch_youtube='yt.xml'):
        c2 = WindowsCommand.Command(self.get_companion_automation_command(stbip, launch_youtube))
        c2.run(timeout=10)
        return self.get_driver(stbip)

    def launch_youtube_get_driver_common(self, stbip):
        return self.launch_youtube_get_driver(stbip, launch_youtube='yt_plain.xml')

    def exit_to_mr(self, stbip):
        exit2mr = 'exit.xml'
        c = WindowsCommand.Command(self.get_companion_automation_command(stbip, exit2mr))
        c.run(timeout=10)

    def get_driver(self,stbip):
        c = {'chromeOptions': {'debuggerAddress': '{}:9222'.format(stbip)}}
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

    def get_companion_automation_command(self, stbip, command):
        return "CompanionAutomation.exe -ipaddress {} -start -quit {}".format(stbip, command)

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
    # </editor-fold>
