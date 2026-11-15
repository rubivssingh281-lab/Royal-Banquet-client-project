from backend.app.routers.auth import router as auth_router
from backend.app.routers.availability import router as availability_router
from backend.app.routers.blog import router as blog_router
from backend.app.routers.inquiries import router as inquiries_router
from backend.app.routers.testimonials import router as testimonials_router
from backend.app.routers.venues import router as venues_router

__all__ = [
    "inquiries_router",
    "venues_router",
    "availability_router",
    "testimonials_router",
    "blog_router",
    "auth_router",
]
