from django.urls import path, include

urlpatterns = [
    path("auth/", include("api.v1.user.urls")),
    path("vacancies/", include("api.v1.vacancies.urls")),
]
