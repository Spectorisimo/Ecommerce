import pytest

from core.apps.users.containers import get_container
from core.apps.users.services.users import IUserService


@pytest.fixture()
def user_service() -> IUserService:
    container = get_container()
    user_service = container.resolve(IUserService)
    return user_service
