import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from app.modules.explore.services import ExploreService


@pytest.fixture
def explore_service():
    return ExploreService()


def test_filter_by_date_range(explore_service):
    with patch.object(explore_service.repository, "filter") as mock_filter:
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
            "",
            "newest",
            "any",
            [],
            after_date=after_date,
            before_date=before_date,
            min_size=None,
            max_size=None,
            number_of_features="",
            number_of_models="",
        )


def test_filter_by_size_range(explore_service):
    with patch.object(explore_service.repository, "filter") as mock_filter:
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
            "",
            "newest",
            "any",
            [],
            after_date=None,
            before_date=None,
            min_size=min_size,
            max_size=max_size,
            number_of_features="",
            number_of_models="",
        )


def test_filter_by_date_and_size_range(explore_service):
    with patch.object(explore_service.repository, "filter") as mock_filter:
        mock_datasets = [MagicMock(id=5)]
        mock_filter.return_value = mock_datasets

        after_date = datetime(2023, 1, 1)
        before_date = datetime(2023, 12, 31)
        min_size = 200.0
        max_size = 4000.0

        # Llama al método del servicio con ambos filtros aplicados
        result = explore_service.filter(
            after_date=after_date,
            before_date=before_date,
            min_size=min_size,
            max_size=max_size,
        )

        # Verifica que los resultados y las llamadas sean correctas
        assert result == mock_datasets
        assert len(result) == 1
        mock_filter.assert_called_once_with(
            "",
            "newest",
            "any",
            [],
            after_date=after_date,
            before_date=before_date,
            min_size=min_size,
            max_size=max_size,
            number_of_features="",
            number_of_models="",
        )


# Test 4: Filtro por número exacto de características
# Este test valida que el filtro por número de características devuelva únicamente los datasets correspondientes.
def test_filter_by_exact_number_of_features(explore_service):
    with patch.object(explore_service.repository, "filter") as mock_filter:
        mock_datasets = [MagicMock(id=6), MagicMock(id=7)]
        mock_filter.return_value = mock_datasets

        result = explore_service.filter(number_of_features="50")

        assert result == mock_datasets
        assert len(result) == 2
        mock_filter.assert_called_once_with(
            "",
            "newest",
            "any",
            [],
            after_date=None,
            before_date=None,
            min_size=None,
            max_size=None,
            number_of_features="50",
            number_of_models="",
        )


# Test 5: Filtro por número exacto de modelos
# Este test comprueba que al filtrar por número de modelos se obtienen los datasets esperados.
def test_filter_by_exact_number_of_models(explore_service):
    with patch.object(explore_service.repository, "filter") as mock_filter:
        mock_datasets = [MagicMock(id=8)]
        mock_filter.return_value = mock_datasets

        result = explore_service.filter(number_of_models="3")

        assert result == mock_datasets
        assert len(result) == 1
        mock_filter.assert_called_once_with(
            "",
            "newest",
            "any",
            [],
            after_date=None,
            before_date=None,
            min_size=None,
            max_size=None,
            number_of_features="",
            number_of_models="3",
        )


# Test 6: Filtros combinados de características y modelos
# Este test verifica que los filtros de características y modelos combinados devuelven los resultados esperados.
def test_filter_by_features_and_models_combined(explore_service):
    with patch.object(explore_service.repository, "filter") as mock_filter:
        mock_datasets = [MagicMock(id=9)]
        mock_filter.return_value = mock_datasets

        result = explore_service.filter(number_of_features="20", number_of_models="4")

        assert result == mock_datasets
        assert len(result) == 1
        mock_filter.assert_called_once_with(
            "",
            "newest",
            "any",
            [],
            after_date=None,
            before_date=None,
            min_size=None,
            max_size=None,
            number_of_features="20",
            number_of_models="4",
        )


# Test 7: Filtro combinado con ordenamiento (antiguo primero)
# Este test valida que los resultados pueden ordenarse correctamente del más antiguo al más reciente.
def test_filter_sorting_oldest_first(explore_service):
    with patch.object(explore_service.repository, "filter") as mock_filter:
        mock_datasets = [
            MagicMock(created_at=datetime(2021, 1, 1)),
            MagicMock(created_at=datetime(2022, 1, 1)),
        ]
        mock_filter.return_value = mock_datasets

        result = explore_service.filter(sorting="oldest")

        assert result == mock_datasets
        mock_filter.assert_called_once_with(
            "",
            "oldest",
            "any",
            [],
            after_date=None,
            before_date=None,
            min_size=None,
            max_size=None,
            number_of_features="",
            number_of_models="",
        )


# Test 8: Sin filtros aplicados
# Este test asegura que si no se especifican filtros, se devuelven todos los conjuntos de datos.
def test_filter_no_criteria(explore_service):
    with patch.object(explore_service.repository, "filter") as mock_filter:
        mock_datasets = [MagicMock(id=10), MagicMock(id=11)]
        mock_filter.return_value = mock_datasets

        result = explore_service.filter()

        assert result == mock_datasets
        assert len(result) == 2
        mock_filter.assert_called_once_with(
            "",
            "newest",
            "any",
            [],
            after_date=None,
            before_date=None,
            min_size=None,
            max_size=None,
            number_of_features="",
            number_of_models="",
        )
