import unittest
import time
import WindowsCommand
import label_dir
import json

from os import mkdir
from os import path
from os import listdir
from os.path import isfile, join

from shutil import copyfile
import random

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import tensorflow as tf

import hdmi_capture

class test_youtube(unittest.TestCase):
    _imageFolder = "D:\\YouTube\\"
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
        """
        D:\ML>python tensorflow-master\tensorflow\examples\image_retraining\retrain.py -
-bottleneck_dir=tf_yt_files\bottlenecks --how_many_training_steps 3 --model_dir=
tf_yt_files\inception --output_graph=tf_yt_files\retrained_graph.pb --output_lab
els=tf_yt_files\retrained_labels.txt --image_dir D:\YouTube\TrainingData
9300 bottleneck files created.
2017-05-12 19:58:14.786494: Step 0: Train accuracy = 55.0%
2017-05-12 19:58:14.786494: Step 0: Cross entropy = 1.330952
2017-05-12 19:58:14.973996: Step 0: Validation accuracy = 35.0% (N=100)
2017-05-12 19:58:15.364629: Step 2: Train accuracy = 100.0%
2017-05-12 19:58:15.364629: Step 2: Cross entropy = 1.049670
2017-05-12 19:58:15.536511: Step 2: Validation accuracy = 100.0% (N=100)
Final test accuracy = 100.0% (N=892)
Converted 2 variables to const ops.
        :return: 
        """
        for i in range(1,10000):
            self.driver = self.verify_launched_try_get_driver(self.stbip)
            save_to_folder = self._imageFolder + "{:04d}".format(i)
            if not path.exists(save_to_folder):
                mkdir(save_to_folder)
            hdmi_capture.take(save_to_folder, 10) # time.sleep(10)
            print(i)

    def test_launch_yt_and_report(self):
        working_folder = self._imageFolder + "Test{:04d}".format(random.randint(1000,10000))
        if not path.exists(working_folder):
            mkdir(working_folder)
        self.driver = self.verify_launched_try_get_driver(self.stbip)
        hdmi_capture.take(working_folder, 10)
        print('capture done')

        sess, softmax_tensor = label_dir.get_session_softmaxtensor()
        imgFiles = [f for f in listdir(working_folder) if isfile(join(working_folder, f))]
        types = []
        keyframes = [] #(typeid, imagepath)

        last_type = -1
        for img in imgFiles:
            image_data = tf.gfile.FastGFile(join(working_folder, img), 'rb').read()
            m_type = label_dir.label_image(sess, softmax_tensor, image_data)
            types.append(m_type)
            if m_type != last_type:
                print('New Type Of Image on {}'.format(img))
                last_type = m_type
                keyframes.append((m_type, img))

        # copy key frames to report folder
        reportFolder = join(working_folder, "report")
        if not path.exists(reportFolder):
            mkdir(reportFolder)

        for _, img in keyframes:
            copyfile(join(working_folder, img), join(reportFolder, img))

        htmlstr = self.GenerateReportPage(keyframes)

        with open(join(reportFolder, 'index.html'), 'w') as html_file:
            html_file.write(htmlstr)

    def test_hdmi_capture_actions(self):
        for i in range(5):
            save_to_folder = self._imageFolder + "position{:02d}".format(i)
            if not path.exists(save_to_folder):
                mkdir(save_to_folder)

        for i in range(200):
            self.driver = self.verify_launched_try_get_driver(self.stbip)
            #save_to_folder = self._imageFolder + "actions{:02d}".format(i)
            #if not path.exists(save_to_folder):
            #    mkdir(save_to_folder)
            logger = hdmi_capture.setup_custom_logger('YouTube:')
            logger.info("sleep for wait YouTube Launch")
            time.sleep(7)
            logger.info("Start capture.")
            #hdmi_capture.take(save_to_folder, 13*(7+5*(1+3*1))+1, waitTillFinish=False)
            for tabs in range(13):
                for _ in range(5):
                    #time.sleep(1)
                    logger.info("Keys.ARROW_DOWN")
                    ActionChains(self.driver).send_keys(Keys.ARROW_DOWN).perform()
                    for i in range(3):
                        time.sleep(1)
                        to_folder = self._imageFolder + "position{:02d}".format(i)
                        hdmi_capture.take(to_folder, seconds=0.015)
                        logger.info("Keys.ARROW_RIGHT")
                        ActionChains(self.driver).send_keys(Keys.ARROW_RIGHT).perform()
                    time.sleep(1)
                    hdmi_capture.take(self._imageFolder + "position{:02d}".format(3))
                time.sleep(1)
                ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                time.sleep(1)
                ActionChains(self.driver).send_keys(Keys.RIGHT).perform()
                time.sleep(5)
            #time.sleep(1)
            #ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            #time.sleep(5)

    def test_classify(self):
        """
        Manully classify images and move to folders
        :return: 
        """
        indexs = [10, 100, 300, 440, 500]
        classNames = ["WhiteScreen", "Logo", "SpinLoading", "TextLoaded", "ImageLoaded"]
        for c in classNames:
            c_folder = "D:\\YouTube\\{}".format(c)
            if not path.exists(c_folder):
                print("{} not exist, create it.".format(c_folder))
                mkdir(c_folder)

        for i in range(100,1000):
            savedFolder = "D:\\YouTube\\{:04d}".format(i)
            if not path.exists(savedFolder):
                continue
            print("Try to copy images from {}".format(savedFolder))
            files = [f for f in listdir(savedFolder) if isfile(join(savedFolder, f))]
            if len(files) < indexs[-1]:
                print("Not able to get file from {}".format(savedFolder))
                continue
            for i, f in enumerate(indexs):
                from_file = join(savedFolder, files[f])
                to_file = join("D:\\YouTube\\{}".format(classNames[i]), files[f])
                print("Copying {} to {}".format(from_file, to_file))
                copyfile(from_file, to_file)

    def test_GenerateReportPage(self):
        keyframes = [(1,"1234.jpg"), (2, "2341.jpg"), (0, "7777.jpg"), (4, "8888.jpg")]
        str = self.GenerateReportPage(keyframes)
        print(str)

     # <editor-fold desc="common private functions">
    def GenerateReportPage(self, Keyframes):
        html = '<html><body><table><tr><td>image</td><td>page name</td><td>took time</td></tr>'
        #pages = ['Loading OnNow', 'OnNow Guide', 'Loading Full Guide', 'Full Guide']
        framerate = 60.0
        for typeId, frame in Keyframes:
            pageName = label_dir.type_order_name[label_dir.type_ord.index(typeId)]
            html += self.append_line(frame, pageName, label_dir.get_frame_number(frame) / framerate)
        html += '</table></body></html>'
        return html

    def append_line(self, imageFile, pagename, tooktime):
        return '<tr><td><image width=\'400\' src=\'{}\'/></td><td>{}</td><td>{:.2f}</td></tr>'.format(
            imageFile, pagename, tooktime)

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
