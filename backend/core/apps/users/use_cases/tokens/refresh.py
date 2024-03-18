from dataclasses import dataclass

from core.apps.users.entities.tokens import (
    TokenPair,
    TokenType,
)
from core.apps.users.services.tokens import ITokenizerService
from core.apps.users.services.users import IUserService


@dataclass
class RefreshTokenUseCase:
    user_service: IUserService
    tokenizer: ITokenizerService

    def execute(self, refresh_token: str) -> TokenPair:
        decoded_token = self.tokenizer.verify_token(token=refresh_token, token_type=TokenType.REFRESH)

        user = self.user_service.get_user_by_email(decoded_token.sub)

        access_token = self.tokenizer.create_access_token(user)
        refresh_token = self.tokenizer.create_refresh_token(user)
        return TokenPair(access_token=access_token, refresh_token=refresh_token)
