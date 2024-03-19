from abc import (
    ABC,
    abstractmethod,
)

from core.apps.users.entities.tokens import Token as TokenEntity
from core.apps.users.models.tokens import IssuedToken


class ITokenRepository(ABC):
    @abstractmethod
    def save_token(self, refresh_token: TokenEntity) -> TokenEntity: ...

    @abstractmethod
    def revoke_token(self, jti: str) -> None: ...

    @abstractmethod
    def check_revoked(self, jti: str) -> bool: ...


class TokenRepository(ITokenRepository):

    def save_token(self, refresh_token: TokenEntity) -> TokenEntity:
        token_dto = IssuedToken.from_entity(refresh_token=refresh_token)
        token_dto.save()
        return refresh_token

    def revoke_token(self, jti: str) -> None:
        IssuedToken.objects.filter(jti=jti).update(is_revoked=True)

    def check_revoked(self, jti: str) -> bool:
        return IssuedToken.objects.filter(jti=jti, is_revoked=True).exists()
