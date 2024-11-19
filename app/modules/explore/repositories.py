from sqlalchemy import any_, or_
import unidecode
from app.modules.dataset.models import Author, DSMetaData, DataSet, PublicationType, DSMetrics
from app.modules.featuremodel.models import FMMetaData, FeatureModel
from core.repositories.BaseRepository import BaseRepository
import re
from datetime import datetime

class ExploreRepository(BaseRepository):
    def __init__(self):
        super().__init__(DataSet)

    def filter(
        self, query="", sorting="newest", publication_type="any", tags=[], 
        after_date=None, before_date=None, min_size=None, max_size=None, 
        min_features=None, max_features=None, min_products=None, max_products=None, **kwargs
    ):
        # Inicializar consulta base
        datasets = (
            self.model.query
            .join(DataSet.ds_meta_data)
            .join(DSMetaData.authors)
            .join(DataSet.feature_models)
            .join(FeatureModel.fm_meta_data)
            .join(DSMetaData.ds_metrics)
            .filter(DSMetaData.dataset_doi.isnot(None))  # Excluir datasets con DOI vacío
        )

        # Filtros de búsqueda general (query)
        if query:
            normalized_query = unidecode.unidecode(query).lower()
            cleaned_query = re.sub(r'[,.":\'()\[\]^;!¡¿?]', "", normalized_query)

            filters = []
            for word in cleaned_query.split():
                filters += [
                    DSMetaData.title.ilike(f"%{word}%"),
                    DSMetaData.description.ilike(f"%{word}%"),
                    Author.name.ilike(f"%{word}%"),
                    Author.affiliation.ilike(f"%{word}%"),
                    Author.orcid.ilike(f"%{word}%"),
                    FMMetaData.uvl_filename.ilike(f"%{word}%"),
                    FMMetaData.title.ilike(f"%{word}%"),
                    FMMetaData.description.ilike(f"%{word}%"),
                    FMMetaData.publication_doi.ilike(f"%{word}%"),
                    FMMetaData.tags.ilike(f"%{word}%"),
                    DSMetaData.tags.ilike(f"%{word}%"),
                ]
            datasets = datasets.filter(or_(*filters))

        # Filtro por tipo de publicación
        if publication_type != "any":
            matching_type = next((member for member in PublicationType if member.value.lower() == publication_type), None)
            if matching_type:
                datasets = datasets.filter(DSMetaData.publication_type == matching_type.name)

        # Filtro por tags
        if tags:
            datasets = datasets.filter(or_(*[DSMetaData.tags.ilike(f"%{tag}%") for tag in tags]))

        # Filtros de métricas (características y productos)
        if min_features is not None:
            datasets = datasets.filter(DSMetrics.feature_count >= min_features)
        if max_features is not None:
            datasets = datasets.filter(DSMetrics.feature_count <= max_features)
        if min_products is not None:
            datasets = datasets.filter(DSMetrics.product_count >= min_products)
        if max_products is not None:
            datasets = datasets.filter(DSMetrics.product_count <= max_products)


        # Filtro de fechas
        if after_date and before_date:
            datasets = datasets.filter(DataSet.created_at.between(after_date, before_date))
        elif after_date:
            datasets = datasets.filter(DataSet.created_at >= after_date)
        elif before_date:
            datasets = datasets.filter(DataSet.created_at <= before_date)
            
        # Filtro de tamaño
        if min_size is not None or max_size is not None:
            if min_size is not None:
                datasets = datasets.filter(DataSet.size_in_kb >= min_size)
            if max_size is not None:
                datasets = datasets.filter(DataSet.size_in_kb <= max_size)

        # Ordenamiento
        if sorting == "oldest":
            datasets = datasets.order_by(DataSet.created_at.asc())
        else:  # Default to "newest"
            datasets = datasets.order_by(DataSet.created_at.desc())

        return datasets.all()
