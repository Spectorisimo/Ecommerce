from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from core.apps.common.clients.elasticsearch import ElasticClient
from core.apps.products.entities.products import Product as ProductEntity


@dataclass
class IProductSearchService(ABC):
    @abstractmethod
    def upsert_product(self, product: ProductEntity) -> None: ...


@dataclass
class ElasticProductSearchService(IProductSearchService):
    client: ElasticClient
    index_name: str

    def upsert_product(self, product: ProductEntity) -> None:
        self.client.upsert_index(
            index=self.index_name,
            document_id=product.id,
            document=self._build_as_document(product),
        )

    @staticmethod
    def _build_as_document(product: ProductEntity) -> dict:
        return {
            'id': product.id,
            'title': product.title,
            'description': product.description,
            'tags': product.tags,
        }
