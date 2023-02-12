import pytest
from Pages.Pos import Pos
from Pages.Station import Station
from Pages.Login import Loginpage
from Pages.OrderQueue import OrderQueue
from Utilities.Utils import Utils
import time
import re
# import softest
# from Utilities.Baseclass import baseclass
# from ddt import ddt, data, unpack
import unittest


@pytest.mark.usefixtures("setup")
class TestCaseFour(unittest.TestCase):
    log = Utils.custom_logger()

    Customer_Name = "Deo"
    product = "Amazing Greens"
    size = "Small"
    ingredient_one = "Lemonade"
    ingredient_two = "Peach Juice"
    key = "i"

    @pytest.fixture(autouse=True)
    def class_setup(self):
        self.lp = Pos(self.browser, self.wait)
        self.sp = Station(self.browser, self.wait)
        self.cp = Loginpage(self.browser, self.wait)
        self.oq = OrderQueue(self.browser, self.wait)
        # self.ut = Utils(self.browser)

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
        global qty_one, qty_two, qty_three, AddCountIng_one
        AddCountIng_one = 0
        self.cp.Login("pos", "pos")
        self.lp.select_order(self.product, self.size, self.Customer_Name)
        self.clickOrderName()
        qty_one = self.lp.getIngredientQty(self.ingredient_one)
        qty_two = self.lp.getIngredientQty(self.ingredient_two)

        # select modification ingredient 1
        self.lp.select_Modif(self.ingredient_one, "LIGHT")

        # select modification ingredient 2
        self.lp.select_Modif(self.ingredient_two, "SUB")
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

        self.cp.Login("station1", "s1")
        self.sp.scanCode(self.key)
        time.sleep(9)
        # StartTime = self.sp.getStartTime()
        station_Name = self.sp.getStation_Name()
        ProductNameOnScreen = self.sp.getProductNameOnScreen()
        OrderSizeOnScreen = self.sp.getOrderSizeOnScreen()
        CustomerNameOnScreen = self.sp.getCustomerNameOnScreen()
        orderNo = self.sp.getorderNo()
        JarImage = self.sp.getJarImage()
        assert JarImage.is_displayed() == True
        list = re.findall(r'#\d+', orderNo)
        orderNo = "".join(list)
        text = self.sp.getText()
        qty_Light = self.sp.GetQtyOnStation(self.ingredient_one, text)
        qty_sub = self.sp.GetQtyOnStation(self.ingredient_two, text)
        time.sleep(3)
        assert station_Name == "LIQUID"
        assert self.product == ProductNameOnScreen
        assert self.size == OrderSizeOnScreen
        assert Order_Number == orderNo
        assert self.Customer_Name == CustomerNameOnScreen

        # asserting whether ingredient chosen earlier and modified to "LIGHT" has correct qty:
        assert int(qty_Light) == int(qty_one / 2)
        self.log.info("qty after Light modification verified successfully on station1")

        # asserting whether ingredient chosen earlier and modified to "SUB" has correct qty:
        assert int(qty_sub) == int(qty_two) + (int(qty_one) - int(qty_one / 2))
        self.log.info("qty after sub modification verified successfully on station1")

        self.sp.logout()
        self.browser.refresh()
        self.cp.Login("station5", "s5")
        self.sp.scanCode(self.key)
        time.sleep(5)
        self.sp.logout()
        self.browser.refresh()

        # logging into station1 again to verify the "jar unavailable popup" after scan out on station 5

        self.cp.Login("station1", "s1")
        self.sp.scanCode(self.key)
        i = 0
        while i < 12:
            try:
                popup = self.sp.getPopupTwo()
                boolean = popup.is_displayed()
                assert boolean == True
                message = self.sp.getWrongMessage()
                self.log.info(message)
                assert message == "Jar unavailable for 30 sec"
                break

            except:
                time.sleep(1)
            i = i + 1





