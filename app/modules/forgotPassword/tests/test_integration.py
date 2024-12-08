import pytest
from app import db
from app.modules.conftest import login, logout


@pytest.fixture(scope="module")
def test_client(test_client):
    with test_client.application.app_context():
        db.session.commit()
    yield test_client


def test_forgotPassword(test_client):
    # Log in as a user
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed."

    # Test "Download All Datasets" functionality
    response = test_client.get("/forgotPassword/forgot")
    assert response.status_code == 200

    logout(test_client)
