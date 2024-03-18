from django.http import HttpRequest
from ninja import (
    Query,
    Router,
)

from core.api.filters import PaginationIn
from core.api.schemas import (
    ApiResponse,
    ListPaginatedResponse,
    PaginationOut,
)
from core.api.v1.products.filters import ProductFilters
from core.api.v1.products.schemas import (
    CreateProductSchema,
    ProductSchema,
)
from core.apps.products.containers.products import get_container
from core.apps.products.filters.products import ProductFilters as ProductFiltersEntity
from core.apps.products.services.products import IProductServices


router = Router(tags=['Products'])


@router.get('', response=ApiResponse[ListPaginatedResponse[ProductSchema]])
def get_product_list_handler(
        request: HttpRequest,
        filters: Query[ProductFilters],
        pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginatedResponse[ProductSchema]]:
    container = get_container()
    product_service: IProductServices = container.resolve(IProductServices)

    product_list = product_service.get_product_list(
        pagination=pagination_in,
        filters=ProductFiltersEntity(search=filters.search),
    )
    product_count = product_service.get_product_count(filters=filters)

    items = [ProductSchema.from_entity(product) for product in product_list]
    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=product_count,
    )

    return ApiResponse(
        data=ListPaginatedResponse(items=items, pagination=pagination_out),
    )


@router.post('', response={201: ApiResponse[ProductSchema]})
def create_product(
        request: HttpRequest,
        product: CreateProductSchema,
) -> ApiResponse[ProductSchema]:
    container = get_container()
    product_service: IProductServices = container.resolve(IProductServices)

    try:
        product = product_service.create_product(product.to_entity())
    except Exception as e:
        print(e)
    else:
        return ApiResponse(
            data=ProductSchema.from_entity(product),
        )
