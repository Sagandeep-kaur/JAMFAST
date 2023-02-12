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
class TestCaseThree(unittest.TestCase):
    log = Utils.custom_logger()

    Customer_Name = "Shagandeepk"
    product = "Acai Primo Bowl"
    size = "Bowl"
    ingredient_one = "Soymilk"
    ingredient_two = "Strawberries"
    key = "q"

    @pytest.fixture(autouse=True)
    def class_setup(self):
        self.lp = Pos(self.browser,self.wait)
        self.sp = Station(self.browser,self.wait)
        self.cp = Loginpage(self.browser, self.wait)
        self.oq = OrderQueue(self.browser,self.wait)
        #self.ut = Utils(self.browser)


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
        global qty_one, qty_two, qty_three,AddCountIng_one
        AddCountIng_one = 0
        self.cp.Login("pos","pos")
        self.lp.select_order(self.product, self.size, self.Customer_Name)
        self.clickOrderName()
        qty_one = self.lp.getIngredientQty(self.ingredient_one)
        qty_two = self.lp.getIngredientQty(self.ingredient_two)

        # select modification ingredient 1
        self.lp.select_Modif(self.ingredient_one, "ADD")
        AddCountIng_one = AddCountIng_one + 1

        self.lp.select_Modif(self.ingredient_one, "ADD")
        AddCountIng_one = AddCountIng_one + 1

        # select modification ingredient 2
        self.lp.select_Modif(self.ingredient_two, "LIGHT")
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
        list = re.findall(r'#\d+', orderNo)
        orderNo = "".join(list)
        text = self.sp.getText()
        time.sleep(3)
        assert station_Name == "LIQUID"
        assert self.product == ProductNameOnScreen
        assert self.size == OrderSizeOnScreen
        assert Order_Number == orderNo
        assert self.Customer_Name == CustomerNameOnScreen

        # asserting whether ingredient chosen earlier and modified to "add" has correct qty:

        self.VerifyADDQtyOnStationOne(self.ingredient_one, text, AddCountIng_one)
        self.sp.logout()
        self.browser.refresh()

    def VerifyADDQtyOnStationOne(self, ingredient, text, AddCountIng_one):
        global qty_one
        LoopCount = 0

        for i in range(0, len(text)):
            if ingredient == text[i]:
                LoopCount = LoopCount + 1
                Qty = text[i - 1]
                if LoopCount == 1:
                    assert int(Qty) == 2 * int(AddCountIng_one)
                else:
                    assert int(Qty) == int(qty_one)


    def test_EStationThreeOrderInfo(self):

        self.cp.Login("station3", "s3")
        self.sp.scanCode(self.key)
        time.sleep(5)
        text_two = self.sp.getText()
        qty_Light = self.GetQtyOnStation(self.ingredient_two, text_two)
        assert qty_Light == "½"
        if counter == 1:
           assert Qty_prev == (qty_two / 2 - 0.5)
        time.sleep(6)
        self.sp.logout()
        self.browser.refresh()

    def GetQtyOnStation(self, ingredient, text):
        global Qty, Qty_prev, counter
        counter = 0
        Search = False
        for i in range(0, len(text)):
            if ingredient == text[i]:
                Search = True
                Qty = text[i - 1]
                if Qty == "½" and text[i - 2].isnumeric():
                   counter = 1
                   Qty_prev = int(text[i - 2])
                   break

        if Search == False:
           raise Exception("ingredient not found on station")

        return Qty

