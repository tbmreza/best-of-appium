import time
from enum import Enum

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

def android_driver(settings, addr="0.0.0.0", port=4723):
    appium_url = f"http://{addr}:{port}"
    o = UiAutomator2Options()
    return I(appium_url, options=o.load_capabilities(settings))

class Attr(Enum):
    TEXT = "text"
    CONTENT_DESC = "content-desc"

# ??: move with_wait to __init__
class I(webdriver.Remote):
    """Our interface extension of library-provided client [class].

    [class]: https://github.com/appium/python-client/blob/master/appium/webdriver/webdriver.py
    """

    def click(self, id_string):
        with_wait = WebDriverWait(self, 10)
        (with_wait
         .until(expected_conditions.presence_of_element_located((AppiumBy.ID, id_string)))
         .click())

    def click_by_accessibility(self, accessibility_id_string, wait=10):
        with_wait = WebDriverWait(self, wait)
        (with_wait
         .until(expected_conditions.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, accessibility_id_string)))
         .click())

    def click_text(self, text):
        with_wait = WebDriverWait(self, 10)
        (with_wait
         .until(expected_conditions.presence_of_element_located((AppiumBy.XPATH, f"//*[@text='{text}']")))
         .click())

    def click_xpath(self, x):
        with_wait = WebDriverWait(self, 10)
        (with_wait
         .until(expected_conditions.presence_of_element_located((AppiumBy.XPATH, x)))
         .click())

    def click_xpath_or(self, x, els):
        with_wait = WebDriverWait(self, 5)
        try:
            (with_wait
             .until(expected_conditions.presence_of_element_located((AppiumBy.XPATH, x)))
             .click())
        except TimeoutException:
            (with_wait
             .until(expected_conditions.presence_of_element_located((AppiumBy.XPATH, els)))
             .click())

    def fill_placeholder(self, placeholder, string):
        with_wait = WebDriverWait(self, 10)
        (with_wait
         .until(expected_conditions.presence_of_element_located((AppiumBy.XPATH, f"//*[@text='{placeholder}']")))
         .send_keys(string))

    def fill_xpath(self, x, string):
        with_wait = WebDriverWait(self, 10)
        e = with_wait \
            .until(expected_conditions.presence_of_element_located((AppiumBy.XPATH, x)))
        e.click()
        
        time.sleep(2)  # ??: appium wait native keyboard
        e.send_keys(string)

    def assert_displayed(self, string, attr=Attr.TEXT):
        with_wait = WebDriverWait(self, 10)
        assert with_wait \
            .until(expected_conditions.presence_of_element_located((AppiumBy.XPATH, f"//*[@{attr.value}='{string}']"))) \
            .is_displayed()

    def assert_content_displayed(self, string):
        self.assert_displayed(string, Attr.CONTENT_DESC)
