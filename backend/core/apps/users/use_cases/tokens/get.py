from dataclasses import dataclass

from core.apps.users.entities.tokens import TokenPair
from core.apps.users.services.tokens import ITokenizerService
from core.apps.users.services.users import IUserService


@dataclass
class GetTokenPairUseCase:
    user_service: IUserService
    tokenizer: ITokenizerService

    def execute(self, email: str, password: str) -> TokenPair:
        user = self.user_service.get_user_by_email(email)
        self.user_service.compare_passwords(given_password=password, user_password=user.password)
        access_token = self.tokenizer.create_access_token(user)
        refresh_token = self.tokenizer.create_refresh_token(user)
        return TokenPair(access_token=access_token, refresh_token=refresh_token)
