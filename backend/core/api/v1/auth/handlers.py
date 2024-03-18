from http import HTTPStatus

from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError
from ninja.security import HttpBearer

from core.api.schemas import ApiResponse
from core.api.v1.auth.schemas import (
    CredentialSchema,
    TokenOutSchema,
)
from core.apps.common.exceptions import ServiceException
from core.apps.users.containers import get_container
from core.apps.users.exceptions.users import (
    UserInvalidCredentialsException,
    UserNotFoundException,
)
from core.apps.users.use_cases.auth.authenticate import AuthenticateUseCase
from core.apps.users.use_cases.tokens.get import GetTokenPairUseCase
from core.apps.users.use_cases.tokens.refresh import RefreshTokenUseCase


router = Router(tags=['Authorization'])


class AuthBearer(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str):
        container = get_container()
        use_case: AuthenticateUseCase = container.resolve(AuthenticateUseCase)

        try:
            user = use_case.execute(token)
        except ServiceException as e:
            raise HttpError(status_code=HTTPStatus.BAD_REQUEST, message=e.message)

        request.user = user
        return token


@router.post('login/', response={HTTPStatus.OK: ApiResponse[TokenOutSchema]})
def login(request: HttpRequest, credentials: CredentialSchema):
    container = get_container()
    use_case: GetTokenPairUseCase = container.resolve(GetTokenPairUseCase)

    try:
        tokens = use_case.execute(credentials.email, credentials.password)
    except UserInvalidCredentialsException as e:
        raise HttpError(status_code=HTTPStatus.UNAUTHORIZED, message=e.message)
    except UserNotFoundException as e:
        raise HttpError(status_code=HTTPStatus.NOT_FOUND, message=e.message)

    return ApiResponse(data=TokenOutSchema.from_entity(tokens))


@router.post('refresh/', response={HTTPStatus.OK: ApiResponse[TokenOutSchema]})
def refresh(request: HttpRequest, refresh_token: str):
    container = get_container()
    use_case: RefreshTokenUseCase = container.resolve(RefreshTokenUseCase)

    try:
        tokens = use_case.execute(refresh_token)
    except ServiceException as e:
        raise HttpError(status_code=HTTPStatus.BAD_REQUEST, message=e.message)

    return ApiResponse(data=TokenOutSchema.from_entity(tokens))
