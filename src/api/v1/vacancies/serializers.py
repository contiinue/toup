from rest_framework import serializers
from django_celery_beat.models import PeriodicTask
from models.models import Vacancy


class WorkerSerializer(serializers.Serializer):
    do_choice = (("start", "Start Worker"), ("stop", "Stop Worker"))
    do = serializers.ChoiceField(choices=do_choice)
    interval = serializers.IntegerField(required=False)


class WorkerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = ("enabled", "interval")


class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = "__all__"
