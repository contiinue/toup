from django.urls import include, path
from .router import router

urlpatterns = [path("notification/", include(router.urls))]
