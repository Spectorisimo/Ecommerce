from functools import lru_cache

from django.conf import settings

import punq
from httpx import Client

from core.apps.common.clients.elasticsearch import ElasticClient
from core.apps.products.repositories.products import (
    IProductRepository,
    ProductRepository,
)
from core.apps.products.services.products import (
    IProductServices,
    ProductServices,
)
from core.apps.products.services.search import (
    ElasticProductSearchService,
    IProductSearchService,
)
from core.apps.products.use_cases.search.upsert_search_data import UpsertSearchDataUseCase


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()

    container.register(IProductRepository, ProductRepository)
    container.register(IProductServices, ProductServices)

    def build_elastic_search_service() -> IProductSearchService:
        return ElasticProductSearchService(
            client=ElasticClient(
                http_client=Client(base_url=settings.ELASTIC_URL),
            ),
            index_name=settings.ELASTIC_PRODUCT_INDEX,
        )

    container.register(IProductSearchService, factory=build_elastic_search_service)

    container.register(UpsertSearchDataUseCase)

    return container
