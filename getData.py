'''
use Selenium to control STB
use AVAnaylizer to launch screen capture
'''
import selenium_helper as sh
import time
v = sh.selenium_helper()
v.init()
v.sendkey("EXIT")
time.sleep(60)
v.sendkey("GUIDE")
time.sleep(60)
v.take_screenshot("test_onnow.jpg")
v.sendkey("RIGHT")
v.take_screenshot("test_full_guide.jpg")
v.deinit()

