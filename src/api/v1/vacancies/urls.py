from django.urls import path, include
from .routers import router

urlpatterns = [path("vacancy/", include(router.urls))]
