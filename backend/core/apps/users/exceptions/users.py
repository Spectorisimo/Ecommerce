from dataclasses import dataclass

from core.apps.common.exceptions import (
    RepositoryException,
    ServiceException,
)


@dataclass(eq=False)
class UserNotFoundException(RepositoryException):
    email: str

    @property
    def message(self):
        return f'User with email {self.email} not found'


@dataclass(eq=False)
class UserInvalidCredentialsException(ServiceException):

    @property
    def message(self):
        return 'Incorrect email or password'
