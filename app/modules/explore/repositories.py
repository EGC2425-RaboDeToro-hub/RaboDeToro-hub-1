import re
from sqlalchemy import any_, or_
import unidecode
from app.modules.dataset.models import Author, DSMetaData, DataSet, PublicationType, DSMetrics
from app.modules.featuremodel.models import FMMetaData, FeatureModel
from core.repositories.BaseRepository import BaseRepository


class ExploreRepository(BaseRepository):
    def __init__(self):
        super().__init__(DataSet)

    def filter(self, query="", sorting="newest", publication_type="any", tags=[], min_features=None, max_features=None, min_products=None, max_products=None, **kwargs):
        # Inicializar datasets con la consulta base
        datasets = (
            self.model.query
            .join(DataSet.ds_meta_data)
            .join(DSMetaData.authors)
            .join(DataSet.feature_models)
            .join(FeatureModel.fm_meta_data)
            .join(DSMetaData.ds_metrics)  # Asegurar la unión con DSMetrics
            .filter(DSMetaData.dataset_doi.isnot(None))  # Excluir datasets con `dataset_doi` vacío
        )

        # Aplica los filtros de búsqueda
        filters = []
        normalized_query = unidecode.unidecode(query).lower()
        cleaned_query = re.sub(r'[,.":\'()\[\]^;!¡¿?]', "", normalized_query)

        for word in cleaned_query.split():
            filters.append(DSMetaData.title.ilike(f"%{word}%"))
            filters.append(DSMetaData.description.ilike(f"%{word}%"))
            filters.append(Author.name.ilike(f"%{word}%"))
            filters.append(Author.affiliation.ilike(f"%{word}%"))
            filters.append(Author.orcid.ilike(f"%{word}%"))
            filters.append(FMMetaData.uvl_filename.ilike(f"%{word}%"))
            filters.append(FMMetaData.title.ilike(f"%{word}%"))
            filters.append(FMMetaData.description.ilike(f"%{word}%"))
            filters.append(FMMetaData.publication_doi.ilike(f"%{word}%"))
            filters.append(FMMetaData.tags.ilike(f"%{word}%"))
            filters.append(DSMetaData.tags.ilike(f"%{word}%"))

        if filters:
            datasets = datasets.filter(or_(*filters))

        # Filtros adicionales
        if publication_type != "any":
            matching_type = next((member for member in PublicationType if member.value.lower() == publication_type), None)
            if matching_type:
                datasets = datasets.filter(DSMetaData.publication_type == matching_type.name)

        if tags:
            datasets = datasets.filter(DSMetaData.tags.ilike(any_(f"%{tag}%" for tag in tags)))

        if min_features is not None:
            datasets = datasets.filter(DSMetrics.feature_count >= min_features)
        if max_features is not None:
            datasets = datasets.filter(DSMetrics.feature_count <= max_features)
        if min_products is not None:
            datasets = datasets.filter(DSMetrics.product_count >= min_products)
        if max_products is not None:
            datasets = datasets.filter(DSMetrics.product_count <= max_products)

        # Ordenar resultados
        if sorting == "oldest":
            datasets = datasets.order_by(self.model.created_at.asc())
        else:
            datasets = datasets.order_by(self.model.created_at.desc())

        return datasets.all()
