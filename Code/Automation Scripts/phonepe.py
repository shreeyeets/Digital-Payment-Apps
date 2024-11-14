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
    return subprocess.Popen(['appium', '--address', '127.0.0.1', '--port', '4723'])

def stop_appium_server(process):
    process.terminate()

def start_scrcpy():
    return subprocess.Popen(['scrcpy'])


class TestAppium(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.appium_process = start_appium_server()
        time.sleep(5)
        cls.scrcpy_process = start_scrcpy()
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        stop_appium_server(cls.appium_process)

    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, options=AppiumOptions().load_capabilities(capabilities))
        self.driver.implicitly_wait(5)
        self.wait = WebDriverWait(self.driver, 5)

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_Full_UPI_Payment(self) -> None:
        transaction_periods = []

        for i in range(3):  # Run the transaction 10 times
            print(f"Starting transaction {i + 1}")

            # Step 1 to Step 9 as in your original test
            try:
                start_time, end_time = self.perform_transaction()
                transaction_period = end_time - start_time
                transaction_periods.append(transaction_period)
                print(f"Transaction {i + 1} completed successfully.")
            except Exception as e:
                print(f"Error during transaction {i + 1}: {e}")

            # Reopen the app for the next transaction
            self.driver.quit()
            time.sleep(2)  # Small pause to ensure the app is fully closed
            self.driver = webdriver.Remote(appium_server_url, options=AppiumOptions().load_capabilities(capabilities))
            self.driver.implicitly_wait(5)
            self.wait = WebDriverWait(self.driver, 5)

        # Print only the list of transaction periods at the end
        print("Transaction Periods (seconds):", transaction_periods)

    def perform_transaction(self):
        # Step 1: Click on the "To Mobile Number" button
        el1 = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.ImageView[@resource-id="com.phonepe.app:id/image"])[1]')))
        el1.click()

        # Step 2: Click on the contact search bar (input field)
        el2 = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.phonepe.app:id/tv_dynamic_hint"]')))
        el2.click()

        # Step 3: Enter the contact name "Tushman"
        search_input = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@text="Search number or name"]')))
        search_input.send_keys("Tushman")

        # Step 4: Select the contact from the search results
        contact_result = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@text="Tushman"]')))
        contact_result.click()

        # Step 5: Tap on the coordinates (147, 2208) to open the keyboard
        self.driver.tap([(147, 2208)], 50)

        # Step 6: Locate the "Enter amount or chat" text input field
        amount_input = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.phonepe.app:id/etInput"]')))
        amount_input.send_keys("1")

        # Step 7: Locate and click the 'Pay' button
        self.driver.tap([(944, 1343)], 100)
        start_time = time.time()  # Record start time

        # Step 8: Enter UPI PIN
        self.enter_upi_pin()

        # Step 9: Confirm transaction completion
        confirmation_message = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.LinearLayout[@resource-id="com.phonepe.app:id/payment_container"])[2]')))
        end_time = time.time()  # Record end time

        return start_time, end_time

    def enter_upi_pin(self):
        self.driver.tap([(203, 1975)], 50)
        self.driver.tap([(914, 1802)], 50)
        self.driver.tap([(559, 1646)], 50)
        self.driver.tap([(550, 2125)], 50)
        self.driver.tap([(914, 1967)], 50)
        self.driver.tap([(529, 1802)], 50)
        self.driver.tap([(911, 2137)], 50)

if __name__ == '__main__':
    unittest.main()