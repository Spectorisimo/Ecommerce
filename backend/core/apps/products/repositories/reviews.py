from abc import (
    ABC,
    abstractmethod,
)

from core.apps.products.entities.reviews import Review as ReviewEntity
from core.apps.products.models.reviews import Review


class IReviewRepository(ABC):

    @abstractmethod
    def create_review(self, review: ReviewEntity) -> ReviewEntity: ...

    @abstractmethod
    def check_review_exists(self, review: ReviewEntity) -> bool: ...


class ReviewRepository(IReviewRepository):

    def create_review(self, review: ReviewEntity) -> ReviewEntity:
        review_dto = Review.from_entity(review)
        review_dto.save()
        return review_dto.to_entity()

    def check_review_exists(self, review: ReviewEntity) -> bool:
        return Review.objects.filter(product_id=review.product.id, user_id=review.user.id).exists()
