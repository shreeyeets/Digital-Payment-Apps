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
    appPackage='com.google.android.apps.nbu.paisa.user',
    appActivity='com.google.nbu.paisa.flutter.gpay.app.MainActivity',
    language='en',
    locale='US',
    noReset=True,
    fullReset=False,
    forceAppLaunch=False,
)

appium_server_url = 'http://localhost:4723'

def start_appium_server():
    # Start the Appium server using subprocess
    return subprocess.Popen(['appium', '--address', '127.0.0.1', '--port', '4723'])

def stop_appium_server(process):
    # Terminate the Appium server process
    process.terminate()

class TestAppium(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the Appium server when the test suite begins
        cls.appium_process = start_appium_server()
        time.sleep(5)  # Wait for a few seconds to allow the server to start

    @classmethod
    def tearDownClass(cls):
        # Stop the Appium server when the test suite ends
        stop_appium_server(cls.appium_process)

    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, options=AppiumOptions().load_capabilities(capabilities))
        self.driver.implicitly_wait(5)  # Set up implicit wait of 5 seconds
        self.wait = WebDriverWait(self.driver, 5)  # Set up explicit wait for up to 5 seconds

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()
        
    def test_Full_UPI_Payment(self) -> None:
        # Step 2: Click on the "Pay by name or phone number" bar (input field)
        # self.driver.tap([(585, 182)], 50)  # Adjust this based on your device if necessary
        time.sleep(1)
        self.driver.tap([(520, 194)], 50)

        # Step 3: Enter the contact name "XYZ"
        enter_contact = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText')))
        enter_contact.send_keys("XYZ")

        # Step 4: Select the contact from the search results
        time.wait(2)
        self.driver.tap([(438, 567)], 100)

        # Step 5: Click on Pay button
        pay_button = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.Button[@content-desc="Pay"]')))
        pay_button.click()

        # Step 6: Locate the "Rupee 0" text input field
        try:
            amount_input = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@text="₹0"]')))
            amount_input.send_keys("1")  # Enter the amount
        except Exception as e:
            print("Amount input box not found. Error:", str(e))

        # Step 7: Locate and click the 'Arrow' button (adjust the identifier if needed)
        try:
            arrow_button = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.Button')))
            arrow_button.click()
        except Exception as e:
            print("Error tapping PAY button:", str(e))
            return
        
        # Step 8: Click on Pay rupee 1
        pay_button = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.Button[@content-desc="Pay ₹1"]')))
        pay_button.click()

        # Step 8: Enter UPI PIN
        self.enter_upi_pin()

    def enter_upi_pin(self):
        # Entering UPI PIN with known coordinates for faster execution
        self.driver.tap([(203, 1975)], 50)  # Replace x1, y1 with actual coordinates for digit 'A'
        self.driver.tap([(914, 1802)], 50)  # Coordinates for digit 'B'
        self.driver.tap([(559, 1646)], 50)  # Coordinates for digit 'C'
        self.driver.tap([(550, 2125)], 50)  # Coordinates for digit 'D'
        self.driver.tap([(914, 1967)], 50)  # Coordinates for digit 'E'
        self.driver.tap([(529, 1802)], 50)  # Coordinates for digit 'F'
        # Tap the tick button
        self.driver.tap([(911, 2137)], 50)  # Replace with actual tick coordinates

if __name__ == '__main__':
    unittest.main()
