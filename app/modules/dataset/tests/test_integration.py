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


def test_filter_datasets_by_features(test_client):
    # Test filtering by features
    response = test_client.get("/api/v1/datasets/filtered?min_features=5&max_features=20")
    assert response.status_code == 200

    data = response.json  # Aquí se accede directamente sin llamarlo como función
    assert all(5 <= dataset["feature_count"] <= 20 for dataset in data), "Datasets not filtered correctly by features."


def test_filter_datasets_by_products(test_client):
    # Test filtering by products
    response = test_client.get("/api/v1/datasets/filtered?min_products=30&max_products=60")
    assert response.status_code == 200

    data = response.json  # Aquí se accede directamente sin llamarlo como función
    assert all(30 <= dataset["product_count"] <= 60 for dataset in data), "Datasets not filtered correctly by products."
