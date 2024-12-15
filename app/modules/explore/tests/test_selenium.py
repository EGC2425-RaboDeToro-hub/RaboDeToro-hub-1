from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class TestPruebaFiltros:
    def setup_method(self, method):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
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

    def test_filter_by_number_of_features(self):
        """
        Probar el filtro por número de características.
        """
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.set_window_size(1854, 1048)

        # Navegar a la sección "Explore"
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".sidebar-item:nth-child(3) .align-middle:nth-child(2)"))
        )
        element.click()

        # Aplicar filtro por número de características
        self.driver.find_element(By.ID, "number_of_features").click()
        self.driver.find_element(By.ID, "number_of_features").send_keys("33")
        self.driver.find_element(By.ID, "clear-filters").click()

    def test_filter_by_number_of_models(self):
        """
        Probar el filtro por número de modelos.
        """
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.set_window_size(1854, 1048)

        # Navegar a la sección "Explore"
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".sidebar-item:nth-child(3) .align-middle:nth-child(2)"))
        )
        element.click()

        # Aplicar filtro por número de modelos
        self.driver.find_element(By.ID, "number_of_models").click()
        self.driver.find_element(By.ID, "number_of_models").send_keys("3")
        self.driver.find_element(By.ID, "clear-filters").click()

    def test_combined_filters(self):
        """
        Probar filtros combinados de características y modelos.
        """
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.set_window_size(1854, 1048)

        # Navegar a la sección "Explore"
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".sidebar-item:nth-child(3) .align-middle:nth-child(2)"))
        )
        element.click()

        # Aplicar filtros combinados
        self.driver.find_element(By.ID, "number_of_features").send_keys("33")
        self.driver.find_element(By.ID, "number_of_models").send_keys("3")
        self.driver.find_element(By.ID, "clear-filters").click()

    def test_no_results_for_invalid_filters(self):
        """
        Probar combinación inválida de filtros que no devuelve resultados.
        """
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.set_window_size(1854, 1048)

        # Navegar a la sección "Explore"
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".sidebar-item:nth-child(3) .align-middle:nth-child(2)"))
        )
        element.click()

        # Aplicar filtros inválidos
        self.driver.find_element(By.ID, "number_of_features").send_keys("999")
        self.driver.find_element(By.ID, "number_of_models").send_keys("999")
        self.driver.find_element(By.ID, "clear-filters").click()
