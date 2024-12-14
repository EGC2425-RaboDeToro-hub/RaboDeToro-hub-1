from locust import HttpUser, TaskSet, task, between
from core.environment.host import get_host_for_locust_testing
from core.locust.common import get_csrf_token


class DatasetFilterBehavior(TaskSet):
    """
    Comportamiento para probar los filtros de datasets.
    """
    def on_start(self):
        """
        Login antes de comenzar las pruebas.
        """
        response = self.client.post("/login", data={
            "email": "user@example.com",
            "password": "test1234"
        })
        if response.status_code != 200:
            print(f"Login failed with status code {response.status_code}")

    @task(1)
    def filter_by_features(self):
        """
        Prueba de carga: Filtrar por número de características.
        """
        response = self.client.post("/explore", json={
            "number_of_features": "33"  # Filtro por número de características como string
        })
        if response.status_code == 200:
            print("Filter by features successful.")
        else:
            print(f"Filter by features failed: {response.status_code}")

    @task(2)
    def filter_by_models(self):
        """
        Prueba de carga: Filtrar por número de modelos.
        """
        response = self.client.post("/explore", json={
            "number_of_models": "3"  # Filtro por número de modelos como string
        })
        if response.status_code == 200:
            print("Filter by models successful.")
        else:
            print(f"Filter by models failed: {response.status_code}")

    @task(3)
    def combined_filters(self):
        """
        Prueba de carga: Filtros combinados (número de características y modelos).
        """
        response = self.client.post("/explore", json={
            "number_of_features": "33",
            "number_of_models": "3"
        })
        if response.status_code == 200:
            print("Combined filters successful.")
        else:
            print(f"Combined filters failed: {response.status_code}")

    @task(4)
    def invalid_filters(self):
        """
        Prueba de carga: Filtros inválidos.
        """
        response = self.client.post("/explore", json={
            "number_of_features": "999",  # Valor inexistente
            "number_of_models": "999"  # Valor inexistente
        })
        if response.status_code == 200:
            print("Invalid filters handled correctly.")
        else:
            print(f"Invalid filters failed: {response.status_code}")

    def on_stop(self):
        """
        Logout al finalizar las pruebas.
        """
        self.client.get("/logout")


class DatasetUser(HttpUser):
    """
    Usuario Locust que ejecuta las tareas relacionadas con el filtrado de datasets.
    """
    tasks = [DatasetFilterBehavior]
    wait_time = between(1, 3)  # Tiempo de espera entre tareas (1-3 segundos)
    host = get_host_for_locust_testing()
