"""
    # Copyright © 2022 By Nguyễn Phú Khương
    # ZALO : 0363561629
    # Email : dev.phukhuong0709@hotmail.com
    # Github : npk-0709
"""


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import ctypes

def getWindowPositionTypeStack(num_browsers: int, width_browser: int, height_browser: int, distance: int):
    """distance is distance to windown stack"""
    width_screen, height_screen = ctypes.windll.user32.GetSystemMetrics(
        0), ctypes.windll.user32.GetSystemMetrics(1)
    distance_heigh=5
    x = - distance
    y = 0
    position  = []
    for i in range(num_browsers):
        x +=  distance
        if x+width_browser > width_screen:
            x = 0
            y += height_browser + distance_heigh
        if (height_browser/2) >= (height_screen - (y + distance)):
            y = 0
            x = 0
        position.append({'index': i, 'x': x, 'y': y})
    return position

def LoginFacebookCookie(driver: webdriver.Chrome, cookie, types="mbasic."):
    url = f"http://{types}facebook.com"
    driver.get(url)
    js = """javascript: void(function() {
                    function setCookie(t) {
                        var list = t.split("; ");
                        console.log(list);
                        for (var i = list.length - 1; i >= 0; i--) {
                            var cname = list[i].split("=")[0];
                            var cvalue = list[i].split("=")[1];
                            var d = new Date();
                            d.setTime(d.getTime() + (7 * 24 * 60 * 60 * 1000));
                            var expires = ";domain=.facebook.com;expires=" + d.toUTCString();
                            document.cookie = cname + "=" + cvalue + "; " + expires;
                        }
                    }
                    setCookie("__cookie__");
                    location.href = "__url__";
                })();
        """
    js = js.replace("__cookie__", cookie).replace("__url__", url)
    driver.execute_script(js)
    if "login.php" in driver.current_url:
        return False, "auth"
    elif "checkpoint" in driver.current_url:
        return False, "checkpoint"
    else:
        return True, None


class WebDriver:
    def __init__(self):
        self.__setup()

    def __setup(self):
        self.options = Options()
        self.options.add_experimental_option(
            'excludeSwitches', ['enable-logging'])
        self.options.add_experimental_option(
            "prefs", {"profile.default_content_setting_values.notifications": 2})

    def startDriver(self,position):
        service = Service(executable_path="chromedriver.exe")
        self.driver = webdriver.Chrome(service=service, options=self.options)
        self.driver.set_window_position(position['x'],position['y'])
        self.driver.set_window_size(400, 600)
        return self.driver
