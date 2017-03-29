'''
use Selenium to control STB
use AVAnaylizer to launch screen capture
'''
import selenium_helper as sh
import time
v = sh.selenium_helper()
v.init()
while True:
    v.sendkey("EXIT")
    time.sleep(60)
    v.sendkey("GUIDE")
    time.sleep(60)
    v.take_hdmi_capture("OnNowGuide")
    v.sendkey("RIGHT")
    time.sleep(60)
    v.take_hdmi_capture("FullGuide")
    for i in range(1,5):
        v.sendkey("CHANNELDOWN")
        time.sleep(60)
        v.take_hdmi_capture("FullGuide")
v.deinit()

