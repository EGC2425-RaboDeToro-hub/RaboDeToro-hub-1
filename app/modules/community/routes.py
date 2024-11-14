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
    community = community_service.get_community_by_id(community_id)
    if not community:
        return redirect(url_for('community.index'))
    return render_template('community/show.html', community=community)


@community_bp.route(base_url + "/join", methods=["POST"])
@login_required
def join_community():
    form = FindCommunityForm()
    if form.validate_on_submit():
        code = form.joinCode.data
        community = community_service.get_community_by_code(code)
        community_user = None
        if not community:
            flash("No existe ninguna comunidad con este codigo", "error")
        else:
            community_user = community_user_service.get_by_user_id_and_community(current_user.id, community.id)
            if community_user is None:
                community_user_service.create(code, current_user.id, community.id)
                return render_template('community/show.html', community_id=community.id)
            else:
                flash("Ya perteneces a esta comunidad", "error")
    return render_template('community/index.html', findForm=form, createForm=CreateCommunityForm())


@community_bp.route(base_url + "/create", methods=["POST"])
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
            return redirect(url_for('community.index'))
        community = community_service.create_community(name=name, description=description,
                                                       code=code, owner=current_user.id)
        flash("Comunidad creada exitosamente!", "success")
        return redirect(url_for('community.get_community', community_id=community.id))
    else:
        flash("Error en el formulario", "error")
    return render_template('community/index.html', createForm=form, findForm=FindCommunityForm())


@community_bp.route(base_url + "/<int:community_id>", methods=["PUT"])
@login_required
def update_community(community_id):
    data = request.json
    name = data.get('name')
    description = data.get('description')
    code = data.get('code')
    community = community_service.update_community(community_id, name, code, description)
    if not community:
        return make_response(jsonify({"message": "Community not found"}), 404)
    return get_community(community_id)


@community_bp.route(base_url + "/<int:community_id>", methods=["DELETE"])
@login_required
def delete_community(community_id):
    success = community_service.delete_community(community_id)
    if not success:
        return make_response(jsonify({"message": "Community not found"}), 404)
    return index()
