from datetime import datetime

from _decimal import Decimal
from pydantic import BaseModel

from core.apps.products.entities.products import Product as ProductEntity


class ProductSchema(BaseModel):
    id: int  # noqa
    title: str
    description: str
    additional_data: dict
    amount: Decimal
    is_active: bool
    tags: list[str]
    created_at: datetime
    updated_at: datetime | None = None

    @classmethod
    def from_entity(cls, product: ProductEntity) -> 'ProductSchema':
        return ProductSchema(
            id=product.id,
            title=product.title,
            description=product.description,
            additional_data=product.additional_data,
            amount=product.amount,
            tags=product.tags,
            is_active=product.is_active,
            created_at=product.created_at,
            updated_at=product.updated_at,
        )


class CreateProductSchema(BaseModel):
    title: str
    description: str
    additional_data: dict
    amount: Decimal
    is_active: bool
    tags: list[str]

    @staticmethod
    def from_entity(product: ProductEntity) -> 'ProductSchema':
        return ProductSchema(
            id=product.id,
            title=product.title,
            description=product.description,
            additional_data=product.additional_data,
            amount=product.amount,
            tags=product.tags,
            is_active=product.is_active,
            created_at=product.created_at,
            updated_at=product.updated_at,
        )

    def to_entity(self) -> ProductEntity:
        return ProductEntity(
            title=self.title,
            description=self.description,
            additional_data=self.additional_data,
            amount=self.amount,
            tags=self.tags,
            is_active=self.is_active,
        )
