from abc import (
    ABC,
    abstractmethod,
)

from core.apps.users.entities.users import User
from core.apps.users.exceptions.users import UserNotFoundException
from core.apps.users.models.users import CustomUser as UserModel


class IUserRepository(ABC):

    @abstractmethod
    def get_by_email(self, email: str) -> User: ...


class UserRepository(IUserRepository):

    def get_by_email(self, email: str) -> User:
        user = UserModel.objects.filter(email=email)
        if not user:
            raise UserNotFoundException(email)
        return user.first().to_entity()
