from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from core.api.filters import PaginationIn
from core.apps.products.entities.products import Product as ProductEntity
from core.apps.products.filters.products import ProductFilters
from core.apps.products.repositories.products import IProductRepository


class IProductServices(ABC):
    @abstractmethod
    def get_product_by_id(self, product_id: int) -> ProductEntity: ...

    @abstractmethod
    def create_product(self, product: ProductEntity) -> ProductEntity: ...

    @abstractmethod
    def get_product_list(self, pagination: PaginationIn, filters: ProductFilters) -> list[ProductEntity]: ...

    @abstractmethod
    def get_product_count(self, filters: ProductFilters) -> int: ...


@dataclass
class ProductServices(IProductServices):
    product_repository: IProductRepository

    def get_product_by_id(self, product_id: int) -> ProductEntity:
        return self.product_repository.get_product_by_id(product_id=product_id)

    def create_product(self, product: ProductEntity) -> ProductEntity:
        return self.product_repository.create_product(product=product)

    def get_product_list(self, pagination: PaginationIn, filters: ProductFilters) -> list[ProductEntity]:
        return self.product_repository.get_product_list(pagination=pagination, filters=filters)

    def get_product_count(self, filters: ProductFilters) -> int:
        return self.product_repository.get_product_count(filters=filters)
