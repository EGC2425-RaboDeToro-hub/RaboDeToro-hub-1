from app.modules.community.repositories import CommunityRepository
from app.modules.community.repositories import CommunityUsersRepository
from core.services.BaseService import BaseService


class CommunityUserService(BaseService):
    def __init__(self):
        super().__init__(CommunityUsersRepository())

    def get_users_by_community(self, community_id):
        return self.repository.get_users_by_community(community_id)

    def get_by_user_id(self, user_id):
        return self.repository.get_by_user_id(user_id)

    def get_by_user_id_and_community(self, community_id, user_id):
        return self.repository.get_community_user_by_user_id_and_community(user_id=user_id, community_id=community_id)

    def create(self, user_id, community_id, is_admin=False):
        # Check if community exists
        community = self.repository.get_by_id(id=community_id)
        if not community:
            return None

        # Check if user is already in community
        community_user = self.repository.get_community_user_by_user_id_and_community(
            user_id=user_id, community_id=community_id)
        if community_user:
            return None

        # Create community user
        community_user = self.repository.model(
            user_id=user_id,
            community_id=community_id,
            is_admin=is_admin
        )
        self.repository.create(community_user.user_id, community_user.community_id, community)
        return community_user

    def delete(self, community_user):
        self.repository.delete(community_user)
        return True

    def make_admin(self, user_id, community_id):
        community_user = self.repository.get_community_user_by_user_id_and_community(
            user_id=user_id, community_id=community_id)
        if not community_user:
            return False
        community_user.is_admin = True
        self.repository.create(community_user)
        return True

    def remove_admin(self, user_id, community_id):
        community_user = self.repository.get_community_user_by_user_id_and_community(
            user_id=user_id, community_id=community_id)
        if not community_user:
            return False

        community_user.is_admin = False
        self.repository.create(community_user)
        return True


class CommunityService(BaseService):
    def __init__(self):
        super().__init__(CommunityRepository())
        self.community_user_service = CommunityUserService()

    def get_community_by_id(self, community_id):
        return self.repository.get_by_id(community_id)

    def get_community_by_code(self, code):
        return self.repository.get_by_code(code=code)

    def get_communities_by_user_id(self, user_id):
        return self.repository.get_communities_by_user_id(user_id)

    def get_communities_by_dataset_id(self, dataset_id):
        return self.repository.get_communities_by_dataset_id(dataset_id)

    def create_community(self, name, description, code, owner):
        community = self.repository.create(
            name=name,
            description=description,
            code=code
        )
        self.community_user_service.create(user_id=owner, community_id=community.id, is_admin=True)
        return community

    def update_community(self, community_id, name=None, code=None, description=None):
        community = self.repository.get_by_id(community_id)
        if not community:
            return None
        community_user_admin = self.community_user_service.get_by_user_id_and_community(
            user_id=community.owner, community_id=community_id)
        if not community_user_admin.is_admin:
            return None
        if name:
            community.name = name
        if description:
            community.description = description
        if code:
            community.code = code
        self.repository.create(community)
        return community

    def delete_community(self, community_id):
        community = self.repository.get_by_id(community_id)
        community_user_admin = self.community_user_service.get_by_user_id_and_community(
            user_id=community.owner, community_id=community_id)
        if community and community_user_admin.is_admin:
            self.repository.delete(community)
            community_users = self.repository.get_users_by_community(community_id=community_id)
            for community_user in community_users:
                self.community_user_service.delete(community_user)
            return True
        return False
