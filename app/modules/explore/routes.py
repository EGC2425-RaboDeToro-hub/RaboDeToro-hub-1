from flask import render_template, request, jsonify
from datetime import datetime

from app.modules.explore import explore_bp
from app.modules.explore.forms import ExploreForm
from app.modules.explore.services import ExploreService


@explore_bp.route('/explore', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        query = request.args.get('query', '')
        after_date = request.args.get('after_date')
        before_date = request.args.get('before_date')
        sorting = request.args.get('sorting', 'newest')
        publication_type = request.args.get('publication_type', 'any')
        tags = request.args.getlist('tags')

        # Convertir las fechas a datetime si están presentes y ajustar la hora
        if after_date:
            try:
                after_date = datetime.strptime(after_date, '%Y-%m-%d')
                after_date = after_date.replace(hour=0, minute=0, second=0)  # Ajustar a 00:00
                print("Adjusted after_date:", after_date)  # Depuración
            except ValueError:
                after_date = None
        if before_date:
            try:
                before_date = datetime.strptime(before_date, '%Y-%m-%d')
                before_date = before_date.replace(hour=23, minute=59, second=59)  # Ajustar a 23:59
                print("Adjusted before_date:", before_date)  # Depuración
            except ValueError:
                before_date = None

        datasets = ExploreService().filter(
            query=query,
            sorting=sorting,
            publication_type=publication_type,
            tags=tags,
            after_date=after_date,
            before_date=before_date
        )

        form = ExploreForm()
        return render_template('explore/index.html', form=form, query=query, datasets=datasets)

    if request.method == 'POST':
        criteria = request.get_json()

        # Extrae after_date y before_date desde el JSON recibido
        after_date = criteria.get('after_date')
        before_date = criteria.get('before_date')

        # Verificar y convertir las fechas
        if after_date:
            try:
                after_date = datetime.strptime(after_date, '%Y-%m-%d')
                after_date = after_date.replace(hour=0, minute=0, second=0)
                print(f"after_date: {after_date}")  # Depuración
            except ValueError:
                print("Formato incorrecto de after_date")
                after_date = None

        if before_date:
            try:
                before_date = datetime.strptime(before_date, '%Y-%m-%d')
                before_date = before_date.replace(hour=23, minute=59, second=59)
                print(f"before_date: {before_date}")  # Depuración
            except ValueError:
                print("Formato incorrecto de before_date")
                before_date = None

        # Actualizar criteria con los valores procesados
        criteria['after_date'] = after_date
        criteria['before_date'] = before_date

        # Llama al servicio de filtrado con los criterios
        datasets = ExploreService().filter(**criteria)
        return jsonify([dataset.to_dict() for dataset in datasets])
