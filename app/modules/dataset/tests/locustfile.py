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


class DatasetFilterBehavior(TaskSet):
    """
    Comportamiento de prueba para filtrar datasets por características y productos.
    No requiere login.
    """
    @task
    def filter_by_features(self):
        """
        Tarea para filtrar datasets por número de características (min_features y max_features).
        Verifica que los datasets cumplen con los filtros establecidos.
        """
        min_features = 5
        max_features = 20
        with self.client.get(f"/api/v1/datasets/filtered?min_features={min_features}&max_features={max_features}",
                             catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                # Verifica que todos los datasets tienen el número de características dentro del rango
                assert all(min_features <= dataset["feature_count"] <= max_features for dataset in data)
                response.success()
            else:
                response.failure(f"Failed with status code {response.status_code}")

    @task
    def filter_by_products(self):
        """
        Tarea para filtrar datasets por número de productos (min_products y max_products).
        Verifica que los datasets cumplen con los filtros establecidos.
        """
        min_products = 30
        max_products = 60
        with self.client.get(f"/api/v1/datasets/filtered?min_products={min_products}&max_products={max_products}",
                             catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                # Verifica que todos los datasets tienen el número de productos dentro del rango
                assert all(min_products <= dataset["product_count"] <= max_products for dataset in data)
                response.success()
            else:
                response.failure(f"Failed with status code {response.status_code}")


class DatasetUser(HttpUser):
    """
    Usuario Locust que ejecuta las tareas de las clases DatasetBehavior, AdditionalDatasetBehavior y
    DatasetFilterBehavior.
    """
    tasks = [DatasetBehavior, AdditionalDatasetBehavior, DatasetFilterBehavior]
    min_wait = 5000
    max_wait = 9000
    host = get_host_for_locust_testing()
