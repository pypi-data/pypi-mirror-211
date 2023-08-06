import selenium
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class BaseElement:
    def __init__(self, DriverHelper, By, Locator, LoggingName = 0 ):
        self.Driver = DriverHelper.Driver 
        self.by = By
        self.locator = Locator
        if LoggingName ==0:
            self.loggingName = Locator
        else:
            self.loggingName = LoggingName
        self.DriverHelper = DriverHelper
    
    def GetElement(self):
        try:
            return self.Driver.find_element(self.by, self.locator)
        except:
            raise Exception(f"Element {self.loggingName} could not be found!!!")
        
    def Click(self):
        try:
            self.GetElement().click()
        except:
            raise Exception(f"Element {self.loggingName} not clickable")
        
    def WaitForElement(self, ms = 10000):
        self.DriverHelper.Wait(500)
        WebDriverWait(self.Driver, float(ms)/1000).until(expected_conditions.presence_of_all_elements_located((self.by, self.locator)))
        return self

class InputBox(BaseElement):
    def __init__(self, Driver, By, Locator, LoggingName):
        super().__init__(Driver, By, Locator, LoggingName)

    def SendKeys(self,keys):
        self.GetElement().send_keys(keys)
