from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from django_celery_beat.models import PeriodicTask
from .serializers import WorkerSerializer, VacancySerializer, WorkerInfoSerializer
from .vacancies_worker import start_or_stop_worker


class VacanciesWorker(ViewSet, GenericAPIView):
    permission_classes = [IsAuthenticated]

    @action(methods=["get"], detail=False)
    def stats_worker(self, request):
        try:
            data = PeriodicTask.objects.get(name=f"Task for: User{request.user.pk}")
        except ObjectDoesNotExist:
            return Response(
                data={"message": "not exist"}, status=status.HTTP_204_NO_CONTENT
            )

        serializer = WorkerInfoSerializer(data=model_to_dict(data))
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(methods=["post"], request_body=WorkerSerializer)
    @action(methods=["post"], detail=False)
    def worker(self, request):
        serializer = WorkerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return start_or_stop_worker(request.user.pk, serializer.validated_data)


class VacanciesView(ModelViewSet):
    serializer_class = VacancySerializer

    def filter_queryset(self, queryset):
        queryset.filter(user=self.request.user)
