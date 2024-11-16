from flask import jsonify, request, make_response, render_template, redirect, url_for, flash
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
    communities = community_service.get_communities_by_user_id(current_user.id)
    return render_template('community/index.html', communities=communities, findForm=findForm, createForm=createForm)


@community_bp.route(base_url + "/<int:community_id>", methods=["GET"])
@login_required
def get_community(community_id):
    community = community_service.get_or_404(id=community_id)
    if not community:
        return make_response(jsonify({"message": "Community not found"}), 404)
    community_user = community_user_service.get_by_user_id_and_community(community_id=community.id,
                                                                         user_id=current_user.id)
    if not community_user:
        return make_response(jsonify({"message": "You are not from this community"}), 404)
    community_users = community_user_service.get_users_by_community(community_id=community.id)

    datasets = []
    for user_id in community_users:
        datasets += community_service.get_datasets_by_user_id(user_id)
    return render_template('community/show.html', community=community,
                           users=community_users, usersSize=len(community_users),
                           datasets=datasets, datasetsSize=len(datasets),
                           is_admin=community_user.is_admin)


@community_bp.route(base_url + "/create", methods=["GET", "POST"])
@login_required
def create_community():
    form = CreateCommunityForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        code = form.code.data
        community = community_service.get_community_by_code(code)
        if community:
            flash("El código ya está en uso", "error")
            return redirect(url_for('community.create_community'))
        community = community_service.create(name=name, description=description,
                                             code=code)
        community = community_service.get_community_by_code(code)
        community_user_service.create(user_id=current_user.id, community_id=community.id, is_admin=True)
        return redirect(url_for('community.get_community', community_id=community.id))
    return render_template('community/create.html', createForm=CreateCommunityForm())


@community_bp.route(base_url + "/join", methods=["GET", "POST"])
@login_required
def join_community():
    form = FindCommunityForm()
    if form.validate_on_submit():
        code = form.joinCode.data
        community = community_service.get_community_by_code(code)
        if not community:
            flash("No existe ninguna comunidad con este código", "error")
            return redirect(url_for('community.join_community'))
        community_user = community_user_service.get_by_user_id_and_community(current_user.id, community.id)
        if community_user:
            flash("Ya perteneces a esta comunidad", "error")
            return redirect(url_for('community.join_community'))
        community_user_service.create(user_id=current_user.id, community_id=community.id)
        return redirect(url_for('community.get_community', community_id=community.id))
    return render_template('community/join.html', findForm=FindCommunityForm())


@community_bp.route(base_url + "/<int:community_id>", methods=["PUT"])
@login_required
def update_community(community_id):
    data = request.json
    name = data.get('name')
    description = data.get('description')
    code = data.get('code')
    community = community_service.update(community_id, name, code, description)
    if not community:
        return make_response(jsonify({"message": "Community not found"}), 404)
    return get_community(community_id)


@community_bp.route(base_url + "/delete/<int:community_id>", methods=["DELETE"])
@login_required
def delete_community(community_id):
    # Revisa que existe la comunidad
    community = community_service.get_or_404(community_id)
    if not community:
        return flash("Comunidad no encontrada", "error")

    # Revisa que el usuario se admin de la comunidad
    community_user = community_user_service.get_by_user_id_and_community(current_user.id, community_id)
    if not community_user or not community_user.is_admin:
        flash("No tienes permisos para eliminar esta comunidad", "error")
        return redirect(url_for('community.edit'))

    community_service.delete(community_id)
    return index()
