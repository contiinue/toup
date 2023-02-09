from rest_framework.routers import DefaultRouter
from .views import UserView, HHTokenView

router = DefaultRouter()
router.register("user", UserView, basename="user")
router.register("token", HHTokenView, basename="token")
