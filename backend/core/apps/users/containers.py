from functools import lru_cache

import punq

from core.apps.users.repositories.users import (
    IUserRepository,
    UserRepository,
)
from core.apps.users.services.tokens import (
    ComposedTokenValidatorService,
    ITokenizerService,
    ITokenValidatorService,
    TokenExpiryValidatorService,
    TokenizerService,
    TokenTypeValidatorService,
)
from core.apps.users.services.users import (
    IUserService,
    UserService,
)
from core.apps.users.use_cases.auth.authenticate import AuthenticateUseCase
from core.apps.users.use_cases.tokens.get import GetTokenPairUseCase
from core.apps.users.use_cases.tokens.refresh import RefreshTokenUseCase


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()

    container.register(IUserRepository, UserRepository)

    container.register(IUserService, UserService)
    container.register(ITokenizerService, TokenizerService)

    container.register(TokenTypeValidatorService)
    container.register(TokenExpiryValidatorService)

    def build_validators() -> ITokenValidatorService:
        return ComposedTokenValidatorService(
            validators=[
                container.resolve(TokenTypeValidatorService),
                container.resolve(TokenExpiryValidatorService),
            ],
        )

    container.register(ITokenValidatorService, factory=build_validators)

    container.register(AuthenticateUseCase)
    container.register(GetTokenPairUseCase)
    container.register(RefreshTokenUseCase)

    return container
