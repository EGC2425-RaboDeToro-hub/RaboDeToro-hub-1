from app import db, create_app
from app.modules.dataset.models import DataSet

# Crear la aplicación para que pueda acceder al contexto de la base de datos
app = create_app()

with app.app_context():
    datasets = DataSet.query.all()
    for dataset in datasets:
        dataset.calculate_total_size()
        db.session.add(dataset)
    db.session.commit()
    print("Se actualizaron los tamaños de todos los datasets.")
