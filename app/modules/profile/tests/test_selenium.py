import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

@pytest.fixture(scope="module")
def driver():
    # Configurar el WebDriver, en este caso usando Chrome
    driver = webdriver.Chrome(executable_path='/path/to/chromedriver')  # Asegúrate de que el path sea correcto
    driver.implicitly_wait(10)  # Esperar hasta 10 segundos por los elementos
    yield driver
    driver.quit()

def test_user_profile_with_datasets(driver):
    """
    Test para verificar que los datasets asociados a un usuario se muestran correctamente en la página de su perfil.
    """

    # 1. Abrir la página de inicio de sesión
    driver.get("http://localhost:5000/login")  # Cambia esta URL a la de tu entorno local o de pruebas

    # 2. Iniciar sesión
    email_field = driver.find_element(By.ID, "email")  # Asegúrate de que el ID sea correcto
    password_field = driver.find_element(By.ID, "password")  # Asegúrate de que el ID sea correcto

    email_field.send_keys("user@example.com")
    password_field.send_keys("test1234")
    password_field.send_keys(Keys.RETURN)  # Enviar el formulario

    # Esperar que la página de perfil se cargue
    time.sleep(2)  # Ajusta el tiempo si es necesario

    # 3. Navegar a la página de perfil
    driver.get("http://localhost:5000/profile/summary")  # Cambia la URL si es necesario

    # 4. Verificar que los datasets asociados al usuario están presentes
    # Comprobar que al menos un dataset está presente en la página
    datasets = driver.find_elements(By.CLASS_NAME, "dataset-item")  # Cambia 'dataset-item' por la clase real que se usa en tu HTML
    assert len(datasets) > 0, "No datasets found in the profile page"

    # 5. Verificar que los títulos de los datasets se muestran
    for dataset in datasets:
        title = dataset.find_element(By.CLASS_NAME, "dataset-title")  # Cambia por la clase real del título del dataset
        assert title.text != "", f"Dataset title is empty for dataset: {dataset}"

    # 6. Cerrar sesión
    logout_button = driver.find_element(By.ID, "logout")  # Cambia el ID de 'logout' si es necesario
    logout_button.click()

    # Esperar que se complete la acción de logout
    time.sleep(2)
