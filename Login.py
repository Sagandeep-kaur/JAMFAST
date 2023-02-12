from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from Base_Driver.Base_Driver import Baseclass
from selenium.webdriver.support.wait import WebDriverWait
import time
import logging
from Utilities.Utils import Utils
class Loginpage(Baseclass):

      log = Utils.custom_logger(logLevel=logging.INFO)
      UsernameField = '//*[@id="PU"]'
      PasswordField = '//*[@id="PS"]'
      LoginButton =  '//*[@id="login-btn"]'


      def __init__(self,browser,wait):
          super().__init__(browser,wait)


      def Login(self,Username, Password):
          self.browser.find_element(By.XPATH, self.UsernameField).send_keys(Username)
          self.browser.find_element(By.XPATH, self.PasswordField).send_keys(Password)
          self.browser.find_element(By.XPATH, self.LoginButton).click()















