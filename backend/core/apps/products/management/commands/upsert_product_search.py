from typing import Any

from django.core.management import BaseCommand

from core.apps.products.containers.search import get_container
from core.apps.products.use_cases.search.upsert_search_data import UpsertSearchDataUseCase


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        container = get_container()

        use_case: UpsertSearchDataUseCase = container.resolve(UpsertSearchDataUseCase)
        use_case.execute()
