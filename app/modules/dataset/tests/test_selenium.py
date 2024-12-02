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
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    def count_datasets(self, host):
        self.driver.get(f"{host}/dataset/list")
        self.wait_for_page_to_load()
        try:
            amount_datasets = len(self.driver.find_elements(By.XPATH, "//table//tbody//tr"))
        except Exception:
            amount_datasets = 0
        return amount_datasets

    # def test_upload_dataset(self):
    #     host = "http://localhost:5000"
        
    #     # Abrir la página de login
    #     self.driver.get(f"{host}/login")
    #     self.wait_for_page_to_load()

    #     # Ingresar credenciales y enviar el formulario
    #     self.driver.find_element(By.NAME, "email").send_keys("user1@example.com")
    #     self.driver.find_element(By.NAME, "password").send_keys("1234", Keys.RETURN)
    #     self.wait_for_page_to_load()

    #     # Contar datasets iniciales
    #     initial_datasets = self.count_datasets(host)

    #     # Abrir la página de subir dataset
    #     self.driver.get(f"{host}/dataset/upload")
    #     self.wait_for_page_to_load()

    #     # Completar el formulario de subida
    #     self.driver.find_element(By.NAME, "title").send_keys("Title")
    #     self.driver.find_element(By.NAME, "desc").send_keys("Description")
    #     self.driver.find_element(By.NAME, "tags").send_keys("tag1,tag2")

    #     # Añadir autores
    #     self.driver.find_element(By.ID, "add_author").send_keys(Keys.RETURN)
    #     self.wait_for_page_to_load()
    #     self.driver.find_element(By.NAME, "authors-0-name").send_keys("Author0")
    #     self.driver.find_element(By.NAME, "authors-0-affiliation").send_keys("Club0")

    #     # Subir archivos UVL
    #     file1_path = os.path.abspath("app/modules/dataset/uvl_examples/file1.uvl")
    #     self.driver.find_element(By.CLASS_NAME, "dz-hidden-input").send_keys(file1_path)
    #     self.wait_for_page_to_load()

    #     # Aceptar términos y enviar
    #     self.driver.find_element(By.ID, "agreeCheckbox").send_keys(Keys.SPACE)
    #     self.driver.find_element(By.ID, "upload_button").send_keys(Keys.RETURN)
    #     self.wait_for_page_to_load()
    #     time.sleep(2)

    #     # Validar resultados
    #     assert self.driver.current_url == f"{host}/dataset/list", "Error al regresar al listado"
    #     final_datasets = self.count_datasets(host)
    #     assert final_datasets == initial_datasets + 1, "El dataset no fue añadido correctamente"

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
