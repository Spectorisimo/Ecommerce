from dataclasses import dataclass

from core.apps.products.entities.reviews import Review as ReviewEntity
from core.apps.products.services.products import IProductServices
from core.apps.products.services.reviews import (
    IReviewServices,
    IReviewValidatorService,
)
from core.apps.users.entities.users import User as UserEntity


@dataclass
class CreateReviewUseCase:
    review_service: IReviewServices
    product_service: IProductServices
    review_validator_service: IReviewValidatorService

    def execute(self, review: ReviewEntity, user: UserEntity, product_id: int) -> ReviewEntity:
        review.user = user
        review.product = self.product_service.get_product_by_id(product_id=product_id)

        self.review_validator_service.validate(review=review)
        saved_review = self.review_service.create_review(review=review)
        return saved_review
