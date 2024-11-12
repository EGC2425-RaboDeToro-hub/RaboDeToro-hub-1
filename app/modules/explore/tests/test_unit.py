import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from app.modules.explore.services import ExploreService


@pytest.fixture
def explore_service():
    return ExploreService()


def test_filter_by_date_range(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        mock_datasets = [MagicMock(id=1), MagicMock(id=2)]
        mock_filter.return_value = mock_datasets

        after_date = datetime(2023, 1, 1)
        before_date = datetime(2023, 12, 31)
        
        # Llama al método del servicio
        result = explore_service.filter(after_date=after_date, before_date=before_date)

        # Verifica que los resultados y las llamadas sean correctas
        assert result == mock_datasets
        assert len(result) == 2
        mock_filter.assert_called_once_with(
            "", "newest", "any", [], after_date=after_date, before_date=before_date, min_size=None, max_size=None
        )


def test_filter_by_size_range(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        mock_datasets = [MagicMock(id=3), MagicMock(id=4)]
        mock_filter.return_value = mock_datasets

        min_size = 100.0  # Tamaño mínimo en KB
        max_size = 5000.0  # Tamaño máximo en KB
        
        # Llama al método del servicio
        result = explore_service.filter(min_size=min_size, max_size=max_size)

        # Verifica que los resultados y las llamadas sean correctas
        assert result == mock_datasets
        assert len(result) == 2
        mock_filter.assert_called_once_with(
            "", "newest", "any", [], after_date=None, before_date=None, min_size=min_size, max_size=max_size
        )


def test_filter_by_date_and_size_range(explore_service):
    with patch.object(explore_service.repository, 'filter') as mock_filter:
        mock_datasets = [MagicMock(id=5)]
        mock_filter.return_value = mock_datasets

        after_date = datetime(2023, 1, 1)
        before_date = datetime(2023, 12, 31)
        min_size = 200.0
        max_size = 4000.0
        
        # Llama al método del servicio con ambos filtros aplicados
        result = explore_service.filter(after_date=after_date, before_date=before_date, min_size=min_size, 
                                        max_size=max_size)

        # Verifica que los resultados y las llamadas sean correctas
        assert result == mock_datasets
        assert len(result) == 1
        mock_filter.assert_called_once_with(
            "", "newest", "any", [], after_date=after_date, before_date=before_date, min_size=min_size, 
            max_size=max_size
        )
