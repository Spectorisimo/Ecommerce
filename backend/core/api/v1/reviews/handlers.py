from http import HTTPStatus

from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from core.api.schemas import ApiResponse
from core.api.v1.auth.handlers import AuthBearer
from core.api.v1.reviews.schemas import (
    ReviewInSchema,
    ReviewOutSchema,
)
from core.apps.common.exceptions import ServiceException
from core.apps.products.containers.reviews import get_container
from core.apps.products.exceptions.products import ProductNotFoundException
from core.apps.products.use_cases.reviews.create import CreateReviewUseCase


router = Router(tags=['Reviews'])


@router.post('{product_id}/reviews', response={HTTPStatus.CREATED: ApiResponse[ReviewOutSchema]}, auth=AuthBearer())
def create_review(request: HttpRequest, product_id: int, schema: ReviewInSchema) -> ApiResponse[ReviewOutSchema]:
    container = get_container()
    use_case: CreateReviewUseCase = container.resolve(CreateReviewUseCase)
    try:
        result = use_case.execute(
            product_id=product_id,
            user=request.user,
            review=schema.to_entity(),
        )

    except ProductNotFoundException as e:
        raise HttpError(status_code=HTTPStatus.NOT_FOUND, message=e.message)
    except ServiceException as e:
        raise HttpError(status_code=HTTPStatus.BAD_REQUEST, message=e.message)

    return ApiResponse(data=ReviewOutSchema.from_entity(result))
