from locust import HttpUser, TaskSet, task
from core.locust.common import get_csrf_token
from core.environment.host import get_host_for_locust_testing


class DatasetBehavior(TaskSet):
    """
    Comportamiento de prueba existente para cargar la página de subida de datasets.
    """
    def on_start(self):
        self.dataset()

    @task
    def dataset(self):
        response = self.client.get("/dataset/upload")
        get_csrf_token(response)


class AdditionalDatasetBehavior(TaskSet):
    """
    Nuevas pruebas para descargar todos los datasets, login y logout.
    """
    def on_start(self):
        # Login al inicio de las pruebas
        response = self.client.post("/login", data={"email": "user@example.com", "password": "test1234"})
        if response.status_code != 200:
            response.failure("Login failed!")

    @task
    def download_all_datasets(self):
        """
        Prueba de descarga de todos los datasets.
        """
        with self.client.get("/dataset/download/all", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status code {response.status_code}")

    def on_stop(self):
        """
        Logout al finalizar las pruebas.
        """
        self.client.get("/logout")

class DatasetUser(HttpUser):
    """
    Usuario Locust que ejecuta las tareas de las clases DatasetBehavior, AdditionalDatasetBehavior y
    DatasetFilterBehavior.
    """
    tasks = [DatasetBehavior, AdditionalDatasetBehavior, DatasetFilterBehavior]
    min_wait = 5000
    max_wait = 9000
    host = get_host_for_locust_testing()
