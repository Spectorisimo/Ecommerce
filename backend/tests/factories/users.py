import factory
from factory.django import DjangoModelFactory

from core.apps.users.models import CustomUser


class UserModelFactory(DjangoModelFactory):
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    class Meta:
        model = CustomUser
