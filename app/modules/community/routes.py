from flask import jsonify, request, make_response, render_template
from flask_login import login_required, current_user
from app.modules.community import community_bp
from app.modules.community.services import CommunityService, CommunityUserService
from app.modules.community.forms import CreateCommunityForm, FindCommunityForm


community_service = CommunityService()
community_user_service = CommunityUserService()

base_url = "/community"


@community_bp.route(base_url, methods=['GET'])
@login_required
def index():
    findForm = FindCommunityForm()
    createForm = CreateCommunityForm()
    communities = community_service.repository.get_communities_by_user_id(current_user.id)
    return render_template('community/index.html', communities=communities, findForm=findForm, createForm=createForm)


@community_bp.route(base_url + "/<int:community_id>", methods=["GET"])
def get_community(community_id):
    community = community_service.get_community_by_id(community_id)
    if not community:
        return make_response(jsonify({"error": "Community not found"}), 404)
    return render_template('community/show.html', community=community)


@community_bp.route(base_url, methods=["POST"])
def create_community():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    code = data.get('code')
    owner_id = current_user.id
    if not owner_id:
        return make_response(jsonify({"error": "Owner not found"}), 404)
    community = community_service.create_community(name, description, code, owner_id)
    return render_template('community/show.html', community=community)


@community_bp.route(base_url + "/<int:community_id>", methods=["PUT"])
def update_community(community_id):
    data = request.json
    name = data.get('name')
    description = data.get('description')
    code = data.get('code')
    community = community_service.update_community(community_id, name, code, description)
    if not community:
        return make_response(jsonify({"error": "Community not found"}), 404)
    return jsonify(community.to_dict())


@community_bp.route(base_url + "/<int:community_id>", methods=["DELETE"])
def delete_community(community_id):
    success = community_service.delete_community(community_id)
    if not success:
        return make_response(jsonify({"error": "Community not found"}), 404)
    return make_response(jsonify({"message": "Community deleted successfully"}), 200)


@community_bp.route(base_url + "/<int:community_id>/users", methods=["GET"])
def get_users_by_community(community_id):
    users = community_user_service.get_users_by_community(community_id)
    return jsonify([user.to_dict() for user in users])
