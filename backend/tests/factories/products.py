import factory
from factory.django import DjangoModelFactory

from core.apps.products.models.products import Product


class ProductModelFactory(DjangoModelFactory):
    title = factory.Faker('first_name')
    description = factory.Faker('text')
    amount = factory.Faker('pydecimal', left_digits=10, right_digits=2)

    class Meta:
        model = Product
