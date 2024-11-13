from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def initialize_driver():
    service = Service('/home/josemorgado/.wdm/drivers/chromedriver/linux64/130.0.6723.69/chromedriver-linux64/chromedriver'
                      )
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def close_driver(driver):
    driver.quit()
