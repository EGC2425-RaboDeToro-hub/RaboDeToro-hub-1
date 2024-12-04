import pytest
from app import db
from app.modules.community.models import Community, CommunityUser
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

    yield test_client


def test_create_community(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed."

    response = test_client.post('/community/create', data=dict(
        name="Test Community",
        description="This is a test community",
        code="testcode"
    ), follow_redirects=True)

    assert response.status_code == 200

    logout(test_client)


def test_join_community(test_client):
    login_response = login(test_client, "user2@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed."

    response = test_client.post('/community/join', data=dict(
        joinCode="testcode"
    ), follow_redirects=True)

    assert response.status_code == 200

    logout(test_client)


def test_update_community(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed."

    # Obtain the community ID
    community = Community.query.filter_by(code="testcode").first()

    response = test_client.post(f'/community/update/{community.id}', data=dict(
        name="Updated Community",
        description="Updated Description",
        code="testcode2"
    ), follow_redirects=True)

    assert response.status_code == 200

    logout(test_client)


def test_delete_community(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed."

    # Obtain the community ID
    community = Community.query.filter_by(code="testcode2").first()

    response = test_client.post(f'/community/delete/{community.id}', follow_redirects=True)

    assert response.status_code == 200

    logout(test_client)


def test_get_communities_by_user(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed."

    # Create a community and join it
    community = Community(name="Test Community", description="This is a test community", code="testcode")
    db.session.add(community)
    db.session.commit()

    community_user = CommunityUser(user_id=1, community_id=community.id)
    db.session.add(community_user)
    db.session.commit()

    response = test_client.get('/community')

    assert response.status_code == 200

    logout(test_client)


def test_leave_community(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login failed."

    # Obtain the community ID
    community = Community.query.filter_by(code="testcode").first()

    community_user = CommunityUser(user_id=1, community_id=community.id)
    db.session.add(community_user)
    db.session.commit()

    response = test_client.post(f'/community/leave/{community.id}', follow_redirects=True)

    assert response.status_code == 200

    logout(test_client)
