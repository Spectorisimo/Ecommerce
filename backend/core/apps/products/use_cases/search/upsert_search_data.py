from dataclasses import dataclass

from core.apps.products.services.products import IProductServices
from core.apps.products.services.search import IProductSearchService


@dataclass
class UpsertSearchDataUseCase:
    search_service: IProductSearchService
    product_service: IProductServices

    def execute(self) -> None:
        products = self.product_service.get_all_products()
        [self.search_service.upsert_product(product=product) for product in products]
