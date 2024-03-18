import pytest

from core.apps.products.containers.products import get_container
from core.apps.products.services.products import IProductServices


@pytest.fixture()
def product_service() -> IProductServices:
    container = get_container()
    product_service = container.resolve(IProductServices)
    return product_service
