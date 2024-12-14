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
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "default_secret_key")
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///:memory:"  # Base de datos en memoria
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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
    with patch.object(dataset_service, "zip_all_datasets") as mock_zip:
        mock_zip.return_value = "/path/to/zip/all_datasets.zip"  # Ruta simulada

        # Llama al método de servicio
        result = dataset_service.zip_all_datasets()

        # Verifica que la ruta del archivo ZIP es la correcta
        assert result == "/path/to/zip/all_datasets.zip"
        mock_zip.assert_called_once()  # Verifica que la función fue llamada una vez


# Test 2: Verificar el manejo de errores en la creación del archivo ZIP
def test_zip_all_datasets_error(dataset_service):
    # Mockea la función zip_all_datasets para simular un error
    with patch.object(dataset_service, "zip_all_datasets") as mock_zip:
        mock_zip.side_effect = Exception(
            "Error al crear el archivo ZIP"
        )  # Simula un error

        # Llama al método del servicio y verifica que se maneje la excepción
        with pytest.raises(Exception):
            dataset_service.zip_all_datasets()


# Test 3: Filtrar por características mínimas
def test_filter_min_features(dataset_service):
    with patch.object(dataset_service.repository, "filter_datasets") as mock_filter:
        mock_filter.return_value = [
            {"id": 2, "features": 20, "products": 15},
            {"id": 3, "features": 30, "products": 25},
        ]

        result = dataset_service.filter_datasets(min_features=15)
        assert len(result) == 2
        assert set(d["id"] for d in result) == {2, 3}
        mock_filter.assert_called_once_with(
            min_features=15, max_features=None, min_products=None, max_products=None
        )


# Test 4: Filtrar por características máximas
def test_filter_max_features(dataset_service):
    with patch.object(dataset_service.repository, "filter_datasets") as mock_filter:
        mock_filter.return_value = [
            {"id": 1, "features": 10, "products": 5},
            {"id": 4, "features": 5, "products": 3},
        ]

        result = dataset_service.filter_datasets(max_features=10)
        assert len(result) == 2
        assert set(d["id"] for d in result) == {1, 4}
        mock_filter.assert_called_once_with(
            min_features=None, max_features=10, min_products=None, max_products=None
        )


# Test 5: Filtrar por productos mínimos
def test_filter_min_products(dataset_service):
    with patch.object(dataset_service.repository, "filter_datasets") as mock_filter:
        mock_filter.return_value = [
            {"id": 2, "features": 20, "products": 15},
            {"id": 3, "features": 30, "products": 25},
        ]

        result = dataset_service.filter_datasets(min_products=10)
        assert len(result) == 2
        assert set(d["id"] for d in result) == {2, 3}
        mock_filter.assert_called_once_with(
            min_features=None, max_features=None, min_products=10, max_products=None
        )


# Test 6: Filtrar por productos máximos
def test_filter_max_products(dataset_service):
    with patch.object(dataset_service.repository, "filter_datasets") as mock_filter:
        mock_filter.return_value = [
            {"id": 1, "features": 10, "products": 5},
            {"id": 4, "features": 5, "products": 3},
        ]

        result = dataset_service.filter_datasets(max_products=5)
        assert len(result) == 2
        assert set(d["id"] for d in result) == {1, 4}
        mock_filter.assert_called_once_with(
            min_features=None, max_features=None, min_products=None, max_products=5
        )


# Test 7: Combinar filtros
def test_combined_filters(dataset_service):
    with patch.object(dataset_service.repository, "filter_datasets") as mock_filter:
        mock_filter.return_value = [{"id": 1, "features": 10, "products": 5}]

        result = dataset_service.filter_datasets(
            min_features=10, max_features=20, min_products=5, max_products=10
        )
        assert len(result) == 1
        assert result[0]["id"] == 1
        mock_filter.assert_called_once_with(
            min_features=10, max_features=20, min_products=5, max_products=10
        )


# Test 8: Sin filtros aplicados (devuelve todos los datasets)
def test_no_filters(dataset_service):
    with patch.object(dataset_service.repository, "filter_datasets") as mock_filter:
        mock_filter.return_value = [
            {"id": 1, "features": 10, "products": 5},
            {"id": 2, "features": 20, "products": 15},
            {"id": 3, "features": 30, "products": 25},
            {"id": 4, "features": 5, "products": 3},
        ]

        result = dataset_service.filter_datasets()
        assert len(result) == 4
        mock_filter.assert_called_once_with(
            min_features=None, max_features=None, min_products=None, max_products=None
        )


# Test 9: Filtros que no devuelven resultados
def test_no_results(dataset_service):
    with patch.object(dataset_service.repository, "filter_datasets") as mock_filter:
        mock_filter.return_value = []

        result = dataset_service.filter_datasets(min_features=50, max_products=1)
        assert len(result) == 0
        mock_filter.assert_called_once_with(
            min_features=50, max_features=None, min_products=None, max_products=1
        )


# Test 10: Verificar conversión a formato glencoe
def test_convert_to_format_glencoe(dataset_service, tmpdir):
    input_file = tmpdir.join("input.uvl")
    input_file.write("feature_model_content")  # Contenido de prueba

    with patch(
        "flamapy.metamodels.fm_metamodel.transformations.UVLReader.transform"
    ) as mock_transform:
        with patch(
            "flamapy.metamodels.fm_metamodel.transformations.GlencoeWriter.transform"
        ) as mock_writer:
            mock_transform.return_value = "mocked_fm"
            mock_writer.return_value = None  # La función no devuelve nada

            result = dataset_service.convert_to_format(str(input_file), "glencoe")
            assert result is not None  # Verifica que hay un resultado


# Test 11: Verificar conversión a formato dimacs
def test_convert_to_format_dimacs(dataset_service, tmpdir):
    input_file = tmpdir.join("input.uvl")
    input_file.write("feature_model_content")

    with patch(
        "flamapy.metamodels.fm_metamodel.transformations.UVLReader.transform"
    ) as mock_transform:
        with patch(
            "flamapy.metamodels.pysat_metamodel.transformations.FmToPysat.transform"
        ) as mock_pysat:
            with patch(
                "flamapy.metamodels.pysat_metamodel.transformations.DimacsWriter.transform"
            ) as mock_writer:
                mock_transform.return_value = "mocked_fm"
                mock_pysat.return_value = "mocked_sat"
                mock_writer.return_value = None

                result = dataset_service.convert_to_format(str(input_file), "dimacs")
                assert result is not None


# Test 12: Verificar conversión a formato splot
def test_convert_to_format_splot(dataset_service, tmpdir):
    input_file = tmpdir.join("input.uvl")
    input_file.write("feature_model_content")

    with patch(
        "flamapy.metamodels.fm_metamodel.transformations.UVLReader.transform"
    ) as mock_transform:
        with patch(
            "flamapy.metamodels.fm_metamodel.transformations.SPLOTWriter.transform"
        ) as mock_writer:
            mock_transform.return_value = "mocked_fm"
            mock_writer.return_value = None

            result = dataset_service.convert_to_format(str(input_file), "splot")
            assert result is not None


# Test 13: Verificar que con un formato desconocido devuelve none
def test_convert_to_format_unknown_format(dataset_service, tmpdir):
    input_file = tmpdir.join("input.uvl")
    input_file.write("feature_model_content")

    result = dataset_service.convert_to_format(str(input_file), "desconocido")
    assert result is None


# Test 14: Verifica que cuando el formato es uvl, devuelve el contenido del archivo original
def test_convert_to_format_uvl(dataset_service, tmpdir):
    input_file = tmpdir.join("input.uvl")
    input_file.write("original")

    result = dataset_service.convert_to_format(str(input_file), "uvl")
    assert result == "original"
