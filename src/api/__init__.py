from src.api.admin.comments import router as admin_comment_router

# from api.admin.posts import router as post_router
# from api.admin.users import router as user_router
from src.api.public.comments import router as comment_router
from src.api.public.leads import router as lead_router

# from api.public.categories import router as categories_router
# from api.public.health import router as health_router
# from api.public.posts import router as posts_router
# from api.public.users import router as profile_router

admin_routers = [
    admin_comment_router
    # admin_comment_router, post_router, category_router
]

public_routers = [
    comment_router,
    lead_router,
    # auth_router,
    # profile_router,
    # posts_router,
    # categories_router,
]
