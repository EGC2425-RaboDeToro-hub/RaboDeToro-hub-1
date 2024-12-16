import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class TestDatasets:
    def setup_method(self, method):
        # Configuración del navegador
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)

    def teardown_method(self, method):
        # Cierra el navegador después del test
        self.driver.quit()

    def wait_for_page_to_load(self, timeout=4):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState")
            == "complete"
        )

    def count_datasets(self, host):
        self.driver.get(f"{host}/dataset/list")
        self.wait_for_page_to_load()
        try:
            amount_datasets = len(
                self.driver.find_elements(By.XPATH, "//table//tbody//tr")
            )
        except Exception:
            amount_datasets = 0
        return amount_datasets

    def test_download_all_datasets(self):
        host = "http://localhost:5000"

        # Abrir la página de login
        self.driver.get(f"{host}/login")
        self.driver.find_element(By.NAME, "email").send_keys("user1@example.com")
        self.driver.find_element(By.NAME, "password").send_keys("1234", Keys.RETURN)
        self.wait_for_page_to_load()

        # Navegar a la página de descarga de todos los datasets
        self.driver.get(f"{host}/dataset/download/all")
        self.wait_for_page_to_load()

        # Asegurarse de que el botón es clickeable
        download_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/dataset/download/all']"))
        )

        # Intentar hacer clic
        try:
            download_button.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", download_button)

        # Esperar la descarga
        time.sleep(5)
