from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from core.environment.host import get_host_for_selenium_testing
from core.selenium.common import initialize_driver, close_driver


def test_login_and_check_element():
    driver = initialize_driver()

    try:
        host = get_host_for_selenium_testing()

        # Open the login page
        driver.get(f'{host}/login')

        # Wait for the email and password fields to be present
        wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
        email_field = wait.until(EC.presence_of_element_located((By.NAME, 'email')))
        password_field = wait.until(EC.presence_of_element_located((By.NAME, 'password')))

        # Enter values
        email_field.send_keys('user1@example.com')
        password_field.send_keys('1234')

        # Submit the form
        password_field.send_keys(Keys.RETURN)

        # Wait for the element to appear on the next page
        try:
            wait.until(EC.presence_of_element_located(
                (By.XPATH, "//h1[contains(@class, 'h2 mb-3') and contains(., 'Latest datasets')]")
            ))
            print('Test passed!')
        except TimeoutException:
            raise AssertionError('Test failed! Element not found within the timeout period.')

    finally:
        # Close the browser
        close_driver(driver)


# Call the test function
test_login_and_check_element()
