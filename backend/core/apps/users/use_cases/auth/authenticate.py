from dataclasses import dataclass

from core.apps.users.entities.tokens import TokenType
from core.apps.users.entities.users import User
from core.apps.users.services.tokens import (
    ITokenizerService,
    ITokenValidatorService,
)
from core.apps.users.services.users import IUserService


@dataclass
class AuthenticateUseCase:
    user_service: IUserService
    tokenizer: ITokenizerService
    token_validator_service: ITokenValidatorService

    def execute(self, access_token: str) -> User:
        token_payload = self.tokenizer.decode_token(token=access_token)
        self.token_validator_service.validate(token_payload=token_payload, token_type=TokenType.ACCESS)
        user = self.user_service.get_user_by_email(token_payload.sub)
        return user
