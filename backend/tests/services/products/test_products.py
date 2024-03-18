import pytest
from tests.factories.products import ProductModelFactory

from core.api.filters import PaginationIn
from core.apps.products.filters.products import ProductFilters
from core.apps.products.services.products import IProductServices


@pytest.mark.django_db
class ProductServiceTest:

    def test_product_count_zero(self, product_service: IProductServices):
        """Test product count zero with no products in database."""
        products_count = product_service.get_product_count(ProductFilters())
        assert products_count == 0

    def test_get_products_count_exist(self, product_service: IProductServices):
        """Test product count zero with no products in database."""
        expected_count = 5
        ProductModelFactory.create_batch(size=expected_count)

        products_count = product_service.get_product_count(ProductFilters())
        assert products_count == expected_count, f'{products_count=}'

    def test_get_products_all(self, product_service: IProductServices):
        """Test all products retrieved from database."""
        expected_count = 5
        products = ProductModelFactory.create_batch(size=expected_count)
        products_titles = [product.title for product in products]

        fetched_products = product_service.get_product_list(PaginationIn(), ProductFilters())
        fetched_titles = [product.title for product in fetched_products]

        assert len(fetched_titles) == expected_count, f'{fetched_titles=}'
        assert products_titles == fetched_titles, f'{products_titles=}'

    def test_get_products_zero(self, product_service: IProductServices):
        fetched_products = product_service.get_product_list(PaginationIn(), ProductFilters())
        fetched_titles = [product.title for product in fetched_products]

        assert len(fetched_titles) == 0, f'{fetched_titles=}'
        assert [] == fetched_titles

    def test_get_product_by_id(self, product_service: IProductServices):
        """Test retrieving product by id from database."""
        expected_count = 1
        product = ProductModelFactory.create_batch(size=expected_count)[0]

        fetched_product = product_service.get_product_by_id(product.id)

        assert product.title == fetched_product.title, f'{product.title}'
