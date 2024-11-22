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
    deviceName='OnePlus 7Pro',
    appPackage='com.mobikwik_new',
    appActivity='com.mobikwik_new.ui.activity.Navigator_MainActivity',
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

    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, options=AppiumOptions().load_capabilities(capabilities))
        self.driver.implicitly_wait(5)  # Set up implicit wait of 5 seconds
        self.wait = WebDriverWait(self.driver, 5)  # Set up explicit wait for up to 5 seconds

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()
        
    def test_Full_UPI_Payment(self) -> None:
        # Step 1: Click on the "UPI Transfers" button
        el1 = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '(//android.widget.FrameLayout[@resource-id="com.mobikwik_new:id/iv_logo"])[1]')))
        el1.click()

        # Step 2: Click on the Enter Name bar (input field)
        el2 = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.view.ViewGroup[@resource-id="com.mobikwik_new:id/cl_root"]')))
        el2.click()

        # Step 3: Enter the contact name "Shreejeet"
        search_input = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.mobikwik_new:id/search_edit_text"]')))
        search_input.send_keys("Shreejeet")

        # Step 4: Select the contact from the search results
        contact_result = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.mobikwik_new:id/contact_name" and @text="Shreejeet"]')))
        contact_result.click()

        # Step 5: Click on "To Bank Account"
        # to_bank_account = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.mobikwik_new:id/title" and @text="To Bank Account"]')))
        # to_bank_account.click()

        # Step 6: Locate the "Rupee 0" text input field
        try:
            amount_input = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.mobikwik_new:id/edit_text"]')))
            amount_input.send_keys("1")  # Enter the amount
        except Exception as e:
            print("Amount input box not found. Error:", str(e))

        # Step 7: Locate and click the 'Confirm Payment' button
        try:
            continue_button = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.mobikwik_new:id/cta"]')))
            continue_button.click()
        except Exception as e:
            print("Error tapping CONTINUE button:", str(e))
            return

        # Step 7: Enter UPI PIN
        time.sleep(10)
        #amount_input = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.mobikwik_new:id/form_item_input"]')))
        #amount_input.send_keys("1 3 0 4 0 1")  # Enter the amount
        self.enter_upi_pin()
        start_time = time.time()
        
        end_time = time.time()
        duration = end_time - start_time

    def enter_upi_pin(self):
        self.driver.tap([(239, 2197)], 50) #1
        self.driver.tap([(1200, 2197)], 50) #3
        self.driver.tap([(698, 2853)], 50) #0
        self.driver.tap([(239, 2375)], 50) #4
        self.driver.tap([(571, 2853)], 50) #0
        self.driver.tap([(239, 2197)], 50) #1
        self.driver.tap([(1203, 2853)], 50) #tick


if __name__ == '__main__':
    unittest.main()
