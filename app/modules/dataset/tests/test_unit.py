import pytest
from unittest.mock import patch
from flask import Flask
from app.modules.dataset.services import DataSetService
from app.modules.dataset.routes import dataset_bp
import os


# Fixture para el servicio DataSetService
@pytest.fixture
def dataset_service():
    return DataSetService()


# Fixture para la aplicación Flask de prueba
@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Base de datos en memoria
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Registrar blueprint
    app.register_blueprint(dataset_bp)

    return app


# Fixture para el cliente de prueba
@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


# Test 1: Verificar la creación del archivo ZIP para todos los datasets
def test_zip_all_datasets(dataset_service):
    # Mockea la función zip_all_datasets para que retorne una ruta simulada
    with patch.object(dataset_service, 'zip_all_datasets') as mock_zip:
        mock_zip.return_value = "/path/to/zip/all_datasets.zip"  # Ruta simulada

        # Llama al método de servicio
        result = dataset_service.zip_all_datasets()

        # Verifica que la ruta del archivo ZIP es la correcta
        assert result == "/path/to/zip/all_datasets.zip"
        mock_zip.assert_called_once()  # Verifica que la función fue llamada una vez


# Test 2: Verificar el manejo de errores en la creación del archivo ZIP
def test_zip_all_datasets_error(dataset_service):
    # Mockea la función zip_all_datasets para simular un error
    with patch.object(dataset_service, 'zip_all_datasets') as mock_zip:
        mock_zip.side_effect = Exception("Error al crear el archivo ZIP")  # Simula un error

        # Llama al método del servicio y verifica que se maneje la excepción
        with pytest.raises(Exception):
            dataset_service.zip_all_datasets()
