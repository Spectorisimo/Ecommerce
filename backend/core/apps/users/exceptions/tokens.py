from dataclasses import dataclass

from core.apps.common.exceptions import ServiceException


@dataclass(eq=False)
class IncorrectTokenValueException(ServiceException):
    token: str

    @property
    def message(self):
        return f'Given incorrect value of token {self.token}'


@dataclass(eq=False)
class TokenExpiredException(ServiceException):

    @property
    def message(self):
        return 'Given token has been expired'


@dataclass(eq=False)
class TokenIncorrectTypeException(ServiceException):
    needed_type: str

    @property
    def message(self):
        return f"Given token's type is not {self.needed_type}"
