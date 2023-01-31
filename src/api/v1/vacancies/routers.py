from rest_framework.routers import DefaultRouter
from .views import VacanciesWorker

router = DefaultRouter()
router.register("", VacanciesWorker, basename="vacancy-worker")
