import pytest
from flask import json
from app import db
from app.modules.conftest import login, logout


@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Configuración inicial para la base de datos y cliente de prueba.
    """
    with test_client.application.app_context():
        db.session.commit()
    yield test_client


def test_no_results_for_invalid_combination(test_client):
    """
    Verifica que una combinación inválida de filtros no devuelva resultados.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed."

    response = test_client.post(
        "/explore",
        data=json.dumps({
            "number_of_features": "999",  # Características inexistentes
            "number_of_models": "999",    # Modelos inexistentes
        }),
        content_type="application/json",
    )

    assert response.status_code == 200, "Failed to filter datasets with invalid filters."
    data = json.loads(response.data)
    assert len(data) == 0, "Datasets were found despite invalid filter combination."

    logout(test_client)
