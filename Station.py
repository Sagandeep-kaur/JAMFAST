from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from Base_Driver.Base_Driver import Baseclass
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
from Utilities.Utils import Utils


class Station(Baseclass):
    log = Utils.custom_logger(logLevel=logging.INFO)

    ScanCode =  '//*[@id="P2_SCAN_CODE"]'
    PageBody = '//*[@id="t_PageBody"]'
    LogoutMenu = '//*[@id="headerCont"]/span[3]'
    LogoutMenuTwo = '//*[@id="splashMainCont"]/div[2]/div[2]/span'
    LogoutButton = '//*[@id="logoutBtnSAT"]'
    Timer = '//*[@id="timer"]'
    StationName = '//*[@id="currTermName"]'
    ProductName = '//*[@id="productName"]'
    OrderSize = '//*[@id="orderSizeCont"]'
    CustomerNameOnScreen = '//*[@id="custName"]'
    orderNo = '//*[@id="orderNoCont"]/span'
    JarImage = '//*[@id="jarImg"]'
    popup = '//*[@id="goToTermMsgPopup"]'
    messageOne = '//*[@id="P2_GO_TO_TXT"]'
    messageTwo = '//*[@id = "P2_MESSAGE_1"]'
    imageBowl = '//*[@id="bowlImage"]/img'
    PopupTwo = '//*[@id="wrongTermMsgPopup"]'
    WrongMessage = '//*[@id = "P2_MESSAGE"]'

    def __init__(self, browser, wait):
        super().__init__(browser, wait)

    def scanCode(self,key):
        # scanning order in station1
        self.wait.until(EC.presence_of_element_located((By.XPATH, self.ScanCode))).send_keys(key)
        self.browser.find_element(By.XPATH, self.ScanCode).send_keys(Keys.ENTER)

    def getStartTime(self):
        Starttime = self.browser.find_element(By.XPATH, self.Timer).text
        return Starttime

    def getEndTime(self):

        EndTime = self.browser.find_element(By.XPATH, self.Timer).text
        return EndTime

    def getStation_Name(self):
        station_Name = self.browser.find_element(By.XPATH, self.StationName).text
        return station_Name

    def getProductNameOnScreen(self):
        ProductNameOnScreen = self.browser.find_element(By.XPATH, self.ProductName).text
        return ProductNameOnScreen

    def getOrderSizeOnScreen(self):
        OrderSizeOnScreen = self.browser.find_element(By.XPATH, self.OrderSize).text
        return OrderSizeOnScreen

    def getCustomerNameOnScreen(self):
        CustomerNameOnScreen = self.browser.find_element(By.XPATH, self.CustomerNameOnScreen).text
        return CustomerNameOnScreen

    def getorderNo(self):
        orderNo = self.browser.find_element(By.XPATH, self.orderNo).text
        return orderNo

    def getJarImage(self):

        JarImage = self.browser.find_element(By.XPATH, self.JarImage)
        return JarImage

    def getText(self):
        global Text
        Text = self.browser.find_element(By.XPATH, self.PageBody).text
        #print(Text)
        time.sleep(3)
        text = Text.split("\n")
        return text

    def gettext(self):

        global Text
        Text = self.browser.find_element(By.XPATH, self.PageBody).text
        print(Text)
        return Text

    def GetQtyOnStation(self,ingredient, text):
        global Qty,  Qty_prev, counter
        counter = 0
        for i in range(0, len(text)):
            if ingredient == text[i]:
                Qty = text[i - 1]
                if Qty == "½" and text[i - 2].isnumeric():
                   counter = 1
                   Qty_prev = int(text[i - 2])
        return Qty

    def logout(self):

        self.browser.find_element(By.XPATH, self.LogoutMenu).click()
        time.sleep(4)
        self.browser.find_element(By.XPATH, self.LogoutButton).click()

    def logoutTwo(self):
        self.browser.find_element(By.XPATH, self. LogoutMenuTwo).click()
        time.sleep(4)
        self.browser.find_element(By.XPATH, self.LogoutButton).click()



    def getPopup(self):
        popup = self.browser.find_element(By.XPATH, self.popup)
        return popup

    def getMessageOne(self):
        message_one = self.browser.find_element(By.XPATH,self.messageOne).text
        return message_one

    def getMessageTwo(self):
        message_two = self.browser.find_element(By.XPATH, self.messageTwo).text
        return message_two

    def getImage(self):
        img = self.browser.find_element(By.XPATH, self.imageBowl)
        return img

    def getPopupTwo(self):

        Popup = self.browser.find_element(By.XPATH, self.PopupTwo)
        return Popup

    def getWrongMessage(self):

        message = self.browser.find_element(By.XPATH, self.WrongMessage).text
        return message










