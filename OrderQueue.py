from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from Base_Driver.Base_Driver import Baseclass
from selenium.webdriver.support.wait import WebDriverWait
import time
import logging
from Utilities.Utils import Utils


class OrderQueue(Baseclass):
    log = Utils.custom_logger(logLevel=logging.INFO)
    CardList = '//*[starts-with(@id, "card")]'
    Order_No = 'div[2]/div[2]'
    BodyText = '//*[@id="main"]/div[2]'

    def __init__(self, browser, wait):
        super().__init__(browser, wait)

    def GetOrderCardList(self):
        global card_list
        card_list = self.browser.find_elements(By.XPATH, self.CardList)
        return card_list

    def GetOrderNumber(self,Customer_Name):
        global Order_Number

        for card in card_list:

            if Customer_Name in card.text:

                print("order name verified")
                Order_Number = card.find_element(By.XPATH, self.Order_No).text
        return Order_Number

    def GetBodyText(self):

        BodyText = self.browser.find_element(By.XPATH, self.BodyText).text
        return BodyText

















