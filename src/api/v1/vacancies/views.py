from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from .serializers import VacancyWorkerSerializer
from .vacancies_worker import start_or_stop_worker


class VacanciesWorker(ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(methods=["post"], request_body=VacancyWorkerSerializer)
    @action(methods=["post"], detail=False)
    def worker(self, request):
        serializer = VacancyWorkerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return start_or_stop_worker(request.user.pk, serializer.validated_data)
