import pytest
from unittest.mock import MagicMock
from app.modules.fakenodo.services import FakenodoService


@pytest.fixture
def fakenodo_service():
    service = FakenodoService()
    service.deposition_repository = MagicMock()
    return service


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
