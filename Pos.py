from selenium.webdriver.common.by import By
#from Tests.testCase_One import TestCaseone

from selenium.webdriver.common.keys import Keys
import logging
from Utilities.Utils import Utils
#logging.basicConfig(level = logging.DEBUG, filename= "/home/sagandeep/Documents/Aim_logs.log",filemode="w")
from Base_Driver.Base_Driver import Baseclass
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
import time
class Pos(Baseclass):
      log = Utils.custom_logger(logLevel=logging.INFO)

      ProductSelect = '//*[@id="P12_PRODUCT"]'
      SizeSelect = '//*[@id="P12_SIZE"]'
      IngredientSelect = '//*[@id="P12_ADD_REMOVE"]'
      ModifSelect = '//*[@id="P12_MOD_TYPE"]'
      qtyRows = '//*[@id="143415628672286350_orig"]/tbody/tr'
      ModifAddButton = '//*[@id="B145107395380706807"]'
      CustomerName = '//*[@id="P12_CUSTOMER_NAME"]'
      OrderButton = '//*[@id="createOrderBtn"]'
      CreateOrderButton = '//*[@id="B65102658859193523"]'
      OrderName = '//*[@id="65000878301180902_orig"]/tbody/tr[2]/td[1]/span'
      CrossButton = '//*[@id="wwvFlowForm"]/div[3]/div[1]/button'
      qty = " "

      def __init__(self,browser,wait):
          super().__init__(browser,wait)

      def selectProduct(self, selectText):
          # selecting product
          select_product = Select(self.browser.find_element(By.XPATH, self.ProductSelect))
          select_product.select_by_visible_text(selectText)
          time.sleep(6)

      def selectSize(self, selectText):
          # selecting size
          select_size = Select(self.browser.find_element(By.XPATH, self.SizeSelect))
          select_size.select_by_visible_text(selectText)
          time.sleep(6)

      def clickOrdername(self):

          self.browser.find_element(By.XPATH, self.OrderName).click()


      def select_Modif(self,ingredient, type):

          # adding modification ingredient
          select = Select(self.browser.find_element(By.XPATH, self.IngredientSelect))
          select.select_by_visible_text(ingredient)
          time.sleep(6)
          # selecting modification type
          select = Select(self.browser.find_element(By.XPATH, self.ModifSelect))
          select.select_by_visible_text(type)
          time.sleep(3)
          self.clickaddButton()

      def clickCrossButton(self):
          # clicking cross button
          self.browser.find_element(By.XPATH, self.CrossButton).click()


      def getIngredientQty(self, ingredient):

          global row, ing_name, qty

          rows = self.browser.find_elements(By.XPATH, self.qtyRows)

          for row in rows[1:]:
              ing_name = row.find_element(By.XPATH, 'td[1]').text

              if ingredient == ing_name:
                  qty = row.find_element(By.XPATH, 'td[2]').text
                  qty = int(qty)
                  print(ingredient, qty)
                  break

          return qty

      def clickaddButton(self):

          self.browser.find_element(By.XPATH, self.ModifAddButton).click()
          time.sleep(6)

      def select_order(self, product, size, Customer_Name):

          self.wait.until(EC.presence_of_element_located((By.XPATH, self.CustomerName))).send_keys(Customer_Name)
          self.selectProduct(product)
          self.selectSize(size)
          self.browser.find_element(By.XPATH, self.OrderButton).click()
          time.sleep(3)

      def createOrder(self):

          self.browser.find_element(By.XPATH, self.CreateOrderButton).click()
          time.sleep(3)