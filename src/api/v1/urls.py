<<<<<<< HEAD
from django.urls import include

urlpatterns = [

]
=======
from django.urls import path, include

urlpatterns = [path("", include("api.v1.vacancies.urls"))]
>>>>>>> vacancies
