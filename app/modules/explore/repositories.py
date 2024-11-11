import re
from sqlalchemy import any_, or_
import unidecode
from app.modules.dataset.models import Author, DSMetaData, DataSet, PublicationType
from app.modules.featuremodel.models import FMMetaData, FeatureModel
from core.repositories.BaseRepository import BaseRepository


class ExploreRepository(BaseRepository):
    def __init__(self):
        super().__init__(DataSet)

    def filter(self, query="", sorting="newest", publication_type="any", tags=[], after_date=None, before_date=None,
               min_size=None, max_size=None, **kwargs):
        
        normalized_query = unidecode.unidecode(query).lower()
        cleaned_query = re.sub(r'[,.":\'()\[\]^;!¡¿?]', "", normalized_query)

        filters = []
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

        datasets = (
            self.model.query
            .join(DataSet.ds_meta_data)
            .join(DSMetaData.authors)
            .join(DataSet.feature_models)
            .join(FeatureModel.fm_meta_data)
            .filter(or_(*filters))
            .filter(DSMetaData.dataset_doi.isnot(None))  
        )

        # Apply publication type filter if specified
        if publication_type != "any":
            matching_type = None
            for member in PublicationType:
                if member.value.lower() == publication_type:
                    matching_type = member
                    break

            if matching_type is not None:
                datasets = datasets.filter(DSMetaData.publication_type == matching_type.name)

        # Apply tags filter if specified
        if tags:
            datasets = datasets.filter(DSMetaData.tags.ilike(any_(f"%{tag}%" for tag in tags)))

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

        # Order by created_at
        if sorting == "oldest":
            datasets = datasets.order_by(DataSet.created_at.asc())
        else:
            datasets = datasets.order_by(DataSet.created_at.desc())

        return datasets.all()
