from dataclasses import dataclass

from core.apps.common.exceptions import RepositoryException


@dataclass(eq=False)
class ProductNotFoundException(RepositoryException):
    product_id: int

    @property
    def message(self):
        return f'Product with id {self.product_id} not found'
