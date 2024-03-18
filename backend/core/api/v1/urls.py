from ninja import Router

from core.api.v1.auth.handlers import router as auth_router
from core.api.v1.products.handlers import router as product_router
from core.api.v1.reviews.handlers import router as reviews_router


router = Router(tags=['v1'])
router.add_router('products/', product_router)
router.add_router('auth/', auth_router)
router.add_router('reviews/', reviews_router)
