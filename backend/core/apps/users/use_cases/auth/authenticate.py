from dataclasses import dataclass

from core.apps.users.entities.tokens import TokenType
from core.apps.users.entities.users import User
from core.apps.users.services.tokens import ITokenizerService
from core.apps.users.services.users import IUserService


@dataclass
class AuthenticateUseCase:
    user_service: IUserService
    tokenizer: ITokenizerService

    def execute(self, access_token: str) -> User:
        token_payload = self.tokenizer.verify_token(token=access_token, token_type=TokenType.ACCESS)

        user = self.user_service.get_user_by_email(token_payload.sub)
        return user
