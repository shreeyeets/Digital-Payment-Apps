import unittest
import subprocess
import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.options.common import AppiumOptions

# Appium capabilities for the test
capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Pixel 7 Pro',
    appPackage='com.phonepe.app',
    appActivity='com.phonepe.app.ui.activity.Navigator_MainActivity',
    language='en',
    locale='US',
    noReset=True,
    fullReset=False,
    forceAppLaunch=True,
)

appium_server_url = 'http://localhost:4723'


def start_appium_server():
    """
    Start the Appium server using subprocess.
    """
    return subprocess.Popen(['appium', '--address', '127.0.0.1', '--port', '4723'])


def stop_appium_server(process):
    """
    Terminate the Appium server process.
    """
    process.terminate()


def start_scrcpy():
    """
    Start scrcpy using subprocess.
    """
    return subprocess.Popen(['scrcpy'])


class TestAppium(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Start the Appium server and scrcpy when the test suite begins.
        """
        cls.appium_process = start_appium_server()
        time.sleep(5)  # Wait for a few seconds to allow the server to start
        cls.scrcpy_process = start_scrcpy()
        time.sleep(2)  # Wait for scrcpy to launch

    @classmethod
    def tearDownClass(cls):
        """
        Stop the Appium server and scrcpy when the test suite ends.
        """
        stop_appium_server(cls.appium_process)
        # cls.scrcpy_process.terminate()

    def setUp(self) -> None:
        """
        Set up the Appium WebDriver and WebDriverWait for each test case.
        """
        self.driver = webdriver.Remote(appium_server_url, options=AppiumOptions().load_capabilities(capabilities))
        self.driver.implicitly_wait(5)  # Set up implicit wait of 5 seconds
        self.wait = WebDriverWait(self.driver, 5)  # Set up explicit wait for up to 5 seconds

    def tearDown(self) -> None:
        """
        Quit the WebDriver after each test case.
        """
        if self.driver:
            self.driver.quit()

    def test_full_upi_payment(self) -> None:
        """
        Test case for making a full UPI payment using the PhonePe app.
        """
        # Step 1: Click on the "To Mobile Number" button
        el1 = self.wait.until(EC.presence_of_element_located(
            (AppiumBy.XPATH, '(//android.widget.ImageView[@resource-id="com.phonepe.app:id/image"])[1]')
        ))
        el1.click()

        # Step 2: Click on the contact search bar (input field)
        el2 = self.wait.until(EC.presence_of_element_located(
            (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.phonepe.app:id/tv_dynamic_hint"]')
        ))
        el2.click()

        # Step 3: Enter the contact name "Tushman"
        search_input = self.wait.until(EC.presence_of_element_located(
            (AppiumBy.XPATH, '//android.widget.EditText[@text="Search number or name"]')
        ))
        search_input.send_keys("Tushman")

        # Step 4: Select the contact from the search results
        contact_result = self.wait.until(EC.presence_of_element_located(
            (AppiumBy.XPATH, '//android.widget.TextView[@text="Tushman"]')
        ))
        contact_result.click()

        # Step 5: Tap on the coordinates (147, 2208) to open the keyboard
        self.driver.tap([(147, 2208)], 50)  # Adjust this based on your device if necessary

        # Step 6: Locate the "Enter amount or chat" text input field
        try:
            amount_input = self.wait.until(EC.presence_of_element_located(
                (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.phonepe.app:id/etInput"]')
            ))
            amount_input.send_keys("1")  # Enter the amount
        except Exception as e:
            print("Amount input box not found. Error:", str(e))

        # Step 7: Locate and click the 'Pay' button
        try:
            self.driver.tap([(944, 1343)], 100)  # Tap the PAY button using coordinates
            print("UPI Payment Gateway opened at:", time.strftime('%Y-%m-%d %H:%M:%S'))
        except Exception as e:
            print("Error tapping PAY button:", str(e))
            return

        # Step 8: Enter UPI PIN
        time.sleep(20)
        self.enter_upi_pin()
        start_time = time.time()

        # Step 9: Confirm transaction completion by waiting for the "Payment Successful" message
        try:
            confirmation_message = self.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.LinearLayout[@resource-id="com.phonepe.app:id/payment_container"])[2]')),15)
            print("Confirmation Message received")
            end_time = time.time()
            duration = end_time - start_time
            print("Payment completed at:", time.strftime('%Y-%m-%d %H:%M:%S'))
            print("Time taken between UPI PIN entry and confirmation:", duration, "seconds")
        except Exception as e:
            print("Payment confirmation not found. Error:", str(e))

    def enter_upi_pin(self):
        """
        Method to enter UPI PIN using known coordinates for faster execution.
        """
        self.driver.tap([(203, 1975)], 50)  # Coordinates for digit '7'
        self.driver.tap([(914, 1802)], 50)  # Coordinates for digit '6'
        self.driver.tap([(559, 1646)], 50)  # Coordinates for digit '2'
        self.driver.tap([(550, 2125)], 50)  # Coordinates for digit '0'
        self.driver.tap([(914, 1967)], 50)  # Coordinates for digit '9'
        self.driver.tap([(529, 1802)], 50)  # Coordinates for digit '5'
        self.driver.tap([(911, 2137)], 50)  # Coordinates for tick button


if __name__ == '__main__':
    unittest.main()

