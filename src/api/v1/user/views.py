import json

from django.contrib.auth import login
from drf_yasg.utils import swagger_auto_schema
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from user.models import User, AuthHH
from .serializers import UserSerializer, AuthHHSerializer
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class UserView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @swagger_auto_schema(methods=["post"], request_body=AuthHHSerializer)
    @action(methods=["post"], detail=False)
    def connect_hh_tokens(self, request):
        serializer = AuthHHSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(data=serializer.validated_data, status=HTTP_201_CREATED)

    def perform_create(self, serializer):
        model = serializer.save()
        if isinstance(model, User):
            login(self.request, model)

        elif isinstance(model, AuthHH):
            self.request.user.auth_hh = model
            self.request.user.save()

    @staticmethod
    def create_task(user_id):
        interval = IntervalSchedule.objects.create(period="hours", every=5)
        PeriodicTask.objects.create(
            task="api.v1.vacancies.tasks.task_to_get_vacancies",
            interval=interval,
            kwargs=json.dumps({"user_id": user_id}),
        )
