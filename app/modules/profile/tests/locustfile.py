from app.modules.profile.tests.locustfile import HttpUser, TaskSet, task
from core.locust.common import get_csrf_token  # Suponiendo que tienes una función para manejar CSRF
from core.environment.host import get_host_for_locust_testing  # Suponiendo que esta función obtiene el host

from app.modules.dataset.models import DataSet, Author, DSMetaData
from app import db


class AuthorProjectsBehavior(TaskSet):
    """
    Comportamiento de prueba para verificar que los datasets de un autor se pueden obtener correctamente.
    """
    def on_start(self):
        """
        Se ejecuta antes de que comiencen las pruebas para asegurar que tenemos un autor válido y con datasets.
        """
        self.author = Author.query.first()  # Suponiendo que hay al menos un autor en la base de datos
        assert self.author is not None, "No hay autores disponibles en la base de datos para las pruebas."

        # Asegurarnos de que el autor tiene datasets asociados
        self.datasets = DataSet.query.join(DSMetaData).filter(DSMetaData.authors.any(id=self.author.id)).all()
        assert self.datasets, f"El autor {self.author.id} no tiene datasets asociados."

    @task
    def get_author_datasets(self):
        """
        Realiza la solicitud GET para obtener los datasets de un autor.
        """
        # Verificamos que el autor tiene datasets asociados antes de realizar la prueba
        response = self.client.get(f"/author/{self.author.id}/projects")
        
        if response.status_code == 200:
            # Verificar que los títulos de los datasets están presentes en la respuesta
            for dataset in self.datasets:
                assert dataset.title.encode('utf-8') in response.data, f"El dataset '{dataset.title}' no aparece en la respuesta."

            response.success()
        else:
            response.failure(f"Fallo con el código de estado {response.status_code}")

    def on_stop(self):
        """
        Opcional: Aquí podrías agregar una lógica para cerrar sesión o realizar otras acciones después de las pruebas.
        """
        pass


class DatasetUser(HttpUser):
    """
    Usuario Locust que ejecuta las tareas de la clase AuthorProjectsBehavior.
    """
    tasks = [AuthorProjectsBehavior]
    min_wait = 5000  # Tiempo mínimo de espera entre tareas
    max_wait = 9000  # Tiempo máximo de espera entre tareas
    host = get_host_for_locust_testing()  # Función para obtener el host de pruebas
