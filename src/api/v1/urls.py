from django.urls import path, include

urlpatterns = [
    path("user/", include("api.v1.user.urls")),
    path("vacancy/", include("api.v1.vacancies.urls")),
]
