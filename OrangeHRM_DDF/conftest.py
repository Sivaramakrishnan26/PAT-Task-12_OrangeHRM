import pytest
from selenium import webdriver
import os
import time

# Directory where screenshots will be saved in case of test failures
SCREENSHOT_DIR = 'screenshots'


@pytest.fixture(scope="function")
def setup(request):
    driver = webdriver.Chrome()  # Initialize the Chrome WebDriver
    driver.maximize_window()  # Maximize the browser window
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")  # Open the website
    request.cls.driver = driver  # Make the WebDriver instance accessible in the test class
    yield driver  # Yield control back to the test
    driver.quit()  # Close the WebDriver


def pytest_runtest_makereport(item, call):
    # Check if the test function execution has failed
    if call.when == 'call' and call.excinfo is not None:
        # Create the screenshots directory if it does not exist
        if not os.path.exists(SCREENSHOT_DIR):
            os.makedirs(SCREENSHOT_DIR)

        # Attempt to capture a screenshot
        driver = item.funcargs['setup']
        if driver:
            # Generate a timestamp for the screenshot file name
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            screenshot_path = os.path.join(SCREENSHOT_DIR, f"Screenshot-{timestamp}.png")
            driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")
        else:
            print("Driver instance not found.")
