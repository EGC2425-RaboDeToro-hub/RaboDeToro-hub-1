import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class TestCommunity:
    def setup_method(self, method):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def login(self):
        self.driver.get("http://localhost:5000/login")
        time.sleep(2)
        self.driver.set_window_size(912, 1011)
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("user1@example.com")
        self.driver.find_element(By.ID, "password").send_keys("1234")
        self.driver.find_element(By.ID, "submit").click()
        time.sleep(2)

    def test_create_community(self):
        self.login()
        self.driver.get("http://localhost:5000/community/create")
        time.sleep(2)
        self.driver.find_element(By.ID, "name").click()
        self.driver.find_element(By.ID, "name").send_keys("Test Community")
        self.driver.find_element(By.ID, "description").click()
        self.driver.find_element(By.ID, "description").send_keys("This is a test community")
        self.driver.find_element(By.ID, "code").click()
        self.driver.find_element(By.ID, "code").send_keys("testcode")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

    def test_join_community(self):
        self.login()
        self.driver.get("http://localhost:5000/community/join")
        time.sleep(2)
        self.driver.find_element(By.ID, "joinCode").click()
        self.driver.find_element(By.ID, "joinCode").send_keys("testcode")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

#   def test_update_community(self):
#       self.login()
#       self.driver.get("http://localhost:5000/community/update/1")  # Replace with a valid community ID
#       time.sleep(2)
#       self.driver.find_element(By.ID, "name").click()
#       self.driver.find_element(By.ID, "name").clear()
#       self.driver.find_element(By.ID, "name").send_keys("Updated Community")
#       self.driver.find_element(By.ID, "description").click()
#       self.driver.find_element(By.ID, "description").clear()
#       self.driver.find_element(By.ID, "description").send_keys("Updated Description")
#       self.driver.find_element(By.ID, "code").click()
#       self.driver.find_element(By.ID, "code").clear()
#       self.driver.find_element(By.ID, "code").send_keys("updatedCode")
#       self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
#       time.sleep(2)

#   def test_delete_community(self):
#       self.login()
#       self.driver.get("http://localhost:5000/community/1")  # Replace with a valid community ID
#       time.sleep(2)
#       self.driver.find_element(By.CSS_SELECTOR, "form[action='/community/delete/1'] button[type='submit']").click()
#        time.sleep(2)
#