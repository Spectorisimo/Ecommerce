from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from decimal import Decimal


@dataclass
class Product:
    id: int | None = field(default=None, kw_only=True)  # noqa

    title: str
    description: str
    additional_data: dict
    amount: Decimal
    is_active: bool = field(default=True)

    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = field(default=None)
