from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def initialize_driver():
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--headless")  # Ejecutar en modo sin interfaz gráfica
    options.add_argument("--no-sandbox")  # Requerido en entornos CI/CD
    options.add_argument("--disable-dev-shm-usage")  # Usa /tmp en lugar de /dev/shm
    options.add_argument("--disable-gpu")  # Desactiva el uso de la GPU
    options.add_argument("--window-size=1920,1080")  # Tamaño de ventana para evitar problemas de visualización
    options.add_argument("--disable-extensions")  # Desactiva extensiones para mejorar rendimiento
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def close_driver(driver):
    driver.quit()
