from abc import (
    ABC,
    abstractmethod,
)

from core.apps.users.entities.users import User
from core.apps.users.exceptions.users import UserNotFoundException
from core.apps.users.models.users import CustomUser as UserModel


class IUserRepository(ABC):

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> User: ...

    @abstractmethod
    def get_user_by_email(self, email: str) -> User: ...


class UserRepository(IUserRepository):

    def get_user_by_id(self, user_id: str) -> User:
        user_dto = UserModel.objects.get(id=user_id)
        return user_dto

    def get_user_by_email(self, email: str) -> User:
        user_dto = UserModel.objects.filter(email=email)
        if not user_dto:
            raise UserNotFoundException(email)
        return user_dto.first().to_entity()
