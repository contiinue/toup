from django.urls import path, include

urlpatterns = [
    path("", include("api.v1.user.urls")),
    path("", include("api.v1.vacancies.urls")),
    path("", include("api.v1.notification.urls")),
]
