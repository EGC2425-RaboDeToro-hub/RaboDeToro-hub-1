from app.modules.explore.repositories import ExploreRepository
from core.services.BaseService import BaseService


class ExploreService(BaseService):
    def __init__(self):
        super().__init__(ExploreRepository())

    def filter(
        self,
        query="",
        sorting="newest",
        publication_type="any",
        tags=[],
        after_date=None,
        before_date=None,
        min_size=None,
        max_size=None,
        number_of_features="",
        number_of_models="",
        **kwargs
    ):
        return self.repository.filter(
            query,
            sorting,
            publication_type,
            tags,
            after_date=after_date,
            before_date=before_date,
            min_size=min_size,
            max_size=max_size,
            number_of_features=number_of_features,
            number_of_models=number_of_models,
            **kwargs
        )
