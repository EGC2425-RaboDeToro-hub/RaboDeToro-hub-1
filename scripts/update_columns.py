from app import db, create_app
from app.modules.dataset.models import DSMetrics, DataSet

# Crear la aplicación
app = create_app()

# Ejecutar dentro del contexto de la aplicación
with app.app_context():
    # Actualizar los valores de DSMetrics
    for metrics in DSMetrics.query.all():
        metrics.feature_count = len(metrics.number_of_features.split(",")) if metrics.number_of_features else 0
        metrics.product_count = len(metrics.number_of_models.split(",")) if metrics.number_of_models else 0
        db.session.add(metrics)

    # Actualizar los valores de DataSet
    for dataset in DataSet.query.all():
        dataset.size_in_kb = sum(file.size for fm in dataset.feature_models for file in fm.files) / 1024
        db.session.add(dataset)

    # Guardar los cambios
    db.session.commit()

print("Valores actualizados correctamente.")
