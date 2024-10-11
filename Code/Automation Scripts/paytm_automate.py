import unittest
import subprocess
import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.options.common import AppiumOptions

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Pixel 7 Pro',
    appPackage='net.one97.paytm',
    appActivity='net.one97.paytm.landingpage.activity.AJRMainActivity',
    language='en',
    locale='US',
    noReset=True,
    fullReset=False,
    forceAppLaunch=True,
)

appium_server_url = 'http://localhost:4723'

def start_appium_server():
    # Start the Appium server using subprocess
    return subprocess.Popen(['appium', '--address', '127.0.0.1', '--port', '4723'])

def stop_appium_server(process):
    # Terminate the Appium server process
    process.terminate()

def start_scrcpy():
    # Start scrcpy using subprocess
    return subprocess.Popen(['scrcpy'])


class TestAppium(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the Appium server when the test suite begins
        cls.appium_process = start_appium_server()
        time.sleep(5)  # Wait for a few seconds to allow the server to start
        cls.scrcpy_process = start_scrcpy()
        time.sleep(2)  # Wait for scrcpy to launch

    @classmethod
    def tearDownClass(cls):
        # Stop the Appium server when the test suite ends
        stop_appium_server(cls.appium_process)
        # cls.scrcpy_process.terminate()

    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, options=AppiumOptions().load_capabilities(capabilities))
        self.driver.implicitly_wait(5)  # Set up implicit wait of 5 seconds
        self.wait = WebDriverWait(self.driver, 5)  # Set up explicit wait for up to 5 seconds

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()
        
    def test_Full_UPI_Payment(self) -> None:
        # Step 1: Click on the "To Mobile or Contact" button
        el1 = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.ImageView[@resource-id="net.one97.paytm:id/groupImageView"])[2]')))
        el1.click()

        # Step 2: Enter the contact name "Tushman"
        search_input = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="net.one97.paytm:id/etSearchView"]')))
        search_input.send_keys("Tushman")

        # Step 3: Select the contact from the search results
        contact_result = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.TextView[@resource-id="net.one97.paytm:id/item_title"])[2]')))
        contact_result.click()

        # Step 4: Click on "Enter amount or message"
        enter_amount = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText')))
        enter_amount.click()
        enter_amount.send_keys("1")  # Enter the amount

        # Step 5: Click on "Pay"
        pay_button = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.view.ViewGroup[@resource-id="net.one97.paytm:id/payButtonContainer"]')))
        pay_button.click()

        # Step 6: Locate and click the 'Tick' button (adjust the identifier if needed)
        try:
            self.driver.tap([(929, 2108)], 100)  # Tap the PAY button using coordinates 967, 2228
        except Exception as e:
            print("Error tapping PAY button:", str(e))
            return
        
        # Step 7: Locate and click the 'Proceed Securely' button (adjust the identifier if needed)
        try:
            self.driver.tap([(561, 2122)], 100)  # Tap the PAY button using coordinates 967, 2228
        except Exception as e:
            print("Error tapping PAY button:", str(e))
            return
        
        # Step 8: Click on the "Pay Securely Rs 1"
        pay_securely = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="net.one97.paytm:id/proceed"]')))
        pay_securely.click()

        # Step 9: Enter UPI PIN
        time.sleep(1)
        self.enter_upi_pin()

    def enter_upi_pin(self):
        # Entering UPI PIN with known coordinates for faster execution
        self.driver.tap([(203, 1975)], 50)  # Replace x1, y1 with actual coordinates for digit '7'
        self.driver.tap([(914, 1802)], 50)  # Coordinates for digit '6'
        self.driver.tap([(559, 1646)], 50)  # Coordinates for digit '2'
        self.driver.tap([(550, 2125)], 50)  # Coordinates for digit '0'
        self.driver.tap([(914, 1967)], 50)  # Coordinates for digit '9'
        self.driver.tap([(529, 1802)], 50)  # Coordinates for digit '5'
        # Tap the tick button
        self.driver.tap([(911, 2137)], 50)  # Replace with actual tick coordinates

if __name__ == '__main__':
    unittest.main()
