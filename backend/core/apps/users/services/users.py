from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from django.contrib.auth.hashers import check_password

from core.apps.users.entities.users import User
from core.apps.users.exceptions.users import UserInvalidCredentialsException
from core.apps.users.repositories.users import IUserRepository


class IUserService(ABC):

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> User: ...

    @abstractmethod
    def get_user_by_email(self, email: str) -> User: ...

    @staticmethod
    @abstractmethod
    def compare_passwords(given_password: str, user_password: str) -> None: ...


@dataclass
class UserService(IUserService):
    user_repository: IUserRepository

    def get_user_by_id(self, user_id: str) -> User:
        return self.user_repository.get_user_by_id(user_id)

    def get_user_by_email(self, email: str) -> User:
        return self.user_repository.get_user_by_email(email)

    @staticmethod
    def compare_passwords(given_password: str, user_password: str) -> None:
        if not check_password(given_password, user_password):
            raise UserInvalidCredentialsException()
