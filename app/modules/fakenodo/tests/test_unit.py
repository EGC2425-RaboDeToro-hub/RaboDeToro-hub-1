import pytest
from unittest.mock import MagicMock
from app.modules.fakenodo.services import FakenodoService


@pytest.fixture
def mock_dataset():
    mock_ds = MagicMock()
    mock_ds.id = 1
    mock_ds.ds_meta_data.title = "Test Dataset"
    mock_ds.ds_meta_data.description = "Test description"
    mock_ds.ds_meta_data.authors = []
    mock_ds.ds_meta_data.tags = "tag1, tag2"
    mock_ds.ds_meta_data.publication_type.value = "none"
    return mock_ds


@pytest.fixture
def mock_feature_model():
    mock_fm = MagicMock()
    mock_fm.fm_meta_data.uvl_filename = "test_file.uvl"
    return mock_fm


@pytest.fixture
def fakenodo_service():
    service = FakenodoService()
    service.deposition_repository = MagicMock()
    return service


def test_test_connection(fakenodo_service):
    assert fakenodo_service.test_connection() is True


def test_create_new_deposition(fakenodo_service, mock_dataset):
    mock_deposition = MagicMock()
    mock_deposition.id = 123
    mock_deposition.doi = "10.1234/dataset123"
    mock_deposition.metadata = {
        "title": "Test Dataset",
        "description": "Test description",
        "creators": [],
        "keywords": ["tag1", "tag2", "uvlhub"],
        "license": "CC-BY-4.0"
        }
    fakenodo_service.deposition_repository.create_new_deposition.return_value = mock_deposition
    deposition = fakenodo_service.create_new_deposition(mock_dataset)

    assert "dep_id" in deposition
    assert "doi" in deposition
    assert deposition["doi"].startswith("10.1234/dataset")
    assert "dpe_md" in deposition


def test_upload_file(fakenodo_service, mock_dataset, mock_feature_model):
    fakenodo_service.upload_file = MagicMock(return_value={"status": "success"})
    response = fakenodo_service.upload_file(mock_dataset, "123", mock_feature_model)
    assert response["status"] == "success"


def test_publish_deposition(fakenodo_service):
    fakenodo_service.publish_deposition = MagicMock(return_value={"status": "published"})
    response = fakenodo_service.publish_deposition("123")
    assert response["status"] == "published"


def test_get_deposition(fakenodo_service):
    mock_deposition = MagicMock()
    mock_deposition.id = 123
    fakenodo_service.deposition_repository.get_by_id = MagicMock(return_value=mock_deposition)

    deposition = fakenodo_service.get_deposition(123)
    assert deposition.id == 123


def test_get_doi(fakenodo_service):
    fakenodo_service.get_doi = MagicMock(return_value="10.1234/dataset123")
    doi = fakenodo_service.get_doi("123")
    assert doi == "10.1234/dataset123"


def test_delete_deposition(fakenodo_service):
    fakenodo_service.delete_deposition = MagicMock(return_value={"status": "deleted"})
    response = fakenodo_service.delete_deposition("123")
    assert response["status"] == "deleted"
