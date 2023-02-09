from django.db.models import Count, F, Q
from django.forms import model_to_dict
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import NotificationSerializer
from models.models import Notification
from ..vacancies.serializers import VacancySerializer


class NotificationView(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=["get"], detail=True)
    def vacancies_by_notification(self, request, pk):
        vacancies_by_notification = self.get_object().vacancies.all()
        serializer = VacancySerializer(
            data=[model_to_dict(i) for i in vacancies_by_notification], many=True
        )
        serializer.is_valid(raise_exception=True)
        return Response(data={"vacancies": serializer.data})

    def filter_queryset(self, queryset):
        return (
            queryset.filter(user=self.request.user)
            .annotate(
                valid_requests=Count(
                    "vacancies", filter=Q(vacancies__vacanciesinfo__is_request=True)
                ),
                invalid_requests=Count(
                    "vacancies", filter=Q(vacancies__vacanciesinfo__is_request=False)
                ),
            )
            .order_by("-date_create")
        )
