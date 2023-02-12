import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.firefox.options import Options


@pytest.fixture(autouse=True)
def setup(request):
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_experimental_option("detach", True)
    browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    #browser = webdriver.Chrome('C:\\chromedriver_win32\\chromedriver', chrome_options=options)
    wait = WebDriverWait(browser, 35)
    browser.get("http://jamfast20.local:8080/ords/jamfast/r/jamfast")
    browser.maximize_window()
    request.cls.browser = browser
    request.cls.wait = wait
    yield
    browser.close()


