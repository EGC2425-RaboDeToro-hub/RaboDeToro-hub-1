# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class TestTestselenium():
  def setup_method(self, method):
    # Configuración del navegador
    self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    self.driver.implicitly_wait(10)

  def teardown_method(self, method):
    self.driver.quit()
  
  def test_testselenium(self):
    self.driver.get("http://127.0.0.1:5000/")
    self.driver.set_window_size(1838, 1048)
    self.driver.find_element(By.LINK_TEXT, "Login").click()
    self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(2) > .col-md-6").click()
    self.driver.find_element(By.ID, "email").send_keys("user1@example.com")
    self.driver.find_element(By.ID, "password").send_keys("1234")
    self.driver.find_element(By.ID, "password").click()
    self.driver.find_element(By.ID, "password").send_keys("12345")
    self.driver.find_element(By.ID, "submit").click()
    self.driver.find_element(By.ID, "password").send_keys("1234")
    self.driver.find_element(By.LINK_TEXT, "here").click()
    self.driver.find_element(By.ID, "email").click()
    self.driver.find_element(By.ID, "email").send_keys("user1@example.com")
    self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
    self.driver.find_element(By.ID, "email").send_keys("josemaria1.jmmp@gmail.com")
    self.driver.find_element(By.ID, "password").send_keys("12345")
  