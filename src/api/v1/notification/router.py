from rest_framework.routers import DefaultRouter
from .views import NotificationView


router = DefaultRouter()
router.register("", NotificationView)
