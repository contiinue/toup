from rest_framework.routers import DefaultRouter
from .views import UserView, TokenView

router = DefaultRouter()
router.register("user", UserView, basename="user")
router.register("token", TokenView, basename="token")
