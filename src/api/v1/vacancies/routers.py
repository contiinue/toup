from rest_framework.routers import DefaultRouter
from .views import VacanciesWorker, VacanciesView

router = DefaultRouter()
router.register("", VacanciesWorker, basename="vacancy-worker")
router.register("", VacanciesView, basename="vacancy")
