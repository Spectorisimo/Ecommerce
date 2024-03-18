from abc import (
    ABC,
    abstractmethod,
)

from django.contrib.auth.hashers import check_password

from core.apps.users.entities.users import User
from core.apps.users.exceptions.users import UserInvalidCredentialsException
from core.apps.users.repositories.users import IUserRepository


class IUserService(ABC):

    @abstractmethod
    def get_user_by_email(self, email: str) -> User: ...

    @staticmethod
    @abstractmethod
    def compare_passwords(given_password: str, user_password: str) -> None: ...


class UserService(IUserService):

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def get_user_by_email(self, email: str) -> User:
        return self.user_repository.get_by_email(email)

    @staticmethod
    def compare_passwords(given_password: str, user_password: str) -> None:
        if not check_password(given_password, user_password):
            raise UserInvalidCredentialsException()
