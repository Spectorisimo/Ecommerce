from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from enum import Enum

from core.apps.common.enums import EntityStatus
from core.apps.products.entities.products import Product
from core.apps.users.entities.users import User


class ReviewRating(int, Enum):
    LOWEST = 1
    HIGHEST = 5


@dataclass
class Review:
    id: int | None = field(default=None, kw_only=True)  # noqa
    user: User | EntityStatus = field(default=EntityStatus.NOT_LOADED)
    product: Product | EntityStatus = field(default=EntityStatus.NOT_LOADED)

    text: str = field(default='')
    rating: ReviewRating = field(default=ReviewRating.LOWEST)

    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = field(default=None)
