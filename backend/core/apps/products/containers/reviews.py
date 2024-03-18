from functools import lru_cache
from logging import (
    getLogger,
    Logger,
)

import punq

from core.apps.products.repositories.products import (
    IProductRepository,
    ProductRepository,
)
from core.apps.products.repositories.reviews import (
    IReviewRepository,
    ReviewRepository,
)
from core.apps.products.services.products import (
    IProductServices,
    ProductServices,
)
from core.apps.products.services.reviews import (
    ComposedReviewValidatorService,
    IReviewServices,
    IReviewValidatorService,
    ReviewRatingValidatorService,
    ReviewServices,
    SingleReviewValidatorService,
)
from core.apps.products.use_cases.reviews.create import CreateReviewUseCase


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()

    container.register(Logger, factory=getLogger, name='django.request')

    container.register(IReviewRepository, ReviewRepository)
    container.register(IReviewServices, ReviewServices)

    container.register(SingleReviewValidatorService)
    container.register(ReviewRatingValidatorService)

    container.register(IProductRepository, ProductRepository)
    container.register(IProductServices, ProductServices)

    def build_validators() -> IReviewValidatorService:
        return ComposedReviewValidatorService(
            validators=[
                container.resolve(SingleReviewValidatorService),
                container.resolve(ReviewRatingValidatorService),
            ],
        )

    container.register(IReviewValidatorService, factory=build_validators)

    container.register(CreateReviewUseCase)

    return container
