from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.common.models import BaseDateTimeModel
from core.apps.products.entities.products import Product as ProductEntity


class Product(BaseDateTimeModel):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    additional_data = models.JSONField(default=dict, verbose_name=_('Additional data'))
    amount = models.DecimalField(max_digits=14, decimal_places=2, verbose_name=('Amount'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is active'))
    tags = ArrayField(verbose_name='Product tags', default=list, base_field=models.CharField(max_length=100))

    @classmethod
    def from_entity(cls, product: ProductEntity) -> 'Product':
        return cls(
            id=product.id,
            title=product.title,
            description=product.description,
            additional_data=product.additional_data,
            amount=product.amount,
            tags=product.tags,
            is_active=product.is_active,
        )

    def to_entity(self) -> ProductEntity:
        return ProductEntity(
            id=self.id,
            title=self.title,
            description=self.description,
            additional_data=self.additional_data,
            amount=self.amount,
            tags=self.tags,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
