import pytest
from unittest.mock import patch, MagicMock
from app.modules.community.services import CommunityService, CommunityUserService


@pytest.fixture(scope='module')
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        # Add HERE new elements to the database that you want to exist in the test context.
        # DO NOT FORGET to use db.session.add(<element>) and db.session.commit() to save the data.
        pass

    yield test_client


@pytest.fixture
def community_service():
    return CommunityService()


@pytest.fixture
def community_user_service():
    return CommunityUserService()


def test_sample_assertion(test_client):
    """
    Sample test to verify that the test framework and environment are working correctly.
    It does not communicate with the Flask application; it only performs a simple assertion to
    confirm that the tests in this module can be executed.
    """
    greeting = "Hello, World!"
    assert greeting == "Hello, World!", "The greeting does not coincide with 'Hello, World!'"


def test_get_community_by_code(community_service):
    with patch.object(community_service.repository, 'get_by_code') as mock_get_by_code:
        mock_community = MagicMock(id=1, code='testcode')
        mock_get_by_code.return_value = mock_community

        code = 'testcode'
        result = community_service.get_community_by_code(code)

        assert result == mock_community
        assert result.code == 'testcode'
        mock_get_by_code.assert_called_once_with(code=code)


def test_get_community_by_code_not_found(community_service):
    with patch.object(community_service.repository, 'get_by_code') as mock_get_by_code:
        mock_get_by_code.return_value = None

        code = 'nonexistentcode'
        result = community_service.get_community_by_code(code)

        assert result is None
        mock_get_by_code.assert_called_once_with(code=code)


def test_create_community(community_service):
    with patch.object(community_service.repository, 'create') as mock_create:
        mock_community = MagicMock(id=1, name='Test Community', code='testcode', description='Test Description')
        mock_create.return_value = mock_community

        name = 'Test Community'
        description = 'Test Description'
        code = 'testcode'

        result = community_service.create(name=name, description=description, code=code)

        assert result == mock_community
        assert result.id == 1
        mock_create.assert_called_once_with(name=name, description=description, code=code)


def test_update_community(community_service):
    with patch.object(community_service.repository, 'update') as mock_update:
        mock_community = MagicMock()
        mock_community.id = 1
        mock_community.name = 'Updated Community'
        mock_community.code = 'updatedCode'
        mock_community.description = 'Updated Description'
        mock_update.return_value = mock_community

        community_id = 1
        name = 'Updated Community'
        description = 'Updated Description'
        code = 'updatedCode'

        result = community_service.update(community_id, name=name, description=description, code=code)

        assert result == mock_community
        assert result.name == 'Updated Community'
        assert result.code == 'updatedCode'
        assert result.description == 'Updated Description'
        mock_update.assert_called_once_with(community_id, name=name, description=description, code=code)


def test_delete_community(community_service):
    with patch.object(community_service.repository, 'delete') as mock_delete:
        mock_delete.return_value = True

        community_id = 1
        result = community_service.delete(community_id)

        assert result is True
        mock_delete.assert_called_once_with(community_id)


def test_get_users_by_community(community_user_service):
    with patch.object(community_user_service.repository, 'get_users_by_community') as mock_get_users:
        mock_users = [MagicMock(id=1), MagicMock(id=2)]
        mock_get_users.return_value = mock_users

        community_id = 1
        result = community_user_service.get_users_by_community(community_id)

        assert result == mock_users
        assert len(result) == 2
        mock_get_users.assert_called_once_with(community_id)


def test_get_users_by_community_not_found(community_user_service):
    with patch.object(community_user_service.repository, 'get_users_by_community') as mock_get_users:
        mock_get_users.return_value = []

        community_id = 1
        result = community_user_service.get_users_by_community(community_id)

        assert result == []
        mock_get_users.assert_called_once_with(community_id)
