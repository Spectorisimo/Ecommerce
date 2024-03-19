from dataclasses import dataclass

from core.apps.users.entities.tokens import TokenPair
from core.apps.users.services.tokens import (
    ITokenizerService,
    ITokenService,
)
from core.apps.users.services.users import IUserService


@dataclass
class GetTokenPairUseCase:
    user_service: IUserService
    tokenizer: ITokenizerService
    token_service: ITokenService

    def execute(self, email: str, password: str) -> TokenPair:
        user = self.user_service.get_user_by_email(email=email)
        self.user_service.compare_passwords(given_password=password, user_password=user.password)

        access_token = self.tokenizer.create_access_token(user)
        refresh_token = self.tokenizer.create_refresh_token(user)

        self.token_service.save_token(refresh_token=self.tokenizer.decode_token(encoded_token=refresh_token))
        return TokenPair(access_token=access_token, refresh_token=refresh_token)
