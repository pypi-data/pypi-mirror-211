import time
from selenium.webdriver.support import expected_conditions


class DriverHelperClass:
    def __init__(self, Driver):
        self.Driver = Driver

    def Wait(self, ms=1000):
        time.sleep(float(ms)/1000)
