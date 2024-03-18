from functools import lru_cache

import punq

from core.apps.products.repositories.products import (
    IProductRepository,
    ProductRepository,
)
from core.apps.products.services.products import (
    IProductServices,
    ProductServices,
)


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()

    container.register(IProductRepository, ProductRepository)
    container.register(IProductServices, ProductServices)

    return container
