from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestPruebaFiltros:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_prueba_filtros(self):
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.set_window_size(1854, 1048)

        # Navegar a la sección "Explore" con espera explícita
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".sidebar-item:nth-child(3) .align-middle:nth-child(2)"))
        )
        element.click()

        # Probar el filtro de fechas
        self.driver.find_element(By.ID, "after_date").click()
        self.driver.find_element(By.ID, "after_date").send_keys("2024-10-11")
        self.driver.find_element(By.ID, "before_date").click()
        self.driver.find_element(By.ID, "before_date").send_keys("2024-11-11")
        self.driver.find_element(By.ID, "clear-filters").click()

        # Probar otra serie de fechas
        self.driver.find_element(By.ID, "after_date").click()
        self.driver.find_element(By.ID, "after_date").send_keys("2024-10-22")
        self.driver.find_element(By.ID, "before_date").click()
        self.driver.find_element(By.ID, "before_date").send_keys("2024-10-27")
        self.driver.find_element(By.ID, "clear-filters").click()

        # Probar el filtro de tamaño mínimo y máximo
        self.driver.find_element(By.ID, "min_size").click()
        self.driver.find_element(By.ID, "min_size").send_keys("2")
        self.driver.find_element(By.ID, "clear-filters").click()

        self.driver.find_element(By.ID, "max_size").click()
        self.driver.find_element(By.ID, "max_size").send_keys("2")
        self.driver.find_element(By.ID, "clear-filters").click()

        self.driver.find_element(By.ID, "min_size").click()
        self.driver.find_element(By.ID, "min_size").send_keys("1")
        self.driver.find_element(By.ID, "clear-filters").click()