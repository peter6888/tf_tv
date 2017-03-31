'''
use Selenium to control STB
use AVAnaylizer to launch screen capture
'''
import selenium_helper as sh
import time
v = sh.selenium_helper()
v.init()
seconds_between_onnowguide = 15
seconds_between_fullguide = 20
seconds_pageload = 30
pageup_times = 50
def onnow_full_guide():
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
#onnow_full_guide()
def to_onnow():
    v.sendkey("EXIT")
    time.sleep(seconds_pageload)
    v.sendkey("GUIDE")
    v.take_hdmi_capture("LoadingOnNow",30)
to_onnow()
v.deinit()

