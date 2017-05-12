'''
use Selenium to control STB
use AVAnaylizer to launch screen capture
'''
import selenium_helper as sh
import time
from os import mkdir
from os import path

seconds_between_onnowguide = 15
seconds_between_fullguide = 20
seconds_pageload = 30
pageup_times = 50
def onnow_full_guide():
    v = sh.selenium_helper()
    v.init()
    while True:
        v.sendkey("EXIT")
        time.sleep(seconds_pageload)
        v.sendkey("GUIDE")
        time.sleep(seconds_pageload)
        v.take_hdmi_capture("OnNowGuide")
        for i in range(1,pageup_times):
            v.sendkey("CHANNELDOWN")
            time.sleep(seconds_between_onnowguide)
            v.take_hdmi_capture("OnNowGuide")
        v.sendkey("RIGHT")
        time.sleep(seconds_pageload)
        v.take_hdmi_capture("FullGuide")
        for i in range(1,pageup_times):
            v.sendkey("CHANNELUP")
            time.sleep(seconds_between_fullguide)
            v.take_hdmi_capture("FullGuide")
    v.deinit()
#onnow_full_guide()
def to_guide(subfolder='ToBePredict'):
    fullpath = path.join(path.dirname(path.realpath(__file__)), subfolder)
    if not path.exists(fullpath):
        mkdir(fullpath)
    print('will store images to ' + fullpath)
    v = sh.selenium_helper()
    v.init()
    v.sendkey("EXIT")
    print("sleep {} seconds for pageload".format(seconds_pageload))
    time.sleep(seconds_pageload)
    v.sendkey("GUIDE")
    #print("sleep 4 seconds")
    #time.sleep(4)
    print("capturing")
    v.take_hdmi_capture(fullpath,24)
    v.sendkey("RIGHT")
    print("capturing")
    v.take_hdmi_capture(fullpath, 30)
    v.deinit()
#to_guide('1')


