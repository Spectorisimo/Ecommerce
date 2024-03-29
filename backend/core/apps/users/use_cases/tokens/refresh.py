from dataclasses import dataclass

from core.apps.users.entities.tokens import (
    TokenPair,
    TokenType,
)
from core.apps.users.services.tokens import (
    ITokenizerService,
    ITokenValidatorService,
)
from core.apps.users.services.users import IUserService


@dataclass
class RefreshTokenUseCase:
    user_service: IUserService
    tokenizer: ITokenizerService
    token_validator_service: ITokenValidatorService

    def execute(self, refresh_token: str) -> TokenPair:
        token = self.tokenizer.decode_token(encoded_token=refresh_token)
        self.token_validator_service.validate(token=token, token_type=TokenType.REFRESH)

        user = self.user_service.get_user_by_id(user_id=token.subject_id)
        access_token = self.tokenizer.create_access_token(user)
        refresh_token = self.tokenizer.create_refresh_token(user)
        return TokenPair(access_token=access_token, refresh_token=refresh_token)
