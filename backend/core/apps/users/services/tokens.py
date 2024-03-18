import uuid
from abc import (
    ABC,
    abstractmethod,
)
from datetime import (
    datetime,
    timedelta,
)

from django.conf import settings

from jose import jwt

from core.apps.users.entities.tokens import (
    TokenPayload,
    TokenType,
)
from core.apps.users.entities.users import User
from core.apps.users.exceptions.tokens import (
    TokenExpiredException,
    TokenIncorrectTypeException,
)


ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"


class ITokenizerService(ABC):

    @abstractmethod
    def create_access_token(self, user: User) -> str: ...

    @abstractmethod
    def create_refresh_token(self, user: User) -> str: ...

    @abstractmethod
    def verify_token(self, token: str, token_type: TokenType) -> TokenPayload: ...


class TokenizerService(ITokenizerService):

    def create_access_token(self, user: User) -> str:
        expires_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return self._sign_token(token_type=TokenType.ACCESS, exp=expires_at, sub=user.email)

    def create_refresh_token(self, user: User) -> str:
        expires_at = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        return self._sign_token(token_type=TokenType.REFRESH, exp=expires_at, sub=user.email)

    def verify_token(self, token: str, token_type: TokenType) -> TokenPayload:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM],
        )

        decoded_token = TokenPayload(**payload)

        if decoded_token.token_type != token_type:
            raise TokenIncorrectTypeException(needed_type=token_type)

        if datetime.fromtimestamp(decoded_token.exp) < datetime.now():
            raise TokenExpiredException()

        return decoded_token

    def _sign_token(self, token_type: TokenType, exp: datetime, sub: str) -> str:
        jti = self._generate_jti()
        to_encode = {"exp": exp, "sub": sub, "jti": jti, "token_type": token_type}
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, ALGORITHM)
        return encoded_jwt

    @staticmethod
    def _generate_jti() -> str:
        return str(uuid.uuid4())
