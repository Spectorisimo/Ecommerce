from datetime import datetime

from pydantic import BaseModel

from core.apps.products.entities.products import Product as ProductEntity


class ProductSchema(BaseModel):
    id: int  # noqa
    title: str
    description: str
    additional_data: dict
    is_active: bool
    created_at: datetime
    updated_at: datetime | None = None

    @staticmethod
    def from_entity(product: ProductEntity) -> 'ProductSchema':
        return ProductSchema(
            id=product.id,
            title=product.title,
            description=product.description,
            additional_data=product.additional_data,
            is_active=product.is_active,
            created_at=product.created_at,
            updated_at=product.updated_at,
        )


class CreateProductSchema(BaseModel):
    title: str
    description: str
    additional_data: dict
    is_active: bool

    @staticmethod
    def from_entity(product: ProductEntity) -> 'ProductSchema':
        return ProductSchema(
            id=product.id,
            title=product.title,
            description=product.description,
            additional_data=product.additional_data,
            is_active=product.is_active,
            created_at=product.created_at,
            updated_at=product.updated_at,
        )

    def to_entity(self) -> ProductEntity:
        return ProductEntity(
            title=self.title,
            description=self.description,
            additional_data=self.additional_data,
            is_active=self.is_active,
        )