from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from core.apps.products.entities.reviews import (
    Review as ReviewEntity,
    ReviewRating,
)
from core.apps.products.exceptions.reviews import (
    ReviewInvalidRating,
    SingleReviewError,
)
from core.apps.products.repositories.reviews import IReviewRepository


class IReviewServices(ABC):

    @abstractmethod
    def create_review(self, review: ReviewEntity) -> ReviewEntity: ...

    @abstractmethod
    def check_review_exists(self, review: ReviewEntity) -> bool: ...


@dataclass
class ReviewServices(IReviewServices):
    review_repository: IReviewRepository

    def create_review(self, review: ReviewEntity) -> ReviewEntity:
        return self.review_repository.create_review(review=review)

    def check_review_exists(self, review: ReviewEntity) -> bool:
        return self.review_repository.check_review_exists(review=review)


class IReviewValidatorService(ABC):
    def validate(self, review: ReviewEntity) -> None:
        ...


class ReviewRatingValidatorService(IReviewValidatorService):
    def validate(self, review: ReviewEntity) -> None:
        if not (ReviewRating.LOWEST <= review.rating <= ReviewRating.HIGHEST):
            raise ReviewInvalidRating(rating=review.rating)


@dataclass
class SingleReviewValidatorService(IReviewValidatorService):
    review_service: IReviewServices

    def validate(self, review: ReviewEntity) -> None:
        if self.review_service.check_review_exists(review=review):
            raise SingleReviewError(product_id=review.product.id, user_id=review.user.id)


@dataclass
class ComposedReviewValidatorService(IReviewValidatorService):
    validators: list[IReviewValidatorService]

    def validate(self, review: ReviewEntity) -> None:
        for validator in self.validators:
            validator.validate(review=review)
