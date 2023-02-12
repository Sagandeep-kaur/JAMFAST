from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import re
import time
class Baseclass:
    def __init__(self,browser,wait):
         self.browser= browser
         self.wait = wait


    def page_scroll(self):
        SCROLL_PAUSE_TIME = 3
        last_height = self.browser.execute_script("return document.body.scrollHeight")

        while True:

            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


    def wait_for_presence_of_all_elements(self,locator_type,locator):
         #wait = WebDriverWait(self.browser, 10)
         list_of_elements = self.wait.until(EC.presence_of_all_elements_located((locator_type,locator)))
         return list_of_elements

    def wait_until_element_is_clickable(self,locator_type,locator):
         #wait = WebDriverWait(self.browser, 10)
         element = self.wait.until(EC.element_to_be_clickable((locator_type,locator)))
         return element

    def getintegerwordfromstring(self, string_text):

        global elem
        list_one = re.findall("\d+", string_text)
        # print(list)
        for i in list_one:
            elem = int(i)
        return elem


