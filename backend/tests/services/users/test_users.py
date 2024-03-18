import pytest
from tests.factories.users import UserModelFactory

from core.apps.users.services.users import IUserService


@pytest.mark.django_db
class UserServiceTest:

    def test_get_product_by_email(self, user_service: IUserService):
        """Test retrieving user by email from database."""
        expected_count = 1
        user = UserModelFactory.create_batch(size=expected_count)[0]

        fetched_user = user_service.get_user_by_email(user.email)

        assert user.email == fetched_user.email, f'{user.email}'
