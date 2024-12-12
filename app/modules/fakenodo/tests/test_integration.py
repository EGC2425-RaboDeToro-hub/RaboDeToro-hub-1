from datetime import datetime
import pytest
from flask import url_for
from app import db
from app.modules.dataset.models import DataSet, DSMetaData, PublicationType
from app.modules.fakenodo.models import Fakenodo
from app.modules.conftest import login, logout
from app.modules.profile.models import UserProfile
from app.modules.auth.models import User


@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        user_test = User(email='user@example.com', password='test1234')
        db.session.add(user_test)
        db.session.commit()

        profile = UserProfile(user_id=user_test.id, name="Name", surname="Surname")
        db.session.add(profile)
        db.session.commit()

        ds_meta_data = DSMetaData(title = "Test metadata", description="Test metadata", publication_type= PublicationType.NONE)
        db.session.add(ds_meta_data)
        db.session.commit()

        dataset = DataSet(user_id=user_test.id, ds_meta_data_id=ds_meta_data.id, size_in_kb=1024.0, created_at=datetime.utcnow())
        db.session.add(dataset)
        db.session.commit()
        
        dep1 = Fakenodo(doi="10.1234/fake1", dep_metadata={"key": "value1"})
        dep2 = Fakenodo(doi="10.1234/fake2", dep_metadata={"key": "value2"})
        db.session.add(dep1)
        db.session.add(dep2)
        db.session.commit()
        db.session.commit()

    yield test_client

def test_test_connection_fakenodo(test_client):
    login(test_client, 'user@example.com', 'test1234')
    response = test_client.get('/fakenodo/api/test_connection')
    assert response.status_code == 200
    assert response.json == {"status": "success", "message": "Connected to FakenodoAPI"}
    logout(test_client)