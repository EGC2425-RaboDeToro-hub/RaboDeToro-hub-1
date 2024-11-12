from app.modules.community.repositories import CommunityRepository
from app.modules.community.repositories import CommunityUsersRepository
from app.modules.community.models import CommunityUser
from app.modules.community.models import Community
from core.services.BaseService import BaseService


class CommunityUserService(BaseService):
    def __init__(self):
        super().__init__(CommunityUsersRepository())

    def get_users_by_community(self, community_id):
        return self.repository.get_users_by_community(community_id)

    def get_by_user_id(self, user_id):
        return self.repository.get_by_user_id(user_id)

    def create(self, code, user_id, community_id, is_admin=False):
        # Check if community exists
        community = Community.query.filter_by(code=code).first()
        if not community:
            return None

        # Check if user is already in community
        community_user = CommunityUser.query.filter_by(user_id=user_id, community_id=community.id).first()
        if community_user:
            return None

        # Create community user
        community_user = self.repository.model(
            user_id=user_id,
            community_id=community_id,
            is_admin=is_admin
        )
        self.repository.save(community_user)
        return community_user

    def delete(self, user_id, community_id):
        community_user = CommunityUser.query.filter_by(user_id=user_id, community_id=community_id).first()
        if not community_user:
            return False
        self.repository.delete(community_user)
        return True

    def make_admin(self, user_id, community_id):
        community_user = CommunityUser.query.filter_by(user_id=user_id, community_id=community_id).first()
        if not community_user:
            return False
        community_user.is_admin = True
        self.repository.save(community_user)
        return True

    def remove_admin(self, user_id, community_id):
        community_user = CommunityUser.query.filter_by(user_id=user_id, community_id=community_id).first()
        if not community_user:
            return False

        community_user.is_admin = False
        self.repository.save(community_user)
        return True


class CommunityService(BaseService):
    def __init__(self):
        super().__init__(CommunityRepository())
        self.community_user_service = CommunityUserService()

    def get_community_by_id(self, community_id):
        return self.repository.get_by_id(community_id)

    def get_communities_by_user_id(self, user_id):
        return self.repository.get_communities_by_user_id(user_id)

    def get_communities_by_dataset_id(self, dataset_id):
        return self.repository.get_communities_by_dataset_id(dataset_id)

    def create_community(self, name, description, code, owner):
        community = self.repository.model(
            name=name,
            description=description,
            code=code
        )
        self.community_user_service.create(user_id=owner.id, community_id=community.id, is_admin=True)
        self.repository.save(community)
        return community

    def update_community(self, community_id, name=None, code=None, description=None):
        community = self.repository.get_by_id(community_id)
        if not community:
            return None
        if name:
            community.name = name
        if description:
            community.description = description
        if code:
            community.code = code
        self.repository.save(community)
        return community

    def delete_community(self, community_id):
        community = self.repository.get_by_id(community_id)
        if community:
            self.repository.delete(community)
            return True
        community_users = CommunityUser.query.filter_by(community_id=community_id).all()
        for user in community_users:
            self.community_user_service.delete(user.user_id, community_id)
        return False
