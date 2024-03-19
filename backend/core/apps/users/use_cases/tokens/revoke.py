from dataclasses import dataclass

from core.apps.users.entities.tokens import TokenType
from core.apps.users.services.tokens import (
    ITokenizerService,
    ITokenService,
    ITokenValidatorService,
)


@dataclass
class RevokeTokenUseCase:
    token_service: ITokenService
    tokenizer: ITokenizerService
    token_validator_service: ITokenValidatorService

    def execute(self, refresh_token: str) -> None:
        token = self.tokenizer.decode_token(encoded_token=refresh_token)
        self.token_validator_service.validate(token=token, token_type=TokenType.REFRESH)
        self.token_service.revoke_token(jti=token.jti)
