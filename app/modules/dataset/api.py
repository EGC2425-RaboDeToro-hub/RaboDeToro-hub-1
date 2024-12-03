from flask import request
from flask_restful import Resource
from app.modules.dataset.models import DataSet
from app.modules.dataset.repositories import DataSetRepository
from core.resources.generic_resource import create_resource
from core.serialisers.serializer import Serializer

# Configuración de serialización
file_fields = {
    'file_id': 'id',
    'file_name': 'name',
    'size': 'get_formatted_size'
}
file_serializer = Serializer(file_fields)

dataset_fields = {
    'dataset_id': 'id',
    'created': 'created_at',
    'name': 'name',
    'doi': 'get_uvlhub_doi',
    'files': 'files'
}

dataset_serializer = Serializer(dataset_fields, related_serializers={'files': file_serializer})

DataSetResource = create_resource(DataSet, dataset_serializer)

# Repositorio de datasets
dataset_repository = DataSetRepository()


# Recurso de búsqueda filtrada de datasets
class FilteredDataSetResource(Resource):
    def get(self):
        min_features = request.args.get('min_features', type=int)
        max_features = request.args.get('max_features', type=int)
        min_products = request.args.get('min_products', type=int)
        max_products = request.args.get('max_products', type=int)

        # Filtrar datasets utilizando el método del repositorio
        datasets = dataset_repository.filter_datasets(
            min_features=min_features,
            max_features=max_features,
            min_products=min_products,
            max_products=max_products
        )

        # Serializar los datasets filtrados
        serialized_datasets = [dataset_serializer.serialize(dataset) for dataset in datasets]
        return serialized_datasets, 200


# Registrar recursos en el blueprint
def init_blueprint_api(api):
    """ Function to register resources with the provided Flask-RESTful Api instance. """
    api.add_resource(DataSetResource, '/api/v1/datasets/', endpoint='datasets')
    api.add_resource(DataSetResource, '/api/v1/datasets/<int:id>', endpoint='dataset')
    api.add_resource(FilteredDataSetResource, '/api/v1/datasets/filtered', endpoint='filtered_datasets')
