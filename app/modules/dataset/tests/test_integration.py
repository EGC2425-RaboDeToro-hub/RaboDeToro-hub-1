import pytest
from app import db
from app.modules.conftest import login, logout


@pytest.fixture(scope="module")
def test_client(test_client):
    with test_client.application.app_context():
        db.session.commit()
    yield test_client


def test_download_all_datasets(test_client):
    # Log in as a user
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed."

    # Test "Download All Datasets" functionality
    response = test_client.get("/dataset/download/all")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/zip"

    logout(test_client)
