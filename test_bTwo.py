import pytest
from Pages.Pos import Pos
from Pages.Station import Station
from Pages.Login import Loginpage
from Pages.OrderQueue import OrderQueue
from Utilities.Utils import Utils
import time
import re
#import softest
#from Utilities.Baseclass import baseclass
#from ddt import ddt, data, unpack
import unittest

@pytest.mark.usefixtures("setup")
class TestCaseTwo(unittest.TestCase):
    log = Utils.custom_logger()

    Customer_Name = "Shagun"
    product = "Acai Primo Bowl"
    size = "Bowl"
    ingredient_one = "Blueberries"
    ingredient_two = "Soymilk"
    ingredient_three = "Honey"
    key = "p"

    @pytest.fixture(autouse=True)
    def class_setup(self):
        self.lp = Pos(self.browser,self.wait)
        self.sp = Station(self.browser,self.wait)
        self.cp = Loginpage(self.browser, self.wait)
        self.oq = OrderQueue(self.browser,self.wait)


    def clickOrderName(self):

        j = 0
        # clicking on order
        while j < 5:
            try:
                self.lp.clickOrdername()
                break

            except:
                self.browser.refresh()
                self.lp.select_order(self.product, self.size, self.Customer_Name)
            j = j + 1
        time.sleep(2)


    def test_AorderCreate(self):
        global qty_one, qty_two, qty_three

        self.cp.Login("pos","pos")
        self.lp.select_order(self.product, self.size, self.Customer_Name)
        self.clickOrderName()
        qty_one = self.lp.getIngredientQty(self.ingredient_one)
        qty_two = self.lp.getIngredientQty(self.ingredient_two)
        qty_three = self.lp.getIngredientQty(self.ingredient_three)

        # select modification ingredient 1
        self.lp.select_Modif(self.ingredient_one, "LIGHT")

        # select modification ingredient 2
        self.lp.select_Modif(self.ingredient_two, "SUB")

        # select modification ingredient 3
        self.lp.select_Modif(self.ingredient_three, "NO")
        self.lp.clickCrossButton()
        self.lp.createOrder()

    def test_BCustomerName(self):
        flag = False
        global Order_Number
        self.cp.Login("order_queue", "qq")
        time.sleep(25)
        card_list = self.oq.GetOrderCardList()
        for card in card_list:

            if self.Customer_Name in card.text:
                flag = True
                print("order name verified")
                self.log.info("order name verified")
        if flag == False:
            raise Exception("order name not in order queue")
        Order_Number = self.oq.GetOrderNumber(self.Customer_Name)

    def test_CStationOneOrderInfo(self):
        #global StartTime
        self.cp.Login("station1", "s1")
        self.sp.scanCode(self.key)
        time.sleep(9)
        #StartTime = self.sp.getStartTime()
        station_Name = self.sp.getStation_Name()
        ProductNameOnScreen  = self.sp.getProductNameOnScreen()
        OrderSizeOnScreen = self.sp.getOrderSizeOnScreen()
        CustomerNameOnScreen = self.sp.getCustomerNameOnScreen()
        orderNo = self.sp.getorderNo()
        JarImage = self.sp.getJarImage()
        assert JarImage.is_displayed() == True
        self.log.info("jar image verified successfully")
        list = re.findall(r'#\d+', orderNo)
        orderNo = "".join(list)
        text = self.sp.getText()
        qty_sub = self.sp.GetQtyOnStation(self.ingredient_two, text)
        time.sleep(3)
        assert station_Name == "LIQUID"
        assert self.product == ProductNameOnScreen
        assert self.size == OrderSizeOnScreen
        assert Order_Number == orderNo
        assert self.Customer_Name == CustomerNameOnScreen

        # asserting whether ingredient chosen earlier and modified to "sub" has correct qty:
        assert int(qty_sub) == int(qty_two)
        self.log.info("quantity verified after SUB operation")
        self.sp.logout()
        self.browser.refresh()

    def test_DStationTwoOrderInfo(self):

        self.cp.Login("station2", "s2")
        self.sp.scanCode(self.key)
        i = 0
        popup = self.sp.getPopup()
        # verifying popup message
        while i < 11:
            try:
                boolean = popup.is_displayed()
                print(boolean)
                assert boolean == True
                self.log.info("Station 2 popup is displayed")
                message_one = self.sp.getMessageOne()
                assert message_one == "Go to"
                message_two = self.sp.getMessageTwo()
                assert message_two == "Fruit - Dip 2"
                self.log.info("station2 popup message verified")
                break
            except:
                time.sleep(1)
            i = i + 1

        time.sleep(8)
        self.sp.logoutTwo()
        self.browser.refresh()

    def test_EStationThreeOrderInfo(self):

        self.cp.Login("station3", "s3")
        self.sp.scanCode(self.key)
        time.sleep(5)
        text_two = self.sp.getText()
        qty_Light = self.sp.GetQtyOnStation(self.ingredient_one, text_two)

        assert int(qty_Light) == int(qty_one/2)
        self.log.info("quantity verified after LIGHT modification")
        self.sp.logout()
        self.browser.refresh()

    def test_FStationFourOrderInfo(self):

        self.cp.Login("station4", "s4")
        self.sp.scanCode(self.key)
        time.sleep(5)
        img = self.sp.getImage()
        boolean = img.is_displayed()

        # verifying image of bowl is present or not
        assert boolean == True
        self.log.info("bowl image is displayed")

        text = self.sp.getText()

        # verifying that ingredient of NO  should not be displayed
        if self.ingredient_three not in text:
           self.log.info("test for NO operation passed")

        else:
           self.log.info("test for NO operation failed")

        self.sp.logout()
        self.browser.refresh()