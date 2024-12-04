import pytest
from app import db
from app.modules.conftest import login, logout
from app.modules.dataset.models import DataSet, User
from app.modules.profile import profile_bp

# Fixture que crea un cliente de prueba
@pytest.fixture(scope="module")
def test_client(test_client):
    with test_client.application.app_context():
        db.session.commit()  # Asegurarse de que los cambios previos en la DB se han guardado
    yield test_client


# Test de integración para la ruta /profile/summary
def test_user_profile_with_datasets(test_client):
    """
    Verifica que la ruta /profile/summary devuelve correctamente los datasets del usuario.
    """
    # Obtener un usuario con datasets en la base de datos
    user = db.session.query(User).filter(User.email == "user@example.com").first()
    assert user is not None, "No user found in the database"

    # Crear datasets asociados al usuario en la base de datos
    datasets = db.session.query(DataSet).filter(DataSet.user_id == user.id).all()
    assert datasets, "No datasets found for the user"

    # Realizar login
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed"

    # Realizar la solicitud a la ruta de perfil
    response = test_client.get("/profile/summary")

    # Verificar que la respuesta fue exitosa (código de estado 200)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Verificar que los datasets asociados al usuario se encuentran en la respuesta HTML
    for dataset in datasets:
        assert dataset.title.encode('utf-8') in response.data, f"Dataset '{dataset.title}' not found in response."

    # Cerrar sesión
    logout(test_client)


# Test de integración para un usuario sin datasets
def test_user_profile_without_datasets(test_client):
    """
    Verifica que la ruta /profile/summary no devuelve datasets para un usuario sin datasets.
    """
    # Obtener un usuario sin datasets
    user = db.session.query(User).filter(User.email == "user_without_datasets@example.com").first()
    assert user is not None, "No user found in the database"

    # Realizar login
    login_response = login(test_client, "user_without_datasets@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed"

    # Realizar la solicitud a la ruta de perfil
    response = test_client.get("/profile/summary")

    # Verificar que la respuesta fue exitosa (código de estado 200)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Verificar que no se muestren datasets en la respuesta
    assert b"datasets" not in response.data, "Datasets should not be present in the response."

    # Cerrar sesión
    logout(test_client)
