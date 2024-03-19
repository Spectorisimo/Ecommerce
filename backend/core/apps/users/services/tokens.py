import uuid
from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from datetime import (
    datetime,
    timedelta,
)

from django.conf import settings

from jose import (
    jwt,
    JWTError,
)

from core.apps.users.entities.tokens import (
    TokenPayload,
    TokenType,
)
from core.apps.users.entities.users import User
from core.apps.users.exceptions.tokens import (
    IncorrectTokenValueException,
    TokenExpiredException,
    TokenIncorrectTypeException,
)


class ITokenizerService(ABC):

    @abstractmethod
    def create_access_token(self, user: User) -> str: ...

    @abstractmethod
    def create_refresh_token(self, user: User) -> str: ...

    @abstractmethod
    def decode_token(self, token: str) -> TokenPayload: ...


class TokenizerService(ITokenizerService):

    def create_access_token(self, user: User) -> str:
        expires_at = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return self._encode_token(token_type=TokenType.ACCESS, exp=expires_at, sub=user.email)

    def create_refresh_token(self, user: User) -> str:
        expires_at = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        return self._encode_token(token_type=TokenType.REFRESH, exp=expires_at, sub=user.email)

    def decode_token(self, token: str) -> TokenPayload:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except JWTError:
            raise IncorrectTokenValueException(token=token)
        else:
            token_payload = TokenPayload(**payload)
            return token_payload

    def _encode_token(self, token_type: TokenType, exp: datetime, sub: str) -> str:
        jti = self._generate_jti()
        to_encode = {"exp": exp, "sub": sub, "jti": jti, "token_type": token_type}
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def _generate_jti() -> str:
        return str(uuid.uuid4())


class ITokenValidatorService(ABC):
    def validate(self, token_payload: TokenPayload, token_type: TokenType) -> None:
        ...


class TokenTypeValidatorService(ITokenValidatorService):
    def validate(self, token_payload: TokenPayload, token_type: TokenType) -> None:
        if token_payload.token_type != token_type:
            raise TokenIncorrectTypeException(needed_type=token_type)


class TokenExpiryValidatorService(ITokenValidatorService):
    def validate(self, token_payload: TokenPayload, *args, **kwargs) -> None:
        if datetime.fromtimestamp(token_payload.exp) < datetime.now():
            raise TokenExpiredException()


@dataclass
class ComposedTokenValidatorService(ITokenValidatorService):
    validators: list[ITokenValidatorService]

    def validate(self, token_payload: TokenPayload, token_type: TokenType) -> None:
        for validator in self.validators:
            validator.validate(token_payload=token_payload, token_type=token_type)
