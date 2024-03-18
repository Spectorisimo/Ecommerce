from abc import (
    ABC,
    abstractmethod,
)

from django.db.models import Q

from core.api.filters import PaginationIn
from core.api.v1.products.filters import ProductFilters
from core.apps.products.entities.products import Product as ProductEntity
from core.apps.products.exceptions.products import ProductNotFoundException
from core.apps.products.models.products import Product


class IProductRepository(ABC):

    @abstractmethod
    def get_product_by_id(self, product_id: int) -> ProductEntity: ...

    @abstractmethod
    def create_product(self, product: ProductEntity) -> ProductEntity: ...

    @abstractmethod
    def get_product_list(self, pagination: PaginationIn, filters: ProductFilters) -> list[ProductEntity]: ...

    @abstractmethod
    def get_product_count(self, filters: ProductFilters) -> int: ...


class ProductRepository(IProductRepository):

    def get_product_by_id(self, product_id: int) -> ProductEntity:
        product = Product.objects.filter(id=product_id)
        if not product:
            raise ProductNotFoundException(product_id=product_id)
        return product.first().to_entity()

    def create_product(self, product: ProductEntity) -> ProductEntity:
        product_dto = Product.from_entity(product)
        product_dto.save()
        return product_dto.to_entity()

    def get_product_list(self, pagination: PaginationIn, filters: ProductFilters) -> list[ProductEntity]:
        query = self._build_product_query(filters)
        queryset = Product.objects.filter(query)[pagination.offset:pagination.offset + pagination.limit]
        return [product.to_entity() for product in queryset]

    def get_product_count(self, filters: ProductFilters) -> int:
        query = self._build_product_query(filters)
        return Product.objects.filter(query).count()

    def _build_product_query(self, filters: ProductFilters) -> Q:
        query = Q(is_active=True)

        if filters.search:
            query &= Q(title__icontains=filters.search) | Q(
                description__icontains=filters.search,
            )

        return query
