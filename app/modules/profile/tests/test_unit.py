from app.modules.dataset.models import Author
import pytest

from app import db
from app.modules.conftest import login, logout
from app.modules.auth.models import User
from app.modules.profile.models import UserProfile
from app.modules.dataset.models import DataSet, DSMetaData

@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    for module testing (por example, new users)
    """
    with test_client.application.app_context():
        user_test = User(email='user@example.com', password='test1234')
        db.session.add(user_test)
        db.session.commit()

        profile = UserProfile(user_id=user_test.id, name="Name", surname="Surname")
        db.session.add(profile)
        db.session.commit()

    yield test_client


def test_edit_profile_page_get(test_client):
    """
    Tests access to the profile editing page via a GET request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.get("/profile/edit")
    assert response.status_code == 200, "The profile editing page could not be accessed."
    assert b"Edit profile" in response.data, "The expected content is not present on the page"

    logout(test_client)


# Test 1: Verifica que los datasets asociados a un autor específico se muestran correctamente
def test_get_author_datasets_with_existing_data(client):
    """
    Verifica que la ruta devuelve correctamente los datasets almacenados en la base de datos
    asociados a un autor específico.
    """
    with client.application.app_context():
        author = Author.query.first()
        assert author is not None, "No hay ningún autor en la base de datos para realizar la prueba."

        datasets = DataSet.query.join(DSMetaData).filter(DSMetaData.authors.any(id=author.id)).all()
        assert datasets, f"El autor con ID {author.id} no tiene datasets asociados en la base de datos."

    response = client.get(f"/author/{author.id}/projects")

    assert response.status_code == 200, "La ruta no devolvió un estado HTTP 200."

    for dataset in datasets:
        assert dataset.title.encode('utf-8') in response.data, f"El dataset '{dataset.title}' no aparece en la respuesta."

    assert author.name.encode('utf-8') in response.data, f"El nombre del autor '{author.name}' no aparece en la respuesta."

# Test 2: Verifica que devuelve un error 404 si el autor no existe
def test_get_author_datasets_not_found(client):
    """
    Verifica que la ruta devuelve un error 404 si el autor no existe.
    """
    # Buscar un ID de autor que no exista
    with client.application.app_context():
        max_id = db.session.query(db.func.max(Author.id)).scalar()
        nonexistent_author_id = (max_id or 0) + 1

    # Realizar la solicitud GET para un autor inexistente
    response = client.get(f"/author/{nonexistent_author_id}/projects")

    # Verificar que la respuesta tiene el estado 404
    assert response.status_code == 404, "La ruta no devolvió un estado HTTP 404 para un autor inexistente."
